"""Auto-generated implementation for BatteryPackCostCalc.

AUTO_IMPLEMENTED = True

SysML Source: models/tests/solar_battery/library.sysml:96

SysML Expressions:
    cost_per_kwh = 171.5
    fab_factor = 0.45
    install_factor = 0.3
    material_cost = capacity_kwh * cost_per_kwh * chemistry_factor
    fab_cost = material_cost * fab_factor
    install_cost = material_cost * install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    
Documentation:
Cost calculation for battery packs.
Material cost driven by capacity and chemistry factor.

*Source**: Battery industry cost modeling
*Last Updated**: 2026-02-01
"""

AUTO_IMPLEMENTED = True

from solar_battery_v2.modules.solarbatterylibrary.batterypackcostcalc import BatteryPackCostCalcInput


def run_batterypackcostcalc(inputs: BatteryPackCostCalcInput) -> tuple[float, float, float, float, float]:
    """Execute BatteryPackCostCalc calculation.

Cost calculation for battery packs.
Material cost driven by capacity and chemistry factor.

*Source**: Battery industry cost modeling
*Last Updated**: 2026-02-01

SysML Source: models/tests/solar_battery/library.sysml:96

SysML Expressions:
    cost_per_kwh = 171.5
    fab_factor = 0.45
    install_factor = 0.3
    material_cost = capacity_kwh * cost_per_kwh * chemistry_factor
    fab_cost = material_cost * fab_factor
    install_cost = material_cost * install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    
Documentation:
Cost calculation for battery packs.
Material cost driven by capacity and chemistry factor.

*Source**: Battery industry cost modeling
*Last Updated**: 2026-02-01

Args:
    inputs: Input parameters validated against BatteryPackCostCalcInput schema

Returns:
    tuple[float, ...]: (material_cost, fab_cost, install_cost, total_cost, idiot_index)

Example:
    >>> inputs = BatteryPackCostCalcInput(...)
    >>> material_cost, fab_cost, install_cost, total_cost, idiot_index = run_batterypackcostcalc(inputs)
    """
    material_cost = ((inputs.capacity_kwh * inputs.cost_per_kwh) * inputs.chemistry_factor)
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
