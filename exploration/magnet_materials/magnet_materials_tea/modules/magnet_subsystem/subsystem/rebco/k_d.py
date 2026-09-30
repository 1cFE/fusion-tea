"""k_dModule Module Wrapper

TEAx module for k_d calculation.

Outputs:
    - k_d: k_d result

SysML Source: root-0/magnet_subsystem.sysml:693

SysML Source: root-0/magnet_subsystem.sysml:693

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/magnet_subsystem/subsystem/rebco/k_d_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from magnet_materials_tea.primitives import Float


class k_dInput(BaseModel):
    """Input model for k_dModule.

    Attributes:
    """


class k_dModule(ModuleBase[k_dInput, Float]):
    """TEAx module for k_d calculation.

Outputs:
    - k_d: k_d result

SysML Source: root-0/magnet_subsystem.sysml:693

    SysML Source: root-0/magnet_subsystem.sysml:693

    Calculation Specification:

    IMPLEMENTATION: See magnet_materials_tea.handwritten.magnet_subsystem.subsystem.rebco.k_d_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "k_dModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self,     ) -> k_dInput:
        """Validate inputs and fill defaults.

        Args:

        Returns:
            Validated input model
        """
        return k_dInput()

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
        from magnet_materials_tea.handwritten.magnet_subsystem.subsystem.rebco.k_d_impl import (
            run_k_d,
        )

        # Execute implementation - returns single value
        k_d = run_k_d(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(k_d))
