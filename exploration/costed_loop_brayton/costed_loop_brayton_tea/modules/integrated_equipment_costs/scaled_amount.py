"""Scaled_AmountModule Module Wrapper

TEAx module for Scaled_Amount calculation.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

Inputs:
    - factor_in: factor_in parameter
    - amount_in: amount_in parameter

Outputs:
    - amount: amount result

SysML Source: root-0/integrated_equipment_costs.sysml:92

SysML Source: root-0/integrated_equipment_costs.sysml:92

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/integrated_equipment_costs/scaled_amount_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from costed_loop_brayton_tea.primitives import Float


class Scaled_AmountInput(BaseModel):
    """Input model for Scaled_AmountModule.

    Attributes:
        factor_in: factor_in input
        amount_in: amount_in input
    """
    factor_in: float = Field(..., description="factor_in input")
    amount_in: float = Field(..., description="amount_in input")


class Scaled_AmountModule(ModuleBase[Scaled_AmountInput, Float]):
    """TEAx module for Scaled_Amount calculation.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

Inputs:
    - factor_in: factor_in parameter
    - amount_in: amount_in parameter

Outputs:
    - amount: amount result

SysML Source: root-0/integrated_equipment_costs.sysml:92

    SysML Source: root-0/integrated_equipment_costs.sysml:92

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

    IMPLEMENTATION: See costed_loop_brayton_tea.handwritten.integrated_equipment_costs.scaled_amount_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Scaled_AmountModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, factor_in: float, amount_in: float    ) -> Scaled_AmountInput:
        """Validate inputs and fill defaults.

        Args:
            factor_in: factor_in input
            amount_in: amount_in input

        Returns:
            Validated input model
        """
        return Scaled_AmountInput(factor_in=factor_in, amount_in=amount_in)

    def run(
        self, factor_in: float, amount_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            factor_in: factor_in input
            amount_in: amount_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(factor_in, amount_in)

        # Import handwritten implementation
        from costed_loop_brayton_tea.handwritten.integrated_equipment_costs.scaled_amount_impl import (
            run_scaled_amount,
        )

        # Execute implementation - returns single value
        amount = run_scaled_amount(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(amount))
