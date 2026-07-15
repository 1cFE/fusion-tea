"""Auto-generated implementation for Blanket_Cost.

AUTO_IMPLEMENTED = True

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:22

SysML Expressions:
    p_th_ref = 2500.0
    alpha = 0.6
    cost = unit_cost * structure_factor * blanket_vol * (p_th / p_th_ref) ** alpha
    
Documentation:
CAS22.1.1 First-wall + blanket + neutron-multiplier cost. Hybrid
volume x thermal-power scaling:

  cost = unit_cost * structure_factor * blanket_vol * (p_th/p_th_ref)^alpha

`unit_cost` is the fuel- and fill-chemistry-effective blanket unit cost
(fuel-keyed table with a Li2O override in the source); `structure_factor`
is the blanket-form multiplier. Both are concept inputs (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:252-254 (c220101), cas22.py:223 (P_TH_REF=2500)
*Basis**: Volume-based blanket cost with thermal-intensity power law
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.blanket_cost import Blanket_CostInput


def run_blanket_cost(inputs: Blanket_CostInput) -> float:
    """Execute Blanket_Cost calculation.

CAS22.1.1 First-wall + blanket + neutron-multiplier cost. Hybrid
volume x thermal-power scaling:

  cost = unit_cost * structure_factor * blanket_vol * (p_th/p_th_ref)^alpha

`unit_cost` is the fuel- and fill-chemistry-effective blanket unit cost
(fuel-keyed table with a Li2O override in the source); `structure_factor`
is the blanket-form multiplier. Both are concept inputs (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:252-254 (c220101), cas22.py:223 (P_TH_REF=2500)
*Basis**: Volume-based blanket cost with thermal-intensity power law

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:22

SysML Expressions:
    p_th_ref = 2500.0
    alpha = 0.6
    cost = unit_cost * structure_factor * blanket_vol * (p_th / p_th_ref) ** alpha
    
Documentation:
CAS22.1.1 First-wall + blanket + neutron-multiplier cost. Hybrid
volume x thermal-power scaling:

  cost = unit_cost * structure_factor * blanket_vol * (p_th/p_th_ref)^alpha

`unit_cost` is the fuel- and fill-chemistry-effective blanket unit cost
(fuel-keyed table with a Li2O override in the source); `structure_factor`
is the blanket-form multiplier. Both are concept inputs (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:252-254 (c220101), cas22.py:223 (P_TH_REF=2500)
*Basis**: Volume-based blanket cost with thermal-intensity power law

Args:
    inputs: Input parameters validated against Blanket_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Blanket_CostInput(...)
    >>> result = run_blanket_cost(inputs)
    """
    return (((inputs.unit_cost * inputs.structure_factor) * inputs.blanket_vol) * ((inputs.p_th / inputs.p_th_ref) ** inputs.alpha))
