"""Auto-generated implementation for SimpleLCOECalc.

AUTO_IMPLEMENTED = True

SysML Source: models/tests/e2e_attr_expr/library.sysml:39

SysML Expressions:
    lcoe = annualized_capital + annual_om / annual_energy
"""

AUTO_IMPLEMENTED = True

from e2e_attr_expr.modules.e2eattrexprlibrary.simplelcoecalc import SimpleLCOECalcInput


def run_simplelcoecalc(inputs: SimpleLCOECalcInput) -> float:
    """Execute SimpleLCOECalc calculation.

SysML Source: models/tests/e2e_attr_expr/library.sysml:39

SysML Expressions:
    lcoe = annualized_capital + annual_om / annual_energy

Args:
    inputs: Input parameters validated against SimpleLCOECalcInput schema

Returns:
    float: lcoe

Example:
    >>> inputs = SimpleLCOECalcInput(...)
    >>> result = run_simplelcoecalc(inputs)
    """
    return ((inputs.annualized_capital + inputs.annual_om) / inputs.annual_energy)
