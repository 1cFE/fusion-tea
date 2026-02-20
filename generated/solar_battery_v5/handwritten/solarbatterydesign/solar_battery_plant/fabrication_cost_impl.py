"""Auto-generated implementation for fabrication_cost.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    solar_array.fabrication_cost + battery_system.fabrication_cost + site_infra.fabrication_cost
"""

AUTO_IMPLEMENTED = True

from solar_battery_v5.modules.solarbatterydesign.solar_battery_plant.fabrication_cost import fabrication_costInput


def run_fabrication_cost(inputs: fabrication_costInput) -> float:
    """Execute fabrication_cost calculation.

SysML Source: unknown:0

SysML Expressions:
    solar_array.fabrication_cost + battery_system.fabrication_cost + site_infra.fabrication_cost

Args:
    inputs: Input parameters validated against fabrication_costInput schema

Returns:
    float: fabrication_cost

Example:
    >>> inputs = fabrication_costInput(...)
    >>> result = run_fabrication_cost(inputs)
    """
    return ((inputs.solar_array_fabrication_cost + inputs.battery_system_fabrication_cost) + inputs.site_infra_fabrication_cost)
