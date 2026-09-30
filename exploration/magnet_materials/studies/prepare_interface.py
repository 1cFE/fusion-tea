"""Discover the built magnet_materials_tea package and write its reviewed interface and study manifest.

Writes `interface_data.py` (entry map, published channels, constraint catalog, and the design section 6 attribute ->
entry-key map with the fixed design values) and `manifest.json` (stock study-manifest schema; baseline = the anchor D
reference case at 10 T from work/active/WI-099_magnet-conductor-alternatives/reference-case.json). One evaluation of the
reference point through the stock evaluator supplies the published channels and the baseline verdicts; no model
arithmetic happens here.
Run: .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python exploration/magnet_materials/studies/prepare_interface.py'
"""
from __future__ import annotations

import json
import math
import pprint
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from scripts.study import common, manifest  # noqa: E402
from exploration.magnet_materials.studies import study_route  # noqa: E402

PACKAGE = HERE.parent / "magnet_materials_tea"
REFERENCE_CASE = ROOT / "work/active/WI-099_magnet-conductor-alternatives/reference-case.json"
PREFIX = "magnet_subsystem__subsystem__"
CONSTRUCTION = ["cabling_factor", "cable_void", "cu_space", "steel_area", "misc_area", "solder_area", "ins_fraction", "J_cu_rule",
                "cu_void", "cu_per_kA_rule", "steel_per_kA_rule", "B_steel_ref", "steel_B_scaling"]
INVENTORY = ["element_density", "rho_cu", "rho_steel", "rho_solder", "price_cu", "price_steel", "price_solder", "element_price_per_m",
             "manufacturing_per_m"]
COLD = ["nuclear_density", "cold_volume", "radiation_ref", "conduction_ref", "T_conduction_ref", "n_leads", "f_lead", "L0",
        "p_joint_ref", "I_joint_ref", "shield_static", "load_multiplier"]
REFRIGERATION = ["rating_cold", "eta_mode", "eta_const", "green_a", "green_b", "f_carnot_shield", "capital_mode", "green_c",
                 "green_d", "T_green"]
COMMON_CONDUCTOR = ["n_elements", "T_supply", "nuclear_rise", "margin_rise", "fraction_rule", "acceptance_rule"]
# Design section 6, names exact.
SECTION_6 = {
    "duty": ["coils", "turns", "turn_length", "available_area", "I_ref", "B_ref", "B_peak"],
    "economics": ["crf", "availability", "electricity_price", "hours", "usd2015_to_2021"],
    "nb3sn": COMMON_CONDUCTOR + ["strand_diameter", "strand_copper_fraction", "p", "q", "C1", "Ca1", "Ca2", "eps0a", "Bc20", "Tc0",
                                 "eps_intrinsic"] + CONSTRUCTION + INVENTORY + COLD + REFRIGERATION,
    "rebco": COMMON_CONDUCTOR + ["tape_width", "tape_thickness", "tape_copper_fraction", "anchor_ic", "shape_mode", "g8", "g10", "g12",
                                 "g15", "g20", "alpha", "T_star", "degradation"] + CONSTRUCTION + INVENTORY + COLD + REFRIGERATION,
}
CRYO_FIXED = ["T_shield", "T_amb"] + [f"k_{letter}" for letter in "abcdefghi"]
FIXED = {
    "nb3sn": ["B_law_min", "B_law_max", "B_design_max", "B_edge_max", "T_law_min", "T_law_max", "eps_min", "eps_max"] + CRYO_FIXED,
    "rebco": ["B_knot_min", "B_knot_max", "B_law_min", "B_law_max", "T_law_min", "T_law_max"] + CRYO_FIXED,
}
# A negative design literal generates as a constant formula module (not an entry point); the one negative section 6 input,
# eps_intrinsic, is therefore an unbound calc input whose entry key sits on the conductor calc usage.
ENTRY_OVERRIDES = {"nb3sn.eps_intrinsic": PREFIX + "nb3sn__conductor__eps_intrinsic_in"}
CONSTRAINTS = ("acceptance_ok", "fit_ok", "copper_ok", "steel_ok", "capacity_ok")


def discover(prepared, contract):
    entry_keys = {key: channel for channel, model in prepared.entry_models.items() for key in model.model_fields}
    attributes = {}
    for part, names in SECTION_6.items():
        for name in names:
            key = ENTRY_OVERRIDES.get(f"{part}.{name}", f"{PREFIX}{part}__{name}")
            if key not in entry_keys:
                raise ValueError(f"design attribute {part}.{name} has no entry key {key}")
            attributes[f"{part}.{name}"] = key
    fixed_entries, fixed_constants = {}, {}
    for part, names in FIXED.items():
        for name in names:
            key = f"{PREFIX}{part}__{name}"
            if key in entry_keys:
                fixed_entries[key] = {"attribute": f"{part}.{name}"}
            else:
                fixed_constants[f"{part}.{name}"] = {"channel": f"{PREFIX}{part}__{name}__{name}"}
    covered = set(attributes.values()) | set(fixed_entries)
    if covered != set(entry_keys) or len(covered) != len(attributes) + len(fixed_entries):
        raise ValueError(f"entry keys not accounted for: {sorted(set(entry_keys) - covered)}; extra: {sorted(covered - set(entry_keys))}")
    constraints = {key: e["source_local_identity"] for key, e in study_route._catalog_by_constraint_id(PACKAGE).items()}
    constraint_ids = {}
    for constraint_id in constraints:
        part, rest = constraint_id.removeprefix(PREFIX).split("__", 1)
        local = rest.rsplit("__", 1)[0]
        constraint_ids[f"{part}.{local}"] = constraint_id
    expected = {f"{part}.{local}" for part in ("nb3sn", "rebco") for local in CONSTRAINTS}
    if set(constraint_ids) != expected:
        raise ValueError(f"constraint catalog differs from the design: {sorted(constraint_ids)}")
    return entry_keys, attributes, fixed_entries, fixed_constants, constraints, constraint_ids


def reference_point(entry_keys, attributes, fixed_entries):
    """Package defaults for the fixed values, reference-case.json for every section 6 attribute."""
    defaults = {}
    for path in sorted((PACKAGE / "inputs").glob("*.json")):
        defaults.update(common.read_json(path, "generated entry defaults"))
    reference = json.loads(REFERENCE_CASE.read_text())
    point = {key: float(defaults[key]) for key in fixed_entries}
    mismatched = []
    for name, key in attributes.items():
        part, attribute = name.split(".")
        value = float(reference[part][attribute])
        if key in defaults and float(defaults[key]) != value and name != "nb3sn.eps_intrinsic":
            mismatched.append((name, defaults[key], value))
        point[key] = value
    if mismatched:
        raise ValueError(f"design-file defaults differ from reference-case.json: {mismatched}")
    if set(point) != set(entry_keys):
        raise ValueError("reference point is incomplete")
    return point, {key: point[key] for key in fixed_entries}


def output_names(channels):
    """Design-meaning names for channels: '<part>.<calc>.<output>', 'pair.<output>', '<part>.<formula>'."""
    names = {}
    for channel in channels:
        parts = channel.removeprefix(PREFIX).split("__")
        names[".".join(parts[:-1] if len(parts) == 3 and parts[1] == parts[2] else parts)] = channel
    return names


def prepare():
    from simkit.study.bridge import CandidateBridge

    with tempfile.TemporaryDirectory() as work:
        prepared, contract = study_route.prepare_unchecked(PACKAGE, Path(work))
        entry_keys, attributes, fixed_entries, fixed_constants, constraints, constraint_ids = discover(prepared, contract)
        point, fixed_values = reference_point(entry_keys, attributes, fixed_entries)
        evidence = prepared.evaluate(CandidateBridge(prepared.entry_models).build(point))
        fingerprint = prepared.fingerprint
    outputs = dict(evidence.outputs)
    channels = {key: key for key, value in sorted(outputs.items())
                if isinstance(value, (int, float)) and not isinstance(value, bool)}
    for name, entry in fixed_constants.items():
        if entry["channel"] not in channels:
            raise ValueError(f"fixed constant {name} is not published as {entry['channel']}")
        entry["value"] = float(outputs[entry["channel"]])
    for key, entry in fixed_entries.items():
        entry["value"] = fixed_values[key]
    provenance = {"executable_fingerprint": manifest.read_executable_fingerprint(PACKAGE),
                  "semantic_fingerprint": contract.semantic_fingerprint}
    if provenance["executable_fingerprint"] != fingerprint:
        raise ValueError("recorded executable fingerprint differs from the prepared evaluator")
    interface = provenance | {
        "entry_keys": dict(sorted(entry_keys.items())),
        "channels": channels,
        "constraints": dict(sorted(constraints.items())),
        "design_attributes": attributes,
        "fixed_entries": dict(sorted(fixed_entries.items())),
        "fixed_constants": fixed_constants,
        "constraint_ids": dict(sorted(constraint_ids.items())),
        "output_channels": dict(sorted(output_names(channels).items())),
    }
    (HERE / "interface_data.py").write_text(
        '"""Discovered native metadata for magnet_materials_tea (written by prepare_interface.py); no physical arithmetic.\n\n'
        "design_attributes maps every design section 6 attribute to its entry key; fixed_entries are the fixed design values\n"
        "that are entry keys (kept at these values unless a test overrides them by name); fixed_constants are negative fixed\n"
        "values that generate as constant formula modules and are not overridable; constraint_ids names each asserted\n"
        'constraint by material; output_channels names every published channel by part, calculation and output."""\n'
        "INTERFACE = " + pprint.pformat(interface, sort_dicts=True, width=140) + "\n")

    verdicts = {}
    for constraint_id, status in evidence.responses.items():
        if constraint_id == "headline":
            continue
        local = constraints[constraint_id]
        if verdicts.get(local, status) != status:
            raise ValueError(f"baseline has different verdicts for the local identity {local}")
        verdicts[local] = status
    indicator = manifest.indicator_input_fingerprint(PACKAGE)
    indicator["files"] = [row["path"] for row in indicator["files"]]
    headline = PREFIX + "pair__cost_difference"
    document = {
        "schema_version": manifest.MANIFEST_SCHEMA_VERSION,
        "package": {"name": manifest.read_package_name(PACKAGE), "path": manifest.repo_relative_posix(PACKAGE)},
        "fingerprints": {"indicator_inputs": indicator, "recorded_provenance": provenance},
        "objective_catalog": [
            {"name": "cost_difference", "channel": headline, "note": "annualized REBCO minus Nb3Sn, USD2021/yr; rank only when pair rankable = 1"},
            {"name": "annualized_nb3sn", "channel": PREFIX + "nb3sn__annualized__annualized_cost"},
            {"name": "annualized_rebco", "channel": PREFIX + "rebco__annualized__annualized_cost"},
            {"name": "breakeven_rebco_price_per_m", "channel": PREFIX + "pair__breakeven_rebco_price_per_m"},
        ],
        "ties": [],
        "baseline": {
            "point": dict(sorted(point.items())),
            "headline": {"channel": headline, "value": float(outputs[headline])},
            "verdicts": [{"source_local_identity": key, "expected": value} for key, value in sorted(verdicts.items())],
        },
        "oracle": {"kind": "python_callable", "module": "exploration.magnet_materials.studies.oracle_entry", "callable": "evaluate",
                   "sys_path": ".",
                   "note": "Adapter not present at build time. The coordinator binds the independently authored oracle "
                           "(exploration/magnet_materials/oracle.py) through this module when preparing the study."},
    }
    manifest.validate(document)
    common.write_document(document, HERE / "manifest.json")
    return {"entries": len(entry_keys), "design_attributes": len(attributes), "fixed_entries": len(fixed_entries),
            "fixed_constants": len(fixed_constants), "channels": len(channels), "constraints": len(constraints),
            "headline": document["baseline"]["headline"], "verdicts": verdicts}


if __name__ == "__main__":
    print(json.dumps(prepare(), indent=1))
