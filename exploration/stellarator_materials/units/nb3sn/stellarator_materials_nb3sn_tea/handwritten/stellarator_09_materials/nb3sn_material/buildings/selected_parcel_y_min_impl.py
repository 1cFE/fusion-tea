"""Auto-generated implementation for selected_parcel_y_min.

AUTO_IMPLEMENTED = True

SysML Source: root-0/designs/stellarator_09_materials/nb3sn_material.sysml:1794

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from stellarator_materials_nb3sn_tea.modules.stellarator_09_materials.nb3sn_material.buildings.selected_parcel_y_min import selected_parcel_y_minInput


def run_selected_parcel_y_min(inputs: selected_parcel_y_minInput) -> float:
    """Execute selected_parcel_y_min calculation.

SysML Source: root-0/designs/stellarator_09_materials/nb3sn_material.sysml:1794

Args:
    inputs: Input parameters validated against selected_parcel_y_minInput schema

Returns:
    float: selected_parcel_y_min

Example:
    >>> inputs = selected_parcel_y_minInput(...)
    >>> result = run_selected_parcel_y_min(inputs)
    """
    return (inputs.parcel_origin_y_offset - 256.9046987566545)
