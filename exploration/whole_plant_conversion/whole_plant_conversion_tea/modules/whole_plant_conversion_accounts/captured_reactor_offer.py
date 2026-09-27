"""Captured_Reactor_OfferModule Module Wrapper

TEAx module for Captured_Reactor_Offer calculation.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/captured_reactor_offer_impl.py; reviewed equations in design/configuration.

Inputs:
    - capture_id_in: capture_id_in parameter

Outputs:
    - nuclear_transport_qualified: nuclear_transport_qualified result
    - inventory_cold_W: inventory_cold_W result
    - identity_supported: identity_supported result
    - peak_field: peak_field result
    - cold_rating_W: cold_rating_W result
    - support_cost: support_cost result
    - cold_volume_m3: cold_volume_m3 result
    - intercept_temperature_K: intercept_temperature_K result
    - intercept_inventory_W: intercept_inventory_W result
    - turn_current_A: turn_current_A result
    - axis_field: axis_field result
    - strain_margin: strain_margin result
    - magnet_capital: magnet_capital result
    - cold_W: cold_W result
    - stress_margin_Pa: stress_margin_Pa result
    - current_margin: current_margin result
    - coil_drive_MW: coil_drive_MW result
    - material_cost: material_cost result
    - stress_Pa: stress_Pa result
    - intercept_W: intercept_W result
    - field_extrapolated: field_extrapolated result
    - cold_carnot_fraction: cold_carnot_fraction result
    - strain: strain result
    - fixed_cold_MW: fixed_cold_MW result
    - insulation_cost: insulation_cost result
    - cold_margin_W: cold_margin_W result
    - global_construction_qualified: global_construction_qualified result
    - intercept_carnot_fraction: intercept_carnot_fraction result
    - ambient_temperature_K: ambient_temperature_K result
    - winding_cost: winding_cost result
    - tape_cost: tape_cost result
    - field_margin_T: field_margin_T result
    - intercept_rating_W: intercept_rating_W result
    - fit_margin: fit_margin result
    - intercept_margin_W: intercept_margin_W result
    - cold_temperature_K: cold_temperature_K result
    - nuclear_heating_W_m3: nuclear_heating_W_m3 result
    - refrigeration_MW: refrigeration_MW result

SysML Source: root-0/whole_plant_conversion_accounts.sysml:14

SysML Source: root-0/whole_plant_conversion_accounts.sysml:14

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/whole_plant_conversion_accounts/captured_reactor_offer_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.primitives import Float
from whole_plant_conversion_tea.schemas.captured_reactor_offer_output import Captured_Reactor_OfferOutput


class Captured_Reactor_OfferInput(BaseModel):
    """Input model for Captured_Reactor_OfferModule.

    Attributes:
        capture_id_in: capture_id_in input
    """
    capture_id_in: float = Field(..., description="capture_id_in input")


class Captured_Reactor_OfferModule(ModuleBase[Captured_Reactor_OfferInput, Captured_Reactor_OfferOutput]):
    """TEAx module for Captured_Reactor_Offer calculation.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/captured_reactor_offer_impl.py; reviewed equations in design/configuration.

Inputs:
    - capture_id_in: capture_id_in parameter

Outputs:
    - nuclear_transport_qualified: nuclear_transport_qualified result
    - inventory_cold_W: inventory_cold_W result
    - identity_supported: identity_supported result
    - peak_field: peak_field result
    - cold_rating_W: cold_rating_W result
    - support_cost: support_cost result
    - cold_volume_m3: cold_volume_m3 result
    - intercept_temperature_K: intercept_temperature_K result
    - intercept_inventory_W: intercept_inventory_W result
    - turn_current_A: turn_current_A result
    - axis_field: axis_field result
    - strain_margin: strain_margin result
    - magnet_capital: magnet_capital result
    - cold_W: cold_W result
    - stress_margin_Pa: stress_margin_Pa result
    - current_margin: current_margin result
    - coil_drive_MW: coil_drive_MW result
    - material_cost: material_cost result
    - stress_Pa: stress_Pa result
    - intercept_W: intercept_W result
    - field_extrapolated: field_extrapolated result
    - cold_carnot_fraction: cold_carnot_fraction result
    - strain: strain result
    - fixed_cold_MW: fixed_cold_MW result
    - insulation_cost: insulation_cost result
    - cold_margin_W: cold_margin_W result
    - global_construction_qualified: global_construction_qualified result
    - intercept_carnot_fraction: intercept_carnot_fraction result
    - ambient_temperature_K: ambient_temperature_K result
    - winding_cost: winding_cost result
    - tape_cost: tape_cost result
    - field_margin_T: field_margin_T result
    - intercept_rating_W: intercept_rating_W result
    - fit_margin: fit_margin result
    - intercept_margin_W: intercept_margin_W result
    - cold_temperature_K: cold_temperature_K result
    - nuclear_heating_W_m3: nuclear_heating_W_m3 result
    - refrigeration_MW: refrigeration_MW result

SysML Source: root-0/whole_plant_conversion_accounts.sysml:14

    SysML Source: root-0/whole_plant_conversion_accounts.sysml:14

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/captured_reactor_offer_impl.py; reviewed equations in design/configuration.

    IMPLEMENTATION: See whole_plant_conversion_tea.handwritten.whole_plant_conversion_accounts.captured_reactor_offer_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts nuclear_transport_qualified, inventory_cold_W, identity_supported, peak_field, cold_rating_W, support_cost, cold_volume_m3, intercept_temperature_K, intercept_inventory_W, turn_current_A, axis_field, strain_margin, magnet_capital, cold_W, stress_margin_Pa, current_margin, coil_drive_MW, material_cost, stress_Pa, intercept_W, field_extrapolated, cold_carnot_fraction, strain, fixed_cold_MW, insulation_cost, cold_margin_W, global_construction_qualified, intercept_carnot_fraction, ambient_temperature_K, winding_cost, tape_cost, field_margin_T, intercept_rating_W, fit_margin, intercept_margin_W, cold_temperature_K, nuclear_heating_W_m3, refrigeration_MW fields to separate channels.
    """

    name: str = "Captured_Reactor_OfferModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, capture_id_in: float    ) -> Captured_Reactor_OfferInput:
        """Validate inputs and fill defaults.

        Args:
            capture_id_in: capture_id_in input

        Returns:
            Validated input model
        """
        return Captured_Reactor_OfferInput(capture_id_in=capture_id_in)

    def run(
        self, capture_id_in: float    ) -> ModuleResult[Captured_Reactor_OfferOutput]:
        """Execute calculation.

        Args:
            capture_id_in: capture_id_in input

        Returns:
            Module result with Captured_Reactor_OfferOutput (nuclear_transport_qualified, inventory_cold_W, identity_supported, peak_field, cold_rating_W, support_cost, cold_volume_m3, intercept_temperature_K, intercept_inventory_W, turn_current_A, axis_field, strain_margin, magnet_capital, cold_W, stress_margin_Pa, current_margin, coil_drive_MW, material_cost, stress_Pa, intercept_W, field_extrapolated, cold_carnot_fraction, strain, fixed_cold_MW, insulation_cost, cold_margin_W, global_construction_qualified, intercept_carnot_fraction, ambient_temperature_K, winding_cost, tape_cost, field_margin_T, intercept_rating_W, fit_margin, intercept_margin_W, cold_temperature_K, nuclear_heating_W_m3, refrigeration_MW)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(capture_id_in)

        # Import handwritten implementation
        from whole_plant_conversion_tea.handwritten.whole_plant_conversion_accounts.captured_reactor_offer_impl import (
            run_captured_reactor_offer,
        )

        # Execute implementation - returns tuple of values
        nuclear_transport_qualified, inventory_cold_W, identity_supported, peak_field, cold_rating_W, support_cost, cold_volume_m3, intercept_temperature_K, intercept_inventory_W, turn_current_A, axis_field, strain_margin, magnet_capital, cold_W, stress_margin_Pa, current_margin, coil_drive_MW, material_cost, stress_Pa, intercept_W, field_extrapolated, cold_carnot_fraction, strain, fixed_cold_MW, insulation_cost, cold_margin_W, global_construction_qualified, intercept_carnot_fraction, ambient_temperature_K, winding_cost, tape_cost, field_margin_T, intercept_rating_W, fit_margin, intercept_margin_W, cold_temperature_K, nuclear_heating_W_m3, refrigeration_MW = run_captured_reactor_offer(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Captured_Reactor_OfferOutput(
                nuclear_transport_qualified=nuclear_transport_qualified,
                inventory_cold_W=inventory_cold_W,
                identity_supported=identity_supported,
                peak_field=peak_field,
                cold_rating_W=cold_rating_W,
                support_cost=support_cost,
                cold_volume_m3=cold_volume_m3,
                intercept_temperature_K=intercept_temperature_K,
                intercept_inventory_W=intercept_inventory_W,
                turn_current_A=turn_current_A,
                axis_field=axis_field,
                strain_margin=strain_margin,
                magnet_capital=magnet_capital,
                cold_W=cold_W,
                stress_margin_Pa=stress_margin_Pa,
                current_margin=current_margin,
                coil_drive_MW=coil_drive_MW,
                material_cost=material_cost,
                stress_Pa=stress_Pa,
                intercept_W=intercept_W,
                field_extrapolated=field_extrapolated,
                cold_carnot_fraction=cold_carnot_fraction,
                strain=strain,
                fixed_cold_MW=fixed_cold_MW,
                insulation_cost=insulation_cost,
                cold_margin_W=cold_margin_W,
                global_construction_qualified=global_construction_qualified,
                intercept_carnot_fraction=intercept_carnot_fraction,
                ambient_temperature_K=ambient_temperature_K,
                winding_cost=winding_cost,
                tape_cost=tape_cost,
                field_margin_T=field_margin_T,
                intercept_rating_W=intercept_rating_W,
                fit_margin=fit_margin,
                intercept_margin_W=intercept_margin_W,
                cold_temperature_K=cold_temperature_K,
                nuclear_heating_W_m3=nuclear_heating_W_m3,
                refrigeration_MW=refrigeration_MW,
            )
        )
