"""Eight_Amount_SumModule Module Wrapper

TEAx module for Eight_Amount_Sum calculation.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

Inputs:
    - amount8_in: amount8_in parameter
    - amount2_in: amount2_in parameter
    - amount1_in: amount1_in parameter
    - amount7_in: amount7_in parameter
    - amount3_in: amount3_in parameter
    - amount4_in: amount4_in parameter
    - amount5_in: amount5_in parameter
    - amount6_in: amount6_in parameter

Outputs:
    - total: total result

SysML Source: root-0/integrated_equipment_costs.sysml:80

SysML Source: root-0/integrated_equipment_costs.sysml:80

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/integrated_equipment_costs/eight_amount_sum_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from component_alternatives_tea.primitives import Float


class Eight_Amount_SumInput(BaseModel):
    """Input model for Eight_Amount_SumModule.

    Attributes:
        amount8_in: amount8_in input
        amount2_in: amount2_in input
        amount1_in: amount1_in input
        amount7_in: amount7_in input
        amount3_in: amount3_in input
        amount4_in: amount4_in input
        amount5_in: amount5_in input
        amount6_in: amount6_in input
    """
    amount8_in: float = Field(..., description="amount8_in input")
    amount2_in: float = Field(..., description="amount2_in input")
    amount1_in: float = Field(..., description="amount1_in input")
    amount7_in: float = Field(..., description="amount7_in input")
    amount3_in: float = Field(..., description="amount3_in input")
    amount4_in: float = Field(..., description="amount4_in input")
    amount5_in: float = Field(..., description="amount5_in input")
    amount6_in: float = Field(..., description="amount6_in input")


class Eight_Amount_SumModule(ModuleBase[Eight_Amount_SumInput, Float]):
    """TEAx module for Eight_Amount_Sum calculation.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

Inputs:
    - amount8_in: amount8_in parameter
    - amount2_in: amount2_in parameter
    - amount1_in: amount1_in parameter
    - amount7_in: amount7_in parameter
    - amount3_in: amount3_in parameter
    - amount4_in: amount4_in parameter
    - amount5_in: amount5_in parameter
    - amount6_in: amount6_in parameter

Outputs:
    - total: total result

SysML Source: root-0/integrated_equipment_costs.sysml:80

    SysML Source: root-0/integrated_equipment_costs.sysml:80

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

    IMPLEMENTATION: See component_alternatives_tea.handwritten.integrated_equipment_costs.eight_amount_sum_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Eight_Amount_SumModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, amount8_in: float, amount2_in: float, amount1_in: float, amount7_in: float, amount3_in: float, amount4_in: float, amount5_in: float, amount6_in: float    ) -> Eight_Amount_SumInput:
        """Validate inputs and fill defaults.

        Args:
            amount8_in: amount8_in input
            amount2_in: amount2_in input
            amount1_in: amount1_in input
            amount7_in: amount7_in input
            amount3_in: amount3_in input
            amount4_in: amount4_in input
            amount5_in: amount5_in input
            amount6_in: amount6_in input

        Returns:
            Validated input model
        """
        return Eight_Amount_SumInput(amount8_in=amount8_in, amount2_in=amount2_in, amount1_in=amount1_in, amount7_in=amount7_in, amount3_in=amount3_in, amount4_in=amount4_in, amount5_in=amount5_in, amount6_in=amount6_in)

    def run(
        self, amount8_in: float, amount2_in: float, amount1_in: float, amount7_in: float, amount3_in: float, amount4_in: float, amount5_in: float, amount6_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            amount8_in: amount8_in input
            amount2_in: amount2_in input
            amount1_in: amount1_in input
            amount7_in: amount7_in input
            amount3_in: amount3_in input
            amount4_in: amount4_in input
            amount5_in: amount5_in input
            amount6_in: amount6_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(amount8_in, amount2_in, amount1_in, amount7_in, amount3_in, amount4_in, amount5_in, amount6_in)

        # Import handwritten implementation
        from component_alternatives_tea.handwritten.integrated_equipment_costs.eight_amount_sum_impl import (
            run_eight_amount_sum,
        )

        # Execute implementation - returns single value
        total = run_eight_amount_sum(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(total))
