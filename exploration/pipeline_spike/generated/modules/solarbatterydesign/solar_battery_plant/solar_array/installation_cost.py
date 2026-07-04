"""installation_costModule Module Wrapper

TEAx module for installation_cost calculation.

Inputs:
    - pv_module_installation_cost: pv_module_installation_cost parameter
    - module_count: module_count parameter
    - inverter_installation_cost: inverter_installation_cost parameter
    - inverter_count: inverter_count parameter
    - array_bos_installation_cost: array_bos_installation_cost parameter

Outputs:
    - installation_cost: installation_cost result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterydesign/solar_battery_plant/solar_array/installation_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_tea.primitives import Float


class installation_costInput(BaseModel):
    """Input model for installation_costModule.

    Attributes:
        pv_module_installation_cost: pv_module_installation_cost input
        module_count: module_count input
        inverter_installation_cost: inverter_installation_cost input
        inverter_count: inverter_count input
        array_bos_installation_cost: array_bos_installation_cost input
    """
    pv_module_installation_cost: float = Field(..., description="pv_module_installation_cost input")
    module_count: float = Field(..., description="module_count input")
    inverter_installation_cost: float = Field(..., description="inverter_installation_cost input")
    inverter_count: float = Field(..., description="inverter_count input")
    array_bos_installation_cost: float = Field(..., description="array_bos_installation_cost input")


class installation_costModule(ModuleBase[installation_costInput, Float]):
    """TEAx module for installation_cost calculation.

Inputs:
    - pv_module_installation_cost: pv_module_installation_cost parameter
    - module_count: module_count parameter
    - inverter_installation_cost: inverter_installation_cost parameter
    - inverter_count: inverter_count parameter
    - array_bos_installation_cost: array_bos_installation_cost parameter

Outputs:
    - installation_cost: installation_cost result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        sum(pv_module.installation_cost) + sum(inverter.installation_cost) + array_bos.installation_cost

    IMPLEMENTATION: See solar_battery_tea.handwritten.solarbatterydesign.solar_battery_plant.solar_array.installation_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "installation_costModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, pv_module_installation_cost: float, module_count: float, inverter_installation_cost: float, inverter_count: float, array_bos_installation_cost: float    ) -> installation_costInput:
        """Validate inputs and fill defaults.

        Args:
            pv_module_installation_cost: pv_module_installation_cost input
            module_count: module_count input
            inverter_installation_cost: inverter_installation_cost input
            inverter_count: inverter_count input
            array_bos_installation_cost: array_bos_installation_cost input

        Returns:
            Validated input model
        """
        return installation_costInput(pv_module_installation_cost=pv_module_installation_cost, module_count=module_count, inverter_installation_cost=inverter_installation_cost, inverter_count=inverter_count, array_bos_installation_cost=array_bos_installation_cost)

    def run(
        self, pv_module_installation_cost: float, module_count: float, inverter_installation_cost: float, inverter_count: float, array_bos_installation_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            pv_module_installation_cost: pv_module_installation_cost input
            module_count: module_count input
            inverter_installation_cost: inverter_installation_cost input
            inverter_count: inverter_count input
            array_bos_installation_cost: array_bos_installation_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(pv_module_installation_cost, module_count, inverter_installation_cost, inverter_count, array_bos_installation_cost)

        # Import handwritten implementation
        from solar_battery_tea.handwritten.solarbatterydesign.solar_battery_plant.solar_array.installation_cost_impl import (
            run_installation_cost,
        )

        # Execute implementation - returns single value
        installation_cost = run_installation_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(installation_cost))
