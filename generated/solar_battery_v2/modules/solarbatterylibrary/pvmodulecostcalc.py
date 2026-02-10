"""PVModuleCostCalcModule Module Wrapper

TEAx module for PVModuleCostCalc calculation.

Cost calculation for photovoltaic modules.
Material cost driven by wattage and cost per watt.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

Inputs:
    - wattage: wattage parameter
    - efficiency: efficiency parameter
    - cost_per_watt: cost_per_watt parameter
    - fab_factor: fab_factor parameter
    - install_factor: install_factor parameter

Outputs:
    - material_cost: material_cost result
    - fab_cost: fab_cost result
    - install_cost: install_cost result
    - total_cost: total_cost result
    - idiot_index: idiot_index result

SysML Source: models/tests/solar_battery/library.sysml:27

SysML Source: models/tests/solar_battery/library.sysml:27

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterylibrary/pvmodulecostcalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_v2.primitives import Float
from solar_battery_v2.schemas.pvmodulecostcalc_output import PVModuleCostCalcOutput


class PVModuleCostCalcInput(BaseModel):
    """Input model for PVModuleCostCalcModule.

    Attributes:
        wattage: wattage input
        efficiency: efficiency input
        cost_per_watt: cost_per_watt input
        fab_factor: fab_factor input
        install_factor: install_factor input
    """
    wattage: float = Field(..., description="wattage input")
    efficiency: float = Field(..., description="efficiency input")
    cost_per_watt: float = Field(..., description="cost_per_watt input")
    fab_factor: float = Field(..., description="fab_factor input")
    install_factor: float = Field(..., description="install_factor input")


class PVModuleCostCalcModule(ModuleBase[PVModuleCostCalcInput, PVModuleCostCalcOutput]):
    """TEAx module for PVModuleCostCalc calculation.

Cost calculation for photovoltaic modules.
Material cost driven by wattage and cost per watt.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

Inputs:
    - wattage: wattage parameter
    - efficiency: efficiency parameter
    - cost_per_watt: cost_per_watt parameter
    - fab_factor: fab_factor parameter
    - install_factor: install_factor parameter

Outputs:
    - material_cost: material_cost result
    - fab_cost: fab_cost result
    - install_cost: install_cost result
    - total_cost: total_cost result
    - idiot_index: idiot_index result

SysML Source: models/tests/solar_battery/library.sysml:27

    SysML Source: models/tests/solar_battery/library.sysml:27

    Calculation Specification:
        cost_per_watt = 1.07
        fab_factor = 0.45
        install_factor = 0.3
        material_cost = wattage * cost_per_watt
        fab_cost = material_cost * fab_factor
        install_cost = material_cost * install_factor
        total_cost = material_cost + fab_cost + install_cost
        idiot_index = total_cost / material_cost
        
Documentation:
Cost calculation for photovoltaic modules.
Material cost driven by wattage and cost per watt.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

    IMPLEMENTATION: See solar_battery_v2.handwritten.solarbatterylibrary.pvmodulecostcalc_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts material_cost, fab_cost, install_cost, total_cost, idiot_index fields to separate channels.
    """

    name: str = "PVModuleCostCalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, wattage: float, efficiency: float, cost_per_watt: float, fab_factor: float, install_factor: float    ) -> PVModuleCostCalcInput:
        """Validate inputs and fill defaults.

        Args:
            wattage: wattage input
            efficiency: efficiency input
            cost_per_watt: cost_per_watt input
            fab_factor: fab_factor input
            install_factor: install_factor input

        Returns:
            Validated input model
        """
        return PVModuleCostCalcInput(wattage=wattage, efficiency=efficiency, cost_per_watt=cost_per_watt, fab_factor=fab_factor, install_factor=install_factor)

    def run(
        self, wattage: float, efficiency: float, cost_per_watt: float, fab_factor: float, install_factor: float    ) -> ModuleResult[PVModuleCostCalcOutput]:
        """Execute calculation.

        Args:
            wattage: wattage input
            efficiency: efficiency input
            cost_per_watt: cost_per_watt input
            fab_factor: fab_factor input
            install_factor: install_factor input

        Returns:
            Module result with PVModuleCostCalcOutput (material_cost, fab_cost, install_cost, total_cost, idiot_index)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(wattage, efficiency, cost_per_watt, fab_factor, install_factor)

        # Import handwritten implementation
        from solar_battery_v2.handwritten.solarbatterylibrary.pvmodulecostcalc_impl import (
            run_pvmodulecostcalc,
        )

        # Execute implementation - returns tuple of values
        material_cost, fab_cost, install_cost, total_cost, idiot_index = run_pvmodulecostcalc(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=PVModuleCostCalcOutput(
                material_cost=material_cost,
                fab_cost=fab_cost,
                install_cost=install_cost,
                total_cost=total_cost,
                idiot_index=idiot_index,
            )
        )
