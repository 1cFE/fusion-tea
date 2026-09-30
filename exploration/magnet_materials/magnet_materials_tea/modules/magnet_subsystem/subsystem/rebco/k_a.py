"""k_aModule Module Wrapper

TEAx module for k_a calculation.

Outputs:
    - k_a: k_a result

SysML Source: root-0/magnet_subsystem.sysml:684

SysML Source: root-0/magnet_subsystem.sysml:684

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/magnet_subsystem/subsystem/rebco/k_a_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from magnet_materials_tea.primitives import Float


class k_aInput(BaseModel):
    """Input model for k_aModule.

    Attributes:
    """


class k_aModule(ModuleBase[k_aInput, Float]):
    """TEAx module for k_a calculation.

Outputs:
    - k_a: k_a result

SysML Source: root-0/magnet_subsystem.sysml:684

    SysML Source: root-0/magnet_subsystem.sysml:684

    Calculation Specification:

    IMPLEMENTATION: See magnet_materials_tea.handwritten.magnet_subsystem.subsystem.rebco.k_a_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "k_aModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self,     ) -> k_aInput:
        """Validate inputs and fill defaults.

        Args:

        Returns:
            Validated input model
        """
        return k_aInput()

    def run(
        self,     ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default()

        # Import handwritten implementation
        from magnet_materials_tea.handwritten.magnet_subsystem.subsystem.rebco.k_a_impl import (
            run_k_a,
        )

        # Execute implementation - returns single value
        k_a = run_k_a(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(k_a))
