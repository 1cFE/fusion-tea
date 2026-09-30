"""Supplied_Purchase_CostModule Module Wrapper

TEAx module for Supplied_Purchase_Cost calculation.

WI-079 evaluates a supplied package purchase estimate, dollars per module.
cost = purchase_cost_in * n_mod_in. Native completion rejects nonfinite,
negative or Boolean amounts and any n_mod_in other than one: account
aggregation beyond the current single-module contract remains unsupported.
The amount and offered specification form one assumed package; demand does
not select either. No price law for hypothetical specification changes.
*Source**: modeling_project/REQUIREMENTS.md
*Reference**: MR-7; work/active/WI-079_supplied-equipment-design-bases-for-residual-costs/design.md
*Basis**: independently reviewed supplied-package evaluation contract
*Last Updated**: 2026-09-20

Inputs:
    - purchase_cost_in: purchase_cost_in parameter
    - n_mod_in: n_mod_in parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:17

SysML Source: root-0/analyses/mfe_account_costs.sysml:17

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/supplied_purchase_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_reference_tea.primitives import Float


class Supplied_Purchase_CostInput(BaseModel):
    """Input model for Supplied_Purchase_CostModule.

    Attributes:
        purchase_cost_in: purchase_cost_in input
        n_mod_in: n_mod_in input
    """
    purchase_cost_in: float = Field(..., description="purchase_cost_in input")
    n_mod_in: float = Field(..., description="n_mod_in input")


class Supplied_Purchase_CostModule(ModuleBase[Supplied_Purchase_CostInput, Float]):
    """TEAx module for Supplied_Purchase_Cost calculation.

WI-079 evaluates a supplied package purchase estimate, dollars per module.
cost = purchase_cost_in * n_mod_in. Native completion rejects nonfinite,
negative or Boolean amounts and any n_mod_in other than one: account
aggregation beyond the current single-module contract remains unsupported.
The amount and offered specification form one assumed package; demand does
not select either. No price law for hypothetical specification changes.
*Source**: modeling_project/REQUIREMENTS.md
*Reference**: MR-7; work/active/WI-079_supplied-equipment-design-bases-for-residual-costs/design.md
*Basis**: independently reviewed supplied-package evaluation contract
*Last Updated**: 2026-09-20

Inputs:
    - purchase_cost_in: purchase_cost_in parameter
    - n_mod_in: n_mod_in parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:17

    SysML Source: root-0/analyses/mfe_account_costs.sysml:17

    Calculation Specification:
        See documentation:
WI-079 evaluates a supplied package purchase estimate, dollars per module.
cost = purchase_cost_in * n_mod_in. Native completion rejects nonfinite,
negative or Boolean amounts and any n_mod_in other than one: account
aggregation beyond the current single-module contract remains unsupported.
The amount and offered specification form one assumed package; demand does
not select either. No price law for hypothetical specification changes.
*Source**: modeling_project/REQUIREMENTS.md
*Reference**: MR-7; work/active/WI-079_supplied-equipment-design-bases-for-residual-costs/design.md
*Basis**: independently reviewed supplied-package evaluation contract
*Last Updated**: 2026-09-20

    IMPLEMENTATION: See stellarator_materials_reference_tea.handwritten.mfe_account_costs.supplied_purchase_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Supplied_Purchase_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, purchase_cost_in: float, n_mod_in: float    ) -> Supplied_Purchase_CostInput:
        """Validate inputs and fill defaults.

        Args:
            purchase_cost_in: purchase_cost_in input
            n_mod_in: n_mod_in input

        Returns:
            Validated input model
        """
        return Supplied_Purchase_CostInput(purchase_cost_in=purchase_cost_in, n_mod_in=n_mod_in)

    def run(
        self, purchase_cost_in: float, n_mod_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            purchase_cost_in: purchase_cost_in input
            n_mod_in: n_mod_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(purchase_cost_in, n_mod_in)

        # Import handwritten implementation
        from stellarator_materials_reference_tea.handwritten.mfe_account_costs.supplied_purchase_cost_impl import (
            run_supplied_purchase_cost,
        )

        # Execute implementation - returns single value
        cost = run_supplied_purchase_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
