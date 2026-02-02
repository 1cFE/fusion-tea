from solar_battery.modules.solarbatterylibrary.annualizedfinancialcalc import AnnualizedFinancialCalcInput


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
    capital_recovery_factor = discount_rate * ??? + discount_rate ** plant_lifetime / ??? + discount_rate ** plant_lifetime - ???
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

    Implementation Pattern:
        # Extract input fields from the validated Input model:
        total_capex = inputs.total_capex
        discount_rate = inputs.discount_rate
        plant_lifetime = inputs.plant_lifetime
        # Perform calculation using extracted values
        # Return result(s)
    """
    r = inputs.discount_rate
    n = inputs.plant_lifetime
    crf = r * (1 + r) ** n / ((1 + r) ** n - 1)
    annualized_capital_cost = crf * inputs.total_capex
    return crf, annualized_capital_cost
