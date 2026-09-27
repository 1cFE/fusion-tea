package controlled_exchanger_closure {
    private import ScalarValues::*;
    calc def 'Controlled Network Heat Driven Closure' {
        doc /* Native selectable legacy or constant-U primary-bypass closure. Full delivered duty fixes required hot temperature from the supplied aggregate return; actual accepted duty closes the cycle and exposes unmet heat. Active HX outlet and mixed loop return are distinct. Mode 0 preserves reviewed legacy arithmetic. **Source**: work/active/WI-097_exchanger-thermal-requirements/design.md. **Reference**: controlled branch equations, coupled cycle closure, domains and exact-return/30 K conditional requirements; original source interpretation in work/orchestration/goals/design-study-exchanger-architecture/evidence/r2-thermal-requirements.md. Units: MW, K, MPa, kg/s, J/(kg K), MW/K; fractions and modes dimensionless. **Last Updated**: 2026-09-27. */
        in attribute cold_temperature_in : Real;
        in attribute flow_in : Real;
        in attribute cp_in : Real;
        in attribute gamma_in : Real;
        in attribute turbine_efficiency_in : Real;
        in attribute turbine_pressure_in : Real;
        in attribute return_pressure_in : Real;
        in attribute recuperator_effectiveness_in : Real;
        in attribute he_available_in : Real;
        in attribute divertor_available_in : Real;
        in attribute pbli_available_in : Real;
        in attribute he_flow_in : Real;
        in attribute he_cp_in : Real;
        in attribute he_ua_in : Real;
        in attribute he_limit_in : Real;
        in attribute divertor_flow_in : Real;
        in attribute divertor_cp_in : Real;
        in attribute divertor_ua_in : Real;
        in attribute divertor_limit_in : Real;
        in attribute pbli_flow_in : Real;
        in attribute pbli_cp_in : Real;
        in attribute pbli_ua_in : Real;
        in attribute pbli_limit_in : Real;
        in attribute network_mode_in : Real;
        in attribute pbli_split_in : Real;
        in attribute control_mode_in : Real;
        in attribute return_tolerance_in : Real;
        in attribute he_required_return_in : Real;
        in attribute he_hot_approach_in : Real;
        in attribute he_cold_approach_in : Real;
        in attribute he_max_bypass_in : Real;
        in attribute pbli_required_return_in : Real;
        in attribute pbli_hot_approach_in : Real;
        in attribute pbli_cold_approach_in : Real;
        in attribute pbli_max_bypass_in : Real;
        in attribute divertor_required_return_in : Real;
        in attribute divertor_hot_approach_in : Real;
        in attribute divertor_cold_approach_in : Real;
        in attribute divertor_max_bypass_in : Real;
        out attribute turbine_temperature : Real;
        out attribute heater_inlet : Real;
        out attribute expansion_factor : Real;
        out attribute accepted_heat : Real;
        out attribute unmet_heat : Real;
        out attribute closure_residual : Real;
        out attribute iterations : Real;
        out attribute he_transferred : Real;
        out attribute he_unmet : Real;
        out attribute he_capability : Real;
        out attribute he_hot : Real;
        out attribute he_return : Real;
        out attribute he_state_defined : Real;
        out attribute he_hot_terminal_difference : Real;
        out attribute he_cold_terminal_difference : Real;
        out attribute he_hot_bound_margin : Real;
        out attribute he_secondary_in : Real;
        out attribute he_secondary_out : Real;
        out attribute divertor_transferred : Real;
        out attribute divertor_unmet : Real;
        out attribute divertor_capability : Real;
        out attribute divertor_hot : Real;
        out attribute divertor_return : Real;
        out attribute divertor_state_defined : Real;
        out attribute divertor_hot_terminal_difference : Real;
        out attribute divertor_cold_terminal_difference : Real;
        out attribute divertor_hot_bound_margin : Real;
        out attribute divertor_secondary_in : Real;
        out attribute divertor_secondary_out : Real;
        out attribute pbli_transferred : Real;
        out attribute pbli_unmet : Real;
        out attribute pbli_capability : Real;
        out attribute pbli_hot : Real;
        out attribute pbli_return : Real;
        out attribute pbli_state_defined : Real;
        out attribute pbli_hot_terminal_difference : Real;
        out attribute pbli_cold_terminal_difference : Real;
        out attribute pbli_hot_bound_margin : Real;
        out attribute pbli_secondary_in : Real;
        out attribute pbli_secondary_out : Real;
        out attribute pbli_stream_out : Real;
        out attribute divertor_stream_out : Real;
        out attribute mixed_outlet : Real;
        out attribute network_mode_used : Real;
        out attribute pbli_split_used : Real;
            out attribute control_mode_used : Real;
        out attribute he_required_hot : Real;
        out attribute he_required_hot_margin : Real;
        out attribute he_hx_return : Real;
        out attribute he_mixed_return : Real;
        out attribute he_active_flow : Real;
        out attribute he_bypass_fraction : Real;
        out attribute he_capability_at_solution : Real;
        out attribute he_return_residual : Real;
        out attribute he_return_residual_magnitude : Real;
        out attribute he_hot_approach_margin : Real;
        out attribute he_cold_approach_margin : Real;
        out attribute he_control_margin : Real;
        out attribute pbli_required_hot : Real;
        out attribute pbli_required_hot_margin : Real;
        out attribute pbli_hx_return : Real;
        out attribute pbli_mixed_return : Real;
        out attribute pbli_active_flow : Real;
        out attribute pbli_bypass_fraction : Real;
        out attribute pbli_capability_at_solution : Real;
        out attribute pbli_return_residual : Real;
        out attribute pbli_return_residual_magnitude : Real;
        out attribute pbli_hot_approach_margin : Real;
        out attribute pbli_cold_approach_margin : Real;
        out attribute pbli_control_margin : Real;
        out attribute divertor_required_hot : Real;
        out attribute divertor_required_hot_margin : Real;
        out attribute divertor_hx_return : Real;
        out attribute divertor_mixed_return : Real;
        out attribute divertor_active_flow : Real;
        out attribute divertor_bypass_fraction : Real;
        out attribute divertor_capability_at_solution : Real;
        out attribute divertor_return_residual : Real;
        out attribute divertor_return_residual_magnitude : Real;
        out attribute divertor_hot_approach_margin : Real;
        out attribute divertor_cold_approach_margin : Real;
        out attribute divertor_control_margin : Real;
    }
    constraint def 'Thermal Nonnegative Margin' {
        doc /* **Source**: work/active/WI-097_exchanger-thermal-requirements/design.md. **Reference**: exact margin acceptance; numerical verification is separate from physical threshold. **Last Updated**: 2026-09-27. */
        in attribute margin_in : Real;
        margin_in >= 0.0
    }
    constraint def 'Thermal State Defined' {
        doc /* **Source**: work/active/WI-097_exchanger-thermal-requirements/design.md. **Reference**: positive-transfer state guard; rounded terminal cancellation does not invalidate finite transfer. **Last Updated**: 2026-09-27. */
        in attribute defined_in : Real;
        defined_in >= 1.0
    }
    constraint def 'Thermal Return Held' {
        doc /* **Source**: work/active/WI-097_exchanger-thermal-requirements/design.md. **Reference**: mixed-return numerical residual; tolerance is a solve check, not a physical return band. **Last Updated**: 2026-09-27. */
        in attribute residual_magnitude_in : Real;
        in attribute tolerance_in : Real;
        residual_magnitude_in <= tolerance_in
    }
}
