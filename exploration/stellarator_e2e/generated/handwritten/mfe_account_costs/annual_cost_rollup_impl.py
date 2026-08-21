"""Auto-generated implementation for Annual_Cost_Rollup.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_account_costs.sysml:891

SysML Expressions:
    cas70 = cas71 + cas72
    annual_total = cas71 + cas72 + cas80
    
Documentation:
CAS70 = CAS71 + CAS72, and the total levelized annual cost the LCOE
numerator carries (CAS70 + CAS80). Pure addition -- it introduces no new
economics, it makes the two sums producer channels the DCF core and the
1cfe-form comparison channel can read.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/model.py (pin 0254385)
*Ref**: model.py:1483-1605 (c70 = c71 + c72; lcoe numerator c90 + c70 + c80);
economics.py:88-92 (compute_lcoe)
*Basis**: 1costingFE CAS70 composition and LCOE annual-cost numerator
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.annual_cost_rollup import Annual_Cost_RollupInput


def run_annual_cost_rollup(inputs: Annual_Cost_RollupInput) -> tuple[float, float]:
    """Execute Annual_Cost_Rollup calculation.

CAS70 = CAS71 + CAS72, and the total levelized annual cost the LCOE
numerator carries (CAS70 + CAS80). Pure addition -- it introduces no new
economics, it makes the two sums producer channels the DCF core and the
1cfe-form comparison channel can read.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/model.py (pin 0254385)
*Ref**: model.py:1483-1605 (c70 = c71 + c72; lcoe numerator c90 + c70 + c80);
economics.py:88-92 (compute_lcoe)
*Basis**: 1costingFE CAS70 composition and LCOE annual-cost numerator

SysML Source: root-0/analyses/mfe_account_costs.sysml:891

SysML Expressions:
    cas70 = cas71 + cas72
    annual_total = cas71 + cas72 + cas80
    
Documentation:
CAS70 = CAS71 + CAS72, and the total levelized annual cost the LCOE
numerator carries (CAS70 + CAS80). Pure addition -- it introduces no new
economics, it makes the two sums producer channels the DCF core and the
1cfe-form comparison channel can read.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/model.py (pin 0254385)
*Ref**: model.py:1483-1605 (c70 = c71 + c72; lcoe numerator c90 + c70 + c80);
economics.py:88-92 (compute_lcoe)
*Basis**: 1costingFE CAS70 composition and LCOE annual-cost numerator

Args:
    inputs: Input parameters validated against Annual_Cost_RollupInput schema

Returns:
    tuple[float, ...]: (cas70, annual_total)

Example:
    >>> inputs = Annual_Cost_RollupInput(...)
    >>> cas70, annual_total = run_annual_cost_rollup(inputs)
    """
    return (
        (inputs.cas71 + inputs.cas72),  # cas70
        ((inputs.cas71 + inputs.cas72) + inputs.cas80),  # annual_total
    )
