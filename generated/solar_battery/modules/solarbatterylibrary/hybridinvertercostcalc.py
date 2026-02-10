"""HybridInverterCostCalcModule Module Wrapper

TEAx module for HybridInverterCostCalc calculation.

Cost calculation for hybrid (bidirectional) inverters.
Material cost driven by power rating.

*Source**: Battery industry cost modeling
*Last Updated**: 2026-02-01

Inputs:
    - power_rating: power_rating parameter
    - cost_per_watt: cost_per_watt parameter
    - fab_factor: fab_factor parameter
    - install_factor: install_factor parameter

Outputs:
    - material_cost: material_cost result
    - fab_cost: fab_cost result
    - install_cost: install_cost result
    - total_cost: total_cost result
    - idiot_index: idiot_index result

SysML Source: models/tests/solar_battery/library.sysml:119

SysML Source: models/tests/solar_battery/library.sysml:119

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterylibrary/hybridinvertercostcalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery.primitives import Float
from solar_battery.schemas.hybridinvertercostcalc_output import HybridInverterCostCalcOutput


class HybridInverterCostCalcInput(BaseModel):
    """Input model for HybridInverterCostCalcModule.

    Attributes:
        power_rating: power_rating input
        cost_per_watt: cost_per_watt input
        fab_factor: fab_factor input
        install_factor: install_factor input
    """
    power_rating: float = Field(..., description="power_rating input")
    cost_per_watt: float = Field(..., description="cost_per_watt input")
    fab_factor: float = Field(..., description="fab_factor input")
    install_factor: float = Field(..., description="install_factor input")


class HybridInverterCostCalcModule(ModuleBase[HybridInverterCostCalcInput, HybridInverterCostCalcOutput]):
    """TEAx module for HybridInverterCostCalc calculation.

Cost calculation for hybrid (bidirectional) inverters.
Material cost driven by power rating.

*Source**: Battery industry cost modeling
*Last Updated**: 2026-02-01

Inputs:
    - power_rating: power_rating parameter
    - cost_per_watt: cost_per_watt parameter
    - fab_factor: fab_factor parameter
    - install_factor: install_factor parameter

Outputs:
    - material_cost: material_cost result
    - fab_cost: fab_cost result
    - install_cost: install_cost result
    - total_cost: total_cost result
    - idiot_index: idiot_index result

SysML Source: models/tests/solar_battery/library.sysml:119

    SysML Source: models/tests/solar_battery/library.sysml:119

    Calculation Specification:
        cost_per_watt = 0.1714
        fab_factor = 0.45
        install_factor = 0.3
        material_cost = power_rating * cost_per_watt
        fab_cost = material_cost * fab_factor
        install_cost = material_cost * install_factor
        total_cost = material_cost + fab_cost + install_cost
        idiot_index = total_cost / material_cost
        
Documentation:
Cost calculation for hybrid (bidirectional) inverters.
Material cost driven by power rating.

*Source**: Battery industry cost modeling
*Last Updated**: 2026-02-01

    IMPLEMENTATION: See solar_battery.handwritten.solarbatterylibrary.hybridinvertercostcalc_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts material_cost, fab_cost, install_cost, total_cost, idiot_index fields to separate channels.
    """

    name: str = "HybridInverterCostCalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, power_rating: float, cost_per_watt: float, fab_factor: float, install_factor: float    ) -> HybridInverterCostCalcInput:
        """Validate inputs and fill defaults.

        Args:
            power_rating: power_rating input
            cost_per_watt: cost_per_watt input
            fab_factor: fab_factor input
            install_factor: install_factor input

        Returns:
            Validated input model
        """
        return HybridInverterCostCalcInput(power_rating=power_rating, cost_per_watt=cost_per_watt, fab_factor=fab_factor, install_factor=install_factor)

    def run(
        self, power_rating: float, cost_per_watt: float, fab_factor: float, install_factor: float    ) -> ModuleResult[HybridInverterCostCalcOutput]:
        """Execute calculation.

        Args:
            power_rating: power_rating input
            cost_per_watt: cost_per_watt input
            fab_factor: fab_factor input
            install_factor: install_factor input

        Returns:
            Module result with HybridInverterCostCalcOutput (material_cost, fab_cost, install_cost, total_cost, idiot_index)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(power_rating, cost_per_watt, fab_factor, install_factor)

        # Import handwritten implementation
        from solar_battery.handwritten.solarbatterylibrary.hybridinvertercostcalc_impl import (
            run_hybridinvertercostcalc,
        )

        # Execute implementation - returns tuple of values
        material_cost, fab_cost, install_cost, total_cost, idiot_index = run_hybridinvertercostcalc(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=HybridInverterCostCalcOutput(
                material_cost=material_cost,
                fab_cost=fab_cost,
                install_cost=install_cost,
                total_cost=total_cost,
                idiot_index=idiot_index,
            )
        )
