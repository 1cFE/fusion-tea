"""Auto-generated implementation for annual_om.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    om_rate * power_kw
"""

AUTO_IMPLEMENTED = True

from e2e_attr_expr_v5.modules.e2eattrexprdesign.e2e_plant.annual_om import annual_omInput


def run_annual_om(inputs: annual_omInput) -> float:
    """Execute annual_om calculation.

SysML Source: unknown:0

SysML Expressions:
    om_rate * power_kw

Args:
    inputs: Input parameters validated against annual_omInput schema

Returns:
    float: annual_om

Example:
    >>> inputs = annual_omInput(...)
    >>> result = run_annual_om(inputs)
    """
    return (inputs.om_rate * inputs.power_kw)
