"""total_capitalModule Module Wrapper

TEAx module for total_capital calculation.

Inputs:
    - direct_capital: direct_capital parameter
    - contingency_capital: contingency_capital parameter
    - indirect_capital: indirect_capital parameter

Outputs:
    - total_capital: total_capital result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/stellarator_09/stellaris/total_capital_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class total_capitalInput(BaseModel):
    """Input model for total_capitalModule.

    Attributes:
        direct_capital: direct_capital input
        contingency_capital: contingency_capital input
        indirect_capital: indirect_capital input
    """
    direct_capital: float = Field(..., description="direct_capital input")
    contingency_capital: float = Field(..., description="contingency_capital input")
    indirect_capital: float = Field(..., description="indirect_capital input")


class total_capitalModule(ModuleBase[total_capitalInput, Float]):
    """TEAx module for total_capital calculation.

Inputs:
    - direct_capital: direct_capital parameter
    - contingency_capital: contingency_capital parameter
    - indirect_capital: indirect_capital parameter

Outputs:
    - total_capital: total_capital result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        direct_capital + contingency_capital + indirect_capital

    IMPLEMENTATION: See stellarator_tea.handwritten.stellarator_09.stellaris.total_capital_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "total_capitalModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, direct_capital: float, contingency_capital: float, indirect_capital: float    ) -> total_capitalInput:
        """Validate inputs and fill defaults.

        Args:
            direct_capital: direct_capital input
            contingency_capital: contingency_capital input
            indirect_capital: indirect_capital input

        Returns:
            Validated input model
        """
        return total_capitalInput(direct_capital=direct_capital, contingency_capital=contingency_capital, indirect_capital=indirect_capital)

    def run(
        self, direct_capital: float, contingency_capital: float, indirect_capital: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            direct_capital: direct_capital input
            contingency_capital: contingency_capital input
            indirect_capital: indirect_capital input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(direct_capital, contingency_capital, indirect_capital)

        # Import handwritten implementation
        from stellarator_tea.handwritten.stellarator_09.stellaris.total_capital_impl import (
            run_total_capital,
        )

        # Execute implementation - returns single value
        total_capital = run_total_capital(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(total_capital))
