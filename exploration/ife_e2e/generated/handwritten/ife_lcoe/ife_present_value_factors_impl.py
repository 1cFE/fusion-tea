from math import exp, expm1, log1p
from ife_tea.modules.ife_lcoe.ife_present_value_factors import IFE_Present_Value_FactorsInput


def run_ife_present_value_factors(inputs: IFE_Present_Value_FactorsInput) -> tuple[float, float]:
    """Return operation then construction factors in native generated order."""
    rate = inputs.discount_rate_in
    construction = inputs.construction_years_in
    operation = inputs.operational_years_in
    if rate == 0.0:
        return operation, construction
    log_discount = log1p(rate)
    construction_factor = -expm1(-construction * log_discount) / rate
    operation_factor = exp(-construction * log_discount) * (-expm1(-operation * log_discount) / rate)
    return operation_factor, construction_factor
