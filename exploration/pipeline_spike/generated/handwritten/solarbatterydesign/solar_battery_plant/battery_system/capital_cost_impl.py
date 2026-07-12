"""Auto-generated implementation for capital_cost.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    sum(battery_pack.capital_cost) + hybrid_inverter.capital_cost + battery_bos.capital_cost
"""

AUTO_IMPLEMENTED = True

from solar_battery_tea.modules.solarbatterydesign.solar_battery_plant.battery_system.capital_cost import capital_costInput


def run_capital_cost(inputs: capital_costInput) -> float:
    """Execute capital_cost calculation.

SysML Source: unknown:0

SysML Expressions:
    sum(battery_pack.capital_cost) + hybrid_inverter.capital_cost + battery_bos.capital_cost

Args:
    inputs: Input parameters validated against capital_costInput schema

Returns:
    float: capital_cost

Example:
    >>> inputs = capital_costInput(...)
    >>> result = run_capital_cost(inputs)
    """
    return (((inputs.pack_count * inputs.battery_pack_capital_cost) + inputs.hybrid_inverter_capital_cost) + inputs.battery_bos_capital_cost)
