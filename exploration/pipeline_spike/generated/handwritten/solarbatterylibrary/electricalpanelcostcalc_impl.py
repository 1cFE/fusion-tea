from solar_battery_tea.modules.solarbatterylibrary.electricalpanelcostcalc import ElectricalPanelCostCalcInput


def run_electricalpanelcostcalc(inputs: ElectricalPanelCostCalcInput) -> tuple[float, float, float, float, float]:
    """Execute ElectricalPanelCostCalc calculation.

Cost calculation for electrical panel and breakers.
Base cost plus per-circuit cost.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

SysML Source: solar_battery_model/library.sysml:187

SysML Expressions:
    base_cost = LiteralRationalEvaluation()
    cost_per_circuit = LiteralRationalEvaluation()
    fab_factor = LiteralRationalEvaluation()
    install_factor = LiteralRationalEvaluation()
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

    Implementation Pattern:
        # Extract input fields from the validated Input model:
        circuit_count = inputs.circuit_count
        base_cost = inputs.base_cost
        cost_per_circuit = inputs.cost_per_circuit
        fab_factor = inputs.fab_factor
        install_factor = inputs.install_factor
        # Perform calculation using extracted values
        # Return result(s)
    """
    # library.sysml:203-207
    material_cost = inputs.base_cost + inputs.circuit_count * inputs.cost_per_circuit
    fab_cost = material_cost * inputs.fab_factor
    install_cost = material_cost * inputs.install_factor
    total_cost = material_cost + fab_cost + install_cost
    idiot_index = total_cost / material_cost
    return (material_cost, fab_cost, install_cost, total_cost, idiot_index)
