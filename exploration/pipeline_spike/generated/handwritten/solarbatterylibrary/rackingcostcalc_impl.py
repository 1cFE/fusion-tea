from solar_battery_tea.modules.solarbatterylibrary.rackingcostcalc import RackingCostCalcInput


def run_rackingcostcalc(inputs: RackingCostCalcInput) -> tuple[float, float, float, float, float]:
    """Execute RackingCostCalc calculation.

Cost calculation for racking and mounting hardware.
Material cost driven by panel count. Tilt angle is a design parameter
but does not affect cost in this simplified model.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

SysML Source: solar_battery_model/library.sysml:163

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

    Implementation Pattern:
        # Extract input fields from the validated Input model:
        panel_count = inputs.panel_count
        tilt_angle = inputs.tilt_angle
        cost_per_panel_rack = inputs.cost_per_panel_rack
        fab_factor = inputs.fab_factor
        install_factor = inputs.install_factor
        # Perform calculation using extracted values
        # Return result(s)
    """
    # library.sysml:180-184 (tilt_angle is a design parameter with no cost effect)
    material_cost = inputs.panel_count * inputs.cost_per_panel_rack
    fab_cost = material_cost * inputs.fab_factor
    install_cost = material_cost * inputs.install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    return (material_cost, fab_cost, install_cost, total_cost, idiot_index)
