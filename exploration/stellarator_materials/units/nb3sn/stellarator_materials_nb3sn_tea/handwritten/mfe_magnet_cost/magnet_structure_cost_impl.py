"""WI-063 exposes the inherited all-in support rate, retaining historical ABI.

Authority: models/library/analyses/mfe_magnet_cost.sysml. The two rate factors
are an assumption, not a measured stock/fabrication split or a qualified quote.
"""
import math
from stellarator_materials_nb3sn_tea.modules.mfe_magnet_cost.magnet_structure_cost import Magnet_Structure_CostInput
from stellarator_materials_nb3sn_tea.schemas.magnet_structure_cost_output import Magnet_Structure_CostOutput

AUTO_IMPLEMENTED = False


def run_magnet_structure_cost(inputs: Magnet_Structure_CostInput) -> tuple[float, float]:
    name = "Magnet Structure Cost"
    for key in ("legacy_casing_fraction", "m_support", "n_coils", "m_casing", "steel_price", "f_steel_fab"):
        value = getattr(inputs, key)
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"{name}: {key} must be finite and nonnegative")
    if inputs.legacy_casing_fraction > 1:
        raise ValueError(f"{name}: legacy fraction must be in [0, 1]")

    def product(key, a, b):
        value = a * b
        if not math.isfinite(value) or (a > 0 and b > 0 and value == 0):
            raise ValueError(f"{name}: {key} arithmetic overflow/underflow")
        return value

    rate = product("effective_all_in_rate", inputs.steel_price, inputs.f_steel_fab)
    casing = product("casing_count", inputs.legacy_casing_fraction, inputs.n_coils)
    casing = product("casing_mass", casing, inputs.m_casing)
    mass = casing + inputs.m_support
    if not math.isfinite(mass):
        raise ValueError(f"{name}: support total mass overflow")
    cost = product("cost", product("cost", mass, inputs.steel_price), inputs.f_steel_fab)
    values = dict(cost=cost, effective_all_in_rate=rate)
    return tuple(values[key] for key in Magnet_Structure_CostOutput.model_fields)
