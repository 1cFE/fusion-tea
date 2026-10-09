"""Step 2: declare the study's axis groups per unit at the design-attribute level with complete entry-key expansion.

One axis-declaration file per unit (axes_<unit>.json), because the three units are three packages with three key
prefixes and `preflight.py`'s declared-key gate checks a declaration against one package. Every WI-100 attribute emits
exactly one entry key per unit, so every group is a plain fan-out list; there are no ties.

Groups (brief t017 step 1; the eighth, conductor-assumptions, is the executor's addition because the Nb3Sn strain
variant moves `eps_intrinsic_in`, which no brief group names):
  assumption-confinement, assumption-geometry, duty, operating-point, winding-offer, plant-offer,
  economic-assumptions, conductor-assumptions (Nb3Sn only).
plant-offer takes every remaining key of the design section 5.1 varied family (interface partition 'varied') plus the
held plant keys the policy re-supplies in some case (facility positions, receipt leads, parcel offsets, service teams,
IHX count; contract r5 section 5 (P)). The check: every key any declared case moves off the package default is in
exactly one group.

    .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" exec python <record>/declare_axes.py'
"""
from __future__ import annotations

import json
import record_common as rc  # noqa: F401  (sets sys.path)
from exploration.stellarator_materials.studies.interface_data import INTERFACE

CONSTRUCTION = ("cu_space", "steel_area", "misc_area", "solder_area", "ins_fraction", "cabling_factor", "cable_void",
                "J_cu_rule", "cu_void", "cu_per_kA_rule", "steel_per_kA_rule", "B_steel_ref", "steel_B_scaling")
GROUPS = [
    ("assumption-confinement", ["plasma__f_ren", "beta_limit"],
     "Confinement assumption (contract r5 section 3.1): the ISS04 renormalization f_ren (1.0, 1.4, 1.8 by cell) and the "
     "beta limit (0.05; the 0.04 second verdict is recomputed study-side). Uniform over a cell and both materials."),
    ("assumption-geometry", ["magnet__coil__peak_ratio", "magnet__coil__arm_slope", "magnet__coil__arm_x_ref",
                             "magnet__coil__k_link"],
     "Coil-geometry assumption (contract section 3.2): anchored ratio 2.7667, HELIAS-class 2.12, the pack-size arm "
     "slope 0.0641 about x_ref 35.278, and the coil-set linkage k_link (0.7731 held; 0.95 variant on HELIAS cells)."),
    ("duty", ["magnet__coil__reference_turns", "magnet__coil__turn_current", "plasma__R", "plasma__a",
              "magnet__coil__coil_t", "magnet__casing__interior_y"],
     "Supplied magnetic duty and machine size (contract section 5): turns and turn current (50 kA; 86 kA variant) set "
     "the ampere-turns; R and a the size; the radial allocation coil_t moves the bore factor, radial build and layout; "
     "interior_y is the transverse cavity (no cost response)."),
    ("operating-point", ["plasma__n_e0", "plasma__T_i0"],
     "Supplied plasma operating point: T_i0 from the ladder 11/13/14.63/16/18 keV and n_e0 at matched fusion power or "
     "the power-short fallback (contract section 5, r5 least-heating rule)."),
    ("winding-offer", ["magnet__n_elements", "magnet__winding_pack__wp_side", "magnet__winding_pack__B_max"]
     + ["magnet__" + c for c in CONSTRUCTION],
     "Supplied winding (MR-7 chosen role): element count from the Round 1 acceptance rule, pack side from the "
     "construction rule, the per-turn construction areas and the construction-rule inputs (P for Nb3Sn, C for REBCO, "
     "common-P variant), and the supplied per-material design envelope B_max (a flag, never a failure)."),
    ("economic-assumptions", ["magnet__element_price_per_m", "cryoplant__usd2015_to_2021"],
     "Conductor price (REBCO 80/30/10 USD2021/m of 4 mm tape; Nb3Sn 8, variants 5.4 and 13.5) and the Green "
     "refrigerator capital's money-year factor, which the CPI 2021->2026 variant scales together with both prices."),
    ("conductor-assumptions", ["magnet__conductor__eps_intrinsic_in"],
     "Nb3Sn intrinsic strain (-0.3 % held, -0.6 % variant; contract section 4). Executor's addition: the brief names "
     "no group for it and the strain variant moves it."),
]
RESUPPLIED_HELD = ("buildings__clean_positions", "buildings__component_receipt_lead_days",
                   "buildings__cooling_clean_bundle_positions", "buildings__cooling_clean_helium_positions",
                   "buildings__cooling_clean_salt_positions", "buildings__cooling_dirty_bundle_positions",
                   "buildings__cooling_dirty_helium_positions", "buildings__cooling_dirty_salt_positions",
                   "buildings__dirty_buffer_positions", "buildings__dirty_store_positions",
                   "buildings__initial_receipt_lead_days", "buildings__parcel_origin_x_offset",
                   "buildings__parcel_origin_y_offset", "buildings__sector_service_teams", "heat_transport__n_loops")
PLANT_NOTE = ("Supplied plant offer re-supplied per design by the policy (contract section 5 rows F2/F8, r5 (P) Q13/Q14): "
              "structure mass, installed heating, cryo ratings and rated states, every screened package rating and "
              "offered state, purchased coolant masses, purchase costs per module (the purchase-exponent variant acts "
              "here), the 22 power classes, the building and parcel selections and dimensions, the facility "
              "positions, receipt leads and service teams, and the IHX exchanger count.")


def declaration(unit: str, cases: list) -> dict:
    U = INTERFACE["units"][unit]
    P = U["prefix"]
    entry = set(U["entry_keys"])
    if unit == "reference":  # every reference key is pinned; its groups are declared for the gates and declined
        varied_family = set(INTERFACE["units"]["rebco"]["partition"]["varied"])
        varied_family = {k[len(INTERFACE["units"]["rebco"]["prefix"]):] for k in varied_family}
    else:
        varied_family = {k[len(P):] for k in U["partition"]["varied"]}
    named = {s for _, keys, _ in GROUPS for s in keys}
    plant = sorted((varied_family - named) | set(RESUPPLIED_HELD))
    groups = []
    for axis, suffixes, note in GROUPS + [("plant-offer", plant, PLANT_NOTE)]:
        keys = [P + s for s in suffixes if P + s in entry]
        if not keys:
            continue  # e.g. conductor-assumptions on REBCO and the reference; recorded as not declared for that unit
        if unit == "reference":
            note = "Reference unit: pinned; declared for the seam's gates and declined (only the baseline runs). " + note
        groups.append({"axis": axis, "keys": [{"key": k, "provenance": "fan_out"} for k in keys], "note": note})
    declared = [k["key"] for g in groups for k in g["keys"]]
    if len(declared) != len(set(declared)):
        raise ValueError(f"{unit}: a key is declared in two groups")
    if unit != "reference":
        defaults = U["baseline_point"]
        constants = U["constant_channels"]
        moved = set()
        for c in cases:
            if c["labels"]["material"] != unit:
                continue
            for k, v in c["inputs"].items():
                if k not in defaults:  # a package constant carried by the case (Nb3Sn eps_min); not an entry key
                    if k not in constants or float(v) != float(constants[k]["value"]):
                        raise ValueError(f"{unit}: case key {k} is neither an entry key nor its package constant")
                    continue
                if float(v) != float(defaults[k]):
                    moved.add(k)
        missing = sorted(moved - set(declared))
        if missing:
            raise ValueError(f"{unit}: case-moved keys not in any group: {missing}")
    return {"schema_version": "study-axis-declaration/v1", "groups": groups}


if __name__ == "__main__":
    cases = rc.load_cases()["cases"]
    for unit in rc.UNITS:
        document = declaration(unit, cases)
        path = rc.axes_path(unit)
        with path.open("x") as stream:
            json.dump(document, stream, indent=2)
            stream.write("\n")
        print(unit, {g["axis"]: len(g["keys"]) for g in document["groups"]}, "->", path.name)
