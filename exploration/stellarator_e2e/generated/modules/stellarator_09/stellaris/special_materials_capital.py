"""special_materials_capitalModule Module Wrapper

TEAx module for special_materials_capital calculation.

Inputs:
    - blanket_vol: blanket_vol parameter

Outputs:
    - special_materials_capital: special_materials_capital result

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:810

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:810

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/stellarator_09/stellaris/special_materials_capital_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class special_materials_capitalInput(BaseModel):
    """Input model for special_materials_capitalModule.

    Attributes:
        blanket_vol: blanket_vol input
    """
    blanket_vol: float = Field(..., description="blanket_vol input")


class special_materials_capitalModule(ModuleBase[special_materials_capitalInput, Float]):
    """TEAx module for special_materials_capital calculation.

Inputs:
    - blanket_vol: blanket_vol parameter

Outputs:
    - special_materials_capital: special_materials_capital result

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:810

    SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:810

    Calculation Specification:

    IMPLEMENTATION: See stellarator_tea.handwritten.stellarator_09.stellaris.special_materials_capital_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "special_materials_capitalModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, blanket_vol: float    ) -> special_materials_capitalInput:
        """Validate inputs and fill defaults.

        Args:
            blanket_vol: blanket_vol input

        Returns:
            Validated input model
        """
        return special_materials_capitalInput(blanket_vol=blanket_vol)

    def run(
        self, blanket_vol: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            blanket_vol: blanket_vol input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(blanket_vol)

        # Import handwritten implementation
        from stellarator_tea.handwritten.stellarator_09.stellaris.special_materials_capital_impl import (
            run_special_materials_capital,
        )

        # Execute implementation - returns single value
        special_materials_capital = run_special_materials_capital(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(special_materials_capital))
