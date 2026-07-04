"""Auto-generated implementation for raw_material_cost.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    racking.raw_material_cost + electrical_panel.raw_material_cost + permitting.raw_material_cost
"""

AUTO_IMPLEMENTED = True

from solar_battery_tea.modules.solarbatterydesign.solar_battery_plant.site_infra.raw_material_cost import raw_material_costInput


def run_raw_material_cost(inputs: raw_material_costInput) -> float:
    """Execute raw_material_cost calculation.

SysML Source: unknown:0

SysML Expressions:
    racking.raw_material_cost + electrical_panel.raw_material_cost + permitting.raw_material_cost

Args:
    inputs: Input parameters validated against raw_material_costInput schema

Returns:
    float: raw_material_cost

Example:
    >>> inputs = raw_material_costInput(...)
    >>> result = run_raw_material_cost(inputs)
    """
    return ((inputs.racking_raw_material_cost + inputs.electrical_panel_raw_material_cost) + inputs.permitting_raw_material_cost)
