"""Package-owned IFE stored execution through stock TEAx APIs."""
from __future__ import annotations
import json
import math
from pathlib import Path
from scripts.study import common, identity
from exploration.ife_e2e.eligibility import price_eligible
from exploration.ife_e2e.studies.oracle_entry import ENTRY_KEYS

HERE = Path(__file__).resolve().parent
E2E = HERE.parent
REPO_ROOT = E2E.parent.parent
PACKAGE_NAME = "ife_tea"
PACKAGE_DIR = E2E / "generated"
MANIFEST_PATH = HERE / "manifest.json"
P = "hif_plant_pkg__hif_plant__"
BASELINE_RESULT_SCHEMA_VERSION = "study-baseline-result/v1"
EXPECTED_CONSTRAINT_COUNT = 2
CHANNELS = {'lcoe_calc__energy_on_target': 'hif_plant_pkg__hif_plant__lcoe_calc__energy_on_target',
 'pv_factors__construction_factor': 'hif_plant_pkg__hif_plant__pv_factors__construction_factor',
 'pv_factors__operation_factor': 'hif_plant_pkg__hif_plant__pv_factors__operation_factor',
 'lcoe_calc__fusion_energy_per_shot': 'hif_plant_pkg__hif_plant__lcoe_calc__fusion_energy_per_shot',
 'lcoe_calc__fusion_power': 'hif_plant_pkg__hif_plant__lcoe_calc__fusion_power',
 'lcoe_calc__thermal_power': 'hif_plant_pkg__hif_plant__lcoe_calc__thermal_power',
 'lcoe_calc__thermal_power_gw': 'hif_plant_pkg__hif_plant__lcoe_calc__thermal_power_gw',
 'lcoe_calc__gross_electric_power': 'hif_plant_pkg__hif_plant__lcoe_calc__gross_electric_power',
 'lcoe_calc__driver_electric_power': 'hif_plant_pkg__hif_plant__lcoe_calc__driver_electric_power',
 'lcoe_calc__other_parasitic_power': 'hif_plant_pkg__hif_plant__lcoe_calc__other_parasitic_power',
 'lcoe_calc__net_electric_power': 'hif_plant_pkg__hif_plant__lcoe_calc__net_electric_power',
 'lcoe_calc__net_electric_power_gw': 'hif_plant_pkg__hif_plant__lcoe_calc__net_electric_power_gw',
 'lcoe_calc__driver_recirculating_fraction': 'hif_plant_pkg__hif_plant__lcoe_calc__driver_recirculating_fraction',
 'lcoe_calc__total_recirculating_fraction': 'hif_plant_pkg__hif_plant__lcoe_calc__total_recirculating_fraction',
 'lcoe_calc__shots_per_year': 'hif_plant_pkg__hif_plant__lcoe_calc__shots_per_year',
 'lcoe_calc__driver_lifetime_years': 'hif_plant_pkg__hif_plant__lcoe_calc__driver_lifetime_years',
 'lcoe_calc__driver_capital_cost': 'hif_plant_pkg__hif_plant__lcoe_calc__driver_capital_cost',
 'lcoe_calc__annual_driver_replacement_cost': 'hif_plant_pkg__hif_plant__lcoe_calc__annual_driver_replacement_cost',
 'lcoe_calc__discounted_cost': 'hif_plant_pkg__hif_plant__lcoe_calc__discounted_cost',
 'lcoe_calc__discounted_energy': 'hif_plant_pkg__hif_plant__lcoe_calc__discounted_energy',
 'driver__meier_cost__bank_energy_joules': 'hif_plant_pkg__hif_plant__driver__meier_cost__bank_energy_joules',
 'driver__meier_cost__cost_billions': 'hif_plant_pkg__hif_plant__driver__meier_cost__cost_billions',
 'driver__meier_cost__gamma': 'hif_plant_pkg__hif_plant__driver__meier_cost__gamma',
 'meier_reactor_cost_calc__reactor_cost_billions': 'hif_plant_pkg__hif_plant__meier_reactor_cost_calc__reactor_cost_billions',
 'meier_capital_calc__total_capital_billions': 'hif_plant_pkg__hif_plant__meier_capital_calc__total_capital_billions',
 'meier_coe_calc__annualized_cost': 'hif_plant_pkg__hif_plant__meier_coe_calc__annualized_cost',
 'meier_coe_calc__energy_denominator': 'hif_plant_pkg__hif_plant__meier_coe_calc__energy_denominator',
 'recirc_calc__f_recirc': 'hif_plant_pkg__hif_plant__recirc_calc__f_recirc',
 'hawker_price__price': 'hif_plant_pkg__hif_plant__hawker_price__price',
 'meier_price__price': 'hif_plant_pkg__hif_plant__meier_price__price',
 'hawker_price__generating': 'hif_plant_pkg__hif_plant__hawker_price__generating',
 'meier_price__generating': 'hif_plant_pkg__hif_plant__meier_price__generating'}


class RouteError(ValueError):
    """The requested IFE execution cannot supply its declared evidence."""


def validate_proposal(raw):
    """Refuse unknown keys and nonfinite/non-numeric proposals before execution."""
    if set(raw) - ENTRY_KEYS.keys():
        return None
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v)
           for v in raw.values()):
        return None
    return {key: float(value) for key, value in raw.items()}


def eligible_prices(case):
    """Return the two eligibility flags from stored price, generation and net evidence."""
    require_published(case, CHANNELS)
    verdicts = short_verdicts(case)
    return {name: price_eligible(case.outputs[P + name + "__price"],
                                case.outputs[P + name + "__generating"],
                                verdicts["net_positive"])
            for name in ("hawker_price", "meier_price")}


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
    return PreparedEvaluator(
        package_loader(package_dir, Path(work_dir) / "pkg_link"),
        spec_path(package_dir),
        expects_constraint_report=ships_constraint_report(contract),
    )


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
            {"proposals": [sorted(p.items()) for p in proposals]}
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
    if not proposals:
        raise RouteError("cannot run a study with no proposals")
    required_channels = CHANNELS
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
    if len(catalog) != EXPECTED_CONSTRAINT_COUNT:
        raise RouteError(
            f"expected exactly {EXPECTED_CONSTRAINT_COUNT} catalogued checks, "
            f"found {len(catalog)}"
        )
    identities = [entry.get("source_local_identity") for entry in catalog.values()]
    if any(not isinstance(identity, str) or not identity for identity in identities):
        raise RouteError("every catalogued check must have a source_local_identity")
    if len(set(identities)) != len(identities):
        raise RouteError(f"catalogued source_local_identity values are not unique: {identities}")
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
    by_identity = {
        catalog[constraint_id]["source_local_identity"]: status
        for constraint_id, status in case.verdicts.items()
    }
    return {identity: by_identity[identity] for identity in sorted(by_identity)}


def short_verdicts(case, package_dir: Path = PACKAGE_DIR) -> dict[str, str]:
    """Resolve verdict names through the emitted contract, never identifier text."""
    return _short_verdicts(case, _export_catalog(package_dir))


def require_published(case, channels: dict[str, str]) -> None:
    """Refuse evidence that lacks a declared column. An absent or null value is a tooling
    omission, never a result, so this is checked during execution."""
    missing = [
        f"{name} ({channel})"
        for name, channel in channels.items()
        if channel not in case.outputs or case.outputs[channel] is None
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
    return {e["constraint_id"]: e for e in contract["constraint_catalog"]["concrete_entries"]}


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
    cases, db = run_points("ife-baseline-point-v1", [point], out_dir / "_work", package_dir)
    case = _completed(cases, "baseline point")[0]
    catalog = _catalog_by_constraint_id(package_dir)

    identity_path = write_identity_document(package_dir, out_dir / "package_identity.json")
    result = {
        "schema_version": BASELINE_RESULT_SCHEMA_VERSION,
        "executed_under": {
            "identity_digest": case.executable_fingerprint,
            "store_id": common.manifest_mod.repo_relative_posix(db)
            if str(db).startswith(str(REPO_ROOT)) else db.name,
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
