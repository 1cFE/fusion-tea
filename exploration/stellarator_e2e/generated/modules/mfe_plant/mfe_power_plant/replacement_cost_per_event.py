"""replacement_cost_per_eventModule Module Wrapper

TEAx module for replacement_cost_per_event calculation.

Inputs:
    - blanket_capital_cost: blanket_capital_cost parameter
    - divertor_capital_cost: divertor_capital_cost parameter
    - n_mod: n_mod parameter

Outputs:
    - replacement_cost_per_event: replacement_cost_per_event result

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:817

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:817

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plant/mfe_power_plant/replacement_cost_per_event_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class replacement_cost_per_eventInput(BaseModel):
    """Input model for replacement_cost_per_eventModule.

    Attributes:
        blanket_capital_cost: blanket_capital_cost input
        divertor_capital_cost: divertor_capital_cost input
        n_mod: n_mod input
    """
    blanket_capital_cost: float = Field(..., description="blanket_capital_cost input")
    divertor_capital_cost: float = Field(..., description="divertor_capital_cost input")
    n_mod: float = Field(..., description="n_mod input")


class replacement_cost_per_eventModule(ModuleBase[replacement_cost_per_eventInput, Float]):
    """TEAx module for replacement_cost_per_event calculation.

Inputs:
    - blanket_capital_cost: blanket_capital_cost parameter
    - divertor_capital_cost: divertor_capital_cost parameter
    - n_mod: n_mod parameter

Outputs:
    - replacement_cost_per_event: replacement_cost_per_event result

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:817

    SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:817

    Calculation Specification:

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plant.mfe_power_plant.replacement_cost_per_event_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "replacement_cost_per_eventModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, blanket_capital_cost: float, divertor_capital_cost: float, n_mod: float    ) -> replacement_cost_per_eventInput:
        """Validate inputs and fill defaults.

        Args:
            blanket_capital_cost: blanket_capital_cost input
            divertor_capital_cost: divertor_capital_cost input
            n_mod: n_mod input

        Returns:
            Validated input model
        """
        return replacement_cost_per_eventInput(blanket_capital_cost=blanket_capital_cost, divertor_capital_cost=divertor_capital_cost, n_mod=n_mod)

    def run(
        self, blanket_capital_cost: float, divertor_capital_cost: float, n_mod: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            blanket_capital_cost: blanket_capital_cost input
            divertor_capital_cost: divertor_capital_cost input
            n_mod: n_mod input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(blanket_capital_cost, divertor_capital_cost, n_mod)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plant.mfe_power_plant.replacement_cost_per_event_impl import (
            run_replacement_cost_per_event,
        )

        # Execute implementation - returns single value
        replacement_cost_per_event = run_replacement_cost_per_event(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(replacement_cost_per_event))
