"""Auto-generated implementation for cas20_capital.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    cas2x_pre_contingency + contingency_capital
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.stellarator_09.stellaris.cas20_capital import cas20_capitalInput


def run_cas20_capital(inputs: cas20_capitalInput) -> float:
    """Execute cas20_capital calculation.

SysML Source: unknown:0

SysML Expressions:
    cas2x_pre_contingency + contingency_capital

Args:
    inputs: Input parameters validated against cas20_capitalInput schema

Returns:
    float: cas20_capital

Example:
    >>> inputs = cas20_capitalInput(...)
    >>> result = run_cas20_capital(inputs)
    """
    return (inputs.cas2x_pre_contingency + inputs.contingency_capital)
