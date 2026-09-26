"""Auto-generated implementation for cycle_rejection.

AUTO_IMPLEMENTED = True

SysML Source: root-0/combinations_plasma_chain.sysml:695

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from combinations_tea.modules.combinations_plasma_chain.plasma_chain.rejection_capacity.cycle_rejection import cycle_rejectionInput


def run_cycle_rejection(inputs: cycle_rejectionInput) -> float:
    """Execute cycle_rejection calculation.

SysML Source: root-0/combinations_plasma_chain.sysml:695

Args:
    inputs: Input parameters validated against cycle_rejectionInput schema

Returns:
    float: cycle_rejection

Example:
    >>> inputs = cycle_rejectionInput(...)
    >>> result = run_cycle_rejection(inputs)
    """
    return (-((inputs.intercooler_1_heat_into_fluid + inputs.intercooler_2_heat_into_fluid) + inputs.precooler_heat_into_fluid))
