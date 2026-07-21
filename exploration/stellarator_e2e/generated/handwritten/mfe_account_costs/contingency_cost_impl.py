"""Auto-generated implementation for Contingency_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_account_costs.sysml:255

SysML Expressions:
    cost = contingency_rate * direct_subtotal
    
Documentation:
CAS29 contingency on direct costs:

  cost = contingency_rate * direct_subtotal

`contingency_rate` is the FOAK/NOAK rate (0.10 FOAK, 0.0 NOAK in the
source) — a concept/maturity input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:220 (cas29_contingency)
*Basis**: Fractional contingency on the direct-cost subtotal
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.contingency_cost import Contingency_CostInput


def run_contingency_cost(inputs: Contingency_CostInput) -> float:
    """Execute Contingency_Cost calculation.

CAS29 contingency on direct costs:

  cost = contingency_rate * direct_subtotal

`contingency_rate` is the FOAK/NOAK rate (0.10 FOAK, 0.0 NOAK in the
source) — a concept/maturity input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:220 (cas29_contingency)
*Basis**: Fractional contingency on the direct-cost subtotal

SysML Source: root-0/analyses/mfe_account_costs.sysml:255

SysML Expressions:
    cost = contingency_rate * direct_subtotal
    
Documentation:
CAS29 contingency on direct costs:

  cost = contingency_rate * direct_subtotal

`contingency_rate` is the FOAK/NOAK rate (0.10 FOAK, 0.0 NOAK in the
source) — a concept/maturity input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:220 (cas29_contingency)
*Basis**: Fractional contingency on the direct-cost subtotal

Args:
    inputs: Input parameters validated against Contingency_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Contingency_CostInput(...)
    >>> result = run_contingency_cost(inputs)
    """
    return (inputs.contingency_rate * inputs.direct_subtotal)
