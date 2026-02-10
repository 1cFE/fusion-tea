"""areaModule Module Wrapper

Computed attribute module.

SysML Expression: length * width

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/e2eattrexprdesign/e2e_plant/area_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from e2e_attr_expr.primitives import Float


class areaInput(BaseModel):
    """Input model for areaModule.

    Attributes:
        length: Input length
        width: Input width
    """
    length: float = Field(..., description="Input length")
    width: float = Field(..., description="Input width")


class areaModule(ModuleBase[areaInput, Float]):
    """Computed attribute module.

SysML Expression: length * width

    SysML Source: unknown:0

    Calculation Specification:
        length * width

    IMPLEMENTATION: See e2e_attr_expr.handwritten.e2eattrexprdesign.e2e_plant.area_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "areaModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, length: float, width: float    ) -> areaInput:
        """Validate inputs and fill defaults.

        Args:
            length: Input length
            width: Input width

        Returns:
            Validated input model
        """
        return areaInput(length=length, width=width)

    def run(
        self, length: float, width: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            length: Input length
            width: Input width

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(length, width)

        # Import handwritten implementation
        from e2e_attr_expr.handwritten.e2eattrexprdesign.e2e_plant.area_impl import (
            run_e2eattrexprdesign__e2e_plant__area,
        )

        # Execute implementation - returns single value
        area = run_e2eattrexprdesign__e2e_plant__area(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(area))
