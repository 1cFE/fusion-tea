"""power_kwModule Module Wrapper

TEAx module for power_kw calculation.

Inputs:
    - power_mw: power_mw parameter

Outputs:
    - power_kw: power_kw result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/e2eattrexprdesign/e2e_plant/power_kw_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from e2e_attr_expr_v5.primitives import Float


class power_kwInput(BaseModel):
    """Input model for power_kwModule.

    Attributes:
        power_mw: power_mw input
    """
    power_mw: float = Field(..., description="power_mw input")


class power_kwModule(ModuleBase[power_kwInput, Float]):
    """TEAx module for power_kw calculation.

Inputs:
    - power_mw: power_mw parameter

Outputs:
    - power_kw: power_kw result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        power_mw * LiteralRationalEvaluation()

    IMPLEMENTATION: See e2e_attr_expr_v5.handwritten.e2eattrexprdesign.e2e_plant.power_kw_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "power_kwModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, power_mw: float    ) -> power_kwInput:
        """Validate inputs and fill defaults.

        Args:
            power_mw: power_mw input

        Returns:
            Validated input model
        """
        return power_kwInput(power_mw=power_mw)

    def run(
        self, power_mw: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            power_mw: power_mw input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(power_mw)

        # Import handwritten implementation
        from e2e_attr_expr_v5.handwritten.e2eattrexprdesign.e2e_plant.power_kw_impl import (
            run_power_kw,
        )

        # Execute implementation - returns single value
        power_kw = run_power_kw(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(power_kw))
