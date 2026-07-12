"""Auto-generated implementation for fabrication_cost.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    sum(pv_module.fabrication_cost) + sum(inverter.fabrication_cost) + array_bos.fabrication_cost
"""

AUTO_IMPLEMENTED = True

from solar_battery_tea.modules.solarbatterydesign.solar_battery_plant.solar_array.fabrication_cost import fabrication_costInput


def run_fabrication_cost(inputs: fabrication_costInput) -> float:
    """Execute fabrication_cost calculation.

SysML Source: unknown:0

SysML Expressions:
    sum(pv_module.fabrication_cost) + sum(inverter.fabrication_cost) + array_bos.fabrication_cost

Args:
    inputs: Input parameters validated against fabrication_costInput schema

Returns:
    float: fabrication_cost

Example:
    >>> inputs = fabrication_costInput(...)
    >>> result = run_fabrication_cost(inputs)
    """
    return (((inputs.module_count * inputs.pv_module_fabrication_cost) + (inputs.inverter_count * inputs.inverter_fabrication_cost)) + inputs.array_bos_fabrication_cost)
