"""Auto-generated implementation for PVModuleCostCalc.

AUTO_IMPLEMENTED = True

SysML Source: models/tests/solar_battery/library.sysml:27

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
"""

AUTO_IMPLEMENTED = True

from solar_battery_v5.modules.solarbatterylibrary.pvmodulecostcalc import PVModuleCostCalcInput


def run_pvmodulecostcalc(inputs: PVModuleCostCalcInput) -> tuple[float, float, float, float, float]:
    """Execute PVModuleCostCalc calculation.

Cost calculation for photovoltaic modules.
Material cost driven by wattage and cost per watt.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

SysML Source: models/tests/solar_battery/library.sysml:27

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
    """
    material_cost = (inputs.wattage * inputs.cost_per_watt)
    fab_cost = (material_cost * inputs.fab_factor)
    install_cost = (material_cost * inputs.install_factor)
    total_cost = ((material_cost + fab_cost) + install_cost)
    idiot_index = (total_cost / material_cost)
    return (
        material_cost,
        fab_cost,
        install_cost,
        total_cost,
        idiot_index,
    )
