"""Auto-generated implementation for all_pass.

AUTO_IMPLEMENTED = True

SysML Source: root-0/magnet_subsystem.sysml:445

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from magnet_materials_tea.modules.magnet_subsystem.subsystem.nb3sn.all_pass import all_passInput


def run_all_pass(inputs: all_passInput) -> float:
    """Execute all_pass calculation.

SysML Source: root-0/magnet_subsystem.sysml:445

Args:
    inputs: Input parameters validated against all_passInput schema

Returns:
    float: all_pass

Example:
    >>> inputs = all_passInput(...)
    >>> result = run_all_pass(inputs)
    """
    return ((((inputs.acceptance_pass * inputs.fit_pass) * inputs.cu_pass) * inputs.steel_pass) * inputs.capacity_pass)
