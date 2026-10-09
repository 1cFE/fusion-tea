"""WI-055 typed completion of the canonical nonzero stress-side contract."""
from stellarator_materials_rebco_tea.modules.mfe_magnet_field.winding_pack_stress import Winding_Pack_StressInput

AUTO_IMPLEMENTED = False


def run_winding_pack_stress(inputs: Winding_Pack_StressInput) -> float:
    """Evaluate the unchanged mean-stress equation on a nonzero side."""
    if inputs.wp_side == 0:
        raise ValueError("Winding Pack Stress: wp_side must be nonzero")
    return (((inputs.k_sigma * inputs.I_coil) * inputs.B_peak_in) / inputs.wp_side)
