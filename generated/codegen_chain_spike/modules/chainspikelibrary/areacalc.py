"""AreaCalcModule Module Wrapper

TEAx module for AreaCalc calculation.

Inputs:
    - length: length parameter
    - width: width parameter

Outputs:
    - area: area result

SysML Source: /home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike/library.sysml:4

SysML Source: /home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike/library.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/chainspikelibrary/areacalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from chain_spike.primitives import Float


class AreaCalcInput(BaseModel):
    """Input model for AreaCalcModule.

    Attributes:
        length: length input
        width: width input
    """
    length: float = Field(..., description="length input")
    width: float = Field(..., description="width input")


class AreaCalcModule(ModuleBase[AreaCalcInput, Float]):
    """TEAx module for AreaCalc calculation.

Inputs:
    - length: length parameter
    - width: width parameter

Outputs:
    - area: area result

SysML Source: /home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike/library.sysml:4

    SysML Source: /home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike/library.sysml:4

    Calculation Specification:
        area = length * width

    IMPLEMENTATION: See chain_spike.handwritten.chainspikelibrary.areacalc_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "AreaCalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, length: float, width: float    ) -> AreaCalcInput:
        """Validate inputs and fill defaults.

        Args:
            length: length input
            width: width input

        Returns:
            Validated input model
        """
        return AreaCalcInput(length=length, width=width)

    def run(
        self, length: float, width: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            length: length input
            width: width input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(length, width)

        # Import handwritten implementation
        from chain_spike.handwritten.chainspikelibrary.areacalc_impl import (
            run_areacalc,
        )

        # Execute implementation - returns single value
        area = run_areacalc(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(area))
