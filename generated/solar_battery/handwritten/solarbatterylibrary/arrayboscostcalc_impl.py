from solar_battery.modules.solarbatterylibrary.arrayboscostcalc import ArrayBOSCostCalcInput


def run_arrayboscostcalc(inputs: ArrayBOSCostCalcInput) -> tuple[float, float, float, float, float]:
    """Execute ArrayBOSCostCalc calculation.

Cost calculation for solar array balance-of-system.
Includes combiners, disconnects, conduit per string and per panel.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

SysML Source: models/tests/solar_battery/library.sysml:72

SysML Expressions:
    material_cost = string_count * cost_per_string + panel_count * cost_per_panel_bos
    fab_cost = material_cost * fab_factor
    install_cost = material_cost * install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    
Documentation:
Cost calculation for solar array balance-of-system.
Includes combiners, disconnects, conduit per string and per panel.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

Args:
    inputs: Input parameters validated against ArrayBOSCostCalcInput schema

Returns:
    tuple[float, ...]: (material_cost, fab_cost, install_cost, total_cost, idiot_index)

Example:
    >>> inputs = ArrayBOSCostCalcInput(...)
    >>> material_cost, fab_cost, install_cost, total_cost, idiot_index = run_arrayboscostcalc(inputs)

    Implementation Pattern:
        # Extract input fields from the validated Input model:
        string_count = inputs.string_count
        panel_count = inputs.panel_count
        cost_per_string = inputs.cost_per_string
        cost_per_panel_bos = inputs.cost_per_panel_bos
        fab_factor = inputs.fab_factor
        install_factor = inputs.install_factor
        # Perform calculation using extracted values
        # Return result(s)
    """
    raise NotImplementedError(
        "Manual implementation required for ArrayBOSCostCalc. "
        "See SysML source: models/tests/solar_battery/library.sysml:72"
    )
