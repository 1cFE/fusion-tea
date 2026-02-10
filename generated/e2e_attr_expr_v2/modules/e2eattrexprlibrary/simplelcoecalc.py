"""SimpleLCOECalcModule Module Wrapper

TEAx module for SimpleLCOECalc calculation.

Inputs:
    - annualized_capital: annualized_capital parameter
    - annual_om: annual_om parameter
    - annual_energy: annual_energy parameter

Outputs:
    - lcoe: lcoe result

SysML Source: models/tests/e2e_attr_expr/library.sysml:39

SysML Source: models/tests/e2e_attr_expr/library.sysml:39

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/e2eattrexprlibrary/simplelcoecalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from e2e_attr_expr_v2.primitives import Float


class SimpleLCOECalcInput(BaseModel):
    """Input model for SimpleLCOECalcModule.

    Attributes:
        annualized_capital: annualized_capital input
        annual_om: annual_om input
        annual_energy: annual_energy input
    """
    annualized_capital: float = Field(..., description="annualized_capital input")
    annual_om: float = Field(..., description="annual_om input")
    annual_energy: float = Field(..., description="annual_energy input")


class SimpleLCOECalcModule(ModuleBase[SimpleLCOECalcInput, Float]):
    """TEAx module for SimpleLCOECalc calculation.

Inputs:
    - annualized_capital: annualized_capital parameter
    - annual_om: annual_om parameter
    - annual_energy: annual_energy parameter

Outputs:
    - lcoe: lcoe result

SysML Source: models/tests/e2e_attr_expr/library.sysml:39

    SysML Source: models/tests/e2e_attr_expr/library.sysml:39

    Calculation Specification:
        lcoe = annualized_capital + annual_om / annual_energy

    IMPLEMENTATION: See e2e_attr_expr_v2.handwritten.e2eattrexprlibrary.simplelcoecalc_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "SimpleLCOECalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, annualized_capital: float, annual_om: float, annual_energy: float    ) -> SimpleLCOECalcInput:
        """Validate inputs and fill defaults.

        Args:
            annualized_capital: annualized_capital input
            annual_om: annual_om input
            annual_energy: annual_energy input

        Returns:
            Validated input model
        """
        return SimpleLCOECalcInput(annualized_capital=annualized_capital, annual_om=annual_om, annual_energy=annual_energy)

    def run(
        self, annualized_capital: float, annual_om: float, annual_energy: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            annualized_capital: annualized_capital input
            annual_om: annual_om input
            annual_energy: annual_energy input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(annualized_capital, annual_om, annual_energy)

        # Import handwritten implementation
        from e2e_attr_expr_v2.handwritten.e2eattrexprlibrary.simplelcoecalc_impl import (
            run_simplelcoecalc,
        )

        # Execute implementation - returns single value
        lcoe = run_simplelcoecalc(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(lcoe))
