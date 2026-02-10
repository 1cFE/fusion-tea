"""RackingCostCalcModule Module Wrapper

TEAx module for RackingCostCalc calculation.

Cost calculation for racking and mounting hardware.
Material cost driven by panel count. Tilt angle is a design parameter
but does not affect cost in this simplified model.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

Inputs:
    - panel_count: panel_count parameter
    - tilt_angle: tilt_angle parameter
    - cost_per_panel_rack: cost_per_panel_rack parameter
    - fab_factor: fab_factor parameter
    - install_factor: install_factor parameter

Outputs:
    - material_cost: material_cost result
    - fab_cost: fab_cost result
    - install_cost: install_cost result
    - total_cost: total_cost result
    - idiot_index: idiot_index result

SysML Source: models/tests/solar_battery/library.sysml:163

SysML Source: models/tests/solar_battery/library.sysml:163

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterylibrary/rackingcostcalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery.primitives import Float
from solar_battery.schemas.rackingcostcalc_output import RackingCostCalcOutput


class RackingCostCalcInput(BaseModel):
    """Input model for RackingCostCalcModule.

    Attributes:
        panel_count: panel_count input
        tilt_angle: tilt_angle input
        cost_per_panel_rack: cost_per_panel_rack input
        fab_factor: fab_factor input
        install_factor: install_factor input
    """
    panel_count: float = Field(..., description="panel_count input")
    tilt_angle: float = Field(..., description="tilt_angle input")
    cost_per_panel_rack: float = Field(..., description="cost_per_panel_rack input")
    fab_factor: float = Field(..., description="fab_factor input")
    install_factor: float = Field(..., description="install_factor input")


class RackingCostCalcModule(ModuleBase[RackingCostCalcInput, RackingCostCalcOutput]):
    """TEAx module for RackingCostCalc calculation.

Cost calculation for racking and mounting hardware.
Material cost driven by panel count. Tilt angle is a design parameter
but does not affect cost in this simplified model.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

Inputs:
    - panel_count: panel_count parameter
    - tilt_angle: tilt_angle parameter
    - cost_per_panel_rack: cost_per_panel_rack parameter
    - fab_factor: fab_factor parameter
    - install_factor: install_factor parameter

Outputs:
    - material_cost: material_cost result
    - fab_cost: fab_cost result
    - install_cost: install_cost result
    - total_cost: total_cost result
    - idiot_index: idiot_index result

SysML Source: models/tests/solar_battery/library.sysml:163

    SysML Source: models/tests/solar_battery/library.sysml:163

    Calculation Specification:
        cost_per_panel_rack = 57.0
        fab_factor = 0.45
        install_factor = 0.3
        material_cost = panel_count * cost_per_panel_rack
        fab_cost = material_cost * fab_factor
        install_cost = material_cost * install_factor
        total_cost = material_cost + fab_cost + install_cost
        idiot_index = total_cost / material_cost
        
Documentation:
Cost calculation for racking and mounting hardware.
Material cost driven by panel count. Tilt angle is a design parameter
but does not affect cost in this simplified model.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

    IMPLEMENTATION: See solar_battery.handwritten.solarbatterylibrary.rackingcostcalc_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts material_cost, fab_cost, install_cost, total_cost, idiot_index fields to separate channels.
    """

    name: str = "RackingCostCalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, panel_count: float, tilt_angle: float, cost_per_panel_rack: float, fab_factor: float, install_factor: float    ) -> RackingCostCalcInput:
        """Validate inputs and fill defaults.

        Args:
            panel_count: panel_count input
            tilt_angle: tilt_angle input
            cost_per_panel_rack: cost_per_panel_rack input
            fab_factor: fab_factor input
            install_factor: install_factor input

        Returns:
            Validated input model
        """
        return RackingCostCalcInput(panel_count=panel_count, tilt_angle=tilt_angle, cost_per_panel_rack=cost_per_panel_rack, fab_factor=fab_factor, install_factor=install_factor)

    def run(
        self, panel_count: float, tilt_angle: float, cost_per_panel_rack: float, fab_factor: float, install_factor: float    ) -> ModuleResult[RackingCostCalcOutput]:
        """Execute calculation.

        Args:
            panel_count: panel_count input
            tilt_angle: tilt_angle input
            cost_per_panel_rack: cost_per_panel_rack input
            fab_factor: fab_factor input
            install_factor: install_factor input

        Returns:
            Module result with RackingCostCalcOutput (material_cost, fab_cost, install_cost, total_cost, idiot_index)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(panel_count, tilt_angle, cost_per_panel_rack, fab_factor, install_factor)

        # Import handwritten implementation
        from solar_battery.handwritten.solarbatterylibrary.rackingcostcalc_impl import (
            run_rackingcostcalc,
        )

        # Execute implementation - returns tuple of values
        material_cost, fab_cost, install_cost, total_cost, idiot_index = run_rackingcostcalc(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=RackingCostCalcOutput(
                material_cost=material_cost,
                fab_cost=fab_cost,
                install_cost=install_cost,
                total_cost=total_cost,
                idiot_index=idiot_index,
            )
        )
