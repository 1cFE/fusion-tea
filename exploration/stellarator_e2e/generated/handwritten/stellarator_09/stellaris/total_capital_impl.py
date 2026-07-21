"""Auto-generated implementation for total_capital.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    preconstruction_capital + cas20_capital + cas30_capital + owner_capital + supplementary_capital
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.stellarator_09.stellaris.total_capital import total_capitalInput


def run_total_capital(inputs: total_capitalInput) -> float:
    """Execute total_capital calculation.

SysML Source: unknown:0

SysML Expressions:
    preconstruction_capital + cas20_capital + cas30_capital + owner_capital + supplementary_capital

Args:
    inputs: Input parameters validated against total_capitalInput schema

Returns:
    float: total_capital

Example:
    >>> inputs = total_capitalInput(...)
    >>> result = run_total_capital(inputs)
    """
    return ((((inputs.preconstruction_capital + inputs.cas20_capital) + inputs.cas30_capital) + inputs.owner_capital) + inputs.supplementary_capital)
