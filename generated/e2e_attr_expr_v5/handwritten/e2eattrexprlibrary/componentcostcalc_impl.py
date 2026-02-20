"""Auto-generated implementation for ComponentCostCalc.

AUTO_IMPLEMENTED = True

SysML Source: models/tests/e2e_attr_expr/library.sysml:5

SysML Expressions:
    fab_factor = LiteralRationalEvaluation()
    install_factor = LiteralRationalEvaluation()
    material_cost = quantity * unit_cost
    fab_cost = material_cost * fab_factor
    install_cost = material_cost * install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
"""

AUTO_IMPLEMENTED = True

from e2e_attr_expr_v5.modules.e2eattrexprlibrary.componentcostcalc import ComponentCostCalcInput


def run_componentcostcalc(inputs: ComponentCostCalcInput) -> tuple[float, float, float, float, float]:
    """Execute ComponentCostCalc calculation.

SysML Source: models/tests/e2e_attr_expr/library.sysml:5

SysML Expressions:
    fab_factor = LiteralRationalEvaluation()
    install_factor = LiteralRationalEvaluation()
    material_cost = quantity * unit_cost
    fab_cost = material_cost * fab_factor
    install_cost = material_cost * install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost

Args:
    inputs: Input parameters validated against ComponentCostCalcInput schema

Returns:
    tuple[float, ...]: (material_cost, fab_cost, install_cost, total_cost, idiot_index)

Example:
    >>> inputs = ComponentCostCalcInput(...)
    >>> material_cost, fab_cost, install_cost, total_cost, idiot_index = run_componentcostcalc(inputs)
    """
    material_cost = (inputs.quantity * inputs.unit_cost)
    fab_cost = (material_cost * inputs.fab_factor)
    install_cost = (material_cost * inputs.install_factor)
    total_cost = ((material_cost + fab_cost) + install_cost)
    idiot_index = (total_cost / material_cost)
    return (
        material_cost,
        fab_cost,
        install_cost,
        total_cost,
        idiot_index,
    )
