"""SinkModule Module Wrapper

TEAx module for Sink calculation.

Inputs:
    - value_in: value_in parameter

Outputs:
    - result: result result

SysML Source: root-0/probe.sysml:15

SysML Source: root-0/probe.sysml:15

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/probe/sink_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from probe_selector.primitives import Float


class SinkInput(BaseModel):
    """Input model for SinkModule.

    Attributes:
        value_in: value_in input
    """
    value_in: float = Field(..., description="value_in input")


class SinkModule(ModuleBase[SinkInput, Float]):
    """TEAx module for Sink calculation.

Inputs:
    - value_in: value_in parameter

Outputs:
    - result: result result

SysML Source: root-0/probe.sysml:15

    SysML Source: root-0/probe.sysml:15

    Calculation Specification:
        result = value_in

    IMPLEMENTATION: See probe_selector.handwritten.probe.sink_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "SinkModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, value_in: float    ) -> SinkInput:
        """Validate inputs and fill defaults.

        Args:
            value_in: value_in input

        Returns:
            Validated input model
        """
        return SinkInput(value_in=value_in)

    def run(
        self, value_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            value_in: value_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(value_in)

        # Import handwritten implementation
        from probe_selector.handwritten.probe.sink_impl import (
            run_sink,
        )

        # Execute implementation - returns single value
        result = run_sink(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(result))
