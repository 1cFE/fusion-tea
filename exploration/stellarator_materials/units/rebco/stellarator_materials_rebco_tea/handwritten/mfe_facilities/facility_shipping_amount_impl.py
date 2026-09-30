"""Auto-generated implementation for Facility_Shipping_Amount.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_facilities.sysml:777

SysML Expressions:
    exclusion = mode_in * (1.0 + contingency_in) * installed_in
    
Documentation:
*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Exclude the entire contingency-loaded installed facility contribution from freight, without altering tax or insurance.
"""

AUTO_IMPLEMENTED = True

from stellarator_materials_rebco_tea.modules.mfe_facilities.facility_shipping_amount import Facility_Shipping_AmountInput


def run_facility_shipping_amount(inputs: Facility_Shipping_AmountInput) -> float:
    """Execute Facility_Shipping_Amount calculation.

*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Exclude the entire contingency-loaded installed facility contribution from freight, without altering tax or insurance.

SysML Source: root-0/analyses/mfe_facilities.sysml:777

SysML Expressions:
    exclusion = mode_in * (1.0 + contingency_in) * installed_in
    
Documentation:
*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Exclude the entire contingency-loaded installed facility contribution from freight, without altering tax or insurance.

Args:
    inputs: Input parameters validated against Facility_Shipping_AmountInput schema

Returns:
    float: exclusion

Example:
    >>> inputs = Facility_Shipping_AmountInput(...)
    >>> result = run_facility_shipping_amount(inputs)
    """
    return ((inputs.mode_in * (1.0 + inputs.contingency_in)) * inputs.installed_in)
