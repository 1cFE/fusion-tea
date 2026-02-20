"""Auto-generated implementation for HybridInverterCostCalc.

AUTO_IMPLEMENTED = True

SysML Source: models/tests/solar_battery/library.sysml:119

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
Cost calculation for hybrid (bidirectional) inverters.
Material cost driven by power rating.

*Source**: Battery industry cost modeling
*Last Updated**: 2026-02-01
"""

AUTO_IMPLEMENTED = True

from solar_battery_v5.modules.solarbatterylibrary.hybridinvertercostcalc import HybridInverterCostCalcInput


def run_hybridinvertercostcalc(inputs: HybridInverterCostCalcInput) -> tuple[float, float, float, float, float]:
    """Execute HybridInverterCostCalc calculation.

Cost calculation for hybrid (bidirectional) inverters.
Material cost driven by power rating.

*Source**: Battery industry cost modeling
*Last Updated**: 2026-02-01

SysML Source: models/tests/solar_battery/library.sysml:119

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
Cost calculation for hybrid (bidirectional) inverters.
Material cost driven by power rating.

*Source**: Battery industry cost modeling
*Last Updated**: 2026-02-01

Args:
    inputs: Input parameters validated against HybridInverterCostCalcInput schema

Returns:
    tuple[float, ...]: (material_cost, fab_cost, install_cost, total_cost, idiot_index)

Example:
    >>> inputs = HybridInverterCostCalcInput(...)
    >>> material_cost, fab_cost, install_cost, total_cost, idiot_index = run_hybridinvertercostcalc(inputs)
    """
    material_cost = (inputs.power_rating * inputs.cost_per_watt)
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
