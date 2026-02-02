"""BatteryBOSCostCalcModule Module Wrapper

TEAx module for BatteryBOSCostCalc calculation.

Cost calculation for battery balance-of-system.
Includes management system, wiring, thermal management per pack.

*Source**: Battery industry cost modeling
*Last Updated**: 2026-02-01

Inputs:
    - pack_count: pack_count parameter
    - cost_per_pack_bos: cost_per_pack_bos parameter
    - fab_factor: fab_factor parameter
    - install_factor: install_factor parameter

Outputs:
    - material_cost: material_cost result
    - fab_cost: fab_cost result
    - install_cost: install_cost result
    - total_cost: total_cost result
    - idiot_index: idiot_index result

SysML Source: models/tests/solar_battery/library.sysml:141

SysML Source: models/tests/solar_battery/library.sysml:141

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterylibrary/batteryboscostcalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery.primitives import Float
from solar_battery.schemas.batteryboscostcalc_output import BatteryBOSCostCalcOutput


class BatteryBOSCostCalcInput(BaseModel):
    """Input model for BatteryBOSCostCalcModule.

    Attributes:
        pack_count: pack_count input
        cost_per_pack_bos: cost_per_pack_bos input
        fab_factor: fab_factor input
        install_factor: install_factor input
    """
    pack_count: float = Field(..., description="pack_count input")
    cost_per_pack_bos: float = Field(..., description="cost_per_pack_bos input")
    fab_factor: float = Field(..., description="fab_factor input")
    install_factor: float = Field(..., description="install_factor input")


class BatteryBOSCostCalcModule(ModuleBase[BatteryBOSCostCalcInput, BatteryBOSCostCalcOutput]):
    """TEAx module for BatteryBOSCostCalc calculation.

Cost calculation for battery balance-of-system.
Includes management system, wiring, thermal management per pack.

*Source**: Battery industry cost modeling
*Last Updated**: 2026-02-01

Inputs:
    - pack_count: pack_count parameter
    - cost_per_pack_bos: cost_per_pack_bos parameter
    - fab_factor: fab_factor parameter
    - install_factor: install_factor parameter

Outputs:
    - material_cost: material_cost result
    - fab_cost: fab_cost result
    - install_cost: install_cost result
    - total_cost: total_cost result
    - idiot_index: idiot_index result

SysML Source: models/tests/solar_battery/library.sysml:141

    SysML Source: models/tests/solar_battery/library.sysml:141

    Calculation Specification:
        material_cost = pack_count * cost_per_pack_bos
        fab_cost = material_cost * fab_factor
        install_cost = material_cost * install_factor
        total_cost = material_cost + fab_cost + install_cost
        idiot_index = total_cost / material_cost
        
Documentation:
Cost calculation for battery balance-of-system.
Includes management system, wiring, thermal management per pack.

*Source**: Battery industry cost modeling
*Last Updated**: 2026-02-01

    IMPLEMENTATION: See solar_battery.handwritten.solarbatterylibrary.batteryboscostcalc_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts material_cost, fab_cost, install_cost, total_cost, idiot_index fields to separate channels.
    """

    name: str = "BatteryBOSCostCalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, pack_count: float, cost_per_pack_bos: float, fab_factor: float, install_factor: float    ) -> BatteryBOSCostCalcInput:
        """Validate inputs and fill defaults.

        Args:
            pack_count: pack_count input
            cost_per_pack_bos: cost_per_pack_bos input
            fab_factor: fab_factor input
            install_factor: install_factor input

        Returns:
            Validated input model
        """
        return BatteryBOSCostCalcInput(pack_count=pack_count, cost_per_pack_bos=cost_per_pack_bos, fab_factor=fab_factor, install_factor=install_factor)

    def run(
        self, pack_count: float, cost_per_pack_bos: float, fab_factor: float, install_factor: float    ) -> ModuleResult[BatteryBOSCostCalcOutput]:
        """Execute calculation.

        Args:
            pack_count: pack_count input
            cost_per_pack_bos: cost_per_pack_bos input
            fab_factor: fab_factor input
            install_factor: install_factor input

        Returns:
            Module result with BatteryBOSCostCalcOutput (material_cost, fab_cost, install_cost, total_cost, idiot_index)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(pack_count, cost_per_pack_bos, fab_factor, install_factor)

        # Import handwritten implementation
        from solar_battery.handwritten.solarbatterylibrary.batteryboscostcalc_impl import (
            run_batteryboscostcalc,
        )

        # Execute implementation - returns tuple of values
        material_cost, fab_cost, install_cost, total_cost, idiot_index = run_batteryboscostcalc(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=BatteryBOSCostCalcOutput(
                material_cost=material_cost,
                fab_cost=fab_cost,
                install_cost=install_cost,
                total_cost=total_cost,
                idiot_index=idiot_index,
            )
        )
