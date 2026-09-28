"""Auto-generated implementation for Legacy.

AUTO_IMPLEMENTED = True

SysML Source: root-0/probe.sysml:3

SysML Expressions:
    gross_out = x_in * 2.0
"""

AUTO_IMPLEMENTED = True

from probe_selector.modules.probe.legacy import LegacyInput


def run_legacy(inputs: LegacyInput) -> float:
    """Execute Legacy calculation.

SysML Source: root-0/probe.sysml:3

SysML Expressions:
    gross_out = x_in * 2.0

Args:
    inputs: Input parameters validated against LegacyInput schema

Returns:
    float: gross_out

Example:
    >>> inputs = LegacyInput(...)
    >>> result = run_legacy(inputs)
    """
    return (inputs.x_in * 2.0)
