"""annual_omModule Module Wrapper

Computed attribute module.

SysML Expression: om_rate * power_kw

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/e2eattrexprdesign/e2e_plant/annual_om_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from e2e_attr_expr_v2.primitives import Float


class annual_omInput(BaseModel):
    """Input model for annual_omModule.

    Attributes:
        om_rate: Input om_rate
        power_kw: Input power_kw
    """
    om_rate: float = Field(..., description="Input om_rate")
    power_kw: float = Field(..., description="Input power_kw")


class annual_omModule(ModuleBase[annual_omInput, Float]):
    """Computed attribute module.

SysML Expression: om_rate * power_kw

    SysML Source: unknown:0

    Calculation Specification:
        om_rate * power_kw

    IMPLEMENTATION: See e2e_attr_expr_v2.handwritten.e2eattrexprdesign.e2e_plant.annual_om_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "annual_omModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, om_rate: float, power_kw: float    ) -> annual_omInput:
        """Validate inputs and fill defaults.

        Args:
            om_rate: Input om_rate
            power_kw: Input power_kw

        Returns:
            Validated input model
        """
        return annual_omInput(om_rate=om_rate, power_kw=power_kw)

    def run(
        self, om_rate: float, power_kw: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            om_rate: Input om_rate
            power_kw: Input power_kw

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(om_rate, power_kw)

        # Import handwritten implementation
        from e2e_attr_expr_v2.handwritten.e2eattrexprdesign.e2e_plant.annual_om_impl import (
            run_e2eattrexprdesign__e2e_plant__annual_om,
        )

        # Execute implementation - returns single value
        annual_om = run_e2eattrexprdesign__e2e_plant__annual_om(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(annual_om))
