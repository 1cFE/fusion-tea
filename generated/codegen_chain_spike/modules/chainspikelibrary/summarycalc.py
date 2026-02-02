"""SummaryCalcModule Module Wrapper

TEAx module for SummaryCalc calculation.

Inputs:
    - area: area parameter
    - cost: cost parameter

Outputs:
    - cost_per_area: cost_per_area result

SysML Source: /home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike/library.sysml:18

SysML Source: /home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike/library.sysml:18

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/chainspikelibrary/summarycalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from chain_spike.primitives import Float


class SummaryCalcInput(BaseModel):
    """Input model for SummaryCalcModule.

    Attributes:
        area: area input
        cost: cost input
    """
    area: float = Field(..., description="area input")
    cost: float = Field(..., description="cost input")


class SummaryCalcModule(ModuleBase[SummaryCalcInput, Float]):
    """TEAx module for SummaryCalc calculation.

Inputs:
    - area: area parameter
    - cost: cost parameter

Outputs:
    - cost_per_area: cost_per_area result

SysML Source: /home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike/library.sysml:18

    SysML Source: /home/reid/1cfe/fusion-tea/models/tests/codegen_chain_spike/library.sysml:18

    Calculation Specification:
        cost_per_area = cost / area

    IMPLEMENTATION: See chain_spike.handwritten.chainspikelibrary.summarycalc_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "SummaryCalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, area: float, cost: float    ) -> SummaryCalcInput:
        """Validate inputs and fill defaults.

        Args:
            area: area input
            cost: cost input

        Returns:
            Validated input model
        """
        return SummaryCalcInput(area=area, cost=cost)

    def run(
        self, area: float, cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            area: area input
            cost: cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(area, cost)

        # Import handwritten implementation
        from chain_spike.handwritten.chainspikelibrary.summarycalc_impl import (
            run_summarycalc,
        )

        # Execute implementation - returns single value
        cost_per_area = run_summarycalc(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost_per_area))
