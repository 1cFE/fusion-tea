"""Auto-generated implementation for Facility_Site_Allowance.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_facilities.sysml:763

SysML Expressions:
    cost = active_in * amount_in
    
Documentation:
*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Retain the identified site-improvement allowance once in an active proposed layout; dormant contribution zero.
"""

AUTO_IMPLEMENTED = True

from stellarator_materials_reference_tea.modules.mfe_facilities.facility_site_allowance import Facility_Site_AllowanceInput


def run_facility_site_allowance(inputs: Facility_Site_AllowanceInput) -> float:
    """Execute Facility_Site_Allowance calculation.

*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Retain the identified site-improvement allowance once in an active proposed layout; dormant contribution zero.

SysML Source: root-0/analyses/mfe_facilities.sysml:763

SysML Expressions:
    cost = active_in * amount_in
    
Documentation:
*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Retain the identified site-improvement allowance once in an active proposed layout; dormant contribution zero.

Args:
    inputs: Input parameters validated against Facility_Site_AllowanceInput schema

Returns:
    float: cost

Example:
    >>> inputs = Facility_Site_AllowanceInput(...)
    >>> result = run_facility_site_allowance(inputs)
    """
    return (inputs.active_in * inputs.amount_in)
