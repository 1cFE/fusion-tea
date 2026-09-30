"""all_passModule Module Wrapper

TEAx module for all_pass calculation.

Inputs:
    - acceptance_pass: acceptance_pass parameter
    - fit_pass: fit_pass parameter
    - cu_pass: cu_pass parameter
    - steel_pass: steel_pass parameter
    - capacity_pass: capacity_pass parameter

Outputs:
    - all_pass: all_pass result

SysML Source: root-0/magnet_subsystem.sysml:445

SysML Source: root-0/magnet_subsystem.sysml:445

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/magnet_subsystem/subsystem/nb3sn/all_pass_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from magnet_materials_tea.primitives import Float


class all_passInput(BaseModel):
    """Input model for all_passModule.

    Attributes:
        acceptance_pass: acceptance_pass input
        fit_pass: fit_pass input
        cu_pass: cu_pass input
        steel_pass: steel_pass input
        capacity_pass: capacity_pass input
    """
    acceptance_pass: float = Field(..., description="acceptance_pass input")
    fit_pass: float = Field(..., description="fit_pass input")
    cu_pass: float = Field(..., description="cu_pass input")
    steel_pass: float = Field(..., description="steel_pass input")
    capacity_pass: float = Field(..., description="capacity_pass input")


class all_passModule(ModuleBase[all_passInput, Float]):
    """TEAx module for all_pass calculation.

Inputs:
    - acceptance_pass: acceptance_pass parameter
    - fit_pass: fit_pass parameter
    - cu_pass: cu_pass parameter
    - steel_pass: steel_pass parameter
    - capacity_pass: capacity_pass parameter

Outputs:
    - all_pass: all_pass result

SysML Source: root-0/magnet_subsystem.sysml:445

    SysML Source: root-0/magnet_subsystem.sysml:445

    Calculation Specification:

    IMPLEMENTATION: See magnet_materials_tea.handwritten.magnet_subsystem.subsystem.nb3sn.all_pass_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "all_passModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, acceptance_pass: float, fit_pass: float, cu_pass: float, steel_pass: float, capacity_pass: float    ) -> all_passInput:
        """Validate inputs and fill defaults.

        Args:
            acceptance_pass: acceptance_pass input
            fit_pass: fit_pass input
            cu_pass: cu_pass input
            steel_pass: steel_pass input
            capacity_pass: capacity_pass input

        Returns:
            Validated input model
        """
        return all_passInput(acceptance_pass=acceptance_pass, fit_pass=fit_pass, cu_pass=cu_pass, steel_pass=steel_pass, capacity_pass=capacity_pass)

    def run(
        self, acceptance_pass: float, fit_pass: float, cu_pass: float, steel_pass: float, capacity_pass: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            acceptance_pass: acceptance_pass input
            fit_pass: fit_pass input
            cu_pass: cu_pass input
            steel_pass: steel_pass input
            capacity_pass: capacity_pass input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(acceptance_pass, fit_pass, cu_pass, steel_pass, capacity_pass)

        # Import handwritten implementation
        from magnet_materials_tea.handwritten.magnet_subsystem.subsystem.nb3sn.all_pass_impl import (
            run_all_pass,
        )

        # Execute implementation - returns single value
        all_pass = run_all_pass(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(all_pass))
