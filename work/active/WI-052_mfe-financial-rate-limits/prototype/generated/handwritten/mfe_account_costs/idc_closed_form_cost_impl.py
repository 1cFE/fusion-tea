import math
from wi052_probe.modules.mfe_account_costs.idc_closed_form_cost import IDC_Closed_Form_CostInput
from wi052_probe.handwritten.mfe_account_costs.financial_factors import crf, annuity_pv, idc
AUTO_IMPLEMENTED = False
def run_idc_closed_form_cost(inputs: IDC_Closed_Form_CostInput) -> float:
    return idc(inputs.interest_rate, inputs.construction_years_in) * inputs.overnight_cost
