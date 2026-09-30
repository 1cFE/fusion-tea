"""eps_minModule Module Wrapper

TEAx module for eps_min calculation.

Outputs:
    - eps_min: eps_min result

SysML Source: root-0/magnet_subsystem.sysml:256

SysML Source: root-0/magnet_subsystem.sysml:256

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/magnet_subsystem/subsystem/nb3sn/eps_min_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from magnet_materials_tea.primitives import Float


class eps_minInput(BaseModel):
    """Input model for eps_minModule.

    Attributes:
    """


class eps_minModule(ModuleBase[eps_minInput, Float]):
    """TEAx module for eps_min calculation.

Outputs:
    - eps_min: eps_min result

SysML Source: root-0/magnet_subsystem.sysml:256

    SysML Source: root-0/magnet_subsystem.sysml:256

    Calculation Specification:

    IMPLEMENTATION: See magnet_materials_tea.handwritten.magnet_subsystem.subsystem.nb3sn.eps_min_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "eps_minModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self,     ) -> eps_minInput:
        """Validate inputs and fill defaults.

        Args:

        Returns:
            Validated input model
        """
        return eps_minInput()

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
        from magnet_materials_tea.handwritten.magnet_subsystem.subsystem.nb3sn.eps_min_impl import (
            run_eps_min,
        )

        # Execute implementation - returns single value
        eps_min = run_eps_min(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(eps_min))
