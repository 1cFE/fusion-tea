"""Auto-generated implementation for Indirect_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_account_costs.sysml:276

SysML Expressions:
    reference_construction_time = 6.0
    cost = indirect_fraction * direct_cost * (construction_time / reference_construction_time)
    
Documentation:
CAS30 indirect service costs, a fraction of total direct cost scaled by
construction time relative to a reference duration:

  cost = indirect_fraction * direct_cost
(construction_time / reference_construction_time)

`indirect_fraction` (0.20 of direct in the source) is a concept input.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:231-236 (cas30_indirect)
*Basis**: Direct-cost fraction scaled by construction-time ratio
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.indirect_cost import Indirect_CostInput


def run_indirect_cost(inputs: Indirect_CostInput) -> float:
    """Execute Indirect_Cost calculation.

CAS30 indirect service costs, a fraction of total direct cost scaled by
construction time relative to a reference duration:

  cost = indirect_fraction * direct_cost
(construction_time / reference_construction_time)

`indirect_fraction` (0.20 of direct in the source) is a concept input.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:231-236 (cas30_indirect)
*Basis**: Direct-cost fraction scaled by construction-time ratio

SysML Source: root-0/analyses/mfe_account_costs.sysml:276

SysML Expressions:
    reference_construction_time = 6.0
    cost = indirect_fraction * direct_cost * (construction_time / reference_construction_time)
    
Documentation:
CAS30 indirect service costs, a fraction of total direct cost scaled by
construction time relative to a reference duration:

  cost = indirect_fraction * direct_cost
(construction_time / reference_construction_time)

`indirect_fraction` (0.20 of direct in the source) is a concept input.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:231-236 (cas30_indirect)
*Basis**: Direct-cost fraction scaled by construction-time ratio

Args:
    inputs: Input parameters validated against Indirect_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Indirect_CostInput(...)
    >>> result = run_indirect_cost(inputs)
    """
    return ((inputs.indirect_fraction * inputs.direct_cost) * (inputs.construction_time / inputs.reference_construction_time))
