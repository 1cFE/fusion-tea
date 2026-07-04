"""Auto-generated implementation for raw_material_cost.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    sum(pv_module.raw_material_cost) + sum(inverter.raw_material_cost) + array_bos.raw_material_cost + allocation_model.material_portion
"""

AUTO_IMPLEMENTED = True

from solar_battery_tea.modules.solarbatterydesign.solar_battery_plant.solar_array.raw_material_cost import raw_material_costInput


def run_raw_material_cost(inputs: raw_material_costInput) -> float:
    """Execute raw_material_cost calculation.

SysML Source: unknown:0

SysML Expressions:
    sum(pv_module.raw_material_cost) + sum(inverter.raw_material_cost) + array_bos.raw_material_cost + allocation_model.material_portion

Args:
    inputs: Input parameters validated against raw_material_costInput schema

Returns:
    float: raw_material_cost

Example:
    >>> inputs = raw_material_costInput(...)
    >>> result = run_raw_material_cost(inputs)
    """
    return ((((inputs.module_count * inputs.pv_module_raw_material_cost) + (inputs.inverter_count * inputs.inverter_raw_material_cost)) + inputs.array_bos_raw_material_cost) + inputs.allocation_model_material_portion)
