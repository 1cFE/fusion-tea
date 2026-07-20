"""Auto-generated implementation for direct_capital.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    powercore_capital + bop_capital + buildings.capital_cost + preconstruction_capital + special_materials_capital
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.stellarator_09.stellaris.direct_capital import direct_capitalInput


def run_direct_capital(inputs: direct_capitalInput) -> float:
    """Execute direct_capital calculation.

SysML Source: unknown:0

SysML Expressions:
    powercore_capital + bop_capital + buildings.capital_cost + preconstruction_capital + special_materials_capital

Args:
    inputs: Input parameters validated against direct_capitalInput schema

Returns:
    float: direct_capital

Example:
    >>> inputs = direct_capitalInput(...)
    >>> result = run_direct_capital(inputs)
    """
    return ((((inputs.powercore_capital + inputs.bop_capital) + inputs.buildings_capital_cost) + inputs.preconstruction_capital) + inputs.special_materials_capital)
