"""bop_capitalModule Module Wrapper

TEAx module for bop_capital calculation.

Inputs:
    - turbine_capital_cost: turbine_capital_cost parameter
    - electric_plant_capital_cost: electric_plant_capital_cost parameter
    - heat_rejection_capital_cost: heat_rejection_capital_cost parameter
    - misc_plant_capital_cost: misc_plant_capital_cost parameter

Outputs:
    - bop_capital: bop_capital result

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:429

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:429

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plant/mfe_power_plant/bop_capital_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class bop_capitalInput(BaseModel):
    """Input model for bop_capitalModule.

    Attributes:
        turbine_capital_cost: turbine_capital_cost input
        electric_plant_capital_cost: electric_plant_capital_cost input
        heat_rejection_capital_cost: heat_rejection_capital_cost input
        misc_plant_capital_cost: misc_plant_capital_cost input
    """
    turbine_capital_cost: float = Field(..., description="turbine_capital_cost input")
    electric_plant_capital_cost: float = Field(..., description="electric_plant_capital_cost input")
    heat_rejection_capital_cost: float = Field(..., description="heat_rejection_capital_cost input")
    misc_plant_capital_cost: float = Field(..., description="misc_plant_capital_cost input")


class bop_capitalModule(ModuleBase[bop_capitalInput, Float]):
    """TEAx module for bop_capital calculation.

Inputs:
    - turbine_capital_cost: turbine_capital_cost parameter
    - electric_plant_capital_cost: electric_plant_capital_cost parameter
    - heat_rejection_capital_cost: heat_rejection_capital_cost parameter
    - misc_plant_capital_cost: misc_plant_capital_cost parameter

Outputs:
    - bop_capital: bop_capital result

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:429

    SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:429

    Calculation Specification:

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plant.mfe_power_plant.bop_capital_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "bop_capitalModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, turbine_capital_cost: float, electric_plant_capital_cost: float, heat_rejection_capital_cost: float, misc_plant_capital_cost: float    ) -> bop_capitalInput:
        """Validate inputs and fill defaults.

        Args:
            turbine_capital_cost: turbine_capital_cost input
            electric_plant_capital_cost: electric_plant_capital_cost input
            heat_rejection_capital_cost: heat_rejection_capital_cost input
            misc_plant_capital_cost: misc_plant_capital_cost input

        Returns:
            Validated input model
        """
        return bop_capitalInput(turbine_capital_cost=turbine_capital_cost, electric_plant_capital_cost=electric_plant_capital_cost, heat_rejection_capital_cost=heat_rejection_capital_cost, misc_plant_capital_cost=misc_plant_capital_cost)

    def run(
        self, turbine_capital_cost: float, electric_plant_capital_cost: float, heat_rejection_capital_cost: float, misc_plant_capital_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            turbine_capital_cost: turbine_capital_cost input
            electric_plant_capital_cost: electric_plant_capital_cost input
            heat_rejection_capital_cost: heat_rejection_capital_cost input
            misc_plant_capital_cost: misc_plant_capital_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(turbine_capital_cost, electric_plant_capital_cost, heat_rejection_capital_cost, misc_plant_capital_cost)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plant.mfe_power_plant.bop_capital_impl import (
            run_bop_capital,
        )

        # Execute implementation - returns single value
        bop_capital = run_bop_capital(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(bop_capital))
