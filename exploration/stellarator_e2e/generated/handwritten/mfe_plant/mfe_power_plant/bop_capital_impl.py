"""Auto-generated implementation for bop_capital.

AUTO_IMPLEMENTED = True

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:429

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_plant.mfe_power_plant.bop_capital import bop_capitalInput


def run_bop_capital(inputs: bop_capitalInput) -> float:
    """Execute bop_capital calculation.

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:429

Args:
    inputs: Input parameters validated against bop_capitalInput schema

Returns:
    float: bop_capital

Example:
    >>> inputs = bop_capitalInput(...)
    >>> result = run_bop_capital(inputs)
    """
    return (((inputs.turbine_capital_cost + inputs.electric_plant_capital_cost) + inputs.heat_rejection_capital_cost) + inputs.misc_plant_capital_cost)
