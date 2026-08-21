"""Auto-generated implementation for overnight_capital.

AUTO_IMPLEMENTED = True

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:605

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_plant.mfe_power_plant.overnight_capital import overnight_capitalInput


def run_overnight_capital(inputs: overnight_capitalInput) -> float:
    """Execute overnight_capital calculation.

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:605

Args:
    inputs: Input parameters validated against overnight_capitalInput schema

Returns:
    float: overnight_capital

Example:
    >>> inputs = overnight_capitalInput(...)
    >>> result = run_overnight_capital(inputs)
    """
    return ((((inputs.preconstruction_capital + inputs.cas20_capital) + inputs.cas30_capital) + inputs.owner_capital) + inputs.supplementary_capital)
