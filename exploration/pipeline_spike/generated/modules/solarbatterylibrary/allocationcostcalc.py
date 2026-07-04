"""AllocationCostCalcModule Module Wrapper

TEAx module for AllocationCostCalc calculation.

Bundled allocation costs for assembly-level minor items.
Covers items not modeled as separate parts: fasteners, seals, wiring.

Duplicated from coffee maker (CoffeeMakerLibrary) — not shared because
the coffee maker uses a local 'Costed Component' interface.

*Pattern**: Rule R3 from strategic cost patterns
*Reference**: models/tests/coffee_maker/library.sysml:195-220
*Last Updated**: 2026-02-01

Inputs:
    - child_count: child_count parameter
    - total_child_mass: total_child_mass parameter
    - fastener_cost_per_child: fastener_cost_per_child parameter
    - seal_cost_per_child: seal_cost_per_child parameter
    - wiring_cost_per_kg: wiring_cost_per_kg parameter

Outputs:
    - fastener_cost: fastener_cost result
    - seal_cost: seal_cost result
    - wiring_cost: wiring_cost result
    - total_allocation: total_allocation result
    - material_portion: material_portion result

SysML Source: solar_battery_model/library.sysml:235

SysML Source: solar_battery_model/library.sysml:235

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterylibrary/allocationcostcalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery_tea.primitives import Float
from solar_battery_tea.schemas.allocationcostcalc_output import AllocationCostCalcOutput


class AllocationCostCalcInput(BaseModel):
    """Input model for AllocationCostCalcModule.

    Attributes:
        child_count: child_count input
        total_child_mass: total_child_mass input
        fastener_cost_per_child: fastener_cost_per_child input
        seal_cost_per_child: seal_cost_per_child input
        wiring_cost_per_kg: wiring_cost_per_kg input
    """
    child_count: float = Field(..., description="child_count input")
    total_child_mass: float = Field(..., description="total_child_mass input")
    fastener_cost_per_child: float = Field(..., description="fastener_cost_per_child input")
    seal_cost_per_child: float = Field(..., description="seal_cost_per_child input")
    wiring_cost_per_kg: float = Field(..., description="wiring_cost_per_kg input")


class AllocationCostCalcModule(ModuleBase[AllocationCostCalcInput, AllocationCostCalcOutput]):
    """TEAx module for AllocationCostCalc calculation.

Bundled allocation costs for assembly-level minor items.
Covers items not modeled as separate parts: fasteners, seals, wiring.

Duplicated from coffee maker (CoffeeMakerLibrary) — not shared because
the coffee maker uses a local 'Costed Component' interface.

*Pattern**: Rule R3 from strategic cost patterns
*Reference**: models/tests/coffee_maker/library.sysml:195-220
*Last Updated**: 2026-02-01

Inputs:
    - child_count: child_count parameter
    - total_child_mass: total_child_mass parameter
    - fastener_cost_per_child: fastener_cost_per_child parameter
    - seal_cost_per_child: seal_cost_per_child parameter
    - wiring_cost_per_kg: wiring_cost_per_kg parameter

Outputs:
    - fastener_cost: fastener_cost result
    - seal_cost: seal_cost result
    - wiring_cost: wiring_cost result
    - total_allocation: total_allocation result
    - material_portion: material_portion result

SysML Source: solar_battery_model/library.sysml:235

    SysML Source: solar_battery_model/library.sysml:235

    Calculation Specification:
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

    IMPLEMENTATION: See solar_battery_tea.handwritten.solarbatterylibrary.allocationcostcalc_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts fastener_cost, seal_cost, wiring_cost, total_allocation, material_portion fields to separate channels.
    """

    name: str = "AllocationCostCalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, child_count: float, total_child_mass: float, fastener_cost_per_child: float, seal_cost_per_child: float, wiring_cost_per_kg: float    ) -> AllocationCostCalcInput:
        """Validate inputs and fill defaults.

        Args:
            child_count: child_count input
            total_child_mass: total_child_mass input
            fastener_cost_per_child: fastener_cost_per_child input
            seal_cost_per_child: seal_cost_per_child input
            wiring_cost_per_kg: wiring_cost_per_kg input

        Returns:
            Validated input model
        """
        return AllocationCostCalcInput(child_count=child_count, total_child_mass=total_child_mass, fastener_cost_per_child=fastener_cost_per_child, seal_cost_per_child=seal_cost_per_child, wiring_cost_per_kg=wiring_cost_per_kg)

    def run(
        self, child_count: float, total_child_mass: float, fastener_cost_per_child: float, seal_cost_per_child: float, wiring_cost_per_kg: float    ) -> ModuleResult[AllocationCostCalcOutput]:
        """Execute calculation.

        Args:
            child_count: child_count input
            total_child_mass: total_child_mass input
            fastener_cost_per_child: fastener_cost_per_child input
            seal_cost_per_child: seal_cost_per_child input
            wiring_cost_per_kg: wiring_cost_per_kg input

        Returns:
            Module result with AllocationCostCalcOutput (fastener_cost, seal_cost, wiring_cost, total_allocation, material_portion)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(child_count, total_child_mass, fastener_cost_per_child, seal_cost_per_child, wiring_cost_per_kg)

        # Import handwritten implementation
        from solar_battery_tea.handwritten.solarbatterylibrary.allocationcostcalc_impl import (
            run_allocationcostcalc,
        )

        # Execute implementation - returns tuple of values
        fastener_cost, seal_cost, wiring_cost, total_allocation, material_portion = run_allocationcostcalc(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=AllocationCostCalcOutput(
                fastener_cost=fastener_cost,
                seal_cost=seal_cost,
                wiring_cost=wiring_cost,
                total_allocation=total_allocation,
                material_portion=material_portion,
            )
        )
