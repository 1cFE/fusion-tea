"""surface_costModule Module Wrapper

TEAx module for surface_cost calculation.

Inputs:
    - area: area parameter
    - cost_per_sqm: cost_per_sqm parameter

Outputs:
    - surface_cost: surface_cost result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/e2eattrexprdesign/e2e_plant/surface_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from e2e_attr_expr_v5.primitives import Float


class surface_costInput(BaseModel):
    """Input model for surface_costModule.

    Attributes:
        area: area input
        cost_per_sqm: cost_per_sqm input
    """
    area: float = Field(..., description="area input")
    cost_per_sqm: float = Field(..., description="cost_per_sqm input")


class surface_costModule(ModuleBase[surface_costInput, Float]):
    """TEAx module for surface_cost calculation.

Inputs:
    - area: area parameter
    - cost_per_sqm: cost_per_sqm parameter

Outputs:
    - surface_cost: surface_cost result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        area * cost_per_sqm

    IMPLEMENTATION: See e2e_attr_expr_v5.handwritten.e2eattrexprdesign.e2e_plant.surface_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "surface_costModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, area: float, cost_per_sqm: float    ) -> surface_costInput:
        """Validate inputs and fill defaults.

        Args:
            area: area input
            cost_per_sqm: cost_per_sqm input

        Returns:
            Validated input model
        """
        return surface_costInput(area=area, cost_per_sqm=cost_per_sqm)

    def run(
        self, area: float, cost_per_sqm: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            area: area input
            cost_per_sqm: cost_per_sqm input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(area, cost_per_sqm)

        # Import handwritten implementation
        from e2e_attr_expr_v5.handwritten.e2eattrexprdesign.e2e_plant.surface_cost_impl import (
            run_surface_cost,
        )

        # Execute implementation - returns single value
        surface_cost = run_surface_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(surface_cost))
