"""Auto-generated implementation for idiot_index.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    capital_cost / raw_material_cost
"""

AUTO_IMPLEMENTED = True

from solar_battery_tea.modules.solarbatterydesign.solar_battery_plant.battery_system.idiot_index import idiot_indexInput


def run_idiot_index(inputs: idiot_indexInput) -> float:
    """Execute idiot_index calculation.

SysML Source: unknown:0

SysML Expressions:
    capital_cost / raw_material_cost

Args:
    inputs: Input parameters validated against idiot_indexInput schema

Returns:
    float: idiot_index

Example:
    >>> inputs = idiot_indexInput(...)
    >>> result = run_idiot_index(inputs)
    """
    return (inputs.capital_cost / inputs.raw_material_cost)
