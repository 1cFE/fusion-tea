"""raw_material_costModule Module Wrapper

TEAx module for raw_material_cost calculation.

Inputs:
    - pv_module_raw_material_cost: pv_module_raw_material_cost parameter
    - module_count: module_count parameter
    - inverter_raw_material_cost: inverter_raw_material_cost parameter
    - inverter_count: inverter_count parameter
    - array_bos_raw_material_cost: array_bos_raw_material_cost parameter
    - allocation_model_material_portion: allocation_model_material_portion parameter

Outputs:
    - raw_material_cost: raw_material_cost result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterydesign/solar_battery_plant/solar_array/raw_material_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_tea.primitives import Float


class raw_material_costInput(BaseModel):
    """Input model for raw_material_costModule.

    Attributes:
        pv_module_raw_material_cost: pv_module_raw_material_cost input
        module_count: module_count input
        inverter_raw_material_cost: inverter_raw_material_cost input
        inverter_count: inverter_count input
        array_bos_raw_material_cost: array_bos_raw_material_cost input
        allocation_model_material_portion: allocation_model_material_portion input
    """
    pv_module_raw_material_cost: float = Field(..., description="pv_module_raw_material_cost input")
    module_count: float = Field(..., description="module_count input")
    inverter_raw_material_cost: float = Field(..., description="inverter_raw_material_cost input")
    inverter_count: float = Field(..., description="inverter_count input")
    array_bos_raw_material_cost: float = Field(..., description="array_bos_raw_material_cost input")
    allocation_model_material_portion: float = Field(..., description="allocation_model_material_portion input")


class raw_material_costModule(ModuleBase[raw_material_costInput, Float]):
    """TEAx module for raw_material_cost calculation.

Inputs:
    - pv_module_raw_material_cost: pv_module_raw_material_cost parameter
    - module_count: module_count parameter
    - inverter_raw_material_cost: inverter_raw_material_cost parameter
    - inverter_count: inverter_count parameter
    - array_bos_raw_material_cost: array_bos_raw_material_cost parameter
    - allocation_model_material_portion: allocation_model_material_portion parameter

Outputs:
    - raw_material_cost: raw_material_cost result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        sum(pv_module.raw_material_cost) + sum(inverter.raw_material_cost) + array_bos.raw_material_cost + allocation_model.material_portion

    IMPLEMENTATION: See solar_battery_tea.handwritten.solarbatterydesign.solar_battery_plant.solar_array.raw_material_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "raw_material_costModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, pv_module_raw_material_cost: float, module_count: float, inverter_raw_material_cost: float, inverter_count: float, array_bos_raw_material_cost: float, allocation_model_material_portion: float    ) -> raw_material_costInput:
        """Validate inputs and fill defaults.

        Args:
            pv_module_raw_material_cost: pv_module_raw_material_cost input
            module_count: module_count input
            inverter_raw_material_cost: inverter_raw_material_cost input
            inverter_count: inverter_count input
            array_bos_raw_material_cost: array_bos_raw_material_cost input
            allocation_model_material_portion: allocation_model_material_portion input

        Returns:
            Validated input model
        """
        return raw_material_costInput(pv_module_raw_material_cost=pv_module_raw_material_cost, module_count=module_count, inverter_raw_material_cost=inverter_raw_material_cost, inverter_count=inverter_count, array_bos_raw_material_cost=array_bos_raw_material_cost, allocation_model_material_portion=allocation_model_material_portion)

    def run(
        self, pv_module_raw_material_cost: float, module_count: float, inverter_raw_material_cost: float, inverter_count: float, array_bos_raw_material_cost: float, allocation_model_material_portion: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            pv_module_raw_material_cost: pv_module_raw_material_cost input
            module_count: module_count input
            inverter_raw_material_cost: inverter_raw_material_cost input
            inverter_count: inverter_count input
            array_bos_raw_material_cost: array_bos_raw_material_cost input
            allocation_model_material_portion: allocation_model_material_portion input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(pv_module_raw_material_cost, module_count, inverter_raw_material_cost, inverter_count, array_bos_raw_material_cost, allocation_model_material_portion)

        # Import handwritten implementation
        from solar_battery_tea.handwritten.solarbatterydesign.solar_battery_plant.solar_array.raw_material_cost_impl import (
            run_raw_material_cost,
        )

        # Execute implementation - returns single value
        raw_material_cost = run_raw_material_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(raw_material_cost))
