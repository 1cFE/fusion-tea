"""Conditional_Cryogenic_DemandModule Module Wrapper

TEAx module for Conditional_Cryogenic_Demand calculation.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/conditional_cryogenic_demand_impl.py; reviewed equations in design/configuration.

Inputs:
    - inventory_cold_W_in: inventory_cold_W_in parameter
    - cold_rating_W_in: cold_rating_W_in parameter
    - intercept_temperature_K_in: intercept_temperature_K_in parameter
    - fixed_cold_MW_in: fixed_cold_MW_in parameter
    - intercept_carnot_fraction_in: intercept_carnot_fraction_in parameter
    - cold_volume_m3_in: cold_volume_m3_in parameter
    - cold_temperature_K_in: cold_temperature_K_in parameter
    - intercept_rating_W_in: intercept_rating_W_in parameter
    - extra_cold_W_in: extra_cold_W_in parameter
    - q_nuc_W_m3_in: q_nuc_W_m3_in parameter
    - intercept_inventory_W_in: intercept_inventory_W_in parameter
    - cold_carnot_fraction_in: cold_carnot_fraction_in parameter
    - ambient_temperature_K_in: ambient_temperature_K_in parameter

Outputs:
    - intercept_W: intercept_W result
    - extra_cold_capacity_W: extra_cold_capacity_W result
    - domain_supported: domain_supported result
    - refrigeration_MW: refrigeration_MW result
    - nuclear_transport_qualified: nuclear_transport_qualified result
    - intercept_margin_W: intercept_margin_W result
    - cold_W: cold_W result
    - cold_electric_MW: cold_electric_MW result
    - intercept_electric_MW: intercept_electric_MW result
    - cold_margin_W: cold_margin_W result
    - q_nuc_capacity_W_m3: q_nuc_capacity_W_m3 result

SysML Source: root-0/whole_plant_conversion_accounts.sysml:56

SysML Source: root-0/whole_plant_conversion_accounts.sysml:56

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/whole_plant_conversion_accounts/conditional_cryogenic_demand_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.primitives import Float
from whole_plant_conversion_tea.schemas.conditional_cryogenic_demand_output import Conditional_Cryogenic_DemandOutput


class Conditional_Cryogenic_DemandInput(BaseModel):
    """Input model for Conditional_Cryogenic_DemandModule.

    Attributes:
        inventory_cold_W_in: inventory_cold_W_in input
        cold_rating_W_in: cold_rating_W_in input
        intercept_temperature_K_in: intercept_temperature_K_in input
        fixed_cold_MW_in: fixed_cold_MW_in input
        intercept_carnot_fraction_in: intercept_carnot_fraction_in input
        cold_volume_m3_in: cold_volume_m3_in input
        cold_temperature_K_in: cold_temperature_K_in input
        intercept_rating_W_in: intercept_rating_W_in input
        extra_cold_W_in: extra_cold_W_in input
        q_nuc_W_m3_in: q_nuc_W_m3_in input
        intercept_inventory_W_in: intercept_inventory_W_in input
        cold_carnot_fraction_in: cold_carnot_fraction_in input
        ambient_temperature_K_in: ambient_temperature_K_in input
    """
    inventory_cold_W_in: float = Field(..., description="inventory_cold_W_in input")
    cold_rating_W_in: float = Field(..., description="cold_rating_W_in input")
    intercept_temperature_K_in: float = Field(..., description="intercept_temperature_K_in input")
    fixed_cold_MW_in: float = Field(..., description="fixed_cold_MW_in input")
    intercept_carnot_fraction_in: float = Field(..., description="intercept_carnot_fraction_in input")
    cold_volume_m3_in: float = Field(..., description="cold_volume_m3_in input")
    cold_temperature_K_in: float = Field(..., description="cold_temperature_K_in input")
    intercept_rating_W_in: float = Field(..., description="intercept_rating_W_in input")
    extra_cold_W_in: float = Field(..., description="extra_cold_W_in input")
    q_nuc_W_m3_in: float = Field(..., description="q_nuc_W_m3_in input")
    intercept_inventory_W_in: float = Field(..., description="intercept_inventory_W_in input")
    cold_carnot_fraction_in: float = Field(..., description="cold_carnot_fraction_in input")
    ambient_temperature_K_in: float = Field(..., description="ambient_temperature_K_in input")


class Conditional_Cryogenic_DemandModule(ModuleBase[Conditional_Cryogenic_DemandInput, Conditional_Cryogenic_DemandOutput]):
    """TEAx module for Conditional_Cryogenic_Demand calculation.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/conditional_cryogenic_demand_impl.py; reviewed equations in design/configuration.

Inputs:
    - inventory_cold_W_in: inventory_cold_W_in parameter
    - cold_rating_W_in: cold_rating_W_in parameter
    - intercept_temperature_K_in: intercept_temperature_K_in parameter
    - fixed_cold_MW_in: fixed_cold_MW_in parameter
    - intercept_carnot_fraction_in: intercept_carnot_fraction_in parameter
    - cold_volume_m3_in: cold_volume_m3_in parameter
    - cold_temperature_K_in: cold_temperature_K_in parameter
    - intercept_rating_W_in: intercept_rating_W_in parameter
    - extra_cold_W_in: extra_cold_W_in parameter
    - q_nuc_W_m3_in: q_nuc_W_m3_in parameter
    - intercept_inventory_W_in: intercept_inventory_W_in parameter
    - cold_carnot_fraction_in: cold_carnot_fraction_in parameter
    - ambient_temperature_K_in: ambient_temperature_K_in parameter

Outputs:
    - intercept_W: intercept_W result
    - extra_cold_capacity_W: extra_cold_capacity_W result
    - domain_supported: domain_supported result
    - refrigeration_MW: refrigeration_MW result
    - nuclear_transport_qualified: nuclear_transport_qualified result
    - intercept_margin_W: intercept_margin_W result
    - cold_W: cold_W result
    - cold_electric_MW: cold_electric_MW result
    - intercept_electric_MW: intercept_electric_MW result
    - cold_margin_W: cold_margin_W result
    - q_nuc_capacity_W_m3: q_nuc_capacity_W_m3 result

SysML Source: root-0/whole_plant_conversion_accounts.sysml:56

    SysML Source: root-0/whole_plant_conversion_accounts.sysml:56

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/conditional_cryogenic_demand_impl.py; reviewed equations in design/configuration.

    IMPLEMENTATION: See whole_plant_conversion_tea.handwritten.whole_plant_conversion_accounts.conditional_cryogenic_demand_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts intercept_W, extra_cold_capacity_W, domain_supported, refrigeration_MW, nuclear_transport_qualified, intercept_margin_W, cold_W, cold_electric_MW, intercept_electric_MW, cold_margin_W, q_nuc_capacity_W_m3 fields to separate channels.
    """

    name: str = "Conditional_Cryogenic_DemandModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, inventory_cold_W_in: float, cold_rating_W_in: float, intercept_temperature_K_in: float, fixed_cold_MW_in: float, intercept_carnot_fraction_in: float, cold_volume_m3_in: float, cold_temperature_K_in: float, intercept_rating_W_in: float, extra_cold_W_in: float, q_nuc_W_m3_in: float, intercept_inventory_W_in: float, cold_carnot_fraction_in: float, ambient_temperature_K_in: float    ) -> Conditional_Cryogenic_DemandInput:
        """Validate inputs and fill defaults.

        Args:
            inventory_cold_W_in: inventory_cold_W_in input
            cold_rating_W_in: cold_rating_W_in input
            intercept_temperature_K_in: intercept_temperature_K_in input
            fixed_cold_MW_in: fixed_cold_MW_in input
            intercept_carnot_fraction_in: intercept_carnot_fraction_in input
            cold_volume_m3_in: cold_volume_m3_in input
            cold_temperature_K_in: cold_temperature_K_in input
            intercept_rating_W_in: intercept_rating_W_in input
            extra_cold_W_in: extra_cold_W_in input
            q_nuc_W_m3_in: q_nuc_W_m3_in input
            intercept_inventory_W_in: intercept_inventory_W_in input
            cold_carnot_fraction_in: cold_carnot_fraction_in input
            ambient_temperature_K_in: ambient_temperature_K_in input

        Returns:
            Validated input model
        """
        return Conditional_Cryogenic_DemandInput(inventory_cold_W_in=inventory_cold_W_in, cold_rating_W_in=cold_rating_W_in, intercept_temperature_K_in=intercept_temperature_K_in, fixed_cold_MW_in=fixed_cold_MW_in, intercept_carnot_fraction_in=intercept_carnot_fraction_in, cold_volume_m3_in=cold_volume_m3_in, cold_temperature_K_in=cold_temperature_K_in, intercept_rating_W_in=intercept_rating_W_in, extra_cold_W_in=extra_cold_W_in, q_nuc_W_m3_in=q_nuc_W_m3_in, intercept_inventory_W_in=intercept_inventory_W_in, cold_carnot_fraction_in=cold_carnot_fraction_in, ambient_temperature_K_in=ambient_temperature_K_in)

    def run(
        self, inventory_cold_W_in: float, cold_rating_W_in: float, intercept_temperature_K_in: float, fixed_cold_MW_in: float, intercept_carnot_fraction_in: float, cold_volume_m3_in: float, cold_temperature_K_in: float, intercept_rating_W_in: float, extra_cold_W_in: float, q_nuc_W_m3_in: float, intercept_inventory_W_in: float, cold_carnot_fraction_in: float, ambient_temperature_K_in: float    ) -> ModuleResult[Conditional_Cryogenic_DemandOutput]:
        """Execute calculation.

        Args:
            inventory_cold_W_in: inventory_cold_W_in input
            cold_rating_W_in: cold_rating_W_in input
            intercept_temperature_K_in: intercept_temperature_K_in input
            fixed_cold_MW_in: fixed_cold_MW_in input
            intercept_carnot_fraction_in: intercept_carnot_fraction_in input
            cold_volume_m3_in: cold_volume_m3_in input
            cold_temperature_K_in: cold_temperature_K_in input
            intercept_rating_W_in: intercept_rating_W_in input
            extra_cold_W_in: extra_cold_W_in input
            q_nuc_W_m3_in: q_nuc_W_m3_in input
            intercept_inventory_W_in: intercept_inventory_W_in input
            cold_carnot_fraction_in: cold_carnot_fraction_in input
            ambient_temperature_K_in: ambient_temperature_K_in input

        Returns:
            Module result with Conditional_Cryogenic_DemandOutput (intercept_W, extra_cold_capacity_W, domain_supported, refrigeration_MW, nuclear_transport_qualified, intercept_margin_W, cold_W, cold_electric_MW, intercept_electric_MW, cold_margin_W, q_nuc_capacity_W_m3)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(inventory_cold_W_in, cold_rating_W_in, intercept_temperature_K_in, fixed_cold_MW_in, intercept_carnot_fraction_in, cold_volume_m3_in, cold_temperature_K_in, intercept_rating_W_in, extra_cold_W_in, q_nuc_W_m3_in, intercept_inventory_W_in, cold_carnot_fraction_in, ambient_temperature_K_in)

        # Import handwritten implementation
        from whole_plant_conversion_tea.handwritten.whole_plant_conversion_accounts.conditional_cryogenic_demand_impl import (
            run_conditional_cryogenic_demand,
        )

        # Execute implementation - returns tuple of values
        intercept_W, extra_cold_capacity_W, domain_supported, refrigeration_MW, nuclear_transport_qualified, intercept_margin_W, cold_W, cold_electric_MW, intercept_electric_MW, cold_margin_W, q_nuc_capacity_W_m3 = run_conditional_cryogenic_demand(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Conditional_Cryogenic_DemandOutput(
                intercept_W=intercept_W,
                extra_cold_capacity_W=extra_cold_capacity_W,
                domain_supported=domain_supported,
                refrigeration_MW=refrigeration_MW,
                nuclear_transport_qualified=nuclear_transport_qualified,
                intercept_margin_W=intercept_margin_W,
                cold_W=cold_W,
                cold_electric_MW=cold_electric_MW,
                intercept_electric_MW=intercept_electric_MW,
                cold_margin_W=cold_margin_W,
                q_nuc_capacity_W_m3=q_nuc_capacity_W_m3,
            )
        )
