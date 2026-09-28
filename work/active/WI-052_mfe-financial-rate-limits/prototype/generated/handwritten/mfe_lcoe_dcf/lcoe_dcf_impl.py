import math
from wi052_probe.modules.mfe_lcoe_dcf.lcoe_dcf import LCOE_DCFInput
from wi052_probe.handwritten.mfe_account_costs.financial_factors import crf, annuity_pv, idc
AUTO_IMPLEMENTED = False
def run_lcoe_dcf(inputs: LCOE_DCFInput) -> float:
    c = crf(inputs.discount_rate_in, inputs.operational_years_in)
    midpoint = math.exp(inputs.construction_years_in / 2.0 * math.log1p(inputs.discount_rate_in))
    return (inputs.total_capital_in * midpoint * c + inputs.annual_om_in) / (8760.0 * inputs.net_electric_mw * inputs.availability_in)
