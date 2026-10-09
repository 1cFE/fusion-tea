"""Auto-generated implementation for Facility_Account_Selection.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_facilities.sysml:746

SysML Expressions:
    installed_facility_capital = civil_in + ventilation_in
    layout_buildings_capital = installed_facility_capital + site_in
    cost = (1.0 - mode_in) * legacy_in + mode_in * layout_buildings_capital
    
Documentation:
*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Select the complete priced facility account or the preserved grouped legacy account; layout validates the binary mode.
"""

AUTO_IMPLEMENTED = True

from stellarator_materials_nb3sn_tea.modules.mfe_facilities.facility_account_selection import Facility_Account_SelectionInput


def run_facility_account_selection(inputs: Facility_Account_SelectionInput) -> tuple[float, float, float]:
    """Execute Facility_Account_Selection calculation.

*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Select the complete priced facility account or the preserved grouped legacy account; layout validates the binary mode.

SysML Source: root-0/analyses/mfe_facilities.sysml:746

SysML Expressions:
    installed_facility_capital = civil_in + ventilation_in
    layout_buildings_capital = installed_facility_capital + site_in
    cost = (1.0 - mode_in) * legacy_in + mode_in * layout_buildings_capital
    
Documentation:
*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Select the complete priced facility account or the preserved grouped legacy account; layout validates the binary mode.

Args:
    inputs: Input parameters validated against Facility_Account_SelectionInput schema

Returns:
    tuple[float, ...]: (layout_buildings_capital, cost, installed_facility_capital)

Example:
    >>> inputs = Facility_Account_SelectionInput(...)
    >>> layout_buildings_capital, cost, installed_facility_capital = run_facility_account_selection(inputs)
    """
    installed_facility_capital = (inputs.civil_in + inputs.ventilation_in)
    layout_buildings_capital = (installed_facility_capital + inputs.site_in)
    return (
        layout_buildings_capital,
        (((1.0 - inputs.mode_in) * inputs.legacy_in) + (inputs.mode_in * layout_buildings_capital)),  # cost
        installed_facility_capital,
    )
