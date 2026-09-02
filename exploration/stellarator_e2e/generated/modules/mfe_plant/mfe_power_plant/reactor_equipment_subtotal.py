"""reactor_equipment_subtotalModule Module Wrapper

TEAx module for reactor_equipment_subtotal calculation.

Inputs:
    - powercore_capital: powercore_capital parameter
    - remote_handling_capital: remote_handling_capital parameter

Outputs:
    - reactor_equipment_subtotal: reactor_equipment_subtotal result

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:584

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:584

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plant/mfe_power_plant/reactor_equipment_subtotal_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class reactor_equipment_subtotalInput(BaseModel):
    """Input model for reactor_equipment_subtotalModule.

    Attributes:
        powercore_capital: powercore_capital input
        remote_handling_capital: remote_handling_capital input
    """
    powercore_capital: float = Field(..., description="powercore_capital input")
    remote_handling_capital: float = Field(..., description="remote_handling_capital input")


class reactor_equipment_subtotalModule(ModuleBase[reactor_equipment_subtotalInput, Float]):
    """TEAx module for reactor_equipment_subtotal calculation.

Inputs:
    - powercore_capital: powercore_capital parameter
    - remote_handling_capital: remote_handling_capital parameter

Outputs:
    - reactor_equipment_subtotal: reactor_equipment_subtotal result

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:584

    SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:584

    Calculation Specification:

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plant.mfe_power_plant.reactor_equipment_subtotal_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "reactor_equipment_subtotalModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, powercore_capital: float, remote_handling_capital: float    ) -> reactor_equipment_subtotalInput:
        """Validate inputs and fill defaults.

        Args:
            powercore_capital: powercore_capital input
            remote_handling_capital: remote_handling_capital input

        Returns:
            Validated input model
        """
        return reactor_equipment_subtotalInput(powercore_capital=powercore_capital, remote_handling_capital=remote_handling_capital)

    def run(
        self, powercore_capital: float, remote_handling_capital: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            powercore_capital: powercore_capital input
            remote_handling_capital: remote_handling_capital input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(powercore_capital, remote_handling_capital)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plant.mfe_power_plant.reactor_equipment_subtotal_impl import (
            run_reactor_equipment_subtotal,
        )

        # Execute implementation - returns single value
        reactor_equipment_subtotal = run_reactor_equipment_subtotal(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(reactor_equipment_subtotal))
