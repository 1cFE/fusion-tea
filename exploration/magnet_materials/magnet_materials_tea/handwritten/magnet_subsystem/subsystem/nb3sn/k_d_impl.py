"""Auto-generated implementation for k_d.

AUTO_IMPLEMENTED = True

SysML Source: root-0/magnet_subsystem.sysml:277

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from magnet_materials_tea.modules.magnet_subsystem.subsystem.nb3sn.k_d import k_dInput


def run_k_d(inputs: k_dInput) -> float:
    """Execute k_d calculation.

SysML Source: root-0/magnet_subsystem.sysml:277

Args:
    inputs: Input parameters validated against k_dInput schema

Returns:
    float: k_d

Example:
    >>> inputs = k_dInput(...)
    >>> result = run_k_d(inputs)
    """
    return (-0.626)
