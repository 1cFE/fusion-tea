"""Auto-generated implementation for selected_parcel_y_min.

AUTO_IMPLEMENTED = True

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:1633

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.stellarator_09.stellaris.buildings.selected_parcel_y_min import selected_parcel_y_minInput


def run_selected_parcel_y_min(inputs: selected_parcel_y_minInput) -> float:
    """Execute selected_parcel_y_min calculation.

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:1633

Args:
    inputs: Input parameters validated against selected_parcel_y_minInput schema

Returns:
    float: selected_parcel_y_min

Example:
    >>> inputs = selected_parcel_y_minInput(...)
    >>> result = run_selected_parcel_y_min(inputs)
    """
    return (inputs.parcel_origin_y_offset - 256.9046987566545)
