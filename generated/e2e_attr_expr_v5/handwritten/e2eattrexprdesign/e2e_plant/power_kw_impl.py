"""Auto-generated implementation for power_kw.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    power_mw * LiteralRationalEvaluation()
"""

AUTO_IMPLEMENTED = True

from e2e_attr_expr_v5.modules.e2eattrexprdesign.e2e_plant.power_kw import power_kwInput


def run_power_kw(inputs: power_kwInput) -> float:
    """Execute power_kw calculation.

SysML Source: unknown:0

SysML Expressions:
    power_mw * LiteralRationalEvaluation()

Args:
    inputs: Input parameters validated against power_kwInput schema

Returns:
    float: power_kw

Example:
    >>> inputs = power_kwInput(...)
    >>> result = run_power_kw(inputs)
    """
    return (inputs.power_mw * 1000.0)
