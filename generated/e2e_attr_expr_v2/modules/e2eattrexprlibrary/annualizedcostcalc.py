"""AnnualizedCostCalcModule Module Wrapper

TEAx module for AnnualizedCostCalc calculation.

Inputs:
    - total_capex: total_capex parameter
    - discount_rate: discount_rate parameter
    - lifetime: lifetime parameter

Outputs:
    - crf: crf result
    - annualized_cost: annualized_cost result

SysML Source: models/tests/e2e_attr_expr/library.sysml:19

SysML Source: models/tests/e2e_attr_expr/library.sysml:19

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/e2eattrexprlibrary/annualizedcostcalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from e2e_attr_expr_v2.primitives import Float
from e2e_attr_expr_v2.schemas.annualizedcostcalc_output import AnnualizedCostCalcOutput


class AnnualizedCostCalcInput(BaseModel):
    """Input model for AnnualizedCostCalcModule.

    Attributes:
        total_capex: total_capex input
        discount_rate: discount_rate input
        lifetime: lifetime input
    """
    total_capex: float = Field(..., description="total_capex input")
    discount_rate: float = Field(..., description="discount_rate input")
    lifetime: float = Field(..., description="lifetime input")


class AnnualizedCostCalcModule(ModuleBase[AnnualizedCostCalcInput, AnnualizedCostCalcOutput]):
    """TEAx module for AnnualizedCostCalc calculation.

Inputs:
    - total_capex: total_capex parameter
    - discount_rate: discount_rate parameter
    - lifetime: lifetime parameter

Outputs:
    - crf: crf result
    - annualized_cost: annualized_cost result

SysML Source: models/tests/e2e_attr_expr/library.sysml:19

    SysML Source: models/tests/e2e_attr_expr/library.sysml:19

    Calculation Specification:
        crf = discount_rate * 1.0 + discount_rate ** lifetime / 1.0 + discount_rate ** lifetime - 1.0
        annualized_cost = crf * total_capex

    IMPLEMENTATION: See e2e_attr_expr_v2.handwritten.e2eattrexprlibrary.annualizedcostcalc_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts crf, annualized_cost fields to separate channels.
    """

    name: str = "AnnualizedCostCalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, total_capex: float, discount_rate: float, lifetime: float    ) -> AnnualizedCostCalcInput:
        """Validate inputs and fill defaults.

        Args:
            total_capex: total_capex input
            discount_rate: discount_rate input
            lifetime: lifetime input

        Returns:
            Validated input model
        """
        return AnnualizedCostCalcInput(total_capex=total_capex, discount_rate=discount_rate, lifetime=lifetime)

    def run(
        self, total_capex: float, discount_rate: float, lifetime: float    ) -> ModuleResult[AnnualizedCostCalcOutput]:
        """Execute calculation.

        Args:
            total_capex: total_capex input
            discount_rate: discount_rate input
            lifetime: lifetime input

        Returns:
            Module result with AnnualizedCostCalcOutput (crf, annualized_cost)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(total_capex, discount_rate, lifetime)

        # Import handwritten implementation
        from e2e_attr_expr_v2.handwritten.e2eattrexprlibrary.annualizedcostcalc_impl import (
            run_annualizedcostcalc,
        )

        # Execute implementation - returns tuple of values
        crf, annualized_cost = run_annualizedcostcalc(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=AnnualizedCostCalcOutput(
                crf=crf,
                annualized_cost=annualized_cost,
            )
        )
