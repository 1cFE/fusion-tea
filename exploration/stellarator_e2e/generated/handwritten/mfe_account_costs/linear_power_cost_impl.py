"""Auto-generated implementation for Linear_Power_Cost.

AUTO_IMPLEMENTED = True

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:226

SysML Expressions:
    n_mod = 1.0
    cost = n_mod * power * cost_per_mw
    
Documentation:
Generic balance-of-plant account cost linear in plant-total power:

  cost = n_mod * power * cost_per_mw

Reused for the four flat BOP accounts, each with its own driving power
and per-MW unit cost (concept/power-cycle inputs, WI-011):
  - Turbine plant       : power = p_the,  turbine_per_mw
  - Electric plant      : power = p_et,   electric_per_mw
  - Heat rejection      : power = p_th,   heat_rej_per_mw
  - Miscellaneous plant : power = p_et,   misc_per_mw

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:154 (turbine), :162 (electric), :170 (misc), :179 (heat_rej)
*Basis**: Balance-of-plant cost linear in plant-total driving power
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.linear_power_cost import Linear_Power_CostInput


def run_linear_power_cost(inputs: Linear_Power_CostInput) -> float:
    """Execute Linear_Power_Cost calculation.

Generic balance-of-plant account cost linear in plant-total power:

  cost = n_mod * power * cost_per_mw

Reused for the four flat BOP accounts, each with its own driving power
and per-MW unit cost (concept/power-cycle inputs, WI-011):
  - Turbine plant       : power = p_the,  turbine_per_mw
  - Electric plant      : power = p_et,   electric_per_mw
  - Heat rejection      : power = p_th,   heat_rej_per_mw
  - Miscellaneous plant : power = p_et,   misc_per_mw

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:154 (turbine), :162 (electric), :170 (misc), :179 (heat_rej)
*Basis**: Balance-of-plant cost linear in plant-total driving power

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:226

SysML Expressions:
    n_mod = 1.0
    cost = n_mod * power * cost_per_mw
    
Documentation:
Generic balance-of-plant account cost linear in plant-total power:

  cost = n_mod * power * cost_per_mw

Reused for the four flat BOP accounts, each with its own driving power
and per-MW unit cost (concept/power-cycle inputs, WI-011):
  - Turbine plant       : power = p_the,  turbine_per_mw
  - Electric plant      : power = p_et,   electric_per_mw
  - Heat rejection      : power = p_th,   heat_rej_per_mw
  - Miscellaneous plant : power = p_et,   misc_per_mw

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:154 (turbine), :162 (electric), :170 (misc), :179 (heat_rej)
*Basis**: Balance-of-plant cost linear in plant-total driving power

Args:
    inputs: Input parameters validated against Linear_Power_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Linear_Power_CostInput(...)
    >>> result = run_linear_power_cost(inputs)
    """
    return ((inputs.n_mod * inputs.power) * inputs.cost_per_mw)
