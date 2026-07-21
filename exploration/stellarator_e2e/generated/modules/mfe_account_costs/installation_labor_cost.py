"""Installation_Labor_CostModule Module Wrapper

TEAx module for Installation_Labor_Cost calculation.

Installation-labor account:

  cost = installation_frac * reactor_subtotal

reactor_subtotal = Σ(C220101..C220110) per-module (includes C220109 = 0
for this concept, excludes 111/112). The multi-unit labor factor (0.92)
is a plant-aggregate concern at n_mod > 1; the account value compared
under A-2 is single-module.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:652-664 (c220111); installation_frac cas22.py:664 (0.14)
*Basis**: Fixed fraction of the reactor-equipment subtotal

Inputs:
    - installation_frac: installation_frac parameter
    - reactor_subtotal: reactor_subtotal parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:479

SysML Source: root-0/analyses/mfe_account_costs.sysml:479

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/installation_labor_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Installation_Labor_CostInput(BaseModel):
    """Input model for Installation_Labor_CostModule.

    Attributes:
        installation_frac: installation_frac input
        reactor_subtotal: reactor_subtotal input
    """
    installation_frac: float = Field(..., description="installation_frac input")
    reactor_subtotal: float = Field(..., description="reactor_subtotal input")


class Installation_Labor_CostModule(ModuleBase[Installation_Labor_CostInput, Float]):
    """TEAx module for Installation_Labor_Cost calculation.

Installation-labor account:

  cost = installation_frac * reactor_subtotal

reactor_subtotal = Σ(C220101..C220110) per-module (includes C220109 = 0
for this concept, excludes 111/112). The multi-unit labor factor (0.92)
is a plant-aggregate concern at n_mod > 1; the account value compared
under A-2 is single-module.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:652-664 (c220111); installation_frac cas22.py:664 (0.14)
*Basis**: Fixed fraction of the reactor-equipment subtotal

Inputs:
    - installation_frac: installation_frac parameter
    - reactor_subtotal: reactor_subtotal parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:479

    SysML Source: root-0/analyses/mfe_account_costs.sysml:479

    Calculation Specification:
        installation_frac = 0.14
        cost = installation_frac * reactor_subtotal
        
Documentation:
Installation-labor account:

  cost = installation_frac * reactor_subtotal

reactor_subtotal = Σ(C220101..C220110) per-module (includes C220109 = 0
for this concept, excludes 111/112). The multi-unit labor factor (0.92)
is a plant-aggregate concern at n_mod > 1; the account value compared
under A-2 is single-module.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:652-664 (c220111); installation_frac cas22.py:664 (0.14)
*Basis**: Fixed fraction of the reactor-equipment subtotal

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.installation_labor_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Installation_Labor_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, installation_frac: float, reactor_subtotal: float    ) -> Installation_Labor_CostInput:
        """Validate inputs and fill defaults.

        Args:
            installation_frac: installation_frac input
            reactor_subtotal: reactor_subtotal input

        Returns:
            Validated input model
        """
        return Installation_Labor_CostInput(installation_frac=installation_frac, reactor_subtotal=reactor_subtotal)

    def run(
        self, installation_frac: float, reactor_subtotal: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            installation_frac: installation_frac input
            reactor_subtotal: reactor_subtotal input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(installation_frac, reactor_subtotal)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.installation_labor_cost_impl import (
            run_installation_labor_cost,
        )

        # Execute implementation - returns single value
        cost = run_installation_labor_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
