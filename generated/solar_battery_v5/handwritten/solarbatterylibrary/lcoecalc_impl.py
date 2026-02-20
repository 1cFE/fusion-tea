"""Auto-generated implementation for LCOECalc.

AUTO_IMPLEMENTED = True

SysML Source: models/tests/solar_battery/library.sysml:335

SysML Expressions:
    lcoe_per_mwh = annualized_capital_cost + annual_om_cost + annual_fuel_cost * LiteralRationalEvaluation() + yearly_inflation ** plant_lifetime / annual_energy_mwh
    
Documentation:
Levelized Cost of Electricity calculation.
Matches PyFECONS lcoe.py formula with inflation escalation on O&M and fuel.
LCOE = (C900000 + (C700000 + C800000) * (1 + inflation)^lifetime) / annual_energy

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/lcoe.py:18-25
*Last Updated**: 2026-02-01
"""

AUTO_IMPLEMENTED = True

from solar_battery_v5.modules.solarbatterylibrary.lcoecalc import LCOECalcInput


def run_lcoecalc(inputs: LCOECalcInput) -> float:
    """Execute LCOECalc calculation.

Levelized Cost of Electricity calculation.
Matches PyFECONS lcoe.py formula with inflation escalation on O&M and fuel.
LCOE = (C900000 + (C700000 + C800000) * (1 + inflation)^lifetime) / annual_energy

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/lcoe.py:18-25
*Last Updated**: 2026-02-01

SysML Source: models/tests/solar_battery/library.sysml:335

SysML Expressions:
    lcoe_per_mwh = annualized_capital_cost + annual_om_cost + annual_fuel_cost * LiteralRationalEvaluation() + yearly_inflation ** plant_lifetime / annual_energy_mwh
    
Documentation:
Levelized Cost of Electricity calculation.
Matches PyFECONS lcoe.py formula with inflation escalation on O&M and fuel.
LCOE = (C900000 + (C700000 + C800000) * (1 + inflation)^lifetime) / annual_energy

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/lcoe.py:18-25
*Last Updated**: 2026-02-01

Args:
    inputs: Input parameters validated against LCOECalcInput schema

Returns:
    float: lcoe_per_mwh

Example:
    >>> inputs = LCOECalcInput(...)
    >>> result = run_lcoecalc(inputs)
    """
    return ((inputs.annualized_capital_cost + ((inputs.annual_om_cost + inputs.annual_fuel_cost) * ((1.0 + inputs.yearly_inflation) ** inputs.plant_lifetime))) / inputs.annual_energy_mwh)
