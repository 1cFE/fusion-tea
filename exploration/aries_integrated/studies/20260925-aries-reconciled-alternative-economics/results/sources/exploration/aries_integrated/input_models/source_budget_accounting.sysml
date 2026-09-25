package source_budget_accounting {
    private import ScalarValues::*;
    calc def 'Disjoint Capital Budget' {
        doc /* Source: work/active/WI-088_aries-source-budget-cost-contribution/spec.md. Ref: accepted financial scope and Lyon Eq7/account mapping. Basis: AGENT generic disjoint-budget accounting and explicit period convention. direct_total=sum(account1..8); inclusive_capital=direct_total*inclusive_multiplier; inclusive_addition=inclusive_capital-direct_total. Dollars, supplied disjoint scope and inclusive multiplier; not a price/financing prediction. Native guard rejects nonfinite/negative budgets, nonpositive multiplier/period/power, mode outside0/1, availability outside(0,1], overflow and zero energy. Last Updated: 2026-09-21. */
        in attribute account_1_in : Real;
        in attribute account_2_in : Real;
        in attribute account_3_in : Real;
        in attribute account_4_in : Real;
        in attribute account_5_in : Real;
        in attribute account_6_in : Real;
        in attribute account_7_in : Real;
        in attribute account_8_in : Real;
        in attribute inclusive_multiplier_in : Real;
        out attribute direct_total : Real;
        out attribute inclusive_capital : Real;
        out attribute inclusive_addition : Real;
    }
    calc def 'Budget Period Allocation' {
        doc /* Source: work/active/WI-088_aries-source-budget-cost-contribution/spec.md. Ref: accepted financial scope and Lyon Eq7/account mapping. Basis: AGENT generic disjoint-budget accounting and explicit period convention. period=selected_period for mode0; period=selected_period/availability for mode1. annual_capital=capital/period; annual_replacement=replacement/period; partial_annual_cost=annual_capital+annual_replacement; annual_energy=8760*net_power*availability; lifetime_energy=annual_energy*period. Guarded pass-through net_power/availability; constant module_count1 and excluded_annual_channel0 are nonpublic outputs. Dollars, MW, years, MWh; mode selects explicit comparison convention, not inferred reliability. Native guard rejects nonfinite/negative budgets, nonpositive multiplier/period/power, mode outside0/1, availability outside(0,1], overflow and zero energy. Last Updated: 2026-09-21. */
        in attribute capital_budget_in : Real;
        in attribute replacement_budget_in : Real;
        in attribute selected_period_in : Real;
        in attribute period_mode_in : Real;
        in attribute net_power_in : Real;
        in attribute availability_in : Real;
        out attribute annual_capital : Real;
        out attribute annual_replacement : Real;
        out attribute partial_annual_cost : Real;
        out attribute comparison_period : Real;
        out attribute annual_energy : Real;
        out attribute lifetime_energy : Real;
        out attribute validated_net_power : Real;
        out attribute validated_availability : Real;
        out attribute module_count : Real;
        out attribute excluded_annual_channel : Real;
    }
}
