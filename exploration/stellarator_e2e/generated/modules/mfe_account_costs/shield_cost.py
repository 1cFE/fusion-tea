"""Shield_CostModule Module Wrapper

TEAx module for Shield_Cost calculation.

CAS22.1.2 Shield (HT + LT + bioshield) cost. Volume x thermal-power
scaling with a fuel-dependent shield-mass scale factor:

  cost = unit_cost * shield_vol * shield_scale * (p_th/p_th_ref)^alpha

`shield_scale` is the fuel neutron-load factor (DT 1.0, DD 0.7, DHe3 0.3,
pB11 0.1 in the source) -- a concept input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:267-269 (c220102), cas22.py:223 (P_TH_REF=2500)
*Basis**: Volume-based shield cost with fuel neutron-load scale

Inputs:
    - shield_scale: shield_scale parameter
    - unit_cost: unit_cost parameter
    - shield_vol: shield_vol parameter
    - p_th_in: p_th_in parameter
    - p_th_ref: p_th_ref parameter
    - alpha: alpha parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:52

SysML Source: root-0/analyses/mfe_account_costs.sysml:52

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/shield_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Shield_CostInput(BaseModel):
    """Input model for Shield_CostModule.

    Attributes:
        shield_scale: shield_scale input
        unit_cost: unit_cost input
        shield_vol: shield_vol input
        p_th_in: p_th_in input
        p_th_ref: p_th_ref input
        alpha: alpha input
    """
    shield_scale: float = Field(..., description="shield_scale input")
    unit_cost: float = Field(..., description="unit_cost input")
    shield_vol: float = Field(..., description="shield_vol input")
    p_th_in: float = Field(..., description="p_th_in input")
    p_th_ref: float = Field(..., description="p_th_ref input")
    alpha: float = Field(..., description="alpha input")


class Shield_CostModule(ModuleBase[Shield_CostInput, Float]):
    """TEAx module for Shield_Cost calculation.

CAS22.1.2 Shield (HT + LT + bioshield) cost. Volume x thermal-power
scaling with a fuel-dependent shield-mass scale factor:

  cost = unit_cost * shield_vol * shield_scale * (p_th/p_th_ref)^alpha

`shield_scale` is the fuel neutron-load factor (DT 1.0, DD 0.7, DHe3 0.3,
pB11 0.1 in the source) -- a concept input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:267-269 (c220102), cas22.py:223 (P_TH_REF=2500)
*Basis**: Volume-based shield cost with fuel neutron-load scale

Inputs:
    - shield_scale: shield_scale parameter
    - unit_cost: unit_cost parameter
    - shield_vol: shield_vol parameter
    - p_th_in: p_th_in parameter
    - p_th_ref: p_th_ref parameter
    - alpha: alpha parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:52

    SysML Source: root-0/analyses/mfe_account_costs.sysml:52

    Calculation Specification:
        p_th_ref = 2500.0
        alpha = 0.6
        cost = unit_cost * shield_vol * shield_scale * (p_th_in / p_th_ref) ** alpha
        
Documentation:
CAS22.1.2 Shield (HT + LT + bioshield) cost. Volume x thermal-power
scaling with a fuel-dependent shield-mass scale factor:

  cost = unit_cost * shield_vol * shield_scale * (p_th/p_th_ref)^alpha

`shield_scale` is the fuel neutron-load factor (DT 1.0, DD 0.7, DHe3 0.3,
pB11 0.1 in the source) -- a concept input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:267-269 (c220102), cas22.py:223 (P_TH_REF=2500)
*Basis**: Volume-based shield cost with fuel neutron-load scale

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.shield_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Shield_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, shield_scale: float, unit_cost: float, shield_vol: float, p_th_in: float, p_th_ref: float, alpha: float    ) -> Shield_CostInput:
        """Validate inputs and fill defaults.

        Args:
            shield_scale: shield_scale input
            unit_cost: unit_cost input
            shield_vol: shield_vol input
            p_th_in: p_th_in input
            p_th_ref: p_th_ref input
            alpha: alpha input

        Returns:
            Validated input model
        """
        return Shield_CostInput(shield_scale=shield_scale, unit_cost=unit_cost, shield_vol=shield_vol, p_th_in=p_th_in, p_th_ref=p_th_ref, alpha=alpha)

    def run(
        self, shield_scale: float, unit_cost: float, shield_vol: float, p_th_in: float, p_th_ref: float, alpha: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            shield_scale: shield_scale input
            unit_cost: unit_cost input
            shield_vol: shield_vol input
            p_th_in: p_th_in input
            p_th_ref: p_th_ref input
            alpha: alpha input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(shield_scale, unit_cost, shield_vol, p_th_in, p_th_ref, alpha)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.shield_cost_impl import (
            run_shield_cost,
        )

        # Execute implementation - returns single value
        cost = run_shield_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
