import math
from wi052_probe.modules.mfe_account_costs.levelized_annual_cost import Levelized_Annual_CostInput
from wi052_probe.handwritten.mfe_account_costs.financial_factors import crf, annuity_pv, idc
AUTO_IMPLEMENTED = False
def run_levelized_annual_cost(inputs: Levelized_Annual_CostInput) -> tuple[float, float]:
    c = crf(inputs.interest_rate, inputs.operational_years_in)
    return c * annuity_pv(inputs.annual_cost, inputs.interest_rate, inputs.inflation_rate_in, inputs.operational_years_in, inputs.project_time), c
