"""ArrayBOSCostCalcModule Module Wrapper

TEAx module for ArrayBOSCostCalc calculation.

Cost calculation for solar array balance-of-system.
Includes combiners, disconnects, conduit per string and per panel.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

Inputs:
    - string_count: string_count parameter
    - panel_count: panel_count parameter
    - cost_per_string: cost_per_string parameter
    - cost_per_panel_bos: cost_per_panel_bos parameter
    - fab_factor: fab_factor parameter
    - install_factor: install_factor parameter

Outputs:
    - material_cost: material_cost result
    - fab_cost: fab_cost result
    - install_cost: install_cost result
    - total_cost: total_cost result
    - idiot_index: idiot_index result

SysML Source: solar_battery_model/library.sysml:72

SysML Source: solar_battery_model/library.sysml:72

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterylibrary/arrayboscostcalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_tea.primitives import Float
from solar_battery_tea.schemas.arrayboscostcalc_output import ArrayBOSCostCalcOutput


class ArrayBOSCostCalcInput(BaseModel):
    """Input model for ArrayBOSCostCalcModule.

    Attributes:
        string_count: string_count input
        panel_count: panel_count input
        cost_per_string: cost_per_string input
        cost_per_panel_bos: cost_per_panel_bos input
        fab_factor: fab_factor input
        install_factor: install_factor input
    """
    string_count: float = Field(..., description="string_count input")
    panel_count: float = Field(..., description="panel_count input")
    cost_per_string: float = Field(..., description="cost_per_string input")
    cost_per_panel_bos: float = Field(..., description="cost_per_panel_bos input")
    fab_factor: float = Field(..., description="fab_factor input")
    install_factor: float = Field(..., description="install_factor input")


class ArrayBOSCostCalcModule(ModuleBase[ArrayBOSCostCalcInput, ArrayBOSCostCalcOutput]):
    """TEAx module for ArrayBOSCostCalc calculation.

Cost calculation for solar array balance-of-system.
Includes combiners, disconnects, conduit per string and per panel.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

Inputs:
    - string_count: string_count parameter
    - panel_count: panel_count parameter
    - cost_per_string: cost_per_string parameter
    - cost_per_panel_bos: cost_per_panel_bos parameter
    - fab_factor: fab_factor parameter
    - install_factor: install_factor parameter

Outputs:
    - material_cost: material_cost result
    - fab_cost: fab_cost result
    - install_cost: install_cost result
    - total_cost: total_cost result
    - idiot_index: idiot_index result

SysML Source: solar_battery_model/library.sysml:72

    SysML Source: solar_battery_model/library.sysml:72

    Calculation Specification:
        cost_per_string = LiteralRationalEvaluation()
        cost_per_panel_bos = LiteralRationalEvaluation()
        fab_factor = LiteralRationalEvaluation()
        install_factor = LiteralRationalEvaluation()
        material_cost = string_count * cost_per_string + panel_count * cost_per_panel_bos
        fab_cost = material_cost * fab_factor
        install_cost = material_cost * install_factor
        total_cost = material_cost + fab_cost + install_cost
        idiot_index = total_cost / material_cost
        
Documentation:
Cost calculation for solar array balance-of-system.
Includes combiners, disconnects, conduit per string and per panel.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

    IMPLEMENTATION: See solar_battery_tea.handwritten.solarbatterylibrary.arrayboscostcalc_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts material_cost, fab_cost, install_cost, total_cost, idiot_index fields to separate channels.
    """

    name: str = "ArrayBOSCostCalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, string_count: float, panel_count: float, cost_per_string: float, cost_per_panel_bos: float, fab_factor: float, install_factor: float    ) -> ArrayBOSCostCalcInput:
        """Validate inputs and fill defaults.

        Args:
            string_count: string_count input
            panel_count: panel_count input
            cost_per_string: cost_per_string input
            cost_per_panel_bos: cost_per_panel_bos input
            fab_factor: fab_factor input
            install_factor: install_factor input

        Returns:
            Validated input model
        """
        return ArrayBOSCostCalcInput(string_count=string_count, panel_count=panel_count, cost_per_string=cost_per_string, cost_per_panel_bos=cost_per_panel_bos, fab_factor=fab_factor, install_factor=install_factor)

    def run(
        self, string_count: float, panel_count: float, cost_per_string: float, cost_per_panel_bos: float, fab_factor: float, install_factor: float    ) -> ModuleResult[ArrayBOSCostCalcOutput]:
        """Execute calculation.

        Args:
            string_count: string_count input
            panel_count: panel_count input
            cost_per_string: cost_per_string input
            cost_per_panel_bos: cost_per_panel_bos input
            fab_factor: fab_factor input
            install_factor: install_factor input

        Returns:
            Module result with ArrayBOSCostCalcOutput (material_cost, fab_cost, install_cost, total_cost, idiot_index)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(string_count, panel_count, cost_per_string, cost_per_panel_bos, fab_factor, install_factor)

        # Import handwritten implementation
        from solar_battery_tea.handwritten.solarbatterylibrary.arrayboscostcalc_impl import (
            run_arrayboscostcalc,
        )

        # Execute implementation - returns tuple of values
        material_cost, fab_cost, install_cost, total_cost, idiot_index = run_arrayboscostcalc(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=ArrayBOSCostCalcOutput(
                material_cost=material_cost,
                fab_cost=fab_cost,
                install_cost=install_cost,
                total_cost=total_cost,
                idiot_index=idiot_index,
            )
        )
