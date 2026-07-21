"""Auto-generated implementation for Remote_Handling_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_account_costs.sysml:456

SysML Expressions:
    p_et_ref = 1100.0
    alpha = 0.5
    cost = base * concept_scale * (p_et / p_et_ref) ** alpha
    
Documentation:
Remote-handling account:

  cost = base * concept_scale * (p_et / p_et_ref) ** alpha

p_et is per-module gross electric (no n_mod). concept_scale is 1.0
toroidal (tok/stell), 0.55 end-access — a concept input (MR-3), NOT a
library default.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:631-645 (c220110); cas22.py:224 (P_ET_REF ref_gross 1100)
*Basis**: Per-module gross-electric power law, concept-scaled
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.remote_handling_cost import Remote_Handling_CostInput


def run_remote_handling_cost(inputs: Remote_Handling_CostInput) -> float:
    """Execute Remote_Handling_Cost calculation.

Remote-handling account:

  cost = base * concept_scale * (p_et / p_et_ref) ** alpha

p_et is per-module gross electric (no n_mod). concept_scale is 1.0
toroidal (tok/stell), 0.55 end-access — a concept input (MR-3), NOT a
library default.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:631-645 (c220110); cas22.py:224 (P_ET_REF ref_gross 1100)
*Basis**: Per-module gross-electric power law, concept-scaled

SysML Source: root-0/analyses/mfe_account_costs.sysml:456

SysML Expressions:
    p_et_ref = 1100.0
    alpha = 0.5
    cost = base * concept_scale * (p_et / p_et_ref) ** alpha
    
Documentation:
Remote-handling account:

  cost = base * concept_scale * (p_et / p_et_ref) ** alpha

p_et is per-module gross electric (no n_mod). concept_scale is 1.0
toroidal (tok/stell), 0.55 end-access — a concept input (MR-3), NOT a
library default.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:631-645 (c220110); cas22.py:224 (P_ET_REF ref_gross 1100)
*Basis**: Per-module gross-electric power law, concept-scaled

Args:
    inputs: Input parameters validated against Remote_Handling_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Remote_Handling_CostInput(...)
    >>> result = run_remote_handling_cost(inputs)
    """
    return ((inputs.base * inputs.concept_scale) * ((inputs.p_et / inputs.p_et_ref) ** inputs.alpha))
