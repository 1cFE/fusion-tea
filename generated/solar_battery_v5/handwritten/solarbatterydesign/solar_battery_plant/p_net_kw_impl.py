"""Auto-generated implementation for p_net_kw.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    p_net_mw * LiteralRationalEvaluation()
"""

AUTO_IMPLEMENTED = True

from solar_battery_v5.modules.solarbatterydesign.solar_battery_plant.p_net_kw import p_net_kwInput


def run_p_net_kw(inputs: p_net_kwInput) -> float:
    """Execute p_net_kw calculation.

SysML Source: unknown:0

SysML Expressions:
    p_net_mw * LiteralRationalEvaluation()

Args:
    inputs: Input parameters validated against p_net_kwInput schema

Returns:
    float: p_net_kw

Example:
    >>> inputs = p_net_kwInput(...)
    >>> result = run_p_net_kw(inputs)
    """
    return (inputs.p_net_mw * 1000.0)
