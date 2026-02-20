"""Auto-generated implementation for EnergyProductionCalc.

AUTO_IMPLEMENTED = True

SysML Source: models/tests/solar_battery/library.sysml:267

SysML Expressions:
    annual_energy_mwh = LiteralRationalEvaluation() * p_net_mw * n_mod * plant_availability
    
Documentation:
Annual energy production calculation.
Matches PyFECONS lcoe.py denominator: 8760 * p_net * n_mod * plant_availability.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/lcoe.py:24
*Last Updated**: 2026-02-01
"""

AUTO_IMPLEMENTED = True

from solar_battery_v5.modules.solarbatterylibrary.energyproductioncalc import EnergyProductionCalcInput


def run_energyproductioncalc(inputs: EnergyProductionCalcInput) -> float:
    """Execute EnergyProductionCalc calculation.

Annual energy production calculation.
Matches PyFECONS lcoe.py denominator: 8760 * p_net * n_mod * plant_availability.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/lcoe.py:24
*Last Updated**: 2026-02-01

SysML Source: models/tests/solar_battery/library.sysml:267

SysML Expressions:
    annual_energy_mwh = LiteralRationalEvaluation() * p_net_mw * n_mod * plant_availability
    
Documentation:
Annual energy production calculation.
Matches PyFECONS lcoe.py denominator: 8760 * p_net * n_mod * plant_availability.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/lcoe.py:24
*Last Updated**: 2026-02-01

Args:
    inputs: Input parameters validated against EnergyProductionCalcInput schema

Returns:
    float: annual_energy_mwh

Example:
    >>> inputs = EnergyProductionCalcInput(...)
    >>> result = run_energyproductioncalc(inputs)
    """
    return (((8760.0 * inputs.p_net_mw) * inputs.n_mod) * inputs.plant_availability)
