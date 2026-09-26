"""Auto-generated implementation for rejected_heat.

AUTO_IMPLEMENTED = True

SysML Source: root-0/costed_loop_brayton.sysml:434

SysML Expressions:
"""

AUTO_IMPLEMENTED = True

from costed_loop_brayton_tea.modules.costed_loop_brayton.plant.rejection_capacity.rejected_heat import rejected_heatInput


def run_rejected_heat(inputs: rejected_heatInput) -> float:
    """Execute rejected_heat calculation.

SysML Source: root-0/costed_loop_brayton.sysml:434

Args:
    inputs: Input parameters validated against rejected_heatInput schema

Returns:
    float: rejected_heat

Example:
    >>> inputs = rejected_heatInput(...)
    >>> result = run_rejected_heat(inputs)
    """
    return (-((inputs.intercooler_1_heat_into_fluid + inputs.intercooler_2_heat_into_fluid) + inputs.precooler_heat_into_fluid))
