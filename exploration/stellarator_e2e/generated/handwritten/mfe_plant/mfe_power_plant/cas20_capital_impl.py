"""Auto-generated implementation for cas20_capital.

AUTO_IMPLEMENTED = True

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:554

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_plant.mfe_power_plant.cas20_capital import cas20_capitalInput


def run_cas20_capital(inputs: cas20_capitalInput) -> float:
    """Execute cas20_capital calculation.

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:554

Args:
    inputs: Input parameters validated against cas20_capitalInput schema

Returns:
    float: cas20_capital

Example:
    >>> inputs = cas20_capitalInput(...)
    >>> result = run_cas20_capital(inputs)
    """
    return (inputs.cas2x_pre_contingency + inputs.contingency_capital)
