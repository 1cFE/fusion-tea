"""WI-066 conditional fuel conservation and numerical breeding screen.

Authority: models/library/analyses/mfe_tritium_breeding.sysml and WI-066 spec.
Invalid numerical carriers are explicitly undefined; defined_flag prevents a pass.
This numerical screen is not a physical confidence bound or plant qualification.
"""
import math
from stellarator_materials_reference_tea.modules.mfe_tritium_breeding.tritium_breeding_adequacy import Tritium_Breeding_AdequacyInput

AUTO_IMPLEMENTED = False


def run_tritium_breeding_adequacy(inputs: Tritium_Breeding_AdequacyInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float, float]:
    invalid = (0.0,) * 12
    p = inputs
    if not all(math.isfinite(getattr(p, name)) for name in type(p).model_fields):
        return invalid
    if not (p.burn_rate_in > 0 and 0 < p.burn_fraction_in <= 1
            and 0 < p.eta_extract_in <= 1 and 0 <= p.t_recycle_in <= 1
            and p.tbr_floor_in > 0 and p.tbr_required_in > 0
            and p.defined_in in (0.0, 1.0)):
        return invalid
    if min(p.loss_rate_in, p.lambda_T_in, p.I_total_in, p.G_stock_in) < 0:
        return invalid
    decay = p.lambda_T_in * p.I_total_in
    expected_loss = (1 - p.t_recycle_in) * (p.burn_rate_in / p.burn_fraction_in - p.burn_rate_in)
    numerator = p.burn_rate_in + p.loss_rate_in + decay + p.G_stock_in
    denominator = p.eta_extract_in * p.burn_rate_in
    if not all(math.isfinite(x) for x in (decay, expected_loss, numerator, denominator)) or denominator <= 0:
        return invalid
    expected_requirement = numerator / denominator
    if not math.isfinite(expected_requirement):
        return invalid
    if not (math.isclose(p.loss_rate_in, expected_loss, rel_tol=1e-12, abs_tol=0.0)
            and math.isclose(p.tbr_required_in, expected_requirement, rel_tol=1e-12, abs_tol=0.0)):
        return invalid
    requirement = max(p.tbr_floor_in, p.tbr_required_in)
    if p.defined_in == 0:
        # Non-breeding streams and the valid requirement remain interpretable.
        return (0.0, decay, 0.0, 0.0, p.loss_rate_in, 0.0, requirement,
                0.0, 0.0, p.G_stock_in, 0.0, 0.0)
    if p.tbr_mean_in < 0 or p.tbr_lower_in > p.tbr_mean_in:
        return invalid
    production = p.tbr_mean_in * p.burn_rate_in
    extracted = p.eta_extract_in * production
    extraction_loss = (1 - p.eta_extract_in) * production
    balance = extracted - p.burn_rate_in - p.loss_rate_in - decay - p.G_stock_in
    values = (p.tbr_mean_in - p.tbr_floor_in, decay,
              p.tbr_mean_in - p.tbr_required_in, extracted, p.loss_rate_in,
              1.0, requirement, balance, extraction_loss, p.G_stock_in,
              p.tbr_lower_in - requirement, production)
    return values if all(math.isfinite(x) for x in values) else invalid
