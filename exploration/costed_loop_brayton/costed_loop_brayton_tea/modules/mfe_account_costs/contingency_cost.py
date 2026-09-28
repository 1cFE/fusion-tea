"""Contingency_CostModule Module Wrapper

TEAx module for Contingency_Cost calculation.

CAS29 contingency on direct costs:

  cost = contingency_rate * direct_subtotal

`contingency_rate` is the FOAK/NOAK rate (0.10 FOAK, 0.0 NOAK in the
source) -- a concept/maturity input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:220 (cas29_contingency)
*Basis**: Fractional contingency on the direct-cost subtotal

Inputs:
    - contingency_rate_in: contingency_rate_in parameter
    - direct_subtotal: direct_subtotal parameter

Outputs:
    - cost: cost result

SysML Source: root-0/mfe_account_costs.sysml:311

SysML Source: root-0/mfe_account_costs.sysml:311

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/contingency_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from costed_loop_brayton_tea.primitives import Float


class Contingency_CostInput(BaseModel):
    """Input model for Contingency_CostModule.

    Attributes:
        contingency_rate_in: contingency_rate_in input
        direct_subtotal: direct_subtotal input
    """
    contingency_rate_in: float = Field(..., description="contingency_rate_in input")
    direct_subtotal: float = Field(..., description="direct_subtotal input")


class Contingency_CostModule(ModuleBase[Contingency_CostInput, Float]):
    """TEAx module for Contingency_Cost calculation.

CAS29 contingency on direct costs:

  cost = contingency_rate * direct_subtotal

`contingency_rate` is the FOAK/NOAK rate (0.10 FOAK, 0.0 NOAK in the
source) -- a concept/maturity input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:220 (cas29_contingency)
*Basis**: Fractional contingency on the direct-cost subtotal

Inputs:
    - contingency_rate_in: contingency_rate_in parameter
    - direct_subtotal: direct_subtotal parameter

Outputs:
    - cost: cost result

SysML Source: root-0/mfe_account_costs.sysml:311

    SysML Source: root-0/mfe_account_costs.sysml:311

    Calculation Specification:
        cost = contingency_rate_in * direct_subtotal
        
Documentation:
CAS29 contingency on direct costs:

  cost = contingency_rate * direct_subtotal

`contingency_rate` is the FOAK/NOAK rate (0.10 FOAK, 0.0 NOAK in the
source) -- a concept/maturity input (WI-011).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:220 (cas29_contingency)
*Basis**: Fractional contingency on the direct-cost subtotal

    IMPLEMENTATION: See costed_loop_brayton_tea.handwritten.mfe_account_costs.contingency_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Contingency_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, contingency_rate_in: float, direct_subtotal: float    ) -> Contingency_CostInput:
        """Validate inputs and fill defaults.

        Args:
            contingency_rate_in: contingency_rate_in input
            direct_subtotal: direct_subtotal input

        Returns:
            Validated input model
        """
        return Contingency_CostInput(contingency_rate_in=contingency_rate_in, direct_subtotal=direct_subtotal)

    def run(
        self, contingency_rate_in: float, direct_subtotal: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            contingency_rate_in: contingency_rate_in input
            direct_subtotal: direct_subtotal input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(contingency_rate_in, direct_subtotal)

        # Import handwritten implementation
        from costed_loop_brayton_tea.handwritten.mfe_account_costs.contingency_cost_impl import (
            run_contingency_cost,
        )

        # Execute implementation - returns single value
        cost = run_contingency_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
