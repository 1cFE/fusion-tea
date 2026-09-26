package combinations_plasma_chain {
    doc /*
    C-2: the Stellaris parabolic plasma ('Plasma' at the Stellaris operating point with a supplied field) as the
    calculated fusion source of the ARIES deposition, coolant-branch, exchanger, pump, Brayton, electrical and fuel
    chain with the ARIES capacity screens. Existing definitions only; every binding is a new case binding
    (WI-093 design § 3). The plasma's own p_aux_required is published beside the ARIES 20 MW auxiliary heat and not
    wired into it (a disclosed mismatch, design § 6). No quantity is sized from demand.
    **Source**: work/active/WI-093_combination-assemblies/design.md **Reference**: goal design-space-combinations, map row P1
    **Basis**: [INHERITED: Stellaris] plasma values from models/designs/stellarator_09/stellarator_plant.sysml:895-1030 and
    B from the documented baseline; [INHERITED: ARIES] every downstream value from models/designs/aries_cs_integrated/plant.sysml;
    [ASSUMED] producer mode 1 (calculated power selected). **Last Updated**: 2026-09-26
    */
    private import ScalarValues::*;
    private import mfe_plasma::*;
    private import integrated_heat_electricity::*;
    private import dual_circuit_heat_accounting::*;
    private import ideal_gas_brayton_components::*;
    private import integrated_equipment_costs::*;
    private import mfe_fuel_cycle::*;
    private import mfe_viability::*;

    part plasma_chain {
        doc /* Root occurrence of the combinations_plasma_chain assembly (the generator renders output aliases by part path, so each assembly needs its own root part; the Stellaris nesting shape). */
        part plasma : 'Plasma' {
            doc /* The Stellaris design point. **Basis**: [INHERITED: Stellaris stellarator_plant.sysml:895-1030]; B [INHERITED: Stellaris baseline magnet__field_calc__B_axis 9.0 T], supplied because no magnet is assembled. The ports are declarative (WI-057) and unconnected here, as the generator accepts. */
            :>> R = 12.7;
            :>> a = 1.3;
            :>> kappa = 1.0;
            :>> f_shape = 1.0031567;
            :>> n_e = 3.17e20;
            :>> sigma_v = 0.0;
            :>> E_fus = 2.817e-12;
            :>> T_i0 = 14.63;
            :>> alpha_n = 0.33;
            :>> alpha_T = 1.19;
            :>> n_e0 = 5.06e20;
            :>> iota_23 = 0.92;
            :>> f_ren = 1.0;
            :>> f_alpha_fast = 0.95;
            :>> tau_ratio_ash = 8.0;
            :>> f_suppr_ash = 0.5;
            :>> Z_eff_core = 1.20;
            :>> f_W_core = 7.76e-6;
            :>> Ti_over_Te = 0.95;
            :>> B = 9.0;
        }
        part source {
            doc /* 'Fusion Source Selector' with the Stellaris calculated fusion power selected. **Basis**: reference [INHERITED: ARIES plant.sysml:17]; producer_mode 1 [ASSUMED: this assembly's choice; ARIES nominal binds 0 = the reference]. */
            attribute reference_fusion_mw : Real = 2436.0;
            attribute producer_mode : Real = 1.0;
            calc evaluate : 'Fusion Source Selector' {
                in calculated_power_in = plasma.p_fus;
                in reference_power_in = reference_fusion_mw;
                in mode_in = producer_mode;
            }
            attribute selected_power : Real = evaluate.selected_power;
            attribute selected_mode : Real = evaluate.selected_mode;
        }
        part deposition {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:27-84]. */
            attribute heat_mode : Real = 0.0;
            attribute neutron_multiplier : Real = 1.16;
            attribute radiation_fraction : Real = 0.25;
            attribute helium_fraction : Real = 0.38;
            attribute exchange_fraction : Real = 0.04;
            attribute auxiliary_heat : Real = 20.0;
            attribute he_pump : Real = combinations_plasma_chain::plasma_chain.he_pump.electric;
            attribute pbli_pump : Real = combinations_plasma_chain::plasma_chain.pbli_pump.electric;
            attribute divertor_pump : Real = combinations_plasma_chain::plasma_chain.divertor_pump.electric;
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
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:85-94]. */
            calc evaluate : 'Coolant Branch Heat' {
                in deposited_heat_in = deposition.he_deposition;
                in received_exchange_in = deposition.exchange;
                in exported_exchange_in = deposition.topology_zero;
                in recovered_friction_in = deposition.he_friction;
            }
            attribute delivered_heat : Real = evaluate.delivered_heat;
        }
        part pbli_coolant {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:95-104]. */
            calc evaluate : 'Coolant Branch Heat' {
                in deposited_heat_in = deposition.pbli_deposition;
                in received_exchange_in = deposition.topology_zero;
                in exported_exchange_in = deposition.exchange;
                in recovered_friction_in = deposition.pbli_friction;
            }
            attribute delivered_heat : Real = evaluate.delivered_heat;
        }
        part divertor_coolant {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:105-114]. */
            calc evaluate : 'Coolant Branch Heat' {
                in deposited_heat_in = deposition.divertor_deposition;
                in received_exchange_in = deposition.topology_zero;
                in exported_exchange_in = deposition.topology_zero;
                in recovered_friction_in = deposition.divertor_friction;
            }
            attribute delivered_heat : Real = evaluate.delivered_heat;
        }
        part fuel_inventory {
            doc /* Selected tritium stock as atoms for the fuel balance. **Basis**: [INHERITED: ARIES plant.sysml:1595-1609]. */
            attribute selected_tritium_kg : Real = 10.0;
            calc atoms : 'Selected Stock Atoms' {
                in stock_kg_in = selected_tritium_kg;
                in atom_mass_in = fuel.tritium_atom_kg;
            }
            attribute selected_tritium_atoms : Real = atoms.atoms;
        }
        part fuel {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:115-141]. */
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
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:142-151]. */
            attribute selected_flow : Real = 1400.0;
            attribute cp : Real = 5193.0;
            attribute gamma : Real = 1.6666666666666667;
            attribute return_pressure : Real = 4.285714285714286;
            attribute low_temperature : Real = 308.15;
            attribute turbine_efficiency : Real = 0.93;
            attribute recuperator_effectiveness : Real = 0.8;
        }
        part compressor_1 {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:152-168]. */
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
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:169-184]. */
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
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:185-201]. */
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
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:202-217]. */
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
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:218-234]. */
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
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:235-243]. */
            attribute loss_fraction : Real = 0.045;
            calc evaluate : 'Fractional Pressure Loss' {
                in pressure_in = compressor_3.pressure_out;
                in loss_fraction_in = loss_fraction;
            }
            attribute pressure_out : Real = evaluate.pressure_out;
        }
        part he_hx {
            doc /* **Basis**: [INHERITED: ARIES he_hx selected_area 50,000 m², U 1000 W/m²K]. */
            attribute selected_area : Real = 50000.0;
            attribute assumed_u : Real = 1000.0;
            calc evaluate : 'Exchanger Area Conductance' {
                in area_in = selected_area;
                in u_in = assumed_u;
            }
            attribute ua : Real = evaluate.ua;
            attribute area : Real = evaluate.area;
        }
        part pbli_hx {
            doc /* **Basis**: [INHERITED: ARIES pbli_hx]. */
            attribute selected_area : Real = 50000.0;
            attribute assumed_u : Real = 1000.0;
            calc evaluate : 'Exchanger Area Conductance' {
                in area_in = selected_area;
                in u_in = assumed_u;
            }
            attribute ua : Real = evaluate.ua;
            attribute area : Real = evaluate.area;
        }
        part divertor_hx {
            doc /* **Basis**: [INHERITED: ARIES divertor_hx]. */
            attribute selected_area : Real = 50000.0;
            attribute assumed_u : Real = 1000.0;
            calc evaluate : 'Exchanger Area Conductance' {
                in area_in = selected_area;
                in u_in = assumed_u;
            }
            attribute ua : Real = evaluate.ua;
            attribute area : Real = evaluate.area;
        }
        part he_pump {
            doc /* Selected helium pump against the chosen stage flow. **Basis**: [INHERITED: ARIES he_pump plant.sysml:750-799]. */
            attribute selected_flow_capacity : Real = 3261.0;
            attribute efficiency : Real = 0.8;
            attribute reference_flow : Real = 3261.0;
            attribute reference_power : Real = 156.0;
            attribute reference_efficiency : Real = 0.8;
            attribute pump_mode : Real = 0.0;
            attribute fixed_power : Real = 156.0;
            calc evaluate : 'Selected Flow Pump' {
                in flow_in = combinations_plasma_chain::plasma_chain.heat_exchangers.he_flow;
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
        part pbli_pump {
            doc /* **Basis**: [INHERITED: ARIES pbli_pump plant.sysml:846-896]. */
            attribute selected_flow_capacity : Real = 26860.0;
            attribute efficiency : Real = 0.8;
            attribute reference_flow : Real = 26860.0;
            attribute reference_power : Real = 0.01;
            attribute reference_efficiency : Real = 0.8;
            attribute pump_mode : Real = 0.0;
            attribute fixed_power : Real = 0.01;
            calc evaluate : 'Selected Flow Pump' {
                in flow_in = combinations_plasma_chain::plasma_chain.heat_exchangers.pbli_flow;
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
        part divertor_pump {
            doc /* **Basis**: [INHERITED: ARIES divertor_pump plant.sysml:942-992]. */
            attribute selected_flow_capacity : Real = 500.0;
            attribute efficiency : Real = 0.8;
            attribute reference_flow : Real = 500.0;
            attribute reference_power : Real = 10.0;
            attribute reference_efficiency : Real = 0.8;
            attribute pump_mode : Real = 0.0;
            attribute fixed_power : Real = 10.0;
            calc evaluate : 'Selected Flow Pump' {
                in flow_in = combinations_plasma_chain::plasma_chain.heat_exchangers.divertor_flow;
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
        part heat_exchangers {
            doc /* 'Network Heat Driven Closure' on the three ARIES branches fed by the Stellaris-sourced deposition. **Basis**: [INHERITED: ARIES plant.sysml:244-331]. */
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
            attribute he_hot_bound_margin : Real = evaluate.he_hot_bound_margin;
            attribute he_secondary_in : Real = evaluate.he_secondary_in;
            attribute he_secondary_out : Real = evaluate.he_secondary_out;
            attribute divertor_transferred : Real = evaluate.divertor_transferred;
            attribute divertor_unmet : Real = evaluate.divertor_unmet;
            attribute divertor_capability : Real = evaluate.divertor_capability;
            attribute divertor_hot : Real = evaluate.divertor_hot;
            attribute divertor_return : Real = evaluate.divertor_return;
            attribute divertor_state_defined : Real = evaluate.divertor_state_defined;
            attribute divertor_secondary_in : Real = evaluate.divertor_secondary_in;
            attribute divertor_secondary_out : Real = evaluate.divertor_secondary_out;
            attribute pbli_transferred : Real = evaluate.pbli_transferred;
            attribute pbli_unmet : Real = evaluate.pbli_unmet;
            attribute pbli_capability : Real = evaluate.pbli_capability;
            attribute pbli_hot : Real = evaluate.pbli_hot;
            attribute pbli_return : Real = evaluate.pbli_return;
            attribute pbli_state_defined : Real = evaluate.pbli_state_defined;
            attribute pbli_secondary_in : Real = evaluate.pbli_secondary_in;
            attribute pbli_secondary_out : Real = evaluate.pbli_secondary_out;
            attribute network_mode_used : Real = evaluate.network_mode_used;
            attribute pbli_split_used : Real = evaluate.pbli_split_used;
        }
        part turbine {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:333-347]. */
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
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:348-361]. */
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
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:362-376]. */
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
        part electrical {
            doc /* 'Plant Electrical Balance' as the ARIES generator_auxiliaries part; the plasma's own p_aux_required is published beside deposition.auxiliary_heat (20 MW) and not wired (design § 6). **Basis**: [INHERITED: ARIES plant.sysml:377-424]. */
            attribute heating_efficiency : Real = 0.5;
            attribute generator_efficiency : Real = 0.98;
            attribute motor_efficiency : Real = 0.95;
            attribute cryo : Real = 10.0;
            attribute fuel_base : Real = 5.0;
            attribute fuel_coefficient : Real = 1e-22;
            attribute control : Real = 5.0;
            attribute other_electric : Real = 5.0;
            attribute plasma_aux_required_published : Real = plasma.p_aux_required;
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
            attribute heating_electric : Real = evaluate.heating_electric;
            attribute fuel_electric : Real = evaluate.fuel_electric;
            attribute fuel_variable_electric : Real = evaluate.fuel_variable_electric;
            attribute auxiliary_electric : Real = evaluate.auxiliary_electric;
            attribute net_electric : Real = evaluate.net_electric;
            attribute primary_pump_electric : Real = evaluate.primary_pump_electric;
            attribute pump_loss : Real = evaluate.pump_loss;
            attribute cryo_electric : Real = evaluate.cryo_electric;
            attribute control_electric : Real = evaluate.control_electric;
            attribute other_electric_demand : Real = evaluate.other_electric_demand;
        }
        part he_capacity {
            doc /* **Basis**: [INHERITED: ARIES 1500 MW]. */
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
            doc /* **Basis**: [INHERITED: ARIES 1800 MW]. */
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
            doc /* **Basis**: [INHERITED: ARIES 800 MW]. */
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
            doc /* **Basis**: [INHERITED: ARIES 1600 MW]; the alternative-hardware case re-selects. */
            attribute selected_rating : Real = 1600.0;
            attribute assumed_supported : Boolean = true;
            attribute scenario_applicable : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = selected_rating;
                in demand_in = electrical.compressor_demand;
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
            doc /* **Basis**: [INHERITED: ARIES 3500 MW]. */
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
            doc /* The demand is an assembly expression reproducing the ledger's cycle_rejection formula (integrated_plant_ledger_impl.py:31); the ledger is not assembled here. **Basis**: [INHERITED: ARIES 2500 MW]. */
            attribute selected_rating : Real = 2500.0;
            attribute assumed_supported : Boolean = true;
            attribute scenario_applicable : Boolean = true;
            attribute demand_available : Boolean = true;
            attribute cycle_rejection : Real = -(intercooler_1.heat_into_fluid + intercooler_2.heat_into_fluid + precooler.heat_into_fluid);
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = selected_rating;
                in demand_in = cycle_rejection;
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
            doc /* **Basis**: [INHERITED: ARIES 1800 MW]. */
            attribute selected_rating : Real = 1800.0;
            attribute assumed_supported : Boolean = true;
            attribute scenario_applicable : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = selected_rating;
                in demand_in = electrical.gross_electric;
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
            doc /* Selected exhaust-processing rating against the calculated exhaust rate. **Basis**: [INHERITED: ARIES 3e22 atoms/s]. */
            attribute selected_rating : Real = 3e22;
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
        part checks {
            doc /* **Basis**: energy_tolerance [ASSUMED: 1e-6 MW, the ledger body's floor, as in combinations_loop_brayton]. */
            attribute energy_tolerance : Real = 1e-6;
            assert constraint heat_removal_ok : 'Heat Removal Adequate' {
                in unmet_in = heat_exchangers.unmet_heat;
                in tolerance_in = energy_tolerance;
            }
            assert constraint net_positive : 'Net Power Positive' {
                in net_electric = electrical.net_electric;
            }
        }
    }
}
