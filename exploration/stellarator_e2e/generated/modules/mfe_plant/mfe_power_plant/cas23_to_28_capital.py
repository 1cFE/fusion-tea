"""cas23_to_28_capitalModule Module Wrapper

TEAx module for cas23_to_28_capital calculation.

Inputs:
    - bop_capital: bop_capital parameter
    - special_materials_capital: special_materials_capital parameter
    - cas28_capital: cas28_capital parameter

Outputs:
    - cas23_to_28_capital: cas23_to_28_capital result

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:803

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:803

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plant/mfe_power_plant/cas23_to_28_capital_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class cas23_to_28_capitalInput(BaseModel):
    """Input model for cas23_to_28_capitalModule.

    Attributes:
        bop_capital: bop_capital input
        special_materials_capital: special_materials_capital input
        cas28_capital: cas28_capital input
    """
    bop_capital: float = Field(..., description="bop_capital input")
    special_materials_capital: float = Field(..., description="special_materials_capital input")
    cas28_capital: float = Field(..., description="cas28_capital input")


class cas23_to_28_capitalModule(ModuleBase[cas23_to_28_capitalInput, Float]):
    """TEAx module for cas23_to_28_capital calculation.

Inputs:
    - bop_capital: bop_capital parameter
    - special_materials_capital: special_materials_capital parameter
    - cas28_capital: cas28_capital parameter

Outputs:
    - cas23_to_28_capital: cas23_to_28_capital result

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:803

    SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:803

    Calculation Specification:

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plant.mfe_power_plant.cas23_to_28_capital_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "cas23_to_28_capitalModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, bop_capital: float, special_materials_capital: float, cas28_capital: float    ) -> cas23_to_28_capitalInput:
        """Validate inputs and fill defaults.

        Args:
            bop_capital: bop_capital input
            special_materials_capital: special_materials_capital input
            cas28_capital: cas28_capital input

        Returns:
            Validated input model
        """
        return cas23_to_28_capitalInput(bop_capital=bop_capital, special_materials_capital=special_materials_capital, cas28_capital=cas28_capital)

    def run(
        self, bop_capital: float, special_materials_capital: float, cas28_capital: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            bop_capital: bop_capital input
            special_materials_capital: special_materials_capital input
            cas28_capital: cas28_capital input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(bop_capital, special_materials_capital, cas28_capital)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plant.mfe_power_plant.cas23_to_28_capital_impl import (
            run_cas23_to_28_capital,
        )

        # Execute implementation - returns single value
        cas23_to_28_capital = run_cas23_to_28_capital(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cas23_to_28_capital))
