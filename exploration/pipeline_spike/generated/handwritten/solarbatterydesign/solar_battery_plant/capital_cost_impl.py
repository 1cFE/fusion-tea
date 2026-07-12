"""Auto-generated implementation for capital_cost.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    solar_array.capital_cost + battery_system.capital_cost + site_infra.capital_cost
"""

AUTO_IMPLEMENTED = True

from solar_battery_tea.modules.solarbatterydesign.solar_battery_plant.capital_cost import capital_costInput


def run_capital_cost(inputs: capital_costInput) -> float:
    """Execute capital_cost calculation.

SysML Source: unknown:0

SysML Expressions:
    solar_array.capital_cost + battery_system.capital_cost + site_infra.capital_cost

Args:
    inputs: Input parameters validated against capital_costInput schema

Returns:
    float: capital_cost

Example:
    >>> inputs = capital_costInput(...)
    >>> result = run_capital_cost(inputs)
    """
    return ((inputs.solar_array_capital_cost + inputs.battery_system_capital_cost) + inputs.site_infra_capital_cost)
