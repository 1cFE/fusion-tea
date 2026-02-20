"""annual_omModule Module Wrapper

TEAx module for annual_om calculation.

Inputs:
    - om_rate: om_rate parameter
    - power_kw: power_kw parameter

Outputs:
    - annual_om: annual_om result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/e2eattrexprdesign/e2e_plant/annual_om_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from e2e_attr_expr_v5.primitives import Float


class annual_omInput(BaseModel):
    """Input model for annual_omModule.

    Attributes:
        om_rate: om_rate input
        power_kw: power_kw input
    """
    om_rate: float = Field(..., description="om_rate input")
    power_kw: float = Field(..., description="power_kw input")


class annual_omModule(ModuleBase[annual_omInput, Float]):
    """TEAx module for annual_om calculation.

Inputs:
    - om_rate: om_rate parameter
    - power_kw: power_kw parameter

Outputs:
    - annual_om: annual_om result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        om_rate * power_kw

    IMPLEMENTATION: See e2e_attr_expr_v5.handwritten.e2eattrexprdesign.e2e_plant.annual_om_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "annual_omModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, om_rate: float, power_kw: float    ) -> annual_omInput:
        """Validate inputs and fill defaults.

        Args:
            om_rate: om_rate input
            power_kw: power_kw input

        Returns:
            Validated input model
        """
        return annual_omInput(om_rate=om_rate, power_kw=power_kw)

    def run(
        self, om_rate: float, power_kw: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            om_rate: om_rate input
            power_kw: power_kw input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(om_rate, power_kw)

        # Import handwritten implementation
        from e2e_attr_expr_v5.handwritten.e2eattrexprdesign.e2e_plant.annual_om_impl import (
            run_annual_om,
        )

        # Execute implementation - returns single value
        annual_om = run_annual_om(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(annual_om))
