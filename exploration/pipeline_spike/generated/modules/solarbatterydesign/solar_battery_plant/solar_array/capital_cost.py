"""capital_costModule Module Wrapper

TEAx module for capital_cost calculation.

Inputs:
    - pv_module_capital_cost: pv_module_capital_cost parameter
    - module_count: module_count parameter
    - inverter_capital_cost: inverter_capital_cost parameter
    - inverter_count: inverter_count parameter
    - array_bos_capital_cost: array_bos_capital_cost parameter
    - misc_hardware_cost: misc_hardware_cost parameter

Outputs:
    - capital_cost: capital_cost result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterydesign/solar_battery_plant/solar_array/capital_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_tea.primitives import Float


class capital_costInput(BaseModel):
    """Input model for capital_costModule.

    Attributes:
        pv_module_capital_cost: pv_module_capital_cost input
        module_count: module_count input
        inverter_capital_cost: inverter_capital_cost input
        inverter_count: inverter_count input
        array_bos_capital_cost: array_bos_capital_cost input
        misc_hardware_cost: misc_hardware_cost input
    """
    pv_module_capital_cost: float = Field(..., description="pv_module_capital_cost input")
    module_count: float = Field(..., description="module_count input")
    inverter_capital_cost: float = Field(..., description="inverter_capital_cost input")
    inverter_count: float = Field(..., description="inverter_count input")
    array_bos_capital_cost: float = Field(..., description="array_bos_capital_cost input")
    misc_hardware_cost: float = Field(..., description="misc_hardware_cost input")


class capital_costModule(ModuleBase[capital_costInput, Float]):
    """TEAx module for capital_cost calculation.

Inputs:
    - pv_module_capital_cost: pv_module_capital_cost parameter
    - module_count: module_count parameter
    - inverter_capital_cost: inverter_capital_cost parameter
    - inverter_count: inverter_count parameter
    - array_bos_capital_cost: array_bos_capital_cost parameter
    - misc_hardware_cost: misc_hardware_cost parameter

Outputs:
    - capital_cost: capital_cost result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        sum(pv_module.capital_cost) + sum(inverter.capital_cost) + array_bos.capital_cost + misc_hardware_cost

    IMPLEMENTATION: See solar_battery_tea.handwritten.solarbatterydesign.solar_battery_plant.solar_array.capital_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "capital_costModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, pv_module_capital_cost: float, module_count: float, inverter_capital_cost: float, inverter_count: float, array_bos_capital_cost: float, misc_hardware_cost: float    ) -> capital_costInput:
        """Validate inputs and fill defaults.

        Args:
            pv_module_capital_cost: pv_module_capital_cost input
            module_count: module_count input
            inverter_capital_cost: inverter_capital_cost input
            inverter_count: inverter_count input
            array_bos_capital_cost: array_bos_capital_cost input
            misc_hardware_cost: misc_hardware_cost input

        Returns:
            Validated input model
        """
        return capital_costInput(pv_module_capital_cost=pv_module_capital_cost, module_count=module_count, inverter_capital_cost=inverter_capital_cost, inverter_count=inverter_count, array_bos_capital_cost=array_bos_capital_cost, misc_hardware_cost=misc_hardware_cost)

    def run(
        self, pv_module_capital_cost: float, module_count: float, inverter_capital_cost: float, inverter_count: float, array_bos_capital_cost: float, misc_hardware_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            pv_module_capital_cost: pv_module_capital_cost input
            module_count: module_count input
            inverter_capital_cost: inverter_capital_cost input
            inverter_count: inverter_count input
            array_bos_capital_cost: array_bos_capital_cost input
            misc_hardware_cost: misc_hardware_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(pv_module_capital_cost, module_count, inverter_capital_cost, inverter_count, array_bos_capital_cost, misc_hardware_cost)

        # Import handwritten implementation
        from solar_battery_tea.handwritten.solarbatterydesign.solar_battery_plant.solar_array.capital_cost_impl import (
            run_capital_cost,
        )

        # Execute implementation - returns single value
        capital_cost = run_capital_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(capital_cost))
