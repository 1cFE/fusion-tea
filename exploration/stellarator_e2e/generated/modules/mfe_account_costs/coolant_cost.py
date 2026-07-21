"""Coolant_CostModule Module Wrapper

TEAx module for Coolant_Cost calculation.

Coolant account (two-term, plant-total):

  cost = primary_base * (n_mod * p_net / ref_net_power)
       + intermediate_base * (n_mod * p_th / p_th_ref) ** alpha

primary linear in plant-total net; intermediate power-law in plant-total
thermal.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:684-686 (c220200); ref_net 1000 (:684), p_th_ref 3500 (:685), alpha 0.55 (:685)
*Basis**: Plant-total two-term coolant cost

Inputs:
    - primary_base: primary_base parameter
    - p_net: p_net parameter
    - intermediate_base: intermediate_base parameter
    - p_th: p_th parameter
    - n_mod: n_mod parameter
    - ref_net_power: ref_net_power parameter
    - p_th_ref: p_th_ref parameter
    - alpha: alpha parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:500

SysML Source: root-0/analyses/mfe_account_costs.sysml:500

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/coolant_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Coolant_CostInput(BaseModel):
    """Input model for Coolant_CostModule.

    Attributes:
        primary_base: primary_base input
        p_net: p_net input
        intermediate_base: intermediate_base input
        p_th: p_th input
        n_mod: n_mod input
        ref_net_power: ref_net_power input
        p_th_ref: p_th_ref input
        alpha: alpha input
    """
    primary_base: float = Field(..., description="primary_base input")
    p_net: float = Field(..., description="p_net input")
    intermediate_base: float = Field(..., description="intermediate_base input")
    p_th: float = Field(..., description="p_th input")
    n_mod: float = Field(..., description="n_mod input")
    ref_net_power: float = Field(..., description="ref_net_power input")
    p_th_ref: float = Field(..., description="p_th_ref input")
    alpha: float = Field(..., description="alpha input")


class Coolant_CostModule(ModuleBase[Coolant_CostInput, Float]):
    """TEAx module for Coolant_Cost calculation.

Coolant account (two-term, plant-total):

  cost = primary_base * (n_mod * p_net / ref_net_power)
       + intermediate_base * (n_mod * p_th / p_th_ref) ** alpha

primary linear in plant-total net; intermediate power-law in plant-total
thermal.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:684-686 (c220200); ref_net 1000 (:684), p_th_ref 3500 (:685), alpha 0.55 (:685)
*Basis**: Plant-total two-term coolant cost

Inputs:
    - primary_base: primary_base parameter
    - p_net: p_net parameter
    - intermediate_base: intermediate_base parameter
    - p_th: p_th parameter
    - n_mod: n_mod parameter
    - ref_net_power: ref_net_power parameter
    - p_th_ref: p_th_ref parameter
    - alpha: alpha parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:500

    SysML Source: root-0/analyses/mfe_account_costs.sysml:500

    Calculation Specification:
        n_mod = 1.0
        ref_net_power = 1000.0
        p_th_ref = 3500.0
        alpha = 0.55
        cost = primary_base * (n_mod * p_net / ref_net_power) + intermediate_base * (n_mod * p_th / p_th_ref) ** alpha
        
Documentation:
Coolant account (two-term, plant-total):

  cost = primary_base * (n_mod * p_net / ref_net_power)
       + intermediate_base * (n_mod * p_th / p_th_ref) ** alpha

primary linear in plant-total net; intermediate power-law in plant-total
thermal.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:684-686 (c220200); ref_net 1000 (:684), p_th_ref 3500 (:685), alpha 0.55 (:685)
*Basis**: Plant-total two-term coolant cost

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.coolant_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Coolant_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, primary_base: float, p_net: float, intermediate_base: float, p_th: float, n_mod: float, ref_net_power: float, p_th_ref: float, alpha: float    ) -> Coolant_CostInput:
        """Validate inputs and fill defaults.

        Args:
            primary_base: primary_base input
            p_net: p_net input
            intermediate_base: intermediate_base input
            p_th: p_th input
            n_mod: n_mod input
            ref_net_power: ref_net_power input
            p_th_ref: p_th_ref input
            alpha: alpha input

        Returns:
            Validated input model
        """
        return Coolant_CostInput(primary_base=primary_base, p_net=p_net, intermediate_base=intermediate_base, p_th=p_th, n_mod=n_mod, ref_net_power=ref_net_power, p_th_ref=p_th_ref, alpha=alpha)

    def run(
        self, primary_base: float, p_net: float, intermediate_base: float, p_th: float, n_mod: float, ref_net_power: float, p_th_ref: float, alpha: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            primary_base: primary_base input
            p_net: p_net input
            intermediate_base: intermediate_base input
            p_th: p_th input
            n_mod: n_mod input
            ref_net_power: ref_net_power input
            p_th_ref: p_th_ref input
            alpha: alpha input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(primary_base, p_net, intermediate_base, p_th, n_mod, ref_net_power, p_th_ref, alpha)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.coolant_cost_impl import (
            run_coolant_cost,
        )

        # Execute implementation - returns single value
        cost = run_coolant_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
