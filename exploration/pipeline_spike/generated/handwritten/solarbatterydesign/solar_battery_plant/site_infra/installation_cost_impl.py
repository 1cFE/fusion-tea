"""Auto-generated implementation for installation_cost.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    racking.installation_cost + electrical_panel.installation_cost + permitting.installation_cost
"""

AUTO_IMPLEMENTED = True

from solar_battery_tea.modules.solarbatterydesign.solar_battery_plant.site_infra.installation_cost import installation_costInput


def run_installation_cost(inputs: installation_costInput) -> float:
    """Execute installation_cost calculation.

SysML Source: unknown:0

SysML Expressions:
    racking.installation_cost + electrical_panel.installation_cost + permitting.installation_cost

Args:
    inputs: Input parameters validated against installation_costInput schema

Returns:
    float: installation_cost

Example:
    >>> inputs = installation_costInput(...)
    >>> result = run_installation_cost(inputs)
    """
    return ((inputs.racking_installation_cost + inputs.electrical_panel_installation_cost) + inputs.permitting_installation_cost)
