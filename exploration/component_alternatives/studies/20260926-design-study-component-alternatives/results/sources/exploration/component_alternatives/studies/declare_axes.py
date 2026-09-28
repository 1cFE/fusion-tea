"""Declare the study's chosen SysML attributes; no equations or evaluations."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from exploration.component_alternatives.studies.prepare_interface import PACKAGE, discover

PREFIX = "component_alternatives__plant__"


def declarations() -> dict:
    rows = []

    def add(owner, attribute, note):
        rows.append({"axis": owner + "_" + attribute,
                     "keys": [{"key": PREFIX + owner + "__" + attribute,
                               "provenance": "fan_out"}],
                     "note": "SysML attribute component_alternatives::plant::"
                     + owner + "::" + attribute + ". " + note})

    add("blanket_source", "q_source", "Chosen common source heat scenarios; no matching solve.")
    add("cycle", "selected_flow", "Chosen gas operating flow at held installed ratings.")
    for stage in (1, 2, 3):
        add("compressor_" + str(stage), "selected_ratio",
            "Independent stage choice. The proposal catalog coordinates the three choices at equal values; no physical identity is inferred.")
        add("compressor_" + str(stage), "efficiency", "Hypothetical performance sensitivity.")
    add("cycle", "turbine_efficiency", "Hypothetical performance sensitivity.")
    for owner in ("water_ic1", "water_ic2", "water_pre", "recuperator_hardware"):
        add(owner, "ua", "Installed capability selected from an explicitly priced coordinated service offer.")
    for attr in ("n_loops", "salt_pumps_per_circuit", "selected_salt_design_flow_kg_s"):
        add("steam_transport", attr,
            "Selected salt/IHX equipment offer. Here n_loops counts offered IHX circuits; upstream primary loop count remains held at 14.")
    for branch in ("steam", "gas"):
        add(branch + "_boundary", "bypass_flow_rating", "Full or deliberately undersized purchased controller offer.")
        add(branch + "_ledger", "controller_capital", "Hypothetical controller quote paired with its declared flow rating; also subject to branch quote sensitivity.")
        for attr in ("annual_service_fraction", "replacement_fraction"):
            add(branch + "_ledger", attr, "Hypothetical recurring-cost sensitivity. Separate salt event schedule remains explicit.")
        add(branch + "_ledger", "common_source_pv", "Illustrative common upstream present-value charge, coordinated equally across branches; no fuel price model.")
    for owner in ("compressor_equipment", "turbine_equipment", "generator_equipment",
                  "he_hx", "he_duty_equipment", "conversion_services", "heat_rejection_equipment"):
        add(owner, "price_factor", "Hypothetical quote sensitivity, with physical ratings held. The service quote is also part of its named equipment offer.")
    add("gas_ledger", "capital9", "Selected cycle-transport quote in USD2004; physical scope held.")
    for attr in ("capital3", "capital4"):
        add("steam_ledger", attr, "Selected steam conversion or rejection aggregate quote in USD2025; physical scope held.")
    add("steam_transport", "costscale", "Existing salt-connector cost multiplier; no physical equipment sizing.")
    for attr in ("eta_hp", "eta_lp"):
        add("steam_cycle", attr, "Hypothetical performance sensitivity on the selected steam offer.")
    for attr in ("steam_temperature_C", "reheat_temperature_C", "condenser_temperature_C"):
        add("steam_cycle", attr, "Declared but declined: held steam offer does not establish an off-design temperature envelope.")
    add("steam_transport", "secondary_head", "Declared but declined: altered operating salt head changes the captured steam return condition.")

    available = discover(PACKAGE.resolve())["entry_keys"]
    keys = [key["key"] for row in rows for key in row["keys"]]
    if len(keys) != len(set(keys)) or not set(keys) <= set(available):
        raise ValueError({"missing_entry_keys": sorted(set(keys) - set(available)),
                          "duplicate_count": len(keys) - len(set(keys))})
    return {"schema_version": "study-axis-declaration/v1", "groups": rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    with args.out.open("x") as stream:
        json.dump(declarations(), stream, indent=2)
        stream.write("\n")
