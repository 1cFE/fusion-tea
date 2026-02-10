"""Auto-generated implementation for AnnualizedFuelCalc.

AUTO_IMPLEMENTED = True

SysML Source: models/tests/solar_battery/library.sysml:298

SysML Expressions:
    annual_fuel_cost = fuel_unit_cost * fuel_consumption
    
Documentation:
Annualized fuel cost.
For solar: fuel_unit_cost = 0, fuel_consumption = 0 → annual_fuel_cost = 0.
Included for pipeline completeness (fusion plants have non-zero fuel costs).

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/cas80_annualized_fuel.py:14
*Last Updated**: 2026-02-01
"""

AUTO_IMPLEMENTED = True

from solar_battery_v2.modules.solarbatterylibrary.annualizedfuelcalc import AnnualizedFuelCalcInput


def run_annualizedfuelcalc(inputs: AnnualizedFuelCalcInput) -> float:
    """Execute AnnualizedFuelCalc calculation.

Annualized fuel cost.
For solar: fuel_unit_cost = 0, fuel_consumption = 0 → annual_fuel_cost = 0.
Included for pipeline completeness (fusion plants have non-zero fuel costs).

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/cas80_annualized_fuel.py:14
*Last Updated**: 2026-02-01

SysML Source: models/tests/solar_battery/library.sysml:298

SysML Expressions:
    annual_fuel_cost = fuel_unit_cost * fuel_consumption
    
Documentation:
Annualized fuel cost.
For solar: fuel_unit_cost = 0, fuel_consumption = 0 → annual_fuel_cost = 0.
Included for pipeline completeness (fusion plants have non-zero fuel costs).

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/cas80_annualized_fuel.py:14
*Last Updated**: 2026-02-01

Args:
    inputs: Input parameters validated against AnnualizedFuelCalcInput schema

Returns:
    float: annual_fuel_cost

Example:
    >>> inputs = AnnualizedFuelCalcInput(...)
    >>> result = run_annualizedfuelcalc(inputs)
    """
    return (inputs.fuel_unit_cost * inputs.fuel_consumption)
