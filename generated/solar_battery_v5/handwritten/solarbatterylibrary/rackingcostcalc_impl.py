"""Auto-generated implementation for RackingCostCalc.

AUTO_IMPLEMENTED = True

SysML Source: models/tests/solar_battery/library.sysml:163

SysML Expressions:
    cost_per_panel_rack = LiteralRationalEvaluation()
    fab_factor = LiteralRationalEvaluation()
    install_factor = LiteralRationalEvaluation()
    material_cost = panel_count * cost_per_panel_rack
    fab_cost = material_cost * fab_factor
    install_cost = material_cost * install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    
Documentation:
Cost calculation for racking and mounting hardware.
Material cost driven by panel count. Tilt angle is a design parameter
but does not affect cost in this simplified model.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01
"""

AUTO_IMPLEMENTED = True

from solar_battery_v5.modules.solarbatterylibrary.rackingcostcalc import RackingCostCalcInput


def run_rackingcostcalc(inputs: RackingCostCalcInput) -> tuple[float, float, float, float, float]:
    """Execute RackingCostCalc calculation.

Cost calculation for racking and mounting hardware.
Material cost driven by panel count. Tilt angle is a design parameter
but does not affect cost in this simplified model.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

SysML Source: models/tests/solar_battery/library.sysml:163

SysML Expressions:
    cost_per_panel_rack = LiteralRationalEvaluation()
    fab_factor = LiteralRationalEvaluation()
    install_factor = LiteralRationalEvaluation()
    material_cost = panel_count * cost_per_panel_rack
    fab_cost = material_cost * fab_factor
    install_cost = material_cost * install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    
Documentation:
Cost calculation for racking and mounting hardware.
Material cost driven by panel count. Tilt angle is a design parameter
but does not affect cost in this simplified model.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

Args:
    inputs: Input parameters validated against RackingCostCalcInput schema

Returns:
    tuple[float, ...]: (material_cost, fab_cost, install_cost, total_cost, idiot_index)

Example:
    >>> inputs = RackingCostCalcInput(...)
    >>> material_cost, fab_cost, install_cost, total_cost, idiot_index = run_rackingcostcalc(inputs)
    """
    material_cost = (inputs.panel_count * inputs.cost_per_panel_rack)
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
