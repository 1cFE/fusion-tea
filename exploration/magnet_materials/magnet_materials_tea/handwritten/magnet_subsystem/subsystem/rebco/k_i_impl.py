"""Auto-generated implementation for k_i.

AUTO_IMPLEMENTED = True

SysML Source: root-0/magnet_subsystem.sysml:708

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from magnet_materials_tea.modules.magnet_subsystem.subsystem.rebco.k_i import k_iInput


def run_k_i(inputs: k_iInput) -> float:
    """Execute k_i calculation.

SysML Source: root-0/magnet_subsystem.sysml:708

Args:
    inputs: Input parameters validated against k_iInput schema

Returns:
    float: k_i

Example:
    >>> inputs = k_iInput(...)
    >>> result = run_k_i(inputs)
    """
    return (-0.0199)
