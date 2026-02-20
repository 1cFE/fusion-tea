"""fabrication_costModule Module Wrapper

TEAx module for fabrication_cost calculation.

Inputs:
    - battery_pack_fabrication_cost: battery_pack_fabrication_cost parameter
    - pack_count: pack_count parameter
    - hybrid_inverter_fabrication_cost: hybrid_inverter_fabrication_cost parameter
    - battery_bos_fabrication_cost: battery_bos_fabrication_cost parameter

Outputs:
    - fabrication_cost: fabrication_cost result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterydesign/solar_battery_plant/battery_system/fabrication_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_v5.primitives import Float


class fabrication_costInput(BaseModel):
    """Input model for fabrication_costModule.

    Attributes:
        battery_pack_fabrication_cost: battery_pack_fabrication_cost input
        pack_count: pack_count input
        hybrid_inverter_fabrication_cost: hybrid_inverter_fabrication_cost input
        battery_bos_fabrication_cost: battery_bos_fabrication_cost input
    """
    battery_pack_fabrication_cost: float = Field(..., description="battery_pack_fabrication_cost input")
    pack_count: float = Field(..., description="pack_count input")
    hybrid_inverter_fabrication_cost: float = Field(..., description="hybrid_inverter_fabrication_cost input")
    battery_bos_fabrication_cost: float = Field(..., description="battery_bos_fabrication_cost input")


class fabrication_costModule(ModuleBase[fabrication_costInput, Float]):
    """TEAx module for fabrication_cost calculation.

Inputs:
    - battery_pack_fabrication_cost: battery_pack_fabrication_cost parameter
    - pack_count: pack_count parameter
    - hybrid_inverter_fabrication_cost: hybrid_inverter_fabrication_cost parameter
    - battery_bos_fabrication_cost: battery_bos_fabrication_cost parameter

Outputs:
    - fabrication_cost: fabrication_cost result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        sum(battery_pack.fabrication_cost) + hybrid_inverter.fabrication_cost + battery_bos.fabrication_cost

    IMPLEMENTATION: See solar_battery_v5.handwritten.solarbatterydesign.solar_battery_plant.battery_system.fabrication_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "fabrication_costModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, battery_pack_fabrication_cost: float, pack_count: float, hybrid_inverter_fabrication_cost: float, battery_bos_fabrication_cost: float    ) -> fabrication_costInput:
        """Validate inputs and fill defaults.

        Args:
            battery_pack_fabrication_cost: battery_pack_fabrication_cost input
            pack_count: pack_count input
            hybrid_inverter_fabrication_cost: hybrid_inverter_fabrication_cost input
            battery_bos_fabrication_cost: battery_bos_fabrication_cost input

        Returns:
            Validated input model
        """
        return fabrication_costInput(battery_pack_fabrication_cost=battery_pack_fabrication_cost, pack_count=pack_count, hybrid_inverter_fabrication_cost=hybrid_inverter_fabrication_cost, battery_bos_fabrication_cost=battery_bos_fabrication_cost)

    def run(
        self, battery_pack_fabrication_cost: float, pack_count: float, hybrid_inverter_fabrication_cost: float, battery_bos_fabrication_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            battery_pack_fabrication_cost: battery_pack_fabrication_cost input
            pack_count: pack_count input
            hybrid_inverter_fabrication_cost: hybrid_inverter_fabrication_cost input
            battery_bos_fabrication_cost: battery_bos_fabrication_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(battery_pack_fabrication_cost, pack_count, hybrid_inverter_fabrication_cost, battery_bos_fabrication_cost)

        # Import handwritten implementation
        from solar_battery_v5.handwritten.solarbatterydesign.solar_battery_plant.battery_system.fabrication_cost_impl import (
            run_fabrication_cost,
        )

        # Execute implementation - returns single value
        fabrication_cost = run_fabrication_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(fabrication_cost))
