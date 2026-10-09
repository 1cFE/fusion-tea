"""Facility_Land_CostModule Module Wrapper

TEAx module for Facility_Land_Cost calculation.

*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Convert the computed parcel area in m^2 to acres at the explicit inherited land rate.

Inputs:
    - parcel_area_in: parcel_area_in parameter
    - rate_per_acre_in: rate_per_acre_in parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_facilities.sysml:757

SysML Source: root-0/analyses/mfe_facilities.sysml:757

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_facilities/facility_land_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_reference_tea.primitives import Float


class Facility_Land_CostInput(BaseModel):
    """Input model for Facility_Land_CostModule.

    Attributes:
        parcel_area_in: parcel_area_in input
        rate_per_acre_in: rate_per_acre_in input
    """
    parcel_area_in: float = Field(..., description="parcel_area_in input")
    rate_per_acre_in: float = Field(..., description="rate_per_acre_in input")


class Facility_Land_CostModule(ModuleBase[Facility_Land_CostInput, Float]):
    """TEAx module for Facility_Land_Cost calculation.

*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Convert the computed parcel area in m^2 to acres at the explicit inherited land rate.

Inputs:
    - parcel_area_in: parcel_area_in parameter
    - rate_per_acre_in: rate_per_acre_in parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_facilities.sysml:757

    SysML Source: root-0/analyses/mfe_facilities.sysml:757

    Calculation Specification:
        cost = parcel_area_in / 4046.8564224 * rate_per_acre_in
        
Documentation:
*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Convert the computed parcel area in m^2 to acres at the explicit inherited land rate.

    IMPLEMENTATION: See stellarator_materials_reference_tea.handwritten.mfe_facilities.facility_land_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Facility_Land_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, parcel_area_in: float, rate_per_acre_in: float    ) -> Facility_Land_CostInput:
        """Validate inputs and fill defaults.

        Args:
            parcel_area_in: parcel_area_in input
            rate_per_acre_in: rate_per_acre_in input

        Returns:
            Validated input model
        """
        return Facility_Land_CostInput(parcel_area_in=parcel_area_in, rate_per_acre_in=rate_per_acre_in)

    def run(
        self, parcel_area_in: float, rate_per_acre_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            parcel_area_in: parcel_area_in input
            rate_per_acre_in: rate_per_acre_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(parcel_area_in, rate_per_acre_in)

        # Import handwritten implementation
        from stellarator_materials_reference_tea.handwritten.mfe_facilities.facility_land_cost_impl import (
            run_facility_land_cost,
        )

        # Execute implementation - returns single value
        cost = run_facility_land_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
