"""turn_currentModule Module Wrapper

TEAx module for turn_current calculation.

Inputs:
    - I_ref: I_ref parameter
    - B_peak: B_peak parameter
    - B_ref: B_ref parameter

Outputs:
    - turn_current: turn_current result

SysML Source: root-0/magnet_subsystem.sysml:30

SysML Source: root-0/magnet_subsystem.sysml:30

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/magnet_subsystem/subsystem/duty/turn_current_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from magnet_materials_tea.primitives import Float


class turn_currentInput(BaseModel):
    """Input model for turn_currentModule.

    Attributes:
        I_ref: I_ref input
        B_peak: B_peak input
        B_ref: B_ref input
    """
    I_ref: float = Field(..., description="I_ref input")
    B_peak: float = Field(..., description="B_peak input")
    B_ref: float = Field(..., description="B_ref input")


class turn_currentModule(ModuleBase[turn_currentInput, Float]):
    """TEAx module for turn_current calculation.

Inputs:
    - I_ref: I_ref parameter
    - B_peak: B_peak parameter
    - B_ref: B_ref parameter

Outputs:
    - turn_current: turn_current result

SysML Source: root-0/magnet_subsystem.sysml:30

    SysML Source: root-0/magnet_subsystem.sysml:30

    Calculation Specification:

    IMPLEMENTATION: See magnet_materials_tea.handwritten.magnet_subsystem.subsystem.duty.turn_current_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "turn_currentModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, I_ref: float, B_peak: float, B_ref: float    ) -> turn_currentInput:
        """Validate inputs and fill defaults.

        Args:
            I_ref: I_ref input
            B_peak: B_peak input
            B_ref: B_ref input

        Returns:
            Validated input model
        """
        return turn_currentInput(I_ref=I_ref, B_peak=B_peak, B_ref=B_ref)

    def run(
        self, I_ref: float, B_peak: float, B_ref: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            I_ref: I_ref input
            B_peak: B_peak input
            B_ref: B_ref input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(I_ref, B_peak, B_ref)

        # Import handwritten implementation
        from magnet_materials_tea.handwritten.magnet_subsystem.subsystem.duty.turn_current_impl import (
            run_turn_current,
        )

        # Execute implementation - returns single value
        turn_current = run_turn_current(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(turn_current))
