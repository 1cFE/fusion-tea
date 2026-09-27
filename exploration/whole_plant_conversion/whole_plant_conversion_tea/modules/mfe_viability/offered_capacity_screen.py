"""Offered_Capacity_ScreenModule Module Wrapper

TEAx module for Offered_Capacity_Screen calculation.

Strict rating minus demand at separately checked offered conditions. The guarded native completion rejects nonfinite/negative ratings and active demands, reports undefined if inactive, unsupported or demand unavailable, and never snaps margins. No equipment qualification is implied. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: round2/architecture-review.md; entering-model checkpoint 53a0366a. **Basis**: [AGENT] assumed offered capability at declared conditions; captured design, not vendor qualification. **Last Updated**: 2026-09-20

Inputs:
    - applicable_in: applicable_in parameter
    - demand_available_in: demand_available_in parameter
    - conditions_supported_in: conditions_supported_in parameter
    - rating_in: rating_in parameter
    - demand_in: demand_in parameter

Outputs:
    - evaluation_defined: evaluation_defined result
    - margin: margin result
    - applicable: applicable result
    - supported: supported result
    - capacity_ok: capacity_ok result

SysML Source: root-0/mfe_viability.sysml:106

SysML Source: root-0/mfe_viability.sysml:106

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_viability/offered_capacity_screen_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.primitives import Float
from whole_plant_conversion_tea.schemas.offered_capacity_screen_output import Offered_Capacity_ScreenOutput


class Offered_Capacity_ScreenInput(BaseModel):
    """Input model for Offered_Capacity_ScreenModule.

    Attributes:
        applicable_in: applicable_in input
        demand_available_in: demand_available_in input
        conditions_supported_in: conditions_supported_in input
        rating_in: rating_in input
        demand_in: demand_in input
    """
    applicable_in: bool = Field(..., description="applicable_in input")
    demand_available_in: bool = Field(..., description="demand_available_in input")
    conditions_supported_in: bool = Field(..., description="conditions_supported_in input")
    rating_in: float = Field(..., description="rating_in input")
    demand_in: float = Field(..., description="demand_in input")


class Offered_Capacity_ScreenModule(ModuleBase[Offered_Capacity_ScreenInput, Offered_Capacity_ScreenOutput]):
    """TEAx module for Offered_Capacity_Screen calculation.

Strict rating minus demand at separately checked offered conditions. The guarded native completion rejects nonfinite/negative ratings and active demands, reports undefined if inactive, unsupported or demand unavailable, and never snaps margins. No equipment qualification is implied. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: round2/architecture-review.md; entering-model checkpoint 53a0366a. **Basis**: [AGENT] assumed offered capability at declared conditions; captured design, not vendor qualification. **Last Updated**: 2026-09-20

Inputs:
    - applicable_in: applicable_in parameter
    - demand_available_in: demand_available_in parameter
    - conditions_supported_in: conditions_supported_in parameter
    - rating_in: rating_in parameter
    - demand_in: demand_in parameter

Outputs:
    - evaluation_defined: evaluation_defined result
    - margin: margin result
    - applicable: applicable result
    - supported: supported result
    - capacity_ok: capacity_ok result

SysML Source: root-0/mfe_viability.sysml:106

    SysML Source: root-0/mfe_viability.sysml:106

    Calculation Specification:
        See documentation:
Strict rating minus demand at separately checked offered conditions. The guarded native completion rejects nonfinite/negative ratings and active demands, reports undefined if inactive, unsupported or demand unavailable, and never snaps margins. No equipment qualification is implied. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: round2/architecture-review.md; entering-model checkpoint 53a0366a. **Basis**: [AGENT] assumed offered capability at declared conditions; captured design, not vendor qualification. **Last Updated**: 2026-09-20

    IMPLEMENTATION: See whole_plant_conversion_tea.handwritten.mfe_viability.offered_capacity_screen_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts evaluation_defined, margin, applicable, supported, capacity_ok fields to separate channels.
    """

    name: str = "Offered_Capacity_ScreenModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, applicable_in: bool, demand_available_in: bool, conditions_supported_in: bool, rating_in: float, demand_in: float    ) -> Offered_Capacity_ScreenInput:
        """Validate inputs and fill defaults.

        Args:
            applicable_in: applicable_in input
            demand_available_in: demand_available_in input
            conditions_supported_in: conditions_supported_in input
            rating_in: rating_in input
            demand_in: demand_in input

        Returns:
            Validated input model
        """
        return Offered_Capacity_ScreenInput(applicable_in=applicable_in, demand_available_in=demand_available_in, conditions_supported_in=conditions_supported_in, rating_in=rating_in, demand_in=demand_in)

    def run(
        self, applicable_in: bool, demand_available_in: bool, conditions_supported_in: bool, rating_in: float, demand_in: float    ) -> ModuleResult[Offered_Capacity_ScreenOutput]:
        """Execute calculation.

        Args:
            applicable_in: applicable_in input
            demand_available_in: demand_available_in input
            conditions_supported_in: conditions_supported_in input
            rating_in: rating_in input
            demand_in: demand_in input

        Returns:
            Module result with Offered_Capacity_ScreenOutput (evaluation_defined, margin, applicable, supported, capacity_ok)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(applicable_in, demand_available_in, conditions_supported_in, rating_in, demand_in)

        # Import handwritten implementation
        from whole_plant_conversion_tea.handwritten.mfe_viability.offered_capacity_screen_impl import (
            run_offered_capacity_screen,
        )

        # Execute implementation - returns tuple of values
        evaluation_defined, margin, applicable, supported, capacity_ok = run_offered_capacity_screen(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Offered_Capacity_ScreenOutput(
                evaluation_defined=evaluation_defined,
                margin=margin,
                applicable=applicable,
                supported=supported,
                capacity_ok=capacity_ok,
            )
        )
