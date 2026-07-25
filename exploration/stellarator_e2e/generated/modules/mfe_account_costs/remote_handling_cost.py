"""Remote_Handling_CostModule Module Wrapper

TEAx module for Remote_Handling_Cost calculation.

Remote-handling account:

  cost = base * concept_scale * (p_et / p_et_ref) ** alpha

p_et is per-module gross electric (no n_mod). concept_scale is 1.0
toroidal (tok/stell), 0.55 end-access — a concept input (MR-3), NOT a
library default.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:631-645 (c220110); cas22.py:224 (P_ET_REF ref_gross 1100)
*Basis**: Per-module gross-electric power law, concept-scaled

Inputs:
    - base: base parameter
    - concept_scale: concept_scale parameter
    - p_et: p_et parameter
    - p_et_ref: p_et_ref parameter
    - alpha: alpha parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:460

SysML Source: root-0/analyses/mfe_account_costs.sysml:460

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/remote_handling_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Remote_Handling_CostInput(BaseModel):
    """Input model for Remote_Handling_CostModule.

    Attributes:
        base: base input
        concept_scale: concept_scale input
        p_et: p_et input
        p_et_ref: p_et_ref input
        alpha: alpha input
    """
    base: float = Field(..., description="base input")
    concept_scale: float = Field(..., description="concept_scale input")
    p_et: float = Field(..., description="p_et input")
    p_et_ref: float = Field(..., description="p_et_ref input")
    alpha: float = Field(..., description="alpha input")


class Remote_Handling_CostModule(ModuleBase[Remote_Handling_CostInput, Float]):
    """TEAx module for Remote_Handling_Cost calculation.

Remote-handling account:

  cost = base * concept_scale * (p_et / p_et_ref) ** alpha

p_et is per-module gross electric (no n_mod). concept_scale is 1.0
toroidal (tok/stell), 0.55 end-access — a concept input (MR-3), NOT a
library default.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:631-645 (c220110); cas22.py:224 (P_ET_REF ref_gross 1100)
*Basis**: Per-module gross-electric power law, concept-scaled

Inputs:
    - base: base parameter
    - concept_scale: concept_scale parameter
    - p_et: p_et parameter
    - p_et_ref: p_et_ref parameter
    - alpha: alpha parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:460

    SysML Source: root-0/analyses/mfe_account_costs.sysml:460

    Calculation Specification:
        p_et_ref = 1100.0
        alpha = 0.5
        cost = base * concept_scale * (p_et / p_et_ref) ** alpha
        
Documentation:
Remote-handling account:

  cost = base * concept_scale * (p_et / p_et_ref) ** alpha

p_et is per-module gross electric (no n_mod). concept_scale is 1.0
toroidal (tok/stell), 0.55 end-access — a concept input (MR-3), NOT a
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
        self, base: float, concept_scale: float, p_et: float, p_et_ref: float, alpha: float    ) -> Remote_Handling_CostInput:
        """Validate inputs and fill defaults.

        Args:
            base: base input
            concept_scale: concept_scale input
            p_et: p_et input
            p_et_ref: p_et_ref input
            alpha: alpha input

        Returns:
            Validated input model
        """
        return Remote_Handling_CostInput(base=base, concept_scale=concept_scale, p_et=p_et, p_et_ref=p_et_ref, alpha=alpha)

    def run(
        self, base: float, concept_scale: float, p_et: float, p_et_ref: float, alpha: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            base: base input
            concept_scale: concept_scale input
            p_et: p_et input
            p_et_ref: p_et_ref input
            alpha: alpha input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(base, concept_scale, p_et, p_et_ref, alpha)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.remote_handling_cost_impl import (
            run_remote_handling_cost,
        )

        # Execute implementation - returns single value
        cost = run_remote_handling_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
