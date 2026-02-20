"""installation_costModule Module Wrapper

TEAx module for installation_cost calculation.

Inputs:
    - solar_array_installation_cost: solar_array_installation_cost parameter
    - battery_system_installation_cost: battery_system_installation_cost parameter
    - site_infra_installation_cost: site_infra_installation_cost parameter

Outputs:
    - installation_cost: installation_cost result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterydesign/solar_battery_plant/installation_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_v5.primitives import Float


class installation_costInput(BaseModel):
    """Input model for installation_costModule.

    Attributes:
        solar_array_installation_cost: solar_array_installation_cost input
        battery_system_installation_cost: battery_system_installation_cost input
        site_infra_installation_cost: site_infra_installation_cost input
    """
    solar_array_installation_cost: float = Field(..., description="solar_array_installation_cost input")
    battery_system_installation_cost: float = Field(..., description="battery_system_installation_cost input")
    site_infra_installation_cost: float = Field(..., description="site_infra_installation_cost input")


class installation_costModule(ModuleBase[installation_costInput, Float]):
    """TEAx module for installation_cost calculation.

Inputs:
    - solar_array_installation_cost: solar_array_installation_cost parameter
    - battery_system_installation_cost: battery_system_installation_cost parameter
    - site_infra_installation_cost: site_infra_installation_cost parameter

Outputs:
    - installation_cost: installation_cost result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        solar_array.installation_cost + battery_system.installation_cost + site_infra.installation_cost

    IMPLEMENTATION: See solar_battery_v5.handwritten.solarbatterydesign.solar_battery_plant.installation_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "installation_costModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, solar_array_installation_cost: float, battery_system_installation_cost: float, site_infra_installation_cost: float    ) -> installation_costInput:
        """Validate inputs and fill defaults.

        Args:
            solar_array_installation_cost: solar_array_installation_cost input
            battery_system_installation_cost: battery_system_installation_cost input
            site_infra_installation_cost: site_infra_installation_cost input

        Returns:
            Validated input model
        """
        return installation_costInput(solar_array_installation_cost=solar_array_installation_cost, battery_system_installation_cost=battery_system_installation_cost, site_infra_installation_cost=site_infra_installation_cost)

    def run(
        self, solar_array_installation_cost: float, battery_system_installation_cost: float, site_infra_installation_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            solar_array_installation_cost: solar_array_installation_cost input
            battery_system_installation_cost: battery_system_installation_cost input
            site_infra_installation_cost: site_infra_installation_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(solar_array_installation_cost, battery_system_installation_cost, site_infra_installation_cost)

        # Import handwritten implementation
        from solar_battery_v5.handwritten.solarbatterydesign.solar_battery_plant.installation_cost_impl import (
            run_installation_cost,
        )

        # Execute implementation - returns single value
        installation_cost = run_installation_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(installation_cost))
