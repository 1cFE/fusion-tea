"""Auto-generated implementation for Vessel_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_account_costs.sysml:108

SysML Expressions:
    p_et_ref = 1100.0
    alpha = 0.6
    cost = unit_cost * vessel_vol * (p_et_in / p_et_ref) ** alpha
    
Documentation:
CAS22.1.6 Vacuum-vessel SHELL cost (double-walled SS chamber, port
extensions, gauges, leak detection). Volume x gross-electric scaling:

  cost = unit_cost * vessel_vol * (p_et/p_et_ref)^alpha

Reproduces only the volume-based vessel-shell sub-term (c220106_vessel).
The gas-load pumping sub-term (c220106_pump) is a within-envelope but
input-heavy expression (Boltzmann/charge constants, fuel-keyed E_fus,
NBI/fueling throughput); it is omitted here and left for Stage-3
deepening. See the plant doc's initial-model-limitations note.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:515 (c220106_vessel), cas22.py:224 (P_ET_REF)
*Basis**: Volume-based vessel-shell cost with gross-electric power law
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.vessel_cost import Vessel_CostInput


def run_vessel_cost(inputs: Vessel_CostInput) -> float:
    """Execute Vessel_Cost calculation.

CAS22.1.6 Vacuum-vessel SHELL cost (double-walled SS chamber, port
extensions, gauges, leak detection). Volume x gross-electric scaling:

  cost = unit_cost * vessel_vol * (p_et/p_et_ref)^alpha

Reproduces only the volume-based vessel-shell sub-term (c220106_vessel).
The gas-load pumping sub-term (c220106_pump) is a within-envelope but
input-heavy expression (Boltzmann/charge constants, fuel-keyed E_fus,
NBI/fueling throughput); it is omitted here and left for Stage-3
deepening. See the plant doc's initial-model-limitations note.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:515 (c220106_vessel), cas22.py:224 (P_ET_REF)
*Basis**: Volume-based vessel-shell cost with gross-electric power law

SysML Source: root-0/analyses/mfe_account_costs.sysml:108

SysML Expressions:
    p_et_ref = 1100.0
    alpha = 0.6
    cost = unit_cost * vessel_vol * (p_et_in / p_et_ref) ** alpha
    
Documentation:
CAS22.1.6 Vacuum-vessel SHELL cost (double-walled SS chamber, port
extensions, gauges, leak detection). Volume x gross-electric scaling:

  cost = unit_cost * vessel_vol * (p_et/p_et_ref)^alpha

Reproduces only the volume-based vessel-shell sub-term (c220106_vessel).
The gas-load pumping sub-term (c220106_pump) is a within-envelope but
input-heavy expression (Boltzmann/charge constants, fuel-keyed E_fus,
NBI/fueling throughput); it is omitted here and left for Stage-3
deepening. See the plant doc's initial-model-limitations note.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:515 (c220106_vessel), cas22.py:224 (P_ET_REF)
*Basis**: Volume-based vessel-shell cost with gross-electric power law

Args:
    inputs: Input parameters validated against Vessel_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Vessel_CostInput(...)
    >>> result = run_vessel_cost(inputs)
    """
    return ((inputs.unit_cost * inputs.vessel_vol) * ((inputs.p_et_in / inputs.p_et_ref) ** inputs.alpha))
