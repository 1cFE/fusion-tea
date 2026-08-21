"""Auto-generated implementation for Aux_Cooling_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_account_costs.sysml:559

SysML Expressions:
    n_mod_in = 1.0
    p_cryo_ref = 30.0
    alpha = 0.7
    cost = aux_per_mw_in * (n_mod_in * p_th_in) + cryo_base * (p_cryo / p_cryo_ref) ** alpha
    
Documentation:
Auxiliary cooling + cryoplant account:

  cost = aux_per_mw * (n_mod * p_th) + cryo_base * (p_cryo / p_cryo_ref) ** alpha

aux term linear in plant-total thermal; cryoplant power-law in
per-module cryo electric power (NOT scaled by n_mod -- each module has
its own cryoplant).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:693-695 (c220300); p_cryo_ref 30 (:694), alpha 0.7 (:694)
*Basis**: Plant-total aux + per-module cryoplant power law
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.aux_cooling_cost import Aux_Cooling_CostInput


def run_aux_cooling_cost(inputs: Aux_Cooling_CostInput) -> float:
    """Execute Aux_Cooling_Cost calculation.

Auxiliary cooling + cryoplant account:

  cost = aux_per_mw * (n_mod * p_th) + cryo_base * (p_cryo / p_cryo_ref) ** alpha

aux term linear in plant-total thermal; cryoplant power-law in
per-module cryo electric power (NOT scaled by n_mod -- each module has
its own cryoplant).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:693-695 (c220300); p_cryo_ref 30 (:694), alpha 0.7 (:694)
*Basis**: Plant-total aux + per-module cryoplant power law

SysML Source: root-0/analyses/mfe_account_costs.sysml:559

SysML Expressions:
    n_mod_in = 1.0
    p_cryo_ref = 30.0
    alpha = 0.7
    cost = aux_per_mw_in * (n_mod_in * p_th_in) + cryo_base * (p_cryo / p_cryo_ref) ** alpha
    
Documentation:
Auxiliary cooling + cryoplant account:

  cost = aux_per_mw * (n_mod * p_th) + cryo_base * (p_cryo / p_cryo_ref) ** alpha

aux term linear in plant-total thermal; cryoplant power-law in
per-module cryo electric power (NOT scaled by n_mod -- each module has
its own cryoplant).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:693-695 (c220300); p_cryo_ref 30 (:694), alpha 0.7 (:694)
*Basis**: Plant-total aux + per-module cryoplant power law

Args:
    inputs: Input parameters validated against Aux_Cooling_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Aux_Cooling_CostInput(...)
    >>> result = run_aux_cooling_cost(inputs)
    """
    return ((inputs.aux_per_mw_in * (inputs.n_mod_in * inputs.p_th_in)) + (inputs.cryo_base * ((inputs.p_cryo / inputs.p_cryo_ref) ** inputs.alpha)))
