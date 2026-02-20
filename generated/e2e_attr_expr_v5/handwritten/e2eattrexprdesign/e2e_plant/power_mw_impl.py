"""Auto-generated implementation for power_mw.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    quantity * unit_cost / LiteralRationalEvaluation()
"""

AUTO_IMPLEMENTED = True

from e2e_attr_expr_v5.modules.e2eattrexprdesign.e2e_plant.power_mw import power_mwInput


def run_power_mw(inputs: power_mwInput) -> float:
    """Execute power_mw calculation.

SysML Source: unknown:0

SysML Expressions:
    quantity * unit_cost / LiteralRationalEvaluation()

Args:
    inputs: Input parameters validated against power_mwInput schema

Returns:
    float: power_mw

Example:
    >>> inputs = power_mwInput(...)
    >>> result = run_power_mw(inputs)
    """
    return ((inputs.quantity * inputs.unit_cost) / 1000000.0)
