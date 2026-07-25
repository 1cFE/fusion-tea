"""Auto-generated implementation for Coolant_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_account_costs.sysml:504

SysML Expressions:
    n_mod = 1.0
    ref_net_power = 1000.0
    p_th_ref = 3500.0
    alpha = 0.55
    cost = primary_base * (n_mod * p_net / ref_net_power) + intermediate_base * (n_mod * p_th / p_th_ref) ** alpha
    
Documentation:
Coolant account (two-term, plant-total):

  cost = primary_base * (n_mod * p_net / ref_net_power)
       + intermediate_base * (n_mod * p_th / p_th_ref) ** alpha

primary linear in plant-total net; intermediate power-law in plant-total
thermal.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:684-686 (c220200); ref_net 1000 (:684), p_th_ref 3500 (:685), alpha 0.55 (:685)
*Basis**: Plant-total two-term coolant cost
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.coolant_cost import Coolant_CostInput


def run_coolant_cost(inputs: Coolant_CostInput) -> float:
    """Execute Coolant_Cost calculation.

Coolant account (two-term, plant-total):

  cost = primary_base * (n_mod * p_net / ref_net_power)
       + intermediate_base * (n_mod * p_th / p_th_ref) ** alpha

primary linear in plant-total net; intermediate power-law in plant-total
thermal.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:684-686 (c220200); ref_net 1000 (:684), p_th_ref 3500 (:685), alpha 0.55 (:685)
*Basis**: Plant-total two-term coolant cost

SysML Source: root-0/analyses/mfe_account_costs.sysml:504

SysML Expressions:
    n_mod = 1.0
    ref_net_power = 1000.0
    p_th_ref = 3500.0
    alpha = 0.55
    cost = primary_base * (n_mod * p_net / ref_net_power) + intermediate_base * (n_mod * p_th / p_th_ref) ** alpha
    
Documentation:
Coolant account (two-term, plant-total):

  cost = primary_base * (n_mod * p_net / ref_net_power)
       + intermediate_base * (n_mod * p_th / p_th_ref) ** alpha

primary linear in plant-total net; intermediate power-law in plant-total
thermal.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:684-686 (c220200); ref_net 1000 (:684), p_th_ref 3500 (:685), alpha 0.55 (:685)
*Basis**: Plant-total two-term coolant cost

Args:
    inputs: Input parameters validated against Coolant_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Coolant_CostInput(...)
    >>> result = run_coolant_cost(inputs)
    """
    return ((inputs.primary_base * ((inputs.n_mod * inputs.p_net) / inputs.ref_net_power)) + (inputs.intermediate_base * (((inputs.n_mod * inputs.p_th) / inputs.p_th_ref) ** inputs.alpha)))
