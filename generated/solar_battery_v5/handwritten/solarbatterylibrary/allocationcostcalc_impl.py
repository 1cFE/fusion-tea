"""Auto-generated implementation for AllocationCostCalc.

AUTO_IMPLEMENTED = True

SysML Source: models/tests/solar_battery/library.sysml:235

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
"""

AUTO_IMPLEMENTED = True

from solar_battery_v5.modules.solarbatterylibrary.allocationcostcalc import AllocationCostCalcInput


def run_allocationcostcalc(inputs: AllocationCostCalcInput) -> tuple[float, float, float, float, float]:
    """Execute AllocationCostCalc calculation.

Bundled allocation costs for assembly-level minor items.
Covers items not modeled as separate parts: fasteners, seals, wiring.

Duplicated from coffee maker (CoffeeMakerLibrary) — not shared because
the coffee maker uses a local 'Costed Component' interface.

*Pattern**: Rule R3 from strategic cost patterns
*Reference**: models/tests/coffee_maker/library.sysml:195-220
*Last Updated**: 2026-02-01

SysML Source: models/tests/solar_battery/library.sysml:235

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
    """
    fastener_cost = (inputs.child_count * inputs.fastener_cost_per_child)
    seal_cost = (inputs.child_count * inputs.seal_cost_per_child)
    wiring_cost = (inputs.total_child_mass * inputs.wiring_cost_per_kg)
    total_allocation = ((fastener_cost + seal_cost) + wiring_cost)
    material_portion = (total_allocation * 0.8)
    return (
        fastener_cost,
        seal_cost,
        wiring_cost,
        total_allocation,
        material_portion,
    )
