package aries_integrated_plant {
    private import ScalarValues::*;
    private import integrated_lifecycle_costs::*;
    private import mfe_lcoe_dcf::*;
    private import integrated_equipment_costs::*;
    private import integrated_equipment_parts::*;
    private import mfe_account_costs::*;
    private import source_budget_accounting::*;
    private import aries_cs_plasma_integration::*;
    private import integrated_heat_electricity::*;
    private import mfe_fuel_cycle::*;
    private import mfe_viability::*;
    private import dual_circuit_heat_accounting::*;
    private import ideal_gas_brayton_components::*;
    part source {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: source owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute reference_fusion_mw : Real = 2436.0;
        attribute producer_mode : Real = 0.0;
        calc evaluate : 'Fusion Source Selector' {
            in calculated_power_in = plasma.fusion_power_MW;
            in reference_power_in = reference_fusion_mw;
            in mode_in = producer_mode;
        }
        attribute selected_power : Real = evaluate.selected_power;
        attribute selected_mode : Real = evaluate.selected_mode;
    }
    part deposition {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: deposition owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute heat_mode : Real = 0.0;
        attribute neutron_multiplier : Real = 1.16;
        attribute radiation_fraction : Real = 0.25;
        attribute helium_fraction : Real = 0.38;
        attribute exchange_fraction : Real = 0.04;
        attribute auxiliary_heat : Real = 20.0;
        attribute he_pump : Real = aries_integrated_plant::he_pump.electric;
        attribute pbli_pump : Real = aries_integrated_plant::pbli_pump.electric;
        attribute divertor_pump : Real = aries_integrated_plant::divertor_pump.electric;
        attribute he_recovery : Real = 0.9038461538461539;
        attribute pbli_recovery : Real = 0.0;
        attribute divertor_recovery : Real = 0.9;
        attribute literal_he : Real = 940.0;
        attribute literal_pbli : Real = 1555.0;
        attribute literal_exchange : Real = 111.0;
        attribute literal_divertor : Real = 374.75;
        calc evaluate : 'Integrated Heat Source' {
            in fusion_power_in = source.selected_power;
            in heat_mode_in = heat_mode;
            in neutron_multiplier_in = neutron_multiplier;
            in radiation_fraction_in = radiation_fraction;
            in helium_fraction_in = helium_fraction;
            in exchange_fraction_in = exchange_fraction;
            in auxiliary_heat_in = auxiliary_heat;
            in he_pump_in = he_pump;
            in pbli_pump_in = pbli_pump;
            in divertor_pump_in = divertor_pump;
            in he_recovery_in = he_recovery;
            in pbli_recovery_in = pbli_recovery;
            in divertor_recovery_in = divertor_recovery;
            in literal_he_in = literal_he;
            in literal_pbli_in = literal_pbli;
            in literal_exchange_in = literal_exchange;
            in literal_divertor_in = literal_divertor;
        }
        attribute neutron_power : Real = evaluate.neutron_power;
        attribute charged_power : Real = evaluate.charged_power;
        attribute nuclear_gain : Real = evaluate.nuclear_gain;
        attribute he_deposition : Real = evaluate.he_deposition;
        attribute pbli_deposition : Real = evaluate.pbli_deposition;
        attribute divertor_deposition : Real = evaluate.divertor_deposition;
        attribute exchange : Real = evaluate.exchange;
        attribute he_friction : Real = evaluate.he_friction;
        attribute pbli_friction : Real = evaluate.pbli_friction;
        attribute divertor_friction : Real = evaluate.divertor_friction;
        attribute other_heat : Real = evaluate.other_heat;
        attribute source_residual : Real = evaluate.source_residual;
        attribute topology_zero : Real = evaluate.topology_zero;
        attribute pump_electric : Real = evaluate.pump_electric;
        attribute pump_recovered : Real = evaluate.pump_recovered;
    }
    part he_coolant {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: he_coolant owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Coolant Branch Heat' {
            in deposited_heat_in = deposition.he_deposition;
            in received_exchange_in = deposition.exchange;
            in exported_exchange_in = deposition.topology_zero;
            in recovered_friction_in = deposition.he_friction;
        }
        attribute delivered_heat : Real = evaluate.delivered_heat;
    }
    part pbli_coolant {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: pbli_coolant owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Coolant Branch Heat' {
            in deposited_heat_in = deposition.pbli_deposition;
            in received_exchange_in = deposition.topology_zero;
            in exported_exchange_in = deposition.exchange;
            in recovered_friction_in = deposition.pbli_friction;
        }
        attribute delivered_heat : Real = evaluate.delivered_heat;
    }
    part divertor_coolant {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: divertor_coolant owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Coolant Branch Heat' {
            in deposited_heat_in = deposition.divertor_deposition;
            in received_exchange_in = deposition.topology_zero;
            in exported_exchange_in = deposition.topology_zero;
            in recovered_friction_in = deposition.divertor_friction;
        }
        attribute delivered_heat : Real = evaluate.delivered_heat;
    }
    part fuel {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: fuel owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute reaction_energy_mev : Real = 17.58;
        attribute mev_joules : Real = 1.6021766339999998e-13;
        attribute tritium_atom_kg : Real = 5.008267663228036e-27;
        attribute pass_burn_fraction : Real = 0.05;
        attribute exhaust_recovery : Real = 0.99;
        attribute decay_constant_s : Real = 1.782785958230312e-09;
        attribute unused_tbr_placeholder : Real = 0.0;
        attribute assumed_extraction : Real = 1.0;
        attribute dormant_stock_growth_atoms_s : Real = 0.0;
        attribute seconds_per_year : Real = 31536000.0;
        calc evaluate : 'Fuel Cycle Flows' {
            in p_fus_in = source.selected_power;
            in q_eff_in = reaction_energy_mev;
            in mev_to_joules_in = mev_joules;
            in burn_fraction_in = pass_burn_fraction;
            in t_recycle_in = exhaust_recovery;
            in tbr_available_in = unused_tbr_placeholder;
            in eta_extract_in = assumed_extraction;
            in lambda_T_in = decay_constant_s;
            in I_total_in = fuel_inventory.selected_tritium_atoms;
            in G_stock_in = dormant_stock_growth_atoms_s;
            in m_T_kg_in = tritium_atom_kg;
            in s_per_fpy_in = seconds_per_year;
        }
        attribute burn_rate : Real = evaluate.burn_rate;
        attribute inject_rate : Real = evaluate.inject_rate;
        attribute exhaust_rate : Real = evaluate.exhaust_rate;
        attribute loss_rate : Real = evaluate.loss_rate;
        attribute tbr_required : Real = evaluate.tbr_required;
    }
    part cycle {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: A3/S3 selected operating conditions, ideal helium. **Last Updated**: 2026-09-22. */
        attribute selected_flow : Real = 1400.0;
        attribute cp : Real = 5193.0;
        attribute gamma : Real = 1.6666666666666667;
        attribute return_pressure : Real = 4.285714285714286;
        attribute low_temperature : Real = 308.15;
        attribute turbine_efficiency : Real = 0.93;
        attribute recuperator_effectiveness : Real = 0.8;
    }
    part compressor_1 {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: compressor_1 owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute selected_ratio : Real = 1.5182944859378311;
        attribute efficiency : Real = 0.89;
        calc evaluate : 'Ideal Gas Compressor' {
            in temperature_in = cycle.low_temperature;
            in pressure_in = cycle.return_pressure;
            in ratio_in = selected_ratio;
            in flow_in = cycle.selected_flow;
            in cp_in = cycle.cp;
            in gamma_in = cycle.gamma;
            in efficiency_in = efficiency;
        }
        attribute temperature_out : Real = evaluate.temperature_out;
        attribute pressure_out : Real = evaluate.pressure_out;
        attribute shaft_demand : Real = evaluate.shaft_demand;
    }
    part intercooler_1 {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: intercooler_1 owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute target_temperature : Real = 308.15;
        attribute heating_role : Real = 0.0;
        calc evaluate : 'Fixed Outlet Conditioning' {
            in temperature_in = compressor_1.temperature_out;
            in target_temperature_in = target_temperature;
            in pressure_in = compressor_1.pressure_out;
            in flow_in = cycle.selected_flow;
            in cp_in = cycle.cp;
            in heating_role_in = heating_role;
        }
        attribute temperature_out : Real = evaluate.temperature_out;
        attribute pressure_out : Real = evaluate.pressure_out;
        attribute heat_into_fluid : Real = evaluate.heat_into_fluid;
    }
    part compressor_2 {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: compressor_2 owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute selected_ratio : Real = 1.5182944859378311;
        attribute efficiency : Real = 0.89;
        calc evaluate : 'Ideal Gas Compressor' {
            in temperature_in = intercooler_1.temperature_out;
            in pressure_in = intercooler_1.pressure_out;
            in ratio_in = selected_ratio;
            in flow_in = cycle.selected_flow;
            in cp_in = cycle.cp;
            in gamma_in = cycle.gamma;
            in efficiency_in = efficiency;
        }
        attribute temperature_out : Real = evaluate.temperature_out;
        attribute pressure_out : Real = evaluate.pressure_out;
        attribute shaft_demand : Real = evaluate.shaft_demand;
    }
    part intercooler_2 {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: intercooler_2 owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute target_temperature : Real = 308.15;
        attribute heating_role : Real = 0.0;
        calc evaluate : 'Fixed Outlet Conditioning' {
            in temperature_in = compressor_2.temperature_out;
            in target_temperature_in = target_temperature;
            in pressure_in = compressor_2.pressure_out;
            in flow_in = cycle.selected_flow;
            in cp_in = cycle.cp;
            in heating_role_in = heating_role;
        }
        attribute temperature_out : Real = evaluate.temperature_out;
        attribute pressure_out : Real = evaluate.pressure_out;
        attribute heat_into_fluid : Real = evaluate.heat_into_fluid;
    }
    part compressor_3 {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: compressor_3 owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute selected_ratio : Real = 1.5182944859378311;
        attribute efficiency : Real = 0.89;
        calc evaluate : 'Ideal Gas Compressor' {
            in temperature_in = intercooler_2.temperature_out;
            in pressure_in = intercooler_2.pressure_out;
            in ratio_in = selected_ratio;
            in flow_in = cycle.selected_flow;
            in cp_in = cycle.cp;
            in gamma_in = cycle.gamma;
            in efficiency_in = efficiency;
        }
        attribute temperature_out : Real = evaluate.temperature_out;
        attribute pressure_out : Real = evaluate.pressure_out;
        attribute shaft_demand : Real = evaluate.shaft_demand;
    }
    part pressure_loss {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: pressure_loss owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute loss_fraction : Real = 0.045;
        calc evaluate : 'Fractional Pressure Loss' {
            in pressure_in = compressor_3.pressure_out;
            in loss_fraction_in = loss_fraction;
        }
        attribute pressure_out : Real = evaluate.pressure_out;
    }
    part heat_exchangers {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md; work/active/WI-092_aries-parallel-exchanger-network/design.md. **Reference**: heat_exchangers owner/interface; values retain register S1-S3/A1-A9 provenance; network mode (default 0, series as reviewed) and supplied PbLi split fraction (N1) per WI-092. **Last Updated**: 2026-09-25. */
        attribute he_flow : Real = 3261.0;
        attribute he_cp : Real = 5193.0;
        attribute he_ua : Real = he_hx.ua;
        attribute he_limit : Real = 729.15;
        attribute divertor_flow : Real = 500.0;
        attribute divertor_cp : Real = 5193.0;
        attribute divertor_ua : Real = divertor_hx.ua;
        attribute divertor_limit : Real = 973.15;
        attribute pbli_flow : Real = 26860.0;
        attribute pbli_cp : Real = 190.0;
        attribute pbli_ua : Real = pbli_hx.ua;
        attribute pbli_limit : Real = 1011.15;
        attribute network_mode : Real = 0.0;
        attribute pbli_split_fraction : Real = 0.85;
        calc evaluate : 'Network Heat Driven Closure' {
            in cold_temperature_in = compressor_3.temperature_out;
            in flow_in = cycle.selected_flow;
            in cp_in = cycle.cp;
            in gamma_in = cycle.gamma;
            in turbine_efficiency_in = cycle.turbine_efficiency;
            in turbine_pressure_in = pressure_loss.pressure_out;
            in return_pressure_in = cycle.return_pressure;
            in recuperator_effectiveness_in = cycle.recuperator_effectiveness;
            in he_available_in = he_coolant.delivered_heat;
            in pbli_available_in = pbli_coolant.delivered_heat;
            in divertor_available_in = divertor_coolant.delivered_heat;
            in he_flow_in = he_flow;
            in he_cp_in = he_cp;
            in he_ua_in = he_ua;
            in he_limit_in = he_limit;
            in divertor_flow_in = divertor_flow;
            in divertor_cp_in = divertor_cp;
            in divertor_ua_in = divertor_ua;
            in divertor_limit_in = divertor_limit;
            in pbli_flow_in = pbli_flow;
            in pbli_cp_in = pbli_cp;
            in pbli_ua_in = pbli_ua;
            in pbli_limit_in = pbli_limit;
            in network_mode_in = network_mode;
            in pbli_split_in = pbli_split_fraction;
        }
        attribute turbine_temperature : Real = evaluate.turbine_temperature;
        attribute heater_inlet : Real = evaluate.heater_inlet;
        attribute expansion_factor : Real = evaluate.expansion_factor;
        attribute accepted_heat : Real = evaluate.accepted_heat;
        attribute unmet_heat : Real = evaluate.unmet_heat;
        attribute closure_residual : Real = evaluate.closure_residual;
        attribute iterations : Real = evaluate.iterations;
        attribute he_transferred : Real = evaluate.he_transferred;
        attribute he_unmet : Real = evaluate.he_unmet;
        attribute he_capability : Real = evaluate.he_capability;
        attribute he_hot : Real = evaluate.he_hot;
        attribute he_return : Real = evaluate.he_return;
        attribute he_state_defined : Real = evaluate.he_state_defined;
        attribute he_hot_terminal_difference : Real = evaluate.he_hot_terminal_difference;
        attribute he_cold_terminal_difference : Real = evaluate.he_cold_terminal_difference;
        attribute he_hot_bound_margin : Real = evaluate.he_hot_bound_margin;
        attribute he_secondary_in : Real = evaluate.he_secondary_in;
        attribute he_secondary_out : Real = evaluate.he_secondary_out;
        attribute divertor_transferred : Real = evaluate.divertor_transferred;
        attribute divertor_unmet : Real = evaluate.divertor_unmet;
        attribute divertor_capability : Real = evaluate.divertor_capability;
        attribute divertor_hot : Real = evaluate.divertor_hot;
        attribute divertor_return : Real = evaluate.divertor_return;
        attribute divertor_state_defined : Real = evaluate.divertor_state_defined;
        attribute divertor_hot_terminal_difference : Real = evaluate.divertor_hot_terminal_difference;
        attribute divertor_cold_terminal_difference : Real = evaluate.divertor_cold_terminal_difference;
        attribute divertor_hot_bound_margin : Real = evaluate.divertor_hot_bound_margin;
        attribute divertor_secondary_in : Real = evaluate.divertor_secondary_in;
        attribute divertor_secondary_out : Real = evaluate.divertor_secondary_out;
        attribute pbli_transferred : Real = evaluate.pbli_transferred;
        attribute pbli_unmet : Real = evaluate.pbli_unmet;
        attribute pbli_capability : Real = evaluate.pbli_capability;
        attribute pbli_hot : Real = evaluate.pbli_hot;
        attribute pbli_return : Real = evaluate.pbli_return;
        attribute pbli_state_defined : Real = evaluate.pbli_state_defined;
        attribute pbli_hot_terminal_difference : Real = evaluate.pbli_hot_terminal_difference;
        attribute pbli_cold_terminal_difference : Real = evaluate.pbli_cold_terminal_difference;
        attribute pbli_hot_bound_margin : Real = evaluate.pbli_hot_bound_margin;
        attribute pbli_secondary_in : Real = evaluate.pbli_secondary_in;
        attribute pbli_secondary_out : Real = evaluate.pbli_secondary_out;
        attribute pbli_stream_out : Real = evaluate.pbli_stream_out;
        attribute divertor_stream_out : Real = evaluate.divertor_stream_out;
        attribute mixed_outlet : Real = evaluate.mixed_outlet;
        attribute network_mode_used : Real = evaluate.network_mode_used;
        attribute pbli_split_used : Real = evaluate.pbli_split_used;
    }
    part turbine {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: turbine owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Ideal Gas Expander' {
            in temperature_in = heat_exchangers.turbine_temperature;
            in pressure_in = pressure_loss.pressure_out;
            in exit_pressure_in = cycle.return_pressure;
            in flow_in = cycle.selected_flow;
            in cp_in = cycle.cp;
            in gamma_in = cycle.gamma;
            in efficiency_in = cycle.turbine_efficiency;
        }
        attribute temperature_out : Real = evaluate.temperature_out;
        attribute pressure_out : Real = evaluate.pressure_out;
        attribute shaft_produced : Real = evaluate.shaft_produced;
    }
    part recuperator {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: recuperator owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Passive Recuperator' {
            in cold_temperature_in = compressor_3.temperature_out;
            in hot_temperature_in = turbine.temperature_out;
            in flow_in = cycle.selected_flow;
            in cp_in = cycle.cp;
            in effectiveness_in = cycle.recuperator_effectiveness;
        }
        attribute cold_out : Real = evaluate.cold_out;
        attribute hot_out : Real = evaluate.hot_out;
        attribute recovered_heat : Real = evaluate.recovered_heat;
        attribute bypass_active : Real = evaluate.bypass_active;
    }
    part precooler {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: precooler owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute heating_role : Real = 0.0;
        calc evaluate : 'Fixed Outlet Conditioning' {
            in temperature_in = recuperator.hot_out;
            in target_temperature_in = cycle.low_temperature;
            in pressure_in = turbine.pressure_out;
            in flow_in = cycle.selected_flow;
            in cp_in = cycle.cp;
            in heating_role_in = heating_role;
        }
        attribute temperature_out : Real = evaluate.temperature_out;
        attribute pressure_out : Real = evaluate.pressure_out;
        attribute heat_into_fluid : Real = evaluate.heat_into_fluid;
    }
    part generator_auxiliaries {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: generator and auxiliary electrical responsibilities; S/A provenance retained. **Last Updated**: 2026-09-22. */
        attribute heating_efficiency : Real = 0.5;
        attribute generator_efficiency : Real = 0.98;
        attribute motor_efficiency : Real = 0.95;
        attribute cryo : Real = 10.0;
        attribute fuel_base : Real = 5.0;
        attribute fuel_coefficient : Real = 1e-22;
        attribute control : Real = 5.0;
        attribute other_electric : Real = 5.0;
        calc evaluate : 'Plant Electrical Balance' {
            in turbine_work_in = turbine.shaft_produced;
            in compressor_1_in = compressor_1.shaft_demand;
            in compressor_2_in = compressor_2.shaft_demand;
            in compressor_3_in = compressor_3.shaft_demand;
            in auxiliary_heat_in = deposition.auxiliary_heat;
            in pump_electric_in = deposition.pump_electric;
            in pump_recovered_in = deposition.pump_recovered;
            in heating_efficiency_in = heating_efficiency;
            in generator_efficiency_in = generator_efficiency;
            in motor_efficiency_in = motor_efficiency;
            in cryo_in = cryo;
            in fuel_base_in = fuel_base;
            in fuel_coefficient_in = fuel_coefficient;
            in fuel_exhaust_in = fuel.exhaust_rate;
            in control_in = control;
            in other_electric_in = other_electric;
        }
        attribute compressor_demand : Real = evaluate.compressor_demand;
        attribute net_shaft : Real = evaluate.net_shaft;
        attribute gross_electric : Real = evaluate.gross_electric;
        attribute shaft_import : Real = evaluate.shaft_import;
        attribute generator_loss : Real = evaluate.generator_loss;
        attribute motor_loss : Real = evaluate.motor_loss;
        attribute heating_electric : Real = evaluate.heating_electric;
        attribute heating_loss : Real = evaluate.heating_loss;
        attribute fuel_electric : Real = evaluate.fuel_electric;
        attribute fuel_base_electric : Real = evaluate.fuel_base_electric;
        attribute fuel_variable_electric : Real = evaluate.fuel_variable_electric;
        attribute auxiliary_electric : Real = evaluate.auxiliary_electric;
        attribute net_electric : Real = evaluate.net_electric;
        attribute pump_loss : Real = evaluate.pump_loss;
        attribute dissipated_auxiliary : Real = evaluate.dissipated_auxiliary;
        attribute cryo_electric : Real = evaluate.cryo_electric;
        attribute control_electric : Real = evaluate.control_electric;
        attribute other_electric_demand : Real = evaluate.other_electric_demand;
        attribute primary_pump_electric : Real = evaluate.primary_pump_electric;
    }
    part plant_ledger {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: plant_ledger owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute reference_fusion : Real = 2436.0;
        attribute reference_gross : Real = 1253.0;
        attribute reference_net : Real = 1000.0;
        attribute reference_turbine_temperature : Real = 980.15;
        attribute reference_heater_temperature : Real = 628.15;
        attribute reference_blanket_deposition : Real = 2496.0;
        calc evaluate : 'Integrated Plant Ledger' {
            in electric_primary_pump_electric_in = generator_auxiliaries.primary_pump_electric;
            in electric_other_electric_demand_in = generator_auxiliaries.other_electric_demand;
            in electric_control_electric_in = generator_auxiliaries.control_electric;
            in electric_cryo_electric_in = generator_auxiliaries.cryo_electric;
            in electric_dissipated_auxiliary_in = generator_auxiliaries.dissipated_auxiliary;
            in electric_pump_loss_in = generator_auxiliaries.pump_loss;
            in electric_net_electric_in = generator_auxiliaries.net_electric;
            in electric_auxiliary_electric_in = generator_auxiliaries.auxiliary_electric;
            in electric_fuel_variable_electric_in = generator_auxiliaries.fuel_variable_electric;
            in electric_fuel_base_electric_in = generator_auxiliaries.fuel_base_electric;
            in electric_fuel_electric_in = generator_auxiliaries.fuel_electric;
            in electric_heating_loss_in = generator_auxiliaries.heating_loss;
            in electric_heating_electric_in = generator_auxiliaries.heating_electric;
            in electric_motor_loss_in = generator_auxiliaries.motor_loss;
            in electric_generator_loss_in = generator_auxiliaries.generator_loss;
            in electric_shaft_import_in = generator_auxiliaries.shaft_import;
            in electric_gross_electric_in = generator_auxiliaries.gross_electric;
            in electric_net_shaft_in = generator_auxiliaries.net_shaft;
            in electric_compressor_demand_in = generator_auxiliaries.compressor_demand;
            in reference_fusion_in = reference_fusion;
            in reference_gross_in = reference_gross;
            in reference_net_in = reference_net;
            in reference_turbine_temperature_in = reference_turbine_temperature;
            in reference_heater_temperature_in = reference_heater_temperature;
            in reference_blanket_deposition_in = reference_blanket_deposition;
            in fusion_power_in = source.selected_power;
            in producer_mode_in = source.selected_mode;
            in nuclear_gain_in = deposition.nuclear_gain;
            in auxiliary_heat_in = deposition.auxiliary_heat;
            in other_heat_in = deposition.other_heat;
            in source_residual_in = deposition.source_residual;
            in accepted_heat_in = heat_exchangers.accepted_heat;
            in unmet_heat_in = heat_exchangers.unmet_heat;
            in turbine_work_in = turbine.shaft_produced;
            in precooler_in = precooler.heat_into_fluid;
            in pump_electric_in = deposition.pump_electric;
            in pump_recovered_in = deposition.pump_recovered;
            in turbine_temperature_in = heat_exchangers.turbine_temperature;
            in turbine_exhaust_in = turbine.temperature_out;
            in expansion_factor_in = heat_exchangers.expansion_factor;
            in heater_inlet_in = heat_exchangers.heater_inlet;
            in recuperator_cold_out_in = recuperator.cold_out;
            in closure_residual_in = heat_exchangers.closure_residual;
            in he_available_in = he_coolant.delivered_heat;
            in he_deposition_in = deposition.he_deposition;
            in he_friction_in = deposition.he_friction;
            in pbli_available_in = pbli_coolant.delivered_heat;
            in pbli_deposition_in = deposition.pbli_deposition;
            in pbli_friction_in = deposition.pbli_friction;
            in divertor_available_in = divertor_coolant.delivered_heat;
            in divertor_deposition_in = deposition.divertor_deposition;
            in divertor_friction_in = deposition.divertor_friction;
            in compressor_1_in = compressor_1.shaft_demand;
            in compressor_2_in = compressor_2.shaft_demand;
            in compressor_3_in = compressor_3.shaft_demand;
            in intercooler_1_in = intercooler_1.heat_into_fluid;
            in intercooler_2_in = intercooler_2.heat_into_fluid;
        }
        attribute compressor_demand : Real = evaluate.compressor_demand;
        attribute net_shaft : Real = evaluate.net_shaft;
        attribute cycle_rejection : Real = evaluate.cycle_rejection;
        attribute gross_electric : Real = evaluate.gross_electric;
        attribute shaft_import : Real = evaluate.shaft_import;
        attribute generator_loss : Real = evaluate.generator_loss;
        attribute motor_loss : Real = evaluate.motor_loss;
        attribute heating_electric : Real = evaluate.heating_electric;
        attribute heating_loss : Real = evaluate.heating_loss;
        attribute fuel_base_electric : Real = evaluate.fuel_base_electric;
        attribute fuel_variable_electric : Real = evaluate.fuel_variable_electric;
        attribute fuel_electric : Real = evaluate.fuel_electric;
        attribute auxiliary_electric : Real = evaluate.auxiliary_electric;
        attribute net_electric : Real = evaluate.net_electric;
        attribute pump_loss : Real = evaluate.pump_loss;
        attribute dissipated_auxiliary : Real = evaluate.dissipated_auxiliary;
        attribute branch_residual : Real = evaluate.branch_residual;
        attribute cycle_residual : Real = evaluate.cycle_residual;
        attribute electrical_residual : Real = evaluate.electrical_residual;
        attribute plant_residual : Real = evaluate.plant_residual;
        attribute source_energy_residual : Real = evaluate.source_energy_residual;
        attribute unmatched_source_heat : Real = evaluate.unmatched_source_heat;
        attribute energy_tolerance : Real = evaluate.energy_tolerance;
        attribute residual_magnitude : Real = evaluate.residual_magnitude;
        attribute thermal_efficiency : Real = evaluate.thermal_efficiency;
        attribute efficiency_defined : Real = evaluate.efficiency_defined;
        attribute total_available_heat : Real = evaluate.total_available_heat;
        attribute comparison_fusion_difference : Real = evaluate.comparison_fusion_difference;
        attribute comparison_gross_difference : Real = evaluate.comparison_gross_difference;
        attribute comparison_net_difference : Real = evaluate.comparison_net_difference;
        attribute comparison_turbine_temperature_difference : Real = evaluate.comparison_turbine_temperature_difference;
        attribute comparison_heater_temperature_difference : Real = evaluate.comparison_heater_temperature_difference;
        attribute comparison_blanket_deposition_difference : Real = evaluate.comparison_blanket_deposition_difference;
        attribute turbine_state_residual : Real = evaluate.turbine_state_residual;
        attribute recuperator_state_residual : Real = evaluate.recuperator_state_residual;
        attribute supported_magnet : Real = evaluate.supported_magnet;
        attribute supported_breeding : Real = evaluate.supported_breeding;
        attribute supported_deposition : Real = evaluate.supported_deposition;
        attribute supported_hydraulics : Real = evaluate.supported_hydraulics;
        attribute supported_materials : Real = evaluate.supported_materials;
        attribute supported_machine_map : Real = evaluate.supported_machine_map;
        attribute assumed_auxiliary_demands : Real = evaluate.assumed_auxiliary_demands;
        attribute conditional_net_result : Real = evaluate.conditional_net_result;
        attribute net_result_producer_mode : Real = evaluate.net_result_producer_mode;
        attribute cryo_electric : Real = evaluate.cryo_electric;
        attribute control_electric : Real = evaluate.control_electric;
        attribute other_electric_demand : Real = evaluate.other_electric_demand;
        attribute primary_pump_electric : Real = evaluate.primary_pump_electric;
        assert constraint heat_removal_ok : 'Heat Removal Adequate' {
            in unmet_in = heat_exchangers.unmet_heat;
            in tolerance_in = energy_tolerance;
        }
        assert constraint balances_ok : 'Integrated Ledger Balanced' {
            in magnitude_in = residual_magnitude;
            in tolerance_in = energy_tolerance;
        }
    }
    part he_capacity {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: he_capacity owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute selected_rating : Real = 1500.0;
        attribute assumed_supported : Boolean = true;
        attribute scenario_applicable : Boolean = true;
        attribute demand_available : Boolean = true;
        calc evaluate : 'Offered Capacity Screen' {
            in rating_in = selected_rating;
            in demand_in = he_coolant.delivered_heat;
            in applicable_in = scenario_applicable;
            in conditions_supported_in = assumed_supported;
            in demand_available_in = demand_available;
        }
        attribute margin : Real = evaluate.margin;
        attribute evaluation_defined : Real = evaluate.evaluation_defined;
        assert constraint capacity_ok : 'Offered Equipment Capacity' {
            in defined_in = evaluation_defined;
            in margin_in = margin;
        }
    }
    part pbli_capacity {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: pbli_capacity owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute selected_rating : Real = 1800.0;
        attribute assumed_supported : Boolean = true;
        attribute scenario_applicable : Boolean = true;
        attribute demand_available : Boolean = true;
        calc evaluate : 'Offered Capacity Screen' {
            in rating_in = selected_rating;
            in demand_in = pbli_coolant.delivered_heat;
            in applicable_in = scenario_applicable;
            in conditions_supported_in = assumed_supported;
            in demand_available_in = demand_available;
        }
        attribute margin : Real = evaluate.margin;
        attribute evaluation_defined : Real = evaluate.evaluation_defined;
        assert constraint capacity_ok : 'Offered Equipment Capacity' {
            in defined_in = evaluation_defined;
            in margin_in = margin;
        }
    }
    part divertor_capacity {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: divertor_capacity owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute selected_rating : Real = 800.0;
        attribute assumed_supported : Boolean = true;
        attribute scenario_applicable : Boolean = true;
        attribute demand_available : Boolean = true;
        calc evaluate : 'Offered Capacity Screen' {
            in rating_in = selected_rating;
            in demand_in = divertor_coolant.delivered_heat;
            in applicable_in = scenario_applicable;
            in conditions_supported_in = assumed_supported;
            in demand_available_in = demand_available;
        }
        attribute margin : Real = evaluate.margin;
        attribute evaluation_defined : Real = evaluate.evaluation_defined;
        assert constraint capacity_ok : 'Offered Equipment Capacity' {
            in defined_in = evaluation_defined;
            in margin_in = margin;
        }
    }
    part compressor_capacity {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: compressor_capacity owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute selected_rating : Real = 1600.0;
        attribute assumed_supported : Boolean = true;
        attribute scenario_applicable : Boolean = true;
        attribute demand_available : Boolean = true;
        calc evaluate : 'Offered Capacity Screen' {
            in rating_in = selected_rating;
            in demand_in = plant_ledger.compressor_demand;
            in applicable_in = scenario_applicable;
            in conditions_supported_in = assumed_supported;
            in demand_available_in = demand_available;
        }
        attribute margin : Real = evaluate.margin;
        attribute evaluation_defined : Real = evaluate.evaluation_defined;
        assert constraint capacity_ok : 'Offered Equipment Capacity' {
            in defined_in = evaluation_defined;
            in margin_in = margin;
        }
    }
    part turbine_capacity {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: turbine_capacity owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute selected_rating : Real = 3500.0;
        attribute assumed_supported : Boolean = true;
        attribute scenario_applicable : Boolean = true;
        attribute demand_available : Boolean = true;
        calc evaluate : 'Offered Capacity Screen' {
            in rating_in = selected_rating;
            in demand_in = turbine.shaft_produced;
            in applicable_in = scenario_applicable;
            in conditions_supported_in = assumed_supported;
            in demand_available_in = demand_available;
        }
        attribute margin : Real = evaluate.margin;
        attribute evaluation_defined : Real = evaluate.evaluation_defined;
        assert constraint capacity_ok : 'Offered Equipment Capacity' {
            in defined_in = evaluation_defined;
            in margin_in = margin;
        }
    }
    part rejection_capacity {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: rejection_capacity owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute selected_rating : Real = 2500.0;
        attribute assumed_supported : Boolean = true;
        attribute scenario_applicable : Boolean = true;
        attribute demand_available : Boolean = true;
        calc evaluate : 'Offered Capacity Screen' {
            in rating_in = selected_rating;
            in demand_in = plant_ledger.cycle_rejection;
            in applicable_in = scenario_applicable;
            in conditions_supported_in = assumed_supported;
            in demand_available_in = demand_available;
        }
        attribute margin : Real = evaluate.margin;
        attribute evaluation_defined : Real = evaluate.evaluation_defined;
        assert constraint capacity_ok : 'Offered Equipment Capacity' {
            in defined_in = evaluation_defined;
            in margin_in = margin;
        }
    }
    part generator_capacity {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: generator_capacity owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute selected_rating : Real = 1800.0;
        attribute assumed_supported : Boolean = true;
        attribute scenario_applicable : Boolean = true;
        attribute demand_available : Boolean = true;
        calc evaluate : 'Offered Capacity Screen' {
            in rating_in = selected_rating;
            in demand_in = plant_ledger.gross_electric;
            in applicable_in = scenario_applicable;
            in conditions_supported_in = assumed_supported;
            in demand_available_in = demand_available;
        }
        attribute margin : Real = evaluate.margin;
        attribute evaluation_defined : Real = evaluate.evaluation_defined;
        assert constraint capacity_ok : 'Offered Equipment Capacity' {
            in defined_in = evaluation_defined;
            in margin_in = margin;
        }
    }
    part fuel_capacity {
        doc /* **Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: fuel_capacity owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute selected_rating : Real = 3e+22;
        attribute assumed_supported : Boolean = true;
        attribute scenario_applicable : Boolean = true;
        attribute demand_available : Boolean = true;
        calc evaluate : 'Offered Capacity Screen' {
            in rating_in = selected_rating;
            in demand_in = fuel.exhaust_rate;
            in applicable_in = scenario_applicable;
            in conditions_supported_in = assumed_supported;
            in demand_available_in = demand_available;
        }
        attribute margin : Real = evaluate.margin;
        attribute evaluation_defined : Real = evaluate.evaluation_defined;
        assert constraint capacity_ok : 'Offered Equipment Capacity' {
            in defined_in = evaluation_defined;
            in margin_in = margin;
        }
    }
    // WI-090 selected inventory and cost ownership
    part cost_accounts {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        attribute estimate_mode : Real = 0.0;
        attribute one_module : Real = 1.0;
    }
    part cost_schedule {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        attribute availability : Real = 0.85;
        attribute plant_years : Real = 40.0;
        attribute replacement_life_fpy : Real = 5.0;
        attribute replacement_factor : Real = 1.0;
        attribute lipb_makeup_fraction : Real = 0.05;
    }
    part he_hx : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.2";
        attribute reference_quantity : Real = 50000.0;
        attribute reference_cost : Real = 58325700.00000001;
        attribute price_factor : Real = 1.0;
        calc purchase : 'Selected Inventory Purchase' {
            in quantity_in = selected_area;
            in reference_quantity_in = reference_quantity;
            in reference_cost_in = reference_cost;
            in price_factor_in = price_factor;
            in mode_in = aries_integrated_plant::cost_accounts.estimate_mode;
        }
        attribute inventory_quantity : Real = purchase.purchased_quantity;
        attribute quantity_ratio : Real = purchase.quantity_ratio;
        attribute estimated_cost : Real = purchase.capital;
        attribute cost_extrapolated : Real = purchase.extrapolated;
        :>> capital_cost = purchase.capital;
        attribute selected_area : Real = 50000.0;
        attribute assumed_u : Real = 1000.0;
        calc evaluate : 'Exchanger Area Conductance' {
            in area_in = selected_area;
            in u_in = assumed_u;
        }
        attribute ua : Real = evaluate.ua;
        attribute area : Real = evaluate.area;
    }
    part he_pump : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.2";
        attribute reference_quantity : Real = 3261.0;
        attribute reference_cost : Real = 19441900.0;
        attribute price_factor : Real = 1.0;
        calc purchase : 'Selected Inventory Purchase' {
            in quantity_in = selected_flow_capacity;
            in reference_quantity_in = reference_quantity;
            in reference_cost_in = reference_cost;
            in price_factor_in = price_factor;
            in mode_in = aries_integrated_plant::cost_accounts.estimate_mode;
        }
        attribute inventory_quantity : Real = purchase.purchased_quantity;
        attribute quantity_ratio : Real = purchase.quantity_ratio;
        attribute estimated_cost : Real = purchase.capital;
        attribute cost_extrapolated : Real = purchase.extrapolated;
        :>> capital_cost = purchase.capital;
        attribute selected_flow_capacity : Real = 3261.0;
        attribute efficiency : Real = 0.8;
        attribute reference_flow : Real = 3261.0;
        attribute reference_power : Real = 156.0;
        attribute reference_efficiency : Real = 0.8;
        attribute pump_mode : Real = 0.0;
        attribute fixed_power : Real = 156.0;
        calc evaluate : 'Selected Flow Pump' {
            in flow_in = aries_integrated_plant::heat_exchangers.he_flow;
            in reference_flow_in = reference_flow;
            in reference_power_in = reference_power;
            in efficiency_in = efficiency;
            in reference_efficiency_in = reference_efficiency;
            in mode_in = pump_mode;
            in fixed_power_in = fixed_power;
        }
        attribute electric : Real = evaluate.electric;
        attribute operating_flow : Real = evaluate.operating_flow;
        attribute hydraulic_supported : Real = evaluate.hydraulic_supported;
        calc screen : 'Offered Capacity Screen' {
            in rating_in = selected_flow_capacity;
            in demand_in = operating_flow;
            in applicable_in = true;
            in conditions_supported_in = true;
            in demand_available_in = true;
        }
        attribute margin : Real = screen.margin;
        attribute evaluation_defined : Real = screen.evaluation_defined;
        assert constraint capacity_ok : 'Offered Equipment Capacity' {
            in defined_in = evaluation_defined;
            in margin_in = margin;
        }
    }
    part he_duty_equipment : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.2";
        attribute reference_quantity : Real = 1500.0;
        attribute reference_cost : Real = 32403166.66666667;
        attribute price_factor : Real = 1.0;
        calc purchase : 'Selected Inventory Purchase' {
            in quantity_in = aries_integrated_plant::he_capacity.selected_rating;
            in reference_quantity_in = reference_quantity;
            in reference_cost_in = reference_cost;
            in price_factor_in = price_factor;
            in mode_in = aries_integrated_plant::cost_accounts.estimate_mode;
        }
        attribute inventory_quantity : Real = purchase.purchased_quantity;
        attribute quantity_ratio : Real = purchase.quantity_ratio;
        attribute estimated_cost : Real = purchase.capital;
        attribute cost_extrapolated : Real = purchase.extrapolated;
        :>> capital_cost = purchase.capital;
    }
    part pbli_hx : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.2";
        attribute reference_quantity : Real = 50000.0;
        attribute reference_cost : Real = 58325700.00000001;
        attribute price_factor : Real = 1.0;
        calc purchase : 'Selected Inventory Purchase' {
            in quantity_in = selected_area;
            in reference_quantity_in = reference_quantity;
            in reference_cost_in = reference_cost;
            in price_factor_in = price_factor;
            in mode_in = aries_integrated_plant::cost_accounts.estimate_mode;
        }
        attribute inventory_quantity : Real = purchase.purchased_quantity;
        attribute quantity_ratio : Real = purchase.quantity_ratio;
        attribute estimated_cost : Real = purchase.capital;
        attribute cost_extrapolated : Real = purchase.extrapolated;
        :>> capital_cost = purchase.capital;
        attribute selected_area : Real = 50000.0;
        attribute assumed_u : Real = 1000.0;
        calc evaluate : 'Exchanger Area Conductance' {
            in area_in = selected_area;
            in u_in = assumed_u;
        }
        attribute ua : Real = evaluate.ua;
        attribute area : Real = evaluate.area;
    }
    part pbli_pump : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.2";
        attribute reference_quantity : Real = 26860.0;
        attribute reference_cost : Real = 19441900.0;
        attribute price_factor : Real = 1.0;
        calc purchase : 'Selected Inventory Purchase' {
            in quantity_in = selected_flow_capacity;
            in reference_quantity_in = reference_quantity;
            in reference_cost_in = reference_cost;
            in price_factor_in = price_factor;
            in mode_in = aries_integrated_plant::cost_accounts.estimate_mode;
        }
        attribute inventory_quantity : Real = purchase.purchased_quantity;
        attribute quantity_ratio : Real = purchase.quantity_ratio;
        attribute estimated_cost : Real = purchase.capital;
        attribute cost_extrapolated : Real = purchase.extrapolated;
        :>> capital_cost = purchase.capital;
        attribute selected_flow_capacity : Real = 26860.0;
        attribute efficiency : Real = 0.8;
        attribute reference_flow : Real = 26860.0;
        attribute reference_power : Real = 0.01;
        attribute reference_efficiency : Real = 0.8;
        attribute pump_mode : Real = 0.0;
        attribute fixed_power : Real = 0.01;
        calc evaluate : 'Selected Flow Pump' {
            in flow_in = aries_integrated_plant::heat_exchangers.pbli_flow;
            in reference_flow_in = reference_flow;
            in reference_power_in = reference_power;
            in efficiency_in = efficiency;
            in reference_efficiency_in = reference_efficiency;
            in mode_in = pump_mode;
            in fixed_power_in = fixed_power;
        }
        attribute electric : Real = evaluate.electric;
        attribute operating_flow : Real = evaluate.operating_flow;
        attribute hydraulic_supported : Real = evaluate.hydraulic_supported;
        calc screen : 'Offered Capacity Screen' {
            in rating_in = selected_flow_capacity;
            in demand_in = operating_flow;
            in applicable_in = true;
            in conditions_supported_in = true;
            in demand_available_in = true;
        }
        attribute margin : Real = screen.margin;
        attribute evaluation_defined : Real = screen.evaluation_defined;
        assert constraint capacity_ok : 'Offered Equipment Capacity' {
            in defined_in = evaluation_defined;
            in margin_in = margin;
        }
    }
    part pbli_duty_equipment : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.2";
        attribute reference_quantity : Real = 1800.0;
        attribute reference_cost : Real = 32403166.66666667;
        attribute price_factor : Real = 1.0;
        calc purchase : 'Selected Inventory Purchase' {
            in quantity_in = aries_integrated_plant::pbli_capacity.selected_rating;
            in reference_quantity_in = reference_quantity;
            in reference_cost_in = reference_cost;
            in price_factor_in = price_factor;
            in mode_in = aries_integrated_plant::cost_accounts.estimate_mode;
        }
        attribute inventory_quantity : Real = purchase.purchased_quantity;
        attribute quantity_ratio : Real = purchase.quantity_ratio;
        attribute estimated_cost : Real = purchase.capital;
        attribute cost_extrapolated : Real = purchase.extrapolated;
        :>> capital_cost = purchase.capital;
    }
    part divertor_hx : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.2";
        attribute reference_quantity : Real = 50000.0;
        attribute reference_cost : Real = 58325700.00000001;
        attribute price_factor : Real = 1.0;
        calc purchase : 'Selected Inventory Purchase' {
            in quantity_in = selected_area;
            in reference_quantity_in = reference_quantity;
            in reference_cost_in = reference_cost;
            in price_factor_in = price_factor;
            in mode_in = aries_integrated_plant::cost_accounts.estimate_mode;
        }
        attribute inventory_quantity : Real = purchase.purchased_quantity;
        attribute quantity_ratio : Real = purchase.quantity_ratio;
        attribute estimated_cost : Real = purchase.capital;
        attribute cost_extrapolated : Real = purchase.extrapolated;
        :>> capital_cost = purchase.capital;
        attribute selected_area : Real = 50000.0;
        attribute assumed_u : Real = 1000.0;
        calc evaluate : 'Exchanger Area Conductance' {
            in area_in = selected_area;
            in u_in = assumed_u;
        }
        attribute ua : Real = evaluate.ua;
        attribute area : Real = evaluate.area;
    }
    part divertor_pump : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.2";
        attribute reference_quantity : Real = 500.0;
        attribute reference_cost : Real = 19441900.0;
        attribute price_factor : Real = 1.0;
        calc purchase : 'Selected Inventory Purchase' {
            in quantity_in = selected_flow_capacity;
            in reference_quantity_in = reference_quantity;
            in reference_cost_in = reference_cost;
            in price_factor_in = price_factor;
            in mode_in = aries_integrated_plant::cost_accounts.estimate_mode;
        }
        attribute inventory_quantity : Real = purchase.purchased_quantity;
        attribute quantity_ratio : Real = purchase.quantity_ratio;
        attribute estimated_cost : Real = purchase.capital;
        attribute cost_extrapolated : Real = purchase.extrapolated;
        :>> capital_cost = purchase.capital;
        attribute selected_flow_capacity : Real = 500.0;
        attribute efficiency : Real = 0.8;
        attribute reference_flow : Real = 500.0;
        attribute reference_power : Real = 10.0;
        attribute reference_efficiency : Real = 0.8;
        attribute pump_mode : Real = 0.0;
        attribute fixed_power : Real = 10.0;
        calc evaluate : 'Selected Flow Pump' {
            in flow_in = aries_integrated_plant::heat_exchangers.divertor_flow;
            in reference_flow_in = reference_flow;
            in reference_power_in = reference_power;
            in efficiency_in = efficiency;
            in reference_efficiency_in = reference_efficiency;
            in mode_in = pump_mode;
            in fixed_power_in = fixed_power;
        }
        attribute electric : Real = evaluate.electric;
        attribute operating_flow : Real = evaluate.operating_flow;
        attribute hydraulic_supported : Real = evaluate.hydraulic_supported;
        calc screen : 'Offered Capacity Screen' {
            in rating_in = selected_flow_capacity;
            in demand_in = operating_flow;
            in applicable_in = true;
            in conditions_supported_in = true;
            in demand_available_in = true;
        }
        attribute margin : Real = screen.margin;
        attribute evaluation_defined : Real = screen.evaluation_defined;
        assert constraint capacity_ok : 'Offered Equipment Capacity' {
            in defined_in = evaluation_defined;
            in margin_in = margin;
        }
    }
    part divertor_duty_equipment : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.2";
        attribute reference_quantity : Real = 800.0;
        attribute reference_cost : Real = 32403166.66666667;
        attribute price_factor : Real = 1.0;
        calc purchase : 'Selected Inventory Purchase' {
            in quantity_in = aries_integrated_plant::divertor_capacity.selected_rating;
            in reference_quantity_in = reference_quantity;
            in reference_cost_in = reference_cost;
            in price_factor_in = price_factor;
            in mode_in = aries_integrated_plant::cost_accounts.estimate_mode;
        }
        attribute inventory_quantity : Real = purchase.purchased_quantity;
        attribute quantity_ratio : Real = purchase.quantity_ratio;
        attribute estimated_cost : Real = purchase.capital;
        attribute cost_extrapolated : Real = purchase.extrapolated;
        :>> capital_cost = purchase.capital;
    }
    part primary_piping : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.2";
        attribute selected_quantity : Real = 1.0;
        attribute reference_cost : Real = 58325700.0;
        attribute price_factor : Real = 1.0;
        calc estimate : 'Scaled Amount' {
            in amount_in = reference_cost;
            in factor_in = price_factor;
        }
        attribute supplied_budget : Real = estimate.amount;
        calc purchase : 'Supplied Purchase Cost' {
            in purchase_cost_in = supplied_budget;
            in n_mod_in = selected_quantity;
        }
        attribute estimated_cost : Real = purchase.cost;
        :>> capital_cost = purchase.cost;
    }
    part secondary_transport : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.2";
        attribute selected_quantity : Real = 1.0;
        attribute reference_cost : Real = 85933000.0;
        attribute price_factor : Real = 1.0;
        calc estimate : 'Scaled Amount' {
            in amount_in = reference_cost;
            in factor_in = price_factor;
        }
        attribute supplied_budget : Real = estimate.amount;
        calc purchase : 'Supplied Purchase Cost' {
            in purchase_cost_in = supplied_budget;
            in n_mod_in = selected_quantity;
        }
        attribute estimated_cost : Real = purchase.cost;
        :>> capital_cost = purchase.cost;
    }
    part compressor_equipment : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "23";
        attribute reference_quantity : Real = 1600.0;
        attribute reference_cost : Real = 78639500.0;
        attribute price_factor : Real = 1.0;
        calc purchase : 'Selected Inventory Purchase' {
            in quantity_in = aries_integrated_plant::compressor_capacity.selected_rating;
            in reference_quantity_in = reference_quantity;
            in reference_cost_in = reference_cost;
            in price_factor_in = price_factor;
            in mode_in = aries_integrated_plant::cost_accounts.estimate_mode;
        }
        attribute inventory_quantity : Real = purchase.purchased_quantity;
        attribute quantity_ratio : Real = purchase.quantity_ratio;
        attribute estimated_cost : Real = purchase.capital;
        attribute cost_extrapolated : Real = purchase.extrapolated;
        :>> capital_cost = purchase.capital;
    }
    part turbine_equipment : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "23";
        attribute reference_quantity : Real = 3500.0;
        attribute reference_cost : Real = 125823200.0;
        attribute price_factor : Real = 1.0;
        calc purchase : 'Selected Inventory Purchase' {
            in quantity_in = aries_integrated_plant::turbine_capacity.selected_rating;
            in reference_quantity_in = reference_quantity;
            in reference_cost_in = reference_cost;
            in price_factor_in = price_factor;
            in mode_in = aries_integrated_plant::cost_accounts.estimate_mode;
        }
        attribute inventory_quantity : Real = purchase.purchased_quantity;
        attribute quantity_ratio : Real = purchase.quantity_ratio;
        attribute estimated_cost : Real = purchase.capital;
        attribute cost_extrapolated : Real = purchase.extrapolated;
        :>> capital_cost = purchase.capital;
    }
    part generator_equipment : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "23";
        attribute reference_quantity : Real = 1800.0;
        attribute reference_cost : Real = 47183699.99999999;
        attribute price_factor : Real = 1.0;
        calc purchase : 'Selected Inventory Purchase' {
            in quantity_in = aries_integrated_plant::generator_capacity.selected_rating;
            in reference_quantity_in = reference_quantity;
            in reference_cost_in = reference_cost;
            in price_factor_in = price_factor;
            in mode_in = aries_integrated_plant::cost_accounts.estimate_mode;
        }
        attribute inventory_quantity : Real = purchase.purchased_quantity;
        attribute quantity_ratio : Real = purchase.quantity_ratio;
        attribute estimated_cost : Real = purchase.capital;
        attribute cost_extrapolated : Real = purchase.extrapolated;
        :>> capital_cost = purchase.capital;
    }
    part heat_rejection_equipment : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "27";
        attribute reference_quantity : Real = 2500.0;
        attribute reference_cost : Real = 56086000.0;
        attribute price_factor : Real = 1.0;
        calc purchase : 'Selected Inventory Purchase' {
            in quantity_in = aries_integrated_plant::rejection_capacity.selected_rating;
            in reference_quantity_in = reference_quantity;
            in reference_cost_in = reference_cost;
            in price_factor_in = price_factor;
            in mode_in = aries_integrated_plant::cost_accounts.estimate_mode;
        }
        attribute inventory_quantity : Real = purchase.purchased_quantity;
        attribute quantity_ratio : Real = purchase.quantity_ratio;
        attribute estimated_cost : Real = purchase.capital;
        attribute cost_extrapolated : Real = purchase.extrapolated;
        :>> capital_cost = purchase.capital;
    }
    part fuel_processing_equipment : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.5";
        attribute reference_quantity : Real = 3e+22;
        attribute reference_cost : Real = 16590000.0;
        attribute price_factor : Real = 1.0;
        calc purchase : 'Selected Inventory Purchase' {
            in quantity_in = aries_integrated_plant::fuel_capacity.selected_rating;
            in reference_quantity_in = reference_quantity;
            in reference_cost_in = reference_cost;
            in price_factor_in = price_factor;
            in mode_in = aries_integrated_plant::cost_accounts.estimate_mode;
        }
        attribute inventory_quantity : Real = purchase.purchased_quantity;
        attribute quantity_ratio : Real = purchase.quantity_ratio;
        attribute estimated_cost : Real = purchase.capital;
        attribute cost_extrapolated : Real = purchase.extrapolated;
        :>> capital_cost = purchase.capital;
    }
    part conversion_services : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "23";
        attribute selected_quantity : Real = 1.0;
        attribute reference_cost : Real = 62911600.0;
        attribute price_factor : Real = 1.0;
        calc estimate : 'Scaled Amount' {
            in amount_in = reference_cost;
            in factor_in = price_factor;
        }
        attribute supplied_budget : Real = estimate.amount;
        calc purchase : 'Supplied Purchase Cost' {
            in purchase_cost_in = supplied_budget;
            in n_mod_in = selected_quantity;
        }
        attribute estimated_cost : Real = purchase.cost;
        :>> capital_cost = purchase.cost;
    }
    part magnet_inventory : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.1.3";
        attribute reference_quantity : Real = 4092200.0;
        attribute reference_cost : Real = 204208000.0;
        attribute price_factor : Real = 1.0;
        calc purchase : 'Selected Inventory Purchase' {
            in quantity_in = selected_mass;
            in reference_quantity_in = reference_quantity;
            in reference_cost_in = reference_cost;
            in price_factor_in = price_factor;
            in mode_in = aries_integrated_plant::cost_accounts.estimate_mode;
        }
        attribute inventory_quantity : Real = purchase.purchased_quantity;
        attribute quantity_ratio : Real = purchase.quantity_ratio;
        attribute estimated_cost : Real = purchase.capital;
        attribute cost_extrapolated : Real = purchase.extrapolated;
        :>> capital_cost = purchase.capital;
        attribute selected_winding_mass : Real = 627200.0;
        attribute selected_structure_mass : Real = 3465000.0;
        calc inventory : 'Eight Amount Sum' {
            in amount1_in = selected_winding_mass;
            in amount2_in = selected_structure_mass;
            in amount3_in = 0.0;
            in amount4_in = 0.0;
            in amount5_in = 0.0;
            in amount6_in = 0.0;
            in amount7_in = 0.0;
            in amount8_in = 0.0;
        }
        attribute selected_mass : Real = inventory.total;
    }
    part vf_coils : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.1.3";
        attribute selected_quantity : Real = 1.0;
        attribute reference_cost : Real = 13358000.0;
        attribute price_factor : Real = 1.0;
        calc estimate : 'Scaled Amount' {
            in amount_in = reference_cost;
            in factor_in = price_factor;
        }
        attribute supplied_budget : Real = estimate.amount;
        calc purchase : 'Supplied Purchase Cost' {
            in purchase_cost_in = supplied_budget;
            in n_mod_in = selected_quantity;
        }
        attribute estimated_cost : Real = purchase.cost;
        :>> capital_cost = purchase.cost;
    }
    part divertor_inventory : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.1.3";
        attribute selected_quantity : Real = 1.0;
        attribute reference_cost : Real = 5318000.0;
        attribute price_factor : Real = 1.0;
        calc estimate : 'Scaled Amount' {
            in amount_in = reference_cost;
            in factor_in = price_factor;
        }
        attribute supplied_budget : Real = estimate.amount;
        calc purchase : 'Supplied Purchase Cost' {
            in purchase_cost_in = supplied_budget;
            in n_mod_in = selected_quantity;
        }
        attribute estimated_cost : Real = purchase.cost;
        :>> capital_cost = purchase.cost;
    }
    part blanket_inventory : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.1.1";
        attribute selected_mass : Real = 662500.0;
        attribute reference_quantity : Real = 662500.0;
        attribute reference_cost : Real = 59347000.0;
        attribute price_factor : Real = 1.0;
        calc purchase : 'Selected Inventory Purchase' {
            in quantity_in = selected_mass;
            in reference_quantity_in = reference_quantity;
            in reference_cost_in = reference_cost;
            in price_factor_in = price_factor;
            in mode_in = aries_integrated_plant::cost_accounts.estimate_mode;
        }
        attribute inventory_quantity : Real = purchase.purchased_quantity;
        attribute quantity_ratio : Real = purchase.quantity_ratio;
        attribute estimated_cost : Real = purchase.capital;
        attribute cost_extrapolated : Real = purchase.extrapolated;
        :>> capital_cost = purchase.capital;
    }
    part shield_inventory : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.1.2";
        attribute reference_quantity : Real = 4585000.0;
        attribute reference_cost : Real = 228627000.0;
        attribute price_factor : Real = 1.0;
        calc purchase : 'Selected Inventory Purchase' {
            in quantity_in = selected_mass;
            in reference_quantity_in = reference_quantity;
            in reference_cost_in = reference_cost;
            in price_factor_in = price_factor;
            in mode_in = aries_integrated_plant::cost_accounts.estimate_mode;
        }
        attribute inventory_quantity : Real = purchase.purchased_quantity;
        attribute quantity_ratio : Real = purchase.quantity_ratio;
        attribute estimated_cost : Real = purchase.capital;
        attribute cost_extrapolated : Real = purchase.extrapolated;
        :>> capital_cost = purchase.capital;
        attribute selected_shield_mass : Real = 3280000.0;
        attribute selected_manifold_mass : Real = 1305000.0;
        calc inventory : 'Eight Amount Sum' {
            in amount1_in = selected_shield_mass;
            in amount2_in = selected_manifold_mass;
            in amount3_in = 0.0;
            in amount4_in = 0.0;
            in amount5_in = 0.0;
            in amount6_in = 0.0;
            in amount7_in = 0.0;
            in amount8_in = 0.0;
        }
        attribute selected_mass : Real = inventory.total;
    }
    part primary_support : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.1.5";
        attribute selected_mass : Real = 2909000.0;
        attribute reference_quantity : Real = 2909000.0;
        attribute reference_cost : Real = 73126000.0;
        attribute price_factor : Real = 1.0;
        calc purchase : 'Selected Inventory Purchase' {
            in quantity_in = selected_mass;
            in reference_quantity_in = reference_quantity;
            in reference_cost_in = reference_cost;
            in price_factor_in = price_factor;
            in mode_in = aries_integrated_plant::cost_accounts.estimate_mode;
        }
        attribute inventory_quantity : Real = purchase.purchased_quantity;
        attribute quantity_ratio : Real = purchase.quantity_ratio;
        attribute estimated_cost : Real = purchase.capital;
        attribute cost_extrapolated : Real = purchase.extrapolated;
        :>> capital_cost = purchase.capital;
    }
    part vacuum_equipment : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.1.6";
        attribute reference_quantity : Real = 2773000.0;
        attribute reference_cost : Real = 137135000.0;
        attribute price_factor : Real = 1.0;
        calc purchase : 'Selected Inventory Purchase' {
            in quantity_in = selected_mass;
            in reference_quantity_in = reference_quantity;
            in reference_cost_in = reference_cost;
            in price_factor_in = price_factor;
            in mode_in = aries_integrated_plant::cost_accounts.estimate_mode;
        }
        attribute inventory_quantity : Real = purchase.purchased_quantity;
        attribute quantity_ratio : Real = purchase.quantity_ratio;
        attribute estimated_cost : Real = purchase.capital;
        attribute cost_extrapolated : Real = purchase.extrapolated;
        :>> capital_cost = purchase.capital;
        attribute selected_vessel_mass : Real = 1440000.0;
        attribute selected_cryostat_mass : Real = 1333000.0;
        calc inventory : 'Eight Amount Sum' {
            in amount1_in = selected_vessel_mass;
            in amount2_in = selected_cryostat_mass;
            in amount3_in = 0.0;
            in amount4_in = 0.0;
            in amount5_in = 0.0;
            in amount6_in = 0.0;
            in amount7_in = 0.0;
            in amount8_in = 0.0;
        }
        attribute selected_mass : Real = inventory.total;
    }
    part site_land : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "20";
        attribute selected_quantity : Real = 1.0;
        attribute reference_cost : Real = 12929000.0;
        attribute price_factor : Real = 1.0;
        calc estimate : 'Scaled Amount' {
            in amount_in = reference_cost;
            in factor_in = price_factor;
        }
        attribute supplied_budget : Real = estimate.amount;
        calc purchase : 'Supplied Purchase Cost' {
            in purchase_cost_in = supplied_budget;
            in n_mod_in = selected_quantity;
        }
        attribute estimated_cost : Real = purchase.cost;
        :>> capital_cost = purchase.cost;
    }
    part facilities : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "21";
        attribute selected_quantity : Real = 1.0;
        attribute reference_cost : Real = 336133000.0;
        attribute price_factor : Real = 1.0;
        calc estimate : 'Scaled Amount' {
            in amount_in = reference_cost;
            in factor_in = price_factor;
        }
        attribute supplied_budget : Real = estimate.amount;
        calc purchase : 'Supplied Purchase Cost' {
            in purchase_cost_in = supplied_budget;
            in n_mod_in = selected_quantity;
        }
        attribute estimated_cost : Real = purchase.cost;
        :>> capital_cost = purchase.cost;
    }
    part heating_equipment : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.1.4";
        attribute selected_quantity : Real = 1.0;
        attribute reference_cost : Real = 66427000.00000001;
        attribute price_factor : Real = 1.0;
        calc estimate : 'Scaled Amount' {
            in amount_in = reference_cost;
            in factor_in = price_factor;
        }
        attribute supplied_budget : Real = estimate.amount;
        calc purchase : 'Supplied Purchase Cost' {
            in purchase_cost_in = supplied_budget;
            in n_mod_in = selected_quantity;
        }
        attribute estimated_cost : Real = purchase.cost;
        :>> capital_cost = purchase.cost;
    }
    part magnet_power_supplies : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.1.7";
        attribute selected_quantity : Real = 1.0;
        attribute reference_cost : Real = 70624000.0;
        attribute price_factor : Real = 1.0;
        calc estimate : 'Scaled Amount' {
            in amount_in = reference_cost;
            in factor_in = price_factor;
        }
        attribute supplied_budget : Real = estimate.amount;
        calc purchase : 'Supplied Purchase Cost' {
            in purchase_cost_in = supplied_budget;
            in n_mod_in = selected_quantity;
        }
        attribute estimated_cost : Real = purchase.cost;
        :>> capital_cost = purchase.cost;
    }
    part impurity_control : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.1.8";
        attribute selected_quantity : Real = 1.0;
        attribute reference_cost : Real = 6561000.0;
        attribute price_factor : Real = 1.0;
        calc estimate : 'Scaled Amount' {
            in amount_in = reference_cost;
            in factor_in = price_factor;
        }
        attribute supplied_budget : Real = estimate.amount;
        calc purchase : 'Supplied Purchase Cost' {
            in purchase_cost_in = supplied_budget;
            in n_mod_in = selected_quantity;
        }
        attribute estimated_cost : Real = purchase.cost;
        :>> capital_cost = purchase.cost;
    }
    part auxiliary_cooling : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.3";
        attribute selected_quantity : Real = 1.0;
        attribute reference_cost : Real = 3735000.0;
        attribute price_factor : Real = 1.0;
        calc estimate : 'Scaled Amount' {
            in amount_in = reference_cost;
            in factor_in = price_factor;
        }
        attribute supplied_budget : Real = estimate.amount;
        calc purchase : 'Supplied Purchase Cost' {
            in purchase_cost_in = supplied_budget;
            in n_mod_in = selected_quantity;
        }
        attribute estimated_cost : Real = purchase.cost;
        :>> capital_cost = purchase.cost;
    }
    part waste_equipment : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.4";
        attribute selected_quantity : Real = 1.0;
        attribute reference_cost : Real = 6655000.0;
        attribute price_factor : Real = 1.0;
        calc estimate : 'Scaled Amount' {
            in amount_in = reference_cost;
            in factor_in = price_factor;
        }
        attribute supplied_budget : Real = estimate.amount;
        calc purchase : 'Supplied Purchase Cost' {
            in purchase_cost_in = supplied_budget;
            in n_mod_in = selected_quantity;
        }
        attribute estimated_cost : Real = purchase.cost;
        :>> capital_cost = purchase.cost;
    }
    part fuel_services : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.5";
        attribute selected_quantity : Real = 1.0;
        attribute reference_cost : Real = 38689000.0;
        attribute price_factor : Real = 1.0;
        calc estimate : 'Scaled Amount' {
            in amount_in = reference_cost;
            in factor_in = price_factor;
        }
        attribute supplied_budget : Real = estimate.amount;
        calc purchase : 'Supplied Purchase Cost' {
            in purchase_cost_in = supplied_budget;
            in n_mod_in = selected_quantity;
        }
        attribute estimated_cost : Real = purchase.cost;
        :>> capital_cost = purchase.cost;
    }
    part other_reactor_equipment : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.6";
        attribute selected_quantity : Real = 1.0;
        attribute reference_cost : Real = 60723000.0;
        attribute price_factor : Real = 1.0;
        calc estimate : 'Scaled Amount' {
            in amount_in = reference_cost;
            in factor_in = price_factor;
        }
        attribute supplied_budget : Real = estimate.amount;
        calc purchase : 'Supplied Purchase Cost' {
            in purchase_cost_in = supplied_budget;
            in n_mod_in = selected_quantity;
        }
        attribute estimated_cost : Real = purchase.cost;
        :>> capital_cost = purchase.cost;
    }
    part instrumentation_control : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22.7";
        attribute selected_quantity : Real = 1.0;
        attribute reference_cost : Real = 44558000.0;
        attribute price_factor : Real = 1.0;
        calc estimate : 'Scaled Amount' {
            in amount_in = reference_cost;
            in factor_in = price_factor;
        }
        attribute supplied_budget : Real = estimate.amount;
        calc purchase : 'Supplied Purchase Cost' {
            in purchase_cost_in = supplied_budget;
            in n_mod_in = selected_quantity;
        }
        attribute estimated_cost : Real = purchase.cost;
        :>> capital_cost = purchase.cost;
    }
    part unallocated_source_scope : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "22";
        attribute selected_quantity : Real = 1.0;
        attribute reference_cost : Real = 28396000.0;
        attribute price_factor : Real = 1.0;
        calc estimate : 'Scaled Amount' {
            in amount_in = reference_cost;
            in factor_in = price_factor;
        }
        attribute supplied_budget : Real = estimate.amount;
        calc purchase : 'Supplied Purchase Cost' {
            in purchase_cost_in = supplied_budget;
            in n_mod_in = selected_quantity;
        }
        attribute estimated_cost : Real = purchase.cost;
        :>> capital_cost = purchase.cost;
    }
    part electrical_equipment : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "24";
        attribute selected_quantity : Real = 1.0;
        attribute reference_cost : Real = 138764000.0;
        attribute price_factor : Real = 1.0;
        calc estimate : 'Scaled Amount' {
            in amount_in = reference_cost;
            in factor_in = price_factor;
        }
        attribute supplied_budget : Real = estimate.amount;
        calc purchase : 'Supplied Purchase Cost' {
            in purchase_cost_in = supplied_budget;
            in n_mod_in = selected_quantity;
        }
        attribute estimated_cost : Real = purchase.cost;
        :>> capital_cost = purchase.cost;
    }
    part miscellaneous_equipment : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "25";
        attribute selected_quantity : Real = 1.0;
        attribute reference_cost : Real = 70958000.0;
        attribute price_factor : Real = 1.0;
        calc estimate : 'Scaled Amount' {
            in amount_in = reference_cost;
            in factor_in = price_factor;
        }
        attribute supplied_budget : Real = estimate.amount;
        calc purchase : 'Supplied Purchase Cost' {
            in purchase_cost_in = supplied_budget;
            in n_mod_in = selected_quantity;
        }
        attribute estimated_cost : Real = purchase.cost;
        :>> capital_cost = purchase.cost;
    }
    part lipb_inventory : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "26";
        attribute reference_quantity : Real = 8830000.0;
        attribute reference_cost : Real = 151327000.0;
        attribute price_factor : Real = 1.0;
        calc purchase : 'Selected Inventory Purchase' {
            in quantity_in = total_mass;
            in reference_quantity_in = reference_quantity;
            in reference_cost_in = reference_cost;
            in price_factor_in = price_factor;
            in mode_in = aries_integrated_plant::cost_accounts.estimate_mode;
        }
        attribute inventory_quantity : Real = purchase.purchased_quantity;
        attribute quantity_ratio : Real = purchase.quantity_ratio;
        attribute estimated_cost : Real = purchase.capital;
        attribute cost_extrapolated : Real = purchase.extrapolated;
        :>> capital_cost = purchase.capital;
        attribute selected_core_mass : Real = 3532000.0;
        attribute external_mass_factor : Real = 2.5;
        calc inventory : 'Scaled Amount' {
            in amount_in = selected_core_mass;
            in factor_in = external_mass_factor;
        }
        attribute total_mass : Real = inventory.amount;
    }
    part fuel_inventory : 'Selected Equipment' {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        :>> cas_code = "26.fuel";
        attribute selected_tritium_kg : Real = 10.0;
        attribute process_residence_s : Real = 1000.0;
        // New usable T feed [kg/calendar year], excluding already recycled exhaust; no breeding qualification.
        attribute annual_recovery_kg : Real = 0.0;
        attribute tritium_price : Real = 30000000.0;
        attribute deuterium_price : Real = 1000.0;
        attribute deuterium_atom_kg : Real = 3.3435837724e-27;
        calc atoms : 'Selected Stock Atoms' {
            in stock_kg_in = selected_tritium_kg;
            in atom_mass_in = aries_integrated_plant::fuel.tritium_atom_kg;
        }
        attribute selected_tritium_atoms : Real = atoms.atoms;
        calc purchase : 'Scaled Amount' {
            in amount_in = selected_tritium_kg;
            in factor_in = tritium_price;
        }
        attribute initial_stock_cost : Real = purchase.amount;
        :>> capital_cost = purchase.amount;
        calc annual : 'Annual Selected Fuel' {
            in stock_kg_in = selected_tritium_kg;
            in atom_mass_in = aries_integrated_plant::fuel.tritium_atom_kg;
            in decay_in = aries_integrated_plant::fuel.decay_constant_s;
            in seconds_in = aries_integrated_plant::fuel.seconds_per_year;
            in availability_in = aries_integrated_plant::cost_schedule.availability;
            in burn_in = aries_integrated_plant::fuel.burn_rate;
            in loss_in = aries_integrated_plant::fuel.loss_rate;
            in exhaust_in = aries_integrated_plant::fuel.exhaust_rate;
            in residence_in = process_residence_s;
            in annual_recovery_in = annual_recovery_kg;
            in tritium_price_in = tritium_price;
        }
        attribute annual_burn : Real = annual.annual_burn;
        attribute annual_loss : Real = annual.annual_loss;
        attribute annual_decay : Real = annual.annual_decay;
        attribute annual_recovery : Real = annual.annual_recovery;
        attribute annual_external : Real = annual.annual_external;
        attribute annual_cost : Real = annual.annual_cost;
        attribute required_stock : Real = annual.required_stock;
        attribute breeding_supported : Real = annual.breeding_supported;
        calc screen : 'Offered Capacity Screen' {
            in rating_in = selected_tritium_kg;
            in demand_in = required_stock;
            in applicable_in = true;
            in conditions_supported_in = true;
            in demand_available_in = true;
        }
        attribute margin : Real = screen.margin;
        attribute evaluation_defined : Real = screen.evaluation_defined;
        assert constraint capacity_ok : 'Offered Equipment Capacity' {
            in defined_in = evaluation_defined;
            in margin_in = margin;
        }
        calc deuterium_rate : 'Scaled Amount' {
            in amount_in = deuterium_atom_kg;
            in factor_in = deuterium_price;
        }
        attribute deuterium_per_reaction : Real = deuterium_rate.amount;
        calc deuterium : 'DT Fuel Cost' {
            in p_fus = aries_integrated_plant::source.selected_power;
            in n_mod_in = aries_integrated_plant::cost_accounts.one_module;
            in availability_in = aries_integrated_plant::cost_schedule.availability;
            in cost_per_rxn = deuterium_per_reaction;
            in q_eff = aries_integrated_plant::fuel.reaction_energy_mev;
            in mev_to_joules_in = aries_integrated_plant::fuel.mev_joules;
            in burn_fraction_in = aries_integrated_plant::fuel.pass_burn_fraction;
            in fuel_recovery_in = aries_integrated_plant::fuel.exhaust_recovery;
        }
        attribute annual_deuterium_cost : Real = deuterium.annual_fuel;
    }
    part source_budget {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        attribute account_1 : Real = 12929000.0;
        attribute account_2 : Real = 336133000.0;
        attribute account_3 : Real = 1538817000.0;
        attribute account_4 : Real = 314558000.0;
        attribute account_5 : Real = 138764000.0;
        attribute account_6 : Real = 70958000.0;
        attribute account_7 : Real = 151327000.0;
        attribute account_8 : Real = 56086000.0;
        attribute inclusive_multiplier : Real = 1.93;
        calc evaluate : 'Disjoint Capital Budget' {
            in account_1_in = account_1;
            in account_2_in = account_2;
            in account_3_in = account_3;
            in account_4_in = account_4;
            in account_5_in = account_5;
            in account_6_in = account_6;
            in account_7_in = account_7;
            in account_8_in = account_8;
            in inclusive_multiplier_in = inclusive_multiplier;
        }
        attribute direct_total : Real = evaluate.direct_total;
        attribute inclusive_capital : Real = evaluate.inclusive_capital;
    }
    part source_reactor_children {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Eight Amount Sum' {
            in amount1_in = aries_integrated_plant::source_reconciliation.core_parent;
            in amount2_in = 474771000.0;
            in amount3_in = 3735000.0;
            in amount4_in = 6655000.0;
            in amount5_in = aries_integrated_plant::source_reconciliation.fuel_parent;
            in amount6_in = 60723000.0;
            in amount7_in = 44558000.0;
            in amount8_in = 0.0;
        }
        attribute total : Real = evaluate.total;
    }
    part source_core_children_first {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Eight Amount Sum' {
            in amount1_in = 59347000.0;
            in amount2_in = 228627000.0;
            in amount3_in = aries_integrated_plant::source_reconciliation.coil_parent;
            in amount4_in = 66427000.0;
            in amount5_in = 73126000.0;
            in amount6_in = 137135000.0;
            in amount7_in = 70624000.0;
            in amount8_in = 6561000.0;
        }
        attribute total : Real = evaluate.total;
    }
    part source_coil_children {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Eight Amount Sum' {
            in amount1_in = 115960000.0;
            in amount2_in = 13358000.0;
            in amount3_in = 5318000.0;
            in amount4_in = 93535000.0;
            in amount5_in = 0.0;
            in amount6_in = 0.0;
            in amount7_in = 0.0;
            in amount8_in = 0.0;
        }
        attribute total : Real = evaluate.total;
    }
    part source_fuel_children {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Eight Amount Sum' {
            in amount1_in = 14134000.0;
            in amount2_in = 16590000.0;
            in amount3_in = 7067000.0;
            in amount4_in = 3353000.0;
            in amount5_in = 7067000.0;
            in amount6_in = 7067000.0;
            in amount7_in = 0.0;
            in amount8_in = 0.0;
        }
        attribute total : Real = evaluate.total;
    }
    part source_reconciliation {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        attribute core_parent : Real = 864700000.0;
        attribute coil_parent : Real = 222884000.0;
        attribute fuel_parent : Real = 55279000.0;
        calc reactor_gap_calc : 'Comparison Difference' {
            in left_in = aries_integrated_plant::source_budget.account_3;
            in right_in = aries_integrated_plant::source_reactor_children.total;
        }
        attribute reactor_gap : Real = reactor_gap_calc.difference;
        calc core_excess_calc : 'Comparison Difference' {
            in left_in = aries_integrated_plant::source_core_children_first.total;
            in right_in = core_parent;
        }
        attribute core_excess : Real = core_excess_calc.difference;
        calc coil_excess_calc : 'Comparison Difference' {
            in left_in = aries_integrated_plant::source_coil_children.total;
            in right_in = coil_parent;
        }
        attribute coil_excess : Real = coil_excess_calc.difference;
        calc fuel_gap_calc : 'Comparison Difference' {
            in left_in = fuel_parent;
            in right_in = aries_integrated_plant::source_fuel_children.total;
        }
        attribute fuel_gap : Real = fuel_gap_calc.difference;
    }
    part known_dry_inventory {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Eight Amount Sum' {
            in amount1_in = aries_integrated_plant::magnet_inventory.selected_mass;
            in amount2_in = aries_integrated_plant::blanket_inventory.selected_mass;
            in amount3_in = aries_integrated_plant::shield_inventory.selected_mass;
            in amount4_in = aries_integrated_plant::vacuum_equipment.selected_mass;
            in amount5_in = aries_integrated_plant::primary_support.selected_mass;
            in amount6_in = 0.0;
            in amount7_in = 0.0;
            in amount8_in = 0.0;
        }
        attribute total : Real = evaluate.total;
    }
    part inventory_comparison {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        attribute source_dry_core_mass : Real = 13688000.0;
        attribute vf_mass_available : Real = 0.0;
        calc evaluate : 'Comparison Difference' {
            in left_in = aries_integrated_plant::known_dry_inventory.total;
            in right_in = source_dry_core_mass;
        }
        attribute known_mass_minus_source : Real = evaluate.difference;
        calc support : 'Scaled Amount' {
            in amount_in = vf_mass_available;
            in factor_in = 1.0;
        }
        attribute vf_mass_availability : Real = support.amount;
    }
    part lipb_comparison {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        attribute source_unit_rate : Real = 17.1;
        calc price : 'Scaled Amount' {
            in amount_in = aries_integrated_plant::lipb_inventory.total_mass;
            in factor_in = source_unit_rate;
        }
        attribute material_price : Real = price.amount;
        calc evaluate : 'Comparison Difference' {
            in left_in = material_price;
            in right_in = aries_integrated_plant::source_budget.account_7;
        }
        attribute material_minus_source : Real = evaluate.difference;
    }
    part source_replacement_comparison {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        attribute event_cost : Real = 75000000.0;
        attribute events : Real = 13.0;
        attribute event_mass : Real = 842000.0;
        attribute printed_lifetime_cost : Real = 966000000.0;
        calc cost : 'Scaled Amount' {
            in amount_in = event_cost;
            in factor_in = events;
        }
        attribute rounded_lifetime_cost : Real = cost.amount;
        calc mass : 'Scaled Amount' {
            in amount_in = event_mass;
            in factor_in = events;
        }
        attribute lifetime_mass : Real = mass.amount;
        calc evaluate : 'Comparison Difference' {
            in left_in = rounded_lifetime_cost;
            in right_in = printed_lifetime_cost;
        }
        attribute rounded_minus_printed : Real = evaluate.difference;
    }
    part core_first {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Eight Amount Sum' {
            in amount1_in = aries_integrated_plant::blanket_inventory.capital_cost;
            in amount2_in = aries_integrated_plant::shield_inventory.capital_cost;
            in amount3_in = aries_integrated_plant::magnet_inventory.capital_cost;
            in amount4_in = aries_integrated_plant::vf_coils.capital_cost;
            in amount5_in = aries_integrated_plant::divertor_inventory.capital_cost;
            in amount6_in = aries_integrated_plant::heating_equipment.capital_cost;
            in amount7_in = aries_integrated_plant::primary_support.capital_cost;
            in amount8_in = aries_integrated_plant::vacuum_equipment.capital_cost;
        }
        attribute total : Real = evaluate.total;
    }
    part core_cost {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Eight Amount Sum' {
            in amount1_in = aries_integrated_plant::core_first.total;
            in amount2_in = aries_integrated_plant::magnet_power_supplies.capital_cost;
            in amount3_in = aries_integrated_plant::impurity_control.capital_cost;
            in amount4_in = 0.0;
            in amount5_in = 0.0;
            in amount6_in = 0.0;
            in amount7_in = 0.0;
            in amount8_in = 0.0;
        }
        attribute total : Real = evaluate.total;
    }
    part primary_heat_cost {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Eight Amount Sum' {
            in amount1_in = aries_integrated_plant::he_hx.capital_cost;
            in amount2_in = aries_integrated_plant::pbli_hx.capital_cost;
            in amount3_in = aries_integrated_plant::divertor_hx.capital_cost;
            in amount4_in = aries_integrated_plant::he_pump.capital_cost;
            in amount5_in = aries_integrated_plant::pbli_pump.capital_cost;
            in amount6_in = aries_integrated_plant::divertor_pump.capital_cost;
            in amount7_in = aries_integrated_plant::primary_piping.capital_cost;
            in amount8_in = 0.0;
        }
        attribute total : Real = evaluate.total;
    }
    part heat_transport_cost {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Eight Amount Sum' {
            in amount1_in = aries_integrated_plant::primary_heat_cost.total;
            in amount2_in = aries_integrated_plant::he_duty_equipment.capital_cost;
            in amount3_in = aries_integrated_plant::pbli_duty_equipment.capital_cost;
            in amount4_in = aries_integrated_plant::divertor_duty_equipment.capital_cost;
            in amount5_in = aries_integrated_plant::secondary_transport.capital_cost;
            in amount6_in = 0.0;
            in amount7_in = 0.0;
            in amount8_in = 0.0;
        }
        attribute total : Real = evaluate.total;
    }
    part fuel_equipment {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Eight Amount Sum' {
            in amount1_in = aries_integrated_plant::fuel_processing_equipment.capital_cost;
            in amount2_in = aries_integrated_plant::fuel_services.capital_cost;
            in amount3_in = 0.0;
            in amount4_in = 0.0;
            in amount5_in = 0.0;
            in amount6_in = 0.0;
            in amount7_in = 0.0;
            in amount8_in = 0.0;
        }
        attribute total : Real = evaluate.total;
    }
    part reactor_cost {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Eight Amount Sum' {
            in amount1_in = aries_integrated_plant::core_cost.total;
            in amount2_in = aries_integrated_plant::heat_transport_cost.total;
            in amount3_in = aries_integrated_plant::auxiliary_cooling.capital_cost;
            in amount4_in = aries_integrated_plant::waste_equipment.capital_cost;
            in amount5_in = aries_integrated_plant::fuel_equipment.total;
            in amount6_in = aries_integrated_plant::other_reactor_equipment.capital_cost;
            in amount7_in = aries_integrated_plant::instrumentation_control.capital_cost;
            in amount8_in = aries_integrated_plant::unallocated_source_scope.capital_cost;
        }
        attribute total : Real = evaluate.total;
    }
    part conversion_equipment {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Eight Amount Sum' {
            in amount1_in = aries_integrated_plant::compressor_equipment.capital_cost;
            in amount2_in = aries_integrated_plant::turbine_equipment.capital_cost;
            in amount3_in = aries_integrated_plant::generator_equipment.capital_cost;
            in amount4_in = aries_integrated_plant::conversion_services.capital_cost;
            in amount5_in = 0.0;
            in amount6_in = 0.0;
            in amount7_in = 0.0;
            in amount8_in = 0.0;
        }
        attribute total : Real = evaluate.total;
    }
    part direct_source_scope {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Eight Amount Sum' {
            in amount1_in = aries_integrated_plant::site_land.capital_cost;
            in amount2_in = aries_integrated_plant::facilities.capital_cost;
            in amount3_in = aries_integrated_plant::reactor_cost.total;
            in amount4_in = aries_integrated_plant::conversion_equipment.total;
            in amount5_in = aries_integrated_plant::electrical_equipment.capital_cost;
            in amount6_in = aries_integrated_plant::miscellaneous_equipment.capital_cost;
            in amount7_in = aries_integrated_plant::lipb_inventory.capital_cost;
            in amount8_in = aries_integrated_plant::heat_rejection_equipment.capital_cost;
        }
        attribute total : Real = evaluate.total;
    }
    part direct_cost {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Eight Amount Sum' {
            in amount1_in = aries_integrated_plant::direct_source_scope.total;
            in amount2_in = aries_integrated_plant::fuel_inventory.capital_cost;
            in amount3_in = 0.0;
            in amount4_in = 0.0;
            in amount5_in = 0.0;
            in amount6_in = 0.0;
            in amount7_in = 0.0;
            in amount8_in = 0.0;
        }
        attribute total : Real = evaluate.total;
    }
    part indirect_cost {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        attribute fraction : Real = 0.2;
        calc evaluate : 'Indirect Cost' {
            in indirect_fraction_in = fraction;
            in direct_cost = aries_integrated_plant::direct_cost.total;
            in construction_time = 6.0;
            in reference_construction_time = 6.0;
        }
        attribute amount : Real = evaluate.cost;
    }
    part contingency_basis {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Eight Amount Sum' {
            in amount1_in = aries_integrated_plant::direct_cost.total;
            in amount2_in = aries_integrated_plant::indirect_cost.amount;
            in amount3_in = 0.0;
            in amount4_in = 0.0;
            in amount5_in = 0.0;
            in amount6_in = 0.0;
            in amount7_in = 0.0;
            in amount8_in = 0.0;
        }
        attribute total : Real = evaluate.total;
    }
    part contingency {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        attribute fraction : Real = 0.2;
        calc evaluate : 'Contingency Cost' {
            in contingency_rate_in = fraction;
            in direct_subtotal = aries_integrated_plant::contingency_basis.total;
        }
        attribute amount : Real = evaluate.cost;
    }
    part owner_commissioning {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        attribute fraction : Real = 0.05;
        calc evaluate : 'Scaled Amount' {
            in amount_in = aries_integrated_plant::direct_cost.total;
            in factor_in = fraction;
        }
        attribute amount : Real = evaluate.amount;
    }
    part annual_om {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        attribute selected_amount : Real = 70000000.0;
        calc evaluate : 'Annual OM Cost' {
            in om_ref = 0.0;
            in p_net = 1000.0;
            in n_mod_in = 1.0;
            in ref_net_power = 1000.0;
            in alpha = 0.5;
            in om_direct = selected_amount;
        }
        attribute amount : Real = evaluate.annual_om;
    }
    part replacement_lipb {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Scaled Amount' {
            in amount_in = aries_integrated_plant::lipb_inventory.capital_cost;
            in factor_in = aries_integrated_plant::cost_schedule.lipb_makeup_fraction;
        }
        attribute amount : Real = evaluate.amount;
    }
    part replacement_scope {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Eight Amount Sum' {
            in amount1_in = aries_integrated_plant::blanket_inventory.capital_cost;
            in amount2_in = aries_integrated_plant::divertor_inventory.capital_cost;
            in amount3_in = aries_integrated_plant::replacement_lipb.amount;
            in amount4_in = 0.0;
            in amount5_in = 0.0;
            in amount6_in = 0.0;
            in amount7_in = 0.0;
            in amount8_in = 0.0;
        }
        attribute total : Real = evaluate.total;
    }
    part replacement_price {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Scaled Amount' {
            in amount_in = aries_integrated_plant::replacement_scope.total;
            in factor_in = aries_integrated_plant::cost_schedule.replacement_factor;
        }
        attribute amount : Real = evaluate.amount;
    }
    part replacement {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Replacement Events' {
            in event_cost_in = aries_integrated_plant::replacement_price.amount;
            in life_fpy_in = aries_integrated_plant::cost_schedule.replacement_life_fpy;
            in availability_in = aries_integrated_plant::cost_schedule.availability;
            in plant_years_in = aries_integrated_plant::cost_schedule.plant_years;
        }
        attribute event_cost : Real = evaluate.event_cost;
        attribute interval_years : Real = evaluate.interval_years;
        attribute event_count : Real = evaluate.event_count;
        attribute lifetime_total : Real = evaluate.lifetime_total;
        attribute annual_reserve : Real = evaluate.annual_reserve;
        attribute first_event_year : Real = evaluate.first_event_year;
        attribute last_event_year : Real = evaluate.last_event_year;
    }
    part cost_ledger {
        doc /* **Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22. */
        attribute consumables : Real = 5000000.0;
        attribute import_price : Real = 50.0;
        calc evaluate : 'Equipment Cost Ledger' {
            in direct_in = aries_integrated_plant::direct_cost.total;
            in source_direct_in = aries_integrated_plant::source_budget.direct_total;
            in source_inclusive_in = aries_integrated_plant::source_budget.inclusive_capital;
            in indirect_in = aries_integrated_plant::indirect_cost.amount;
            in contingency_in = aries_integrated_plant::contingency.amount;
            in owner_in = aries_integrated_plant::owner_commissioning.amount;
            in om_in = aries_integrated_plant::annual_om.amount;
            in tritium_in = aries_integrated_plant::fuel_inventory.annual_cost;
            in deuterium_in = aries_integrated_plant::fuel_inventory.annual_deuterium_cost;
            in consumables_in = consumables;
            in replacement_reserve_in = aries_integrated_plant::replacement.annual_reserve;
            in replacement_total_in = aries_integrated_plant::replacement.lifetime_total;
            in net_power_in = aries_integrated_plant::plant_ledger.net_electric;
            in availability_in = aries_integrated_plant::cost_schedule.availability;
            in import_price_in = import_price;
            in source_reactor_gap_in = aries_integrated_plant::source_reconciliation.reactor_gap;
            in source_core_excess_in = aries_integrated_plant::source_reconciliation.core_excess;
            in source_coil_excess_in = aries_integrated_plant::source_reconciliation.coil_excess;
            in currency_year_in = 2004.0;
        }
        attribute direct : Real = evaluate.direct;
        attribute source_direct : Real = evaluate.source_direct;
        attribute source_inclusive : Real = evaluate.source_inclusive;
        attribute direct_difference : Real = evaluate.direct_difference;
        attribute overnight : Real = evaluate.overnight;
        attribute annual_operating : Real = evaluate.annual_operating;
        attribute annual_replacement_reserve : Real = evaluate.annual_replacement_reserve;
        attribute lifetime_replacement : Real = evaluate.lifetime_replacement;
        attribute annual_export_mwh : Real = evaluate.annual_export_mwh;
        attribute annual_import_mwh : Real = evaluate.annual_import_mwh;
        attribute annual_import_cost : Real = evaluate.annual_import_cost;
        attribute source_reactor_gap : Real = evaluate.source_reactor_gap;
        attribute source_core_excess : Real = evaluate.source_core_excess;
        attribute source_coil_excess : Real = evaluate.source_coil_excess;
        attribute currency_year : Real = evaluate.currency_year;
    }
    part finance {
        doc /* **Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22. */
        attribute discount_rate : Real = 0.05;
        attribute construction_years : Real = 6.0;
        attribute terminal_fraction : Real = 0.1;
        attribute salvage_fraction : Real = 0.02;
        attribute other_overhaul_fraction : Real = 0.05;
        attribute other_overhaul_year : Real = 20.0;
        attribute supply_service_annual : Real = 0.0;
    }
    part source_finance {
        doc /* **Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22. */
        attribute net_power : Real = 1000.0;
        // Boundary validation only: supported domain {0}; not a sensitivity axis.
        attribute construction_years : Real = 0.0;
        calc boundary : 'Already Financed Duration' {
            in years_in = construction_years;
        }
        attribute validated_years : Real = boundary.years;
    }
    part operating_levelization {
        doc /* **Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Levelized Annual Cost' {
            in annual_cost = aries_integrated_plant::cost_ledger.annual_operating;
            in interest_rate = aries_integrated_plant::finance.discount_rate;
            in inflation_rate_in = 0.0;
            in operational_years_in = aries_integrated_plant::cost_schedule.plant_years;
            in project_time = 0.0;
        }
        attribute factor : Real = evaluate.crf;
        attribute annual : Real = evaluate.levelized;
    }
    part source_finance_energy {
        doc /* **Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Supplied Annual Energy' {
            in net_power_in = aries_integrated_plant::source_finance.net_power;
            in availability_in = aries_integrated_plant::cost_schedule.availability;
        }
        attribute annual_energy : Real = evaluate.annual_energy;
    }
    part lifecycle_accounts {
        doc /* **Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Lifecycle Cashflow Accounts' {
            in overnight_in = aries_integrated_plant::cost_ledger.overnight;
            in net_power_in = aries_integrated_plant::plant_ledger.net_electric;
            in annual_energy_in = aries_integrated_plant::cost_ledger.annual_export_mwh;
            in annual_operating_in = aries_integrated_plant::cost_ledger.annual_operating;
            in om_in = aries_integrated_plant::annual_om.amount;
            in tritium_in = aries_integrated_plant::fuel_inventory.annual_cost;
            in deuterium_in = aries_integrated_plant::fuel_inventory.annual_deuterium_cost;
            in consumables_in = aries_integrated_plant::cost_ledger.consumables;
            in imports_in = aries_integrated_plant::cost_ledger.annual_import_cost;
            in supply_service_in = aries_integrated_plant::finance.supply_service_annual;
            in crf_in = aries_integrated_plant::operating_levelization.factor;
            in discount_in = aries_integrated_plant::finance.discount_rate;
            in construction_years_in = aries_integrated_plant::finance.construction_years;
            in plant_years_in = aries_integrated_plant::cost_schedule.plant_years;
            in availability_in = aries_integrated_plant::cost_schedule.availability;
            in event_cost_in = aries_integrated_plant::replacement.event_cost;
            in interval_years_in = aries_integrated_plant::replacement.interval_years;
            in event_count_in = aries_integrated_plant::replacement.event_count;
            in terminal_fraction_in = aries_integrated_plant::finance.terminal_fraction;
            in salvage_fraction_in = aries_integrated_plant::finance.salvage_fraction;
            in other_overhaul_fraction_in = aries_integrated_plant::finance.other_overhaul_fraction;
            in other_overhaul_year_in = aries_integrated_plant::finance.other_overhaul_year;
            in annual_burn_in = aries_integrated_plant::fuel_inventory.annual_burn;
            in annual_loss_in = aries_integrated_plant::fuel_inventory.annual_loss;
            in annual_decay_in = aries_integrated_plant::fuel_inventory.annual_decay;
            in annual_feed_in = aries_integrated_plant::fuel_inventory.annual_recovery_kg;
            in external_shortfall_in = aries_integrated_plant::fuel_inventory.annual_external;
        }
        attribute noncapital_annual : Real = evaluate.noncapital_annual;
        attribute financed_capital : Real = evaluate.financed_capital;
        attribute idc : Real = evaluate.idc;
        attribute annual_capital : Real = evaluate.annual_capital;
        attribute annual_energy : Real = evaluate.annual_energy;
        attribute lifetime_energy : Real = evaluate.lifetime_energy;
        attribute pv_energy : Real = evaluate.pv_energy;
        attribute pv_operating : Real = evaluate.pv_operating;
        attribute pv_supply : Real = evaluate.pv_supply;
        attribute pv_replacement : Real = evaluate.pv_replacement;
        attribute pv_other_overhaul : Real = evaluate.pv_other_overhaul;
        attribute gross_terminal : Real = evaluate.gross_terminal;
        attribute salvage : Real = evaluate.salvage;
        attribute pv_terminal_gross : Real = evaluate.pv_terminal_gross;
        attribute pv_salvage : Real = evaluate.pv_salvage;
        attribute pv_terminal_net : Real = evaluate.pv_terminal_net;
        attribute other_overhaul_cost : Real = evaluate.other_overhaul_cost;
        attribute other_overhaul_occurs : Real = evaluate.other_overhaul_occurs;
        attribute pv_total_cost : Real = evaluate.pv_total_cost;
        attribute lcoe_sum : Real = evaluate.lcoe_sum;
        attribute capital_lcoe : Real = evaluate.capital_lcoe;
        attribute om_lcoe : Real = evaluate.om_lcoe;
        attribute tritium_lcoe : Real = evaluate.tritium_lcoe;
        attribute deuterium_lcoe : Real = evaluate.deuterium_lcoe;
        attribute consumables_lcoe : Real = evaluate.consumables_lcoe;
        attribute imports_lcoe : Real = evaluate.imports_lcoe;
        attribute supply_lcoe : Real = evaluate.supply_lcoe;
        attribute replacement_lcoe : Real = evaluate.replacement_lcoe;
        attribute other_overhaul_lcoe : Real = evaluate.other_overhaul_lcoe;
        attribute terminal_lcoe : Real = evaluate.terminal_lcoe;
        attribute salvage_lcoe : Real = evaluate.salvage_lcoe;
        attribute gross_makeup : Real = evaluate.gross_makeup;
        attribute new_feed : Real = evaluate.new_feed;
        attribute external_shortfall : Real = evaluate.external_shortfall;
        attribute curtailed_feed : Real = evaluate.curtailed_feed;
        attribute supply_supported : Real = evaluate.supply_supported;
        attribute breeding_supported : Real = evaluate.breeding_supported;
        attribute financial_defined : Real = evaluate.financial_defined;
        attribute currency_year : Real = evaluate.currency_year;
        attribute real_convention : Real = evaluate.real_convention;
    }
    part lifecycle_price {
        doc /* **Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22. */
        calc evaluate : 'LCOE DCF' {
            in total_capital_in = aries_integrated_plant::cost_ledger.overnight;
            in annual_om_in = aries_integrated_plant::lifecycle_accounts.noncapital_annual;
            in net_electric_mw = aries_integrated_plant::plant_ledger.net_electric;
            in availability_in = aries_integrated_plant::cost_schedule.availability;
            in discount_rate_in = aries_integrated_plant::finance.discount_rate;
            in construction_years_in = aries_integrated_plant::finance.construction_years;
            in operational_years_in = aries_integrated_plant::cost_schedule.plant_years;
        }
        attribute lcoe : Real = evaluate.lcoe;
    }
    part source_lifecycle_accounts {
        doc /* **Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Lifecycle Cashflow Accounts' {
            in overnight_in = aries_integrated_plant::source_budget.inclusive_capital;
            in net_power_in = aries_integrated_plant::source_finance.net_power;
            in annual_energy_in = aries_integrated_plant::source_finance_energy.annual_energy;
            in annual_operating_in = aries_integrated_plant::cost_ledger.annual_operating;
            in om_in = aries_integrated_plant::annual_om.amount;
            in tritium_in = aries_integrated_plant::fuel_inventory.annual_cost;
            in deuterium_in = aries_integrated_plant::fuel_inventory.annual_deuterium_cost;
            in consumables_in = aries_integrated_plant::cost_ledger.consumables;
            in imports_in = aries_integrated_plant::cost_ledger.annual_import_cost;
            in supply_service_in = aries_integrated_plant::finance.supply_service_annual;
            in crf_in = aries_integrated_plant::operating_levelization.factor;
            in discount_in = aries_integrated_plant::finance.discount_rate;
            in construction_years_in = aries_integrated_plant::source_finance.validated_years;
            in plant_years_in = aries_integrated_plant::cost_schedule.plant_years;
            in availability_in = aries_integrated_plant::cost_schedule.availability;
            in event_cost_in = aries_integrated_plant::replacement.event_cost;
            in interval_years_in = aries_integrated_plant::replacement.interval_years;
            in event_count_in = aries_integrated_plant::replacement.event_count;
            in terminal_fraction_in = aries_integrated_plant::finance.terminal_fraction;
            in salvage_fraction_in = aries_integrated_plant::finance.salvage_fraction;
            in other_overhaul_fraction_in = aries_integrated_plant::finance.other_overhaul_fraction;
            in other_overhaul_year_in = aries_integrated_plant::finance.other_overhaul_year;
            in annual_burn_in = aries_integrated_plant::fuel_inventory.annual_burn;
            in annual_loss_in = aries_integrated_plant::fuel_inventory.annual_loss;
            in annual_decay_in = aries_integrated_plant::fuel_inventory.annual_decay;
            in annual_feed_in = aries_integrated_plant::fuel_inventory.annual_recovery_kg;
            in external_shortfall_in = aries_integrated_plant::fuel_inventory.annual_external;
        }
        attribute noncapital_annual : Real = evaluate.noncapital_annual;
        attribute financed_capital : Real = evaluate.financed_capital;
        attribute idc : Real = evaluate.idc;
        attribute annual_capital : Real = evaluate.annual_capital;
        attribute annual_energy : Real = evaluate.annual_energy;
        attribute lifetime_energy : Real = evaluate.lifetime_energy;
        attribute pv_energy : Real = evaluate.pv_energy;
        attribute pv_operating : Real = evaluate.pv_operating;
        attribute pv_supply : Real = evaluate.pv_supply;
        attribute pv_replacement : Real = evaluate.pv_replacement;
        attribute pv_other_overhaul : Real = evaluate.pv_other_overhaul;
        attribute gross_terminal : Real = evaluate.gross_terminal;
        attribute salvage : Real = evaluate.salvage;
        attribute pv_terminal_gross : Real = evaluate.pv_terminal_gross;
        attribute pv_salvage : Real = evaluate.pv_salvage;
        attribute pv_terminal_net : Real = evaluate.pv_terminal_net;
        attribute other_overhaul_cost : Real = evaluate.other_overhaul_cost;
        attribute other_overhaul_occurs : Real = evaluate.other_overhaul_occurs;
        attribute pv_total_cost : Real = evaluate.pv_total_cost;
        attribute lcoe_sum : Real = evaluate.lcoe_sum;
        attribute capital_lcoe : Real = evaluate.capital_lcoe;
        attribute om_lcoe : Real = evaluate.om_lcoe;
        attribute tritium_lcoe : Real = evaluate.tritium_lcoe;
        attribute deuterium_lcoe : Real = evaluate.deuterium_lcoe;
        attribute consumables_lcoe : Real = evaluate.consumables_lcoe;
        attribute imports_lcoe : Real = evaluate.imports_lcoe;
        attribute supply_lcoe : Real = evaluate.supply_lcoe;
        attribute replacement_lcoe : Real = evaluate.replacement_lcoe;
        attribute other_overhaul_lcoe : Real = evaluate.other_overhaul_lcoe;
        attribute terminal_lcoe : Real = evaluate.terminal_lcoe;
        attribute salvage_lcoe : Real = evaluate.salvage_lcoe;
        attribute gross_makeup : Real = evaluate.gross_makeup;
        attribute new_feed : Real = evaluate.new_feed;
        attribute external_shortfall : Real = evaluate.external_shortfall;
        attribute curtailed_feed : Real = evaluate.curtailed_feed;
        attribute supply_supported : Real = evaluate.supply_supported;
        attribute breeding_supported : Real = evaluate.breeding_supported;
        attribute financial_defined : Real = evaluate.financial_defined;
        attribute currency_year : Real = evaluate.currency_year;
        attribute real_convention : Real = evaluate.real_convention;
    }
    part source_lifecycle_price {
        doc /* **Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22. */
        calc evaluate : 'LCOE DCF' {
            in total_capital_in = aries_integrated_plant::source_budget.inclusive_capital;
            in annual_om_in = aries_integrated_plant::source_lifecycle_accounts.noncapital_annual;
            in net_electric_mw = aries_integrated_plant::source_finance.net_power;
            in availability_in = aries_integrated_plant::cost_schedule.availability;
            in discount_rate_in = aries_integrated_plant::finance.discount_rate;
            in construction_years_in = aries_integrated_plant::source_finance.validated_years;
            in operational_years_in = aries_integrated_plant::cost_schedule.plant_years;
        }
        attribute lcoe : Real = evaluate.lcoe;
    }
}
