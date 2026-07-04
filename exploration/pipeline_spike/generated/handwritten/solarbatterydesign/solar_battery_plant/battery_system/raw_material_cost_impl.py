"""Auto-generated implementation for raw_material_cost.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    sum(battery_pack.raw_material_cost) + hybrid_inverter.raw_material_cost + battery_bos.raw_material_cost
"""

AUTO_IMPLEMENTED = True

from solar_battery_tea.modules.solarbatterydesign.solar_battery_plant.battery_system.raw_material_cost import raw_material_costInput


def run_raw_material_cost(inputs: raw_material_costInput) -> float:
    """Execute raw_material_cost calculation.

SysML Source: unknown:0

SysML Expressions:
    sum(battery_pack.raw_material_cost) + hybrid_inverter.raw_material_cost + battery_bos.raw_material_cost

Args:
    inputs: Input parameters validated against raw_material_costInput schema

Returns:
    float: raw_material_cost

Example:
    >>> inputs = raw_material_costInput(...)
    >>> result = run_raw_material_cost(inputs)
    """
    return (((inputs.pack_count * inputs.battery_pack_raw_material_cost) + inputs.hybrid_inverter_raw_material_cost) + inputs.battery_bos_raw_material_cost)
