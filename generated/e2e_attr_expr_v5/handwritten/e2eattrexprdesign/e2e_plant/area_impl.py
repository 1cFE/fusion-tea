"""Auto-generated implementation for area.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    length * width
"""

AUTO_IMPLEMENTED = True

from e2e_attr_expr_v5.modules.e2eattrexprdesign.e2e_plant.area import areaInput


def run_area(inputs: areaInput) -> float:
    """Execute area calculation.

SysML Source: unknown:0

SysML Expressions:
    length * width

Args:
    inputs: Input parameters validated against areaInput schema

Returns:
    float: area

Example:
    >>> inputs = areaInput(...)
    >>> result = run_area(inputs)
    """
    return (inputs.length * inputs.width)
