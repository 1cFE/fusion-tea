"""Auto-generated implementation for surface_cost.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    area * cost_per_sqm
"""

AUTO_IMPLEMENTED = True

from e2e_attr_expr_v5.modules.e2eattrexprdesign.e2e_plant.surface_cost import surface_costInput


def run_surface_cost(inputs: surface_costInput) -> float:
    """Execute surface_cost calculation.

SysML Source: unknown:0

SysML Expressions:
    area * cost_per_sqm

Args:
    inputs: Input parameters validated against surface_costInput schema

Returns:
    float: surface_cost

Example:
    >>> inputs = surface_costInput(...)
    >>> result = run_surface_cost(inputs)
    """
    return (inputs.area * inputs.cost_per_sqm)
