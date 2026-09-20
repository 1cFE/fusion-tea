"""Auto-generated implementation for Facility_Land_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_facilities.sysml:757

SysML Expressions:
    cost = parcel_area_in / 4046.8564224 * rate_per_acre_in
    
Documentation:
*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Convert the computed parcel area in m^2 to acres at the explicit inherited land rate.
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_facilities.facility_land_cost import Facility_Land_CostInput


def run_facility_land_cost(inputs: Facility_Land_CostInput) -> float:
    """Execute Facility_Land_Cost calculation.

*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Convert the computed parcel area in m^2 to acres at the explicit inherited land rate.

SysML Source: root-0/analyses/mfe_facilities.sysml:757

SysML Expressions:
    cost = parcel_area_in / 4046.8564224 * rate_per_acre_in
    
Documentation:
*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Convert the computed parcel area in m^2 to acres at the explicit inherited land rate.

Args:
    inputs: Input parameters validated against Facility_Land_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Facility_Land_CostInput(...)
    >>> result = run_facility_land_cost(inputs)
    """
    return ((inputs.parcel_area_in / 4046.8564224) * inputs.rate_per_acre_in)
