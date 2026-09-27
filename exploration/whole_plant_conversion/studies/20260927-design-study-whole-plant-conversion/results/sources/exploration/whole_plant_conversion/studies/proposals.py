"""Retained finite conversion offers with the reviewed whole-plant source input.

Inherited hardware catalogs and performance/price sensitivities are unchanged.
The predecessor common-cost surcharge scenarios are omitted: this package models
the complete plant inventory. No model evaluation occurs here.
"""
from __future__ import annotations

import itertools
import math

P = "whole_plant_conversion__plant__"
SOURCE_MW = (2500.0, 2800.0, 3000.0)
GAS_FLOWS = (1500.0, 1750.0, 2000.0, 2250.0, 2500.0)
STAGE_RATIOS = (1.2, 1.35, 1.5, 1.65, 1.8)
SERVICE_OFFERS = (
    {"name": "25-25-20", "ua": (25.0, 25.0, 20.0), "recuperator_ua": 60.0, "quote_factor": 1.0},
    {"name": "25-25-25", "ua": (25.0, 25.0, 25.0), "recuperator_ua": 60.0, "quote_factor": 1.0},
    {"name": "25-25-40", "ua": (25.0, 25.0, 40.0), "recuperator_ua": 60.0, "quote_factor": 1.0},
    {"name": "30-30-50", "ua": (30.0, 30.0, 50.0), "recuperator_ua": 60.0, "quote_factor": 1.25},
    {"name": "40-40-60", "ua": (40.0, 40.0, 60.0), "recuperator_ua": 80.0, "quote_factor": 1.5},
)
GAS_QUOTE_KEYS = tuple(owner + "__price_factor" for owner in (
    "compressor_equipment", "turbine_equipment", "generator_equipment", "he_hx",
    "he_duty_equipment", "conversion_services", "heat_rejection_equipment"
)) + ("gas_ledger__capital9", "gas_ledger__controller_capital")
STEAM_QUOTE_KEYS = ("steam_ledger__capital3", "steam_ledger__capital4",
                    "steam_ledger__controller_capital", "steam_transport__costscale")


def change(base: dict, choices: dict) -> dict:
    """Apply declared input choices; reject stale or misspelled entry names."""
    point = dict(base)
    for suffix, value in choices.items():
        key = P + suffix
        if key not in point or not math.isfinite(value):
            raise ValueError(f"unknown or nonfinite chosen input: {key}")
        point[key] = float(value)
    return point


def gas_catalog(base: dict):
    for source, flow, ratio, offer in itertools.product(
            SOURCE_MW, GAS_FLOWS, STAGE_RATIOS, SERVICE_OFFERS):
        choices = {"source_basis__q_source_MW": source, "cycle__selected_flow": flow,
                   "recuperator_hardware__ua": offer["recuperator_ua"],
                   "conversion_services__price_factor": offer["quote_factor"],
                   "steam_transport__n_loops": 14,
                   "steam_transport__salt_pumps_per_circuit": 4,
                   "steam_transport__selected_salt_design_flow_kg_s": 250}
        choices.update({f"compressor_{n}__selected_ratio": ratio for n in (1, 2, 3)})
        choices.update({owner + "__ua": ua for owner, ua in
                        zip(("water_ic1", "water_ic2", "water_pre"), offer["ua"])})
        yield {"case": f"gas-q{source:g}-m{flow:g}-r{ratio:g}-ua{offer['name']}",
               "role": "gas_catalog", "chosen": choices, "point": change(base, choices)}


def steam_catalog(gas_anchor: dict):
    source = gas_anchor[P + "source_basis__q_source_MW"]
    for circuits, pumps, design_flow in itertools.product((10, 11, 12, 14), (2, 3, 4), (225, 250)):
        choices = {"steam_transport__n_loops": circuits,
                   "steam_transport__salt_pumps_per_circuit": pumps,
                   "steam_transport__selected_salt_design_flow_kg_s": design_flow}
        yield {"case": f"steam-q{source:g}-n{circuits}-k{pumps}-pump{design_flow}",
               "role": "steam_connector_catalog", "chosen": choices,
               "point": change(gas_anchor, choices)}


def sensitivity_catalog(anchor: dict):
    """Declared hypothetical offsets/multipliers at a previously tested anchor."""
    source = anchor[P + "source_basis__q_source_MW"]

    def row(name, choices):
        return {"case": f"sensitivity-q{source:g}-{name}", "role": "sensitivity",
                "chosen": choices, "point": change(anchor, choices)}

    gas_eta = tuple(f"compressor_{n}__efficiency" for n in (1, 2, 3)) + ("cycle__turbine_efficiency",)
    steam_eta = ("steam_cycle__eta_hp", "steam_cycle__eta_lp")
    for branch, keys in (("gas", gas_eta), ("steam", steam_eta), ("both", gas_eta + steam_eta)):
        for delta in (-0.03, 0.03):
            values = {key: anchor[P + key] + delta for key in keys}
            if any(not 0 < value <= 1 for value in values.values()):
                raise ValueError("declared efficiency sensitivity lies outside (0, 1]")
            yield row(f"{branch}-eta{delta:+.2f}", values)
    for branch, keys in (("gas", GAS_QUOTE_KEYS), ("steam", STEAM_QUOTE_KEYS)):
        for factor in (0.5, 1.5):
            yield row(f"{branch}-quote-x{factor:g}", {key: anchor[P + key] * factor for key in keys})
    for gas_factor, steam_factor in ((0.5, 1.5), (1.5, 0.5)):
        values = {key: anchor[P + key] * gas_factor for key in GAS_QUOTE_KEYS}
        values.update({key: anchor[P + key] * steam_factor for key in STEAM_QUOTE_KEYS})
        yield row(f"gas-quote-x{gas_factor:g}-steam-x{steam_factor:g}", values)
    for factor in (0.5, 1.5):
        keys = tuple(f"{branch}_ledger__{attr}" for branch in ("gas", "steam")
                     for attr in ("annual_service_fraction", "replacement_fraction"))
        yield row(f"recurring-x{factor:g}", {key: anchor[P + key] * factor for key in keys})


def adverse_controller_catalog(anchor: dict):
    source = anchor[P + "source_basis__q_source_MW"]
    for branch in ("gas", "steam"):
        choices = {branch + "_boundary__bypass_flow_rating": 500.0,
                   branch + "_ledger__controller_capital": 8_000_000.0}
        yield {"case": f"controller-q{source:g}-{branch}-500",
               "role": "adverse_controller_offer", "chosen": choices,
               "point": change(anchor, choices)}
