"""Auto-generated implementation for selected_parcel_x_min.

AUTO_IMPLEMENTED = True

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:1634

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.stellarator_09.stellaris.buildings.selected_parcel_x_min import selected_parcel_x_minInput


def run_selected_parcel_x_min(inputs: selected_parcel_x_minInput) -> float:
    """Execute selected_parcel_x_min calculation.

SysML Source: root-0/designs/stellarator_09/stellarator_plant.sysml:1634

Args:
    inputs: Input parameters validated against selected_parcel_x_minInput schema

Returns:
    float: selected_parcel_x_min

Example:
    >>> inputs = selected_parcel_x_minInput(...)
    >>> result = run_selected_parcel_x_min(inputs)
    """
    return (inputs.parcel_origin_x_offset - 186.9046987566545)
