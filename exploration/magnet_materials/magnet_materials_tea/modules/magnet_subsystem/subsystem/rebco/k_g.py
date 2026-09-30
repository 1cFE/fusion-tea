"""k_gModule Module Wrapper

TEAx module for k_g calculation.

Outputs:
    - k_g: k_g result

SysML Source: root-0/magnet_subsystem.sysml:702

SysML Source: root-0/magnet_subsystem.sysml:702

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/magnet_subsystem/subsystem/rebco/k_g_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from magnet_materials_tea.primitives import Float


class k_gInput(BaseModel):
    """Input model for k_gModule.

    Attributes:
    """


class k_gModule(ModuleBase[k_gInput, Float]):
    """TEAx module for k_g calculation.

Outputs:
    - k_g: k_g result

SysML Source: root-0/magnet_subsystem.sysml:702

    SysML Source: root-0/magnet_subsystem.sysml:702

    Calculation Specification:

    IMPLEMENTATION: See magnet_materials_tea.handwritten.magnet_subsystem.subsystem.rebco.k_g_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "k_gModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self,     ) -> k_gInput:
        """Validate inputs and fill defaults.

        Args:

        Returns:
            Validated input model
        """
        return k_gInput()

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
        from magnet_materials_tea.handwritten.magnet_subsystem.subsystem.rebco.k_g_impl import (
            run_k_g,
        )

        # Execute implementation - returns single value
        k_g = run_k_g(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(k_g))
