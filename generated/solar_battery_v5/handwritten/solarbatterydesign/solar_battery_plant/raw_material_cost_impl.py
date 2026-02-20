"""Auto-generated implementation for raw_material_cost.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    solar_array.raw_material_cost + battery_system.raw_material_cost + site_infra.raw_material_cost
"""

AUTO_IMPLEMENTED = True

from solar_battery_v5.modules.solarbatterydesign.solar_battery_plant.raw_material_cost import raw_material_costInput


def run_raw_material_cost(inputs: raw_material_costInput) -> float:
    """Execute raw_material_cost calculation.

SysML Source: unknown:0

SysML Expressions:
    solar_array.raw_material_cost + battery_system.raw_material_cost + site_infra.raw_material_cost

Args:
    inputs: Input parameters validated against raw_material_costInput schema

Returns:
    float: raw_material_cost

Example:
    >>> inputs = raw_material_costInput(...)
    >>> result = run_raw_material_cost(inputs)
    """
    return ((inputs.solar_array_raw_material_cost + inputs.battery_system_raw_material_cost) + inputs.site_infra_raw_material_cost)
