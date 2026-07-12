"""raw_material_costModule Module Wrapper

TEAx module for raw_material_cost calculation.

Inputs:
    - solar_array_raw_material_cost: solar_array_raw_material_cost parameter
    - battery_system_raw_material_cost: battery_system_raw_material_cost parameter
    - site_infra_raw_material_cost: site_infra_raw_material_cost parameter

Outputs:
    - raw_material_cost: raw_material_cost result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterydesign/solar_battery_plant/raw_material_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_tea.primitives import Float


class raw_material_costInput(BaseModel):
    """Input model for raw_material_costModule.

    Attributes:
        solar_array_raw_material_cost: solar_array_raw_material_cost input
        battery_system_raw_material_cost: battery_system_raw_material_cost input
        site_infra_raw_material_cost: site_infra_raw_material_cost input
    """
    solar_array_raw_material_cost: float = Field(..., description="solar_array_raw_material_cost input")
    battery_system_raw_material_cost: float = Field(..., description="battery_system_raw_material_cost input")
    site_infra_raw_material_cost: float = Field(..., description="site_infra_raw_material_cost input")


class raw_material_costModule(ModuleBase[raw_material_costInput, Float]):
    """TEAx module for raw_material_cost calculation.

Inputs:
    - solar_array_raw_material_cost: solar_array_raw_material_cost parameter
    - battery_system_raw_material_cost: battery_system_raw_material_cost parameter
    - site_infra_raw_material_cost: site_infra_raw_material_cost parameter

Outputs:
    - raw_material_cost: raw_material_cost result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        solar_array.raw_material_cost + battery_system.raw_material_cost + site_infra.raw_material_cost

    IMPLEMENTATION: See solar_battery_tea.handwritten.solarbatterydesign.solar_battery_plant.raw_material_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "raw_material_costModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, solar_array_raw_material_cost: float, battery_system_raw_material_cost: float, site_infra_raw_material_cost: float    ) -> raw_material_costInput:
        """Validate inputs and fill defaults.

        Args:
            solar_array_raw_material_cost: solar_array_raw_material_cost input
            battery_system_raw_material_cost: battery_system_raw_material_cost input
            site_infra_raw_material_cost: site_infra_raw_material_cost input

        Returns:
            Validated input model
        """
        return raw_material_costInput(solar_array_raw_material_cost=solar_array_raw_material_cost, battery_system_raw_material_cost=battery_system_raw_material_cost, site_infra_raw_material_cost=site_infra_raw_material_cost)

    def run(
        self, solar_array_raw_material_cost: float, battery_system_raw_material_cost: float, site_infra_raw_material_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            solar_array_raw_material_cost: solar_array_raw_material_cost input
            battery_system_raw_material_cost: battery_system_raw_material_cost input
            site_infra_raw_material_cost: site_infra_raw_material_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(solar_array_raw_material_cost, battery_system_raw_material_cost, site_infra_raw_material_cost)

        # Import handwritten implementation
        from solar_battery_tea.handwritten.solarbatterydesign.solar_battery_plant.raw_material_cost_impl import (
            run_raw_material_cost,
        )

        # Execute implementation - returns single value
        raw_material_cost = run_raw_material_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(raw_material_cost))
