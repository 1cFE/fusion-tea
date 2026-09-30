"""Declare the study's axis groups at the design-attribute level with complete entry-key expansion.

Every design section 6 attribute of the WI-099 package (136 attributes, one generated entry key each) is placed in
exactly one of seven groups. No equations, no evaluation. Run from the repository root:

    .codex-test/run bash -c 'PYTHONPATH="$PWD" exec python <record>/declare_axes.py --out <record>/axes.json'
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from exploration.magnet_materials.studies import interface_data

OFFER = ("n_elements", "cabling_factor", "cable_void", "cu_space", "steel_area", "misc_area", "solder_area",
         "ins_fraction", "rating_cold")
COMMON_CONDUCTOR = ("T_supply", "nuclear_rise", "margin_rise", "fraction_rule", "acceptance_rule")
CONSTRUCTION_RULE = ("J_cu_rule", "cu_void", "cu_per_kA_rule", "steel_per_kA_rule", "B_steel_ref", "steel_B_scaling")
DENSITIES = ("element_density", "rho_cu", "rho_steel", "rho_solder")
NB3SN_LAW = ("strand_diameter", "strand_copper_fraction", "p", "q", "C1", "Ca1", "Ca2", "eps0a", "Bc20", "Tc0",
             "eps_intrinsic")
REBCO_LAW = ("tape_width", "tape_thickness", "tape_copper_fraction", "anchor_ic", "shape_mode", "g8", "g10", "g12",
             "g15", "g20", "alpha", "T_star", "degradation")
CRYO = ("nuclear_density", "cold_volume", "radiation_ref", "conduction_ref", "T_conduction_ref", "n_leads", "f_lead",
        "L0", "p_joint_ref", "I_joint_ref", "shield_static", "load_multiplier", "eta_mode", "eta_const", "green_a",
        "green_b", "f_carnot_shield", "capital_mode", "green_c", "green_d", "T_green")
PRICES = ("price_cu", "price_steel", "price_solder", "element_price_per_m", "manufacturing_per_m")


def declarations() -> dict:
    attributes = interface_data.INTERFACE["design_attributes"]

    def keys(names):
        return [{"key": attributes[name], "provenance": "fan_out"} for name in names]

    groups = [
        {"axis": "duty",
         "keys": keys(["duty." + a for a in ("B_peak", "B_ref", "I_ref", "available_area", "coils", "turns",
                                               "turn_length")]),
         "note": "Specified magnetic duty and anchor geometry (contract r3 section 2). B_peak is the field point; "
                 "the model derives turn_current = I_ref*B_peak/B_ref as a channel, so the duty axis reaches every "
                 "current-dependent calculation through that derived channel. The anchor attributes select anchor D "
                 "or S and its turn-length sensitivity; no field is computed from winding size."},
        {"axis": "nb3sn-offer", "keys": keys(["nb3sn." + a for a in OFFER]),
         "note": "The supplied Nb3Sn winding offer: element count, construction areas and packing, insulation "
                 "fraction and installed cold-stage refrigerator rating (contract section 5, MR-7 chosen role). "
                 "Proposed by the declared offer policy outside the evaluator; never resized by it."},
        {"axis": "rebco-offer", "keys": keys(["rebco." + a for a in OFFER]),
         "note": "The supplied REBCO winding offer, same quantities as nb3sn-offer."},
        {"axis": "nb3sn-conductor-assumptions",
         "keys": keys(["nb3sn." + a for a in COMMON_CONDUCTOR + NB3SN_LAW + CONSTRUCTION_RULE + DENSITIES]),
         "note": "Nb3Sn conductor law parameters (strand grade, strain), operating temperatures and margin rule, "
                 "allowance-rule inputs for copper and steel, and material densities."},
        {"axis": "rebco-conductor-assumptions",
         "keys": keys(["rebco." + a for a in COMMON_CONDUCTOR + REBCO_LAW + CONSTRUCTION_RULE + DENSITIES]),
         "note": "REBCO tape law (anchor, shape, T*, degradation), operating temperatures and margin rule, "
                 "allowance-rule inputs for copper and steel, and material densities."},
        {"axis": "cryogenic-assumptions",
         "keys": keys([m + "." + a for m in ("nb3sn", "rebco") for a in CRYO]),
         "note": "Cold-stage and intercept load terms, lead and joint parameters, load multiplier, refrigerator "
                 "efficiency and capital basis (contract section 6). Both material parts carry their own copy."},
        {"axis": "economic-assumptions",
         "keys": keys(["economics." + a for a in ("crf", "availability", "electricity_price", "hours",
                                                   "usd2015_to_2021")]
                      + [m + "." + a for m in ("nb3sn", "rebco") for a in PRICES]),
         "note": "Finance and electricity conventions plus conductor, material and manufacturing prices "
                 "(contract section 7)."},
    ]
    declared = [k["key"] for g in groups for k in g["keys"]]
    expected = set(attributes.values())
    if len(declared) != len(set(declared)) or set(declared) != expected:
        raise ValueError({"duplicates": len(declared) - len(set(declared)),
                          "missing": sorted(expected - set(declared)),
                          "unknown": sorted(set(declared) - expected)})
    return {"schema_version": "study-axis-declaration/v1", "groups": groups}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    with args.out.open("x") as stream:
        json.dump(declarations(), stream, indent=2)
        stream.write("\n")
    print("declared", sum(len(g["keys"]) for g in declarations()["groups"]), "keys in",
          len(declarations()["groups"]), "groups ->", args.out)
