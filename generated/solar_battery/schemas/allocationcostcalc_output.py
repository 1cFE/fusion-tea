from pydantic import Field
from simkit.config.schema import MultiOutput

class AllocationCostCalcOutput(MultiOutput):
    """Multi-output container for AllocationCostCalc.

Bundled allocation costs for assembly-level minor items.
Covers items not modeled as separate parts: fasteners, seals, wiring.

Duplicated from coffee maker (CoffeeMakerLibrary) — not shared because
the coffee maker uses a local 'Costed Component' interface.

*Pattern**: Rule R3 from strategic cost patterns
*Reference**: models/tests/coffee_maker/library.sysml:195-220
*Last Updated**: 2026-02-01

SysML Source: models/tests/solar_battery/library.sysml:235
    """
    fastener_cost: float = Field(description="fastener_cost output")
    seal_cost: float = Field(description="seal_cost output")
    wiring_cost: float = Field(description="wiring_cost output")
    total_allocation: float = Field(description="total_allocation output")
    material_portion: float = Field(description="material_portion output")
