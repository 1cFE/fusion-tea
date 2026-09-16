"""WI-065 typed completion of the native Divertor Heat Ledger equations.

Source and domain: models/library/analyses/mfe_divertor_heat.sysml.
The source peak already embeds capture and spatial shape. Capture annotates that
profile; it changes deposition and implied area together, never the peak twice.
"""
import math

from stellarator_tea.modules.mfe_divertor_heat.divertor_heat_ledger import Divertor_Heat_LedgerInput

AUTO_IMPLEMENTED = False


def run_divertor_heat_ledger(inputs: Divertor_Heat_LedgerInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float]:
    """Compute conserved destinations and preserve the original peak arithmetic."""
    def checked(name, value, positive=False):
        if not math.isfinite(value) or (positive and value <= 0):
            raise ValueError(f'Divertor Heat Ledger: {name} must be finite' + (' and positive' if positive else ''))
        return value

    fractions = ('f_rad_total_in', 'target_capture_fraction_in')
    positive_inputs = ('p_nonrad_ref_in', 'R_in', 'R_ref_in')
    for name in type(inputs).model_fields:
        value = getattr(inputs, name)
        checked(name, value, name in positive_inputs)
        if name != 'p_aux_required_in' and value < 0:
            raise ValueError(f'Divertor Heat Ledger: {name} must be nonnegative')
        if name in fractions and value > 1:
            raise ValueError(f'Divertor Heat Ledger: {name} must lie in [0, 1]')
    c = inputs.target_capture_fraction_in
    f = inputs.f_rad_total_in
    qref = inputs.q_target_ref_in
    if qref > 0 and c == 0:
        raise ValueError('Divertor Heat Ledger: active q_target_ref_in requires positive target_capture_fraction_in')
    h = checked('p_heat_abs', inputs.p_alpha_heat_in + inputs.p_coupled_in)
    if inputs.p_rad_core_in > h:
        raise ValueError('Divertor Heat Ledger: p_rad_core_in exceeds p_heat_abs')
    s = checked('p_sep', h - inputs.p_rad_core_in)
    radiation = checked('p_rad_total', f * h, f > 0 and h > 0)
    edge = checked('p_rad_edge', radiation - inputs.p_rad_core_in)
    nonrad = checked('p_target_nonrad', h - radiation, f < 1 and h > 0)
    deposited = checked('p_target_deposited', c * nonrad, c > 0 and nonrad > 0)
    uncaptured = checked('p_nonrad_uncaptured', nonrad - deposited, c < 1 and nonrad > 0)
    edge_fraction = checked('f_rad_edge', edge / s) if s > 0 else 0.0
    edge_range = checked('f_rad_edge_in_range', edge_fraction * (1.0 - edge_fraction))
    # Preserve the original product-then-division arithmetic exactly.
    peak_product = checked('peak_product', qref * nonrad, qref > 0 and nonrad > 0)
    peak = checked('q_target_peak', peak_product / inputs.p_nonrad_ref_in, peak_product > 0)
    shadow_product = checked('shadow_product', peak * inputs.R_ref_in, peak > 0)
    shadow = checked('q_target_peak_area_scaled', shadow_product / inputs.R_in, shadow_product > 0)
    margin = checked('q_target_margin', inputs.q_target_limit_in - peak)
    installed_margin = checked('p_heat_operating_minus_installed', inputs.p_aux_required_in - inputs.p_installed_coupled_in)
    area = 0.0
    if qref > 0:
        reference_deposition = checked('reference_deposition', c * inputs.p_nonrad_ref_in, True)
        area = checked('peak_equivalent_area', reference_deposition / qref, True)
    # Native generated schema order, explicitly typed; all flags are Real 0/1.
    return (area, shadow, float(s > 0), float(qref > 0), h, edge_range,
            margin, radiation, nonrad, uncaptured, edge_fraction, deposited,
            edge, installed_margin, float(edge >= 0), s, peak)
