"""Auto-generated implementation for turn_current.

AUTO_IMPLEMENTED = True

SysML Source: root-0/magnet_subsystem.sysml:30

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from magnet_materials_tea.modules.magnet_subsystem.subsystem.duty.turn_current import turn_currentInput


def run_turn_current(inputs: turn_currentInput) -> float:
    """Execute turn_current calculation.

SysML Source: root-0/magnet_subsystem.sysml:30

Args:
    inputs: Input parameters validated against turn_currentInput schema

Returns:
    float: turn_current

Example:
    >>> inputs = turn_currentInput(...)
    >>> result = run_turn_current(inputs)
    """
    return ((inputs.I_ref * inputs.B_peak) / inputs.B_ref)
