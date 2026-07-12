"""raw_material_costModule Module Wrapper

TEAx module for raw_material_cost calculation.

Inputs:
    - battery_pack_raw_material_cost: battery_pack_raw_material_cost parameter
    - pack_count: pack_count parameter
    - hybrid_inverter_raw_material_cost: hybrid_inverter_raw_material_cost parameter
    - battery_bos_raw_material_cost: battery_bos_raw_material_cost parameter

Outputs:
    - raw_material_cost: raw_material_cost result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterydesign/solar_battery_plant/battery_system/raw_material_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_tea.primitives import Float


class raw_material_costInput(BaseModel):
    """Input model for raw_material_costModule.

    Attributes:
        battery_pack_raw_material_cost: battery_pack_raw_material_cost input
        pack_count: pack_count input
        hybrid_inverter_raw_material_cost: hybrid_inverter_raw_material_cost input
        battery_bos_raw_material_cost: battery_bos_raw_material_cost input
    """
    battery_pack_raw_material_cost: float = Field(..., description="battery_pack_raw_material_cost input")
    pack_count: float = Field(..., description="pack_count input")
    hybrid_inverter_raw_material_cost: float = Field(..., description="hybrid_inverter_raw_material_cost input")
    battery_bos_raw_material_cost: float = Field(..., description="battery_bos_raw_material_cost input")


class raw_material_costModule(ModuleBase[raw_material_costInput, Float]):
    """TEAx module for raw_material_cost calculation.

Inputs:
    - battery_pack_raw_material_cost: battery_pack_raw_material_cost parameter
    - pack_count: pack_count parameter
    - hybrid_inverter_raw_material_cost: hybrid_inverter_raw_material_cost parameter
    - battery_bos_raw_material_cost: battery_bos_raw_material_cost parameter

Outputs:
    - raw_material_cost: raw_material_cost result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        sum(battery_pack.raw_material_cost) + hybrid_inverter.raw_material_cost + battery_bos.raw_material_cost

    IMPLEMENTATION: See solar_battery_tea.handwritten.solarbatterydesign.solar_battery_plant.battery_system.raw_material_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "raw_material_costModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, battery_pack_raw_material_cost: float, pack_count: float, hybrid_inverter_raw_material_cost: float, battery_bos_raw_material_cost: float    ) -> raw_material_costInput:
        """Validate inputs and fill defaults.

        Args:
            battery_pack_raw_material_cost: battery_pack_raw_material_cost input
            pack_count: pack_count input
            hybrid_inverter_raw_material_cost: hybrid_inverter_raw_material_cost input
            battery_bos_raw_material_cost: battery_bos_raw_material_cost input

        Returns:
            Validated input model
        """
        return raw_material_costInput(battery_pack_raw_material_cost=battery_pack_raw_material_cost, pack_count=pack_count, hybrid_inverter_raw_material_cost=hybrid_inverter_raw_material_cost, battery_bos_raw_material_cost=battery_bos_raw_material_cost)

    def run(
        self, battery_pack_raw_material_cost: float, pack_count: float, hybrid_inverter_raw_material_cost: float, battery_bos_raw_material_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            battery_pack_raw_material_cost: battery_pack_raw_material_cost input
            pack_count: pack_count input
            hybrid_inverter_raw_material_cost: hybrid_inverter_raw_material_cost input
            battery_bos_raw_material_cost: battery_bos_raw_material_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(battery_pack_raw_material_cost, pack_count, hybrid_inverter_raw_material_cost, battery_bos_raw_material_cost)

        # Import handwritten implementation
        from solar_battery_tea.handwritten.solarbatterydesign.solar_battery_plant.battery_system.raw_material_cost_impl import (
            run_raw_material_cost,
        )

        # Execute implementation - returns single value
        raw_material_cost = run_raw_material_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(raw_material_cost))
