"""capital_costModule Module Wrapper

TEAx module for capital_cost calculation.

Inputs:
    - racking_capital_cost: racking_capital_cost parameter
    - electrical_panel_capital_cost: electrical_panel_capital_cost parameter
    - permitting_capital_cost: permitting_capital_cost parameter

Outputs:
    - capital_cost: capital_cost result

SysML Source: unknown:0

SysML Source: unknown:0

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterydesign/solar_battery_plant/site_infra/capital_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_tea.primitives import Float


class capital_costInput(BaseModel):
    """Input model for capital_costModule.

    Attributes:
        racking_capital_cost: racking_capital_cost input
        electrical_panel_capital_cost: electrical_panel_capital_cost input
        permitting_capital_cost: permitting_capital_cost input
    """
    racking_capital_cost: float = Field(..., description="racking_capital_cost input")
    electrical_panel_capital_cost: float = Field(..., description="electrical_panel_capital_cost input")
    permitting_capital_cost: float = Field(..., description="permitting_capital_cost input")


class capital_costModule(ModuleBase[capital_costInput, Float]):
    """TEAx module for capital_cost calculation.

Inputs:
    - racking_capital_cost: racking_capital_cost parameter
    - electrical_panel_capital_cost: electrical_panel_capital_cost parameter
    - permitting_capital_cost: permitting_capital_cost parameter

Outputs:
    - capital_cost: capital_cost result

SysML Source: unknown:0

    SysML Source: unknown:0

    Calculation Specification:
        racking.capital_cost + electrical_panel.capital_cost + permitting.capital_cost

    IMPLEMENTATION: See solar_battery_tea.handwritten.solarbatterydesign.solar_battery_plant.site_infra.capital_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "capital_costModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, racking_capital_cost: float, electrical_panel_capital_cost: float, permitting_capital_cost: float    ) -> capital_costInput:
        """Validate inputs and fill defaults.

        Args:
            racking_capital_cost: racking_capital_cost input
            electrical_panel_capital_cost: electrical_panel_capital_cost input
            permitting_capital_cost: permitting_capital_cost input

        Returns:
            Validated input model
        """
        return capital_costInput(racking_capital_cost=racking_capital_cost, electrical_panel_capital_cost=electrical_panel_capital_cost, permitting_capital_cost=permitting_capital_cost)

    def run(
        self, racking_capital_cost: float, electrical_panel_capital_cost: float, permitting_capital_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            racking_capital_cost: racking_capital_cost input
            electrical_panel_capital_cost: electrical_panel_capital_cost input
            permitting_capital_cost: permitting_capital_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(racking_capital_cost, electrical_panel_capital_cost, permitting_capital_cost)

        # Import handwritten implementation
        from solar_battery_tea.handwritten.solarbatterydesign.solar_battery_plant.site_infra.capital_cost_impl import (
            run_capital_cost,
        )

        # Execute implementation - returns single value
        capital_cost = run_capital_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(capital_cost))
