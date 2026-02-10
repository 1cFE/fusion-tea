"""Auto-generated implementation for AnnualizedCostCalc.

AUTO_IMPLEMENTED = True

SysML Source: models/tests/e2e_attr_expr/library.sysml:19

SysML Expressions:
    crf = discount_rate * 1.0 + discount_rate ** lifetime / 1.0 + discount_rate ** lifetime - 1.0
    annualized_cost = crf * total_capex
"""

AUTO_IMPLEMENTED = True

from e2e_attr_expr_v2.modules.e2eattrexprlibrary.annualizedcostcalc import AnnualizedCostCalcInput


def run_annualizedcostcalc(inputs: AnnualizedCostCalcInput) -> tuple[float, float]:
    """Execute AnnualizedCostCalc calculation.

SysML Source: models/tests/e2e_attr_expr/library.sysml:19

SysML Expressions:
    crf = discount_rate * 1.0 + discount_rate ** lifetime / 1.0 + discount_rate ** lifetime - 1.0
    annualized_cost = crf * total_capex

Args:
    inputs: Input parameters validated against AnnualizedCostCalcInput schema

Returns:
    tuple[float, ...]: (crf, annualized_cost)

Example:
    >>> inputs = AnnualizedCostCalcInput(...)
    >>> crf, annualized_cost = run_annualizedcostcalc(inputs)
    """
    crf = ((inputs.discount_rate * ((1.0 + inputs.discount_rate) ** inputs.lifetime)) / (((1.0 + inputs.discount_rate) ** inputs.lifetime) - 1.0))
    annualized_cost = (crf * inputs.total_capex)
    return (
        crf,
        annualized_cost,
    )
