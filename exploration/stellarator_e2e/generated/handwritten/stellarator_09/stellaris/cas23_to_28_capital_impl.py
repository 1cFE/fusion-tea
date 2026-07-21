"""Auto-generated implementation for cas23_to_28_capital.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    bop_capital + special_materials_capital + cas28_capital
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.stellarator_09.stellaris.cas23_to_28_capital import cas23_to_28_capitalInput


def run_cas23_to_28_capital(inputs: cas23_to_28_capitalInput) -> float:
    """Execute cas23_to_28_capital calculation.

SysML Source: unknown:0

SysML Expressions:
    bop_capital + special_materials_capital + cas28_capital

Args:
    inputs: Input parameters validated against cas23_to_28_capitalInput schema

Returns:
    float: cas23_to_28_capital

Example:
    >>> inputs = cas23_to_28_capitalInput(...)
    >>> result = run_cas23_to_28_capital(inputs)
    """
    return ((inputs.bop_capital + inputs.special_materials_capital) + inputs.cas28_capital)
