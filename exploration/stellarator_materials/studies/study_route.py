"""Package-owned WI-100 route for the three stellarator material packages on stock TEAx (design section 5.3).

Carried over from exploration/stellarator_e2e/studies/study_route.py: the retired-key refusals (:184-189), the
numeric and Boolean typing of `validate_proposal` (:181-204) and the stock strict loader and runner (:207-335).

Changed for WI-100 (design section 5.3 and the probe P2 fallback, K21): codegen refuses a package holding two or more
instances of 'MFE Power Plant', so the design's three instances are three packages built from one staged source set
(exploration/stellarator_materials/build.py). A study case names one unit and evaluates exactly one plant:

  reference  the staged, unchanged Stellaris instance; pinned, so a proposal may only restate its baseline point
  rebco      stellarator_09_materials__rebco_material__...
  nb3sn      stellarator_09_materials__nb3sn_material__...

Refusals (design section 5.3; K6, K11): a key outside the unit's generated entry map (which includes every key of the
other two units); any reference key whose value differs from the pinned baseline; under a material unit
`magnet__rebco_law_enabled` or `cryoplant__inventory_enabled` (final in the variants; probe P3 found both emitted);
an Nb3Sn proposal without `magnet__conductor__eps_intrinsic_in` (a negative design literal is not an entry point, so the
case must supply it). No bypass switch (D8): tests that must set a pinned or final key use `prepare()` and the stock
evaluator directly.

What the split removes (prototype/P2-double-retype.md): with one plant per case the unselected material instance does not
run, so the design's D4 fill-and-witness has nothing to witness, and the reference is not re-run on every case; its
parity with the pin is `reference_parity`, run by the build regression, the reference baseline and the tests.

Flags are study-side (contract section 7; coordinator amendment A4): `material_flags` derives them from published
channels. Statuses that need the offer policy's search (ignited, capacity-limited) are the study's, not the route's.

Teax is imported from STOP_PARSER_TEAX_ROOT by the caller (the sealed-runner contract); `simkit` is imported lazily.
"""
from __future__ import annotations

import atexit
import importlib
import json
import math
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGE_ROOT = HERE.parent
REPO_ROOT = PACKAGE_ROOT.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.study import common, identity  # noqa: E402

INTERFACE_MODULE = "exploration.stellarator_materials.studies.interface_data"
BASELINE_RESULT_SCHEMA_VERSION = "study-baseline-result/v1"
PIN_PATH = REPO_ROOT / "work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/integration/baseline.json"


@dataclass(frozen=True)
class Unit:
    name: str
    package_name: str
    prefix: str
    constraint_count: int

    @property
    def package_dir(self) -> Path:
        return PACKAGE_ROOT / "units" / self.name / self.package_name

    @property
    def manifest_path(self) -> Path:
        return HERE / self.name / "manifest.json"

    @property
    def baseline_dir(self) -> Path:
        return HERE / self.name / "baseline"


UNITS = {
    "reference": Unit("reference", "stellarator_materials_reference_tea", "stellarator_09__stellaris__", 67),
    "rebco": Unit("rebco", "stellarator_materials_rebco_tea", "stellarator_09_materials__rebco_material__", 73),
    "nb3sn": Unit("nb3sn", "stellarator_materials_nb3sn_tea", "stellarator_09_materials__nb3sn_material__", 73),
}
MATERIALS = ("rebco", "nb3sn")
FINAL_SUFFIXES = ("magnet__rebco_law_enabled", "cryoplant__inventory_enabled")  # K11
REQUIRED_SUFFIXES = {"nb3sn": ("magnet__conductor__eps_intrinsic_in",)}  # K6
RETIRED_MAGNET = ("coil__I_coil", "winding_pack__j_wp", "winding_pack__B_grade_ref", "winding_pack__field_exponent",
                  "winding_pack__sizing_mode", "winding_pack__inventory_multiplier", "c_support", "e_support",
                  "casing__m_casing_ref")
# The stellarator_e2e route's Boolean suffixes (study_route.py:124-179); the variants add K10's intercept flag.
E2E_BOOLEAN_SUFFIXES = frozenset((
    "buildings__facilities_enabled", "cryoplant__inventory_enabled", "fuel_cycle__inventory_enabled",
    "fuel_cycle__processing_enabled", "fuel_cycle__processing_source_conditions", "heat_transport__equipment_enabled",
    "cryoplant__cold_stage_capability__demand_available_in", "cryoplant__cryogenic_offered_conditions__enabled_in",
    "cryoplant__direct_electric_capability__applicable_in", "cryoplant__direct_electric_capability__conditions_supported_in",
    "cryoplant__direct_electric_capability__demand_available_in", "electric_plant__electric_gross_capability__applicable_in",
    "electric_plant__electric_gross_capability__conditions_supported_in",
    "electric_plant__electric_gross_capability__demand_available_in",
    "heat_rejection__water_electric_capability__demand_available_in", "heat_rejection__water_flow_capability__demand_available_in",
    "heat_rejection__water_head_capability__demand_available_in",
    "heat_rejection__water_rejection_capability__demand_available_in",
    "heat_transport__helium_electric_capability__demand_available_in",
    "heat_transport__helium_flow_capability__demand_available_in",
    "heat_transport__helium_pressure_rise_capability__demand_available_in",
    "heat_transport__helium_pumping_capability__demand_available_in",
    "heat_transport__salt_electric_capability__demand_available_in", "heat_transport__salt_flow_capability__demand_available_in",
    "heat_transport__salt_head_capability__demand_available_in", "heat_transport__salt_shaft_capability__demand_available_in",
    "power_supplies__magnet_pf_electric_capability__applicable_in",
    "power_supplies__magnet_pf_electric_capability__conditions_supported_in",
    "power_supplies__magnet_pf_electric_capability__demand_available_in",
    "power_supplies__magnet_tf_electric_capability__applicable_in",
    "power_supplies__magnet_tf_electric_capability__conditions_supported_in",
    "power_supplies__magnet_tf_electric_capability__demand_available_in",
    "turbine__condensate_electric_capability__demand_available_in", "turbine__condensate_flow_capability__demand_available_in",
    "turbine__condensate_pressure_rise_capability__demand_available_in",
    "turbine__condenser_rejection_capability__demand_available_in", "turbine__feedwater_electric_capability__demand_available_in",
    "turbine__feedwater_flow_capability__demand_available_in",
    "turbine__feedwater_pressure_rise_capability__demand_available_in", "turbine__hp_flow_capability__demand_available_in",
    "turbine__hp_shaft_capability__demand_available_in", "turbine__lp_flow_capability__demand_available_in",
    "turbine__lp_shaft_capability__demand_available_in", "turbine__turbine_gross_capability__applicable_in",
    "turbine__turbine_gross_capability__conditions_supported_in", "turbine__turbine_gross_capability__demand_available_in",
))
BOOLEAN_SUFFIXES = {"reference": E2E_BOOLEAN_SUFFIXES,
                    "rebco": E2E_BOOLEAN_SUFFIXES | {"cryoplant__intercept_demand_available"},
                    "nb3sn": E2E_BOOLEAN_SUFFIXES | {"cryoplant__intercept_demand_available"}}


class RouteError(Exception):
    """The route could not do what it was asked. Never a silent skip."""


def unit_of(name: str) -> Unit:
    if name not in UNITS:
        raise RouteError(f"unknown unit {name!r}; expected one of {sorted(UNITS)}")
    return UNITS[name]


def interface(name: str) -> dict:
    """The reviewed interface of one unit (written by prepare_interface.py); absence prevents execution."""
    try:
        document = importlib.import_module(INTERFACE_MODULE).INTERFACE["units"][name]
    except (ImportError, AttributeError, KeyError) as exc:
        raise RouteError(f"reviewed interface for unit {name!r} is absent") from exc
    for key in ("executable_fingerprint", "semantic_fingerprint", "entry_keys", "baseline_point", "constraints", "partition"):
        if not document.get(key):
            raise RouteError(f"interface for {name} requires {key}")
    return document


def boolean_keys(name: str) -> frozenset[str]:
    unit = unit_of(name)
    return frozenset(unit.prefix + suffix for suffix in BOOLEAN_SUFFIXES[name])


def assert_boolean_declarations(name: str, package_dir: Path | None = None) -> None:
    unit = unit_of(name)
    contract = json.loads((Path(package_dir or unit.package_dir) / "contracts/model_contract.json").read_text())
    declared = {p["qualified_name"] for p in contract["parameters"] if p["python_type"] == "bool"}
    if declared != boolean_keys(name):
        raise RouteError(f"{name}: Boolean declaration drift: {sorted(declared ^ boolean_keys(name))}")


def proposal_validator(name: str):
    """The unit's `validate_proposal`: typing as the stellarator_e2e route, plus the WI-100 refusals."""
    unit = unit_of(name)
    document = interface(name)
    entry_keys = set(document["entry_keys"])
    pinned = document["baseline_point"]
    booleans = boolean_keys(name)
    P = unit.prefix

    def validate_proposal(raw):
        if not isinstance(raw, dict):
            raise RouteError("proposal must be a mapping of entry keys to values")
        obsolete = sorted({P + "magnet__" + n for n in RETIRED_MAGNET}.intersection(raw))
        if obsolete:
            raise RouteError(f"retired magnet entry keys {obsolete}; migrate to supplied pack side, reference turns and masses")
        if P + "magnet__R0" in raw:
            raise RouteError(f"retired entry key {P}magnet__R0; use plant R")
        unknown = sorted(set(raw) - entry_keys)
        if unknown:
            other = sorted({u for u in unknown for other in UNITS.values() if other.name != name and u.startswith(other.prefix)})
            raise RouteError(f"{name}: keys outside this unit's entry map (one material per case; the reference is its own "
                             f"package): {other or unknown[:5]}")
        if name in MATERIALS:
            final = sorted(P + s for s in FINAL_SUFFIXES if P + s in raw)
            if final:
                raise RouteError(f"{name}: {final} are final in the variants (K11) and may not be proposed")
            missing = [P + s for s in REQUIRED_SUFFIXES.get(name, ()) if P + s not in raw]
            if missing:
                raise RouteError(f"{name}: proposal must supply {missing} (a negative design literal is not an entry point, K6)")
        out = {}
        for key, value in raw.items():
            if key in booleans:
                if isinstance(value, bool) or (isinstance(value, (int, float)) and value in (0, 1)):
                    out[key] = bool(value)
                else:
                    raise RouteError(f"{key}: Boolean value or numeric zero/one required")
            elif not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
                raise RouteError(f"{key}: finite numeric value required; Boolean values are not numeric controls")
            else:
                out[key] = float(value)
        if name == "reference":
            moved = sorted(k for k, v in out.items() if float(v) != float(pinned[k]))
            if moved:
                raise RouteError(f"reference: the reference instance is pinned; {moved[:5]} differ from its baseline point")
        return out

    return validate_proposal


def spec_path(package_dir: Path) -> Path:
    specs = sorted((Path(package_dir) / "pipelines").glob("*.yaml"))
    if len(specs) != 1:
        raise RouteError(f"expected exactly one pipeline spec under {package_dir}, found {specs}")
    return specs[0]


def package_loader(name: str, package_dir: Path, link_root: Path):
    """The stock strict loader; `link_root` is the caller's so the loader's import symlink stays out of the package."""
    from simkit.evaluation.package_load import ProvisionalPackageLoader

    return ProvisionalPackageLoader(package_dir=Path(package_dir).resolve(), package_name=unit_of(name).package_name,
                                    link_root=Path(link_root).resolve(), strict=True)


def prepare_unchecked(name: str, package_dir: Path | None = None):
    """Load through the stock loader and prepare the evaluator, without the reviewed-interface identity checks.
    Only interface discovery (prepare_interface.py) uses this directly; execution goes through `prepare`."""
    from simkit.evaluation.evaluator import PreparedEvaluator
    from simkit.study.model_contract import load_model_contract, ships_constraint_report

    package_dir = Path(package_dir or unit_of(name).package_dir)
    contract = load_model_contract(package_dir.resolve())
    link_root = Path(tempfile.mkdtemp(prefix="fusion-tea-imports-"))
    atexit.register(shutil.rmtree, link_root, ignore_errors=True)
    prepared = PreparedEvaluator(package_loader(name, package_dir, link_root), spec_path(package_dir),
                                 expects_constraint_report=ships_constraint_report(contract))
    return prepared, contract


def prepare(name: str, package_dir: Path | None = None):
    """Prepare the evaluator once and check it against the reviewed interface identity and entry map."""
    prepared, contract = prepare_unchecked(name, package_dir)
    expected = interface(name)
    if prepared.fingerprint != expected["executable_fingerprint"]:
        raise RouteError(f"{name}: prepared executable differs from the reviewed interface identity")
    if contract.semantic_fingerprint != expected["semantic_fingerprint"]:
        raise RouteError(f"{name}: model semantics differ from the reviewed interface identity")
    actual = {key: channel for channel, model in prepared.entry_models.items() for key in model.model_fields}
    if actual != expected["entry_keys"]:
        raise RouteError(f"{name}: prepared entry mapping differs from the reviewed interface")
    assert_boolean_declarations(name, package_dir)
    _export_catalog(name, package_dir)
    return prepared


def definition(name: str, study_id: str, prepared, proposals, package_dir: Path):
    from simkit.study.definition import StudyDefinition
    from simkit.study.identity import digest_of
    from simkit.study.model_contract import load_model_contract
    from simkit.study.policy import ObjectivePolicy
    from simkit.study.strategy import PreparedListStrategy

    return StudyDefinition(
        study_id=study_id,
        entry_models=prepared.entry_models,
        strategy=PreparedListStrategy(proposals),
        validate_proposal=proposal_validator(name),
        policy=ObjectivePolicy(objectives=(), response_roles={}),
        executable_fingerprint=prepared.fingerprint,
        model_contract_fingerprint=load_model_contract(Path(package_dir).resolve()).semantic_fingerprint,
        input_schema_version="input-v1",
        evidence_schema_version=prepared.EVIDENCE_SCHEMA_VERSION,
        study_definition_fingerprint=digest_of({"unit": name, "proposals": [sorted(p.items()) for p in proposals]}),
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
            raise RouteError(f"evaluation constraint publication differs from the catalog: {sorted(actual ^ set(self.catalog))[:5]}")
        return evidence


def run_points(name: str, study_id: str, proposals, work_dir: Path, *, required_channels=None, package_dir: Path | None = None):
    """Execute one unit's proposals through `StudyRunner`. Returns (cases, db path).

    Proposals are partial entry maps; the runner completes them from the package defaults, which prepare_interface.py
    proved equal to the unit's manifest baseline point except the Nb3Sn strain, which the validator requires. Every
    declared channel must be published; a nonfinite value is a model result and is kept. The store is left on disk.
    """
    from simkit.study.query import StudyQuery
    from simkit.study.runner import StudyRunner
    from simkit.study.store import StudyStore

    unit = unit_of(name)
    package_dir = Path(package_dir or unit.package_dir)
    validate = proposal_validator(name)
    proposals = [validate(point) for point in proposals]
    if not proposals:
        raise RouteError("cannot run a study with no proposals")
    channels = dict(required_channels or {"lcoe": unit.prefix + "lcoe_calc__lcoe"})
    work_dir = Path(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    prepared = prepare(name, package_dir)
    study = definition(name, study_id, prepared, proposals, package_dir)
    catalog = _export_catalog(name, package_dir)
    db = work_dir / f"{study_id}.db"
    store = StudyStore.create_or_open(db, study.compatibility())
    try:
        store.acquire_lease()
        try:
            for case in StudyQuery(store, package_dir.resolve()).cases():
                if case.state == "completed":
                    require_published(case, channels)
            StudyRunner(store, study, _RequiredOutputsEvaluator(prepared, channels, catalog)).run()
        finally:
            store.release_lease()
    finally:
        store.close()
    reopened = StudyStore(db)
    try:
        cases = StudyQuery(reopened, package_dir.resolve()).cases()
    finally:
        reopened.close()
    return cases, db


def require_published(case, channels: dict[str, str]) -> None:
    missing = [f"{n} ({c})" for n, c in channels.items() if c not in case.outputs or case.outputs[c] is None]
    if missing:
        raise RouteError(f"case is missing required result channels: {missing}")


def _catalog_by_constraint_id(package_dir: Path) -> dict[str, dict]:
    contract = json.loads((Path(package_dir) / "contracts" / "model_contract.json").read_text())
    entries = contract["constraint_catalog"]["concrete_entries"]
    catalog = {e["constraint_id"]: e for e in entries}
    if len(catalog) != len(entries):
        raise RouteError("duplicate constraint IDs in the emitted catalog")
    return catalog


def _export_catalog(name: str, package_dir: Path | None = None) -> dict[str, dict]:
    unit = unit_of(name)
    catalog = _catalog_by_constraint_id(package_dir or unit.package_dir)
    if len(catalog) != unit.constraint_count:
        raise RouteError(f"{name}: expected exactly {unit.constraint_count} catalogued checks, found {len(catalog)}")
    identities = [entry.get("source_local_identity") for entry in catalog.values()]
    if any(not isinstance(i, str) or not i for i in identities) or len(set(identities)) != len(identities):
        raise RouteError(f"{name}: catalogued source_local_identity values must be nonempty and unique")
    return catalog


def short_verdicts(name: str, case) -> dict[str, str]:
    """Verdicts keyed by source-local identity, resolved through the emitted contract, never identifier text."""
    catalog = _export_catalog(name)
    if set(case.verdicts) != set(catalog):
        raise RouteError(f"{name}: case verdicts do not match the emitted catalog")
    return {catalog[cid]["source_local_identity"]: status for cid, status in sorted(case.verdicts.items())}


def completed(cases, what: str):
    done = [c for c in cases if c.state == "completed"]
    if len(done) != len(cases):
        raise RouteError(f"{what}: {len(cases) - len(done)} of {len(cases)} cases did not complete")
    return done


def reference_parity(outputs: dict, verdicts: dict) -> dict:
    """Design section 1.5: reference outputs and verdicts against the WI-080 pin, with the declared delta."""
    pin = json.loads(PIN_PATH.read_text())
    added = sorted(set(outputs) - set(pin["outputs"]))
    return dict(
        numeric_count=len(outputs),
        missing=sorted(set(pin["outputs"]) - set(outputs)),
        added=added,
        added_values={k: outputs[k] for k in added},
        unequal={k: [v, outputs.get(k)] for k, v in pin["outputs"].items() if v != outputs.get(k)},
        verdict_unequal={k: [v, verdicts.get(k)] for k, v in pin["responses"].items() if k != "headline" and v != verdicts.get(k)},
        declared_delta_ok=added == ["stellarator_09__stellaris__magnet__conductor_current__evaluation_defined"]
        and outputs.get("stellarator_09__stellaris__magnet__conductor_current__evaluation_defined") == 1.0,
    )


def write_identity_document(name: str, out_path: Path) -> Path:
    unit = unit_of(name)
    return common.write_document(identity.build_sealed(package_name=unit.package_name, package_root=unit.package_dir), out_path)


def execute_baseline(name: str, out_dir: Path | None = None) -> dict[str, Path]:
    """Execute the unit's manifest baseline point; deposit `package_identity.json` and `baseline_result.json`."""
    unit = unit_of(name)
    out_dir = Path(out_dir or unit.baseline_dir)
    point = dict(json.loads(unit.manifest_path.read_text())["baseline"]["point"])
    cases, db = run_points(name, f"stellarator-materials-{name}-baseline-v1", [point], out_dir / "_work")
    case = completed(cases, f"{name} baseline point")[0]
    catalog = _catalog_by_constraint_id(unit.package_dir)
    identity_path = write_identity_document(name, out_dir / "package_identity.json")
    result = {
        "schema_version": BASELINE_RESULT_SCHEMA_VERSION,
        "executed_under": {
            "identity_digest": case.executable_fingerprint,
            "store_id": common.manifest_mod.repo_relative_posix(db) if db.resolve().is_relative_to(REPO_ROOT) else db.name,
            "case_id": case.candidate_id,
        },
        "point": {key: float(value) for key, value in sorted(point.items())},
        "channels": {key: float(value) for key, value in sorted(case.outputs.items())},
        "verdicts": [{"constraint_id": cid, "definition_qualified_name": catalog[cid]["definition_qualified_name"],
                      "source_local_identity": catalog[cid]["source_local_identity"], "status": status}
                     for cid, status in sorted(case.verdicts.items())],
    }
    result_path = common.write_document(result, out_dir / "baseline_result.json")
    return {"identity": identity_path, "baseline_result": result_path}


# ------------------------------------------------------------------ study-side flags (contract section 7; A4)

REBCO_EXTRAPOLATED_BAND = (20.0, 24.0)  # T, contract section 4
REBCO_BEYOND_EXTENTS_BAND = (24.0, 25.0)  # T
STELLARIS_ENVELOPE_T = 24.9
ARM_FLAG_BAND = (25.0, 40.0)  # R/sqrt(A_wp), contract section 3.2 agent-chosen tolerance band


def material_flags(name: str, outputs: dict, verdicts: dict[str, str]) -> dict:
    """Flags carried on a material design (contract section 7), from published channels and short verdicts.

    `unsupported` is the conductor status alone (status_code 0); `envelope_flag` is `peak_field_ok` violated (B_max is a
    supplied envelope, never a failure). Nb3Sn `extrapolated` is the Round 1 law's own status 2 (edge) or 3 (law-only)
    (A4); REBCO bands follow contract section 4 from the evaluated B_peak."""
    if name not in MATERIALS:
        raise RouteError("flags are defined for the material units only")
    P = unit_of(name).prefix
    B = outputs[P + "magnet__peak_field_calc__B_peak"]
    status = outputs[P + "magnet__conductor__status_code"]
    x = outputs[P + "magnet__pack_field__R_over_sqrt_A_wp"]
    flags = dict(unsupported=status == 0.0, envelope_flag=verdicts.get("peak_field_ok") == "violated",
                 green_extrapolated=outputs[P + "cryoplant__refrigeration__green_extrapolated"] != 0.0,
                 arm_extrapolated=not ARM_FLAG_BAND[0] <= x <= ARM_FLAG_BAND[1], R_over_sqrt_A_wp=x,
                 ampere_floor_margin=outputs[P + "magnet__pack_field__ampere_floor_margin"],
                 ampere_floor_ok=verdicts.get("ampere_floor_ok"), beta_ok=verdicts.get("beta_ok"),
                 free_capacity=[P + "cryoplant__rated_intercept_W"])  # D17: the Green law prices the cold rating only
    if name == "nb3sn":
        flags["extrapolated"] = status in (2.0, 3.0)
    else:
        flags["extrapolated"] = REBCO_EXTRAPOLATED_BAND[0] < B <= REBCO_EXTRAPOLATED_BAND[1]
        flags["beyond_law_extents"] = REBCO_BEYOND_EXTENTS_BAND[0] < B <= REBCO_BEYOND_EXTENTS_BAND[1]
        flags["above_stellaris_envelope"] = B > STELLARIS_ENVELOPE_T
    return flags


def failure_texts(db: Path) -> dict[str, dict]:
    """Recorded refusals of a store, by candidate id (K25: a domain refusal is a failed evaluation with its text,
    which the study files `unsupported (domain refusal)`; it is never a status output)."""
    import sqlite3

    connection = sqlite3.connect(str(db))
    try:
        rows = connection.execute("SELECT candidate_id, failure_json FROM cases WHERE state = 'execution_failed'").fetchall()
    finally:
        connection.close()
    return {candidate: json.loads(text) for candidate, text in rows}
