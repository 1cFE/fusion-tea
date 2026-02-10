"""Auto-generated implementation for ElectricalPanelCostCalc.

AUTO_IMPLEMENTED = True

SysML Source: models/tests/solar_battery/library.sysml:187

SysML Expressions:
    base_cost = 150.0
    cost_per_circuit = 34.0
    fab_factor = 0.45
    install_factor = 0.3
    material_cost = base_cost + circuit_count * cost_per_circuit
    fab_cost = material_cost * fab_factor
    install_cost = material_cost * install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    
Documentation:
Cost calculation for electrical panel and breakers.
Base cost plus per-circuit cost.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01
"""

AUTO_IMPLEMENTED = True

from solar_battery_v2.modules.solarbatterylibrary.electricalpanelcostcalc import ElectricalPanelCostCalcInput


def run_electricalpanelcostcalc(inputs: ElectricalPanelCostCalcInput) -> tuple[float, float, float, float, float]:
    """Execute ElectricalPanelCostCalc calculation.

Cost calculation for electrical panel and breakers.
Base cost plus per-circuit cost.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

SysML Source: models/tests/solar_battery/library.sysml:187

SysML Expressions:
    base_cost = 150.0
    cost_per_circuit = 34.0
    fab_factor = 0.45
    install_factor = 0.3
    material_cost = base_cost + circuit_count * cost_per_circuit
    fab_cost = material_cost * fab_factor
    install_cost = material_cost * install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    
Documentation:
Cost calculation for electrical panel and breakers.
Base cost plus per-circuit cost.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

Args:
    inputs: Input parameters validated against ElectricalPanelCostCalcInput schema

Returns:
    tuple[float, ...]: (material_cost, fab_cost, install_cost, total_cost, idiot_index)

Example:
    >>> inputs = ElectricalPanelCostCalcInput(...)
    >>> material_cost, fab_cost, install_cost, total_cost, idiot_index = run_electricalpanelcostcalc(inputs)
    """
    material_cost = (inputs.base_cost + (inputs.circuit_count * inputs.cost_per_circuit))
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
