"""Annual_OM_CostModule Module Wrapper

TEAx module for Annual_OM_Cost calculation.

CAS70 UNLEVELIZED annual O&M: fuel-keyed staffing base (om_ref, a
concept input) scaled by sqrt of plant-total net electric. CAS71
inflation levelization and CAS72 scheduled replacement are documented
Stage-3 refinements, not carried (convention preserved, MR-WI025-3).
om_direct is an additive direct term for concepts that specify O&M
outright (WI-024 p_direct pattern); 0 -> pure costs.py:353 formula,
and with om_ref = 0 the calc passes om_direct through exactly (IEEE-
exact identity, the handshake injection path -- WI-025 D5/D6).
*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:319-357 (cas70_om; annual line :353);
costing_constants.yaml:272 (om_cost_dt 54.9), :8 (ref 1000)
*Basis**: staffing power-law O&M, unlevelized (CAS71/72 out of scope)

Inputs:
    - alpha: alpha parameter
    - ref_net_power: ref_net_power parameter
    - n_mod_in: n_mod_in parameter
    - om_direct: om_direct parameter
    - p_net: p_net parameter
    - om_ref: om_ref parameter

Outputs:
    - annual_om: annual_om result

SysML Source: root-0/analyses/mfe_account_costs.sysml:403

SysML Source: root-0/analyses/mfe_account_costs.sysml:403

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/annual_om_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Annual_OM_CostInput(BaseModel):
    """Input model for Annual_OM_CostModule.

    Attributes:
        alpha: alpha input
        ref_net_power: ref_net_power input
        n_mod_in: n_mod_in input
        om_direct: om_direct input
        p_net: p_net input
        om_ref: om_ref input
    """
    alpha: float = Field(..., description="alpha input")
    ref_net_power: float = Field(..., description="ref_net_power input")
    n_mod_in: float = Field(..., description="n_mod_in input")
    om_direct: float = Field(..., description="om_direct input")
    p_net: float = Field(..., description="p_net input")
    om_ref: float = Field(..., description="om_ref input")


class Annual_OM_CostModule(ModuleBase[Annual_OM_CostInput, Float]):
    """TEAx module for Annual_OM_Cost calculation.

CAS70 UNLEVELIZED annual O&M: fuel-keyed staffing base (om_ref, a
concept input) scaled by sqrt of plant-total net electric. CAS71
inflation levelization and CAS72 scheduled replacement are documented
Stage-3 refinements, not carried (convention preserved, MR-WI025-3).
om_direct is an additive direct term for concepts that specify O&M
outright (WI-024 p_direct pattern); 0 -> pure costs.py:353 formula,
and with om_ref = 0 the calc passes om_direct through exactly (IEEE-
exact identity, the handshake injection path -- WI-025 D5/D6).
*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:319-357 (cas70_om; annual line :353);
costing_constants.yaml:272 (om_cost_dt 54.9), :8 (ref 1000)
*Basis**: staffing power-law O&M, unlevelized (CAS71/72 out of scope)

Inputs:
    - alpha: alpha parameter
    - ref_net_power: ref_net_power parameter
    - n_mod_in: n_mod_in parameter
    - om_direct: om_direct parameter
    - p_net: p_net parameter
    - om_ref: om_ref parameter

Outputs:
    - annual_om: annual_om result

SysML Source: root-0/analyses/mfe_account_costs.sysml:403

    SysML Source: root-0/analyses/mfe_account_costs.sysml:403

    Calculation Specification:
        n_mod_in = 1.0
        ref_net_power = 1000.0
        alpha = 0.5
        om_direct = 0.0
        annual_om = om_ref * (p_net * n_mod_in / ref_net_power) ** alpha + om_direct
        
Documentation:
CAS70 UNLEVELIZED annual O&M: fuel-keyed staffing base (om_ref, a
concept input) scaled by sqrt of plant-total net electric. CAS71
inflation levelization and CAS72 scheduled replacement are documented
Stage-3 refinements, not carried (convention preserved, MR-WI025-3).
om_direct is an additive direct term for concepts that specify O&M
outright (WI-024 p_direct pattern); 0 -> pure costs.py:353 formula,
and with om_ref = 0 the calc passes om_direct through exactly (IEEE-
exact identity, the handshake injection path -- WI-025 D5/D6).
*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:319-357 (cas70_om; annual line :353);
costing_constants.yaml:272 (om_cost_dt 54.9), :8 (ref 1000)
*Basis**: staffing power-law O&M, unlevelized (CAS71/72 out of scope)

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.annual_om_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Annual_OM_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, alpha: float, ref_net_power: float, n_mod_in: float, om_direct: float, p_net: float, om_ref: float    ) -> Annual_OM_CostInput:
        """Validate inputs and fill defaults.

        Args:
            alpha: alpha input
            ref_net_power: ref_net_power input
            n_mod_in: n_mod_in input
            om_direct: om_direct input
            p_net: p_net input
            om_ref: om_ref input

        Returns:
            Validated input model
        """
        return Annual_OM_CostInput(alpha=alpha, ref_net_power=ref_net_power, n_mod_in=n_mod_in, om_direct=om_direct, p_net=p_net, om_ref=om_ref)

    def run(
        self, alpha: float, ref_net_power: float, n_mod_in: float, om_direct: float, p_net: float, om_ref: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            alpha: alpha input
            ref_net_power: ref_net_power input
            n_mod_in: n_mod_in input
            om_direct: om_direct input
            p_net: p_net input
            om_ref: om_ref input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(alpha, ref_net_power, n_mod_in, om_direct, p_net, om_ref)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.annual_om_cost_impl import (
            run_annual_om_cost,
        )

        # Execute implementation - returns single value
        annual_om = run_annual_om_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(annual_om))
