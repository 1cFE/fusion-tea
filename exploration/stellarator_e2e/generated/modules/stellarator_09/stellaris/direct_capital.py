"""direct_capitalModule Module Wrapper

TEAx module for direct_capital calculation.

Inputs:
    - buildings_capital_cost: buildings_capital_cost parameter
    - powercore_capital: powercore_capital parameter
    - bop_capital: bop_capital parameter
    - preconstruction_capital: preconstruction_capital parameter
    - special_materials_capital: special_materials_capital parameter

Outputs:
    - direct_capital: direct_capital result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/stellarator_09/stellaris/direct_capital_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class direct_capitalInput(BaseModel):
    """Input model for direct_capitalModule.

    Attributes:
        buildings_capital_cost: buildings_capital_cost input
        powercore_capital: powercore_capital input
        bop_capital: bop_capital input
        preconstruction_capital: preconstruction_capital input
        special_materials_capital: special_materials_capital input
    """
    buildings_capital_cost: float = Field(..., description="buildings_capital_cost input")
    powercore_capital: float = Field(..., description="powercore_capital input")
    bop_capital: float = Field(..., description="bop_capital input")
    preconstruction_capital: float = Field(..., description="preconstruction_capital input")
    special_materials_capital: float = Field(..., description="special_materials_capital input")


class direct_capitalModule(ModuleBase[direct_capitalInput, Float]):
    """TEAx module for direct_capital calculation.

Inputs:
    - buildings_capital_cost: buildings_capital_cost parameter
    - powercore_capital: powercore_capital parameter
    - bop_capital: bop_capital parameter
    - preconstruction_capital: preconstruction_capital parameter
    - special_materials_capital: special_materials_capital parameter

Outputs:
    - direct_capital: direct_capital result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        powercore_capital + bop_capital + buildings.capital_cost + preconstruction_capital + special_materials_capital

    IMPLEMENTATION: See stellarator_tea.handwritten.stellarator_09.stellaris.direct_capital_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "direct_capitalModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, buildings_capital_cost: float, powercore_capital: float, bop_capital: float, preconstruction_capital: float, special_materials_capital: float    ) -> direct_capitalInput:
        """Validate inputs and fill defaults.

        Args:
            buildings_capital_cost: buildings_capital_cost input
            powercore_capital: powercore_capital input
            bop_capital: bop_capital input
            preconstruction_capital: preconstruction_capital input
            special_materials_capital: special_materials_capital input

        Returns:
            Validated input model
        """
        return direct_capitalInput(buildings_capital_cost=buildings_capital_cost, powercore_capital=powercore_capital, bop_capital=bop_capital, preconstruction_capital=preconstruction_capital, special_materials_capital=special_materials_capital)

    def run(
        self, buildings_capital_cost: float, powercore_capital: float, bop_capital: float, preconstruction_capital: float, special_materials_capital: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            buildings_capital_cost: buildings_capital_cost input
            powercore_capital: powercore_capital input
            bop_capital: bop_capital input
            preconstruction_capital: preconstruction_capital input
            special_materials_capital: special_materials_capital input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(buildings_capital_cost, powercore_capital, bop_capital, preconstruction_capital, special_materials_capital)

        # Import handwritten implementation
        from stellarator_tea.handwritten.stellarator_09.stellaris.direct_capital_impl import (
            run_direct_capital,
        )

        # Execute implementation - returns single value
        direct_capital = run_direct_capital(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(direct_capital))
