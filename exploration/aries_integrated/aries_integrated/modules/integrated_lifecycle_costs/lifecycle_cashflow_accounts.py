"""Lifecycle_Cashflow_AccountsModule Module Wrapper

TEAx module for Lifecycle_Cashflow_Accounts calculation.

*Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22.

Inputs:
    - crf_in: crf_in parameter
    - salvage_fraction_in: salvage_fraction_in parameter
    - annual_operating_in: annual_operating_in parameter
    - annual_energy_in: annual_energy_in parameter
    - event_count_in: event_count_in parameter
    - other_overhaul_fraction_in: other_overhaul_fraction_in parameter
    - annual_decay_in: annual_decay_in parameter
    - external_shortfall_in: external_shortfall_in parameter
    - discount_in: discount_in parameter
    - imports_in: imports_in parameter
    - annual_feed_in: annual_feed_in parameter
    - availability_in: availability_in parameter
    - supply_service_in: supply_service_in parameter
    - construction_years_in: construction_years_in parameter
    - other_overhaul_year_in: other_overhaul_year_in parameter
    - deuterium_in: deuterium_in parameter
    - overnight_in: overnight_in parameter
    - annual_loss_in: annual_loss_in parameter
    - tritium_in: tritium_in parameter
    - event_cost_in: event_cost_in parameter
    - plant_years_in: plant_years_in parameter
    - om_in: om_in parameter
    - annual_burn_in: annual_burn_in parameter
    - interval_years_in: interval_years_in parameter
    - net_power_in: net_power_in parameter
    - terminal_fraction_in: terminal_fraction_in parameter
    - consumables_in: consumables_in parameter

Outputs:
    - real_convention: real_convention result
    - other_overhaul_cost: other_overhaul_cost result
    - gross_makeup: gross_makeup result
    - supply_lcoe: supply_lcoe result
    - other_overhaul_lcoe: other_overhaul_lcoe result
    - lcoe_sum: lcoe_sum result
    - noncapital_annual: noncapital_annual result
    - pv_total_cost: pv_total_cost result
    - breeding_supported: breeding_supported result
    - pv_supply: pv_supply result
    - other_overhaul_occurs: other_overhaul_occurs result
    - curtailed_feed: curtailed_feed result
    - replacement_lcoe: replacement_lcoe result
    - gross_terminal: gross_terminal result
    - salvage_lcoe: salvage_lcoe result
    - financial_defined: financial_defined result
    - idc: idc result
    - annual_capital: annual_capital result
    - pv_replacement: pv_replacement result
    - supply_supported: supply_supported result
    - om_lcoe: om_lcoe result
    - pv_terminal_gross: pv_terminal_gross result
    - tritium_lcoe: tritium_lcoe result
    - capital_lcoe: capital_lcoe result
    - annual_energy: annual_energy result
    - external_shortfall: external_shortfall result
    - pv_salvage: pv_salvage result
    - pv_operating: pv_operating result
    - new_feed: new_feed result
    - lifetime_energy: lifetime_energy result
    - financed_capital: financed_capital result
    - pv_other_overhaul: pv_other_overhaul result
    - terminal_lcoe: terminal_lcoe result
    - currency_year: currency_year result
    - pv_energy: pv_energy result
    - salvage: salvage result
    - deuterium_lcoe: deuterium_lcoe result
    - pv_terminal_net: pv_terminal_net result
    - imports_lcoe: imports_lcoe result
    - consumables_lcoe: consumables_lcoe result

SysML Source: root-0/integrated_lifecycle_costs.sysml:3

SysML Source: root-0/integrated_lifecycle_costs.sysml:3

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/integrated_lifecycle_costs/lifecycle_cashflow_accounts_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from aries_integrated.primitives import Float
from aries_integrated.schemas.lifecycle_cashflow_accounts_output import Lifecycle_Cashflow_AccountsOutput


class Lifecycle_Cashflow_AccountsInput(BaseModel):
    """Input model for Lifecycle_Cashflow_AccountsModule.

    Attributes:
        crf_in: crf_in input
        salvage_fraction_in: salvage_fraction_in input
        annual_operating_in: annual_operating_in input
        annual_energy_in: annual_energy_in input
        event_count_in: event_count_in input
        other_overhaul_fraction_in: other_overhaul_fraction_in input
        annual_decay_in: annual_decay_in input
        external_shortfall_in: external_shortfall_in input
        discount_in: discount_in input
        imports_in: imports_in input
        annual_feed_in: annual_feed_in input
        availability_in: availability_in input
        supply_service_in: supply_service_in input
        construction_years_in: construction_years_in input
        other_overhaul_year_in: other_overhaul_year_in input
        deuterium_in: deuterium_in input
        overnight_in: overnight_in input
        annual_loss_in: annual_loss_in input
        tritium_in: tritium_in input
        event_cost_in: event_cost_in input
        plant_years_in: plant_years_in input
        om_in: om_in input
        annual_burn_in: annual_burn_in input
        interval_years_in: interval_years_in input
        net_power_in: net_power_in input
        terminal_fraction_in: terminal_fraction_in input
        consumables_in: consumables_in input
    """
    crf_in: float = Field(..., description="crf_in input")
    salvage_fraction_in: float = Field(..., description="salvage_fraction_in input")
    annual_operating_in: float = Field(..., description="annual_operating_in input")
    annual_energy_in: float = Field(..., description="annual_energy_in input")
    event_count_in: float = Field(..., description="event_count_in input")
    other_overhaul_fraction_in: float = Field(..., description="other_overhaul_fraction_in input")
    annual_decay_in: float = Field(..., description="annual_decay_in input")
    external_shortfall_in: float = Field(..., description="external_shortfall_in input")
    discount_in: float = Field(..., description="discount_in input")
    imports_in: float = Field(..., description="imports_in input")
    annual_feed_in: float = Field(..., description="annual_feed_in input")
    availability_in: float = Field(..., description="availability_in input")
    supply_service_in: float = Field(..., description="supply_service_in input")
    construction_years_in: float = Field(..., description="construction_years_in input")
    other_overhaul_year_in: float = Field(..., description="other_overhaul_year_in input")
    deuterium_in: float = Field(..., description="deuterium_in input")
    overnight_in: float = Field(..., description="overnight_in input")
    annual_loss_in: float = Field(..., description="annual_loss_in input")
    tritium_in: float = Field(..., description="tritium_in input")
    event_cost_in: float = Field(..., description="event_cost_in input")
    plant_years_in: float = Field(..., description="plant_years_in input")
    om_in: float = Field(..., description="om_in input")
    annual_burn_in: float = Field(..., description="annual_burn_in input")
    interval_years_in: float = Field(..., description="interval_years_in input")
    net_power_in: float = Field(..., description="net_power_in input")
    terminal_fraction_in: float = Field(..., description="terminal_fraction_in input")
    consumables_in: float = Field(..., description="consumables_in input")


class Lifecycle_Cashflow_AccountsModule(ModuleBase[Lifecycle_Cashflow_AccountsInput, Lifecycle_Cashflow_AccountsOutput]):
    """TEAx module for Lifecycle_Cashflow_Accounts calculation.

*Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22.

Inputs:
    - crf_in: crf_in parameter
    - salvage_fraction_in: salvage_fraction_in parameter
    - annual_operating_in: annual_operating_in parameter
    - annual_energy_in: annual_energy_in parameter
    - event_count_in: event_count_in parameter
    - other_overhaul_fraction_in: other_overhaul_fraction_in parameter
    - annual_decay_in: annual_decay_in parameter
    - external_shortfall_in: external_shortfall_in parameter
    - discount_in: discount_in parameter
    - imports_in: imports_in parameter
    - annual_feed_in: annual_feed_in parameter
    - availability_in: availability_in parameter
    - supply_service_in: supply_service_in parameter
    - construction_years_in: construction_years_in parameter
    - other_overhaul_year_in: other_overhaul_year_in parameter
    - deuterium_in: deuterium_in parameter
    - overnight_in: overnight_in parameter
    - annual_loss_in: annual_loss_in parameter
    - tritium_in: tritium_in parameter
    - event_cost_in: event_cost_in parameter
    - plant_years_in: plant_years_in parameter
    - om_in: om_in parameter
    - annual_burn_in: annual_burn_in parameter
    - interval_years_in: interval_years_in parameter
    - net_power_in: net_power_in parameter
    - terminal_fraction_in: terminal_fraction_in parameter
    - consumables_in: consumables_in parameter

Outputs:
    - real_convention: real_convention result
    - other_overhaul_cost: other_overhaul_cost result
    - gross_makeup: gross_makeup result
    - supply_lcoe: supply_lcoe result
    - other_overhaul_lcoe: other_overhaul_lcoe result
    - lcoe_sum: lcoe_sum result
    - noncapital_annual: noncapital_annual result
    - pv_total_cost: pv_total_cost result
    - breeding_supported: breeding_supported result
    - pv_supply: pv_supply result
    - other_overhaul_occurs: other_overhaul_occurs result
    - curtailed_feed: curtailed_feed result
    - replacement_lcoe: replacement_lcoe result
    - gross_terminal: gross_terminal result
    - salvage_lcoe: salvage_lcoe result
    - financial_defined: financial_defined result
    - idc: idc result
    - annual_capital: annual_capital result
    - pv_replacement: pv_replacement result
    - supply_supported: supply_supported result
    - om_lcoe: om_lcoe result
    - pv_terminal_gross: pv_terminal_gross result
    - tritium_lcoe: tritium_lcoe result
    - capital_lcoe: capital_lcoe result
    - annual_energy: annual_energy result
    - external_shortfall: external_shortfall result
    - pv_salvage: pv_salvage result
    - pv_operating: pv_operating result
    - new_feed: new_feed result
    - lifetime_energy: lifetime_energy result
    - financed_capital: financed_capital result
    - pv_other_overhaul: pv_other_overhaul result
    - terminal_lcoe: terminal_lcoe result
    - currency_year: currency_year result
    - pv_energy: pv_energy result
    - salvage: salvage result
    - deuterium_lcoe: deuterium_lcoe result
    - pv_terminal_net: pv_terminal_net result
    - imports_lcoe: imports_lcoe result
    - consumables_lcoe: consumables_lcoe result

SysML Source: root-0/integrated_lifecycle_costs.sysml:3

    SysML Source: root-0/integrated_lifecycle_costs.sysml:3

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22.

    IMPLEMENTATION: See aries_integrated.handwritten.integrated_lifecycle_costs.lifecycle_cashflow_accounts_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts real_convention, other_overhaul_cost, gross_makeup, supply_lcoe, other_overhaul_lcoe, lcoe_sum, noncapital_annual, pv_total_cost, breeding_supported, pv_supply, other_overhaul_occurs, curtailed_feed, replacement_lcoe, gross_terminal, salvage_lcoe, financial_defined, idc, annual_capital, pv_replacement, supply_supported, om_lcoe, pv_terminal_gross, tritium_lcoe, capital_lcoe, annual_energy, external_shortfall, pv_salvage, pv_operating, new_feed, lifetime_energy, financed_capital, pv_other_overhaul, terminal_lcoe, currency_year, pv_energy, salvage, deuterium_lcoe, pv_terminal_net, imports_lcoe, consumables_lcoe fields to separate channels.
    """

    name: str = "Lifecycle_Cashflow_AccountsModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, crf_in: float, salvage_fraction_in: float, annual_operating_in: float, annual_energy_in: float, event_count_in: float, other_overhaul_fraction_in: float, annual_decay_in: float, external_shortfall_in: float, discount_in: float, imports_in: float, annual_feed_in: float, availability_in: float, supply_service_in: float, construction_years_in: float, other_overhaul_year_in: float, deuterium_in: float, overnight_in: float, annual_loss_in: float, tritium_in: float, event_cost_in: float, plant_years_in: float, om_in: float, annual_burn_in: float, interval_years_in: float, net_power_in: float, terminal_fraction_in: float, consumables_in: float    ) -> Lifecycle_Cashflow_AccountsInput:
        """Validate inputs and fill defaults.

        Args:
            crf_in: crf_in input
            salvage_fraction_in: salvage_fraction_in input
            annual_operating_in: annual_operating_in input
            annual_energy_in: annual_energy_in input
            event_count_in: event_count_in input
            other_overhaul_fraction_in: other_overhaul_fraction_in input
            annual_decay_in: annual_decay_in input
            external_shortfall_in: external_shortfall_in input
            discount_in: discount_in input
            imports_in: imports_in input
            annual_feed_in: annual_feed_in input
            availability_in: availability_in input
            supply_service_in: supply_service_in input
            construction_years_in: construction_years_in input
            other_overhaul_year_in: other_overhaul_year_in input
            deuterium_in: deuterium_in input
            overnight_in: overnight_in input
            annual_loss_in: annual_loss_in input
            tritium_in: tritium_in input
            event_cost_in: event_cost_in input
            plant_years_in: plant_years_in input
            om_in: om_in input
            annual_burn_in: annual_burn_in input
            interval_years_in: interval_years_in input
            net_power_in: net_power_in input
            terminal_fraction_in: terminal_fraction_in input
            consumables_in: consumables_in input

        Returns:
            Validated input model
        """
        return Lifecycle_Cashflow_AccountsInput(crf_in=crf_in, salvage_fraction_in=salvage_fraction_in, annual_operating_in=annual_operating_in, annual_energy_in=annual_energy_in, event_count_in=event_count_in, other_overhaul_fraction_in=other_overhaul_fraction_in, annual_decay_in=annual_decay_in, external_shortfall_in=external_shortfall_in, discount_in=discount_in, imports_in=imports_in, annual_feed_in=annual_feed_in, availability_in=availability_in, supply_service_in=supply_service_in, construction_years_in=construction_years_in, other_overhaul_year_in=other_overhaul_year_in, deuterium_in=deuterium_in, overnight_in=overnight_in, annual_loss_in=annual_loss_in, tritium_in=tritium_in, event_cost_in=event_cost_in, plant_years_in=plant_years_in, om_in=om_in, annual_burn_in=annual_burn_in, interval_years_in=interval_years_in, net_power_in=net_power_in, terminal_fraction_in=terminal_fraction_in, consumables_in=consumables_in)

    def run(
        self, crf_in: float, salvage_fraction_in: float, annual_operating_in: float, annual_energy_in: float, event_count_in: float, other_overhaul_fraction_in: float, annual_decay_in: float, external_shortfall_in: float, discount_in: float, imports_in: float, annual_feed_in: float, availability_in: float, supply_service_in: float, construction_years_in: float, other_overhaul_year_in: float, deuterium_in: float, overnight_in: float, annual_loss_in: float, tritium_in: float, event_cost_in: float, plant_years_in: float, om_in: float, annual_burn_in: float, interval_years_in: float, net_power_in: float, terminal_fraction_in: float, consumables_in: float    ) -> ModuleResult[Lifecycle_Cashflow_AccountsOutput]:
        """Execute calculation.

        Args:
            crf_in: crf_in input
            salvage_fraction_in: salvage_fraction_in input
            annual_operating_in: annual_operating_in input
            annual_energy_in: annual_energy_in input
            event_count_in: event_count_in input
            other_overhaul_fraction_in: other_overhaul_fraction_in input
            annual_decay_in: annual_decay_in input
            external_shortfall_in: external_shortfall_in input
            discount_in: discount_in input
            imports_in: imports_in input
            annual_feed_in: annual_feed_in input
            availability_in: availability_in input
            supply_service_in: supply_service_in input
            construction_years_in: construction_years_in input
            other_overhaul_year_in: other_overhaul_year_in input
            deuterium_in: deuterium_in input
            overnight_in: overnight_in input
            annual_loss_in: annual_loss_in input
            tritium_in: tritium_in input
            event_cost_in: event_cost_in input
            plant_years_in: plant_years_in input
            om_in: om_in input
            annual_burn_in: annual_burn_in input
            interval_years_in: interval_years_in input
            net_power_in: net_power_in input
            terminal_fraction_in: terminal_fraction_in input
            consumables_in: consumables_in input

        Returns:
            Module result with Lifecycle_Cashflow_AccountsOutput (real_convention, other_overhaul_cost, gross_makeup, supply_lcoe, other_overhaul_lcoe, lcoe_sum, noncapital_annual, pv_total_cost, breeding_supported, pv_supply, other_overhaul_occurs, curtailed_feed, replacement_lcoe, gross_terminal, salvage_lcoe, financial_defined, idc, annual_capital, pv_replacement, supply_supported, om_lcoe, pv_terminal_gross, tritium_lcoe, capital_lcoe, annual_energy, external_shortfall, pv_salvage, pv_operating, new_feed, lifetime_energy, financed_capital, pv_other_overhaul, terminal_lcoe, currency_year, pv_energy, salvage, deuterium_lcoe, pv_terminal_net, imports_lcoe, consumables_lcoe)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(crf_in, salvage_fraction_in, annual_operating_in, annual_energy_in, event_count_in, other_overhaul_fraction_in, annual_decay_in, external_shortfall_in, discount_in, imports_in, annual_feed_in, availability_in, supply_service_in, construction_years_in, other_overhaul_year_in, deuterium_in, overnight_in, annual_loss_in, tritium_in, event_cost_in, plant_years_in, om_in, annual_burn_in, interval_years_in, net_power_in, terminal_fraction_in, consumables_in)

        # Import handwritten implementation
        from aries_integrated.handwritten.integrated_lifecycle_costs.lifecycle_cashflow_accounts_impl import (
            run_lifecycle_cashflow_accounts,
        )

        # Execute implementation - returns tuple of values
        real_convention, other_overhaul_cost, gross_makeup, supply_lcoe, other_overhaul_lcoe, lcoe_sum, noncapital_annual, pv_total_cost, breeding_supported, pv_supply, other_overhaul_occurs, curtailed_feed, replacement_lcoe, gross_terminal, salvage_lcoe, financial_defined, idc, annual_capital, pv_replacement, supply_supported, om_lcoe, pv_terminal_gross, tritium_lcoe, capital_lcoe, annual_energy, external_shortfall, pv_salvage, pv_operating, new_feed, lifetime_energy, financed_capital, pv_other_overhaul, terminal_lcoe, currency_year, pv_energy, salvage, deuterium_lcoe, pv_terminal_net, imports_lcoe, consumables_lcoe = run_lifecycle_cashflow_accounts(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Lifecycle_Cashflow_AccountsOutput(
                real_convention=real_convention,
                other_overhaul_cost=other_overhaul_cost,
                gross_makeup=gross_makeup,
                supply_lcoe=supply_lcoe,
                other_overhaul_lcoe=other_overhaul_lcoe,
                lcoe_sum=lcoe_sum,
                noncapital_annual=noncapital_annual,
                pv_total_cost=pv_total_cost,
                breeding_supported=breeding_supported,
                pv_supply=pv_supply,
                other_overhaul_occurs=other_overhaul_occurs,
                curtailed_feed=curtailed_feed,
                replacement_lcoe=replacement_lcoe,
                gross_terminal=gross_terminal,
                salvage_lcoe=salvage_lcoe,
                financial_defined=financial_defined,
                idc=idc,
                annual_capital=annual_capital,
                pv_replacement=pv_replacement,
                supply_supported=supply_supported,
                om_lcoe=om_lcoe,
                pv_terminal_gross=pv_terminal_gross,
                tritium_lcoe=tritium_lcoe,
                capital_lcoe=capital_lcoe,
                annual_energy=annual_energy,
                external_shortfall=external_shortfall,
                pv_salvage=pv_salvage,
                pv_operating=pv_operating,
                new_feed=new_feed,
                lifetime_energy=lifetime_energy,
                financed_capital=financed_capital,
                pv_other_overhaul=pv_other_overhaul,
                terminal_lcoe=terminal_lcoe,
                currency_year=currency_year,
                pv_energy=pv_energy,
                salvage=salvage,
                deuterium_lcoe=deuterium_lcoe,
                pv_terminal_net=pv_terminal_net,
                imports_lcoe=imports_lcoe,
                consumables_lcoe=consumables_lcoe,
            )
        )
