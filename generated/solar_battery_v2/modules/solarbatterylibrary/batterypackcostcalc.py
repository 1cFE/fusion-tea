"""BatteryPackCostCalcModule Module Wrapper

TEAx module for BatteryPackCostCalc calculation.

Cost calculation for battery packs.
Material cost driven by capacity and chemistry factor.

*Source**: Battery industry cost modeling
*Last Updated**: 2026-02-01

Inputs:
    - capacity_kwh: capacity_kwh parameter
    - chemistry_factor: chemistry_factor parameter
    - cost_per_kwh: cost_per_kwh parameter
    - fab_factor: fab_factor parameter
    - install_factor: install_factor parameter

Outputs:
    - material_cost: material_cost result
    - fab_cost: fab_cost result
    - install_cost: install_cost result
    - total_cost: total_cost result
    - idiot_index: idiot_index result

SysML Source: models/tests/solar_battery/library.sysml:96

SysML Source: models/tests/solar_battery/library.sysml:96

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterylibrary/batterypackcostcalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_v2.primitives import Float
from solar_battery_v2.schemas.batterypackcostcalc_output import BatteryPackCostCalcOutput


class BatteryPackCostCalcInput(BaseModel):
    """Input model for BatteryPackCostCalcModule.

    Attributes:
        capacity_kwh: capacity_kwh input
        chemistry_factor: chemistry_factor input
        cost_per_kwh: cost_per_kwh input
        fab_factor: fab_factor input
        install_factor: install_factor input
    """
    capacity_kwh: float = Field(..., description="capacity_kwh input")
    chemistry_factor: float = Field(..., description="chemistry_factor input")
    cost_per_kwh: float = Field(..., description="cost_per_kwh input")
    fab_factor: float = Field(..., description="fab_factor input")
    install_factor: float = Field(..., description="install_factor input")


class BatteryPackCostCalcModule(ModuleBase[BatteryPackCostCalcInput, BatteryPackCostCalcOutput]):
    """TEAx module for BatteryPackCostCalc calculation.

Cost calculation for battery packs.
Material cost driven by capacity and chemistry factor.

*Source**: Battery industry cost modeling
*Last Updated**: 2026-02-01

Inputs:
    - capacity_kwh: capacity_kwh parameter
    - chemistry_factor: chemistry_factor parameter
    - cost_per_kwh: cost_per_kwh parameter
    - fab_factor: fab_factor parameter
    - install_factor: install_factor parameter

Outputs:
    - material_cost: material_cost result
    - fab_cost: fab_cost result
    - install_cost: install_cost result
    - total_cost: total_cost result
    - idiot_index: idiot_index result

SysML Source: models/tests/solar_battery/library.sysml:96

    SysML Source: models/tests/solar_battery/library.sysml:96

    Calculation Specification:
        cost_per_kwh = 171.5
        fab_factor = 0.45
        install_factor = 0.3
        material_cost = capacity_kwh * cost_per_kwh * chemistry_factor
        fab_cost = material_cost * fab_factor
        install_cost = material_cost * install_factor
        total_cost = material_cost + fab_cost + install_cost
        idiot_index = total_cost / material_cost
        
Documentation:
Cost calculation for battery packs.
Material cost driven by capacity and chemistry factor.

*Source**: Battery industry cost modeling
*Last Updated**: 2026-02-01

    IMPLEMENTATION: See solar_battery_v2.handwritten.solarbatterylibrary.batterypackcostcalc_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts material_cost, fab_cost, install_cost, total_cost, idiot_index fields to separate channels.
    """

    name: str = "BatteryPackCostCalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, capacity_kwh: float, chemistry_factor: float, cost_per_kwh: float, fab_factor: float, install_factor: float    ) -> BatteryPackCostCalcInput:
        """Validate inputs and fill defaults.

        Args:
            capacity_kwh: capacity_kwh input
            chemistry_factor: chemistry_factor input
            cost_per_kwh: cost_per_kwh input
            fab_factor: fab_factor input
            install_factor: install_factor input

        Returns:
            Validated input model
        """
        return BatteryPackCostCalcInput(capacity_kwh=capacity_kwh, chemistry_factor=chemistry_factor, cost_per_kwh=cost_per_kwh, fab_factor=fab_factor, install_factor=install_factor)

    def run(
        self, capacity_kwh: float, chemistry_factor: float, cost_per_kwh: float, fab_factor: float, install_factor: float    ) -> ModuleResult[BatteryPackCostCalcOutput]:
        """Execute calculation.

        Args:
            capacity_kwh: capacity_kwh input
            chemistry_factor: chemistry_factor input
            cost_per_kwh: cost_per_kwh input
            fab_factor: fab_factor input
            install_factor: install_factor input

        Returns:
            Module result with BatteryPackCostCalcOutput (material_cost, fab_cost, install_cost, total_cost, idiot_index)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(capacity_kwh, chemistry_factor, cost_per_kwh, fab_factor, install_factor)

        # Import handwritten implementation
        from solar_battery_v2.handwritten.solarbatterylibrary.batterypackcostcalc_impl import (
            run_batterypackcostcalc,
        )

        # Execute implementation - returns tuple of values
        material_cost, fab_cost, install_cost, total_cost, idiot_index = run_batterypackcostcalc(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=BatteryPackCostCalcOutput(
                material_cost=material_cost,
                fab_cost=fab_cost,
                install_cost=install_cost,
                total_cost=total_cost,
                idiot_index=idiot_index,
            )
        )
