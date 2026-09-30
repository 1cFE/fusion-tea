package mfe_matched_steam_cycle {
    private import ScalarValues::*;
    calc def 'Matched Steam Cycle' {
        doc /* **Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Numerical semantic: the normative handwritten implementation executes the exact state/work equations in the cited design. Disabled modes branch before property access; no extrapolation. Units are given by the scalar names and interface inventory. */
        in attribute enabled_in : Real;
        in attribute heat_available_MW_in : Real;
        in attribute source_heat_MW_in : Real;
        in attribute selected_recovered_MW_in : Real;
        in attribute salt_flow_per_circuit_in : Real;
        in attribute salt_circuit_count_in : Real;
        in attribute salt_hot_C_in : Real;
        in attribute salt_return_C_in : Real;
        in attribute salt_cp_kJ_kgK_in : Real;
        in attribute main_pressure_MPa_in : Real;
        in attribute extraction_pressure_MPa_in : Real;
        in attribute steam_temperature_C_in : Real;
        in attribute reheat_temperature_C_in : Real;
        in attribute condenser_temperature_C_in : Real;
        in attribute eta_hp_in : Real;
        in attribute eta_lp_in : Real;
        in attribute eta_condensate_pump_in : Real;
        in attribute eta_feedwater_pump_in : Real;
        in attribute eta_pump_motor_in : Real;
        in attribute eta_mechanical_in : Real;
        in attribute eta_generator_in : Real;
        out attribute p_feed_MPa : Real;
        out attribute h_feed_kJ_kg : Real;
        out attribute mdot_feed_kg_s : Real;
        out attribute t_feed_C : Real;
        out attribute s_feed_kJ_kgK : Real;
        out attribute p_main_MPa : Real;
        out attribute h_main_kJ_kg : Real;
        out attribute mdot_main_kg_s : Real;
        out attribute t_main_C : Real;
        out attribute s_main_kJ_kgK : Real;
        out attribute p_hp_MPa : Real;
        out attribute h_hp_kJ_kg : Real;
        out attribute mdot_hp_kg_s : Real;
        out attribute t_hp_C : Real;
        out attribute s_hp_kJ_kgK : Real;
        out attribute p_reheat_MPa : Real;
        out attribute h_reheat_kJ_kg : Real;
        out attribute mdot_reheat_kg_s : Real;
        out attribute t_reheat_C : Real;
        out attribute s_reheat_kJ_kgK : Real;
        out attribute p_lp_MPa : Real;
        out attribute h_lp_kJ_kg : Real;
        out attribute mdot_lp_kg_s : Real;
        out attribute t_lp_C : Real;
        out attribute s_lp_kJ_kgK : Real;
        out attribute p_condensate_MPa : Real;
        out attribute h_condensate_kJ_kg : Real;
        out attribute mdot_condensate_kg_s : Real;
        out attribute t_condensate_C : Real;
        out attribute s_condensate_kJ_kgK : Real;
        out attribute p_condensate_pumped_MPa : Real;
        out attribute h_condensate_pumped_kJ_kg : Real;
        out attribute mdot_condensate_pumped_kg_s : Real;
        out attribute p_heater_MPa : Real;
        out attribute h_heater_kJ_kg : Real;
        out attribute mdot_heater_kg_s : Real;
        out attribute t_heater_C : Real;
        out attribute s_heater_kJ_kgK : Real;
        out attribute bleed_fraction : Real;
        out attribute mdot_bleed_kg_s : Real;
        out attribute salt_flow_total_kg_s : Real;
        out attribute salt_main_flow_kg_s : Real;
        out attribute salt_reheat_flow_kg_s : Real;
        out attribute q_main_MW : Real;
        out attribute q_reheat_MW : Real;
        out attribute q_condenser_MW : Real;
        out attribute p_hp_shaft_MW : Real;
        out attribute p_lp_shaft_MW : Real;
        out attribute p_condensate_shaft_MW : Real;
        out attribute p_feedwater_shaft_MW : Real;
        out attribute p_condensate_electric_MW : Real;
        out attribute p_feedwater_electric_MW : Real;
        out attribute p_cycle_pumps_MW : Real;
        out attribute p_gross_MW : Real;
        out attribute eta_gross : Real;
        out attribute p_cycle_net_before_cooling_MW : Real;
        out attribute q_mechanical_loss_MW : Real;
        out attribute q_generator_loss_MW : Real;
        out attribute q_pump_motor_loss_MW : Real;
        out attribute q_rejection_before_cooling_MW : Real;
        out attribute lp_quality : Real;
        out attribute lp_moisture_fraction : Real;
        out attribute main_min_gap_K : Real;
        out attribute reheat_min_gap_K : Real;
        out attribute main_UA_MW_K : Real;
        out attribute reheat_UA_MW_K : Real;
        out attribute salt_heat_residual_MW : Real;
        out attribute heater_mass_residual_kg_s : Real;
        out attribute heater_energy_residual_MW : Real;
        out attribute cycle_shaft_residual_MW : Real;
        out attribute cycle_electric_residual_MW : Real;
        out attribute active : Boolean;
        out attribute main_UA_available : Boolean;
        out attribute reheat_UA_available : Boolean;
        out attribute main_admission_ok : Boolean;
        out attribute reheat_admission_ok : Boolean;
        out attribute turbine_equipment_qualified : Boolean;
        out attribute installed_sg_capacity_qualified : Boolean;
    }
    calc def 'Cooling Water Rejection' {
        doc /* **Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Numerical semantic: the normative handwritten implementation executes the exact state/work equations in the cited design. Disabled modes branch before property access; no extrapolation. Units are given by the scalar names and interface inventory. */
        in attribute enabled_in : Real;
        in attribute cycle_active_in : Real;
        in attribute q_rejection_before_cooling_MW_in : Real;
        in attribute condenser_temperature_C_in : Real;
        in attribute water_inlet_C_in : Real;
        in attribute water_outlet_C_in : Real;
        in attribute head_m_in : Real;
        in attribute eta_pump_in : Real;
        in attribute eta_motor_in : Real;
        out attribute water_flow_kg_s : Real;
        out attribute p_cooling_pump_shaft_MW : Real;
        out attribute p_cooling_pump_electric_MW : Real;
        out attribute q_cooling_motor_loss_MW : Real;
        out attribute q_total_rejection_MW : Real;
        out attribute water_pump_rise_K : Real;
        out attribute condenser_water_gap_K : Real;
        out attribute water_energy_residual_MW : Real;
        out attribute denominator_kJ_kg : Real;
        out attribute active : Boolean;
        out attribute reference_scenario : Boolean;
        out attribute site_qualified : Boolean;
        out attribute cooling_approach_ok : Boolean;
    }
    calc def 'Cycle Mode Selection' {
        doc /* **Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Numerical semantic: the normative handwritten implementation executes the exact state/work equations in the cited design. Disabled modes branch before property access; no extrapolation. Units are given by the scalar names and interface inventory. */
        in attribute matched_enabled_in : Real;
        in attribute legacy_eta_in : Real;
        in attribute matched_eta_in : Real;
        in attribute legacy_domain_product_in : Real;
        out attribute eta_selected : Real;
        out attribute legacy_domain_applicable : Boolean;
        out attribute matched_domain_applicable : Boolean;
    }
    constraint def 'Active Steam Heat Direction' {
        // Exact mode domain {0,1} is enforced by the solver; <=0 means disabled only.
        // Invalid modes refuse before predicate reporting. Physical approach remains strictly positive.
        doc /* **Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Positive temperature difference is necessary for the modeled heat direction. Disabled mode is inapplicable; raw module flags and margins remain separately visible. This does not replace the prior scenario-specific20K screen or qualify installed capacity. */
        in attribute enabled_in : Real;
        in attribute gap_in : Real;
        enabled_in <= 0.0 or gap_in > 0.0
    }
}
