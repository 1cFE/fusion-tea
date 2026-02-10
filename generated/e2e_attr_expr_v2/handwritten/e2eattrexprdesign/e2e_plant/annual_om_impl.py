"""Auto-generated implementation for E2EAttrExprDesign__e2e_plant__annual_om.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    om_rate * power_kw
"""

AUTO_IMPLEMENTED = True

from e2e_attr_expr_v2.modules.e2eattrexprdesign.e2e_plant.annual_om import annual_omInput


def run_e2eattrexprdesign__e2e_plant__annual_om(inputs: annual_omInput) -> float:
    """Execute annual_om computed attribute.

SysML Expression: om_rate * power_kw
    """
    return (inputs.om_rate * inputs.power_kw)
