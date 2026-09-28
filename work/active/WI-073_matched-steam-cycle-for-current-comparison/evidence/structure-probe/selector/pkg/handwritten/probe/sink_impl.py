"""Auto-generated implementation for Sink.

AUTO_IMPLEMENTED = True

SysML Source: root-0/probe.sysml:15

SysML Expressions:
    result = value_in
"""

AUTO_IMPLEMENTED = True

from probe_selector.modules.probe.sink import SinkInput


def run_sink(inputs: SinkInput) -> float:
    """Execute Sink calculation.

SysML Source: root-0/probe.sysml:15

SysML Expressions:
    result = value_in

Args:
    inputs: Input parameters validated against SinkInput schema

Returns:
    float: result

Example:
    >>> inputs = SinkInput(...)
    >>> result = run_sink(inputs)
    """
    return inputs.value_in
