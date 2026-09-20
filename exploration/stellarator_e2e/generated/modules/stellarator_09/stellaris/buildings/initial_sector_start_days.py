"""initial_sector_start_daysModule Module Wrapper

TEAx module for initial_sector_start_days calculation.

Outputs:
    - initial_sector_start_days: initial_sector_start_days result

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:1668

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:1668

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/stellarator_09/stellaris/buildings/initial_sector_start_days_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class initial_sector_start_daysInput(BaseModel):
    """Input model for initial_sector_start_daysModule.

    Attributes:
    """


class initial_sector_start_daysModule(ModuleBase[initial_sector_start_daysInput, Float]):
    """TEAx module for initial_sector_start_days calculation.

Outputs:
    - initial_sector_start_days: initial_sector_start_days result

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:1668

    SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:1668

    Calculation Specification:

    IMPLEMENTATION: See stellarator_tea.handwritten.stellarator_09.stellaris.buildings.initial_sector_start_days_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "initial_sector_start_daysModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self,     ) -> initial_sector_start_daysInput:
        """Validate inputs and fill defaults.

        Args:

        Returns:
            Validated input model
        """
        return initial_sector_start_daysInput()

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
        from stellarator_tea.handwritten.stellarator_09.stellaris.buildings.initial_sector_start_days_impl import (
            run_initial_sector_start_days,
        )

        # Execute implementation - returns single value
        initial_sector_start_days = run_initial_sector_start_days(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(initial_sector_start_days))
