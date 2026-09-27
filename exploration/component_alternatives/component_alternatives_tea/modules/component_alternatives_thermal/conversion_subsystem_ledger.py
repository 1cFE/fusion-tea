"""Conversion_Subsystem_LedgerModule Module Wrapper

TEAx module for Conversion_Subsystem_Ledger calculation.

*Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. Numerical semantics are the complete calculate function in exploration/component_alternatives/bodies/component_alternatives_thermal/conversion_subsystem_ledger_impl.py; units MW, K/degC, kg/s, Pa, MW/K, USD2025 and years as named.

Inputs:
    - actual_heat_in: actual_heat_in parameter
    - capital3_in: capital3_in parameter
    - water3_in: water3_in parameter
    - capital5_in: capital5_in parameter
    - scope_correction_in: scope_correction_in parameter
    - controller_capital_in: controller_capital_in parameter
    - rate_in: rate_in parameter
    - rejected3_in: rejected3_in parameter
    - capital8_in: capital8_in parameter
    - rejected2_in: rejected2_in parameter
    - water1_in: water1_in parameter
    - capital7_in: capital7_in parameter
    - bundle_event_in: bundle_event_in parameter
    - capital4_in: capital4_in parameter
    - gross_in: gross_in parameter
    - shaft_import_in: shaft_import_in parameter
    - capital10_in: capital10_in parameter
    - capital1_in: capital1_in parameter
    - replacement_fraction_in: replacement_fraction_in parameter
    - currency_factor_in: currency_factor_in parameter
    - availability_in: availability_in parameter
    - available_heat_in: available_heat_in parameter
    - rejected1_in: rejected1_in parameter
    - annual_service_fraction_in: annual_service_fraction_in parameter
    - capital9_in: capital9_in parameter
    - water2_in: water2_in parameter
    - salt_stock_cost_in: salt_stock_cost_in parameter
    - salt_removal_in: salt_removal_in parameter
    - salt_vendor_in: salt_vendor_in parameter
    - bundle_life_in: bundle_life_in parameter
    - capital6_in: capital6_in parameter
    - makeup_fraction_in: makeup_fraction_in parameter
    - steam_pumps_in: steam_pumps_in parameter
    - salt_installation_in: salt_installation_in parameter
    - common_source_pv_in: common_source_pv_in parameter
    - separately_replaced_capital_in: separately_replaced_capital_in parameter
    - machine_life_in: machine_life_in parameter
    - salt_pumps_in: salt_pumps_in parameter
    - capital2_in: capital2_in parameter
    - water4_in: water4_in parameter
    - controller_electric_in: controller_electric_in parameter
    - years_in: years_in parameter
    - rejected4_in: rejected4_in parameter
    - replacement_year_in: replacement_year_in parameter

Outputs:
    - annual_energy: annual_energy result
    - cost_per_net_MWh: cost_per_net_MWh result
    - capital_10: capital_10 result
    - gross_electric: gross_electric result
    - conversion_energy_residual: conversion_energy_residual result
    - energy_residual: energy_residual result
    - replacement_pv: replacement_pv result
    - capital_3: capital_3 result
    - economic_defined: economic_defined result
    - electrical_load: electrical_load result
    - accounted_pv: accounted_pv result
    - capital_4: capital_4 result
    - capital_1: capital_1 result
    - annual_service: annual_service result
    - total_rejected: total_rejected result
    - recurring_base: recurring_base result
    - unremoved_heat: unremoved_heat result
    - capital_9: capital_9 result
    - corrected_pv: corrected_pv result
    - machine_replacement_pv: machine_replacement_pv result
    - capital_7: capital_7 result
    - net_electric: net_electric result
    - annuity_factor: annuity_factor result
    - capital_2: capital_2 result
    - capital_6: capital_6 result
    - annual_makeup: annual_makeup result
    - bundle_replacement_pv: bundle_replacement_pv result
    - conversion_replacement_pv: conversion_replacement_pv result
    - capital_5: capital_5 result
    - capital_8: capital_8 result
    - energy_tolerance: energy_tolerance result
    - discounted_energy: discounted_energy result
    - capital_total: capital_total result

SysML Source: root-0/component_alternatives_thermal.sysml:3

SysML Source: root-0/component_alternatives_thermal.sysml:3

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/component_alternatives_thermal/conversion_subsystem_ledger_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from component_alternatives_tea.primitives import Float
from component_alternatives_tea.schemas.conversion_subsystem_ledger_output import Conversion_Subsystem_LedgerOutput


class Conversion_Subsystem_LedgerInput(BaseModel):
    """Input model for Conversion_Subsystem_LedgerModule.

    Attributes:
        actual_heat_in: actual_heat_in input
        capital3_in: capital3_in input
        water3_in: water3_in input
        capital5_in: capital5_in input
        scope_correction_in: scope_correction_in input
        controller_capital_in: controller_capital_in input
        rate_in: rate_in input
        rejected3_in: rejected3_in input
        capital8_in: capital8_in input
        rejected2_in: rejected2_in input
        water1_in: water1_in input
        capital7_in: capital7_in input
        bundle_event_in: bundle_event_in input
        capital4_in: capital4_in input
        gross_in: gross_in input
        shaft_import_in: shaft_import_in input
        capital10_in: capital10_in input
        capital1_in: capital1_in input
        replacement_fraction_in: replacement_fraction_in input
        currency_factor_in: currency_factor_in input
        availability_in: availability_in input
        available_heat_in: available_heat_in input
        rejected1_in: rejected1_in input
        annual_service_fraction_in: annual_service_fraction_in input
        capital9_in: capital9_in input
        water2_in: water2_in input
        salt_stock_cost_in: salt_stock_cost_in input
        salt_removal_in: salt_removal_in input
        salt_vendor_in: salt_vendor_in input
        bundle_life_in: bundle_life_in input
        capital6_in: capital6_in input
        makeup_fraction_in: makeup_fraction_in input
        steam_pumps_in: steam_pumps_in input
        salt_installation_in: salt_installation_in input
        common_source_pv_in: common_source_pv_in input
        separately_replaced_capital_in: separately_replaced_capital_in input
        machine_life_in: machine_life_in input
        salt_pumps_in: salt_pumps_in input
        capital2_in: capital2_in input
        water4_in: water4_in input
        controller_electric_in: controller_electric_in input
        years_in: years_in input
        rejected4_in: rejected4_in input
        replacement_year_in: replacement_year_in input
    """
    actual_heat_in: float = Field(..., description="actual_heat_in input")
    capital3_in: float = Field(..., description="capital3_in input")
    water3_in: float = Field(..., description="water3_in input")
    capital5_in: float = Field(..., description="capital5_in input")
    scope_correction_in: float = Field(..., description="scope_correction_in input")
    controller_capital_in: float = Field(..., description="controller_capital_in input")
    rate_in: float = Field(..., description="rate_in input")
    rejected3_in: float = Field(..., description="rejected3_in input")
    capital8_in: float = Field(..., description="capital8_in input")
    rejected2_in: float = Field(..., description="rejected2_in input")
    water1_in: float = Field(..., description="water1_in input")
    capital7_in: float = Field(..., description="capital7_in input")
    bundle_event_in: float = Field(..., description="bundle_event_in input")
    capital4_in: float = Field(..., description="capital4_in input")
    gross_in: float = Field(..., description="gross_in input")
    shaft_import_in: float = Field(..., description="shaft_import_in input")
    capital10_in: float = Field(..., description="capital10_in input")
    capital1_in: float = Field(..., description="capital1_in input")
    replacement_fraction_in: float = Field(..., description="replacement_fraction_in input")
    currency_factor_in: float = Field(..., description="currency_factor_in input")
    availability_in: float = Field(..., description="availability_in input")
    available_heat_in: float = Field(..., description="available_heat_in input")
    rejected1_in: float = Field(..., description="rejected1_in input")
    annual_service_fraction_in: float = Field(..., description="annual_service_fraction_in input")
    capital9_in: float = Field(..., description="capital9_in input")
    water2_in: float = Field(..., description="water2_in input")
    salt_stock_cost_in: float = Field(..., description="salt_stock_cost_in input")
    salt_removal_in: float = Field(..., description="salt_removal_in input")
    salt_vendor_in: float = Field(..., description="salt_vendor_in input")
    bundle_life_in: float = Field(..., description="bundle_life_in input")
    capital6_in: float = Field(..., description="capital6_in input")
    makeup_fraction_in: float = Field(..., description="makeup_fraction_in input")
    steam_pumps_in: float = Field(..., description="steam_pumps_in input")
    salt_installation_in: float = Field(..., description="salt_installation_in input")
    common_source_pv_in: float = Field(..., description="common_source_pv_in input")
    separately_replaced_capital_in: float = Field(..., description="separately_replaced_capital_in input")
    machine_life_in: float = Field(..., description="machine_life_in input")
    salt_pumps_in: float = Field(..., description="salt_pumps_in input")
    capital2_in: float = Field(..., description="capital2_in input")
    water4_in: float = Field(..., description="water4_in input")
    controller_electric_in: float = Field(..., description="controller_electric_in input")
    years_in: float = Field(..., description="years_in input")
    rejected4_in: float = Field(..., description="rejected4_in input")
    replacement_year_in: float = Field(..., description="replacement_year_in input")


class Conversion_Subsystem_LedgerModule(ModuleBase[Conversion_Subsystem_LedgerInput, Conversion_Subsystem_LedgerOutput]):
    """TEAx module for Conversion_Subsystem_Ledger calculation.

*Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. Numerical semantics are the complete calculate function in exploration/component_alternatives/bodies/component_alternatives_thermal/conversion_subsystem_ledger_impl.py; units MW, K/degC, kg/s, Pa, MW/K, USD2025 and years as named.

Inputs:
    - actual_heat_in: actual_heat_in parameter
    - capital3_in: capital3_in parameter
    - water3_in: water3_in parameter
    - capital5_in: capital5_in parameter
    - scope_correction_in: scope_correction_in parameter
    - controller_capital_in: controller_capital_in parameter
    - rate_in: rate_in parameter
    - rejected3_in: rejected3_in parameter
    - capital8_in: capital8_in parameter
    - rejected2_in: rejected2_in parameter
    - water1_in: water1_in parameter
    - capital7_in: capital7_in parameter
    - bundle_event_in: bundle_event_in parameter
    - capital4_in: capital4_in parameter
    - gross_in: gross_in parameter
    - shaft_import_in: shaft_import_in parameter
    - capital10_in: capital10_in parameter
    - capital1_in: capital1_in parameter
    - replacement_fraction_in: replacement_fraction_in parameter
    - currency_factor_in: currency_factor_in parameter
    - availability_in: availability_in parameter
    - available_heat_in: available_heat_in parameter
    - rejected1_in: rejected1_in parameter
    - annual_service_fraction_in: annual_service_fraction_in parameter
    - capital9_in: capital9_in parameter
    - water2_in: water2_in parameter
    - salt_stock_cost_in: salt_stock_cost_in parameter
    - salt_removal_in: salt_removal_in parameter
    - salt_vendor_in: salt_vendor_in parameter
    - bundle_life_in: bundle_life_in parameter
    - capital6_in: capital6_in parameter
    - makeup_fraction_in: makeup_fraction_in parameter
    - steam_pumps_in: steam_pumps_in parameter
    - salt_installation_in: salt_installation_in parameter
    - common_source_pv_in: common_source_pv_in parameter
    - separately_replaced_capital_in: separately_replaced_capital_in parameter
    - machine_life_in: machine_life_in parameter
    - salt_pumps_in: salt_pumps_in parameter
    - capital2_in: capital2_in parameter
    - water4_in: water4_in parameter
    - controller_electric_in: controller_electric_in parameter
    - years_in: years_in parameter
    - rejected4_in: rejected4_in parameter
    - replacement_year_in: replacement_year_in parameter

Outputs:
    - annual_energy: annual_energy result
    - cost_per_net_MWh: cost_per_net_MWh result
    - capital_10: capital_10 result
    - gross_electric: gross_electric result
    - conversion_energy_residual: conversion_energy_residual result
    - energy_residual: energy_residual result
    - replacement_pv: replacement_pv result
    - capital_3: capital_3 result
    - economic_defined: economic_defined result
    - electrical_load: electrical_load result
    - accounted_pv: accounted_pv result
    - capital_4: capital_4 result
    - capital_1: capital_1 result
    - annual_service: annual_service result
    - total_rejected: total_rejected result
    - recurring_base: recurring_base result
    - unremoved_heat: unremoved_heat result
    - capital_9: capital_9 result
    - corrected_pv: corrected_pv result
    - machine_replacement_pv: machine_replacement_pv result
    - capital_7: capital_7 result
    - net_electric: net_electric result
    - annuity_factor: annuity_factor result
    - capital_2: capital_2 result
    - capital_6: capital_6 result
    - annual_makeup: annual_makeup result
    - bundle_replacement_pv: bundle_replacement_pv result
    - conversion_replacement_pv: conversion_replacement_pv result
    - capital_5: capital_5 result
    - capital_8: capital_8 result
    - energy_tolerance: energy_tolerance result
    - discounted_energy: discounted_energy result
    - capital_total: capital_total result

SysML Source: root-0/component_alternatives_thermal.sysml:3

    SysML Source: root-0/component_alternatives_thermal.sysml:3

    Calculation Specification:
        available_heat_in = 0.0
        actual_heat_in = 0.0
        gross_in = 0.0
        shaft_import_in = 0.0
        steam_pumps_in = 0.0
        salt_pumps_in = 0.0
        water1_in = 0.0
        water2_in = 0.0
        water3_in = 0.0
        water4_in = 0.0
        controller_electric_in = 0.1
        rejected1_in = 0.0
        rejected2_in = 0.0
        rejected3_in = 0.0
        rejected4_in = 0.0
        capital1_in = 0.0
        capital2_in = 0.0
        capital3_in = 0.0
        capital4_in = 0.0
        capital5_in = 0.0
        capital6_in = 0.0
        capital7_in = 0.0
        capital8_in = 0.0
        capital9_in = 0.0
        capital10_in = 0.0
        currency_factor_in = 1.0
        controller_capital_in = 10000000.0
        separately_replaced_capital_in = 0.0
        salt_vendor_in = 0.0
        salt_installation_in = 0.0
        salt_removal_in = 0.0
        bundle_event_in = 0.0
        salt_stock_cost_in = 0.0
        machine_life_in = 10.0
        bundle_life_in = 15.0
        makeup_fraction_in = 0.001
        annual_service_fraction_in = 0.02
        replacement_fraction_in = 0.2
        replacement_year_in = 15.0
        rate_in = 0.05
        years_in = 30.0
        availability_in = 0.85
        scope_correction_in = 0.0
        common_source_pv_in = 0.0
        
Documentation:
*Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. Numerical semantics are the complete calculate function in exploration/component_alternatives/bodies/component_alternatives_thermal/conversion_subsystem_ledger_impl.py; units MW, K/degC, kg/s, Pa, MW/K, USD2025 and years as named.

    IMPLEMENTATION: See component_alternatives_tea.handwritten.component_alternatives_thermal.conversion_subsystem_ledger_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts annual_energy, cost_per_net_MWh, capital_10, gross_electric, conversion_energy_residual, energy_residual, replacement_pv, capital_3, economic_defined, electrical_load, accounted_pv, capital_4, capital_1, annual_service, total_rejected, recurring_base, unremoved_heat, capital_9, corrected_pv, machine_replacement_pv, capital_7, net_electric, annuity_factor, capital_2, capital_6, annual_makeup, bundle_replacement_pv, conversion_replacement_pv, capital_5, capital_8, energy_tolerance, discounted_energy, capital_total fields to separate channels.
    """

    name: str = "Conversion_Subsystem_LedgerModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, actual_heat_in: float, capital3_in: float, water3_in: float, capital5_in: float, scope_correction_in: float, controller_capital_in: float, rate_in: float, rejected3_in: float, capital8_in: float, rejected2_in: float, water1_in: float, capital7_in: float, bundle_event_in: float, capital4_in: float, gross_in: float, shaft_import_in: float, capital10_in: float, capital1_in: float, replacement_fraction_in: float, currency_factor_in: float, availability_in: float, available_heat_in: float, rejected1_in: float, annual_service_fraction_in: float, capital9_in: float, water2_in: float, salt_stock_cost_in: float, salt_removal_in: float, salt_vendor_in: float, bundle_life_in: float, capital6_in: float, makeup_fraction_in: float, steam_pumps_in: float, salt_installation_in: float, common_source_pv_in: float, separately_replaced_capital_in: float, machine_life_in: float, salt_pumps_in: float, capital2_in: float, water4_in: float, controller_electric_in: float, years_in: float, rejected4_in: float, replacement_year_in: float    ) -> Conversion_Subsystem_LedgerInput:
        """Validate inputs and fill defaults.

        Args:
            actual_heat_in: actual_heat_in input
            capital3_in: capital3_in input
            water3_in: water3_in input
            capital5_in: capital5_in input
            scope_correction_in: scope_correction_in input
            controller_capital_in: controller_capital_in input
            rate_in: rate_in input
            rejected3_in: rejected3_in input
            capital8_in: capital8_in input
            rejected2_in: rejected2_in input
            water1_in: water1_in input
            capital7_in: capital7_in input
            bundle_event_in: bundle_event_in input
            capital4_in: capital4_in input
            gross_in: gross_in input
            shaft_import_in: shaft_import_in input
            capital10_in: capital10_in input
            capital1_in: capital1_in input
            replacement_fraction_in: replacement_fraction_in input
            currency_factor_in: currency_factor_in input
            availability_in: availability_in input
            available_heat_in: available_heat_in input
            rejected1_in: rejected1_in input
            annual_service_fraction_in: annual_service_fraction_in input
            capital9_in: capital9_in input
            water2_in: water2_in input
            salt_stock_cost_in: salt_stock_cost_in input
            salt_removal_in: salt_removal_in input
            salt_vendor_in: salt_vendor_in input
            bundle_life_in: bundle_life_in input
            capital6_in: capital6_in input
            makeup_fraction_in: makeup_fraction_in input
            steam_pumps_in: steam_pumps_in input
            salt_installation_in: salt_installation_in input
            common_source_pv_in: common_source_pv_in input
            separately_replaced_capital_in: separately_replaced_capital_in input
            machine_life_in: machine_life_in input
            salt_pumps_in: salt_pumps_in input
            capital2_in: capital2_in input
            water4_in: water4_in input
            controller_electric_in: controller_electric_in input
            years_in: years_in input
            rejected4_in: rejected4_in input
            replacement_year_in: replacement_year_in input

        Returns:
            Validated input model
        """
        return Conversion_Subsystem_LedgerInput(actual_heat_in=actual_heat_in, capital3_in=capital3_in, water3_in=water3_in, capital5_in=capital5_in, scope_correction_in=scope_correction_in, controller_capital_in=controller_capital_in, rate_in=rate_in, rejected3_in=rejected3_in, capital8_in=capital8_in, rejected2_in=rejected2_in, water1_in=water1_in, capital7_in=capital7_in, bundle_event_in=bundle_event_in, capital4_in=capital4_in, gross_in=gross_in, shaft_import_in=shaft_import_in, capital10_in=capital10_in, capital1_in=capital1_in, replacement_fraction_in=replacement_fraction_in, currency_factor_in=currency_factor_in, availability_in=availability_in, available_heat_in=available_heat_in, rejected1_in=rejected1_in, annual_service_fraction_in=annual_service_fraction_in, capital9_in=capital9_in, water2_in=water2_in, salt_stock_cost_in=salt_stock_cost_in, salt_removal_in=salt_removal_in, salt_vendor_in=salt_vendor_in, bundle_life_in=bundle_life_in, capital6_in=capital6_in, makeup_fraction_in=makeup_fraction_in, steam_pumps_in=steam_pumps_in, salt_installation_in=salt_installation_in, common_source_pv_in=common_source_pv_in, separately_replaced_capital_in=separately_replaced_capital_in, machine_life_in=machine_life_in, salt_pumps_in=salt_pumps_in, capital2_in=capital2_in, water4_in=water4_in, controller_electric_in=controller_electric_in, years_in=years_in, rejected4_in=rejected4_in, replacement_year_in=replacement_year_in)

    def run(
        self, actual_heat_in: float, capital3_in: float, water3_in: float, capital5_in: float, scope_correction_in: float, controller_capital_in: float, rate_in: float, rejected3_in: float, capital8_in: float, rejected2_in: float, water1_in: float, capital7_in: float, bundle_event_in: float, capital4_in: float, gross_in: float, shaft_import_in: float, capital10_in: float, capital1_in: float, replacement_fraction_in: float, currency_factor_in: float, availability_in: float, available_heat_in: float, rejected1_in: float, annual_service_fraction_in: float, capital9_in: float, water2_in: float, salt_stock_cost_in: float, salt_removal_in: float, salt_vendor_in: float, bundle_life_in: float, capital6_in: float, makeup_fraction_in: float, steam_pumps_in: float, salt_installation_in: float, common_source_pv_in: float, separately_replaced_capital_in: float, machine_life_in: float, salt_pumps_in: float, capital2_in: float, water4_in: float, controller_electric_in: float, years_in: float, rejected4_in: float, replacement_year_in: float    ) -> ModuleResult[Conversion_Subsystem_LedgerOutput]:
        """Execute calculation.

        Args:
            actual_heat_in: actual_heat_in input
            capital3_in: capital3_in input
            water3_in: water3_in input
            capital5_in: capital5_in input
            scope_correction_in: scope_correction_in input
            controller_capital_in: controller_capital_in input
            rate_in: rate_in input
            rejected3_in: rejected3_in input
            capital8_in: capital8_in input
            rejected2_in: rejected2_in input
            water1_in: water1_in input
            capital7_in: capital7_in input
            bundle_event_in: bundle_event_in input
            capital4_in: capital4_in input
            gross_in: gross_in input
            shaft_import_in: shaft_import_in input
            capital10_in: capital10_in input
            capital1_in: capital1_in input
            replacement_fraction_in: replacement_fraction_in input
            currency_factor_in: currency_factor_in input
            availability_in: availability_in input
            available_heat_in: available_heat_in input
            rejected1_in: rejected1_in input
            annual_service_fraction_in: annual_service_fraction_in input
            capital9_in: capital9_in input
            water2_in: water2_in input
            salt_stock_cost_in: salt_stock_cost_in input
            salt_removal_in: salt_removal_in input
            salt_vendor_in: salt_vendor_in input
            bundle_life_in: bundle_life_in input
            capital6_in: capital6_in input
            makeup_fraction_in: makeup_fraction_in input
            steam_pumps_in: steam_pumps_in input
            salt_installation_in: salt_installation_in input
            common_source_pv_in: common_source_pv_in input
            separately_replaced_capital_in: separately_replaced_capital_in input
            machine_life_in: machine_life_in input
            salt_pumps_in: salt_pumps_in input
            capital2_in: capital2_in input
            water4_in: water4_in input
            controller_electric_in: controller_electric_in input
            years_in: years_in input
            rejected4_in: rejected4_in input
            replacement_year_in: replacement_year_in input

        Returns:
            Module result with Conversion_Subsystem_LedgerOutput (annual_energy, cost_per_net_MWh, capital_10, gross_electric, conversion_energy_residual, energy_residual, replacement_pv, capital_3, economic_defined, electrical_load, accounted_pv, capital_4, capital_1, annual_service, total_rejected, recurring_base, unremoved_heat, capital_9, corrected_pv, machine_replacement_pv, capital_7, net_electric, annuity_factor, capital_2, capital_6, annual_makeup, bundle_replacement_pv, conversion_replacement_pv, capital_5, capital_8, energy_tolerance, discounted_energy, capital_total)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(actual_heat_in, capital3_in, water3_in, capital5_in, scope_correction_in, controller_capital_in, rate_in, rejected3_in, capital8_in, rejected2_in, water1_in, capital7_in, bundle_event_in, capital4_in, gross_in, shaft_import_in, capital10_in, capital1_in, replacement_fraction_in, currency_factor_in, availability_in, available_heat_in, rejected1_in, annual_service_fraction_in, capital9_in, water2_in, salt_stock_cost_in, salt_removal_in, salt_vendor_in, bundle_life_in, capital6_in, makeup_fraction_in, steam_pumps_in, salt_installation_in, common_source_pv_in, separately_replaced_capital_in, machine_life_in, salt_pumps_in, capital2_in, water4_in, controller_electric_in, years_in, rejected4_in, replacement_year_in)

        # Import handwritten implementation
        from component_alternatives_tea.handwritten.component_alternatives_thermal.conversion_subsystem_ledger_impl import (
            run_conversion_subsystem_ledger,
        )

        # Execute implementation - returns tuple of values
        annual_energy, cost_per_net_MWh, capital_10, gross_electric, conversion_energy_residual, energy_residual, replacement_pv, capital_3, economic_defined, electrical_load, accounted_pv, capital_4, capital_1, annual_service, total_rejected, recurring_base, unremoved_heat, capital_9, corrected_pv, machine_replacement_pv, capital_7, net_electric, annuity_factor, capital_2, capital_6, annual_makeup, bundle_replacement_pv, conversion_replacement_pv, capital_5, capital_8, energy_tolerance, discounted_energy, capital_total = run_conversion_subsystem_ledger(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Conversion_Subsystem_LedgerOutput(
                annual_energy=annual_energy,
                cost_per_net_MWh=cost_per_net_MWh,
                capital_10=capital_10,
                gross_electric=gross_electric,
                conversion_energy_residual=conversion_energy_residual,
                energy_residual=energy_residual,
                replacement_pv=replacement_pv,
                capital_3=capital_3,
                economic_defined=economic_defined,
                electrical_load=electrical_load,
                accounted_pv=accounted_pv,
                capital_4=capital_4,
                capital_1=capital_1,
                annual_service=annual_service,
                total_rejected=total_rejected,
                recurring_base=recurring_base,
                unremoved_heat=unremoved_heat,
                capital_9=capital_9,
                corrected_pv=corrected_pv,
                machine_replacement_pv=machine_replacement_pv,
                capital_7=capital_7,
                net_electric=net_electric,
                annuity_factor=annuity_factor,
                capital_2=capital_2,
                capital_6=capital_6,
                annual_makeup=annual_makeup,
                bundle_replacement_pv=bundle_replacement_pv,
                conversion_replacement_pv=conversion_replacement_pv,
                capital_5=capital_5,
                capital_8=capital_8,
                energy_tolerance=energy_tolerance,
                discounted_energy=discounted_energy,
                capital_total=capital_total,
            )
        )
