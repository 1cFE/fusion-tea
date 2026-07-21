"""Auto-generated implementation for overnight_capital.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    preconstruction_capital + cas20_capital + cas30_capital + owner_capital + supplementary_capital
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.stellarator_09.stellaris.overnight_capital import overnight_capitalInput


def run_overnight_capital(inputs: overnight_capitalInput) -> float:
    """Execute overnight_capital calculation.

SysML Source: unknown:0

SysML Expressions:
    preconstruction_capital + cas20_capital + cas30_capital + owner_capital + supplementary_capital

Args:
    inputs: Input parameters validated against overnight_capitalInput schema

Returns:
    float: overnight_capital

Example:
    >>> inputs = overnight_capitalInput(...)
    >>> result = run_overnight_capital(inputs)
    """
    return ((((inputs.preconstruction_capital + inputs.cas20_capital) + inputs.cas30_capital) + inputs.owner_capital) + inputs.supplementary_capital)
