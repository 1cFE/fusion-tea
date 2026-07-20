"""Preconstruction_CostModule Module Wrapper

TEAx module for Preconstruction_Cost calculation.

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

Inputs:
    - fixed_precon: fixed_precon parameter
    - p_net: p_net parameter
    - n_mod: n_mod parameter
    - land_intensity: land_intensity parameter
    - land_cost: land_cost parameter
    - ref_net_power: ref_net_power parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:356

SysML Source: root-0/analyses/mfe_account_costs.sysml:356

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/preconstruction_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Preconstruction_CostInput(BaseModel):
    """Input model for Preconstruction_CostModule.

    Attributes:
        fixed_precon: fixed_precon input
        p_net: p_net input
        n_mod: n_mod input
        land_intensity: land_intensity input
        land_cost: land_cost input
        ref_net_power: ref_net_power input
    """
    fixed_precon: float = Field(..., description="fixed_precon input")
    p_net: float = Field(..., description="p_net input")
    n_mod: float = Field(..., description="n_mod input")
    land_intensity: float = Field(..., description="land_intensity input")
    land_cost: float = Field(..., description="land_cost input")
    ref_net_power: float = Field(..., description="ref_net_power input")


class Preconstruction_CostModule(ModuleBase[Preconstruction_CostInput, Float]):
    """TEAx module for Preconstruction_Cost calculation.

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

Inputs:
    - fixed_precon: fixed_precon parameter
    - p_net: p_net parameter
    - n_mod: n_mod parameter
    - land_intensity: land_intensity parameter
    - land_cost: land_cost parameter
    - ref_net_power: ref_net_power parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:356

    SysML Source: root-0/analyses/mfe_account_costs.sysml:356

    Calculation Specification:
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

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.preconstruction_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Preconstruction_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, fixed_precon: float, p_net: float, n_mod: float, land_intensity: float, land_cost: float, ref_net_power: float    ) -> Preconstruction_CostInput:
        """Validate inputs and fill defaults.

        Args:
            fixed_precon: fixed_precon input
            p_net: p_net input
            n_mod: n_mod input
            land_intensity: land_intensity input
            land_cost: land_cost input
            ref_net_power: ref_net_power input

        Returns:
            Validated input model
        """
        return Preconstruction_CostInput(fixed_precon=fixed_precon, p_net=p_net, n_mod=n_mod, land_intensity=land_intensity, land_cost=land_cost, ref_net_power=ref_net_power)

    def run(
        self, fixed_precon: float, p_net: float, n_mod: float, land_intensity: float, land_cost: float, ref_net_power: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            fixed_precon: fixed_precon input
            p_net: p_net input
            n_mod: n_mod input
            land_intensity: land_intensity input
            land_cost: land_cost input
            ref_net_power: ref_net_power input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(fixed_precon, p_net, n_mod, land_intensity, land_cost, ref_net_power)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.preconstruction_cost_impl import (
            run_preconstruction_cost,
        )

        # Execute implementation - returns single value
        cost = run_preconstruction_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
