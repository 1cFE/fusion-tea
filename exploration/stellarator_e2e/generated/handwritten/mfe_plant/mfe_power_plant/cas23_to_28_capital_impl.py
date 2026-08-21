"""Auto-generated implementation for cas23_to_28_capital.

AUTO_IMPLEMENTED = True

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:570

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_plant.mfe_power_plant.cas23_to_28_capital import cas23_to_28_capitalInput


def run_cas23_to_28_capital(inputs: cas23_to_28_capitalInput) -> float:
    """Execute cas23_to_28_capital calculation.

SysML Source: root-0/designs/generic_mfe/mfe_plant.sysml:570

Args:
    inputs: Input parameters validated against cas23_to_28_capitalInput schema

Returns:
    float: cas23_to_28_capital

Example:
    >>> inputs = cas23_to_28_capitalInput(...)
    >>> result = run_cas23_to_28_capital(inputs)
    """
    return ((inputs.bop_capital + inputs.special_materials_capital) + inputs.cas28_capital)
