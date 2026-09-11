"""Qualified IFE oracle adapter; arithmetic stays in the independent source oracle."""
from math import isfinite
from tests.ife_oracle import BASE, PREFIX as P, NET_GATE, HEURISTIC, source_oracle

ENTRY_KEYS = {P + name: name for name in BASE} | {P + "viability__threshold": "viability__threshold"}


class OracleSeamError(ValueError):
    """The independent oracle cannot represent the requested point."""


def evaluate(point):
    """Map qualified inputs to independent annual cash flows and qualified outputs."""
    unknown = set(point) - ENTRY_KEYS.keys()
    if unknown:
        raise OracleSeamError(f"undeclared entry keys: {sorted(unknown)}")
    overrides = {}
    for key, value in point.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
            raise OracleSeamError(f"finite numeric input required: {key}")
        name = ENTRY_KEYS[key]
        if name in ("construction_duration", "operational_duration"):
            if value <= 0 or not float(value).is_integer():
                raise OracleSeamError(f"oracle requires positive integral years: {key}")
        if name != "viability__threshold":
            overrides[name] = float(value)
    return source_oracle(overrides)


def operand_bindings():
    """Explicitly bind the two audited predicates to independent inputs/channels."""
    return {
        NET_GATE: {"net_power": {"kind": "channel", "key": P + "lcoe_calc__net_electric_power"}},
        HEURISTIC: {
            "eta": {"kind": "input", "key": P + "driver__efficiency"},
            "gain_in": {"kind": "input", "key": P + "gain"},
            "threshold": {"kind": "input", "key": P + "viability__threshold"},
        },
    }
