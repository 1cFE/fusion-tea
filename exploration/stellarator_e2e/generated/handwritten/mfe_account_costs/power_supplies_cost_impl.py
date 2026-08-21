"""Auto-generated implementation for Power_Supplies_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_account_costs.sysml:140

SysML Expressions:
    p_et_ref = 1100.0
    alpha = 0.7
    cost = base * (p_et / p_et_ref) ** alpha
    
Documentation:
CAS22.1.7 Power supplies (steady-state: high-current DC for SC magnets,
switchgear). Power-law in gross electric:

  cost = base * (p_et/p_et_ref)^alpha

`base` is the account cost at the calibration power (power_supplies_base,
M$ at 1 GWe in the source) — a concept input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:554 (c220107 steady-state), cas22.py:224 (P_ET_REF)
*Basis**: Power-scaled power-supply cost
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.power_supplies_cost import Power_Supplies_CostInput


def run_power_supplies_cost(inputs: Power_Supplies_CostInput) -> float:
    """Execute Power_Supplies_Cost calculation.

CAS22.1.7 Power supplies (steady-state: high-current DC for SC magnets,
switchgear). Power-law in gross electric:

  cost = base * (p_et/p_et_ref)^alpha

`base` is the account cost at the calibration power (power_supplies_base,
M$ at 1 GWe in the source) — a concept input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:554 (c220107 steady-state), cas22.py:224 (P_ET_REF)
*Basis**: Power-scaled power-supply cost

SysML Source: root-0/analyses/mfe_account_costs.sysml:140

SysML Expressions:
    p_et_ref = 1100.0
    alpha = 0.7
    cost = base * (p_et / p_et_ref) ** alpha
    
Documentation:
CAS22.1.7 Power supplies (steady-state: high-current DC for SC magnets,
switchgear). Power-law in gross electric:

  cost = base * (p_et/p_et_ref)^alpha

`base` is the account cost at the calibration power (power_supplies_base,
M$ at 1 GWe in the source) — a concept input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:554 (c220107 steady-state), cas22.py:224 (P_ET_REF)
*Basis**: Power-scaled power-supply cost

Args:
    inputs: Input parameters validated against Power_Supplies_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Power_Supplies_CostInput(...)
    >>> result = run_power_supplies_cost(inputs)
    """
    return (inputs.base * ((inputs.p_et / inputs.p_et_ref) ** inputs.alpha))
