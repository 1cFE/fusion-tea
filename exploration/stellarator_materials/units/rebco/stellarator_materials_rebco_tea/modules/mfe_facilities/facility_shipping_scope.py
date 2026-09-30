"""Facility_Shipping_ScopeModule Module Wrapper

TEAx module for Facility_Shipping_Scope calculation.

Source: work/active/WI-068_layout-based-facilities/design.md; layout-capacity-design.md; evidence/facility-contract.md. Ref: released geometry, capacity, exact civil takeoff and account boundary. Basis: conditional conceptual scenario; unqualified shielding/loading/transport and explicit provisional equipment envelopes. Reject negative/nonfinite exclusions or sum exceedingCAS20, never clamp.

Inputs:
    - contingency_in: contingency_in parameter
    - facility_exclusion_in: facility_exclusion_in parameter
    - cooling_exclusion_in: cooling_exclusion_in parameter
    - cas20_in: cas20_in parameter
    - fuel_installation_in: fuel_installation_in parameter

Outputs:
    - facility_exclusion: facility_exclusion result
    - cooling_exclusion: cooling_exclusion result
    - fuel_installation_exclusion: fuel_installation_exclusion result
    - remaining_shipping_base: remaining_shipping_base result

SysML Source: root-0/analyses/mfe_facilities.sysml:690

SysML Source: root-0/analyses/mfe_facilities.sysml:690

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_facilities/facility_shipping_scope_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.primitives import Float
from stellarator_materials_rebco_tea.schemas.facility_shipping_scope_output import Facility_Shipping_ScopeOutput


class Facility_Shipping_ScopeInput(BaseModel):
    """Input model for Facility_Shipping_ScopeModule.

    Attributes:
        contingency_in: contingency_in input
        facility_exclusion_in: facility_exclusion_in input
        cooling_exclusion_in: cooling_exclusion_in input
        cas20_in: cas20_in input
        fuel_installation_in: fuel_installation_in input
    """
    contingency_in: float = Field(..., description="contingency_in input")
    facility_exclusion_in: float = Field(..., description="facility_exclusion_in input")
    cooling_exclusion_in: float = Field(..., description="cooling_exclusion_in input")
    cas20_in: float = Field(..., description="cas20_in input")
    fuel_installation_in: float = Field(..., description="fuel_installation_in input")


class Facility_Shipping_ScopeModule(ModuleBase[Facility_Shipping_ScopeInput, Facility_Shipping_ScopeOutput]):
    """TEAx module for Facility_Shipping_Scope calculation.

Source: work/active/WI-068_layout-based-facilities/design.md; layout-capacity-design.md; evidence/facility-contract.md. Ref: released geometry, capacity, exact civil takeoff and account boundary. Basis: conditional conceptual scenario; unqualified shielding/loading/transport and explicit provisional equipment envelopes. Reject negative/nonfinite exclusions or sum exceedingCAS20, never clamp.

Inputs:
    - contingency_in: contingency_in parameter
    - facility_exclusion_in: facility_exclusion_in parameter
    - cooling_exclusion_in: cooling_exclusion_in parameter
    - cas20_in: cas20_in parameter
    - fuel_installation_in: fuel_installation_in parameter

Outputs:
    - facility_exclusion: facility_exclusion result
    - cooling_exclusion: cooling_exclusion result
    - fuel_installation_exclusion: fuel_installation_exclusion result
    - remaining_shipping_base: remaining_shipping_base result

SysML Source: root-0/analyses/mfe_facilities.sysml:690

    SysML Source: root-0/analyses/mfe_facilities.sysml:690

    Calculation Specification:
        fuel_installation_in = 0.0
        contingency_in = 0.0
        
Documentation:
Source: work/active/WI-068_layout-based-facilities/design.md; layout-capacity-design.md; evidence/facility-contract.md. Ref: released geometry, capacity, exact civil takeoff and account boundary. Basis: conditional conceptual scenario; unqualified shielding/loading/transport and explicit provisional equipment envelopes. Reject negative/nonfinite exclusions or sum exceedingCAS20, never clamp.

    IMPLEMENTATION: See stellarator_materials_rebco_tea.handwritten.mfe_facilities.facility_shipping_scope_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts facility_exclusion, cooling_exclusion, fuel_installation_exclusion, remaining_shipping_base fields to separate channels.
    """

    name: str = "Facility_Shipping_ScopeModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, contingency_in: float, facility_exclusion_in: float, cooling_exclusion_in: float, cas20_in: float, fuel_installation_in: float    ) -> Facility_Shipping_ScopeInput:
        """Validate inputs and fill defaults.

        Args:
            contingency_in: contingency_in input
            facility_exclusion_in: facility_exclusion_in input
            cooling_exclusion_in: cooling_exclusion_in input
            cas20_in: cas20_in input
            fuel_installation_in: fuel_installation_in input

        Returns:
            Validated input model
        """
        return Facility_Shipping_ScopeInput(contingency_in=contingency_in, facility_exclusion_in=facility_exclusion_in, cooling_exclusion_in=cooling_exclusion_in, cas20_in=cas20_in, fuel_installation_in=fuel_installation_in)

    def run(
        self, contingency_in: float, facility_exclusion_in: float, cooling_exclusion_in: float, cas20_in: float, fuel_installation_in: float    ) -> ModuleResult[Facility_Shipping_ScopeOutput]:
        """Execute calculation.

        Args:
            contingency_in: contingency_in input
            facility_exclusion_in: facility_exclusion_in input
            cooling_exclusion_in: cooling_exclusion_in input
            cas20_in: cas20_in input
            fuel_installation_in: fuel_installation_in input

        Returns:
            Module result with Facility_Shipping_ScopeOutput (facility_exclusion, cooling_exclusion, fuel_installation_exclusion, remaining_shipping_base)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(contingency_in, facility_exclusion_in, cooling_exclusion_in, cas20_in, fuel_installation_in)

        # Import handwritten implementation
        from stellarator_materials_rebco_tea.handwritten.mfe_facilities.facility_shipping_scope_impl import (
            run_facility_shipping_scope,
        )

        # Execute implementation - returns tuple of values
        facility_exclusion, cooling_exclusion, fuel_installation_exclusion, remaining_shipping_base = run_facility_shipping_scope(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Facility_Shipping_ScopeOutput(
                facility_exclusion=facility_exclusion,
                cooling_exclusion=cooling_exclusion,
                fuel_installation_exclusion=fuel_installation_exclusion,
                remaining_shipping_base=remaining_shipping_base,
            )
        )
