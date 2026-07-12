from solar_battery_tea.modules.solarbatterylibrary.invertercostcalc import InverterCostCalcInput


def run_invertercostcalc(inputs: InverterCostCalcInput) -> tuple[float, float, float, float, float]:
    """Execute InverterCostCalc calculation.

Cost calculation for string inverters.
Material cost driven by power rating.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

SysML Source: solar_battery_model/library.sysml:50

SysML Expressions:
    cost_per_watt = LiteralRationalEvaluation()
    fab_factor = LiteralRationalEvaluation()
    install_factor = LiteralRationalEvaluation()
    material_cost = power_rating * cost_per_watt
    fab_cost = material_cost * fab_factor
    install_cost = material_cost * install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    
Documentation:
Cost calculation for string inverters.
Material cost driven by power rating.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

Args:
    inputs: Input parameters validated against InverterCostCalcInput schema

Returns:
    tuple[float, ...]: (material_cost, fab_cost, install_cost, total_cost, idiot_index)

Example:
    >>> inputs = InverterCostCalcInput(...)
    >>> material_cost, fab_cost, install_cost, total_cost, idiot_index = run_invertercostcalc(inputs)

    Implementation Pattern:
        # Extract input fields from the validated Input model:
        power_rating = inputs.power_rating
        cost_per_watt = inputs.cost_per_watt
        fab_factor = inputs.fab_factor
        install_factor = inputs.install_factor
        # Perform calculation using extracted values
        # Return result(s)
    """
    # library.sysml:65-69
    material_cost = inputs.power_rating * inputs.cost_per_watt
    fab_cost = material_cost * inputs.fab_factor
    install_cost = material_cost * inputs.install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    return (material_cost, fab_cost, install_cost, total_cost, idiot_index)
