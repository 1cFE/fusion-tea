"""Auto-generated implementation for Annual_OM_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_account_costs.sysml:387

SysML Expressions:
    n_mod = 1.0
    ref_net_power = 1000.0
    alpha = 0.5
    om_direct = 0.0
    annual_om = om_ref * (p_net * n_mod / ref_net_power) ** alpha + om_direct
    
Documentation:
CAS70 UNLEVELIZED annual O&M: fuel-keyed staffing base (om_ref, a
concept input) scaled by sqrt of plant-total net electric. CAS71
inflation levelization and CAS72 scheduled replacement are documented
Stage-3 refinements, not carried (convention preserved, MR-WI025-3).
om_direct is an additive direct term for concepts that specify O&M
outright (WI-024 p_direct pattern); 0 -> pure costs.py:353 formula,
and with om_ref = 0 the calc passes om_direct through exactly (IEEE-
exact identity, the handshake injection path — WI-025 D5/D6).
*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:319-357 (cas70_om; annual line :353);
costing_constants.yaml:272 (om_cost_dt 54.9), :8 (ref 1000)
*Basis**: staffing power-law O&M, unlevelized (CAS71/72 out of scope)
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.annual_om_cost import Annual_OM_CostInput


def run_annual_om_cost(inputs: Annual_OM_CostInput) -> float:
    """Execute Annual_OM_Cost calculation.

CAS70 UNLEVELIZED annual O&M: fuel-keyed staffing base (om_ref, a
concept input) scaled by sqrt of plant-total net electric. CAS71
inflation levelization and CAS72 scheduled replacement are documented
Stage-3 refinements, not carried (convention preserved, MR-WI025-3).
om_direct is an additive direct term for concepts that specify O&M
outright (WI-024 p_direct pattern); 0 -> pure costs.py:353 formula,
and with om_ref = 0 the calc passes om_direct through exactly (IEEE-
exact identity, the handshake injection path — WI-025 D5/D6).
*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:319-357 (cas70_om; annual line :353);
costing_constants.yaml:272 (om_cost_dt 54.9), :8 (ref 1000)
*Basis**: staffing power-law O&M, unlevelized (CAS71/72 out of scope)

SysML Source: root-0/analyses/mfe_account_costs.sysml:387

SysML Expressions:
    n_mod = 1.0
    ref_net_power = 1000.0
    alpha = 0.5
    om_direct = 0.0
    annual_om = om_ref * (p_net * n_mod / ref_net_power) ** alpha + om_direct
    
Documentation:
CAS70 UNLEVELIZED annual O&M: fuel-keyed staffing base (om_ref, a
concept input) scaled by sqrt of plant-total net electric. CAS71
inflation levelization and CAS72 scheduled replacement are documented
Stage-3 refinements, not carried (convention preserved, MR-WI025-3).
om_direct is an additive direct term for concepts that specify O&M
outright (WI-024 p_direct pattern); 0 -> pure costs.py:353 formula,
and with om_ref = 0 the calc passes om_direct through exactly (IEEE-
exact identity, the handshake injection path — WI-025 D5/D6).
*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:319-357 (cas70_om; annual line :353);
costing_constants.yaml:272 (om_cost_dt 54.9), :8 (ref 1000)
*Basis**: staffing power-law O&M, unlevelized (CAS71/72 out of scope)

Args:
    inputs: Input parameters validated against Annual_OM_CostInput schema

Returns:
    float: annual_om

Example:
    >>> inputs = Annual_OM_CostInput(...)
    >>> result = run_annual_om_cost(inputs)
    """
    return ((inputs.om_ref * (((inputs.p_net * inputs.n_mod) / inputs.ref_net_power) ** inputs.alpha)) + inputs.om_direct)
