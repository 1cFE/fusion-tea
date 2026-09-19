"""cooling_initial_handoff_daysModule Module Wrapper

TEAx module for cooling_initial_handoff_days calculation.

Outputs:
    - cooling_initial_handoff_days: cooling_initial_handoff_days result

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:1556

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:1556

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/stellarator_09/stellaris/buildings/cooling_initial_handoff_days_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class cooling_initial_handoff_daysInput(BaseModel):
    """Input model for cooling_initial_handoff_daysModule.

    Attributes:
    """


class cooling_initial_handoff_daysModule(ModuleBase[cooling_initial_handoff_daysInput, Float]):
    """TEAx module for cooling_initial_handoff_days calculation.

Outputs:
    - cooling_initial_handoff_days: cooling_initial_handoff_days result

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:1556

    SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:1556

    Calculation Specification:

    IMPLEMENTATION: See stellarator_tea.handwritten.stellarator_09.stellaris.buildings.cooling_initial_handoff_days_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "cooling_initial_handoff_daysModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self,     ) -> cooling_initial_handoff_daysInput:
        """Validate inputs and fill defaults.

        Args:

        Returns:
            Validated input model
        """
        return cooling_initial_handoff_daysInput()

    def run(
        self,     ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default()

        # Import handwritten implementation
        from stellarator_tea.handwritten.stellarator_09.stellaris.buildings.cooling_initial_handoff_days_impl import (
            run_cooling_initial_handoff_days,
        )

        # Execute implementation - returns single value
        cooling_initial_handoff_days = run_cooling_initial_handoff_days(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cooling_initial_handoff_days))
