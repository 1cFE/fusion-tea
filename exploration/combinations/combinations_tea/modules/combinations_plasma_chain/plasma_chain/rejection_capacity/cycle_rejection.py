"""cycle_rejectionModule Module Wrapper

TEAx module for cycle_rejection calculation.

Inputs:
    - intercooler_1_heat_into_fluid: intercooler_1_heat_into_fluid parameter
    - intercooler_2_heat_into_fluid: intercooler_2_heat_into_fluid parameter
    - precooler_heat_into_fluid: precooler_heat_into_fluid parameter

Outputs:
    - cycle_rejection: cycle_rejection result

SysML Source: root-0/combinations_plasma_chain.sysml:695

SysML Source: root-0/combinations_plasma_chain.sysml:695

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/combinations_plasma_chain/plasma_chain/rejection_capacity/cycle_rejection_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from combinations_tea.primitives import Float


class cycle_rejectionInput(BaseModel):
    """Input model for cycle_rejectionModule.

    Attributes:
        intercooler_1_heat_into_fluid: intercooler_1_heat_into_fluid input
        intercooler_2_heat_into_fluid: intercooler_2_heat_into_fluid input
        precooler_heat_into_fluid: precooler_heat_into_fluid input
    """
    intercooler_1_heat_into_fluid: float = Field(..., description="intercooler_1_heat_into_fluid input")
    intercooler_2_heat_into_fluid: float = Field(..., description="intercooler_2_heat_into_fluid input")
    precooler_heat_into_fluid: float = Field(..., description="precooler_heat_into_fluid input")


class cycle_rejectionModule(ModuleBase[cycle_rejectionInput, Float]):
    """TEAx module for cycle_rejection calculation.

Inputs:
    - intercooler_1_heat_into_fluid: intercooler_1_heat_into_fluid parameter
    - intercooler_2_heat_into_fluid: intercooler_2_heat_into_fluid parameter
    - precooler_heat_into_fluid: precooler_heat_into_fluid parameter

Outputs:
    - cycle_rejection: cycle_rejection result

SysML Source: root-0/combinations_plasma_chain.sysml:695

    SysML Source: root-0/combinations_plasma_chain.sysml:695

    Calculation Specification:

    IMPLEMENTATION: See combinations_tea.handwritten.combinations_plasma_chain.plasma_chain.rejection_capacity.cycle_rejection_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "cycle_rejectionModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, intercooler_1_heat_into_fluid: float, intercooler_2_heat_into_fluid: float, precooler_heat_into_fluid: float    ) -> cycle_rejectionInput:
        """Validate inputs and fill defaults.

        Args:
            intercooler_1_heat_into_fluid: intercooler_1_heat_into_fluid input
            intercooler_2_heat_into_fluid: intercooler_2_heat_into_fluid input
            precooler_heat_into_fluid: precooler_heat_into_fluid input

        Returns:
            Validated input model
        """
        return cycle_rejectionInput(intercooler_1_heat_into_fluid=intercooler_1_heat_into_fluid, intercooler_2_heat_into_fluid=intercooler_2_heat_into_fluid, precooler_heat_into_fluid=precooler_heat_into_fluid)

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
        from combinations_tea.handwritten.combinations_plasma_chain.plasma_chain.rejection_capacity.cycle_rejection_impl import (
            run_cycle_rejection,
        )

        # Execute implementation - returns single value
        cycle_rejection = run_cycle_rejection(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cycle_rejection))
