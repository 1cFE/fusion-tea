"""rejected_heatModule Module Wrapper

TEAx module for rejected_heat calculation.

Inputs:
    - intercooler_1_heat_into_fluid: intercooler_1_heat_into_fluid parameter
    - intercooler_2_heat_into_fluid: intercooler_2_heat_into_fluid parameter
    - precooler_heat_into_fluid: precooler_heat_into_fluid parameter

Outputs:
    - rejected_heat: rejected_heat result

SysML Source: root-0/costed_loop_brayton.sysml:437

SysML Source: root-0/costed_loop_brayton.sysml:437

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/costed_loop_brayton/plant/rejection_capacity/rejected_heat_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from costed_loop_brayton_tea.primitives import Float


class rejected_heatInput(BaseModel):
    """Input model for rejected_heatModule.

    Attributes:
        intercooler_1_heat_into_fluid: intercooler_1_heat_into_fluid input
        intercooler_2_heat_into_fluid: intercooler_2_heat_into_fluid input
        precooler_heat_into_fluid: precooler_heat_into_fluid input
    """
    intercooler_1_heat_into_fluid: float = Field(..., description="intercooler_1_heat_into_fluid input")
    intercooler_2_heat_into_fluid: float = Field(..., description="intercooler_2_heat_into_fluid input")
    precooler_heat_into_fluid: float = Field(..., description="precooler_heat_into_fluid input")


class rejected_heatModule(ModuleBase[rejected_heatInput, Float]):
    """TEAx module for rejected_heat calculation.

Inputs:
    - intercooler_1_heat_into_fluid: intercooler_1_heat_into_fluid parameter
    - intercooler_2_heat_into_fluid: intercooler_2_heat_into_fluid parameter
    - precooler_heat_into_fluid: precooler_heat_into_fluid parameter

Outputs:
    - rejected_heat: rejected_heat result

SysML Source: root-0/costed_loop_brayton.sysml:437

    SysML Source: root-0/costed_loop_brayton.sysml:437

    Calculation Specification:

    IMPLEMENTATION: See costed_loop_brayton_tea.handwritten.costed_loop_brayton.plant.rejection_capacity.rejected_heat_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "rejected_heatModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, intercooler_1_heat_into_fluid: float, intercooler_2_heat_into_fluid: float, precooler_heat_into_fluid: float    ) -> rejected_heatInput:
        """Validate inputs and fill defaults.

        Args:
            intercooler_1_heat_into_fluid: intercooler_1_heat_into_fluid input
            intercooler_2_heat_into_fluid: intercooler_2_heat_into_fluid input
            precooler_heat_into_fluid: precooler_heat_into_fluid input

        Returns:
            Validated input model
        """
        return rejected_heatInput(intercooler_1_heat_into_fluid=intercooler_1_heat_into_fluid, intercooler_2_heat_into_fluid=intercooler_2_heat_into_fluid, precooler_heat_into_fluid=precooler_heat_into_fluid)

    def run(
        self, intercooler_1_heat_into_fluid: float, intercooler_2_heat_into_fluid: float, precooler_heat_into_fluid: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            intercooler_1_heat_into_fluid: intercooler_1_heat_into_fluid input
            intercooler_2_heat_into_fluid: intercooler_2_heat_into_fluid input
            precooler_heat_into_fluid: precooler_heat_into_fluid input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(intercooler_1_heat_into_fluid, intercooler_2_heat_into_fluid, precooler_heat_into_fluid)

        # Import handwritten implementation
        from costed_loop_brayton_tea.handwritten.costed_loop_brayton.plant.rejection_capacity.rejected_heat_impl import (
            run_rejected_heat,
        )

        # Execute implementation - returns single value
        rejected_heat = run_rejected_heat(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(rejected_heat))
