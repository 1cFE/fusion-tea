"""volumeModule Module Wrapper

TEAx module for volume calculation.

Inputs:
    - length: length parameter
    - width: width parameter
    - height: height parameter

Outputs:
    - volume: volume result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/e2eattrexprdesign/e2e_plant/volume_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from e2e_attr_expr_v5.primitives import Float


class volumeInput(BaseModel):
    """Input model for volumeModule.

    Attributes:
        length: length input
        width: width input
        height: height input
    """
    length: float = Field(..., description="length input")
    width: float = Field(..., description="width input")
    height: float = Field(..., description="height input")


class volumeModule(ModuleBase[volumeInput, Float]):
    """TEAx module for volume calculation.

Inputs:
    - length: length parameter
    - width: width parameter
    - height: height parameter

Outputs:
    - volume: volume result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        length * width * height

    IMPLEMENTATION: See e2e_attr_expr_v5.handwritten.e2eattrexprdesign.e2e_plant.volume_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "volumeModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, length: float, width: float, height: float    ) -> volumeInput:
        """Validate inputs and fill defaults.

        Args:
            length: length input
            width: width input
            height: height input

        Returns:
            Validated input model
        """
        return volumeInput(length=length, width=width, height=height)

    def run(
        self, length: float, width: float, height: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            length: length input
            width: width input
            height: height input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(length, width, height)

        # Import handwritten implementation
        from e2e_attr_expr_v5.handwritten.e2eattrexprdesign.e2e_plant.volume_impl import (
            run_volume,
        )

        # Execute implementation - returns single value
        volume = run_volume(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(volume))
