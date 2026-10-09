"""Auto-generated implementation for Facility_Preconstruction_Selection.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_facilities.sysml:769

SysML Expressions:
    cost = (1.0 - mode_in) * legacy_in + mode_in * (fixed_in + land_in)
    
Documentation:
*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Replace only land; keep the fixed preconstruction adders and legacy mode.
"""

AUTO_IMPLEMENTED = True

from stellarator_materials_rebco_tea.modules.mfe_facilities.facility_preconstruction_selection import Facility_Preconstruction_SelectionInput


def run_facility_preconstruction_selection(inputs: Facility_Preconstruction_SelectionInput) -> float:
    """Execute Facility_Preconstruction_Selection calculation.

*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Replace only land; keep the fixed preconstruction adders and legacy mode.

SysML Source: root-0/analyses/mfe_facilities.sysml:769

SysML Expressions:
    cost = (1.0 - mode_in) * legacy_in + mode_in * (fixed_in + land_in)
    
Documentation:
*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Replace only land; keep the fixed preconstruction adders and legacy mode.

Args:
    inputs: Input parameters validated against Facility_Preconstruction_SelectionInput schema

Returns:
    float: cost

Example:
    >>> inputs = Facility_Preconstruction_SelectionInput(...)
    >>> result = run_facility_preconstruction_selection(inputs)
    """
    return (((1.0 - inputs.mode_in) * inputs.legacy_in) + (inputs.mode_in * (inputs.fixed_in + inputs.land_in)))
