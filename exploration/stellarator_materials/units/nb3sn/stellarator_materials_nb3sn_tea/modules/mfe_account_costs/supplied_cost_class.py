"""Supplied_Cost_ClassModule Module Wrapper

TEAx module for Supplied_Cost_Class calculation.

Guarded identity for a selected procurement class. Native completion
rejects nonfinite, Boolean or negative quantities. The value is chosen,
not computed from operating demand and not a qualified physical capacity.
Its MW thermal/fusion or MWe interpretation belongs to the owning account.
*Source**: modeling_project/REQUIREMENTS.md
*Reference**: MR-7; work/active/WI-079_supplied-equipment-design-bases-for-residual-costs/design.md
*Basis**: model-owned selected-input domain, preserving the supplied value
*Last Updated**: 2026-09-20

Inputs:
    - class_in: class_in parameter

Outputs:
    - value: value result

SysML Source: root-0/analyses/mfe_account_costs.sysml:4

SysML Source: root-0/analyses/mfe_account_costs.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/supplied_cost_class_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float


class Supplied_Cost_ClassInput(BaseModel):
    """Input model for Supplied_Cost_ClassModule.

    Attributes:
        class_in: class_in input
    """
    class_in: float = Field(..., description="class_in input")


class Supplied_Cost_ClassModule(ModuleBase[Supplied_Cost_ClassInput, Float]):
    """TEAx module for Supplied_Cost_Class calculation.

Guarded identity for a selected procurement class. Native completion
rejects nonfinite, Boolean or negative quantities. The value is chosen,
not computed from operating demand and not a qualified physical capacity.
Its MW thermal/fusion or MWe interpretation belongs to the owning account.
*Source**: modeling_project/REQUIREMENTS.md
*Reference**: MR-7; work/active/WI-079_supplied-equipment-design-bases-for-residual-costs/design.md
*Basis**: model-owned selected-input domain, preserving the supplied value
*Last Updated**: 2026-09-20

Inputs:
    - class_in: class_in parameter

Outputs:
    - value: value result

SysML Source: root-0/analyses/mfe_account_costs.sysml:4

    SysML Source: root-0/analyses/mfe_account_costs.sysml:4

    Calculation Specification:
        See documentation:
Guarded identity for a selected procurement class. Native completion
rejects nonfinite, Boolean or negative quantities. The value is chosen,
not computed from operating demand and not a qualified physical capacity.
Its MW thermal/fusion or MWe interpretation belongs to the owning account.
*Source**: modeling_project/REQUIREMENTS.md
*Reference**: MR-7; work/active/WI-079_supplied-equipment-design-bases-for-residual-costs/design.md
*Basis**: model-owned selected-input domain, preserving the supplied value
*Last Updated**: 2026-09-20

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.mfe_account_costs.supplied_cost_class_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Supplied_Cost_ClassModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, class_in: float    ) -> Supplied_Cost_ClassInput:
        """Validate inputs and fill defaults.

        Args:
            class_in: class_in input

        Returns:
            Validated input model
        """
        return Supplied_Cost_ClassInput(class_in=class_in)

    def run(
        self, class_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            class_in: class_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(class_in)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.mfe_account_costs.supplied_cost_class_impl import (
            run_supplied_cost_class,
        )

        # Execute implementation - returns single value
        value = run_supplied_cost_class(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(value))
