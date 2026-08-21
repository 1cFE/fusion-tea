"""Auto-generated implementation for cas2x_pre_contingency.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    buildings.capital_cost + cas22_capital + bop_capital + special_materials_capital + cas28_capital
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.stellarator_09.stellaris.cas2x_pre_contingency import cas2x_pre_contingencyInput


def run_cas2x_pre_contingency(inputs: cas2x_pre_contingencyInput) -> float:
    """Execute cas2x_pre_contingency calculation.

SysML Source: unknown:0

SysML Expressions:
    buildings.capital_cost + cas22_capital + bop_capital + special_materials_capital + cas28_capital

Args:
    inputs: Input parameters validated against cas2x_pre_contingencyInput schema

Returns:
    float: cas2x_pre_contingency

Example:
    >>> inputs = cas2x_pre_contingencyInput(...)
    >>> result = run_cas2x_pre_contingency(inputs)
    """
    return ((((inputs.buildings_capital_cost + inputs.cas22_capital) + inputs.bop_capital) + inputs.special_materials_capital) + inputs.cas28_capital)
