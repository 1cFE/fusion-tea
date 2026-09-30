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
    - p_th_ref: p_th_ref parameter
    - p_th_in: p_th_in parameter
    - primary_base: primary_base parameter
    - ref_net_power: ref_net_power parameter
    - n_mod_in: n_mod_in parameter
    - alpha: alpha parameter
    - p_net: p_net parameter
    - intermediate_base: intermediate_base parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:584

SysML Source: root-0/analyses/mfe_account_costs.sysml:584

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/coolant_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float


class Coolant_CostInput(BaseModel):
    """Input model for Coolant_CostModule.

    Attributes:
        p_th_ref: p_th_ref input
        p_th_in: p_th_in input
        primary_base: primary_base input
        ref_net_power: ref_net_power input
        n_mod_in: n_mod_in input
        alpha: alpha input
        p_net: p_net input
        intermediate_base: intermediate_base input
    """
    p_th_ref: float = Field(..., description="p_th_ref input")
    p_th_in: float = Field(..., description="p_th_in input")
    primary_base: float = Field(..., description="primary_base input")
    ref_net_power: float = Field(..., description="ref_net_power input")
    n_mod_in: float = Field(..., description="n_mod_in input")
    alpha: float = Field(..., description="alpha input")
    p_net: float = Field(..., description="p_net input")
    intermediate_base: float = Field(..., description="intermediate_base input")


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
    - p_th_ref: p_th_ref parameter
    - p_th_in: p_th_in parameter
    - primary_base: primary_base parameter
    - ref_net_power: ref_net_power parameter
    - n_mod_in: n_mod_in parameter
    - alpha: alpha parameter
    - p_net: p_net parameter
    - intermediate_base: intermediate_base parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:584

    SysML Source: root-0/analyses/mfe_account_costs.sysml:584

    Calculation Specification:
        n_mod_in = 1.0
        ref_net_power = 1000.0
        p_th_ref = 3500.0
        alpha = 0.55
        cost = primary_base * (n_mod_in * p_net / ref_net_power) + intermediate_base * (n_mod_in * p_th_in / p_th_ref) ** alpha
        
Documentation:
Coolant account (two-term, plant-total):

  cost = primary_base * (n_mod * p_net / ref_net_power)
       + intermediate_base * (n_mod * p_th / p_th_ref) ** alpha

primary linear in plant-total net; intermediate power-law in plant-total
thermal.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:684-686 (c220200); ref_net 1000 (:684), p_th_ref 3500 (:685), alpha 0.55 (:685)
*Basis**: Plant-total two-term coolant cost

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.mfe_account_costs.coolant_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Coolant_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, p_th_ref: float, p_th_in: float, primary_base: float, ref_net_power: float, n_mod_in: float, alpha: float, p_net: float, intermediate_base: float    ) -> Coolant_CostInput:
        """Validate inputs and fill defaults.

        Args:
            p_th_ref: p_th_ref input
            p_th_in: p_th_in input
            primary_base: primary_base input
            ref_net_power: ref_net_power input
            n_mod_in: n_mod_in input
            alpha: alpha input
            p_net: p_net input
            intermediate_base: intermediate_base input

        Returns:
            Validated input model
        """
        return Coolant_CostInput(p_th_ref=p_th_ref, p_th_in=p_th_in, primary_base=primary_base, ref_net_power=ref_net_power, n_mod_in=n_mod_in, alpha=alpha, p_net=p_net, intermediate_base=intermediate_base)

    def run(
        self, p_th_ref: float, p_th_in: float, primary_base: float, ref_net_power: float, n_mod_in: float, alpha: float, p_net: float, intermediate_base: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            p_th_ref: p_th_ref input
            p_th_in: p_th_in input
            primary_base: primary_base input
            ref_net_power: ref_net_power input
            n_mod_in: n_mod_in input
            alpha: alpha input
            p_net: p_net input
            intermediate_base: intermediate_base input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(p_th_ref, p_th_in, primary_base, ref_net_power, n_mod_in, alpha, p_net, intermediate_base)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.mfe_account_costs.coolant_cost_impl import (
            run_coolant_cost,
        )

        # Execute implementation - returns single value
        cost = run_coolant_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
