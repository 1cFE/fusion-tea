"""Auto-generated implementation for fabrication_cost.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    sum(battery_pack.fabrication_cost) + hybrid_inverter.fabrication_cost + battery_bos.fabrication_cost
"""

AUTO_IMPLEMENTED = True

from solar_battery_tea.modules.solarbatterydesign.solar_battery_plant.battery_system.fabrication_cost import fabrication_costInput


def run_fabrication_cost(inputs: fabrication_costInput) -> float:
    """Execute fabrication_cost calculation.

SysML Source: unknown:0

SysML Expressions:
    sum(battery_pack.fabrication_cost) + hybrid_inverter.fabrication_cost + battery_bos.fabrication_cost

Args:
    inputs: Input parameters validated against fabrication_costInput schema

Returns:
    float: fabrication_cost

Example:
    >>> inputs = fabrication_costInput(...)
    >>> result = run_fabrication_cost(inputs)
    """
    return (((inputs.pack_count * inputs.battery_pack_fabrication_cost) + inputs.hybrid_inverter_fabrication_cost) + inputs.battery_bos_fabrication_cost)
