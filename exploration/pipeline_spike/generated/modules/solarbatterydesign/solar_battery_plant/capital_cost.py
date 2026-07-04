"""capital_costModule Module Wrapper

TEAx module for capital_cost calculation.

Inputs:
    - solar_array_capital_cost: solar_array_capital_cost parameter
    - battery_system_capital_cost: battery_system_capital_cost parameter
    - site_infra_capital_cost: site_infra_capital_cost parameter

Outputs:
    - capital_cost: capital_cost result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterydesign/solar_battery_plant/capital_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_tea.primitives import Float


class capital_costInput(BaseModel):
    """Input model for capital_costModule.

    Attributes:
        solar_array_capital_cost: solar_array_capital_cost input
        battery_system_capital_cost: battery_system_capital_cost input
        site_infra_capital_cost: site_infra_capital_cost input
    """
    solar_array_capital_cost: float = Field(..., description="solar_array_capital_cost input")
    battery_system_capital_cost: float = Field(..., description="battery_system_capital_cost input")
    site_infra_capital_cost: float = Field(..., description="site_infra_capital_cost input")


class capital_costModule(ModuleBase[capital_costInput, Float]):
    """TEAx module for capital_cost calculation.

Inputs:
    - solar_array_capital_cost: solar_array_capital_cost parameter
    - battery_system_capital_cost: battery_system_capital_cost parameter
    - site_infra_capital_cost: site_infra_capital_cost parameter

Outputs:
    - capital_cost: capital_cost result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        solar_array.capital_cost + battery_system.capital_cost + site_infra.capital_cost

    IMPLEMENTATION: See solar_battery_tea.handwritten.solarbatterydesign.solar_battery_plant.capital_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "capital_costModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, solar_array_capital_cost: float, battery_system_capital_cost: float, site_infra_capital_cost: float    ) -> capital_costInput:
        """Validate inputs and fill defaults.

        Args:
            solar_array_capital_cost: solar_array_capital_cost input
            battery_system_capital_cost: battery_system_capital_cost input
            site_infra_capital_cost: site_infra_capital_cost input

        Returns:
            Validated input model
        """
        return capital_costInput(solar_array_capital_cost=solar_array_capital_cost, battery_system_capital_cost=battery_system_capital_cost, site_infra_capital_cost=site_infra_capital_cost)

    def run(
        self, solar_array_capital_cost: float, battery_system_capital_cost: float, site_infra_capital_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            solar_array_capital_cost: solar_array_capital_cost input
            battery_system_capital_cost: battery_system_capital_cost input
            site_infra_capital_cost: site_infra_capital_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(solar_array_capital_cost, battery_system_capital_cost, site_infra_capital_cost)

        # Import handwritten implementation
        from solar_battery_tea.handwritten.solarbatterydesign.solar_battery_plant.capital_cost_impl import (
            run_capital_cost,
        )

        # Execute implementation - returns single value
        capital_cost = run_capital_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(capital_cost))
