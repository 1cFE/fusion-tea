"""installation_costModule Module Wrapper

TEAx module for installation_cost calculation.

Inputs:
    - racking_installation_cost: racking_installation_cost parameter
    - electrical_panel_installation_cost: electrical_panel_installation_cost parameter
    - permitting_installation_cost: permitting_installation_cost parameter

Outputs:
    - installation_cost: installation_cost result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterydesign/solar_battery_plant/site_infra/installation_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_v5.primitives import Float


class installation_costInput(BaseModel):
    """Input model for installation_costModule.

    Attributes:
        racking_installation_cost: racking_installation_cost input
        electrical_panel_installation_cost: electrical_panel_installation_cost input
        permitting_installation_cost: permitting_installation_cost input
    """
    racking_installation_cost: float = Field(..., description="racking_installation_cost input")
    electrical_panel_installation_cost: float = Field(..., description="electrical_panel_installation_cost input")
    permitting_installation_cost: float = Field(..., description="permitting_installation_cost input")


class installation_costModule(ModuleBase[installation_costInput, Float]):
    """TEAx module for installation_cost calculation.

Inputs:
    - racking_installation_cost: racking_installation_cost parameter
    - electrical_panel_installation_cost: electrical_panel_installation_cost parameter
    - permitting_installation_cost: permitting_installation_cost parameter

Outputs:
    - installation_cost: installation_cost result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        racking.installation_cost + electrical_panel.installation_cost + permitting.installation_cost

    IMPLEMENTATION: See solar_battery_v5.handwritten.solarbatterydesign.solar_battery_plant.site_infra.installation_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "installation_costModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, racking_installation_cost: float, electrical_panel_installation_cost: float, permitting_installation_cost: float    ) -> installation_costInput:
        """Validate inputs and fill defaults.

        Args:
            racking_installation_cost: racking_installation_cost input
            electrical_panel_installation_cost: electrical_panel_installation_cost input
            permitting_installation_cost: permitting_installation_cost input

        Returns:
            Validated input model
        """
        return installation_costInput(racking_installation_cost=racking_installation_cost, electrical_panel_installation_cost=electrical_panel_installation_cost, permitting_installation_cost=permitting_installation_cost)

    def run(
        self, racking_installation_cost: float, electrical_panel_installation_cost: float, permitting_installation_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            racking_installation_cost: racking_installation_cost input
            electrical_panel_installation_cost: electrical_panel_installation_cost input
            permitting_installation_cost: permitting_installation_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(racking_installation_cost, electrical_panel_installation_cost, permitting_installation_cost)

        # Import handwritten implementation
        from solar_battery_v5.handwritten.solarbatterydesign.solar_battery_plant.site_infra.installation_cost_impl import (
            run_installation_cost,
        )

        # Execute implementation - returns single value
        installation_cost = run_installation_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(installation_cost))
