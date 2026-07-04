from solar_battery_tea.modules.solarbatterylibrary.pvmodulecostcalc import PVModuleCostCalcInput


def run_pvmodulecostcalc(inputs: PVModuleCostCalcInput) -> tuple[float, float, float, float, float]:
    """Execute PVModuleCostCalc calculation.

Cost calculation for photovoltaic modules.
Material cost driven by wattage and cost per watt.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

SysML Source: solar_battery_model/library.sysml:27

SysML Expressions:
    cost_per_watt = LiteralRationalEvaluation()
    fab_factor = LiteralRationalEvaluation()
    install_factor = LiteralRationalEvaluation()
    material_cost = wattage * cost_per_watt
    fab_cost = material_cost * fab_factor
    install_cost = material_cost * install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    
Documentation:
Cost calculation for photovoltaic modules.
Material cost driven by wattage and cost per watt.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

Args:
    inputs: Input parameters validated against PVModuleCostCalcInput schema

Returns:
    tuple[float, ...]: (material_cost, fab_cost, install_cost, total_cost, idiot_index)

Example:
    >>> inputs = PVModuleCostCalcInput(...)
    >>> material_cost, fab_cost, install_cost, total_cost, idiot_index = run_pvmodulecostcalc(inputs)

    Implementation Pattern:
        # Extract input fields from the validated Input model:
        wattage = inputs.wattage
        efficiency = inputs.efficiency
        cost_per_watt = inputs.cost_per_watt
        fab_factor = inputs.fab_factor
        install_factor = inputs.install_factor
        # Perform calculation using extracted values
        # Return result(s)
    """
    # library.sysml:43-47
    material_cost = inputs.wattage * inputs.cost_per_watt
    fab_cost = material_cost * inputs.fab_factor
    install_cost = material_cost * inputs.install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    return (material_cost, fab_cost, install_cost, total_cost, idiot_index)
