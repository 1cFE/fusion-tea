package integrated_equipment_costs {
    private import ScalarValues::*;
    calc def 'Selected Inventory Purchase' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        in attribute quantity_in : Real;
        in attribute reference_quantity_in : Real;
        in attribute reference_cost_in : Real;
        in attribute price_factor_in : Real;
        in attribute mode_in : Real;
        out attribute purchased_quantity : Real;
        out attribute quantity_ratio : Real;
        out attribute capital : Real;
        out attribute source_budget : Real;
        out attribute extrapolated : Real;
    }
    calc def 'Exchanger Area Conductance' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        in attribute area_in : Real;
        in attribute u_in : Real;
        out attribute ua : Real;
        out attribute area : Real;
    }
    calc def 'Selected Flow Pump' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        in attribute flow_in : Real;
        in attribute reference_flow_in : Real;
        in attribute reference_power_in : Real;
        in attribute efficiency_in : Real;
        in attribute reference_efficiency_in : Real;
        in attribute mode_in : Real;
        in attribute fixed_power_in : Real;
        out attribute electric : Real;
        out attribute hydraulic_supported : Real;
        out attribute operating_flow : Real;
        out attribute mode : Real;
    }
    calc def 'Selected Stock Atoms' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        in attribute stock_kg_in : Real;
        in attribute atom_mass_in : Real;
        out attribute atoms : Real;
        out attribute stock_kg : Real;
    }
    calc def 'Annual Selected Fuel' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        in attribute stock_kg_in : Real;
        in attribute atom_mass_in : Real;
        in attribute decay_in : Real;
        in attribute seconds_in : Real;
        in attribute availability_in : Real;
        in attribute burn_in : Real;
        in attribute loss_in : Real;
        in attribute exhaust_in : Real;
        in attribute residence_in : Real;
        in attribute annual_recovery_in : Real;
        in attribute tritium_price_in : Real;
        out attribute annual_burn : Real;
        out attribute annual_loss : Real;
        out attribute annual_decay : Real;
        out attribute annual_recovery : Real;
        out attribute annual_external : Real;
        out attribute annual_cost : Real;
        out attribute required_stock : Real;
        out attribute breeding_supported : Real;
    }
    calc def 'Replacement Events' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        in attribute event_cost_in : Real;
        in attribute life_fpy_in : Real;
        in attribute availability_in : Real;
        in attribute plant_years_in : Real;
        out attribute event_cost : Real;
        out attribute interval_years : Real;
        out attribute event_count : Real;
        out attribute lifetime_total : Real;
        out attribute annual_reserve : Real;
        out attribute first_event_year : Real;
        out attribute last_event_year : Real;
    }
    calc def 'Eight Amount Sum' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        in attribute amount1_in : Real;
        in attribute amount2_in : Real;
        in attribute amount3_in : Real;
        in attribute amount4_in : Real;
        in attribute amount5_in : Real;
        in attribute amount6_in : Real;
        in attribute amount7_in : Real;
        in attribute amount8_in : Real;
        out attribute total : Real;
    }
    calc def 'Scaled Amount' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        in attribute amount_in : Real;
        in attribute factor_in : Real;
        out attribute amount : Real;
    }
    calc def 'Equipment Cost Ledger' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        in attribute direct_in : Real;
        in attribute source_direct_in : Real;
        in attribute source_inclusive_in : Real;
        in attribute indirect_in : Real;
        in attribute contingency_in : Real;
        in attribute owner_in : Real;
        in attribute om_in : Real;
        in attribute tritium_in : Real;
        in attribute deuterium_in : Real;
        in attribute consumables_in : Real;
        in attribute replacement_reserve_in : Real;
        in attribute replacement_total_in : Real;
        in attribute net_power_in : Real;
        in attribute availability_in : Real;
        in attribute import_price_in : Real;
        in attribute source_reactor_gap_in : Real;
        in attribute source_core_excess_in : Real;
        in attribute source_coil_excess_in : Real;
        in attribute currency_year_in : Real;
        out attribute direct : Real;
        out attribute source_direct : Real;
        out attribute source_inclusive : Real;
        out attribute direct_difference : Real;
        out attribute overnight : Real;
        out attribute annual_operating : Real;
        out attribute annual_replacement_reserve : Real;
        out attribute lifetime_replacement : Real;
        out attribute annual_export_mwh : Real;
        out attribute annual_import_mwh : Real;
        out attribute annual_import_cost : Real;
        out attribute source_reactor_gap : Real;
        out attribute source_core_excess : Real;
        out attribute source_coil_excess : Real;
        out attribute currency_year : Real;
    }
}
