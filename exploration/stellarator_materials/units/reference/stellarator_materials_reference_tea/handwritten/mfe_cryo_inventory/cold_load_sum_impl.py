"""WI059 cold assembly, preserving old signed nuclear/fixed/direct semantics."""
import math
from stellarator_materials_reference_tea.modules.mfe_cryo_inventory.cold_load_sum import Cold_Load_SumInput
AUTO_IMPLEMENTED = False

def run_cold_load_sum(inputs: Cold_Load_SumInput) -> tuple[float, float]:
    if not math.isfinite(inputs.rho_structure) or inputs.rho_structure <= 0:
        raise ValueError("Cold Load Sum: rho_structure must be finite and positive")
    for name in ("q_nuc_structure", "m_support", "q_inventory_cold"):
        value = getattr(inputs, name)
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"Cold Load Sum: {name} must be finite and nonnegative")
    q = inputs.q_nuc_structure * inputs.m_support / inputs.rho_structure
    p = inputs.f_uplift * (inputs.q_nuc * inputs.vol_cold * 1e-6 + inputs.p_fixed + q * 1e-6) + inputs.q_inventory_cold * 1e-6
    return q, p
