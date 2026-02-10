"""Auto-generated implementation for E2EAttrExprDesign__e2e_plant__surface_cost.

AUTO_IMPLEMENTED = True

SysML Source: unknown:0

SysML Expressions:
    area * cost_per_sqm
"""

AUTO_IMPLEMENTED = True

from e2e_attr_expr_v2.modules.e2eattrexprdesign.e2e_plant.surface_cost import surface_costInput


def run_e2eattrexprdesign__e2e_plant__surface_cost(inputs: surface_costInput) -> float:
    """Execute surface_cost computed attribute.

SysML Expression: area * cost_per_sqm
    """
    return (inputs.area * inputs.cost_per_sqm)
