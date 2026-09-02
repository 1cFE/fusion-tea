"""cas20_capitalModule Module Wrapper

TEAx module for cas20_capital calculation.

Inputs:
    - cas2x_pre_contingency: cas2x_pre_contingency parameter
    - contingency_capital: contingency_capital parameter

Outputs:
    - cas20_capital: cas20_capital result

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:682

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:682

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plant/mfe_power_plant/cas20_capital_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class cas20_capitalInput(BaseModel):
    """Input model for cas20_capitalModule.

    Attributes:
        cas2x_pre_contingency: cas2x_pre_contingency input
        contingency_capital: contingency_capital input
    """
    cas2x_pre_contingency: float = Field(..., description="cas2x_pre_contingency input")
    contingency_capital: float = Field(..., description="contingency_capital input")


class cas20_capitalModule(ModuleBase[cas20_capitalInput, Float]):
    """TEAx module for cas20_capital calculation.

Inputs:
    - cas2x_pre_contingency: cas2x_pre_contingency parameter
    - contingency_capital: contingency_capital parameter

Outputs:
    - cas20_capital: cas20_capital result

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:682

    SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:682

    Calculation Specification:

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plant.mfe_power_plant.cas20_capital_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "cas20_capitalModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, cas2x_pre_contingency: float, contingency_capital: float    ) -> cas20_capitalInput:
        """Validate inputs and fill defaults.

        Args:
            cas2x_pre_contingency: cas2x_pre_contingency input
            contingency_capital: contingency_capital input

        Returns:
            Validated input model
        """
        return cas20_capitalInput(cas2x_pre_contingency=cas2x_pre_contingency, contingency_capital=contingency_capital)

    def run(
        self, cas2x_pre_contingency: float, contingency_capital: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            cas2x_pre_contingency: cas2x_pre_contingency input
            contingency_capital: contingency_capital input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(cas2x_pre_contingency, contingency_capital)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plant.mfe_power_plant.cas20_capital_impl import (
            run_cas20_capital,
        )

        # Execute implementation - returns single value
        cas20_capital = run_cas20_capital(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cas20_capital))
