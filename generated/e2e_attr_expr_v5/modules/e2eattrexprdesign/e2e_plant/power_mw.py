"""power_mwModule Module Wrapper

TEAx module for power_mw calculation.

Inputs:
    - quantity: quantity parameter
    - unit_cost: unit_cost parameter

Outputs:
    - power_mw: power_mw result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/e2eattrexprdesign/e2e_plant/power_mw_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from e2e_attr_expr_v5.primitives import Float


class power_mwInput(BaseModel):
    """Input model for power_mwModule.

    Attributes:
        quantity: quantity input
        unit_cost: unit_cost input
    """
    quantity: float = Field(..., description="quantity input")
    unit_cost: float = Field(..., description="unit_cost input")


class power_mwModule(ModuleBase[power_mwInput, Float]):
    """TEAx module for power_mw calculation.

Inputs:
    - quantity: quantity parameter
    - unit_cost: unit_cost parameter

Outputs:
    - power_mw: power_mw result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        quantity * unit_cost / LiteralRationalEvaluation()

    IMPLEMENTATION: See e2e_attr_expr_v5.handwritten.e2eattrexprdesign.e2e_plant.power_mw_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "power_mwModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, quantity: float, unit_cost: float    ) -> power_mwInput:
        """Validate inputs and fill defaults.

        Args:
            quantity: quantity input
            unit_cost: unit_cost input

        Returns:
            Validated input model
        """
        return power_mwInput(quantity=quantity, unit_cost=unit_cost)

    def run(
        self, quantity: float, unit_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            quantity: quantity input
            unit_cost: unit_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(quantity, unit_cost)

        # Import handwritten implementation
        from e2e_attr_expr_v5.handwritten.e2eattrexprdesign.e2e_plant.power_mw_impl import (
            run_power_mw,
        )

        # Execute implementation - returns single value
        power_mw = run_power_mw(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(power_mw))
