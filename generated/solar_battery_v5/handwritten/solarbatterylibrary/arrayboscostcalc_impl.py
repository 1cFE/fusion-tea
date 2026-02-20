"""Auto-generated implementation for ArrayBOSCostCalc.

AUTO_IMPLEMENTED = True

SysML Source: models/tests/solar_battery/library.sysml:72

SysML Expressions:
    cost_per_string = LiteralRationalEvaluation()
    cost_per_panel_bos = LiteralRationalEvaluation()
    fab_factor = LiteralRationalEvaluation()
    install_factor = LiteralRationalEvaluation()
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
"""

AUTO_IMPLEMENTED = True

from solar_battery_v5.modules.solarbatterylibrary.arrayboscostcalc import ArrayBOSCostCalcInput


def run_arrayboscostcalc(inputs: ArrayBOSCostCalcInput) -> tuple[float, float, float, float, float]:
    """Execute ArrayBOSCostCalc calculation.

Cost calculation for solar array balance-of-system.
Includes combiners, disconnects, conduit per string and per panel.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

SysML Source: models/tests/solar_battery/library.sysml:72

SysML Expressions:
    cost_per_string = LiteralRationalEvaluation()
    cost_per_panel_bos = LiteralRationalEvaluation()
    fab_factor = LiteralRationalEvaluation()
    install_factor = LiteralRationalEvaluation()
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
    """
    material_cost = ((inputs.string_count * inputs.cost_per_string) + (inputs.panel_count * inputs.cost_per_panel_bos))
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
