from solar_battery_tea.modules.solarbatterylibrary.energyproductioncalc import EnergyProductionCalcInput


def run_energyproductioncalc(inputs: EnergyProductionCalcInput) -> float:
    """Execute EnergyProductionCalc calculation.

Annual energy production calculation.
Matches PyFECONS lcoe.py denominator: 8760 * p_net * n_mod * plant_availability.

*Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/calculations/lcoe.py:24
*Last Updated**: 2026-02-01

SysML Source: solar_battery_model/library.sysml:267

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

    Implementation Pattern:
        # Extract input fields from the validated Input model:
        p_net_mw = inputs.p_net_mw
        n_mod = inputs.n_mod
        plant_availability = inputs.plant_availability
        # Perform calculation using extracted values
        # Return result(s)
    """
    # library.sysml:280
    return 8760.0 * inputs.p_net_mw * inputs.n_mod * inputs.plant_availability
