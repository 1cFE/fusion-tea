"""Auto-generated implementation for total_capital.

AUTO_IMPLEMENTED = True

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:624

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_plant.mfe_power_plant.total_capital import total_capitalInput


def run_total_capital(inputs: total_capitalInput) -> float:
    """Execute total_capital calculation.

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:624

Args:
    inputs: Input parameters validated against total_capitalInput schema

Returns:
    float: total_capital

Example:
    >>> inputs = total_capitalInput(...)
    >>> result = run_total_capital(inputs)
    """
    return ((((inputs.preconstruction_capital + inputs.cas20_capital) + inputs.cas30_capital) + inputs.owner_capital) + inputs.supplementary_capital)
