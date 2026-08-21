"""Auto-generated implementation for bop_capital.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    turbine.capital_cost + electric_plant.capital_cost + heat_rejection.capital_cost + misc_plant.capital_cost
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.stellarator_09.stellaris.bop_capital import bop_capitalInput


def run_bop_capital(inputs: bop_capitalInput) -> float:
    """Execute bop_capital calculation.

SysML Source: unknown:0

SysML Expressions:
    turbine.capital_cost + electric_plant.capital_cost + heat_rejection.capital_cost + misc_plant.capital_cost

Args:
    inputs: Input parameters validated against bop_capitalInput schema

Returns:
    float: bop_capital

Example:
    >>> inputs = bop_capitalInput(...)
    >>> result = run_bop_capital(inputs)
    """
    return (((inputs.turbine_capital_cost + inputs.electric_plant_capital_cost) + inputs.heat_rejection_capital_cost) + inputs.misc_plant_capital_cost)
