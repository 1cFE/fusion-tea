"""Package-owned whole-plant-conversion stored execution through stock TEAx APIs (the ARIES route with this package's names; no plant arithmetic)."""
from __future__ import annotations
import json
import importlib
import math
from pathlib import Path
from scripts.study import common, identity

HERE = Path(__file__).resolve().parent
E2E = HERE.parent
REPO_ROOT = E2E.parent.parent
PACKAGE_NAME = "whole_plant_conversion_tea"
PACKAGE_DIR = E2E / "whole_plant_conversion_tea"
MANIFEST_PATH = HERE / "manifest.json"
INTERFACE_MODULE = "exploration.whole_plant_conversion.studies.interface_data"
BASELINE_RESULT_SCHEMA_VERSION = "study-baseline-result/v1"


def interface():
    """Read the reviewed package interface; absence prevents premature execution."""
    try:
        document = importlib.import_module(INTERFACE_MODULE).INTERFACE
    except (ImportError, AttributeError) as exc:
        raise RouteError("reviewed interface_data.py is absent or incomplete") from exc
    if not isinstance(document, dict):
        raise RouteError("reviewed study interface must be a mapping")
    for name in ("executable_fingerprint", "semantic_fingerprint"):
        if not isinstance(document.get(name), str) or not document[name]:
            raise RouteError(f"reviewed interface requires {name}")
    for name in ("entry_keys", "channels", "constraints"):
        mapping = document.get(name)
        if not isinstance(mapping, dict) or not mapping:
            raise RouteError(f"interface requires a nonempty {name} map")
        if any(not isinstance(k, str) or not k or not isinstance(v, str) or not v
               for k, v in mapping.items()):
            raise RouteError(f"interface {name} must map nonempty strings")
    return document


class RouteError(ValueError):
    """The requested whole-plant-conversion execution cannot supply its declared evidence."""


def validate_proposal(raw):
    """Refuse unknown keys and nonfinite/non-numeric proposals before execution."""
    if set(raw) != set(interface()["entry_keys"]):
        return None
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v)
           for v in raw.values()):
        return None
    return {key: float(value) for key, value in raw.items()}


def spec_path(package_dir: Path) -> Path:
    """The package's one pipeline spec, found rather than named."""
    specs = sorted((Path(package_dir) / "pipelines").glob("*.yaml"))
    if len(specs) != 1:
        raise RouteError(f"expected exactly one pipeline spec under {package_dir}, found {specs}")
    return specs[0]


def package_loader(package_dir: Path, link_root: Path):
    """The stock strict loader. The verifier forbids a symlink as the package root, so
    both paths are resolved; ``link_root`` is the caller's because the loader writes an
    import symlink into it, and a default under the package would dirty the tree the
    cleanliness gate watches."""
    from simkit.evaluation.package_load import ProvisionalPackageLoader

    return ProvisionalPackageLoader(
        package_dir=Path(package_dir).resolve(),
        package_name=PACKAGE_NAME,
        link_root=Path(link_root).resolve(),
        strict=True,
    )


def prepare(package_dir: Path, work_dir: Path):
    """Load through the stock loader and prepare the evaluator once.

    ``expects_constraint_report`` is read from the embedded model contract through
    teax's own consumer-side authority, never guessed from the pipeline spec.
    """
    from simkit.evaluation.evaluator import PreparedEvaluator
    from simkit.study.model_contract import load_model_contract, ships_constraint_report

    contract = load_model_contract(Path(package_dir).resolve())
    prepared = PreparedEvaluator(
        package_loader(package_dir, Path(work_dir) / "pkg_link"),
        spec_path(package_dir),
        expects_constraint_report=ships_constraint_report(contract),
    )
    expected = interface()
    if prepared.fingerprint != expected["executable_fingerprint"]:
        raise RouteError("prepared executable differs from reviewed interface identity")
    if contract.semantic_fingerprint != expected["semantic_fingerprint"]:
        raise RouteError("model semantics differ from reviewed interface identity")

    actual = {key: channel for channel, model in prepared.entry_models.items()
              for key in model.model_fields}
    if actual != interface()["entry_keys"]:
        raise RouteError("prepared entry mapping differs from reviewed interface")
    _export_catalog(package_dir)
    return prepared


def definition(study_id: str, prepared, proposals, package_dir: Path):
    from simkit.study.definition import StudyDefinition
    from simkit.study.identity import digest_of
    from simkit.study.model_contract import load_model_contract
    from simkit.study.policy import ObjectivePolicy
    from simkit.study.strategy import PreparedListStrategy

    return StudyDefinition(
        study_id=study_id,
        entry_models=prepared.entry_models,
        strategy=PreparedListStrategy(proposals),
        validate_proposal=validate_proposal,
        policy=ObjectivePolicy(objectives=(), response_roles={}),
        executable_fingerprint=prepared.fingerprint,
        # The contract's published semantic fingerprint, as teax's own builder binds it:
        # a store never silently rebinds across a model-meaning change.
        model_contract_fingerprint=load_model_contract(
            Path(package_dir).resolve()
        ).semantic_fingerprint,
        input_schema_version="input-v1",
        evidence_schema_version=prepared.EVIDENCE_SCHEMA_VERSION,
        study_definition_fingerprint=digest_of(
            {"proposals": [sorted(p.items()) for p in proposals], "interface": interface()}
        ),
    )


class _RequiredOutputsEvaluator:
    """Validate successful evidence without intercepting the runner's failure handling."""

    def __init__(self, prepared, channels, catalog):
        self.prepared = prepared
        self.channels = channels
        self.catalog = catalog

    def evaluate(self, typed_inputs):
        evidence = self.prepared.evaluate(typed_inputs)
        require_published(evidence, self.channels)
        actual = set(evidence.responses) - {"headline"}
        if actual != set(self.catalog):
            raise RouteError(f"evaluation constraint publication differs: {actual}")
        return evidence


def run_points(
    study_id: str, proposals, work_dir: Path, package_dir: Path = PACKAGE_DIR,

):
    """Execute proposals through `StudyRunner`. Returns (cases, db path).

    Every declared column must be published: existing completed cases are checked under
    the lease, new evidence before it is persisted. Nonfinite model outputs remain in
    stored evidence. The store is left on disk so incompatible evidence
    cannot silently replace it.
    """
    from simkit.study.query import StudyQuery
    from simkit.study.runner import StudyRunner
    from simkit.study.store import StudyStore

    work_dir = Path(work_dir)
    proposals = list(proposals)
    if any(validate_proposal(point) is None for point in proposals):
        raise RouteError("each proposal must supply the complete finite numeric entry map")
    if not proposals:
        raise RouteError("cannot run a study with no proposals")
    required_channels = interface()["channels"]
    if not required_channels:
        raise RouteError("a study must declare required result channels")
    work_dir.mkdir(parents=True, exist_ok=True)
    prepared = prepare(package_dir, work_dir)
    study = definition(study_id, prepared, proposals, package_dir)
    db = work_dir / f"{study_id}.db"
    store = StudyStore.create_or_open(db, study.compatibility())
    try:
        store.acquire_lease()
        try:
            for case in StudyQuery(store, Path(package_dir).resolve()).cases():
                if case.state == "completed":
                    require_published(case, required_channels)
                    short_verdicts(case, package_dir)
            StudyRunner(store, study, _RequiredOutputsEvaluator(prepared, required_channels, _export_catalog(package_dir))).run()
        finally:
            store.release_lease()
    finally:
        store.close()
    reopened = StudyStore(db)
    try:
        cases = StudyQuery(reopened, Path(package_dir).resolve()).cases()
    finally:
        reopened.close()
    for case in cases:
        if case.state == "completed":
            require_published(case, required_channels)
            short_verdicts(case, package_dir)
    return cases, db


def write_identity_document(package_dir: Path, out_path: Path) -> Path:
    """The sealed identity: the route bypassed nothing, so the digest *is* the fingerprint."""
    return common.write_document(
        identity.build_sealed(package_name=PACKAGE_NAME, package_root=Path(package_dir)),
        out_path,
    )


def _export_catalog(package_dir: Path) -> dict[str, dict]:
    catalog = _catalog_by_constraint_id(package_dir)
    actual = {key: value.get("source_local_identity") for key, value in catalog.items()}
    if actual != interface()["constraints"]:
        raise RouteError(f"constraint identities differ from reviewed interface: {actual}")
    identities = [entry.get("source_local_identity") for entry in catalog.values()]
    if any(not isinstance(identity, str) or not identity for identity in identities):
        raise RouteError("every catalogued check must have a source_local_identity")
    return catalog


def _short_verdicts(case, catalog: dict[str, dict]) -> dict[str, str]:
    expected = set(catalog)
    actual = set(case.verdicts)
    if actual != expected:
        missing = sorted(expected - actual)
        unexpected = sorted(actual - expected)
        raise RouteError(
            "case verdicts do not match the emitted constraint catalog: "
            f"missing={missing}, unexpected={unexpected}"
        )
    return {constraint_id: case.verdicts[constraint_id] for constraint_id in sorted(catalog)}


def short_verdicts(case, package_dir: Path = PACKAGE_DIR) -> dict[str, str]:
    """Keep complete IDs: reused definitions can have duplicate local names."""
    return _short_verdicts(case, _export_catalog(package_dir))


def require_published(case, channels: dict[str, str]) -> None:
    """Refuse evidence that lacks a declared column. Absent, null and nonnumeric values are tooling omissions. Nonfinite numeric
    values remain available as evidence of model-domain failures."""
    missing = [
        f"{name} ({channel})"
        for name, channel in channels.items()
        if channel not in case.outputs
        or isinstance(case.outputs[channel], bool)
        or not isinstance(case.outputs[channel], (int, float))
    ]
    if missing:
        raise RouteError(f"case is missing required result channels: {missing}")


def _completed(cases, what: str):
    completed = [c for c in cases if c.state == "completed"]
    if len(completed) != len(cases):
        raise RouteError(
            f"{what}: {len(cases) - len(completed)} of {len(cases)} cases did not complete"
        )
    return completed


def _catalog_by_constraint_id(package_dir: Path) -> dict[str, dict]:
    contract = json.loads((Path(package_dir) / "contracts" / "model_contract.json").read_text())
    entries = contract["constraint_catalog"]["concrete_entries"]
    catalog = {e["constraint_id"]: e for e in entries}
    if len(catalog) != len(entries):
        raise RouteError("duplicate constraint IDs in emitted catalog")
    return catalog


def _baseline_point(manifest_path: Path) -> dict[str, float]:
    return dict(json.loads(Path(manifest_path).read_text())["baseline"]["point"])


def execute_baseline(
    out_dir: Path,
    *,
    package_dir: Path = PACKAGE_DIR,
    manifest_path: Path = MANIFEST_PATH,
) -> dict[str, Path]:
    """Load the route and execute the manifest's pinned baseline point.

    Deposits `package_identity.json` and `baseline_result.json` into ``out_dir``: the
    runbook's route-preparation step (step 5), and the only producer of the two
    documents preflight's identity and baseline gates consume.
    """
    out_dir = Path(out_dir)
    point = _baseline_point(manifest_path)
    cases, db = run_points("whole-plant-conversion-baseline-point-v1", [point], out_dir / "_work", package_dir)
    case = _completed(cases, "baseline point")[0]
    catalog = _catalog_by_constraint_id(package_dir)

    identity_path = write_identity_document(package_dir, out_dir / "package_identity.json")
    result = {
        "schema_version": BASELINE_RESULT_SCHEMA_VERSION,
        "executed_under": {
            "identity_digest": case.executable_fingerprint,
            "store_id": common.manifest_mod.repo_relative_posix(db)
            if db.resolve().is_relative_to(REPO_ROOT) else db.name,
            "case_id": case.candidate_id,
        },
        "point": {key: float(value) for key, value in sorted(point.items())},
        "channels": {key: float(value) for key, value in sorted(case.outputs.items())},
        "verdicts": [
            {
                "constraint_id": constraint_id,
                "definition_qualified_name": catalog[constraint_id]["definition_qualified_name"],
                "source_local_identity": catalog[constraint_id]["source_local_identity"],
                "status": status,
            }
            for constraint_id, status in sorted(case.verdicts.items())
        ],
    }
    result_path = common.write_document(result, out_dir / "baseline_result.json")
    return {"identity": identity_path, "baseline_result": result_path}
