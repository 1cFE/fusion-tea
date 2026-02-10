"""Auto-generated implementation for E2EAttrExprDesign__e2e_plant__volume.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    length * width * height
"""

AUTO_IMPLEMENTED = True

from e2e_attr_expr.modules.e2eattrexprdesign.e2e_plant.volume import volumeInput


def run_e2eattrexprdesign__e2e_plant__volume(inputs: volumeInput) -> float:
    """Execute volume computed attribute.

SysML Expression: length * width * height
    """
    return ((inputs.length * inputs.width) * inputs.height)
