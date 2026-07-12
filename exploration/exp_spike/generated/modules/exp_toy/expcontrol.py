"""ExpControlModule Module Wrapper

TEAx module for ExpControl calculation.

In-envelope control: e^x spelled with the power operator and a
literal e. Mathematically the same function as Exp; should
auto-implement mechanically. Distinguishes "pipeline handles **"
(already proven) from "pipeline handles unknown functions"
(the claim under test).

Inputs:
    - exponent_arg: exponent_arg parameter

Outputs:
    - e_to_x: e_to_x result

SysML Source: /home/reid/1cfe/fusion-tea/exploration/exp_spike/models/exp_toy.sysml:62

SysML Source: /home/reid/1cfe/fusion-tea/exploration/exp_spike/models/exp_toy.sysml:62

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/exp_toy/expcontrol_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from exp_toy_tea.primitives import Float


class ExpControlInput(BaseModel):
    """Input model for ExpControlModule.

    Attributes:
        exponent_arg: exponent_arg input
    """
    exponent_arg: float = Field(..., description="exponent_arg input")


class ExpControlModule(ModuleBase[ExpControlInput, Float]):
    """TEAx module for ExpControl calculation.

In-envelope control: e^x spelled with the power operator and a
literal e. Mathematically the same function as Exp; should
auto-implement mechanically. Distinguishes "pipeline handles **"
(already proven) from "pipeline handles unknown functions"
(the claim under test).

Inputs:
    - exponent_arg: exponent_arg parameter

Outputs:
    - e_to_x: e_to_x result

SysML Source: /home/reid/1cfe/fusion-tea/exploration/exp_spike/models/exp_toy.sysml:62

    SysML Source: /home/reid/1cfe/fusion-tea/exploration/exp_spike/models/exp_toy.sysml:62

    Calculation Specification:
        e_to_x = LiteralRationalEvaluation() ** exponent_arg
        
Documentation:
In-envelope control: e^x spelled with the power operator and a
literal e. Mathematically the same function as Exp; should
auto-implement mechanically. Distinguishes "pipeline handles **"
(already proven) from "pipeline handles unknown functions"
(the claim under test).

    IMPLEMENTATION: See exp_toy_tea.handwritten.exp_toy.expcontrol_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "ExpControlModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, exponent_arg: float    ) -> ExpControlInput:
        """Validate inputs and fill defaults.

        Args:
            exponent_arg: exponent_arg input

        Returns:
            Validated input model
        """
        return ExpControlInput(exponent_arg=exponent_arg)

    def run(
        self, exponent_arg: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            exponent_arg: exponent_arg input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(exponent_arg)

        # Import handwritten implementation
        from exp_toy_tea.handwritten.exp_toy.expcontrol_impl import (
            run_expcontrol,
        )

        # Execute implementation - returns single value
        e_to_x = run_expcontrol(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(e_to_x))
