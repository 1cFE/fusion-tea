"""Auto-generated implementation for E2EAttrExprDesign__e2e_plant__power_kw.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    power_mw * 1000.0
"""

AUTO_IMPLEMENTED = True

from e2e_attr_expr.modules.e2eattrexprdesign.e2e_plant.power_kw import power_kwInput


def run_e2eattrexprdesign__e2e_plant__power_kw(inputs: power_kwInput) -> float:
    """Execute power_kw computed attribute.

SysML Expression: power_mw * 1000.0
    """
    return (inputs.power_mw * 1000.0)
