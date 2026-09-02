"""powercore_capitalModule Module Wrapper

TEAx module for powercore_capital calculation.

Inputs:
    - magnet_capital_cost: magnet_capital_cost parameter
    - heating_capital_cost: heating_capital_cost parameter
    - divertor_capital_cost: divertor_capital_cost parameter
    - blanket_capital_cost: blanket_capital_cost parameter
    - shield_capital_cost: shield_capital_cost parameter
    - structure_capital_cost: structure_capital_cost parameter
    - vessel_capital_cost: vessel_capital_cost parameter
    - power_supplies_capital_cost: power_supplies_capital_cost parameter

Outputs:
    - powercore_capital: powercore_capital result

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:551

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:551

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plant/mfe_power_plant/powercore_capital_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class powercore_capitalInput(BaseModel):
    """Input model for powercore_capitalModule.

    Attributes:
        magnet_capital_cost: magnet_capital_cost input
        heating_capital_cost: heating_capital_cost input
        divertor_capital_cost: divertor_capital_cost input
        blanket_capital_cost: blanket_capital_cost input
        shield_capital_cost: shield_capital_cost input
        structure_capital_cost: structure_capital_cost input
        vessel_capital_cost: vessel_capital_cost input
        power_supplies_capital_cost: power_supplies_capital_cost input
    """
    magnet_capital_cost: float = Field(..., description="magnet_capital_cost input")
    heating_capital_cost: float = Field(..., description="heating_capital_cost input")
    divertor_capital_cost: float = Field(..., description="divertor_capital_cost input")
    blanket_capital_cost: float = Field(..., description="blanket_capital_cost input")
    shield_capital_cost: float = Field(..., description="shield_capital_cost input")
    structure_capital_cost: float = Field(..., description="structure_capital_cost input")
    vessel_capital_cost: float = Field(..., description="vessel_capital_cost input")
    power_supplies_capital_cost: float = Field(..., description="power_supplies_capital_cost input")


class powercore_capitalModule(ModuleBase[powercore_capitalInput, Float]):
    """TEAx module for powercore_capital calculation.

Inputs:
    - magnet_capital_cost: magnet_capital_cost parameter
    - heating_capital_cost: heating_capital_cost parameter
    - divertor_capital_cost: divertor_capital_cost parameter
    - blanket_capital_cost: blanket_capital_cost parameter
    - shield_capital_cost: shield_capital_cost parameter
    - structure_capital_cost: structure_capital_cost parameter
    - vessel_capital_cost: vessel_capital_cost parameter
    - power_supplies_capital_cost: power_supplies_capital_cost parameter

Outputs:
    - powercore_capital: powercore_capital result

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:551

    SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:551

    Calculation Specification:

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plant.mfe_power_plant.powercore_capital_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "powercore_capitalModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, magnet_capital_cost: float, heating_capital_cost: float, divertor_capital_cost: float, blanket_capital_cost: float, shield_capital_cost: float, structure_capital_cost: float, vessel_capital_cost: float, power_supplies_capital_cost: float    ) -> powercore_capitalInput:
        """Validate inputs and fill defaults.

        Args:
            magnet_capital_cost: magnet_capital_cost input
            heating_capital_cost: heating_capital_cost input
            divertor_capital_cost: divertor_capital_cost input
            blanket_capital_cost: blanket_capital_cost input
            shield_capital_cost: shield_capital_cost input
            structure_capital_cost: structure_capital_cost input
            vessel_capital_cost: vessel_capital_cost input
            power_supplies_capital_cost: power_supplies_capital_cost input

        Returns:
            Validated input model
        """
        return powercore_capitalInput(magnet_capital_cost=magnet_capital_cost, heating_capital_cost=heating_capital_cost, divertor_capital_cost=divertor_capital_cost, blanket_capital_cost=blanket_capital_cost, shield_capital_cost=shield_capital_cost, structure_capital_cost=structure_capital_cost, vessel_capital_cost=vessel_capital_cost, power_supplies_capital_cost=power_supplies_capital_cost)

    def run(
        self, magnet_capital_cost: float, heating_capital_cost: float, divertor_capital_cost: float, blanket_capital_cost: float, shield_capital_cost: float, structure_capital_cost: float, vessel_capital_cost: float, power_supplies_capital_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            magnet_capital_cost: magnet_capital_cost input
            heating_capital_cost: heating_capital_cost input
            divertor_capital_cost: divertor_capital_cost input
            blanket_capital_cost: blanket_capital_cost input
            shield_capital_cost: shield_capital_cost input
            structure_capital_cost: structure_capital_cost input
            vessel_capital_cost: vessel_capital_cost input
            power_supplies_capital_cost: power_supplies_capital_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(magnet_capital_cost, heating_capital_cost, divertor_capital_cost, blanket_capital_cost, shield_capital_cost, structure_capital_cost, vessel_capital_cost, power_supplies_capital_cost)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plant.mfe_power_plant.powercore_capital_impl import (
            run_powercore_capital,
        )

        # Execute implementation - returns single value
        powercore_capital = run_powercore_capital(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(powercore_capital))
