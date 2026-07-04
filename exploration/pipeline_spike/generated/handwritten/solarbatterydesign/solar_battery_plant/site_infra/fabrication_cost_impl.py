"""Auto-generated implementation for fabrication_cost.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    racking.fabrication_cost + electrical_panel.fabrication_cost + permitting.fabrication_cost
"""

AUTO_IMPLEMENTED = True

from solar_battery_tea.modules.solarbatterydesign.solar_battery_plant.site_infra.fabrication_cost import fabrication_costInput


def run_fabrication_cost(inputs: fabrication_costInput) -> float:
    """Execute fabrication_cost calculation.

SysML Source: unknown:0

SysML Expressions:
    racking.fabrication_cost + electrical_panel.fabrication_cost + permitting.fabrication_cost

Args:
    inputs: Input parameters validated against fabrication_costInput schema

Returns:
    float: fabrication_cost

Example:
    >>> inputs = fabrication_costInput(...)
    >>> result = run_fabrication_cost(inputs)
    """
    return ((inputs.racking_fabrication_cost + inputs.electrical_panel_fabrication_cost) + inputs.permitting_fabrication_cost)
