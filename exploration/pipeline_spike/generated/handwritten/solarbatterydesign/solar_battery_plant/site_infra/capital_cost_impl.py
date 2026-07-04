"""Auto-generated implementation for capital_cost.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    racking.capital_cost + electrical_panel.capital_cost + permitting.capital_cost
"""

AUTO_IMPLEMENTED = True

from solar_battery_tea.modules.solarbatterydesign.solar_battery_plant.site_infra.capital_cost import capital_costInput


def run_capital_cost(inputs: capital_costInput) -> float:
    """Execute capital_cost calculation.

SysML Source: unknown:0

SysML Expressions:
    racking.capital_cost + electrical_panel.capital_cost + permitting.capital_cost

Args:
    inputs: Input parameters validated against capital_costInput schema

Returns:
    float: capital_cost

Example:
    >>> inputs = capital_costInput(...)
    >>> result = run_capital_cost(inputs)
    """
    return ((inputs.racking_capital_cost + inputs.electrical_panel_capital_cost) + inputs.permitting_capital_cost)
