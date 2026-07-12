"""fabrication_costModule Module Wrapper

TEAx module for fabrication_cost calculation.

Inputs:
    - pv_module_fabrication_cost: pv_module_fabrication_cost parameter
    - module_count: module_count parameter
    - inverter_fabrication_cost: inverter_fabrication_cost parameter
    - inverter_count: inverter_count parameter
    - array_bos_fabrication_cost: array_bos_fabrication_cost parameter

Outputs:
    - fabrication_cost: fabrication_cost result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterydesign/solar_battery_plant/solar_array/fabrication_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_tea.primitives import Float


class fabrication_costInput(BaseModel):
    """Input model for fabrication_costModule.

    Attributes:
        pv_module_fabrication_cost: pv_module_fabrication_cost input
        module_count: module_count input
        inverter_fabrication_cost: inverter_fabrication_cost input
        inverter_count: inverter_count input
        array_bos_fabrication_cost: array_bos_fabrication_cost input
    """
    pv_module_fabrication_cost: float = Field(..., description="pv_module_fabrication_cost input")
    module_count: float = Field(..., description="module_count input")
    inverter_fabrication_cost: float = Field(..., description="inverter_fabrication_cost input")
    inverter_count: float = Field(..., description="inverter_count input")
    array_bos_fabrication_cost: float = Field(..., description="array_bos_fabrication_cost input")


class fabrication_costModule(ModuleBase[fabrication_costInput, Float]):
    """TEAx module for fabrication_cost calculation.

Inputs:
    - pv_module_fabrication_cost: pv_module_fabrication_cost parameter
    - module_count: module_count parameter
    - inverter_fabrication_cost: inverter_fabrication_cost parameter
    - inverter_count: inverter_count parameter
    - array_bos_fabrication_cost: array_bos_fabrication_cost parameter

Outputs:
    - fabrication_cost: fabrication_cost result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        sum(pv_module.fabrication_cost) + sum(inverter.fabrication_cost) + array_bos.fabrication_cost

    IMPLEMENTATION: See solar_battery_tea.handwritten.solarbatterydesign.solar_battery_plant.solar_array.fabrication_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "fabrication_costModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, pv_module_fabrication_cost: float, module_count: float, inverter_fabrication_cost: float, inverter_count: float, array_bos_fabrication_cost: float    ) -> fabrication_costInput:
        """Validate inputs and fill defaults.

        Args:
            pv_module_fabrication_cost: pv_module_fabrication_cost input
            module_count: module_count input
            inverter_fabrication_cost: inverter_fabrication_cost input
            inverter_count: inverter_count input
            array_bos_fabrication_cost: array_bos_fabrication_cost input

        Returns:
            Validated input model
        """
        return fabrication_costInput(pv_module_fabrication_cost=pv_module_fabrication_cost, module_count=module_count, inverter_fabrication_cost=inverter_fabrication_cost, inverter_count=inverter_count, array_bos_fabrication_cost=array_bos_fabrication_cost)

    def run(
        self, pv_module_fabrication_cost: float, module_count: float, inverter_fabrication_cost: float, inverter_count: float, array_bos_fabrication_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            pv_module_fabrication_cost: pv_module_fabrication_cost input
            module_count: module_count input
            inverter_fabrication_cost: inverter_fabrication_cost input
            inverter_count: inverter_count input
            array_bos_fabrication_cost: array_bos_fabrication_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(pv_module_fabrication_cost, module_count, inverter_fabrication_cost, inverter_count, array_bos_fabrication_cost)

        # Import handwritten implementation
        from solar_battery_tea.handwritten.solarbatterydesign.solar_battery_plant.solar_array.fabrication_cost_impl import (
            run_fabrication_cost,
        )

        # Execute implementation - returns single value
        fabrication_cost = run_fabrication_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(fabrication_cost))
