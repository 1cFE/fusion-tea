"""Disjoint_Capital_BudgetModule Module Wrapper

TEAx module for Disjoint_Capital_Budget calculation.

Source: work/active/WI-088_aries-source-budget-cost-contribution/spec.md. Ref: accepted financial scope and Lyon Eq7/account mapping. Basis: AGENT generic disjoint-budget accounting and explicit period convention. direct_total=sum(account1..8); inclusive_capital=direct_total*inclusive_multiplier; inclusive_addition=inclusive_capital-direct_total. Dollars, supplied disjoint scope and inclusive multiplier; not a price/financing prediction. Native guard rejects nonfinite/negative budgets, nonpositive multiplier/period/power, mode outside0/1, availability outside(0,1], overflow and zero energy. Last Updated: 2026-09-21.

Inputs:
    - inclusive_multiplier_in: inclusive_multiplier_in parameter
    - account_2_in: account_2_in parameter
    - account_8_in: account_8_in parameter
    - account_1_in: account_1_in parameter
    - account_4_in: account_4_in parameter
    - account_3_in: account_3_in parameter
    - account_5_in: account_5_in parameter
    - account_6_in: account_6_in parameter
    - account_7_in: account_7_in parameter

Outputs:
    - direct_total: direct_total result
    - inclusive_addition: inclusive_addition result
    - inclusive_capital: inclusive_capital result

SysML Source: root-0/source_budget_accounting.sysml:3

SysML Source: root-0/source_budget_accounting.sysml:3

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/source_budget_accounting/disjoint_capital_budget_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from aries_integrated.primitives import Float
from aries_integrated.schemas.disjoint_capital_budget_output import Disjoint_Capital_BudgetOutput


class Disjoint_Capital_BudgetInput(BaseModel):
    """Input model for Disjoint_Capital_BudgetModule.

    Attributes:
        inclusive_multiplier_in: inclusive_multiplier_in input
        account_2_in: account_2_in input
        account_8_in: account_8_in input
        account_1_in: account_1_in input
        account_4_in: account_4_in input
        account_3_in: account_3_in input
        account_5_in: account_5_in input
        account_6_in: account_6_in input
        account_7_in: account_7_in input
    """
    inclusive_multiplier_in: float = Field(..., description="inclusive_multiplier_in input")
    account_2_in: float = Field(..., description="account_2_in input")
    account_8_in: float = Field(..., description="account_8_in input")
    account_1_in: float = Field(..., description="account_1_in input")
    account_4_in: float = Field(..., description="account_4_in input")
    account_3_in: float = Field(..., description="account_3_in input")
    account_5_in: float = Field(..., description="account_5_in input")
    account_6_in: float = Field(..., description="account_6_in input")
    account_7_in: float = Field(..., description="account_7_in input")


class Disjoint_Capital_BudgetModule(ModuleBase[Disjoint_Capital_BudgetInput, Disjoint_Capital_BudgetOutput]):
    """TEAx module for Disjoint_Capital_Budget calculation.

Source: work/active/WI-088_aries-source-budget-cost-contribution/spec.md. Ref: accepted financial scope and Lyon Eq7/account mapping. Basis: AGENT generic disjoint-budget accounting and explicit period convention. direct_total=sum(account1..8); inclusive_capital=direct_total*inclusive_multiplier; inclusive_addition=inclusive_capital-direct_total. Dollars, supplied disjoint scope and inclusive multiplier; not a price/financing prediction. Native guard rejects nonfinite/negative budgets, nonpositive multiplier/period/power, mode outside0/1, availability outside(0,1], overflow and zero energy. Last Updated: 2026-09-21.

Inputs:
    - inclusive_multiplier_in: inclusive_multiplier_in parameter
    - account_2_in: account_2_in parameter
    - account_8_in: account_8_in parameter
    - account_1_in: account_1_in parameter
    - account_4_in: account_4_in parameter
    - account_3_in: account_3_in parameter
    - account_5_in: account_5_in parameter
    - account_6_in: account_6_in parameter
    - account_7_in: account_7_in parameter

Outputs:
    - direct_total: direct_total result
    - inclusive_addition: inclusive_addition result
    - inclusive_capital: inclusive_capital result

SysML Source: root-0/source_budget_accounting.sysml:3

    SysML Source: root-0/source_budget_accounting.sysml:3

    Calculation Specification:
        See documentation:
Source: work/active/WI-088_aries-source-budget-cost-contribution/spec.md. Ref: accepted financial scope and Lyon Eq7/account mapping. Basis: AGENT generic disjoint-budget accounting and explicit period convention. direct_total=sum(account1..8); inclusive_capital=direct_total*inclusive_multiplier; inclusive_addition=inclusive_capital-direct_total. Dollars, supplied disjoint scope and inclusive multiplier; not a price/financing prediction. Native guard rejects nonfinite/negative budgets, nonpositive multiplier/period/power, mode outside0/1, availability outside(0,1], overflow and zero energy. Last Updated: 2026-09-21.

    IMPLEMENTATION: See aries_integrated.handwritten.source_budget_accounting.disjoint_capital_budget_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts direct_total, inclusive_addition, inclusive_capital fields to separate channels.
    """

    name: str = "Disjoint_Capital_BudgetModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, inclusive_multiplier_in: float, account_2_in: float, account_8_in: float, account_1_in: float, account_4_in: float, account_3_in: float, account_5_in: float, account_6_in: float, account_7_in: float    ) -> Disjoint_Capital_BudgetInput:
        """Validate inputs and fill defaults.

        Args:
            inclusive_multiplier_in: inclusive_multiplier_in input
            account_2_in: account_2_in input
            account_8_in: account_8_in input
            account_1_in: account_1_in input
            account_4_in: account_4_in input
            account_3_in: account_3_in input
            account_5_in: account_5_in input
            account_6_in: account_6_in input
            account_7_in: account_7_in input

        Returns:
            Validated input model
        """
        return Disjoint_Capital_BudgetInput(inclusive_multiplier_in=inclusive_multiplier_in, account_2_in=account_2_in, account_8_in=account_8_in, account_1_in=account_1_in, account_4_in=account_4_in, account_3_in=account_3_in, account_5_in=account_5_in, account_6_in=account_6_in, account_7_in=account_7_in)

    def run(
        self, inclusive_multiplier_in: float, account_2_in: float, account_8_in: float, account_1_in: float, account_4_in: float, account_3_in: float, account_5_in: float, account_6_in: float, account_7_in: float    ) -> ModuleResult[Disjoint_Capital_BudgetOutput]:
        """Execute calculation.

        Args:
            inclusive_multiplier_in: inclusive_multiplier_in input
            account_2_in: account_2_in input
            account_8_in: account_8_in input
            account_1_in: account_1_in input
            account_4_in: account_4_in input
            account_3_in: account_3_in input
            account_5_in: account_5_in input
            account_6_in: account_6_in input
            account_7_in: account_7_in input

        Returns:
            Module result with Disjoint_Capital_BudgetOutput (direct_total, inclusive_addition, inclusive_capital)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(inclusive_multiplier_in, account_2_in, account_8_in, account_1_in, account_4_in, account_3_in, account_5_in, account_6_in, account_7_in)

        # Import handwritten implementation
        from aries_integrated.handwritten.source_budget_accounting.disjoint_capital_budget_impl import (
            run_disjoint_capital_budget,
        )

        # Execute implementation - returns tuple of values
        direct_total, inclusive_addition, inclusive_capital = run_disjoint_capital_budget(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Disjoint_Capital_BudgetOutput(
                direct_total=direct_total,
                inclusive_addition=inclusive_addition,
                inclusive_capital=inclusive_capital,
            )
        )
