"""Auto-generated implementation for Installation_Labor_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_account_costs.sysml:483

SysML Expressions:
    installation_frac = 0.14
    cost = installation_frac * reactor_subtotal
    
Documentation:
Installation-labor account:

  cost = installation_frac * reactor_subtotal

reactor_subtotal = Σ(C220101..C220110) per-module (includes C220109 = 0
for this concept, excludes 111/112). The multi-unit labor factor (0.92)
is a plant-aggregate concern at n_mod > 1; the account value compared
under A-2 is single-module.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:652-664 (c220111); installation_frac cas22.py:664 (0.14)
*Basis**: Fixed fraction of the reactor-equipment subtotal
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.installation_labor_cost import Installation_Labor_CostInput


def run_installation_labor_cost(inputs: Installation_Labor_CostInput) -> float:
    """Execute Installation_Labor_Cost calculation.

Installation-labor account:

  cost = installation_frac * reactor_subtotal

reactor_subtotal = Σ(C220101..C220110) per-module (includes C220109 = 0
for this concept, excludes 111/112). The multi-unit labor factor (0.92)
is a plant-aggregate concern at n_mod > 1; the account value compared
under A-2 is single-module.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:652-664 (c220111); installation_frac cas22.py:664 (0.14)
*Basis**: Fixed fraction of the reactor-equipment subtotal

SysML Source: root-0/analyses/mfe_account_costs.sysml:483

SysML Expressions:
    installation_frac = 0.14
    cost = installation_frac * reactor_subtotal
    
Documentation:
Installation-labor account:

  cost = installation_frac * reactor_subtotal

reactor_subtotal = Σ(C220101..C220110) per-module (includes C220109 = 0
for this concept, excludes 111/112). The multi-unit labor factor (0.92)
is a plant-aggregate concern at n_mod > 1; the account value compared
under A-2 is single-module.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:652-664 (c220111); installation_frac cas22.py:664 (0.14)
*Basis**: Fixed fraction of the reactor-equipment subtotal

Args:
    inputs: Input parameters validated against Installation_Labor_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Installation_Labor_CostInput(...)
    >>> result = run_installation_labor_cost(inputs)
    """
    return (inputs.installation_frac * inputs.reactor_subtotal)
