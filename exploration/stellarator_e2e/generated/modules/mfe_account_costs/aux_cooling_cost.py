"""Aux_Cooling_CostModule Module Wrapper

TEAx module for Aux_Cooling_Cost calculation.

Auxiliary cooling + cryoplant account:

  cost = aux_per_mw * (n_mod * p_th) + cryo_base * (p_cryo / p_cryo_ref) ** alpha

aux term linear in plant-total thermal; cryoplant power-law in
per-module cryo electric power (NOT scaled by n_mod — each module has
its own cryoplant).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:693-695 (c220300); p_cryo_ref 30 (:694), alpha 0.7 (:694)
*Basis**: Plant-total aux + per-module cryoplant power law

Inputs:
    - aux_per_mw: aux_per_mw parameter
    - p_th: p_th parameter
    - cryo_base: cryo_base parameter
    - p_cryo: p_cryo parameter
    - n_mod: n_mod parameter
    - p_cryo_ref: p_cryo_ref parameter
    - alpha: alpha parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:532

SysML Source: root-0/analyses/mfe_account_costs.sysml:532

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/aux_cooling_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Aux_Cooling_CostInput(BaseModel):
    """Input model for Aux_Cooling_CostModule.

    Attributes:
        aux_per_mw: aux_per_mw input
        p_th: p_th input
        cryo_base: cryo_base input
        p_cryo: p_cryo input
        n_mod: n_mod input
        p_cryo_ref: p_cryo_ref input
        alpha: alpha input
    """
    aux_per_mw: float = Field(..., description="aux_per_mw input")
    p_th: float = Field(..., description="p_th input")
    cryo_base: float = Field(..., description="cryo_base input")
    p_cryo: float = Field(..., description="p_cryo input")
    n_mod: float = Field(..., description="n_mod input")
    p_cryo_ref: float = Field(..., description="p_cryo_ref input")
    alpha: float = Field(..., description="alpha input")


class Aux_Cooling_CostModule(ModuleBase[Aux_Cooling_CostInput, Float]):
    """TEAx module for Aux_Cooling_Cost calculation.

Auxiliary cooling + cryoplant account:

  cost = aux_per_mw * (n_mod * p_th) + cryo_base * (p_cryo / p_cryo_ref) ** alpha

aux term linear in plant-total thermal; cryoplant power-law in
per-module cryo electric power (NOT scaled by n_mod — each module has
its own cryoplant).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:693-695 (c220300); p_cryo_ref 30 (:694), alpha 0.7 (:694)
*Basis**: Plant-total aux + per-module cryoplant power law

Inputs:
    - aux_per_mw: aux_per_mw parameter
    - p_th: p_th parameter
    - cryo_base: cryo_base parameter
    - p_cryo: p_cryo parameter
    - n_mod: n_mod parameter
    - p_cryo_ref: p_cryo_ref parameter
    - alpha: alpha parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:532

    SysML Source: root-0/analyses/mfe_account_costs.sysml:532

    Calculation Specification:
        n_mod = 1.0
        p_cryo_ref = 30.0
        alpha = 0.7
        cost = aux_per_mw * (n_mod * p_th) + cryo_base * (p_cryo / p_cryo_ref) ** alpha
        
Documentation:
Auxiliary cooling + cryoplant account:

  cost = aux_per_mw * (n_mod * p_th) + cryo_base * (p_cryo / p_cryo_ref) ** alpha

aux term linear in plant-total thermal; cryoplant power-law in
per-module cryo electric power (NOT scaled by n_mod — each module has
its own cryoplant).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:693-695 (c220300); p_cryo_ref 30 (:694), alpha 0.7 (:694)
*Basis**: Plant-total aux + per-module cryoplant power law

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.aux_cooling_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Aux_Cooling_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, aux_per_mw: float, p_th: float, cryo_base: float, p_cryo: float, n_mod: float, p_cryo_ref: float, alpha: float    ) -> Aux_Cooling_CostInput:
        """Validate inputs and fill defaults.

        Args:
            aux_per_mw: aux_per_mw input
            p_th: p_th input
            cryo_base: cryo_base input
            p_cryo: p_cryo input
            n_mod: n_mod input
            p_cryo_ref: p_cryo_ref input
            alpha: alpha input

        Returns:
            Validated input model
        """
        return Aux_Cooling_CostInput(aux_per_mw=aux_per_mw, p_th=p_th, cryo_base=cryo_base, p_cryo=p_cryo, n_mod=n_mod, p_cryo_ref=p_cryo_ref, alpha=alpha)

    def run(
        self, aux_per_mw: float, p_th: float, cryo_base: float, p_cryo: float, n_mod: float, p_cryo_ref: float, alpha: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            aux_per_mw: aux_per_mw input
            p_th: p_th input
            cryo_base: cryo_base input
            p_cryo: p_cryo input
            n_mod: n_mod input
            p_cryo_ref: p_cryo_ref input
            alpha: alpha input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(aux_per_mw, p_th, cryo_base, p_cryo, n_mod, p_cryo_ref, alpha)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.aux_cooling_cost_impl import (
            run_aux_cooling_cost,
        )

        # Execute implementation - returns single value
        cost = run_aux_cooling_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
