package aries_source_budget {
    private import ScalarValues::*;
    private import source_budget_accounting::*;
    private import mfe_account_costs::*;
    part land {
        doc /* Source: work/active/WI-088_aries-source-budget-cost-contribution/evidence/lyon-p707.png. Ref: TableIII 20 Land and land rights. Basis: supplied top-level USD2004 amount, million-dollar conversion explicit at capture. No descendant costs added and no repeated safety credit. Last Updated: 2026-09-21. */
        attribute selected_cost_usd2004 : Real = 12929000.000;
    }
    part structures {
        doc /* Source: work/active/WI-088_aries-source-budget-cost-contribution/evidence/lyon-p707.png. Ref: TableIII 21 Structures and site facilities. Basis: supplied top-level USD2004 amount, million-dollar conversion explicit at capture. No descendant costs added and no repeated safety credit. Last Updated: 2026-09-21. */
        attribute selected_cost_usd2004 : Real = 336133000.000;
    }
    part reactor_equipment {
        doc /* Source: work/active/WI-088_aries-source-budget-cost-contribution/evidence/lyon-p707.png. Ref: TableIII 22 Reactor plant equipment. Basis: supplied top-level USD2004 amount, million-dollar conversion explicit at capture. No descendant costs added and no repeated safety credit. Last Updated: 2026-09-21. */
        attribute selected_cost_usd2004 : Real = 1538817000.000;
    }
    part turbine_equipment {
        doc /* Source: work/active/WI-088_aries-source-budget-cost-contribution/evidence/lyon-p707.png. Ref: TableIII 23 Turbine plant equipment. Basis: supplied top-level USD2004 amount, million-dollar conversion explicit at capture. No descendant costs added and no repeated safety credit. Last Updated: 2026-09-21. */
        attribute selected_cost_usd2004 : Real = 314558000.000;
    }
    part electrical_equipment {
        doc /* Source: work/active/WI-088_aries-source-budget-cost-contribution/evidence/lyon-p707.png. Ref: TableIII 24 Electric plant equipment. Basis: supplied top-level USD2004 amount, million-dollar conversion explicit at capture. No descendant costs added and no repeated safety credit. Last Updated: 2026-09-21. */
        attribute selected_cost_usd2004 : Real = 138764000.000;
    }
    part miscellaneous_equipment {
        doc /* Source: work/active/WI-088_aries-source-budget-cost-contribution/evidence/lyon-p707.png. Ref: TableIII 25 Miscellaneous plant equipment. Basis: supplied top-level USD2004 amount, million-dollar conversion explicit at capture. No descendant costs added and no repeated safety credit. Last Updated: 2026-09-21. */
        attribute selected_cost_usd2004 : Real = 70958000.000;
    }
    part special_materials {
        doc /* Source: work/active/WI-088_aries-source-budget-cost-contribution/evidence/lyon-p707.png. Ref: TableIII 26 Special materials. Basis: supplied top-level USD2004 amount, million-dollar conversion explicit at capture. No descendant costs added and no repeated safety credit. Last Updated: 2026-09-21. */
        attribute selected_cost_usd2004 : Real = 151327000.000;
    }
    part heat_rejection {
        doc /* Source: work/active/WI-088_aries-source-budget-cost-contribution/evidence/lyon-p707.png. Ref: TableIII 27 Heat rejection. Basis: supplied top-level USD2004 amount, million-dollar conversion explicit at capture. No descendant costs added and no repeated safety credit. Last Updated: 2026-09-21. */
        attribute selected_cost_usd2004 : Real = 56086000.000;
    }
    part capital_budget {
        doc /* Source: work/active/WI-088_aries-source-budget-cost-contribution/spec.md. Ref: Lyon p707 Eq7. Basis: selected inclusive1.93 includes financing/escalation and contingencies, not overnight or pure IDC. Last Updated: 2026-09-21. */
        attribute inclusive_multiplier : Real = 1.93;
        calc total : 'Disjoint Capital Budget' {
            in account_1_in = land.selected_cost_usd2004;
            in account_2_in = structures.selected_cost_usd2004;
            in account_3_in = reactor_equipment.selected_cost_usd2004;
            in account_4_in = turbine_equipment.selected_cost_usd2004;
            in account_5_in = electrical_equipment.selected_cost_usd2004;
            in account_6_in = miscellaneous_equipment.selected_cost_usd2004;
            in account_7_in = special_materials.selected_cost_usd2004;
            in account_8_in = heat_rejection.selected_cost_usd2004;
            in inclusive_multiplier_in = inclusive_multiplier;
        }
        attribute direct_total : Real = total.direct_total;
        attribute inclusive_capital : Real = total.inclusive_capital;
        attribute inclusive_addition : Real = total.inclusive_addition;
    }
    part replacement_budget {
        doc /* Source: work/active/WI-088_aries-source-budget-cost-contribution/spec.md. Ref: Lyon p716 TableVII Replaced components966M, mapped to lifetime operating replacements via p709 discussion. Basis: AGENT accepted cross-page interpretation, separate Eq7 replacement numerator. Rounded75M times13=975M remains a separate sensitivity. Last Updated: 2026-09-21. */
        attribute selected_lifetime_cost_usd2004 : Real = 966000000.0;
    }
    part budget_period {
        doc /* Source: work/active/WI-088_aries-source-budget-cost-contribution/spec.md. Ref: Eq7 literal divisor40, availability0.85; TableIV net1000MW. Basis: mode0 literal source expression; mode1 explicitly inferred FPY/calendar interpretation. Fixed availability, no predicted reliability. All reused-formula inputs come from guarded outputs. Last Updated: 2026-09-21. */
        attribute selected_period : Real = 40.0;
        attribute selected_mode : Real = 0.0;
        attribute selected_net_power : Real = 1000.0;
        attribute selected_availability : Real = 0.85;
        calc period : 'Budget Period Allocation' {
            in capital_budget_in = capital_budget.inclusive_capital;
            in replacement_budget_in = replacement_budget.selected_lifetime_cost_usd2004;
            in selected_period_in = selected_period;
            in period_mode_in = selected_mode;
            in net_power_in = selected_net_power;
            in availability_in = selected_availability;
        }
        attribute annual_capital : Real = period.annual_capital;
        attribute annual_replacement : Real = period.annual_replacement;
        attribute partial_annual_cost : Real = period.partial_annual_cost;
        attribute comparison_period : Real = period.comparison_period;
        attribute annual_energy : Real = period.annual_energy;
        attribute lifetime_energy : Real = period.lifetime_energy;
        attribute validated_net_power : Real = period.validated_net_power;
        attribute validated_availability : Real = period.validated_availability;
        attribute module_count : Real = period.module_count;
        attribute excluded_annual_channel : Real = period.excluded_annual_channel;
    }
    part partial_cost {
        doc /* Source: work/active/WI-088_aries-source-budget-cost-contribution/spec.md. Ref: unchanged1cfe-Form LCOE money-unit-transparent formula. Basis: cas90 is allocated inclusive capital, cas70 allocated replacement, cas80 computed excluded-scopezero. This reuses numerator positions, not original CRF/O&M category semantics. Partial contribution only; missing O&M/fuel/decommissioning unquantified. Last Updated: 2026-09-21. */
        calc cost_per_energy : '1cfe-Form LCOE' {
            in cas90 = budget_period.annual_capital;
            in cas70 = budget_period.annual_replacement;
            in cas80 = budget_period.excluded_annual_channel;
            in net_electric_mw = budget_period.validated_net_power;
            in n_mod_in = budget_period.module_count;
            in availability_in = budget_period.validated_availability;
        }
        attribute partial_capital_replacement_cost_per_mwh : Real = cost_per_energy.lcoe;
    }
}
