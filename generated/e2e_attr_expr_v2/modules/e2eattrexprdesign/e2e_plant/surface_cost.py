"""surface_costModule Module Wrapper

Computed attribute module.

SysML Expression: area * cost_per_sqm

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/e2eattrexprdesign/e2e_plant/surface_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from e2e_attr_expr_v2.primitives import Float


class surface_costInput(BaseModel):
    """Input model for surface_costModule.

    Attributes:
        area: Input area
        cost_per_sqm: Input cost_per_sqm
    """
    area: float = Field(..., description="Input area")
    cost_per_sqm: float = Field(..., description="Input cost_per_sqm")


class surface_costModule(ModuleBase[surface_costInput, Float]):
    """Computed attribute module.

SysML Expression: area * cost_per_sqm

    SysML Source: unknown:0

    Calculation Specification:
        area * cost_per_sqm

    IMPLEMENTATION: See e2e_attr_expr_v2.handwritten.e2eattrexprdesign.e2e_plant.surface_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "surface_costModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, area: float, cost_per_sqm: float    ) -> surface_costInput:
        """Validate inputs and fill defaults.

        Args:
            area: Input area
            cost_per_sqm: Input cost_per_sqm

        Returns:
            Validated input model
        """
        return surface_costInput(area=area, cost_per_sqm=cost_per_sqm)

    def run(
        self, area: float, cost_per_sqm: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            area: Input area
            cost_per_sqm: Input cost_per_sqm

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(area, cost_per_sqm)

        # Import handwritten implementation
        from e2e_attr_expr_v2.handwritten.e2eattrexprdesign.e2e_plant.surface_cost_impl import (
            run_e2eattrexprdesign__e2e_plant__surface_cost,
        )

        # Execute implementation - returns single value
        surface_cost = run_e2eattrexprdesign__e2e_plant__surface_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(surface_cost))
