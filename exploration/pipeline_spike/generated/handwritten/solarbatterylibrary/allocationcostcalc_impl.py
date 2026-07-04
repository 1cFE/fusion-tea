from solar_battery_tea.modules.solarbatterylibrary.allocationcostcalc import AllocationCostCalcInput


def run_allocationcostcalc(inputs: AllocationCostCalcInput) -> tuple[float, float, float, float, float]:
    """Execute AllocationCostCalc calculation.

Bundled allocation costs for assembly-level minor items.
Covers items not modeled as separate parts: fasteners, seals, wiring.

Duplicated from coffee maker (CoffeeMakerLibrary) — not shared because
the coffee maker uses a local 'Costed Component' interface.

*Pattern**: Rule R3 from strategic cost patterns
*Reference**: models/tests/coffee_maker/library.sysml:195-220
*Last Updated**: 2026-02-01

SysML Source: solar_battery_model/library.sysml:235

SysML Expressions:
    fastener_cost_per_child = LiteralRationalEvaluation()
    seal_cost_per_child = LiteralRationalEvaluation()
    wiring_cost_per_kg = LiteralRationalEvaluation()
    fastener_cost = child_count * fastener_cost_per_child
    seal_cost = child_count * seal_cost_per_child
    wiring_cost = total_child_mass * wiring_cost_per_kg
    total_allocation = fastener_cost + seal_cost + wiring_cost
    material_portion = total_allocation * LiteralRationalEvaluation()
    
Documentation:
Bundled allocation costs for assembly-level minor items.
Covers items not modeled as separate parts: fasteners, seals, wiring.

Duplicated from coffee maker (CoffeeMakerLibrary) — not shared because
the coffee maker uses a local 'Costed Component' interface.

*Pattern**: Rule R3 from strategic cost patterns
*Reference**: models/tests/coffee_maker/library.sysml:195-220
*Last Updated**: 2026-02-01

Args:
    inputs: Input parameters validated against AllocationCostCalcInput schema

Returns:
    tuple[float, ...]: (fastener_cost, seal_cost, wiring_cost, total_allocation, material_portion)

Example:
    >>> inputs = AllocationCostCalcInput(...)
    >>> fastener_cost, seal_cost, wiring_cost, total_allocation, material_portion = run_allocationcostcalc(inputs)

    Implementation Pattern:
        # Extract input fields from the validated Input model:
        child_count = inputs.child_count
        total_child_mass = inputs.total_child_mass
        fastener_cost_per_child = inputs.fastener_cost_per_child
        seal_cost_per_child = inputs.seal_cost_per_child
        wiring_cost_per_kg = inputs.wiring_cost_per_kg
        # Perform calculation using extracted values
        # Return result(s)
    """
    # library.sysml:255-260
    fastener_cost = inputs.child_count * inputs.fastener_cost_per_child
    seal_cost = inputs.child_count * inputs.seal_cost_per_child
    wiring_cost = inputs.total_child_mass * inputs.wiring_cost_per_kg
    total_allocation = fastener_cost + seal_cost + wiring_cost
    material_portion = total_allocation * 0.8
    return (fastener_cost, seal_cost, wiring_cost, total_allocation, material_portion)
