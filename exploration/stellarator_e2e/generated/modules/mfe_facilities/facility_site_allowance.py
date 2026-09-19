"""Facility_Site_AllowanceModule Module Wrapper

TEAx module for Facility_Site_Allowance calculation.

*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Retain the identified site-improvement allowance once in an active proposed layout; dormant contribution zero.

Inputs:
    - amount_in: amount_in parameter
    - active_in: active_in parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_facilities.sysml:600

SysML Source: root-0/analyses/mfe_facilities.sysml:600

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_facilities/facility_site_allowance_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Facility_Site_AllowanceInput(BaseModel):
    """Input model for Facility_Site_AllowanceModule.

    Attributes:
        amount_in: amount_in input
        active_in: active_in input
    """
    amount_in: float = Field(..., description="amount_in input")
    active_in: float = Field(..., description="active_in input")


class Facility_Site_AllowanceModule(ModuleBase[Facility_Site_AllowanceInput, Float]):
    """TEAx module for Facility_Site_Allowance calculation.

*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Retain the identified site-improvement allowance once in an active proposed layout; dormant contribution zero.

Inputs:
    - amount_in: amount_in parameter
    - active_in: active_in parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_facilities.sysml:600

    SysML Source: root-0/analyses/mfe_facilities.sysml:600

    Calculation Specification:
        cost = active_in * amount_in
        
Documentation:
*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Retain the identified site-improvement allowance once in an active proposed layout; dormant contribution zero.

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_facilities.facility_site_allowance_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Facility_Site_AllowanceModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, amount_in: float, active_in: float    ) -> Facility_Site_AllowanceInput:
        """Validate inputs and fill defaults.

        Args:
            amount_in: amount_in input
            active_in: active_in input

        Returns:
            Validated input model
        """
        return Facility_Site_AllowanceInput(amount_in=amount_in, active_in=active_in)

    def run(
        self, amount_in: float, active_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            amount_in: amount_in input
            active_in: active_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(amount_in, active_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_facilities.facility_site_allowance_impl import (
            run_facility_site_allowance,
        )

        # Execute implementation - returns single value
        cost = run_facility_site_allowance(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
