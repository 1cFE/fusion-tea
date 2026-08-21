"""total_capitalModule Module Wrapper

TEAx module for total_capital calculation.

Inputs:
    - preconstruction_capital: preconstruction_capital parameter
    - cas20_capital: cas20_capital parameter
    - cas30_capital: cas30_capital parameter
    - owner_capital: owner_capital parameter
    - supplementary_capital: supplementary_capital parameter

Outputs:
    - total_capital: total_capital result

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:624

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:624

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plant/mfe_power_plant/total_capital_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class total_capitalInput(BaseModel):
    """Input model for total_capitalModule.

    Attributes:
        preconstruction_capital: preconstruction_capital input
        cas20_capital: cas20_capital input
        cas30_capital: cas30_capital input
        owner_capital: owner_capital input
        supplementary_capital: supplementary_capital input
    """
    preconstruction_capital: float = Field(..., description="preconstruction_capital input")
    cas20_capital: float = Field(..., description="cas20_capital input")
    cas30_capital: float = Field(..., description="cas30_capital input")
    owner_capital: float = Field(..., description="owner_capital input")
    supplementary_capital: float = Field(..., description="supplementary_capital input")


class total_capitalModule(ModuleBase[total_capitalInput, Float]):
    """TEAx module for total_capital calculation.

Inputs:
    - preconstruction_capital: preconstruction_capital parameter
    - cas20_capital: cas20_capital parameter
    - cas30_capital: cas30_capital parameter
    - owner_capital: owner_capital parameter
    - supplementary_capital: supplementary_capital parameter

Outputs:
    - total_capital: total_capital result

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:624

    SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:624

    Calculation Specification:

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plant.mfe_power_plant.total_capital_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "total_capitalModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, preconstruction_capital: float, cas20_capital: float, cas30_capital: float, owner_capital: float, supplementary_capital: float    ) -> total_capitalInput:
        """Validate inputs and fill defaults.

        Args:
            preconstruction_capital: preconstruction_capital input
            cas20_capital: cas20_capital input
            cas30_capital: cas30_capital input
            owner_capital: owner_capital input
            supplementary_capital: supplementary_capital input

        Returns:
            Validated input model
        """
        return total_capitalInput(preconstruction_capital=preconstruction_capital, cas20_capital=cas20_capital, cas30_capital=cas30_capital, owner_capital=owner_capital, supplementary_capital=supplementary_capital)

    def run(
        self, preconstruction_capital: float, cas20_capital: float, cas30_capital: float, owner_capital: float, supplementary_capital: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            preconstruction_capital: preconstruction_capital input
            cas20_capital: cas20_capital input
            cas30_capital: cas30_capital input
            owner_capital: owner_capital input
            supplementary_capital: supplementary_capital input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(preconstruction_capital, cas20_capital, cas30_capital, owner_capital, supplementary_capital)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plant.mfe_power_plant.total_capital_impl import (
            run_total_capital,
        )

        # Execute implementation - returns single value
        total_capital = run_total_capital(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(total_capital))
