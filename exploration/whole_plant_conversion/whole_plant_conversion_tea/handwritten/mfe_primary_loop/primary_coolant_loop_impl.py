"""WI-056 typed completion of the canonical finite-positive primary-loop domain.

Valid arithmetic and thirteen-output ABI are preserved from the entering generated
body. Equations and physical assumptions: models/library/analyses/mfe_primary_loop.sysml.
"""
from __future__ import annotations
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from whole_plant_conversion_tea.modules.mfe_primary_loop.primary_coolant_loop import Primary_Coolant_LoopInput

AUTO_IMPLEMENTED = False


def calculate(inputs) -> dict[str, float]:
    """Evaluate the always-active chain after checking its two heating operands."""
    if not math.isfinite(inputs.cp_in) or inputs.cp_in <= 0:
        raise ValueError("Primary Coolant Loop: cp_in must be finite and positive")
    if not math.isfinite(inputs.dT_blanket_in) or inputs.dT_blanket_in <= 0:
        raise ValueError("Primary Coolant Loop: dT_blanket_in must be finite and positive")
    if not math.isfinite(inputs.mdot_loop_rated_in) or inputs.mdot_loop_rated_in <= 0:
        raise ValueError("Primary Coolant Loop: offered flow ceiling must be finite and positive")
    k_isen = ((inputs.gamma_in - 1.0) / inputs.gamma_in)
    mdot = ((inputs.q_source_in * 1000000.0) / (inputs.cp_in * inputs.dT_blanket_in))
    mdot_loop = (mdot / inputs.n_loops_in)
    dp_loop = ((inputs.f_loss_in * inputs.dp_loop_ref_in) * ((mdot_loop / inputs.mdot_loop_ref_in) ** 2))
    suction = inputs.p_loop_in - dp_loop
    if (not math.isfinite(inputs.p_loop_in) or inputs.p_loop_in <= 0
            or not math.isfinite(dp_loop) or dp_loop < 0
            or not math.isfinite(suction) or suction <= 0):
        raise ValueError(
            "Primary Coolant Loop: unsupported compressor pressure state; "
            f"p_loop_in={inputs.p_loop_in!r} Pa, dp_loop={dp_loop!r} Pa, "
            f"suction={suction!r} Pa; requires finite p_loop_in > dp_loop >= 0 Pa"
        )
    r_comp = (inputs.p_loop_in / (inputs.p_loop_in - dp_loop))
    T_comp_in = (inputs.T_in_in / (1.0 + (((r_comp ** k_isen) - 1.0) / inputs.eta_is_in)))
    w_fluid = (((mdot * inputs.cp_in) * (inputs.T_in_in - T_comp_in)) / 1000000.0)
    p_elec = (w_fluid / inputs.eta_drive_in)
    return {
        'p_loop_margin': inputs.p_loop_in - dp_loop,
        'q_recovered_total': inputs.loop_live_in*w_fluid + inputs.eta_p_direct_in*inputs.p_pump_direct_in,
        'p_elec': p_elec,
        'p_pump_total': inputs.loop_live_in*p_elec + inputs.p_pump_direct_in,
        'T_out': inputs.T_in_in + inputs.dT_blanket_in,
        'T_comp_in': T_comp_in,
        'dp_loop': dp_loop,
        'mdot_loop': mdot_loop,
        'w_fluid': w_fluid,
        'capacity_margin': inputs.mdot_loop_rated_in - mdot_loop,
        'q_ihx': inputs.q_source_in + w_fluid,
        'mdot': mdot,
        'r_comp': r_comp,
    }


def run_primary_coolant_loop(inputs: Primary_Coolant_LoopInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float, float, float]:
    from whole_plant_conversion_tea.schemas.primary_coolant_loop_output import Primary_Coolant_LoopOutput
    result = calculate(inputs)
    return tuple(result[name] for name in Primary_Coolant_LoopOutput.model_fields)
