"""Aux_Cooling_CostModule Module Wrapper

TEAx module for Aux_Cooling_Cost calculation.

Auxiliary cooling + cryoplant account:

  cost = aux_per_mw * (n_mod * p_th) + cryo_base * (p_cryo / p_cryo_ref) ** alpha

aux term linear in plant-total thermal; cryoplant power-law in
per-module cryo electric power (NOT scaled by n_mod -- each module has
its own cryoplant).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:693-695 (c220300); p_cryo_ref 30 (:694), alpha 0.7 (:694)
*Basis**: Plant-total aux + per-module cryoplant power law

Inputs:
    - alpha: alpha parameter
    - p_th_in: p_th_in parameter
    - p_cryo_ref: p_cryo_ref parameter
    - p_cryo: p_cryo parameter
    - cryo_base: cryo_base parameter
    - n_mod_in: n_mod_in parameter
    - aux_per_mw_in: aux_per_mw_in parameter

Outputs:
    - aux_cost: aux_cost result
    - cryo_cost: cryo_cost result
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:559

SysML Source: root-0/analyses/mfe_account_costs.sysml:559

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/aux_cooling_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float
from stellarator_tea.schemas.aux_cooling_cost_output import Aux_Cooling_CostOutput


class Aux_Cooling_CostInput(BaseModel):
    """Input model for Aux_Cooling_CostModule.

    Attributes:
        alpha: alpha input
        p_th_in: p_th_in input
        p_cryo_ref: p_cryo_ref input
        p_cryo: p_cryo input
        cryo_base: cryo_base input
        n_mod_in: n_mod_in input
        aux_per_mw_in: aux_per_mw_in input
    """
    alpha: float = Field(..., description="alpha input")
    p_th_in: float = Field(..., description="p_th_in input")
    p_cryo_ref: float = Field(..., description="p_cryo_ref input")
    p_cryo: float = Field(..., description="p_cryo input")
    cryo_base: float = Field(..., description="cryo_base input")
    n_mod_in: float = Field(..., description="n_mod_in input")
    aux_per_mw_in: float = Field(..., description="aux_per_mw_in input")


class Aux_Cooling_CostModule(ModuleBase[Aux_Cooling_CostInput, Aux_Cooling_CostOutput]):
    """TEAx module for Aux_Cooling_Cost calculation.

Auxiliary cooling + cryoplant account:

  cost = aux_per_mw * (n_mod * p_th) + cryo_base * (p_cryo / p_cryo_ref) ** alpha

aux term linear in plant-total thermal; cryoplant power-law in
per-module cryo electric power (NOT scaled by n_mod -- each module has
its own cryoplant).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:693-695 (c220300); p_cryo_ref 30 (:694), alpha 0.7 (:694)
*Basis**: Plant-total aux + per-module cryoplant power law

Inputs:
    - alpha: alpha parameter
    - p_th_in: p_th_in parameter
    - p_cryo_ref: p_cryo_ref parameter
    - p_cryo: p_cryo parameter
    - cryo_base: cryo_base parameter
    - n_mod_in: n_mod_in parameter
    - aux_per_mw_in: aux_per_mw_in parameter

Outputs:
    - aux_cost: aux_cost result
    - cryo_cost: cryo_cost result
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:559

    SysML Source: root-0/analyses/mfe_account_costs.sysml:559

    Calculation Specification:
        n_mod_in = 1.0
        p_cryo_ref = 30.0
        alpha = 0.7
        aux_cost = aux_per_mw_in * (n_mod_in * p_th_in)
        cryo_cost = cryo_base * (p_cryo / p_cryo_ref) ** alpha
        cost = aux_cost + cryo_cost
        
Documentation:
Auxiliary cooling + cryoplant account:

  cost = aux_per_mw * (n_mod * p_th) + cryo_base * (p_cryo / p_cryo_ref) ** alpha

aux term linear in plant-total thermal; cryoplant power-law in
per-module cryo electric power (NOT scaled by n_mod -- each module has
its own cryoplant).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:693-695 (c220300); p_cryo_ref 30 (:694), alpha 0.7 (:694)
*Basis**: Plant-total aux + per-module cryoplant power law

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.aux_cooling_cost_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts aux_cost, cryo_cost, cost fields to separate channels.
    """

    name: str = "Aux_Cooling_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, alpha: float, p_th_in: float, p_cryo_ref: float, p_cryo: float, cryo_base: float, n_mod_in: float, aux_per_mw_in: float    ) -> Aux_Cooling_CostInput:
        """Validate inputs and fill defaults.

        Args:
            alpha: alpha input
            p_th_in: p_th_in input
            p_cryo_ref: p_cryo_ref input
            p_cryo: p_cryo input
            cryo_base: cryo_base input
            n_mod_in: n_mod_in input
            aux_per_mw_in: aux_per_mw_in input

        Returns:
            Validated input model
        """
        return Aux_Cooling_CostInput(alpha=alpha, p_th_in=p_th_in, p_cryo_ref=p_cryo_ref, p_cryo=p_cryo, cryo_base=cryo_base, n_mod_in=n_mod_in, aux_per_mw_in=aux_per_mw_in)

    def run(
        self, alpha: float, p_th_in: float, p_cryo_ref: float, p_cryo: float, cryo_base: float, n_mod_in: float, aux_per_mw_in: float    ) -> ModuleResult[Aux_Cooling_CostOutput]:
        """Execute calculation.

        Args:
            alpha: alpha input
            p_th_in: p_th_in input
            p_cryo_ref: p_cryo_ref input
            p_cryo: p_cryo input
            cryo_base: cryo_base input
            n_mod_in: n_mod_in input
            aux_per_mw_in: aux_per_mw_in input

        Returns:
            Module result with Aux_Cooling_CostOutput (aux_cost, cryo_cost, cost)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(alpha, p_th_in, p_cryo_ref, p_cryo, cryo_base, n_mod_in, aux_per_mw_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.aux_cooling_cost_impl import (
            run_aux_cooling_cost,
        )

        # Execute implementation - returns tuple of values
        aux_cost, cryo_cost, cost = run_aux_cooling_cost(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Aux_Cooling_CostOutput(
                aux_cost=aux_cost,
                cryo_cost=cryo_cost,
                cost=cost,
            )
        )
