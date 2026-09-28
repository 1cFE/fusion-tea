"""WI-059 exclusive total-support or legacy casing accounting.

Authority: models/library/analyses/mfe_magnet_cost.sysml.
"""
import math
from stellarator_tea.modules.mfe_magnet_cost.magnet_structure_cost import Magnet_Structure_CostInput

AUTO_IMPLEMENTED = False


def run_magnet_structure_cost(inputs: Magnet_Structure_CostInput) -> float:
    if not 0.0 <= inputs.legacy_casing_fraction <= 1.0:
        raise ValueError("Magnet Structure Cost: legacy fraction must be in [0, 1]")
    if not math.isfinite(inputs.m_support) or inputs.m_support < 0.0:
        raise ValueError("Magnet Structure Cost: support mass must be finite and nonnegative")
    return (inputs.legacy_casing_fraction * inputs.n_coils * inputs.m_casing + inputs.m_support) * inputs.steel_price * inputs.f_steel_fab
