"""Auto-generated implementation for E2EAttrExprDesign__e2e_plant__power_mw.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    quantity * unit_cost / 1000000.0
"""

AUTO_IMPLEMENTED = True

from e2e_attr_expr_v2.modules.e2eattrexprdesign.e2e_plant.power_mw import power_mwInput


def run_e2eattrexprdesign__e2e_plant__power_mw(inputs: power_mwInput) -> float:
    """Execute power_mw computed attribute.

SysML Expression: quantity * unit_cost / 1000000.0
    """
    return ((inputs.quantity * inputs.unit_cost) / 1000000.0)
