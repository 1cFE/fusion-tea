"""Auto-generated implementation for installation_cost.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    sum(pv_module.installation_cost) + sum(inverter.installation_cost) + array_bos.installation_cost
"""

AUTO_IMPLEMENTED = True

from solar_battery_tea.modules.solarbatterydesign.solar_battery_plant.solar_array.installation_cost import installation_costInput


def run_installation_cost(inputs: installation_costInput) -> float:
    """Execute installation_cost calculation.

SysML Source: unknown:0

SysML Expressions:
    sum(pv_module.installation_cost) + sum(inverter.installation_cost) + array_bos.installation_cost

Args:
    inputs: Input parameters validated against installation_costInput schema

Returns:
    float: installation_cost

Example:
    >>> inputs = installation_costInput(...)
    >>> result = run_installation_cost(inputs)
    """
    return (((inputs.module_count * inputs.pv_module_installation_cost) + (inputs.inverter_count * inputs.inverter_installation_cost)) + inputs.array_bos_installation_cost)
