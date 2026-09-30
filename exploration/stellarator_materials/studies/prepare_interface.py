"""Discover the three built WI-100 packages and write their reviewed interface and study manifests (design section 5).

For each unit (reference, rebco, nb3sn) this reads the generated entry map, assigns every entry key to exactly one class
of the design's key partition (section 5.1, D5, review R5) and fails closed on any key outside it, checks that the design
files' defaults equal reference_designs.json, evaluates the unit's baseline point once through the stock evaluator (the
published channels, the verdicts and the headline), and writes:

  studies/interface_data.py         INTERFACE['units'][unit]: identity, entry map, Boolean keys, partition, baseline
                                    point, published channels, constraint catalog, constant channels
  studies/<unit>/manifest.json      stock study-manifest schema; baseline = the reference regression point, the REBCO
                                    basis-bridge default, the Nb3Sn default plus eps_intrinsic_in = -0.003 (design D4, K6)

No model arithmetic happens here.
Run: .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python exploration/stellarator_materials/studies/prepare_interface.py'
"""
from __future__ import annotations

import json
import math
import pprint
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from scripts.study import common, manifest  # noqa: E402
from exploration.stellarator_materials.studies import study_route as route  # noqa: E402

PIN_INPUTS = ROOT / "work/active/WI-098_whole-plant-conversion-comparison/evidence/magnet-probe/baseline-inputs.json"
REFERENCE_DESIGNS = HERE.parent / "reference_designs.json"
VARIANTS = HERE.parent / "models/library/analyses/magnet_material_variants.sysml"
PIN_PREFIX = "stellarator_09__stellaris__"
REFERENCE_DELTA = {"magnet__rebco_law_enabled": 1.0, "magnet__coil__arm_slope": 0.0, "magnet__coil__arm_x_ref": 0.0}  # D6
NB3SN_STRAIN = -0.003  # manifest baseline point (K6, D4)
CONSTRUCTION = ("cu_space", "steel_area", "misc_area", "solder_area", "ins_fraction", "cabling_factor", "cable_void",
                "J_cu_rule", "cu_void", "cu_per_kA_rule", "steel_per_kA_rule", "B_steel_ref", "steel_B_scaling")
# Design section 5.1 varied families (after the material prefix).
VARIED_EXACT = frozenset(
    ["plasma__f_ren", "beta_limit", "magnet__coil__peak_ratio", "magnet__coil__arm_slope", "magnet__coil__arm_x_ref",
     "magnet__coil__k_link", "magnet__winding_pack__B_max", "magnet__coil__reference_turns", "magnet__coil__turn_current",
     "plasma__R", "plasma__a", "plasma__T_i0", "plasma__n_e0", "magnet__n_elements", "magnet__winding_pack__wp_side",
     "magnet__coil__coil_t", "magnet__casing__interior_y", "magnet__m_support", "heating__p_wallplug_heat",
     "cryoplant__rated_cold_W", "cryoplant__rated_intercept_W", "cryoplant__rated_cryogenic_cold_K",
     "cryoplant__rated_cryogenic_intercept_K", "cryoplant__rated_cryogenic_ambient_K", "cryoplant__T_cold_cryo",
     "turbine__purchase_cost_per_module", "heat_rejection__purchase_cost_per_module",
     "power_supplies__purchase_cost_per_module", "divertor__purchase_cost_per_module", "magnet__element_price_per_m",
     "turbine__selected_gross_MWe", "heat_transport__mdot_loop_rated"] + ["magnet__" + c for c in CONSTRUCTION])
VARIED_PATTERNS = (r"(^|__)rated_", r"(^|__)installed_", r"^buildings__selected_", r"_class_MWe?$",
                   r"^heat_transport__helium_rated_", r"^heat_transport__equipment_.*_design_",
                   r"^heat_transport__equipment_.*_purchased_mass_kg$")
REMOVED = ("cryoplant__purchase_cost_per_module", "cryoplant__inventory_enabled", "magnet__rebco_law_enabled")
NAMED_CALC_USAGE = {"rebco": ("magnet__pack_field__mu0_in",),
                    "nb3sn": ("magnet__conductor__eps_intrinsic_in", "magnet__pack_field__mu0_in")}
# New keys that are neither variant attributes nor calc-usage formals: K10's Boolean seam flag (an administrative flag
# that can only remove capability credit) and Round 1's zero manufacturing rate bound as a usage literal (contract N4).
NEW_ADMINISTRATIVE = ("cryoplant__intercept_demand_available", "magnet__inventory__manufacturing_per_m_in")
VARIANT_PARTS = {"rebco": ("Round1 REBCO Magnet System", "Staged Cryoplant"), "nb3sn": ("Nb3Sn Magnet System", "Staged Cryoplant")}
# Discovery point for a unit whose default refuses (K22): the Stellaris supplied turns, at which the plant evaluates.
DISCOVERY = {"nb3sn": lambda P: {P + "magnet__coil__reference_turns": 308.0}}
OBJECTIVES = [("lcoe", "lcoe_calc__lcoe", "Headline levelized cost of electricity of the plant instance."),
              ("total_capital", "total_capital__total_capital", "Total capital including interest during construction."),
              ("magnet_capital", "magnet__magnet_capital_rollup__capital_cost", "CAS22.1.3 magnet capital rollup."),
              ("p_net", "pb__p_net", "Net electric power, the LCOE denominator."),
              ("cryo_capital", "cryoplant__aux_cooling__cryo_cost", "Refrigeration capital account."),
              ("p_aux_required", "plasma__sustain__p_aux_required", "Required sustained heating (policy read-back).")]


def variant_attributes(name: str) -> set[str]:
    """Suffixes of the attributes the unit's variant defs declare without a value (design sections 2.5-2.7)."""
    text = VARIANTS.read_text()
    out = set()
    for part in VARIANT_PARTS[name]:
        block = text[text.index(f"part def '{part}'"):]
        block = block[:block.index("\n    }\n")]
        owner = "cryoplant__" if part == "Staged Cryoplant" else "magnet__"
        out |= {owner + m for m in re.findall(r"^\s{8}attribute (\w+) : Real;$", block, re.M)}
    return out


def partition(name: str, entry_keys: set[str], pin_suffixes: set[str]) -> dict[str, list[str]]:
    unit = route.unit_of(name)
    P = unit.prefix
    if not all(k.startswith(P) for k in entry_keys):
        raise ValueError(f"{name}: entry keys outside the unit prefix")
    suffixes = {k[len(P):] for k in entry_keys}
    if name == "reference":
        expected = pin_suffixes | set(REFERENCE_DELTA)
        if suffixes != expected:
            raise ValueError(f"reference entry keys differ from the pin plus the declared delta: "
                             f"extra={sorted(suffixes - expected)}, missing={sorted(expected - suffixes)}")
        return {"reference_pin": sorted(P + s for s in pin_suffixes), "reference_declared_delta": sorted(P + s for s in REFERENCE_DELTA)}
    classes = {"removed": [], "named_calc_usage": [], "varied": [], "new_variant": [], "new_administrative": [], "held_plant": []}
    declared = variant_attributes(name)
    for s in sorted(suffixes):
        if s in REMOVED:
            classes["removed"].append(s)
        elif s in NAMED_CALC_USAGE[name]:
            classes["named_calc_usage"].append(s)
        elif s in VARIED_EXACT or any(re.search(p, s) for p in VARIED_PATTERNS):
            classes["varied"].append(s)
        elif s in declared:
            classes["new_variant"].append(s)
        elif s in NEW_ADMINISTRATIVE:
            classes["new_administrative"].append(s)
        elif s in pin_suffixes:
            classes["held_plant"].append(s)
        else:
            raise ValueError(f"{name}: entry key {P + s} fits no class of the design's key partition (D5)")
    if "cryoplant__purchase_cost_per_module" in suffixes:
        raise ValueError(f"{name}: the cryoplant purchase price must be calculated, not an entry key")
    if set(classes["named_calc_usage"]) != set(NAMED_CALC_USAGE[name]):
        raise ValueError(f"{name}: named calc-usage keys {classes['named_calc_usage']} differ from {NAMED_CALC_USAGE[name]}")
    unassigned_declared = sorted(declared - suffixes - {s for s in declared if s in VARIED_EXACT})
    return {cls: sorted(P + s for s in keys) for cls, keys in classes.items()} | {
        "declared_constants_not_keys": sorted(P + s for s in unassigned_declared)}


def design_value_checks(name: str, defaults: dict, outputs: dict) -> list:
    """Every reference_designs.json value appears in the generated defaults (or, for a negative literal, as its constant
    channel); returns the constant channels."""
    design = json.loads(REFERENCE_DESIGNS.read_text())["designs"][name + "_material"]
    P = route.unit_of(name).prefix
    constants, mismatched = {}, []
    groups = {"magnet": "magnet__", "coil": "magnet__coil__", "cryoplant": "cryoplant__"}
    pairs = [(groups[g] + k, v) for g in groups for k, v in design[g]["values"].items()]
    pairs += [(path.replace(".", "__"), v) for path, v in design["existing"]["values"].items()]
    for suffix, value in pairs:
        key = P + suffix
        if key in defaults:
            if float(defaults[key]) != float(value):
                mismatched.append((key, defaults[key], value))
        else:
            channel = key + "__" + suffix.rsplit("__", 1)[-1]
            if outputs.get(channel) != value:
                mismatched.append((channel, outputs.get(channel), value))
            constants[key] = dict(channel=channel, value=float(value))
    if mismatched:
        raise ValueError(f"{name}: design-file defaults differ from reference_designs.json: {mismatched}")
    return constants


def prepare_unit(name: str, pin: dict) -> tuple[dict, dict | None]:
    from simkit.evaluation.failure import EvaluationFailed
    from simkit.study.bridge import CandidateBridge

    unit = route.unit_of(name)
    prepared, contract = route.prepare_unchecked(name)
    entry_keys = {key: channel for channel, model in prepared.entry_models.items() for key in model.model_fields}
    pin_suffixes = {k[len(PIN_PREFIX):] for k in pin}
    classes = partition(name, set(entry_keys), pin_suffixes)
    defaults = {}
    for path in sorted((unit.package_dir / "inputs").glob("*.json")):
        defaults.update(common.read_json(path, "generated entry defaults"))
    if name == "reference":
        point = {k: float(v) for k, v in pin.items()} | {PIN_PREFIX + k: v for k, v in REFERENCE_DELTA.items()}
        drift = sorted(k for k in point if float(defaults[k]) != point[k])
        if drift:
            raise ValueError(f"reference package defaults differ from the pin inputs: {drift[:5]}")
    else:
        # every entry key except the Removed class, whose final values the route refuses to restate (K11)
        point = {k: float(defaults[k]) for k in entry_keys if k not in classes["removed"]}
        if name == "nb3sn":
            point[unit.prefix + "magnet__conductor__eps_intrinsic_in"] = NB3SN_STRAIN
    if set(point) != set(entry_keys) - set(classes.get("removed", ())):
        raise ValueError(f"{name}: baseline point is incomplete")
    complete = {k: float(defaults[k]) for k in entry_keys}
    booleans = route.boolean_keys(name)
    typed = lambda values: {k: (bool(v) if k in booleans else float(v)) for k, v in values.items()}
    refusal = None
    try:
        evidence = prepared.evaluate(CandidateBridge(prepared.entry_models).build(typed(complete | point)))
    except EvaluationFailed as exc:
        # Design K22: a default that refuses is regenerated from the offer policy's first recorded design that evaluates.
        # The unit's channels are discovered at its Stellaris-duty discovery point instead (the channel set does not
        # depend on the point), and no manifest is written for it until then.
        refusal = f"{type(exc).__name__}: {exc}"
        discovery = complete | point | DISCOVERY[name](unit.prefix)
        evidence = prepared.evaluate(CandidateBridge(prepared.entry_models).build(typed(discovery)))
    outputs = dict(evidence.outputs)
    constants = design_value_checks(name, defaults, outputs) if name != "reference" else {}
    catalog = route._catalog_by_constraint_id(unit.package_dir)
    constraints = {cid: e["source_local_identity"] for cid, e in sorted(catalog.items())}
    if len(constraints) != unit.constraint_count:
        raise ValueError(f"{name}: {len(constraints)} constraints, expected {unit.constraint_count}")
    verdicts = {constraints[cid]: status for cid, status in evidence.responses.items() if cid != "headline"}
    channels = sorted(k for k, v in outputs.items() if isinstance(v, (int, float)) and not isinstance(v, bool))
    provenance = {"executable_fingerprint": manifest.read_executable_fingerprint(unit.package_dir),
                  "semantic_fingerprint": contract.semantic_fingerprint}
    if provenance["executable_fingerprint"] != prepared.fingerprint:
        raise ValueError(f"{name}: recorded executable fingerprint differs from the prepared evaluator")
    if refusal is not None:
        interface = provenance | {
            "package": unit.package_name, "prefix": unit.prefix, "entry_keys": dict(sorted(entry_keys.items())),
            "boolean_keys": sorted(booleans), "partition": classes, "baseline_point": dict(sorted(point.items())),
            "baseline_refusal": refusal, "discovery_point_overrides": DISCOVERY[name](unit.prefix),
            "channels": channels, "constraints": constraints, "constant_channels": constants,
        }
        return interface, None
    interface = provenance | {
        "package": unit.package_name, "prefix": unit.prefix, "entry_keys": dict(sorted(entry_keys.items())),
        "boolean_keys": sorted(booleans), "partition": classes, "baseline_point": dict(sorted(point.items())),
        "channels": channels, "constraints": constraints, "constant_channels": constants,
    }
    indicator = manifest.indicator_input_fingerprint(unit.package_dir)
    indicator["files"] = [row["path"] for row in indicator["files"]]
    headline = unit.prefix + "lcoe_calc__lcoe"
    document = {
        "schema_version": manifest.MANIFEST_SCHEMA_VERSION,
        "package": {"name": manifest.read_package_name(unit.package_dir), "path": manifest.repo_relative_posix(unit.package_dir)},
        "fingerprints": {"indicator_inputs": indicator, "recorded_provenance": provenance},
        "objective_catalog": [{"name": n, "channel": unit.prefix + c, "note": note} for n, c, note in OBJECTIVES],
        "ties": [],
        "baseline": {
            "point": dict(sorted(point.items())),
            "headline": {"channel": headline, "value": float(outputs[headline])},
            "verdicts": [{"source_local_identity": k, "expected": v} for k, v in sorted(verdicts.items())],
        },
        "oracle": {"kind": "python_callable", "module": "exploration.stellarator_materials.studies.oracle_entry",
                   "callable": "evaluate", "sys_path": ".",
                   "note": "Adapter not present at build time. The oracle is written by a separate author from the design and "
                           "contract r4 only (exploration/stellarator_materials/oracle_glue.py, oracle-reuse.json, composing the "
                           "plant oracles and Round 1's oracle, design section 6.3); the coordinator binds it through this module "
                           "when preparing the study."},
    }
    manifest.validate(document)
    return interface, document


def prepare():
    pin = json.loads(PIN_INPUTS.read_text())
    units, summary = {}, {}
    for name in route.UNITS:
        interface, document = prepare_unit(name, pin)
        units[name] = interface
        target = route.unit_of(name).manifest_path
        summary[name] = {"entry_keys": len(interface["entry_keys"]), "channels": len(interface["channels"]),
                         "constraints": len(interface["constraints"]),
                         "partition": {k: len(v) for k, v in interface["partition"].items()}}
        if document is None:
            if target.exists():
                target.unlink()
            summary[name]["baseline_refusal"] = interface["baseline_refusal"]
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        common.write_document(document, target)
        summary[name] |= {"headline": document["baseline"]["headline"],
                          "violated": sorted(v["source_local_identity"] for v in document["baseline"]["verdicts"]
                                             if v["expected"] == "violated")}
    (HERE / "interface_data.py").write_text(
        '"""Discovered native metadata for the three WI-100 packages (written by prepare_interface.py); no physical arithmetic.\n\n'
        "INTERFACE['units'][unit] holds the identity, the generated entry map, the Boolean keys, the complete key partition of\n"
        "design section 5.1 (every entry key in exactly one class), the baseline point of the unit's manifest, the published\n"
        'channels, the constraint catalog (id -> source-local identity) and the negative-literal constant channels."""\n'
        "INTERFACE = " + pprint.pformat({"units": units}, sort_dicts=True, width=140) + "\n")
    return summary


if __name__ == "__main__":
    print(json.dumps(prepare(), indent=1))
