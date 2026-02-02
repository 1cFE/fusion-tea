"""CostCalcModule Module Wrapper

TEAx module for CostCalc calculation.

Inputs:
    - area: area parameter
    - rate: rate parameter

Outputs:
    - total_cost: total_cost result

SysML Source: /home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike/library.sysml:11

SysML Source: /home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike/library.sysml:11

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/chainspikelibrary/costcalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from chain_spike.primitives import Float


class CostCalcInput(BaseModel):
    """Input model for CostCalcModule.

    Attributes:
        area: area input
        rate: rate input
    """
    area: float = Field(..., description="area input")
    rate: float = Field(..., description="rate input")


class CostCalcModule(ModuleBase[CostCalcInput, Float]):
    """TEAx module for CostCalc calculation.

Inputs:
    - area: area parameter
    - rate: rate parameter

Outputs:
    - total_cost: total_cost result

SysML Source: /home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike/library.sysml:11

    SysML Source: /home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike/library.sysml:11

    Calculation Specification:
        total_cost = area * rate

    IMPLEMENTATION: See chain_spike.handwritten.chainspikelibrary.costcalc_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "CostCalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, area: float, rate: float    ) -> CostCalcInput:
        """Validate inputs and fill defaults.

        Args:
            area: area input
            rate: rate input

        Returns:
            Validated input model
        """
        return CostCalcInput(area=area, rate=rate)

    def run(
        self, area: float, rate: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            area: area input
            rate: rate input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(area, rate)

        # Import handwritten implementation
        from chain_spike.handwritten.chainspikelibrary.costcalc_impl import (
            run_costcalc,
        )

        # Execute implementation - returns single value
        total_cost = run_costcalc(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(total_cost))
