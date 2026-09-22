package aries_integrated_plant {
    private import ScalarValues::*;
    private import aries_cs_plasma_integration::*;
    private import integrated_heat_electricity::*;
    private import mfe_fuel_cycle::*;
    private import mfe_viability::*;
    private import dual_circuit_heat_accounting::*;
    private import ideal_gas_brayton_components::*;
    part source {
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: source owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
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
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: deposition owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute heat_mode : Real = 0.0;
        attribute neutron_multiplier : Real = 1.16;
        attribute radiation_fraction : Real = 0.25;
        attribute helium_fraction : Real = 0.38;
        attribute exchange_fraction : Real = 0.04;
        attribute auxiliary_heat : Real = 20.0;
        attribute he_pump : Real = 156.0;
        attribute pbli_pump : Real = 0.01;
        attribute divertor_pump : Real = 10.0;
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
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: he_coolant owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Coolant Branch Heat' {
            in deposited_heat_in = deposition.he_deposition;
            in received_exchange_in = deposition.exchange;
            in exported_exchange_in = deposition.topology_zero;
            in recovered_friction_in = deposition.he_friction;
        }
        attribute delivered_heat : Real = evaluate.delivered_heat;
    }
    part pbli_coolant {
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: pbli_coolant owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Coolant Branch Heat' {
            in deposited_heat_in = deposition.pbli_deposition;
            in received_exchange_in = deposition.topology_zero;
            in exported_exchange_in = deposition.exchange;
            in recovered_friction_in = deposition.pbli_friction;
        }
        attribute delivered_heat : Real = evaluate.delivered_heat;
    }
    part divertor_coolant {
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: divertor_coolant owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        calc evaluate : 'Coolant Branch Heat' {
            in deposited_heat_in = deposition.divertor_deposition;
            in received_exchange_in = deposition.topology_zero;
            in exported_exchange_in = deposition.topology_zero;
            in recovered_friction_in = deposition.divertor_friction;
        }
        attribute delivered_heat : Real = evaluate.delivered_heat;
    }
    part fuel {
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: fuel owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute reaction_energy_mev : Real = 17.58;
        attribute mev_joules : Real = 1.6021766339999998e-13;
        attribute tritium_atom_kg : Real = 5.008267663228036e-27;
        attribute pass_burn_fraction : Real = 0.05;
        attribute exhaust_recovery : Real = 0.99;
        attribute decay_constant_s : Real = 1.782785958230312e-09;
        attribute unused_tbr_placeholder : Real = 0.0;
        attribute assumed_extraction : Real = 1.0;
        attribute dormant_inventory_atoms : Real = 0.0;
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
            in I_total_in = dormant_inventory_atoms;
            in G_stock_in = dormant_stock_growth_atoms_s;
            in m_T_kg_in = tritium_atom_kg;
            in s_per_fpy_in = seconds_per_year;
        }
        attribute burn_rate : Real = evaluate.burn_rate;
        attribute inject_rate : Real = evaluate.inject_rate;
        attribute exhaust_rate : Real = evaluate.exhaust_rate;
        attribute loss_rate : Real = evaluate.loss_rate;
    }
    part cycle {
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: A3/S3 selected operating conditions, ideal helium. **Last Updated**: 2026-09-22. */
        attribute selected_flow : Real = 1400.0;
        attribute cp : Real = 5193.0;
        attribute gamma : Real = 1.6666666666666667;
        attribute return_pressure : Real = 4.285714285714286;
        attribute low_temperature : Real = 308.15;
        attribute turbine_efficiency : Real = 0.93;
        attribute recuperator_effectiveness : Real = 0.8;
    }
    part compressor_1 {
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: compressor_1 owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
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
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: intercooler_1 owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
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
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: compressor_2 owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
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
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: intercooler_2 owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
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
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: compressor_3 owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
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
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: pressure_loss owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute loss_fraction : Real = 0.045;
        calc evaluate : 'Fractional Pressure Loss' {
            in pressure_in = compressor_3.pressure_out;
            in loss_fraction_in = loss_fraction;
        }
        attribute pressure_out : Real = evaluate.pressure_out;
    }
    part heat_exchangers {
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: heat_exchangers owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
        attribute he_flow : Real = 3261.0;
        attribute he_cp : Real = 5193.0;
        attribute he_ua : Real = 50.0;
        attribute he_limit : Real = 729.15;
        attribute divertor_flow : Real = 500.0;
        attribute divertor_cp : Real = 5193.0;
        attribute divertor_ua : Real = 50.0;
        attribute divertor_limit : Real = 973.15;
        attribute pbli_flow : Real = 26860.0;
        attribute pbli_cp : Real = 190.0;
        attribute pbli_ua : Real = 50.0;
        attribute pbli_limit : Real = 1011.15;
        calc evaluate : 'Heat Driven Closure' {
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
    }
    part turbine {
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: turbine owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
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
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: recuperator owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
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
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: precooler owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
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
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: generator and auxiliary electrical responsibilities; S/A provenance retained. **Last Updated**: 2026-09-22. */
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
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: plant_ledger owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
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
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: he_capacity owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
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
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: pbli_capacity owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
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
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: divertor_capacity owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
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
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: compressor_capacity owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
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
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: turbine_capacity owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
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
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: rejection_capacity owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
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
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: generator_capacity owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
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
        doc /* **Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: fuel_capacity owner/interface; values retain register S1-S3/A1-A9 provenance. **Last Updated**: 2026-09-22. */
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
}
