"""Replacement_EventsModule Module Wrapper

TEAx module for Replacement_Events calculation.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

Inputs:
    - life_fpy_in: life_fpy_in parameter
    - plant_years_in: plant_years_in parameter
    - availability_in: availability_in parameter
    - event_cost_in: event_cost_in parameter

Outputs:
    - lifetime_total: lifetime_total result
    - interval_years: interval_years result
    - event_cost: event_cost result
    - last_event_year: last_event_year result
    - annual_reserve: annual_reserve result
    - first_event_year: first_event_year result
    - event_count: event_count result

SysML Source: root-0/integrated_equipment_costs.sysml:66

SysML Source: root-0/integrated_equipment_costs.sysml:66

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/integrated_equipment_costs/replacement_events_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from aries_integrated.primitives import Float
from aries_integrated.schemas.replacement_events_output import Replacement_EventsOutput


class Replacement_EventsInput(BaseModel):
    """Input model for Replacement_EventsModule.

    Attributes:
        life_fpy_in: life_fpy_in input
        plant_years_in: plant_years_in input
        availability_in: availability_in input
        event_cost_in: event_cost_in input
    """
    life_fpy_in: float = Field(..., description="life_fpy_in input")
    plant_years_in: float = Field(..., description="plant_years_in input")
    availability_in: float = Field(..., description="availability_in input")
    event_cost_in: float = Field(..., description="event_cost_in input")


class Replacement_EventsModule(ModuleBase[Replacement_EventsInput, Replacement_EventsOutput]):
    """TEAx module for Replacement_Events calculation.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

Inputs:
    - life_fpy_in: life_fpy_in parameter
    - plant_years_in: plant_years_in parameter
    - availability_in: availability_in parameter
    - event_cost_in: event_cost_in parameter

Outputs:
    - lifetime_total: lifetime_total result
    - interval_years: interval_years result
    - event_cost: event_cost result
    - last_event_year: last_event_year result
    - annual_reserve: annual_reserve result
    - first_event_year: first_event_year result
    - event_count: event_count result

SysML Source: root-0/integrated_equipment_costs.sysml:66

    SysML Source: root-0/integrated_equipment_costs.sysml:66

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

    IMPLEMENTATION: See aries_integrated.handwritten.integrated_equipment_costs.replacement_events_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts lifetime_total, interval_years, event_cost, last_event_year, annual_reserve, first_event_year, event_count fields to separate channels.
    """

    name: str = "Replacement_EventsModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, life_fpy_in: float, plant_years_in: float, availability_in: float, event_cost_in: float    ) -> Replacement_EventsInput:
        """Validate inputs and fill defaults.

        Args:
            life_fpy_in: life_fpy_in input
            plant_years_in: plant_years_in input
            availability_in: availability_in input
            event_cost_in: event_cost_in input

        Returns:
            Validated input model
        """
        return Replacement_EventsInput(life_fpy_in=life_fpy_in, plant_years_in=plant_years_in, availability_in=availability_in, event_cost_in=event_cost_in)

    def run(
        self, life_fpy_in: float, plant_years_in: float, availability_in: float, event_cost_in: float    ) -> ModuleResult[Replacement_EventsOutput]:
        """Execute calculation.

        Args:
            life_fpy_in: life_fpy_in input
            plant_years_in: plant_years_in input
            availability_in: availability_in input
            event_cost_in: event_cost_in input

        Returns:
            Module result with Replacement_EventsOutput (lifetime_total, interval_years, event_cost, last_event_year, annual_reserve, first_event_year, event_count)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(life_fpy_in, plant_years_in, availability_in, event_cost_in)

        # Import handwritten implementation
        from aries_integrated.handwritten.integrated_equipment_costs.replacement_events_impl import (
            run_replacement_events,
        )

        # Execute implementation - returns tuple of values
        lifetime_total, interval_years, event_cost, last_event_year, annual_reserve, first_event_year, event_count = run_replacement_events(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Replacement_EventsOutput(
                lifetime_total=lifetime_total,
                interval_years=interval_years,
                event_cost=event_cost,
                last_event_year=last_event_year,
                annual_reserve=annual_reserve,
                first_event_year=first_event_year,
                event_count=event_count,
            )
        )
