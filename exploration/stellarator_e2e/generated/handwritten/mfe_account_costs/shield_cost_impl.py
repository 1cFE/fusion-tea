"""Auto-generated implementation for Shield_Cost.

AUTO_IMPLEMENTED = True

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:52

SysML Expressions:
    p_th_ref = 2500.0
    alpha = 0.6
    cost = unit_cost * shield_vol * shield_scale * (p_th / p_th_ref) ** alpha
    
Documentation:
CAS22.1.2 Shield (HT + LT + bioshield) cost. Volume x thermal-power
scaling with a fuel-dependent shield-mass scale factor:

  cost = unit_cost * shield_vol * shield_scale * (p_th/p_th_ref)^alpha

`shield_scale` is the fuel neutron-load factor (DT 1.0, DD 0.7, DHe3 0.3,
pB11 0.1 in the source) — a concept input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:267-269 (c220102), cas22.py:223 (P_TH_REF=2500)
*Basis**: Volume-based shield cost with fuel neutron-load scale
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.shield_cost import Shield_CostInput


def run_shield_cost(inputs: Shield_CostInput) -> float:
    """Execute Shield_Cost calculation.

CAS22.1.2 Shield (HT + LT + bioshield) cost. Volume x thermal-power
scaling with a fuel-dependent shield-mass scale factor:

  cost = unit_cost * shield_vol * shield_scale * (p_th/p_th_ref)^alpha

`shield_scale` is the fuel neutron-load factor (DT 1.0, DD 0.7, DHe3 0.3,
pB11 0.1 in the source) — a concept input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:267-269 (c220102), cas22.py:223 (P_TH_REF=2500)
*Basis**: Volume-based shield cost with fuel neutron-load scale

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:52

SysML Expressions:
    p_th_ref = 2500.0
    alpha = 0.6
    cost = unit_cost * shield_vol * shield_scale * (p_th / p_th_ref) ** alpha
    
Documentation:
CAS22.1.2 Shield (HT + LT + bioshield) cost. Volume x thermal-power
scaling with a fuel-dependent shield-mass scale factor:

  cost = unit_cost * shield_vol * shield_scale * (p_th/p_th_ref)^alpha

`shield_scale` is the fuel neutron-load factor (DT 1.0, DD 0.7, DHe3 0.3,
pB11 0.1 in the source) — a concept input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:267-269 (c220102), cas22.py:223 (P_TH_REF=2500)
*Basis**: Volume-based shield cost with fuel neutron-load scale

Args:
    inputs: Input parameters validated against Shield_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Shield_CostInput(...)
    >>> result = run_shield_cost(inputs)
    """
    return (((inputs.unit_cost * inputs.shield_vol) * inputs.shield_scale) * ((inputs.p_th / inputs.p_th_ref) ** inputs.alpha))
