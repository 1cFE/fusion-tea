"""GainDoublingsModule Module Wrapper

TEAx module for GainDoublings calculation.

Number of doublings in the target gain: log2(G) = ln(G)/ln(2).
Out-of-envelope: two inline invocations of Ln.

Inputs:
    - target_gain: target_gain parameter

Outputs:
    - doublings: doublings result

SysML Source: /home/reid/1cfe/fusion-tea/exploration/exp_spike/models/exp_toy.sysml:53

SysML Source: /home/reid/1cfe/fusion-tea/exploration/exp_spike/models/exp_toy.sysml:53

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/exp_toy/gaindoublings_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from exp_toy_tea.primitives import Float


class GainDoublingsInput(BaseModel):
    """Input model for GainDoublingsModule.

    Attributes:
        target_gain: target_gain input
    """
    target_gain: float = Field(..., description="target_gain input")


class GainDoublingsModule(ModuleBase[GainDoublingsInput, Float]):
    """TEAx module for GainDoublings calculation.

Number of doublings in the target gain: log2(G) = ln(G)/ln(2).
Out-of-envelope: two inline invocations of Ln.

Inputs:
    - target_gain: target_gain parameter

Outputs:
    - doublings: doublings result

SysML Source: /home/reid/1cfe/fusion-tea/exploration/exp_spike/models/exp_toy.sysml:53

    SysML Source: /home/reid/1cfe/fusion-tea/exploration/exp_spike/models/exp_toy.sysml:53

    Calculation Specification:
        doublings = Ln(target_gain) / Ln(LiteralRationalEvaluation())
        
Documentation:
Number of doublings in the target gain: log2(G) = ln(G)/ln(2).
Out-of-envelope: two inline invocations of Ln.

    IMPLEMENTATION: See exp_toy_tea.handwritten.exp_toy.gaindoublings_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "GainDoublingsModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, target_gain: float    ) -> GainDoublingsInput:
        """Validate inputs and fill defaults.

        Args:
            target_gain: target_gain input

        Returns:
            Validated input model
        """
        return GainDoublingsInput(target_gain=target_gain)

    def run(
        self, target_gain: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            target_gain: target_gain input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(target_gain)

        # Import handwritten implementation
        from exp_toy_tea.handwritten.exp_toy.gaindoublings_impl import (
            run_gaindoublings,
        )

        # Execute implementation - returns single value
        doublings = run_gaindoublings(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(doublings))
