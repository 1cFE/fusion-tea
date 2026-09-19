"""Facility_Shipping_AmountModule Module Wrapper

TEAx module for Facility_Shipping_Amount calculation.

*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Exclude the entire contingency-loaded installed facility contribution from freight, without altering tax or insurance.

Inputs:
    - installed_in: installed_in parameter
    - contingency_in: contingency_in parameter
    - mode_in: mode_in parameter

Outputs:
    - exclusion: exclusion result

SysML Source: root-0/analyses/mfe_facilities.sysml:614

SysML Source: root-0/analyses/mfe_facilities.sysml:614

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_facilities/facility_shipping_amount_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Facility_Shipping_AmountInput(BaseModel):
    """Input model for Facility_Shipping_AmountModule.

    Attributes:
        installed_in: installed_in input
        contingency_in: contingency_in input
        mode_in: mode_in input
    """
    installed_in: float = Field(..., description="installed_in input")
    contingency_in: float = Field(..., description="contingency_in input")
    mode_in: float = Field(..., description="mode_in input")


class Facility_Shipping_AmountModule(ModuleBase[Facility_Shipping_AmountInput, Float]):
    """TEAx module for Facility_Shipping_Amount calculation.

*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Exclude the entire contingency-loaded installed facility contribution from freight, without altering tax or insurance.

Inputs:
    - installed_in: installed_in parameter
    - contingency_in: contingency_in parameter
    - mode_in: mode_in parameter

Outputs:
    - exclusion: exclusion result

SysML Source: root-0/analyses/mfe_facilities.sysml:614

    SysML Source: root-0/analyses/mfe_facilities.sysml:614

    Calculation Specification:
        exclusion = mode_in * (1.0 + contingency_in) * installed_in
        
Documentation:
*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Exclude the entire contingency-loaded installed facility contribution from freight, without altering tax or insurance.

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_facilities.facility_shipping_amount_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Facility_Shipping_AmountModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, installed_in: float, contingency_in: float, mode_in: float    ) -> Facility_Shipping_AmountInput:
        """Validate inputs and fill defaults.

        Args:
            installed_in: installed_in input
            contingency_in: contingency_in input
            mode_in: mode_in input

        Returns:
            Validated input model
        """
        return Facility_Shipping_AmountInput(installed_in=installed_in, contingency_in=contingency_in, mode_in=mode_in)

    def run(
        self, installed_in: float, contingency_in: float, mode_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            installed_in: installed_in input
            contingency_in: contingency_in input
            mode_in: mode_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(installed_in, contingency_in, mode_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_facilities.facility_shipping_amount_impl import (
            run_facility_shipping_amount,
        )

        # Execute implementation - returns single value
        exclusion = run_facility_shipping_amount(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(exclusion))
