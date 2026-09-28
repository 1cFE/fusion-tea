"""LegacyModule Module Wrapper

TEAx module for Legacy calculation.

Inputs:
    - x_in: x_in parameter

Outputs:
    - gross_out: gross_out result

SysML Source: root-0/probe.sysml:3

SysML Source: root-0/probe.sysml:3

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/probe/legacy_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from probe_selector.primitives import Float


class LegacyInput(BaseModel):
    """Input model for LegacyModule.

    Attributes:
        x_in: x_in input
    """
    x_in: float = Field(..., description="x_in input")


class LegacyModule(ModuleBase[LegacyInput, Float]):
    """TEAx module for Legacy calculation.

Inputs:
    - x_in: x_in parameter

Outputs:
    - gross_out: gross_out result

SysML Source: root-0/probe.sysml:3

    SysML Source: root-0/probe.sysml:3

    Calculation Specification:
        gross_out = x_in * 2.0

    IMPLEMENTATION: See probe_selector.handwritten.probe.legacy_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "LegacyModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, x_in: float    ) -> LegacyInput:
        """Validate inputs and fill defaults.

        Args:
            x_in: x_in input

        Returns:
            Validated input model
        """
        return LegacyInput(x_in=x_in)

    def run(
        self, x_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            x_in: x_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(x_in)

        # Import handwritten implementation
        from probe_selector.handwritten.probe.legacy_impl import (
            run_legacy,
        )

        # Execute implementation - returns single value
        gross_out = run_legacy(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(gross_out))
