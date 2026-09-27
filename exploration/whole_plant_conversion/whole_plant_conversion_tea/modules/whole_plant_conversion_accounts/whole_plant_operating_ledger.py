"""Whole_Plant_Operating_LedgerModule Module Wrapper

TEAx module for Whole_Plant_Operating_Ledger calculation.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/whole_plant_operating_ledger_impl.py; reviewed equations in design/configuration.

Inputs:
    - conversion_net_MW_in: conversion_net_MW_in parameter
    - auxiliary_rating_MW_in: auxiliary_rating_MW_in parameter
    - coil_drive_MW_in: coil_drive_MW_in parameter
    - primary_fluid_MW_in: primary_fluid_MW_in parameter
    - import_price_in: import_price_in parameter
    - auxiliary_electric_MW_in: auxiliary_electric_MW_in parameter
    - availability_in: availability_in parameter
    - auxiliary_water_C_in: auxiliary_water_C_in parameter
    - fuel_vacuum_MW_in: fuel_vacuum_MW_in parameter
    - tf_cooling_MW_in: tf_cooling_MW_in parameter
    - primary_electric_MW_in: primary_electric_MW_in parameter
    - refrigeration_MW_in: refrigeration_MW_in parameter
    - heating_wall_MW_in: heating_wall_MW_in parameter
    - intercept_W_in: intercept_W_in parameter
    - deposited_heating_MW_in: deposited_heating_MW_in parameter
    - pf_cooling_MW_in: pf_cooling_MW_in parameter
    - reactor_controls_MW_in: reactor_controls_MW_in parameter
    - cold_W_in: cold_W_in parameter
    - residual_MW_in: residual_MW_in parameter
    - house_MW_in: house_MW_in parameter

Outputs:
    - auxiliary_margin_MW: auxiliary_margin_MW result
    - annual_net_grid_MWh: annual_net_grid_MWh result
    - domain_supported: domain_supported result
    - annual_import_MWh: annual_import_MWh result
    - power_residual: power_residual result
    - annual_export_MWh: annual_export_MWh result
    - annual_import_cost: annual_import_cost result
    - net_export_MW: net_export_MW result
    - standby_MW: standby_MW result
    - primary_motor_loss_MW: primary_motor_loss_MW result
    - upstream_electric_MW: upstream_electric_MW result
    - auxiliary_heat_MW: auxiliary_heat_MW result

SysML Source: root-0/whole_plant_conversion_accounts.sysml:321

SysML Source: root-0/whole_plant_conversion_accounts.sysml:321

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/whole_plant_conversion_accounts/whole_plant_operating_ledger_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.primitives import Float
from whole_plant_conversion_tea.schemas.whole_plant_operating_ledger_output import Whole_Plant_Operating_LedgerOutput


class Whole_Plant_Operating_LedgerInput(BaseModel):
    """Input model for Whole_Plant_Operating_LedgerModule.

    Attributes:
        conversion_net_MW_in: conversion_net_MW_in input
        auxiliary_rating_MW_in: auxiliary_rating_MW_in input
        coil_drive_MW_in: coil_drive_MW_in input
        primary_fluid_MW_in: primary_fluid_MW_in input
        import_price_in: import_price_in input
        auxiliary_electric_MW_in: auxiliary_electric_MW_in input
        availability_in: availability_in input
        auxiliary_water_C_in: auxiliary_water_C_in input
        fuel_vacuum_MW_in: fuel_vacuum_MW_in input
        tf_cooling_MW_in: tf_cooling_MW_in input
        primary_electric_MW_in: primary_electric_MW_in input
        refrigeration_MW_in: refrigeration_MW_in input
        heating_wall_MW_in: heating_wall_MW_in input
        intercept_W_in: intercept_W_in input
        deposited_heating_MW_in: deposited_heating_MW_in input
        pf_cooling_MW_in: pf_cooling_MW_in input
        reactor_controls_MW_in: reactor_controls_MW_in input
        cold_W_in: cold_W_in input
        residual_MW_in: residual_MW_in input
        house_MW_in: house_MW_in input
    """
    conversion_net_MW_in: float = Field(..., description="conversion_net_MW_in input")
    auxiliary_rating_MW_in: float = Field(..., description="auxiliary_rating_MW_in input")
    coil_drive_MW_in: float = Field(..., description="coil_drive_MW_in input")
    primary_fluid_MW_in: float = Field(..., description="primary_fluid_MW_in input")
    import_price_in: float = Field(..., description="import_price_in input")
    auxiliary_electric_MW_in: float = Field(..., description="auxiliary_electric_MW_in input")
    availability_in: float = Field(..., description="availability_in input")
    auxiliary_water_C_in: float = Field(..., description="auxiliary_water_C_in input")
    fuel_vacuum_MW_in: float = Field(..., description="fuel_vacuum_MW_in input")
    tf_cooling_MW_in: float = Field(..., description="tf_cooling_MW_in input")
    primary_electric_MW_in: float = Field(..., description="primary_electric_MW_in input")
    refrigeration_MW_in: float = Field(..., description="refrigeration_MW_in input")
    heating_wall_MW_in: float = Field(..., description="heating_wall_MW_in input")
    intercept_W_in: float = Field(..., description="intercept_W_in input")
    deposited_heating_MW_in: float = Field(..., description="deposited_heating_MW_in input")
    pf_cooling_MW_in: float = Field(..., description="pf_cooling_MW_in input")
    reactor_controls_MW_in: float = Field(..., description="reactor_controls_MW_in input")
    cold_W_in: float = Field(..., description="cold_W_in input")
    residual_MW_in: float = Field(..., description="residual_MW_in input")
    house_MW_in: float = Field(..., description="house_MW_in input")


class Whole_Plant_Operating_LedgerModule(ModuleBase[Whole_Plant_Operating_LedgerInput, Whole_Plant_Operating_LedgerOutput]):
    """TEAx module for Whole_Plant_Operating_Ledger calculation.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/whole_plant_operating_ledger_impl.py; reviewed equations in design/configuration.

Inputs:
    - conversion_net_MW_in: conversion_net_MW_in parameter
    - auxiliary_rating_MW_in: auxiliary_rating_MW_in parameter
    - coil_drive_MW_in: coil_drive_MW_in parameter
    - primary_fluid_MW_in: primary_fluid_MW_in parameter
    - import_price_in: import_price_in parameter
    - auxiliary_electric_MW_in: auxiliary_electric_MW_in parameter
    - availability_in: availability_in parameter
    - auxiliary_water_C_in: auxiliary_water_C_in parameter
    - fuel_vacuum_MW_in: fuel_vacuum_MW_in parameter
    - tf_cooling_MW_in: tf_cooling_MW_in parameter
    - primary_electric_MW_in: primary_electric_MW_in parameter
    - refrigeration_MW_in: refrigeration_MW_in parameter
    - heating_wall_MW_in: heating_wall_MW_in parameter
    - intercept_W_in: intercept_W_in parameter
    - deposited_heating_MW_in: deposited_heating_MW_in parameter
    - pf_cooling_MW_in: pf_cooling_MW_in parameter
    - reactor_controls_MW_in: reactor_controls_MW_in parameter
    - cold_W_in: cold_W_in parameter
    - residual_MW_in: residual_MW_in parameter
    - house_MW_in: house_MW_in parameter

Outputs:
    - auxiliary_margin_MW: auxiliary_margin_MW result
    - annual_net_grid_MWh: annual_net_grid_MWh result
    - domain_supported: domain_supported result
    - annual_import_MWh: annual_import_MWh result
    - power_residual: power_residual result
    - annual_export_MWh: annual_export_MWh result
    - annual_import_cost: annual_import_cost result
    - net_export_MW: net_export_MW result
    - standby_MW: standby_MW result
    - primary_motor_loss_MW: primary_motor_loss_MW result
    - upstream_electric_MW: upstream_electric_MW result
    - auxiliary_heat_MW: auxiliary_heat_MW result

SysML Source: root-0/whole_plant_conversion_accounts.sysml:321

    SysML Source: root-0/whole_plant_conversion_accounts.sysml:321

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/whole_plant_operating_ledger_impl.py; reviewed equations in design/configuration.

    IMPLEMENTATION: See whole_plant_conversion_tea.handwritten.whole_plant_conversion_accounts.whole_plant_operating_ledger_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts auxiliary_margin_MW, annual_net_grid_MWh, domain_supported, annual_import_MWh, power_residual, annual_export_MWh, annual_import_cost, net_export_MW, standby_MW, primary_motor_loss_MW, upstream_electric_MW, auxiliary_heat_MW fields to separate channels.
    """

    name: str = "Whole_Plant_Operating_LedgerModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, conversion_net_MW_in: float, auxiliary_rating_MW_in: float, coil_drive_MW_in: float, primary_fluid_MW_in: float, import_price_in: float, auxiliary_electric_MW_in: float, availability_in: float, auxiliary_water_C_in: float, fuel_vacuum_MW_in: float, tf_cooling_MW_in: float, primary_electric_MW_in: float, refrigeration_MW_in: float, heating_wall_MW_in: float, intercept_W_in: float, deposited_heating_MW_in: float, pf_cooling_MW_in: float, reactor_controls_MW_in: float, cold_W_in: float, residual_MW_in: float, house_MW_in: float    ) -> Whole_Plant_Operating_LedgerInput:
        """Validate inputs and fill defaults.

        Args:
            conversion_net_MW_in: conversion_net_MW_in input
            auxiliary_rating_MW_in: auxiliary_rating_MW_in input
            coil_drive_MW_in: coil_drive_MW_in input
            primary_fluid_MW_in: primary_fluid_MW_in input
            import_price_in: import_price_in input
            auxiliary_electric_MW_in: auxiliary_electric_MW_in input
            availability_in: availability_in input
            auxiliary_water_C_in: auxiliary_water_C_in input
            fuel_vacuum_MW_in: fuel_vacuum_MW_in input
            tf_cooling_MW_in: tf_cooling_MW_in input
            primary_electric_MW_in: primary_electric_MW_in input
            refrigeration_MW_in: refrigeration_MW_in input
            heating_wall_MW_in: heating_wall_MW_in input
            intercept_W_in: intercept_W_in input
            deposited_heating_MW_in: deposited_heating_MW_in input
            pf_cooling_MW_in: pf_cooling_MW_in input
            reactor_controls_MW_in: reactor_controls_MW_in input
            cold_W_in: cold_W_in input
            residual_MW_in: residual_MW_in input
            house_MW_in: house_MW_in input

        Returns:
            Validated input model
        """
        return Whole_Plant_Operating_LedgerInput(conversion_net_MW_in=conversion_net_MW_in, auxiliary_rating_MW_in=auxiliary_rating_MW_in, coil_drive_MW_in=coil_drive_MW_in, primary_fluid_MW_in=primary_fluid_MW_in, import_price_in=import_price_in, auxiliary_electric_MW_in=auxiliary_electric_MW_in, availability_in=availability_in, auxiliary_water_C_in=auxiliary_water_C_in, fuel_vacuum_MW_in=fuel_vacuum_MW_in, tf_cooling_MW_in=tf_cooling_MW_in, primary_electric_MW_in=primary_electric_MW_in, refrigeration_MW_in=refrigeration_MW_in, heating_wall_MW_in=heating_wall_MW_in, intercept_W_in=intercept_W_in, deposited_heating_MW_in=deposited_heating_MW_in, pf_cooling_MW_in=pf_cooling_MW_in, reactor_controls_MW_in=reactor_controls_MW_in, cold_W_in=cold_W_in, residual_MW_in=residual_MW_in, house_MW_in=house_MW_in)

    def run(
        self, conversion_net_MW_in: float, auxiliary_rating_MW_in: float, coil_drive_MW_in: float, primary_fluid_MW_in: float, import_price_in: float, auxiliary_electric_MW_in: float, availability_in: float, auxiliary_water_C_in: float, fuel_vacuum_MW_in: float, tf_cooling_MW_in: float, primary_electric_MW_in: float, refrigeration_MW_in: float, heating_wall_MW_in: float, intercept_W_in: float, deposited_heating_MW_in: float, pf_cooling_MW_in: float, reactor_controls_MW_in: float, cold_W_in: float, residual_MW_in: float, house_MW_in: float    ) -> ModuleResult[Whole_Plant_Operating_LedgerOutput]:
        """Execute calculation.

        Args:
            conversion_net_MW_in: conversion_net_MW_in input
            auxiliary_rating_MW_in: auxiliary_rating_MW_in input
            coil_drive_MW_in: coil_drive_MW_in input
            primary_fluid_MW_in: primary_fluid_MW_in input
            import_price_in: import_price_in input
            auxiliary_electric_MW_in: auxiliary_electric_MW_in input
            availability_in: availability_in input
            auxiliary_water_C_in: auxiliary_water_C_in input
            fuel_vacuum_MW_in: fuel_vacuum_MW_in input
            tf_cooling_MW_in: tf_cooling_MW_in input
            primary_electric_MW_in: primary_electric_MW_in input
            refrigeration_MW_in: refrigeration_MW_in input
            heating_wall_MW_in: heating_wall_MW_in input
            intercept_W_in: intercept_W_in input
            deposited_heating_MW_in: deposited_heating_MW_in input
            pf_cooling_MW_in: pf_cooling_MW_in input
            reactor_controls_MW_in: reactor_controls_MW_in input
            cold_W_in: cold_W_in input
            residual_MW_in: residual_MW_in input
            house_MW_in: house_MW_in input

        Returns:
            Module result with Whole_Plant_Operating_LedgerOutput (auxiliary_margin_MW, annual_net_grid_MWh, domain_supported, annual_import_MWh, power_residual, annual_export_MWh, annual_import_cost, net_export_MW, standby_MW, primary_motor_loss_MW, upstream_electric_MW, auxiliary_heat_MW)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(conversion_net_MW_in, auxiliary_rating_MW_in, coil_drive_MW_in, primary_fluid_MW_in, import_price_in, auxiliary_electric_MW_in, availability_in, auxiliary_water_C_in, fuel_vacuum_MW_in, tf_cooling_MW_in, primary_electric_MW_in, refrigeration_MW_in, heating_wall_MW_in, intercept_W_in, deposited_heating_MW_in, pf_cooling_MW_in, reactor_controls_MW_in, cold_W_in, residual_MW_in, house_MW_in)

        # Import handwritten implementation
        from whole_plant_conversion_tea.handwritten.whole_plant_conversion_accounts.whole_plant_operating_ledger_impl import (
            run_whole_plant_operating_ledger,
        )

        # Execute implementation - returns tuple of values
        auxiliary_margin_MW, annual_net_grid_MWh, domain_supported, annual_import_MWh, power_residual, annual_export_MWh, annual_import_cost, net_export_MW, standby_MW, primary_motor_loss_MW, upstream_electric_MW, auxiliary_heat_MW = run_whole_plant_operating_ledger(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Whole_Plant_Operating_LedgerOutput(
                auxiliary_margin_MW=auxiliary_margin_MW,
                annual_net_grid_MWh=annual_net_grid_MWh,
                domain_supported=domain_supported,
                annual_import_MWh=annual_import_MWh,
                power_residual=power_residual,
                annual_export_MWh=annual_export_MWh,
                annual_import_cost=annual_import_cost,
                net_export_MW=net_export_MW,
                standby_MW=standby_MW,
                primary_motor_loss_MW=primary_motor_loss_MW,
                upstream_electric_MW=upstream_electric_MW,
                auxiliary_heat_MW=auxiliary_heat_MW,
            )
        )
