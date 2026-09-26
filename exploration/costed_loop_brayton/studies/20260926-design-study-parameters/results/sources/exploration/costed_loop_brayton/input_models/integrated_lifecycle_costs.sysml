package integrated_lifecycle_costs {
    private import ScalarValues::*;
    calc def 'Lifecycle Cashflow Accounts' {
        doc /* **Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22. */
        in attribute overnight_in : Real;
        in attribute net_power_in : Real;
        in attribute annual_energy_in : Real;
        in attribute annual_operating_in : Real;
        in attribute om_in : Real;
        in attribute tritium_in : Real;
        in attribute deuterium_in : Real;
        in attribute consumables_in : Real;
        in attribute imports_in : Real;
        in attribute supply_service_in : Real;
        in attribute crf_in : Real;
        in attribute discount_in : Real;
        in attribute construction_years_in : Real;
        in attribute plant_years_in : Real;
        in attribute availability_in : Real;
        in attribute event_cost_in : Real;
        in attribute interval_years_in : Real;
        in attribute event_count_in : Real;
        in attribute terminal_fraction_in : Real;
        in attribute salvage_fraction_in : Real;
        in attribute other_overhaul_fraction_in : Real;
        in attribute other_overhaul_year_in : Real;
        in attribute annual_burn_in : Real;
        in attribute annual_loss_in : Real;
        in attribute annual_decay_in : Real;
        in attribute annual_feed_in : Real;
        in attribute external_shortfall_in : Real;
        out attribute noncapital_annual : Real;
        out attribute financed_capital : Real;
        out attribute idc : Real;
        out attribute annual_capital : Real;
        out attribute annual_energy : Real;
        out attribute lifetime_energy : Real;
        out attribute pv_energy : Real;
        out attribute pv_operating : Real;
        out attribute pv_supply : Real;
        out attribute pv_replacement : Real;
        out attribute pv_other_overhaul : Real;
        out attribute gross_terminal : Real;
        out attribute salvage : Real;
        out attribute pv_terminal_gross : Real;
        out attribute pv_salvage : Real;
        out attribute pv_terminal_net : Real;
        out attribute other_overhaul_cost : Real;
        out attribute other_overhaul_occurs : Real;
        out attribute pv_total_cost : Real;
        out attribute lcoe_sum : Real;
        out attribute capital_lcoe : Real;
        out attribute om_lcoe : Real;
        out attribute tritium_lcoe : Real;
        out attribute deuterium_lcoe : Real;
        out attribute consumables_lcoe : Real;
        out attribute imports_lcoe : Real;
        out attribute supply_lcoe : Real;
        out attribute replacement_lcoe : Real;
        out attribute other_overhaul_lcoe : Real;
        out attribute terminal_lcoe : Real;
        out attribute salvage_lcoe : Real;
        out attribute gross_makeup : Real;
        out attribute new_feed : Real;
        out attribute external_shortfall : Real;
        out attribute curtailed_feed : Real;
        out attribute supply_supported : Real;
        out attribute breeding_supported : Real;
        out attribute financial_defined : Real;
        out attribute currency_year : Real;
        out attribute real_convention : Real;
    }
    calc def 'Supplied Annual Energy' {
        doc /* **Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22. */
        in attribute net_power_in : Real;
        in attribute availability_in : Real;
        out attribute annual_energy : Real = 8760.0 * net_power_in * availability_in;
    }
    calc def 'Already Financed Duration' {
        doc /* **Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: source comparison financing-once invariant; focused independent review. **Basis**: supplied already-financed capital permits exactly zero additional construction duration. **Last Updated**: 2026-09-22. */
        in attribute years_in : Real;
        out attribute years : Real;
    }
}
