"""cas22_capitalModule Module Wrapper

TEAx module for cas22_capital calculation.

Inputs:
    - powercore_capital: powercore_capital parameter
    - remote_handling_capital: remote_handling_capital parameter
    - installation_capital: installation_capital parameter
    - coolant_capital: coolant_capital parameter
    - aux_cooling_capital: aux_cooling_capital parameter
    - waste_capital: waste_capital parameter
    - fuel_handling_capital: fuel_handling_capital parameter
    - other_rpe_capital: other_rpe_capital parameter
    - inc_capital: inc_capital parameter

Outputs:
    - cas22_capital: cas22_capital result

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:762

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:762

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plant/mfe_power_plant/cas22_capital_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class cas22_capitalInput(BaseModel):
    """Input model for cas22_capitalModule.

    Attributes:
        powercore_capital: powercore_capital input
        remote_handling_capital: remote_handling_capital input
        installation_capital: installation_capital input
        coolant_capital: coolant_capital input
        aux_cooling_capital: aux_cooling_capital input
        waste_capital: waste_capital input
        fuel_handling_capital: fuel_handling_capital input
        other_rpe_capital: other_rpe_capital input
        inc_capital: inc_capital input
    """
    powercore_capital: float = Field(..., description="powercore_capital input")
    remote_handling_capital: float = Field(..., description="remote_handling_capital input")
    installation_capital: float = Field(..., description="installation_capital input")
    coolant_capital: float = Field(..., description="coolant_capital input")
    aux_cooling_capital: float = Field(..., description="aux_cooling_capital input")
    waste_capital: float = Field(..., description="waste_capital input")
    fuel_handling_capital: float = Field(..., description="fuel_handling_capital input")
    other_rpe_capital: float = Field(..., description="other_rpe_capital input")
    inc_capital: float = Field(..., description="inc_capital input")


class cas22_capitalModule(ModuleBase[cas22_capitalInput, Float]):
    """TEAx module for cas22_capital calculation.

Inputs:
    - powercore_capital: powercore_capital parameter
    - remote_handling_capital: remote_handling_capital parameter
    - installation_capital: installation_capital parameter
    - coolant_capital: coolant_capital parameter
    - aux_cooling_capital: aux_cooling_capital parameter
    - waste_capital: waste_capital parameter
    - fuel_handling_capital: fuel_handling_capital parameter
    - other_rpe_capital: other_rpe_capital parameter
    - inc_capital: inc_capital parameter

Outputs:
    - cas22_capital: cas22_capital result

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:762

    SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:762

    Calculation Specification:

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plant.mfe_power_plant.cas22_capital_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "cas22_capitalModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, powercore_capital: float, remote_handling_capital: float, installation_capital: float, coolant_capital: float, aux_cooling_capital: float, waste_capital: float, fuel_handling_capital: float, other_rpe_capital: float, inc_capital: float    ) -> cas22_capitalInput:
        """Validate inputs and fill defaults.

        Args:
            powercore_capital: powercore_capital input
            remote_handling_capital: remote_handling_capital input
            installation_capital: installation_capital input
            coolant_capital: coolant_capital input
            aux_cooling_capital: aux_cooling_capital input
            waste_capital: waste_capital input
            fuel_handling_capital: fuel_handling_capital input
            other_rpe_capital: other_rpe_capital input
            inc_capital: inc_capital input

        Returns:
            Validated input model
        """
        return cas22_capitalInput(powercore_capital=powercore_capital, remote_handling_capital=remote_handling_capital, installation_capital=installation_capital, coolant_capital=coolant_capital, aux_cooling_capital=aux_cooling_capital, waste_capital=waste_capital, fuel_handling_capital=fuel_handling_capital, other_rpe_capital=other_rpe_capital, inc_capital=inc_capital)

    def run(
        self, powercore_capital: float, remote_handling_capital: float, installation_capital: float, coolant_capital: float, aux_cooling_capital: float, waste_capital: float, fuel_handling_capital: float, other_rpe_capital: float, inc_capital: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            powercore_capital: powercore_capital input
            remote_handling_capital: remote_handling_capital input
            installation_capital: installation_capital input
            coolant_capital: coolant_capital input
            aux_cooling_capital: aux_cooling_capital input
            waste_capital: waste_capital input
            fuel_handling_capital: fuel_handling_capital input
            other_rpe_capital: other_rpe_capital input
            inc_capital: inc_capital input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(powercore_capital, remote_handling_capital, installation_capital, coolant_capital, aux_cooling_capital, waste_capital, fuel_handling_capital, other_rpe_capital, inc_capital)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plant.mfe_power_plant.cas22_capital_impl import (
            run_cas22_capital,
        )

        # Execute implementation - returns single value
        cas22_capital = run_cas22_capital(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cas22_capital))
