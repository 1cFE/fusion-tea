"""Auto-generated implementation for IDC_Closed_Form_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_account_costs.sysml:601

SysML Expressions:
    f_idc = ((1.0 + interest_rate) ** construction_years - 1.0) / (interest_rate * construction_years) - 1.0
    cost = f_idc * overnight_cost
    
Documentation:
CAS60 interest-during-construction line (closed form, uniform spend):

  f_idc = ((1 + interest_rate) ** construction_years - 1)
          / (interest_rate * construction_years) - 1
  cost  = f_idc * overnight_cost

Variable real exponent construction_years — the idc_factor precedent
(mfe_lcoe_dcf.sysml:47) proves the codegen envelope handles it. WI-028
Option C (owner-ruled): this line is A-2-checked and reported but
EXCLUDED from total_capital; the DCF idc_factor is untouched.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:286-297 (cas60_idc)
*Basis**: Uniform-spend closed-form interest during construction
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.idc_closed_form_cost import IDC_Closed_Form_CostInput


def run_idc_closed_form_cost(inputs: IDC_Closed_Form_CostInput) -> float:
    """Execute IDC_Closed_Form_Cost calculation.

CAS60 interest-during-construction line (closed form, uniform spend):

  f_idc = ((1 + interest_rate) ** construction_years - 1)
          / (interest_rate * construction_years) - 1
  cost  = f_idc * overnight_cost

Variable real exponent construction_years — the idc_factor precedent
(mfe_lcoe_dcf.sysml:47) proves the codegen envelope handles it. WI-028
Option C (owner-ruled): this line is A-2-checked and reported but
EXCLUDED from total_capital; the DCF idc_factor is untouched.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:286-297 (cas60_idc)
*Basis**: Uniform-spend closed-form interest during construction

SysML Source: root-0/analyses/mfe_account_costs.sysml:601

SysML Expressions:
    f_idc = ((1.0 + interest_rate) ** construction_years - 1.0) / (interest_rate * construction_years) - 1.0
    cost = f_idc * overnight_cost
    
Documentation:
CAS60 interest-during-construction line (closed form, uniform spend):

  f_idc = ((1 + interest_rate) ** construction_years - 1)
          / (interest_rate * construction_years) - 1
  cost  = f_idc * overnight_cost

Variable real exponent construction_years — the idc_factor precedent
(mfe_lcoe_dcf.sysml:47) proves the codegen envelope handles it. WI-028
Option C (owner-ruled): this line is A-2-checked and reported but
EXCLUDED from total_capital; the DCF idc_factor is untouched.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:286-297 (cas60_idc)
*Basis**: Uniform-spend closed-form interest during construction

Args:
    inputs: Input parameters validated against IDC_Closed_Form_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = IDC_Closed_Form_CostInput(...)
    >>> result = run_idc_closed_form_cost(inputs)
    """
    f_idc = (((((1.0 + inputs.interest_rate) ** inputs.construction_years) - 1.0) / (inputs.interest_rate * inputs.construction_years)) - 1.0)
    return (f_idc * inputs.overnight_cost)
