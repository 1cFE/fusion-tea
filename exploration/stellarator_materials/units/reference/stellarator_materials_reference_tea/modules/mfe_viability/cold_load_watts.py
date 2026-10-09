"""Cold_Load_WattsModule Module Wrapper

TEAx module for Cold_Load_Watts calculation.

Cold load W = cold_MW * 1000000; fixed unit conversion. Finite active arithmetic is guarded. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: MR-7 conditional rating contract. **Last Updated**: 2026-09-20

Inputs:
    - cold_MW_in: cold_MW_in parameter

Outputs:
    - demand: demand result

SysML Source: root-0/analyses/mfe_viability.sysml:87

SysML Source: root-0/analyses/mfe_viability.sysml:87

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_viability/cold_load_watts_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_reference_tea.primitives import Float


class Cold_Load_WattsInput(BaseModel):
    """Input model for Cold_Load_WattsModule.

    Attributes:
        cold_MW_in: cold_MW_in input
    """
    cold_MW_in: float = Field(..., description="cold_MW_in input")


class Cold_Load_WattsModule(ModuleBase[Cold_Load_WattsInput, Float]):
    """TEAx module for Cold_Load_Watts calculation.

Cold load W = cold_MW * 1000000; fixed unit conversion. Finite active arithmetic is guarded. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: MR-7 conditional rating contract. **Last Updated**: 2026-09-20

Inputs:
    - cold_MW_in: cold_MW_in parameter

Outputs:
    - demand: demand result

SysML Source: root-0/analyses/mfe_viability.sysml:87

    SysML Source: root-0/analyses/mfe_viability.sysml:87

    Calculation Specification:
        See documentation:
Cold load W = cold_MW * 1000000; fixed unit conversion. Finite active arithmetic is guarded. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: MR-7 conditional rating contract. **Last Updated**: 2026-09-20

    IMPLEMENTATION: See stellarator_materials_reference_tea.handwritten.mfe_viability.cold_load_watts_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Cold_Load_WattsModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, cold_MW_in: float    ) -> Cold_Load_WattsInput:
        """Validate inputs and fill defaults.

        Args:
            cold_MW_in: cold_MW_in input

        Returns:
            Validated input model
        """
        return Cold_Load_WattsInput(cold_MW_in=cold_MW_in)

    def run(
        self, cold_MW_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            cold_MW_in: cold_MW_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(cold_MW_in)

        # Import handwritten implementation
        from stellarator_materials_reference_tea.handwritten.mfe_viability.cold_load_watts_impl import (
            run_cold_load_watts,
        )

        # Execute implementation - returns single value
        demand = run_cold_load_watts(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(demand))
