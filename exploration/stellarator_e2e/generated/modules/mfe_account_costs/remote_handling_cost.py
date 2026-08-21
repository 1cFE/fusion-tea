"""Remote_Handling_CostModule Module Wrapper

TEAx module for Remote_Handling_Cost calculation.

Remote-handling account:

  cost = base * concept_scale * (p_et / p_et_ref) ** alpha

p_et is per-module gross electric (no n_mod). concept_scale is 1.0
toroidal (tok/stell), 0.55 end-access -- a concept input (MR-3), NOT a
library default.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:631-645 (c220110); cas22.py:224 (P_ET_REF ref_gross 1100)
*Basis**: Per-module gross-electric power law, concept-scaled

Inputs:
    - p_et_in: p_et_in parameter
    - alpha: alpha parameter
    - base: base parameter
    - p_et_ref: p_et_ref parameter
    - concept_scale_in: concept_scale_in parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:476

SysML Source: root-0/analyses/mfe_account_costs.sysml:476

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/remote_handling_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Remote_Handling_CostInput(BaseModel):
    """Input model for Remote_Handling_CostModule.

    Attributes:
        p_et_in: p_et_in input
        alpha: alpha input
        base: base input
        p_et_ref: p_et_ref input
        concept_scale_in: concept_scale_in input
    """
    p_et_in: float = Field(..., description="p_et_in input")
    alpha: float = Field(..., description="alpha input")
    base: float = Field(..., description="base input")
    p_et_ref: float = Field(..., description="p_et_ref input")
    concept_scale_in: float = Field(..., description="concept_scale_in input")


class Remote_Handling_CostModule(ModuleBase[Remote_Handling_CostInput, Float]):
    """TEAx module for Remote_Handling_Cost calculation.

Remote-handling account:

  cost = base * concept_scale * (p_et / p_et_ref) ** alpha

p_et is per-module gross electric (no n_mod). concept_scale is 1.0
toroidal (tok/stell), 0.55 end-access -- a concept input (MR-3), NOT a
library default.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:631-645 (c220110); cas22.py:224 (P_ET_REF ref_gross 1100)
*Basis**: Per-module gross-electric power law, concept-scaled

Inputs:
    - p_et_in: p_et_in parameter
    - alpha: alpha parameter
    - base: base parameter
    - p_et_ref: p_et_ref parameter
    - concept_scale_in: concept_scale_in parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:476

    SysML Source: root-0/analyses/mfe_account_costs.sysml:476

    Calculation Specification:
        p_et_ref = 1100.0
        alpha = 0.5
        cost = base * concept_scale_in * (p_et_in / p_et_ref) ** alpha
        
Documentation:
Remote-handling account:

  cost = base * concept_scale * (p_et / p_et_ref) ** alpha

p_et is per-module gross electric (no n_mod). concept_scale is 1.0
toroidal (tok/stell), 0.55 end-access -- a concept input (MR-3), NOT a
library default.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:631-645 (c220110); cas22.py:224 (P_ET_REF ref_gross 1100)
*Basis**: Per-module gross-electric power law, concept-scaled

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.remote_handling_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Remote_Handling_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, p_et_in: float, alpha: float, base: float, p_et_ref: float, concept_scale_in: float    ) -> Remote_Handling_CostInput:
        """Validate inputs and fill defaults.

        Args:
            p_et_in: p_et_in input
            alpha: alpha input
            base: base input
            p_et_ref: p_et_ref input
            concept_scale_in: concept_scale_in input

        Returns:
            Validated input model
        """
        return Remote_Handling_CostInput(p_et_in=p_et_in, alpha=alpha, base=base, p_et_ref=p_et_ref, concept_scale_in=concept_scale_in)

    def run(
        self, p_et_in: float, alpha: float, base: float, p_et_ref: float, concept_scale_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            p_et_in: p_et_in input
            alpha: alpha input
            base: base input
            p_et_ref: p_et_ref input
            concept_scale_in: concept_scale_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(p_et_in, alpha, base, p_et_ref, concept_scale_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.remote_handling_cost_impl import (
            run_remote_handling_cost,
        )

        # Execute implementation - returns single value
        cost = run_remote_handling_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
