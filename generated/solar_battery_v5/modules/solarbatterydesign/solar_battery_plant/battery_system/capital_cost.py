"""capital_costModule Module Wrapper

TEAx module for capital_cost calculation.

Inputs:
    - battery_pack_capital_cost: battery_pack_capital_cost parameter
    - pack_count: pack_count parameter
    - hybrid_inverter_capital_cost: hybrid_inverter_capital_cost parameter
    - battery_bos_capital_cost: battery_bos_capital_cost parameter

Outputs:
    - capital_cost: capital_cost result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterydesign/solar_battery_plant/battery_system/capital_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_v5.primitives import Float


class capital_costInput(BaseModel):
    """Input model for capital_costModule.

    Attributes:
        battery_pack_capital_cost: battery_pack_capital_cost input
        pack_count: pack_count input
        hybrid_inverter_capital_cost: hybrid_inverter_capital_cost input
        battery_bos_capital_cost: battery_bos_capital_cost input
    """
    battery_pack_capital_cost: float = Field(..., description="battery_pack_capital_cost input")
    pack_count: float = Field(..., description="pack_count input")
    hybrid_inverter_capital_cost: float = Field(..., description="hybrid_inverter_capital_cost input")
    battery_bos_capital_cost: float = Field(..., description="battery_bos_capital_cost input")


class capital_costModule(ModuleBase[capital_costInput, Float]):
    """TEAx module for capital_cost calculation.

Inputs:
    - battery_pack_capital_cost: battery_pack_capital_cost parameter
    - pack_count: pack_count parameter
    - hybrid_inverter_capital_cost: hybrid_inverter_capital_cost parameter
    - battery_bos_capital_cost: battery_bos_capital_cost parameter

Outputs:
    - capital_cost: capital_cost result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        sum(battery_pack.capital_cost) + hybrid_inverter.capital_cost + battery_bos.capital_cost

    IMPLEMENTATION: See solar_battery_v5.handwritten.solarbatterydesign.solar_battery_plant.battery_system.capital_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "capital_costModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, battery_pack_capital_cost: float, pack_count: float, hybrid_inverter_capital_cost: float, battery_bos_capital_cost: float    ) -> capital_costInput:
        """Validate inputs and fill defaults.

        Args:
            battery_pack_capital_cost: battery_pack_capital_cost input
            pack_count: pack_count input
            hybrid_inverter_capital_cost: hybrid_inverter_capital_cost input
            battery_bos_capital_cost: battery_bos_capital_cost input

        Returns:
            Validated input model
        """
        return capital_costInput(battery_pack_capital_cost=battery_pack_capital_cost, pack_count=pack_count, hybrid_inverter_capital_cost=hybrid_inverter_capital_cost, battery_bos_capital_cost=battery_bos_capital_cost)

    def run(
        self, battery_pack_capital_cost: float, pack_count: float, hybrid_inverter_capital_cost: float, battery_bos_capital_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            battery_pack_capital_cost: battery_pack_capital_cost input
            pack_count: pack_count input
            hybrid_inverter_capital_cost: hybrid_inverter_capital_cost input
            battery_bos_capital_cost: battery_bos_capital_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(battery_pack_capital_cost, pack_count, hybrid_inverter_capital_cost, battery_bos_capital_cost)

        # Import handwritten implementation
        from solar_battery_v5.handwritten.solarbatterydesign.solar_battery_plant.battery_system.capital_cost_impl import (
            run_capital_cost,
        )

        # Execute implementation - returns single value
        capital_cost = run_capital_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(capital_cost))
