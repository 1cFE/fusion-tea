"""Auto-generated implementation for installation_cost.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    sum(battery_pack.installation_cost) + hybrid_inverter.installation_cost + battery_bos.installation_cost
"""

AUTO_IMPLEMENTED = True

from solar_battery_v5.modules.solarbatterydesign.solar_battery_plant.battery_system.installation_cost import installation_costInput


def run_installation_cost(inputs: installation_costInput) -> float:
    """Execute installation_cost calculation.

SysML Source: unknown:0

SysML Expressions:
    sum(battery_pack.installation_cost) + hybrid_inverter.installation_cost + battery_bos.installation_cost

Args:
    inputs: Input parameters validated against installation_costInput schema

Returns:
    float: installation_cost

Example:
    >>> inputs = installation_costInput(...)
    >>> result = run_installation_cost(inputs)
    """
    return (((inputs.pack_count * inputs.battery_pack_installation_cost) + inputs.hybrid_inverter_installation_cost) + inputs.battery_bos_installation_cost)
