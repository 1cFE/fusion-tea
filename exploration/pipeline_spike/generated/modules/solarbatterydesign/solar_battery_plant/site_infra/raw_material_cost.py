"""raw_material_costModule Module Wrapper

TEAx module for raw_material_cost calculation.

Inputs:
    - racking_raw_material_cost: racking_raw_material_cost parameter
    - electrical_panel_raw_material_cost: electrical_panel_raw_material_cost parameter
    - permitting_raw_material_cost: permitting_raw_material_cost parameter

Outputs:
    - raw_material_cost: raw_material_cost result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterydesign/solar_battery_plant/site_infra/raw_material_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_tea.primitives import Float


class raw_material_costInput(BaseModel):
    """Input model for raw_material_costModule.

    Attributes:
        racking_raw_material_cost: racking_raw_material_cost input
        electrical_panel_raw_material_cost: electrical_panel_raw_material_cost input
        permitting_raw_material_cost: permitting_raw_material_cost input
    """
    racking_raw_material_cost: float = Field(..., description="racking_raw_material_cost input")
    electrical_panel_raw_material_cost: float = Field(..., description="electrical_panel_raw_material_cost input")
    permitting_raw_material_cost: float = Field(..., description="permitting_raw_material_cost input")


class raw_material_costModule(ModuleBase[raw_material_costInput, Float]):
    """TEAx module for raw_material_cost calculation.

Inputs:
    - racking_raw_material_cost: racking_raw_material_cost parameter
    - electrical_panel_raw_material_cost: electrical_panel_raw_material_cost parameter
    - permitting_raw_material_cost: permitting_raw_material_cost parameter

Outputs:
    - raw_material_cost: raw_material_cost result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        racking.raw_material_cost + electrical_panel.raw_material_cost + permitting.raw_material_cost

    IMPLEMENTATION: See solar_battery_tea.handwritten.solarbatterydesign.solar_battery_plant.site_infra.raw_material_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "raw_material_costModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, racking_raw_material_cost: float, electrical_panel_raw_material_cost: float, permitting_raw_material_cost: float    ) -> raw_material_costInput:
        """Validate inputs and fill defaults.

        Args:
            racking_raw_material_cost: racking_raw_material_cost input
            electrical_panel_raw_material_cost: electrical_panel_raw_material_cost input
            permitting_raw_material_cost: permitting_raw_material_cost input

        Returns:
            Validated input model
        """
        return raw_material_costInput(racking_raw_material_cost=racking_raw_material_cost, electrical_panel_raw_material_cost=electrical_panel_raw_material_cost, permitting_raw_material_cost=permitting_raw_material_cost)

    def run(
        self, racking_raw_material_cost: float, electrical_panel_raw_material_cost: float, permitting_raw_material_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            racking_raw_material_cost: racking_raw_material_cost input
            electrical_panel_raw_material_cost: electrical_panel_raw_material_cost input
            permitting_raw_material_cost: permitting_raw_material_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(racking_raw_material_cost, electrical_panel_raw_material_cost, permitting_raw_material_cost)

        # Import handwritten implementation
        from solar_battery_tea.handwritten.solarbatterydesign.solar_battery_plant.site_infra.raw_material_cost_impl import (
            run_raw_material_cost,
        )

        # Execute implementation - returns single value
        raw_material_cost = run_raw_material_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(raw_material_cost))
