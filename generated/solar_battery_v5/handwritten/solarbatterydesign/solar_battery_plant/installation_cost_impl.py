"""Auto-generated implementation for installation_cost.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    solar_array.installation_cost + battery_system.installation_cost + site_infra.installation_cost
"""

AUTO_IMPLEMENTED = True

from solar_battery_v5.modules.solarbatterydesign.solar_battery_plant.installation_cost import installation_costInput


def run_installation_cost(inputs: installation_costInput) -> float:
    """Execute installation_cost calculation.

SysML Source: unknown:0

SysML Expressions:
    solar_array.installation_cost + battery_system.installation_cost + site_infra.installation_cost

Args:
    inputs: Input parameters validated against installation_costInput schema

Returns:
    float: installation_cost

Example:
    >>> inputs = installation_costInput(...)
    >>> result = run_installation_cost(inputs)
    """
    return ((inputs.solar_array_installation_cost + inputs.battery_system_installation_cost) + inputs.site_infra_installation_cost)
