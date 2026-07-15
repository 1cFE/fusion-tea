"""Auto-generated implementation for Heating_Cost.

AUTO_IMPLEMENTED = True

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:196

SysML Expressions:
    cost = nbi_per_mw * p_nbi + icrf_per_mw * p_icrf + ecrh_per_mw * p_ecrh + lhcd_per_mw * p_lhcd
    
Documentation:
CAS22.1.4 Supplementary heating & current drive cost, steady-state MFE.
Sum of per-method installed power times per-MW cost:

  cost = nbi_per_mw*p_nbi + icrf_per_mw*p_icrf
       + ecrh_per_mw*p_ecrh + lhcd_per_mw*p_lhcd

All per-MW rates and delivered powers are the concept heating mix
(WI-011). Per-MW rates are ITER-procurement-calibrated in the source.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:454-459 (c220104 steady-state)
*Basis**: Linear per-method heating capital; MFE analogue of IFE ignition
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.heating_cost import Heating_CostInput


def run_heating_cost(inputs: Heating_CostInput) -> float:
    """Execute Heating_Cost calculation.

CAS22.1.4 Supplementary heating & current drive cost, steady-state MFE.
Sum of per-method installed power times per-MW cost:

  cost = nbi_per_mw*p_nbi + icrf_per_mw*p_icrf
       + ecrh_per_mw*p_ecrh + lhcd_per_mw*p_lhcd

All per-MW rates and delivered powers are the concept heating mix
(WI-011). Per-MW rates are ITER-procurement-calibrated in the source.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:454-459 (c220104 steady-state)
*Basis**: Linear per-method heating capital; MFE analogue of IFE ignition

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:196

SysML Expressions:
    cost = nbi_per_mw * p_nbi + icrf_per_mw * p_icrf + ecrh_per_mw * p_ecrh + lhcd_per_mw * p_lhcd
    
Documentation:
CAS22.1.4 Supplementary heating & current drive cost, steady-state MFE.
Sum of per-method installed power times per-MW cost:

  cost = nbi_per_mw*p_nbi + icrf_per_mw*p_icrf
       + ecrh_per_mw*p_ecrh + lhcd_per_mw*p_lhcd

All per-MW rates and delivered powers are the concept heating mix
(WI-011). Per-MW rates are ITER-procurement-calibrated in the source.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:454-459 (c220104 steady-state)
*Basis**: Linear per-method heating capital; MFE analogue of IFE ignition

Args:
    inputs: Input parameters validated against Heating_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Heating_CostInput(...)
    >>> result = run_heating_cost(inputs)
    """
    return ((((inputs.nbi_per_mw * inputs.p_nbi) + (inputs.icrf_per_mw * inputs.p_icrf)) + (inputs.ecrh_per_mw * inputs.p_ecrh)) + (inputs.lhcd_per_mw * inputs.p_lhcd))
