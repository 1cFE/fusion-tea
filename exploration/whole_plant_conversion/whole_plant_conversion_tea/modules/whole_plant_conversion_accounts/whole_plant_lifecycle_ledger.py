"""Whole_Plant_Lifecycle_LedgerModule Module Wrapper

TEAx module for Whole_Plant_Lifecycle_Ledger calculation.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/whole_plant_lifecycle_ledger_impl.py; reviewed equations in design/configuration.

Inputs:
    - blanket_capital_in: blanket_capital_in parameter
    - pbl_refill_fraction_in: pbl_refill_fraction_in parameter
    - wall_life_in: wall_life_in parameter
    - magnet_outage_in: magnet_outage_in parameter
    - overhaul_fraction_in: overhaul_fraction_in parameter
    - primary_event_in: primary_event_in parameter
    - construction_years_in: construction_years_in parameter
    - conversion_annual_service_in: conversion_annual_service_in parameter
    - magnet_life_in: magnet_life_in parameter
    - overhaul_base_in: overhaul_base_in parameter
    - helium_capital_in: helium_capital_in parameter
    - divertor_capital_in: divertor_capital_in parameter
    - years_in: years_in parameter
    - magnet_removal_fraction_in: magnet_removal_fraction_in parameter
    - primary_life_in: primary_life_in parameter
    - rate_in: rate_in parameter
    - routine_om_in: routine_om_in parameter
    - annual_export_MWh_in: annual_export_MWh_in parameter
    - other_outage_in: other_outage_in parameter
    - salvage_fraction_in: salvage_fraction_in parameter
    - salvage_base_in: salvage_base_in parameter
    - initial_capital_in: initial_capital_in parameter
    - conversion_replacement_pv_in: conversion_replacement_pv_in parameter
    - annual_import_cost_in: annual_import_cost_in parameter
    - annual_net_grid_MWh_in: annual_net_grid_MWh_in parameter
    - wall_load_in: wall_load_in parameter
    - routine_fraction_in: routine_fraction_in parameter
    - dismantle_fraction_in: dismantle_fraction_in parameter
    - blanket_outage_in: blanket_outage_in parameter
    - helium_makeup_fraction_in: helium_makeup_fraction_in parameter
    - magnet_capital_in: magnet_capital_in parameter
    - overhaul_year_in: overhaul_year_in parameter
    - availability_in: availability_in parameter
    - pbl_capital_in: pbl_capital_in parameter
    - annual_fuel_in: annual_fuel_in parameter
    - conversion_annual_makeup_in: conversion_annual_makeup_in parameter
    - blanket_removal_fraction_in: blanket_removal_fraction_in parameter

Outputs:
    - cost_residual: cost_residual result
    - source_replacement_pv: source_replacement_pv result
    - annual_service: annual_service result
    - initial_financed_capital: initial_financed_capital result
    - primary_replacement_pv: primary_replacement_pv result
    - total_cost_pv: total_cost_pv result
    - energy_pv: energy_pv result
    - economic_defined: economic_defined result
    - conversion_replacement_pv: conversion_replacement_pv result
    - magnet_events: magnet_events result
    - annual_expense: annual_expense result
    - lcoe_USD2025_MWh: lcoe_USD2025_MWh result
    - annual_expense_pv: annual_expense_pv result
    - primary_events: primary_events result
    - outage_years: outage_years result
    - domain_supported: domain_supported result
    - terminal_pv: terminal_pv result
    - annual_makeup: annual_makeup result
    - magnet_life_years: magnet_life_years result
    - magnet_replacement_pv: magnet_replacement_pv result
    - overhaul_pv: overhaul_pv result
    - annual_source_service: annual_source_service result
    - blanket_events: blanket_events result
    - outage_margin: outage_margin result
    - blanket_life_years: blanket_life_years result
    - blanket_replacement_pv: blanket_replacement_pv result

SysML Source: root-0/whole_plant_conversion_accounts.sysml:255

SysML Source: root-0/whole_plant_conversion_accounts.sysml:255

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/whole_plant_conversion_accounts/whole_plant_lifecycle_ledger_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.primitives import Float
from whole_plant_conversion_tea.schemas.whole_plant_lifecycle_ledger_output import Whole_Plant_Lifecycle_LedgerOutput


class Whole_Plant_Lifecycle_LedgerInput(BaseModel):
    """Input model for Whole_Plant_Lifecycle_LedgerModule.

    Attributes:
        blanket_capital_in: blanket_capital_in input
        pbl_refill_fraction_in: pbl_refill_fraction_in input
        wall_life_in: wall_life_in input
        magnet_outage_in: magnet_outage_in input
        overhaul_fraction_in: overhaul_fraction_in input
        primary_event_in: primary_event_in input
        construction_years_in: construction_years_in input
        conversion_annual_service_in: conversion_annual_service_in input
        magnet_life_in: magnet_life_in input
        overhaul_base_in: overhaul_base_in input
        helium_capital_in: helium_capital_in input
        divertor_capital_in: divertor_capital_in input
        years_in: years_in input
        magnet_removal_fraction_in: magnet_removal_fraction_in input
        primary_life_in: primary_life_in input
        rate_in: rate_in input
        routine_om_in: routine_om_in input
        annual_export_MWh_in: annual_export_MWh_in input
        other_outage_in: other_outage_in input
        salvage_fraction_in: salvage_fraction_in input
        salvage_base_in: salvage_base_in input
        initial_capital_in: initial_capital_in input
        conversion_replacement_pv_in: conversion_replacement_pv_in input
        annual_import_cost_in: annual_import_cost_in input
        annual_net_grid_MWh_in: annual_net_grid_MWh_in input
        wall_load_in: wall_load_in input
        routine_fraction_in: routine_fraction_in input
        dismantle_fraction_in: dismantle_fraction_in input
        blanket_outage_in: blanket_outage_in input
        helium_makeup_fraction_in: helium_makeup_fraction_in input
        magnet_capital_in: magnet_capital_in input
        overhaul_year_in: overhaul_year_in input
        availability_in: availability_in input
        pbl_capital_in: pbl_capital_in input
        annual_fuel_in: annual_fuel_in input
        conversion_annual_makeup_in: conversion_annual_makeup_in input
        blanket_removal_fraction_in: blanket_removal_fraction_in input
    """
    blanket_capital_in: float = Field(..., description="blanket_capital_in input")
    pbl_refill_fraction_in: float = Field(..., description="pbl_refill_fraction_in input")
    wall_life_in: float = Field(..., description="wall_life_in input")
    magnet_outage_in: float = Field(..., description="magnet_outage_in input")
    overhaul_fraction_in: float = Field(..., description="overhaul_fraction_in input")
    primary_event_in: float = Field(..., description="primary_event_in input")
    construction_years_in: float = Field(..., description="construction_years_in input")
    conversion_annual_service_in: float = Field(..., description="conversion_annual_service_in input")
    magnet_life_in: float = Field(..., description="magnet_life_in input")
    overhaul_base_in: float = Field(..., description="overhaul_base_in input")
    helium_capital_in: float = Field(..., description="helium_capital_in input")
    divertor_capital_in: float = Field(..., description="divertor_capital_in input")
    years_in: float = Field(..., description="years_in input")
    magnet_removal_fraction_in: float = Field(..., description="magnet_removal_fraction_in input")
    primary_life_in: float = Field(..., description="primary_life_in input")
    rate_in: float = Field(..., description="rate_in input")
    routine_om_in: float = Field(..., description="routine_om_in input")
    annual_export_MWh_in: float = Field(..., description="annual_export_MWh_in input")
    other_outage_in: float = Field(..., description="other_outage_in input")
    salvage_fraction_in: float = Field(..., description="salvage_fraction_in input")
    salvage_base_in: float = Field(..., description="salvage_base_in input")
    initial_capital_in: float = Field(..., description="initial_capital_in input")
    conversion_replacement_pv_in: float = Field(..., description="conversion_replacement_pv_in input")
    annual_import_cost_in: float = Field(..., description="annual_import_cost_in input")
    annual_net_grid_MWh_in: float = Field(..., description="annual_net_grid_MWh_in input")
    wall_load_in: float = Field(..., description="wall_load_in input")
    routine_fraction_in: float = Field(..., description="routine_fraction_in input")
    dismantle_fraction_in: float = Field(..., description="dismantle_fraction_in input")
    blanket_outage_in: float = Field(..., description="blanket_outage_in input")
    helium_makeup_fraction_in: float = Field(..., description="helium_makeup_fraction_in input")
    magnet_capital_in: float = Field(..., description="magnet_capital_in input")
    overhaul_year_in: float = Field(..., description="overhaul_year_in input")
    availability_in: float = Field(..., description="availability_in input")
    pbl_capital_in: float = Field(..., description="pbl_capital_in input")
    annual_fuel_in: float = Field(..., description="annual_fuel_in input")
    conversion_annual_makeup_in: float = Field(..., description="conversion_annual_makeup_in input")
    blanket_removal_fraction_in: float = Field(..., description="blanket_removal_fraction_in input")


class Whole_Plant_Lifecycle_LedgerModule(ModuleBase[Whole_Plant_Lifecycle_LedgerInput, Whole_Plant_Lifecycle_LedgerOutput]):
    """TEAx module for Whole_Plant_Lifecycle_Ledger calculation.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/whole_plant_lifecycle_ledger_impl.py; reviewed equations in design/configuration.

Inputs:
    - blanket_capital_in: blanket_capital_in parameter
    - pbl_refill_fraction_in: pbl_refill_fraction_in parameter
    - wall_life_in: wall_life_in parameter
    - magnet_outage_in: magnet_outage_in parameter
    - overhaul_fraction_in: overhaul_fraction_in parameter
    - primary_event_in: primary_event_in parameter
    - construction_years_in: construction_years_in parameter
    - conversion_annual_service_in: conversion_annual_service_in parameter
    - magnet_life_in: magnet_life_in parameter
    - overhaul_base_in: overhaul_base_in parameter
    - helium_capital_in: helium_capital_in parameter
    - divertor_capital_in: divertor_capital_in parameter
    - years_in: years_in parameter
    - magnet_removal_fraction_in: magnet_removal_fraction_in parameter
    - primary_life_in: primary_life_in parameter
    - rate_in: rate_in parameter
    - routine_om_in: routine_om_in parameter
    - annual_export_MWh_in: annual_export_MWh_in parameter
    - other_outage_in: other_outage_in parameter
    - salvage_fraction_in: salvage_fraction_in parameter
    - salvage_base_in: salvage_base_in parameter
    - initial_capital_in: initial_capital_in parameter
    - conversion_replacement_pv_in: conversion_replacement_pv_in parameter
    - annual_import_cost_in: annual_import_cost_in parameter
    - annual_net_grid_MWh_in: annual_net_grid_MWh_in parameter
    - wall_load_in: wall_load_in parameter
    - routine_fraction_in: routine_fraction_in parameter
    - dismantle_fraction_in: dismantle_fraction_in parameter
    - blanket_outage_in: blanket_outage_in parameter
    - helium_makeup_fraction_in: helium_makeup_fraction_in parameter
    - magnet_capital_in: magnet_capital_in parameter
    - overhaul_year_in: overhaul_year_in parameter
    - availability_in: availability_in parameter
    - pbl_capital_in: pbl_capital_in parameter
    - annual_fuel_in: annual_fuel_in parameter
    - conversion_annual_makeup_in: conversion_annual_makeup_in parameter
    - blanket_removal_fraction_in: blanket_removal_fraction_in parameter

Outputs:
    - cost_residual: cost_residual result
    - source_replacement_pv: source_replacement_pv result
    - annual_service: annual_service result
    - initial_financed_capital: initial_financed_capital result
    - primary_replacement_pv: primary_replacement_pv result
    - total_cost_pv: total_cost_pv result
    - energy_pv: energy_pv result
    - economic_defined: economic_defined result
    - conversion_replacement_pv: conversion_replacement_pv result
    - magnet_events: magnet_events result
    - annual_expense: annual_expense result
    - lcoe_USD2025_MWh: lcoe_USD2025_MWh result
    - annual_expense_pv: annual_expense_pv result
    - primary_events: primary_events result
    - outage_years: outage_years result
    - domain_supported: domain_supported result
    - terminal_pv: terminal_pv result
    - annual_makeup: annual_makeup result
    - magnet_life_years: magnet_life_years result
    - magnet_replacement_pv: magnet_replacement_pv result
    - overhaul_pv: overhaul_pv result
    - annual_source_service: annual_source_service result
    - blanket_events: blanket_events result
    - outage_margin: outage_margin result
    - blanket_life_years: blanket_life_years result
    - blanket_replacement_pv: blanket_replacement_pv result

SysML Source: root-0/whole_plant_conversion_accounts.sysml:255

    SysML Source: root-0/whole_plant_conversion_accounts.sysml:255

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/whole_plant_lifecycle_ledger_impl.py; reviewed equations in design/configuration.

    IMPLEMENTATION: See whole_plant_conversion_tea.handwritten.whole_plant_conversion_accounts.whole_plant_lifecycle_ledger_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts cost_residual, source_replacement_pv, annual_service, initial_financed_capital, primary_replacement_pv, total_cost_pv, energy_pv, economic_defined, conversion_replacement_pv, magnet_events, annual_expense, lcoe_USD2025_MWh, annual_expense_pv, primary_events, outage_years, domain_supported, terminal_pv, annual_makeup, magnet_life_years, magnet_replacement_pv, overhaul_pv, annual_source_service, blanket_events, outage_margin, blanket_life_years, blanket_replacement_pv fields to separate channels.
    """

    name: str = "Whole_Plant_Lifecycle_LedgerModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, blanket_capital_in: float, pbl_refill_fraction_in: float, wall_life_in: float, magnet_outage_in: float, overhaul_fraction_in: float, primary_event_in: float, construction_years_in: float, conversion_annual_service_in: float, magnet_life_in: float, overhaul_base_in: float, helium_capital_in: float, divertor_capital_in: float, years_in: float, magnet_removal_fraction_in: float, primary_life_in: float, rate_in: float, routine_om_in: float, annual_export_MWh_in: float, other_outage_in: float, salvage_fraction_in: float, salvage_base_in: float, initial_capital_in: float, conversion_replacement_pv_in: float, annual_import_cost_in: float, annual_net_grid_MWh_in: float, wall_load_in: float, routine_fraction_in: float, dismantle_fraction_in: float, blanket_outage_in: float, helium_makeup_fraction_in: float, magnet_capital_in: float, overhaul_year_in: float, availability_in: float, pbl_capital_in: float, annual_fuel_in: float, conversion_annual_makeup_in: float, blanket_removal_fraction_in: float    ) -> Whole_Plant_Lifecycle_LedgerInput:
        """Validate inputs and fill defaults.

        Args:
            blanket_capital_in: blanket_capital_in input
            pbl_refill_fraction_in: pbl_refill_fraction_in input
            wall_life_in: wall_life_in input
            magnet_outage_in: magnet_outage_in input
            overhaul_fraction_in: overhaul_fraction_in input
            primary_event_in: primary_event_in input
            construction_years_in: construction_years_in input
            conversion_annual_service_in: conversion_annual_service_in input
            magnet_life_in: magnet_life_in input
            overhaul_base_in: overhaul_base_in input
            helium_capital_in: helium_capital_in input
            divertor_capital_in: divertor_capital_in input
            years_in: years_in input
            magnet_removal_fraction_in: magnet_removal_fraction_in input
            primary_life_in: primary_life_in input
            rate_in: rate_in input
            routine_om_in: routine_om_in input
            annual_export_MWh_in: annual_export_MWh_in input
            other_outage_in: other_outage_in input
            salvage_fraction_in: salvage_fraction_in input
            salvage_base_in: salvage_base_in input
            initial_capital_in: initial_capital_in input
            conversion_replacement_pv_in: conversion_replacement_pv_in input
            annual_import_cost_in: annual_import_cost_in input
            annual_net_grid_MWh_in: annual_net_grid_MWh_in input
            wall_load_in: wall_load_in input
            routine_fraction_in: routine_fraction_in input
            dismantle_fraction_in: dismantle_fraction_in input
            blanket_outage_in: blanket_outage_in input
            helium_makeup_fraction_in: helium_makeup_fraction_in input
            magnet_capital_in: magnet_capital_in input
            overhaul_year_in: overhaul_year_in input
            availability_in: availability_in input
            pbl_capital_in: pbl_capital_in input
            annual_fuel_in: annual_fuel_in input
            conversion_annual_makeup_in: conversion_annual_makeup_in input
            blanket_removal_fraction_in: blanket_removal_fraction_in input

        Returns:
            Validated input model
        """
        return Whole_Plant_Lifecycle_LedgerInput(blanket_capital_in=blanket_capital_in, pbl_refill_fraction_in=pbl_refill_fraction_in, wall_life_in=wall_life_in, magnet_outage_in=magnet_outage_in, overhaul_fraction_in=overhaul_fraction_in, primary_event_in=primary_event_in, construction_years_in=construction_years_in, conversion_annual_service_in=conversion_annual_service_in, magnet_life_in=magnet_life_in, overhaul_base_in=overhaul_base_in, helium_capital_in=helium_capital_in, divertor_capital_in=divertor_capital_in, years_in=years_in, magnet_removal_fraction_in=magnet_removal_fraction_in, primary_life_in=primary_life_in, rate_in=rate_in, routine_om_in=routine_om_in, annual_export_MWh_in=annual_export_MWh_in, other_outage_in=other_outage_in, salvage_fraction_in=salvage_fraction_in, salvage_base_in=salvage_base_in, initial_capital_in=initial_capital_in, conversion_replacement_pv_in=conversion_replacement_pv_in, annual_import_cost_in=annual_import_cost_in, annual_net_grid_MWh_in=annual_net_grid_MWh_in, wall_load_in=wall_load_in, routine_fraction_in=routine_fraction_in, dismantle_fraction_in=dismantle_fraction_in, blanket_outage_in=blanket_outage_in, helium_makeup_fraction_in=helium_makeup_fraction_in, magnet_capital_in=magnet_capital_in, overhaul_year_in=overhaul_year_in, availability_in=availability_in, pbl_capital_in=pbl_capital_in, annual_fuel_in=annual_fuel_in, conversion_annual_makeup_in=conversion_annual_makeup_in, blanket_removal_fraction_in=blanket_removal_fraction_in)

    def run(
        self, blanket_capital_in: float, pbl_refill_fraction_in: float, wall_life_in: float, magnet_outage_in: float, overhaul_fraction_in: float, primary_event_in: float, construction_years_in: float, conversion_annual_service_in: float, magnet_life_in: float, overhaul_base_in: float, helium_capital_in: float, divertor_capital_in: float, years_in: float, magnet_removal_fraction_in: float, primary_life_in: float, rate_in: float, routine_om_in: float, annual_export_MWh_in: float, other_outage_in: float, salvage_fraction_in: float, salvage_base_in: float, initial_capital_in: float, conversion_replacement_pv_in: float, annual_import_cost_in: float, annual_net_grid_MWh_in: float, wall_load_in: float, routine_fraction_in: float, dismantle_fraction_in: float, blanket_outage_in: float, helium_makeup_fraction_in: float, magnet_capital_in: float, overhaul_year_in: float, availability_in: float, pbl_capital_in: float, annual_fuel_in: float, conversion_annual_makeup_in: float, blanket_removal_fraction_in: float    ) -> ModuleResult[Whole_Plant_Lifecycle_LedgerOutput]:
        """Execute calculation.

        Args:
            blanket_capital_in: blanket_capital_in input
            pbl_refill_fraction_in: pbl_refill_fraction_in input
            wall_life_in: wall_life_in input
            magnet_outage_in: magnet_outage_in input
            overhaul_fraction_in: overhaul_fraction_in input
            primary_event_in: primary_event_in input
            construction_years_in: construction_years_in input
            conversion_annual_service_in: conversion_annual_service_in input
            magnet_life_in: magnet_life_in input
            overhaul_base_in: overhaul_base_in input
            helium_capital_in: helium_capital_in input
            divertor_capital_in: divertor_capital_in input
            years_in: years_in input
            magnet_removal_fraction_in: magnet_removal_fraction_in input
            primary_life_in: primary_life_in input
            rate_in: rate_in input
            routine_om_in: routine_om_in input
            annual_export_MWh_in: annual_export_MWh_in input
            other_outage_in: other_outage_in input
            salvage_fraction_in: salvage_fraction_in input
            salvage_base_in: salvage_base_in input
            initial_capital_in: initial_capital_in input
            conversion_replacement_pv_in: conversion_replacement_pv_in input
            annual_import_cost_in: annual_import_cost_in input
            annual_net_grid_MWh_in: annual_net_grid_MWh_in input
            wall_load_in: wall_load_in input
            routine_fraction_in: routine_fraction_in input
            dismantle_fraction_in: dismantle_fraction_in input
            blanket_outage_in: blanket_outage_in input
            helium_makeup_fraction_in: helium_makeup_fraction_in input
            magnet_capital_in: magnet_capital_in input
            overhaul_year_in: overhaul_year_in input
            availability_in: availability_in input
            pbl_capital_in: pbl_capital_in input
            annual_fuel_in: annual_fuel_in input
            conversion_annual_makeup_in: conversion_annual_makeup_in input
            blanket_removal_fraction_in: blanket_removal_fraction_in input

        Returns:
            Module result with Whole_Plant_Lifecycle_LedgerOutput (cost_residual, source_replacement_pv, annual_service, initial_financed_capital, primary_replacement_pv, total_cost_pv, energy_pv, economic_defined, conversion_replacement_pv, magnet_events, annual_expense, lcoe_USD2025_MWh, annual_expense_pv, primary_events, outage_years, domain_supported, terminal_pv, annual_makeup, magnet_life_years, magnet_replacement_pv, overhaul_pv, annual_source_service, blanket_events, outage_margin, blanket_life_years, blanket_replacement_pv)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(blanket_capital_in, pbl_refill_fraction_in, wall_life_in, magnet_outage_in, overhaul_fraction_in, primary_event_in, construction_years_in, conversion_annual_service_in, magnet_life_in, overhaul_base_in, helium_capital_in, divertor_capital_in, years_in, magnet_removal_fraction_in, primary_life_in, rate_in, routine_om_in, annual_export_MWh_in, other_outage_in, salvage_fraction_in, salvage_base_in, initial_capital_in, conversion_replacement_pv_in, annual_import_cost_in, annual_net_grid_MWh_in, wall_load_in, routine_fraction_in, dismantle_fraction_in, blanket_outage_in, helium_makeup_fraction_in, magnet_capital_in, overhaul_year_in, availability_in, pbl_capital_in, annual_fuel_in, conversion_annual_makeup_in, blanket_removal_fraction_in)

        # Import handwritten implementation
        from whole_plant_conversion_tea.handwritten.whole_plant_conversion_accounts.whole_plant_lifecycle_ledger_impl import (
            run_whole_plant_lifecycle_ledger,
        )

        # Execute implementation - returns tuple of values
        cost_residual, source_replacement_pv, annual_service, initial_financed_capital, primary_replacement_pv, total_cost_pv, energy_pv, economic_defined, conversion_replacement_pv, magnet_events, annual_expense, lcoe_USD2025_MWh, annual_expense_pv, primary_events, outage_years, domain_supported, terminal_pv, annual_makeup, magnet_life_years, magnet_replacement_pv, overhaul_pv, annual_source_service, blanket_events, outage_margin, blanket_life_years, blanket_replacement_pv = run_whole_plant_lifecycle_ledger(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Whole_Plant_Lifecycle_LedgerOutput(
                cost_residual=cost_residual,
                source_replacement_pv=source_replacement_pv,
                annual_service=annual_service,
                initial_financed_capital=initial_financed_capital,
                primary_replacement_pv=primary_replacement_pv,
                total_cost_pv=total_cost_pv,
                energy_pv=energy_pv,
                economic_defined=economic_defined,
                conversion_replacement_pv=conversion_replacement_pv,
                magnet_events=magnet_events,
                annual_expense=annual_expense,
                lcoe_USD2025_MWh=lcoe_USD2025_MWh,
                annual_expense_pv=annual_expense_pv,
                primary_events=primary_events,
                outage_years=outage_years,
                domain_supported=domain_supported,
                terminal_pv=terminal_pv,
                annual_makeup=annual_makeup,
                magnet_life_years=magnet_life_years,
                magnet_replacement_pv=magnet_replacement_pv,
                overhaul_pv=overhaul_pv,
                annual_source_service=annual_source_service,
                blanket_events=blanket_events,
                outage_margin=outage_margin,
                blanket_life_years=blanket_life_years,
                blanket_replacement_pv=blanket_replacement_pv,
            )
        )
