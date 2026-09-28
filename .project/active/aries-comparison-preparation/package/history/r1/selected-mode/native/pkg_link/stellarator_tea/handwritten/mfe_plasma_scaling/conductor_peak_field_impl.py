"""Native completion of mfe_plasma_scaling::'Conductor Peak Field'.

Authority: models/library/analyses/mfe_plasma_scaling.sysml, normative
positive live/reference clearance and anchored bore equations (WI-053).
Input-domain rejection precedes all division; engineering limits remain
separate evaluated predicates. Valid arithmetic retains its original order.
"""
from stellarator_tea.modules.mfe_plasma_scaling.conductor_peak_field import Conductor_Peak_FieldInput

AUTO_IMPLEMENTED = False


def run_conductor_peak_field(inputs: Conductor_Peak_FieldInput) -> float:
    """Return signed conductor field, refusing invalid clearance first."""
    if not inputs.R_in - inputs.a_coil_in > 0:
        raise ValueError('Conductor Peak Field: live clearance R_in - a_coil_in must be > 0')
    if not inputs.R_ref_in - inputs.a_coil_ref_in > 0:
        raise ValueError('Conductor Peak Field: reference clearance R_ref_in - a_coil_ref_in must be > 0')
    bore_factor = inputs.R_in / (inputs.R_in - inputs.a_coil_in)
    bore_factor_ref = inputs.R_ref_in / (inputs.R_ref_in - inputs.a_coil_ref_in)
    bore_norm = bore_factor / bore_factor_ref
    return (inputs.B_axis_in * inputs.peak_ratio_in) * bore_norm
