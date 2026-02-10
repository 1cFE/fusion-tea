"""Auto-generated implementation for AnnualizedFinancialCalc.

AUTO_IMPLEMENTED = True

SysML Source: models/tests/solar_battery/library.sysml:314

SysML Expressions:
    capital_recovery_factor = discount_rate * 1.0 + discount_rate ** plant_lifetime / 1.0 + discount_rate ** plant_lifetime - 1.0
    annualized_capital_cost = capital_recovery_factor * total_capex
    
Documentation:
Annualized financial cost using Capital Recovery Factor.
CRF = r * (1+r)^n / ((1+r)^n - 1)
Computes CRF from discount_rate and plant_lifetime rather than using
PyFECONS's hardcoded 0.09 default.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/cas90_annualized_financial.py:14
*Last Updated**: 2026-02-01
"""

AUTO_IMPLEMENTED = True

from solar_battery_v2.modules.solarbatterylibrary.annualizedfinancialcalc import AnnualizedFinancialCalcInput


def run_annualizedfinancialcalc(inputs: AnnualizedFinancialCalcInput) -> tuple[float, float]:
    """Execute AnnualizedFinancialCalc calculation.

Annualized financial cost using Capital Recovery Factor.
CRF = r * (1+r)^n / ((1+r)^n - 1)
Computes CRF from discount_rate and plant_lifetime rather than using
PyFECONS's hardcoded 0.09 default.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/cas90_annualized_financial.py:14
*Last Updated**: 2026-02-01

SysML Source: models/tests/solar_battery/library.sysml:314

SysML Expressions:
    capital_recovery_factor = discount_rate * 1.0 + discount_rate ** plant_lifetime / 1.0 + discount_rate ** plant_lifetime - 1.0
    annualized_capital_cost = capital_recovery_factor * total_capex
    
Documentation:
Annualized financial cost using Capital Recovery Factor.
CRF = r * (1+r)^n / ((1+r)^n - 1)
Computes CRF from discount_rate and plant_lifetime rather than using
PyFECONS's hardcoded 0.09 default.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/cas90_annualized_financial.py:14
*Last Updated**: 2026-02-01

Args:
    inputs: Input parameters validated against AnnualizedFinancialCalcInput schema

Returns:
    tuple[float, ...]: (capital_recovery_factor, annualized_capital_cost)

Example:
    >>> inputs = AnnualizedFinancialCalcInput(...)
    >>> capital_recovery_factor, annualized_capital_cost = run_annualizedfinancialcalc(inputs)
    """
    capital_recovery_factor = ((inputs.discount_rate * ((1.0 + inputs.discount_rate) ** inputs.plant_lifetime)) / (((1.0 + inputs.discount_rate) ** inputs.plant_lifetime) - 1.0))
    annualized_capital_cost = (capital_recovery_factor * inputs.total_capex)
    return (
        capital_recovery_factor,
        annualized_capital_cost,
    )
