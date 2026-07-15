"""Auto-generated implementation for Divertor_Cost.

AUTO_IMPLEMENTED = True

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:168

SysML Expressions:
    p_th_ref = 1000.0
    alpha = 0.5
    cost = base * (p_th / p_th_ref) ** alpha
    
Documentation:
CAS22.1.8 Divertor (W monoblock cassettes on CuCrZr heat sinks) cost,
steady-state MFE. Power-law in thermal power:

  cost = base * (p_th/p_th_ref)^alpha

`base` is the account cost at the 1 GWth calibration point
(divertor_base) — a concept input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:570 (c220108 steady-state, divertor concepts)
*Basis**: Power-scaled divertor cost; MFE analogue of IFE target factory
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.divertor_cost import Divertor_CostInput


def run_divertor_cost(inputs: Divertor_CostInput) -> float:
    """Execute Divertor_Cost calculation.

CAS22.1.8 Divertor (W monoblock cassettes on CuCrZr heat sinks) cost,
steady-state MFE. Power-law in thermal power:

  cost = base * (p_th/p_th_ref)^alpha

`base` is the account cost at the 1 GWth calibration point
(divertor_base) — a concept input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:570 (c220108 steady-state, divertor concepts)
*Basis**: Power-scaled divertor cost; MFE analogue of IFE target factory

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:168

SysML Expressions:
    p_th_ref = 1000.0
    alpha = 0.5
    cost = base * (p_th / p_th_ref) ** alpha
    
Documentation:
CAS22.1.8 Divertor (W monoblock cassettes on CuCrZr heat sinks) cost,
steady-state MFE. Power-law in thermal power:

  cost = base * (p_th/p_th_ref)^alpha

`base` is the account cost at the 1 GWth calibration point
(divertor_base) — a concept input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:570 (c220108 steady-state, divertor concepts)
*Basis**: Power-scaled divertor cost; MFE analogue of IFE target factory

Args:
    inputs: Input parameters validated against Divertor_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Divertor_CostInput(...)
    >>> result = run_divertor_cost(inputs)
    """
    return (inputs.base * ((inputs.p_th / inputs.p_th_ref) ** inputs.alpha))
