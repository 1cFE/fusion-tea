"""Auto-generated implementation for EnergyCalc.

AUTO_IMPLEMENTED = True

SysML Source: models/tests/e2e_attr_expr/library.sysml:31

SysML Expressions:
    annual_energy_mwh = LiteralRationalEvaluation() * power_mw * availability
"""

AUTO_IMPLEMENTED = True

from e2e_attr_expr_v5.modules.e2eattrexprlibrary.energycalc import EnergyCalcInput


def run_energycalc(inputs: EnergyCalcInput) -> float:
    """Execute EnergyCalc calculation.

SysML Source: models/tests/e2e_attr_expr/library.sysml:31

SysML Expressions:
    annual_energy_mwh = LiteralRationalEvaluation() * power_mw * availability

Args:
    inputs: Input parameters validated against EnergyCalcInput schema

Returns:
    float: annual_energy_mwh

Example:
    >>> inputs = EnergyCalcInput(...)
    >>> result = run_energycalc(inputs)
    """
    return ((8760.0 * inputs.power_mw) * inputs.availability)
