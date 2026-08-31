"""cas2x_pre_contingencyModule Module Wrapper

TEAx module for cas2x_pre_contingency calculation.

Inputs:
    - capital_cost: capital_cost parameter
    - cas22_capital: cas22_capital parameter
    - bop_capital: bop_capital parameter
    - special_materials_capital: special_materials_capital parameter
    - cas28_capital: cas28_capital parameter

Outputs:
    - cas2x_pre_contingency: cas2x_pre_contingency result

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:623

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:623

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plant/mfe_power_plant/cas2x_pre_contingency_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class cas2x_pre_contingencyInput(BaseModel):
    """Input model for cas2x_pre_contingencyModule.

    Attributes:
        capital_cost: capital_cost input
        cas22_capital: cas22_capital input
        bop_capital: bop_capital input
        special_materials_capital: special_materials_capital input
        cas28_capital: cas28_capital input
    """
    capital_cost: float = Field(..., description="capital_cost input")
    cas22_capital: float = Field(..., description="cas22_capital input")
    bop_capital: float = Field(..., description="bop_capital input")
    special_materials_capital: float = Field(..., description="special_materials_capital input")
    cas28_capital: float = Field(..., description="cas28_capital input")


class cas2x_pre_contingencyModule(ModuleBase[cas2x_pre_contingencyInput, Float]):
    """TEAx module for cas2x_pre_contingency calculation.

Inputs:
    - capital_cost: capital_cost parameter
    - cas22_capital: cas22_capital parameter
    - bop_capital: bop_capital parameter
    - special_materials_capital: special_materials_capital parameter
    - cas28_capital: cas28_capital parameter

Outputs:
    - cas2x_pre_contingency: cas2x_pre_contingency result

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:623

    SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:623

    Calculation Specification:

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plant.mfe_power_plant.cas2x_pre_contingency_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "cas2x_pre_contingencyModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, capital_cost: float, cas22_capital: float, bop_capital: float, special_materials_capital: float, cas28_capital: float    ) -> cas2x_pre_contingencyInput:
        """Validate inputs and fill defaults.

        Args:
            capital_cost: capital_cost input
            cas22_capital: cas22_capital input
            bop_capital: bop_capital input
            special_materials_capital: special_materials_capital input
            cas28_capital: cas28_capital input

        Returns:
            Validated input model
        """
        return cas2x_pre_contingencyInput(capital_cost=capital_cost, cas22_capital=cas22_capital, bop_capital=bop_capital, special_materials_capital=special_materials_capital, cas28_capital=cas28_capital)

    def run(
        self, capital_cost: float, cas22_capital: float, bop_capital: float, special_materials_capital: float, cas28_capital: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            capital_cost: capital_cost input
            cas22_capital: cas22_capital input
            bop_capital: bop_capital input
            special_materials_capital: special_materials_capital input
            cas28_capital: cas28_capital input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(capital_cost, cas22_capital, bop_capital, special_materials_capital, cas28_capital)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plant.mfe_power_plant.cas2x_pre_contingency_impl import (
            run_cas2x_pre_contingency,
        )

        # Execute implementation - returns single value
        cas2x_pre_contingency = run_cas2x_pre_contingency(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cas2x_pre_contingency))
