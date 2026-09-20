"""Auto-generated implementation for cas2x_pre_contingency.

AUTO_IMPLEMENTED = True

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:540

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_plant.mfe_power_plant.cas2x_pre_contingency import cas2x_pre_contingencyInput


def run_cas2x_pre_contingency(inputs: cas2x_pre_contingencyInput) -> float:
    """Execute cas2x_pre_contingency calculation.

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:540

Args:
    inputs: Input parameters validated against cas2x_pre_contingencyInput schema

Returns:
    float: cas2x_pre_contingency

Example:
    >>> inputs = cas2x_pre_contingencyInput(...)
    >>> result = run_cas2x_pre_contingency(inputs)
    """
    return ((((inputs.capital_cost + inputs.cas22_capital) + inputs.bop_capital) + inputs.special_materials_capital) + inputs.cas28_capital)
