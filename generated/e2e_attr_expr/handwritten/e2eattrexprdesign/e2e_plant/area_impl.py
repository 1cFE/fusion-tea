"""Auto-generated implementation for E2EAttrExprDesign__e2e_plant__area.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    length * width
"""

AUTO_IMPLEMENTED = True

from e2e_attr_expr.modules.e2eattrexprdesign.e2e_plant.area import areaInput


def run_e2eattrexprdesign__e2e_plant__area(inputs: areaInput) -> float:
    """Execute area computed attribute.

SysML Expression: length * width
    """
    return (inputs.length * inputs.width)
