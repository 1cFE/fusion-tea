"""Auto-generated implementation for capital_cost.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    sum(pv_module.capital_cost) + sum(inverter.capital_cost) + array_bos.capital_cost + misc_hardware_cost
"""

AUTO_IMPLEMENTED = True

from solar_battery_v5.modules.solarbatterydesign.solar_battery_plant.solar_array.capital_cost import capital_costInput


def run_capital_cost(inputs: capital_costInput) -> float:
    """Execute capital_cost calculation.

SysML Source: unknown:0

SysML Expressions:
    sum(pv_module.capital_cost) + sum(inverter.capital_cost) + array_bos.capital_cost + misc_hardware_cost

Args:
    inputs: Input parameters validated against capital_costInput schema

Returns:
    float: capital_cost

Example:
    >>> inputs = capital_costInput(...)
    >>> result = run_capital_cost(inputs)
    """
    return ((((inputs.module_count * inputs.pv_module_capital_cost) + (inputs.inverter_count * inputs.inverter_capital_cost)) + inputs.array_bos_capital_cost) + inputs.misc_hardware_cost)
