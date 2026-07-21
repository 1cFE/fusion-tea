"""Auto-generated implementation for Preconstruction_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_account_costs.sysml:356

SysML Expressions:
    n_mod = 1.0
    land_intensity = 0.25
    land_cost = 10000.0
    ref_net_power = 1000.0
    cost = land_intensity * (p_net * n_mod * ref_net_power) ** 0.5 * land_cost + fixed_precon
    
Documentation:
CAS10 preconstruction PRE-CONTINGENCY subtotal: land (sqrt of
plant-total net electric, anchored at ref_net_power) plus the fixed
adders (permits + licensing + studies + reports + other — fuel/FOAK-
keyed, so a concept input). costs.py:79 adds CAS10's own contingency;
deliberately NOT carried here — the plant's CAS29 applies contingency
once over the direct sum (convention preserved, MR-WI025-3; design-
stage check: 1cfe full CAS10 = this subtotal x 1.10 exactly).
*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:52-80 (cas10_preconstruction);
costing_constants.yaml:8, :15-23
*Basis**: CAS10 subtotal, contingency deliberately omitted (CAS29)
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.preconstruction_cost import Preconstruction_CostInput


def run_preconstruction_cost(inputs: Preconstruction_CostInput) -> float:
    """Execute Preconstruction_Cost calculation.

CAS10 preconstruction PRE-CONTINGENCY subtotal: land (sqrt of
plant-total net electric, anchored at ref_net_power) plus the fixed
adders (permits + licensing + studies + reports + other — fuel/FOAK-
keyed, so a concept input). costs.py:79 adds CAS10's own contingency;
deliberately NOT carried here — the plant's CAS29 applies contingency
once over the direct sum (convention preserved, MR-WI025-3; design-
stage check: 1cfe full CAS10 = this subtotal x 1.10 exactly).
*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:52-80 (cas10_preconstruction);
costing_constants.yaml:8, :15-23
*Basis**: CAS10 subtotal, contingency deliberately omitted (CAS29)

SysML Source: root-0/analyses/mfe_account_costs.sysml:356

SysML Expressions:
    n_mod = 1.0
    land_intensity = 0.25
    land_cost = 10000.0
    ref_net_power = 1000.0
    cost = land_intensity * (p_net * n_mod * ref_net_power) ** 0.5 * land_cost + fixed_precon
    
Documentation:
CAS10 preconstruction PRE-CONTINGENCY subtotal: land (sqrt of
plant-total net electric, anchored at ref_net_power) plus the fixed
adders (permits + licensing + studies + reports + other — fuel/FOAK-
keyed, so a concept input). costs.py:79 adds CAS10's own contingency;
deliberately NOT carried here — the plant's CAS29 applies contingency
once over the direct sum (convention preserved, MR-WI025-3; design-
stage check: 1cfe full CAS10 = this subtotal x 1.10 exactly).
*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:52-80 (cas10_preconstruction);
costing_constants.yaml:8, :15-23
*Basis**: CAS10 subtotal, contingency deliberately omitted (CAS29)

Args:
    inputs: Input parameters validated against Preconstruction_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Preconstruction_CostInput(...)
    >>> result = run_preconstruction_cost(inputs)
    """
    return (((inputs.land_intensity * (((inputs.p_net * inputs.n_mod) * inputs.ref_net_power) ** 0.5)) * inputs.land_cost) + inputs.fixed_precon)
