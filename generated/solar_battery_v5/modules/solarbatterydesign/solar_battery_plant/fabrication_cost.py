"""fabrication_costModule Module Wrapper

TEAx module for fabrication_cost calculation.

Inputs:
    - solar_array_fabrication_cost: solar_array_fabrication_cost parameter
    - battery_system_fabrication_cost: battery_system_fabrication_cost parameter
    - site_infra_fabrication_cost: site_infra_fabrication_cost parameter

Outputs:
    - fabrication_cost: fabrication_cost result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterydesign/solar_battery_plant/fabrication_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_v5.primitives import Float


class fabrication_costInput(BaseModel):
    """Input model for fabrication_costModule.

    Attributes:
        solar_array_fabrication_cost: solar_array_fabrication_cost input
        battery_system_fabrication_cost: battery_system_fabrication_cost input
        site_infra_fabrication_cost: site_infra_fabrication_cost input
    """
    solar_array_fabrication_cost: float = Field(..., description="solar_array_fabrication_cost input")
    battery_system_fabrication_cost: float = Field(..., description="battery_system_fabrication_cost input")
    site_infra_fabrication_cost: float = Field(..., description="site_infra_fabrication_cost input")


class fabrication_costModule(ModuleBase[fabrication_costInput, Float]):
    """TEAx module for fabrication_cost calculation.

Inputs:
    - solar_array_fabrication_cost: solar_array_fabrication_cost parameter
    - battery_system_fabrication_cost: battery_system_fabrication_cost parameter
    - site_infra_fabrication_cost: site_infra_fabrication_cost parameter

Outputs:
    - fabrication_cost: fabrication_cost result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        solar_array.fabrication_cost + battery_system.fabrication_cost + site_infra.fabrication_cost

    IMPLEMENTATION: See solar_battery_v5.handwritten.solarbatterydesign.solar_battery_plant.fabrication_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "fabrication_costModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, solar_array_fabrication_cost: float, battery_system_fabrication_cost: float, site_infra_fabrication_cost: float    ) -> fabrication_costInput:
        """Validate inputs and fill defaults.

        Args:
            solar_array_fabrication_cost: solar_array_fabrication_cost input
            battery_system_fabrication_cost: battery_system_fabrication_cost input
            site_infra_fabrication_cost: site_infra_fabrication_cost input

        Returns:
            Validated input model
        """
        return fabrication_costInput(solar_array_fabrication_cost=solar_array_fabrication_cost, battery_system_fabrication_cost=battery_system_fabrication_cost, site_infra_fabrication_cost=site_infra_fabrication_cost)

    def run(
        self, solar_array_fabrication_cost: float, battery_system_fabrication_cost: float, site_infra_fabrication_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            solar_array_fabrication_cost: solar_array_fabrication_cost input
            battery_system_fabrication_cost: battery_system_fabrication_cost input
            site_infra_fabrication_cost: site_infra_fabrication_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(solar_array_fabrication_cost, battery_system_fabrication_cost, site_infra_fabrication_cost)

        # Import handwritten implementation
        from solar_battery_v5.handwritten.solarbatterydesign.solar_battery_plant.fabrication_cost_impl import (
            run_fabrication_cost,
        )

        # Execute implementation - returns single value
        fabrication_cost = run_fabrication_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(fabrication_cost))
