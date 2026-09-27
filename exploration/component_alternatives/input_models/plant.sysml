package component_alternatives {
    doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. */
    private import ScalarValues::*;
    private import mfe_primary_loop::*;
    private import loop_return_control::*;
    private import integrated_heat_electricity::*;
    private import integrated_equipment_costs::*;
    private import ideal_gas_brayton_components::*;
    private import mfe_viability::*;
    private import integrated_equipment_parts::*;
    private import costed_component::*;
    private import mfe_account_costs::*;
    private import mfe_matched_steam_cycle::*;
    private import cooling_equipment_selected_pumps::*;
    private import component_alternatives_thermal::*;
    part plant {
        doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. Selected steam offer versus tested Brayton offers; separate ledgers, common source. */
        part blanket_source {
            doc /* Supplied blanket heat delivered to the loop. **Basis**: [INHERITED: Stellaris baseline blanket__source_heat__q_source, MW]; chosen here, no blanket model assembled. */
            attribute q_source : Real = 2500.0;
        }
        part primary_loop {
            doc /* 'Primary Coolant Loop' at the Stellaris circuit facts. Flow is calculated from duty and the chosen temperature rise (the audited operating-point direction, disclosed, unchanged). **Basis**: [INHERITED: Stellaris stellarator_plant.sysml:1226-1321]. */
            attribute loop_T_in : Real = 573.15;
            attribute loop_dT_blanket : Real = 200.0;
            attribute loop_cp : Real = 5193.0;
            attribute loop_gamma : Real = 1.6666666666666667;
            attribute loop_p : Real = 8000000.0;
            attribute n_loops : Real = 14.0;
            attribute mdot_loop_ref : Real = 225.07777777777778;
            attribute mdot_loop_rated : Real = 225.07777777777778;
            attribute dp_loop_ref : Real = 329187.1856931558;
            attribute f_loss : Real = 1.1;
            attribute eta_is : Real = 0.772796639536644;
            attribute eta_drive : Real = 1.0;
            attribute loop_live : Real = 1.0;
            attribute p_pump_direct : Real = 0.0;
            attribute eta_p_direct : Real = 0.0;
            calc evaluate : 'Primary Coolant Loop' {
                in q_source_in = blanket_source.q_source;
                in T_in_in = loop_T_in;
                in dT_blanket_in = loop_dT_blanket;
                in cp_in = loop_cp;
                in gamma_in = loop_gamma;
                in p_loop_in = loop_p;
                in n_loops_in = n_loops;
                in mdot_loop_ref_in = mdot_loop_ref;
                in mdot_loop_rated_in = mdot_loop_rated;
                in dp_loop_ref_in = dp_loop_ref;
                in f_loss_in = f_loss;
                in eta_is_in = eta_is;
                in eta_drive_in = eta_drive;
                in loop_live_in = loop_live;
                in p_pump_direct_in = p_pump_direct;
                in eta_p_direct_in = eta_p_direct;
            }
            attribute w_fluid : Real = evaluate.w_fluid;
            attribute p_loop_margin : Real = evaluate.p_loop_margin;
            attribute mdot : Real = evaluate.mdot;
            attribute T_out : Real = evaluate.T_out;
            attribute mdot_loop : Real = evaluate.mdot_loop;
            attribute T_comp_in : Real = evaluate.T_comp_in;
            attribute dp_loop : Real = evaluate.dp_loop;
            attribute p_elec : Real = evaluate.p_elec;
            attribute q_ihx : Real = evaluate.q_ihx;
            attribute capacity_margin : Real = evaluate.capacity_margin;
            attribute p_pump_total : Real = evaluate.p_pump_total;
            attribute q_recovered_total : Real = evaluate.q_recovered_total;
        }
        part cycle {
            doc /* ARIES cycle operating choices; selected_flow re-selected for the lower-temperature source. **Basis**: [INHERITED: ARIES plant.sysml:142-151] except selected_flow [ASSUMED: 2500 kg/s, inside the round-1 screen's feasible range]. */
            attribute selected_flow : Real = 2000.0;
            attribute cp : Real = 5193.0;
            attribute gamma : Real = 1.6666666666666667;
            attribute return_pressure : Real = 4.285714285714286;
            attribute low_temperature : Real = 308.15;
            attribute turbine_efficiency : Real = 0.93;
            attribute recuperator_effectiveness : Real = recuperator_hardware.effectiveness;
        }
        part compressor_1 {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:152-168]. */
            attribute selected_ratio : Real = 1.5;
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
            attribute selected_ratio : Real = 1.5;
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
            attribute selected_ratio : Real = 1.5;
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
        part he_hx : 'Selected Equipment' {
            doc /* Installed exchanger conductance from the selected area and assumed U, purchased through the linear law from the ARIES reference. **Basis**: [INHERITED: ARIES plant.sysml:723-749, E2/E4]. */
            :>> cas_code = "22.2";
            attribute reference_quantity : Real = 50000.0;
            attribute reference_cost : Real = 58325700.00000001;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Selected Inventory Purchase' {
                in quantity_in = selected_area;
                in reference_quantity_in = reference_quantity;
                in reference_cost_in = reference_cost;
                in price_factor_in = price_factor;
                in mode_in = cost_accounts.estimate_mode;
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
        part idle_branches {
            doc /* Representation quirk: the closure reads three branches; the PbLi and divertor stages are idle here. Positive dummy flow, cp and limit satisfy its guards; UA 0 and available 0 make each stage transfer nothing. **Basis**: [ASSUMED] dummies; they select nothing. */
            attribute dummy_flow : Real = 1.0;
            attribute cp : Real = 1.0;
            attribute limit : Real = 308.15;
            attribute ua : Real = 0.0;
            attribute available : Real = 0.0;
        }
        part heat_exchangers {
            doc /* 'Network Heat Driven Closure' with the Stellaris loop as the helium stage: available = primary_loop.q_ihx, flow = primary_loop.mdot, hot limit = primary_loop.T_out. Series mode; the split is unused in mode 0 but must lie in (0,1). **Basis**: [INHERITED: ARIES binding pattern plant.sysml:244-331]. */
            attribute he_cp : Real = 5193.0;
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
                in he_available_in = primary_loop.q_ihx;
                in pbli_available_in = idle_branches.available;
                in divertor_available_in = idle_branches.available;
                in he_flow_in = primary_loop.mdot;
                in he_cp_in = he_cp;
                in he_ua_in = he_hx.ua;
                in he_limit_in = primary_loop.T_out;
                in divertor_flow_in = idle_branches.dummy_flow;
                in divertor_cp_in = idle_branches.cp;
                in divertor_ua_in = idle_branches.ua;
                in divertor_limit_in = idle_branches.limit;
                in pbli_flow_in = idle_branches.dummy_flow;
                in pbli_cp_in = idle_branches.cp;
                in pbli_ua_in = idle_branches.ua;
                in pbli_limit_in = idle_branches.limit;
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
            attribute pbli_transferred : Real = evaluate.pbli_transferred;
            attribute divertor_transferred : Real = evaluate.divertor_transferred;
            attribute pbli_state_defined : Real = evaluate.pbli_state_defined;
            attribute divertor_state_defined : Real = evaluate.divertor_state_defined;
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
            doc /* 'Plant Electrical Balance' with upstream and whole-plant loads excluded; the auxiliary demands are the ARIES A-register values on a Stellaris loop (disclosed); the exhaust-driven fuel term is held at 0 as in C-1 so the C-1 receipts replay bit-exactly; the assembled fuel chain's exhaust rate feeds only the fuel cost, and the S2 case overrides fuel_exhaust with that stored rate (contract v2 section 3). **Basis**: [INHERITED: ARIES plant.sysml:377-424]. */
            attribute zero_load : Real = 0.0;
            attribute auxiliary_heat : Real = 0.0;
            attribute heating_efficiency : Real = 0.5;
            attribute generator_efficiency : Real = 0.98;
            attribute motor_efficiency : Real = 0.95;
            attribute cryo : Real = 0.0;
            attribute fuel_base : Real = 0.0;
            attribute fuel_coefficient : Real = 1e-22;
            attribute fuel_exhaust : Real = 0.0;
            attribute control : Real = 0.0;
            attribute other_electric : Real = 0.0;
            calc evaluate : 'Plant Electrical Balance' {
                in turbine_work_in = turbine.shaft_produced;
                in compressor_1_in = compressor_1.shaft_demand;
                in compressor_2_in = compressor_2.shaft_demand;
                in compressor_3_in = compressor_3.shaft_demand;
                in auxiliary_heat_in = auxiliary_heat;
                in pump_electric_in = zero_load;
                in pump_recovered_in = zero_load;
                in heating_efficiency_in = heating_efficiency;
                in generator_efficiency_in = generator_efficiency;
                in motor_efficiency_in = motor_efficiency;
                in cryo_in = cryo;
                in fuel_base_in = fuel_base;
                in fuel_coefficient_in = fuel_coefficient;
                in fuel_exhaust_in = fuel_exhaust;
                in control_in = control;
                in other_electric_in = other_electric;
            }
            attribute compressor_demand : Real = evaluate.compressor_demand;
            attribute net_shaft : Real = evaluate.net_shaft;
            attribute gross_electric : Real = evaluate.gross_electric;
            attribute shaft_import : Real = evaluate.shaft_import;
            attribute auxiliary_electric : Real = evaluate.auxiliary_electric;
            attribute net_electric : Real = evaluate.net_electric;
            attribute primary_pump_electric : Real = evaluate.primary_pump_electric;
            attribute pump_loss : Real = evaluate.pump_loss;
        }
        part compressor_capacity {
            doc /* Installed compressor rating against the calculated shaft demand. **Basis**: [INHERITED: ARIES 1600 MW]; cases re-select. */
            attribute selected_rating : Real = 3200.0;
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
            attribute selected_rating : Real = 7000.0;
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
        part generator_capacity {
            doc /* **Basis**: [INHERITED: ARIES 1800 MW]. */
            attribute selected_rating : Real = 3600.0;
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
        part he_capacity {
            doc /* Helium duty package rating against the loop's delivered heat. **Basis**: [INHERITED: ARIES 1500 MW]; cases re-select. */
            attribute selected_rating : Real = 3500.0;
            attribute assumed_supported : Boolean = true;
            attribute scenario_applicable : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = selected_rating;
                in demand_in = primary_loop.q_ihx;
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
        part return_control {
            doc /* 'Primary Bypass Control' on the helium stage: the fraction of loop flow bypassing the exchanger so that the exchanger, at the loop's delivery temperature and reduced flow, transfers the whole delivered duty and the mixed return equals the loop's T_comp_in (WI-095). max_bypass [ASSUMED: 1.0, no design limit declared; the owner's to set]; tolerance [ASSUMED: 1e-6 K, the root-solve closure, not a physical allowance]. **Basis**: work/active/WI-095_loop-return-control/design.md section 4. */
            attribute max_bypass : Real = 0.5;
            attribute tolerance : Real = 1e-6;
            calc evaluate : 'Primary Bypass Control' {
                in ua_in = he_hx.ua;
                in primary_flow_in = primary_loop.mdot;
                in primary_cp_in = heat_exchangers.he_cp;
                in secondary_flow_in = cycle.selected_flow;
                in secondary_cp_in = cycle.cp;
                in primary_limit_in = primary_loop.T_out;
                in secondary_inlet_in = heat_exchangers.he_secondary_in;
                in duty_in = primary_loop.q_ihx;
                in required_return_in = primary_loop.T_comp_in;
                in max_bypass_in = max_bypass;
                in tolerance_in = tolerance;
            }
            attribute bypass_fraction : Real = evaluate.bypass_fraction;
            attribute feasible : Real = evaluate.feasible;
            attribute capability_open : Real = evaluate.capability_open;
            attribute capability_at_solution : Real = evaluate.capability_at_solution;
            attribute exchanger_primary_flow : Real = evaluate.exchanger_primary_flow;
            attribute exchanger_return : Real = evaluate.exchanger_return;
            attribute mixed_return : Real = evaluate.mixed_return;
            attribute return_residual : Real = evaluate.return_residual;
            attribute return_residual_magnitude : Real = evaluate.return_residual_magnitude;
        }
        part cost_accounts {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:710-714]. */
            attribute estimate_mode : Real = 0.0;
            attribute one_module : Real = 1.0;
        }
        part compressor_equipment : 'Selected Equipment' {
            doc /* Purchase of the selected compressor rating through the linear law from the ARIES reference. **Basis**: [INHERITED: ARIES plant.sysml:1050-1068, WI-090 E4]. */
            :>> cas_code = "23";
            attribute reference_quantity : Real = 1600.0;
            attribute reference_cost : Real = 78639500.0;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Selected Inventory Purchase' {
                in quantity_in = compressor_capacity.selected_rating;
                in reference_quantity_in = reference_quantity;
                in reference_cost_in = reference_cost;
                in price_factor_in = price_factor;
                in mode_in = cost_accounts.estimate_mode;
            }
            attribute inventory_quantity : Real = purchase.purchased_quantity;
            attribute quantity_ratio : Real = purchase.quantity_ratio;
            attribute estimated_cost : Real = purchase.capital;
            attribute cost_extrapolated : Real = purchase.extrapolated;
            :>> capital_cost = purchase.capital;
        }
        part turbine_equipment : 'Selected Equipment' {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:1069-1087]. */
            :>> cas_code = "23";
            attribute reference_quantity : Real = 3500.0;
            attribute reference_cost : Real = 125823200.0;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Selected Inventory Purchase' {
                in quantity_in = turbine_capacity.selected_rating;
                in reference_quantity_in = reference_quantity;
                in reference_cost_in = reference_cost;
                in price_factor_in = price_factor;
                in mode_in = cost_accounts.estimate_mode;
            }
            attribute inventory_quantity : Real = purchase.purchased_quantity;
            attribute quantity_ratio : Real = purchase.quantity_ratio;
            attribute estimated_cost : Real = purchase.capital;
            attribute cost_extrapolated : Real = purchase.extrapolated;
            :>> capital_cost = purchase.capital;
        }
        part generator_equipment : 'Selected Equipment' {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:1088-1106]. */
            :>> cas_code = "23";
            attribute reference_quantity : Real = 1800.0;
            attribute reference_cost : Real = 47183699.99999999;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Selected Inventory Purchase' {
                in quantity_in = generator_capacity.selected_rating;
                in reference_quantity_in = reference_quantity;
                in reference_cost_in = reference_cost;
                in price_factor_in = price_factor;
                in mode_in = cost_accounts.estimate_mode;
            }
            attribute inventory_quantity : Real = purchase.purchased_quantity;
            attribute quantity_ratio : Real = purchase.quantity_ratio;
            attribute estimated_cost : Real = purchase.capital;
            attribute cost_extrapolated : Real = purchase.extrapolated;
            :>> capital_cost = purchase.capital;
        }
        part heat_rejection_equipment : 'Selected Equipment' {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:1107-1125]. */
            :>> cas_code = "27";
            attribute reference_quantity : Real = 2500.0;
            attribute reference_cost : Real = 56086000.0;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Selected Inventory Purchase' {
                in quantity_in = rejection_capacity.selected_rating;
                in reference_quantity_in = reference_quantity;
                in reference_cost_in = reference_cost;
                in price_factor_in = price_factor;
                in mode_in = cost_accounts.estimate_mode;
            }
            attribute inventory_quantity : Real = purchase.purchased_quantity;
            attribute quantity_ratio : Real = purchase.quantity_ratio;
            attribute estimated_cost : Real = purchase.capital;
            attribute cost_extrapolated : Real = purchase.extrapolated;
            :>> capital_cost = purchase.capital;
        }
        part he_duty_equipment : 'Selected Equipment' {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:801-819]. */
            :>> cas_code = "22.2";
            attribute reference_quantity : Real = 1500.0;
            attribute reference_cost : Real = 32403166.66666667;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Selected Inventory Purchase' {
                in quantity_in = he_capacity.selected_rating;
                in reference_quantity_in = reference_quantity;
                in reference_cost_in = reference_cost;
                in price_factor_in = price_factor;
                in mode_in = cost_accounts.estimate_mode;
            }
            attribute inventory_quantity : Real = purchase.purchased_quantity;
            attribute quantity_ratio : Real = purchase.quantity_ratio;
            attribute estimated_cost : Real = purchase.capital;
            attribute cost_extrapolated : Real = purchase.extrapolated;
            :>> capital_cost = purchase.capital;
        }
        part conversion_services : 'Selected Equipment' {
            doc /* Fixed recuperator/services share of the ARIES conversion budget; not scaled. **Basis**: [INHERITED: ARIES plant.sysml:1145-1162]. */
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
        part recuperator_hardware {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. recuperator_hardware owns its selected inputs and exposed calculation outputs. */
            attribute ua : Real = 60;
            calc evaluate : 'Recuperator Installed Capability' {
                in ua_in = ua;
                in flow_in = cycle.selected_flow;
                in cp_in = cycle.cp;
            }
            attribute capacity_rate : Real = evaluate.capacity_rate;
            attribute effectiveness : Real = evaluate.effectiveness;
        }
        part steam_transport {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_transport owns its selected inputs and exposed calculation outputs. */
            attribute salt_pumps_per_circuit : Real = 4;
            attribute selected_helium_design_shaft_MW : Real = 6.259319085874574;
            attribute selected_helium_design_suction_Pa : Real = 7670812.814306844;
            attribute selected_salt_design_flow_kg_s : Real = 250;
            attribute selected_salt_design_head_m : Real = 40;
            attribute salt_design_eta_p : Real = 0.75;
            attribute salt_design_eta_motor : Real = 0.95;
            attribute helium_purchased_mass_kg : Real = 100000;
            attribute salt_purchased_mass_kg : Real = 1608750.9823889225;
            attribute enabled : Boolean = true;
            attribute n_mod : Real = 1;
            attribute n_loops : Real = 14;
            attribute layout_multiplier : Real = 1;
            attribute tube_wall : Real = 0.0015;
            attribute shell_wall : Real = 0.2;
            attribute accessory_mass : Real = 10000;
            attribute secondary_head : Real = 40;
            attribute eta_p : Real = 0.75;
            attribute eta_motor : Real = 0.95;
            attribute machine_life : Real = 10;
            attribute bundle_life : Real = 15;
            attribute years : Real = 30;
            attribute discount : Real = 0.05;
            attribute makeup_fraction : Real = 0.001;
            attribute inventory_reserve : Real = 0.1;
            attribute removal_multiplier : Real = 1;
            attribute saltprice_source_choice : Real = 0;
            attribute costscale : Real = 1;
            attribute stainless_fabrication_usd2017_per_kg : Real = 310 ;
            attribute sourcefitargument_C : Real = 480;
            calc evaluate : 'Cooling Equipment With Selected Salt Pump Count' {
                in salt_pumps_per_circuit_in = salt_pumps_per_circuit;
                in helium_design_shaft_MW_in = selected_helium_design_shaft_MW;
                in helium_design_suction_Pa_in = selected_helium_design_suction_Pa;
                in salt_design_flow_kg_s_in = selected_salt_design_flow_kg_s;
                in salt_design_head_m_in = selected_salt_design_head_m;
                in salt_design_eta_p_in = salt_design_eta_p;
                in salt_design_eta_motor_in = salt_design_eta_motor;
                in helium_purchased_mass_kg_in = helium_purchased_mass_kg;
                in salt_purchased_mass_kg_in = salt_purchased_mass_kg;
                in enabled_in = enabled;
                in n_mod_in = n_mod;
                in n_loops_in = n_loops;
                in mdot_loop_in = primary_loop.mdot_loop;
                in dp_loop_in = primary_loop.dp_loop;
                in helium_suction_K_in = primary_loop.T_comp_in;
                in helium_discharge_Pa_in = primary_loop.loop_p;
                in helium_hot_K_in = primary_loop.T_out;
                in helium_cp_in = primary_loop.loop_cp;
                in helium_gamma_in = primary_loop.loop_gamma;
                in primary_shaft_MW_in = primary_loop.w_fluid;
                in primary_electric_MW_in = primary_loop.p_elec;
                in q_ihx_MW_in = primary_loop.q_ihx;
                in layout_multiplier_in = layout_multiplier;
                in tube_wall_in = tube_wall;
                in shell_wall_in = shell_wall;
                in accessory_mass_in = accessory_mass;
                in secondary_head_in = secondary_head;
                in eta_p_in = eta_p;
                in eta_motor_in = eta_motor;
                in machine_life_in = machine_life;
                in bundle_life_in = bundle_life;
                in years_in = years;
                in discount_in = discount;
                in makeup_fraction_in = makeup_fraction;
                in inventory_reserve_in = inventory_reserve;
                in removal_multiplier_in = removal_multiplier;
                in saltprice_source_choice_in = saltprice_source_choice;
                in costscale_in = costscale;
                in stainless_fabrication_usd2017_per_kg_in = stainless_fabrication_usd2017_per_kg;
                in sourcefitargument_C_in = sourcefitargument_C;
            }
            attribute primary_circulators_cost : Real = evaluate.primary_circulators_cost;
            attribute primary_piping_cost : Real = evaluate.primary_piping_cost;
            attribute exchangers_cost : Real = evaluate.exchangers_cost;
            attribute secondary_pumps_cost : Real = evaluate.secondary_pumps_cost;
            attribute secondary_piping_cost : Real = evaluate.secondary_piping_cost;
            attribute inventory_cost : Real = evaluate.inventory_cost;
            attribute spares_cost : Real = evaluate.spares_cost;
            attribute purchased_total : Real = evaluate.purchased_total;
            attribute installation_total : Real = evaluate.installation_total;
            attribute installed_total : Real = evaluate.installed_total;
            attribute delivered_total : Real = evaluate.delivered_total;
            attribute primary_vendor : Real = evaluate.primary_vendor;
            attribute primary_installation : Real = evaluate.primary_installation;
            attribute primary_design : Real = evaluate.primary_design;
            attribute primary_spare : Real = evaluate.primary_spare;
            attribute secondary_vendor : Real = evaluate.secondary_vendor;
            attribute secondary_installation : Real = evaluate.secondary_installation;
            attribute secondary_spare : Real = evaluate.secondary_spare;
            attribute hx_purchase : Real = evaluate.hx_purchase;
            attribute hx_installation : Real = evaluate.hx_installation;
            attribute primary_pipe_purchase : Real = evaluate.primary_pipe_purchase;
            attribute primary_pipe_installation : Real = evaluate.primary_pipe_installation;
            attribute secondary_pipe_purchase : Real = evaluate.secondary_pipe_purchase;
            attribute secondary_pipe_installation : Real = evaluate.secondary_pipe_installation;
            attribute helium_inventory_cost : Real = evaluate.helium_inventory_cost;
            attribute salt_inventory_cost : Real = evaluate.salt_inventory_cost;
            attribute machine_event_purchase : Real = evaluate.machine_event_purchase;
            attribute machine_event_installation : Real = evaluate.machine_event_installation;
            attribute machine_event_removal : Real = evaluate.machine_event_removal;
            attribute bundle_event_purchase : Real = evaluate.bundle_event_purchase;
            attribute bundle_event_installation : Real = evaluate.bundle_event_installation;
            attribute bundle_event_removal : Real = evaluate.bundle_event_removal;
            attribute replacement_annual : Real = evaluate.replacement_annual;
            attribute consumables_annual : Real = evaluate.consumables_annual;
            attribute helium_makeup_annual : Real = evaluate.helium_makeup_annual;
            attribute salt_makeup_annual : Real = evaluate.salt_makeup_annual;
            attribute salt_electric_MW : Real = evaluate.salt_electric_MW;
            attribute salt_shaft_MW : Real = evaluate.salt_shaft_MW;
            attribute conversion_heat_MW : Real = evaluate.conversion_heat_MW;
            attribute circulator_shaft_MW : Real = evaluate.circulator_shaft_MW;
            attribute circulator_electric_MW : Real = evaluate.circulator_electric_MW;
            attribute ihx_duty_MW : Real = evaluate.ihx_duty_MW;
            attribute tube_mass : Real = evaluate.tube_mass;
            attribute shell_mass : Real = evaluate.shell_mass;
            attribute heads_mass : Real = evaluate.heads_mass;
            attribute sheets_mass : Real = evaluate.sheets_mass;
            attribute hx_mass : Real = evaluate.hx_mass;
            attribute bundle_mass : Real = evaluate.bundle_mass;
            attribute primary_pipe_mass : Real = evaluate.primary_pipe_mass;
            attribute secondary_pipe_mass : Real = evaluate.secondary_pipe_mass;
            attribute helium_inventory_mass : Real = evaluate.helium_inventory_mass;
            attribute salt_inventory_mass : Real = evaluate.salt_inventory_mass;
            attribute primary_pipe_volume : Real = evaluate.primary_pipe_volume;
            attribute helium_hx_volume : Real = evaluate.helium_hx_volume;
            attribute helium_inventory_volume : Real = evaluate.helium_inventory_volume;
            attribute helium_standard_volume : Real = evaluate.helium_standard_volume;
            attribute salt_pipe_volume : Real = evaluate.salt_pipe_volume;
            attribute salt_hx_volume : Real = evaluate.salt_hx_volume;
            attribute salt_inventory_volume : Real = evaluate.salt_inventory_volume;
            attribute ihx_installed_area : Real = evaluate.ihx_installed_area;
            attribute ihx_required_area : Real = evaluate.ihx_required_area;
            attribute circulator_count : Real = evaluate.circulator_count;
            attribute salt_pump_count : Real = evaluate.salt_pump_count;
            attribute source_volume_ratio : Real = evaluate.source_volume_ratio;
            attribute salt_expansion_ratio : Real = evaluate.salt_expansion_ratio;
            attribute salt_Re_hot : Real = evaluate.salt_Re_hot;
            attribute salt_Re_cold : Real = evaluate.salt_Re_cold;
            attribute pump_size_factor : Real = evaluate.pump_size_factor;
            attribute pump_shaft_hp : Real = evaluate.pump_shaft_hp;
            attribute motor_electric_hp : Real = evaluate.motor_electric_hp;
            attribute machine_events : Real = evaluate.machine_events;
            attribute bundle_events : Real = evaluate.bundle_events;
            attribute salt_price_raw : Real = evaluate.salt_price_raw;
            attribute salt_price_year : Real = evaluate.salt_price_year;
            attribute salt_unit_price : Real = evaluate.salt_unit_price;
            attribute helium_price_raw : Real = evaluate.helium_price_raw;
            attribute helium_price_year : Real = evaluate.helium_price_year;
            attribute circulator_flow : Real = evaluate.circulator_flow;
            attribute circulator_volume : Real = evaluate.circulator_volume;
            attribute circulator_suction_Pa : Real = evaluate.circulator_suction_Pa;
            attribute ihx_hot_approach : Real = evaluate.ihx_hot_approach;
            attribute ihx_cold_approach : Real = evaluate.ihx_cold_approach;
            attribute ihx_lmtd : Real = evaluate.ihx_lmtd;
            attribute salt_flow : Real = evaluate.salt_flow;
            attribute salt_velocity_hot : Real = evaluate.salt_velocity_hot;
            attribute salt_velocity_cold : Real = evaluate.salt_velocity_cold;
            attribute salt_straight_loss : Real = evaluate.salt_straight_loss;
            attribute salt_head_remaining : Real = evaluate.salt_head_remaining;
            attribute salt_return_C : Real = evaluate.salt_return_C;
            attribute cycle_temperature_gap : Real = evaluate.cycle_temperature_gap;
            attribute pump_flow_gpm : Real = evaluate.pump_flow_gpm;
            attribute pump_head_ft : Real = evaluate.pump_head_ft;
            attribute ihx_capacity_ok : Boolean = evaluate.ihx_capacity_ok;
            attribute ihx_capacity_margin_m2 : Real = evaluate.ihx_capacity_margin_m2;
            attribute ihx_capacity_defined : Real = evaluate.ihx_capacity_defined;
            attribute pump_size_ok : Boolean = evaluate.pump_size_ok;
            attribute pump_type_ok : Boolean = evaluate.pump_type_ok;
            attribute motor_base_ok : Boolean = evaluate.motor_base_ok;
            attribute motor_factor_ok : Boolean = evaluate.motor_factor_ok;
            attribute salt_head_ok : Boolean = evaluate.salt_head_ok;
            attribute salt_flow_regime_ok : Boolean = evaluate.salt_flow_regime_ok;
            attribute cycle_interface_ok : Boolean = evaluate.cycle_interface_ok;
            attribute salt_bulk_scale_ok : Boolean = evaluate.salt_bulk_scale_ok;
            attribute inventory_source_volume_ok : Boolean = evaluate.inventory_source_volume_ok;
            attribute pressure_qualified : Boolean = evaluate.pressure_qualified;
            attribute helium_price_transfer_validated : Boolean = evaluate.helium_price_transfer_validated;
            attribute salt_pump_transfer_validated : Boolean = evaluate.salt_pump_transfer_validated;
            attribute inventory_complete : Boolean = evaluate.inventory_complete;
            attribute salt_pump_flow : Real = evaluate.salt_pump_flow;
            attribute salt_pump_shaft_MW : Real = evaluate.salt_pump_shaft_MW;
            attribute ihx_count : Real = evaluate.ihx_count;
            attribute hx_shell_bore : Real = evaluate.hx_shell_bore;
            attribute hx_shell_wall : Real = evaluate.hx_shell_wall;
            attribute hx_shell_length : Real = evaluate.hx_shell_length;
            attribute hx_tube_length : Real = evaluate.hx_tube_length;
            attribute helium_design_shaft_MW : Real = evaluate.helium_design_shaft_MW;
            attribute helium_design_suction_Pa : Real = evaluate.helium_design_suction_Pa;
            attribute salt_design_flow_kg_s : Real = evaluate.salt_design_flow_kg_s;
            attribute salt_design_head_m : Real = evaluate.salt_design_head_m;
            attribute salt_design_shaft_MW : Real = evaluate.salt_design_shaft_MW;
            attribute salt_design_electric_MW : Real = evaluate.salt_design_electric_MW;
            attribute design_pump_flow_gpm : Real = evaluate.design_pump_flow_gpm;
            attribute design_pump_head_ft : Real = evaluate.design_pump_head_ft;
            attribute design_pump_size_factor : Real = evaluate.design_pump_size_factor;
            attribute design_pump_shaft_hp : Real = evaluate.design_pump_shaft_hp;
            attribute design_motor_electric_hp : Real = evaluate.design_motor_electric_hp;
            attribute helium_required_fill_mass_kg : Real = evaluate.helium_required_fill_mass_kg;
            attribute salt_required_fill_mass_kg : Real = evaluate.salt_required_fill_mass_kg;
            attribute helium_inventory_target_mass_kg : Real = evaluate.helium_inventory_target_mass_kg;
            attribute salt_inventory_target_mass_kg : Real = evaluate.salt_inventory_target_mass_kg;
            attribute helium_represented_fill_margin_kg : Real = evaluate.helium_represented_fill_margin_kg;
            attribute salt_represented_fill_margin_kg : Real = evaluate.salt_represented_fill_margin_kg;
            attribute design_pump_size_ok : Boolean = evaluate.design_pump_size_ok;
            attribute design_pump_type_ok : Boolean = evaluate.design_pump_type_ok;
            attribute design_motor_base_ok : Boolean = evaluate.design_motor_base_ok;
            attribute design_motor_factor_ok : Boolean = evaluate.design_motor_factor_ok;
            attribute machine_off_design_performance_qualified : Boolean = evaluate.machine_off_design_performance_qualified;
            attribute represented_fill_ok : Boolean = evaluate.represented_fill_ok;
            attribute represented_fill_defined : Real = evaluate.represented_fill_defined;
            attribute salt_machine_event_purchase : Real = evaluate.salt_machine_event_purchase;
            attribute salt_machine_event_installation : Real = evaluate.salt_machine_event_installation;
            attribute salt_machine_event_removal : Real = evaluate.salt_machine_event_removal;
            attribute salt_pump_electric_MW : Real = evaluate.salt_pump_electric_MW;
            attribute total_salt_flow_kg_s : Real = evaluate.total_salt_flow_kg_s;
            attribute installed_total_UA_MW_K : Real = evaluate.installed_total_UA_MW_K;
            calc ihx_capacity_ok_required_screen : 'Offered Capacity Screen' {
                in rating_in = 1.0;
                in demand_in = 0.0;
                in applicable_in = true;
                in conditions_supported_in = steam_transport.ihx_capacity_ok;
                in demand_available_in = true;
            }
            attribute ihx_capacity_ok_required_defined : Real = ihx_capacity_ok_required_screen.evaluation_defined;
            attribute ihx_capacity_ok_required_margin : Real = ihx_capacity_ok_required_screen.margin;
            assert constraint ihx_capacity_ok_required : 'Offered Equipment Capacity' {
                in defined_in = ihx_capacity_ok_required_defined;
                in margin_in = ihx_capacity_ok_required_margin;
            }
            calc design_pump_size_ok_required_screen : 'Offered Capacity Screen' {
                in rating_in = 1.0;
                in demand_in = 0.0;
                in applicable_in = true;
                in conditions_supported_in = steam_transport.design_pump_size_ok;
                in demand_available_in = true;
            }
            attribute design_pump_size_ok_required_defined : Real = design_pump_size_ok_required_screen.evaluation_defined;
            attribute design_pump_size_ok_required_margin : Real = design_pump_size_ok_required_screen.margin;
            assert constraint design_pump_size_ok_required : 'Offered Equipment Capacity' {
                in defined_in = design_pump_size_ok_required_defined;
                in margin_in = design_pump_size_ok_required_margin;
            }
            calc design_pump_type_ok_required_screen : 'Offered Capacity Screen' {
                in rating_in = 1.0;
                in demand_in = 0.0;
                in applicable_in = true;
                in conditions_supported_in = steam_transport.design_pump_type_ok;
                in demand_available_in = true;
            }
            attribute design_pump_type_ok_required_defined : Real = design_pump_type_ok_required_screen.evaluation_defined;
            attribute design_pump_type_ok_required_margin : Real = design_pump_type_ok_required_screen.margin;
            assert constraint design_pump_type_ok_required : 'Offered Equipment Capacity' {
                in defined_in = design_pump_type_ok_required_defined;
                in margin_in = design_pump_type_ok_required_margin;
            }
            calc design_motor_base_ok_required_screen : 'Offered Capacity Screen' {
                in rating_in = 1.0;
                in demand_in = 0.0;
                in applicable_in = true;
                in conditions_supported_in = steam_transport.design_motor_base_ok;
                in demand_available_in = true;
            }
            attribute design_motor_base_ok_required_defined : Real = design_motor_base_ok_required_screen.evaluation_defined;
            attribute design_motor_base_ok_required_margin : Real = design_motor_base_ok_required_screen.margin;
            assert constraint design_motor_base_ok_required : 'Offered Equipment Capacity' {
                in defined_in = design_motor_base_ok_required_defined;
                in margin_in = design_motor_base_ok_required_margin;
            }
            calc design_motor_factor_ok_required_screen : 'Offered Capacity Screen' {
                in rating_in = 1.0;
                in demand_in = 0.0;
                in applicable_in = true;
                in conditions_supported_in = steam_transport.design_motor_factor_ok;
                in demand_available_in = true;
            }
            attribute design_motor_factor_ok_required_defined : Real = design_motor_factor_ok_required_screen.evaluation_defined;
            attribute design_motor_factor_ok_required_margin : Real = design_motor_factor_ok_required_screen.margin;
            assert constraint design_motor_factor_ok_required : 'Offered Equipment Capacity' {
                in defined_in = design_motor_factor_ok_required_defined;
                in margin_in = design_motor_factor_ok_required_margin;
            }
            calc pump_size_ok_required_screen : 'Offered Capacity Screen' {
                in rating_in = 1.0;
                in demand_in = 0.0;
                in applicable_in = true;
                in conditions_supported_in = steam_transport.pump_size_ok;
                in demand_available_in = true;
            }
            attribute pump_size_ok_required_defined : Real = pump_size_ok_required_screen.evaluation_defined;
            attribute pump_size_ok_required_margin : Real = pump_size_ok_required_screen.margin;
            assert constraint pump_size_ok_required : 'Offered Equipment Capacity' {
                in defined_in = pump_size_ok_required_defined;
                in margin_in = pump_size_ok_required_margin;
            }
            calc pump_type_ok_required_screen : 'Offered Capacity Screen' {
                in rating_in = 1.0;
                in demand_in = 0.0;
                in applicable_in = true;
                in conditions_supported_in = steam_transport.pump_type_ok;
                in demand_available_in = true;
            }
            attribute pump_type_ok_required_defined : Real = pump_type_ok_required_screen.evaluation_defined;
            attribute pump_type_ok_required_margin : Real = pump_type_ok_required_screen.margin;
            assert constraint pump_type_ok_required : 'Offered Equipment Capacity' {
                in defined_in = pump_type_ok_required_defined;
                in margin_in = pump_type_ok_required_margin;
            }
            calc motor_base_ok_required_screen : 'Offered Capacity Screen' {
                in rating_in = 1.0;
                in demand_in = 0.0;
                in applicable_in = true;
                in conditions_supported_in = steam_transport.motor_base_ok;
                in demand_available_in = true;
            }
            attribute motor_base_ok_required_defined : Real = motor_base_ok_required_screen.evaluation_defined;
            attribute motor_base_ok_required_margin : Real = motor_base_ok_required_screen.margin;
            assert constraint motor_base_ok_required : 'Offered Equipment Capacity' {
                in defined_in = motor_base_ok_required_defined;
                in margin_in = motor_base_ok_required_margin;
            }
            calc motor_factor_ok_required_screen : 'Offered Capacity Screen' {
                in rating_in = 1.0;
                in demand_in = 0.0;
                in applicable_in = true;
                in conditions_supported_in = steam_transport.motor_factor_ok;
                in demand_available_in = true;
            }
            attribute motor_factor_ok_required_defined : Real = motor_factor_ok_required_screen.evaluation_defined;
            attribute motor_factor_ok_required_margin : Real = motor_factor_ok_required_screen.margin;
            assert constraint motor_factor_ok_required : 'Offered Equipment Capacity' {
                in defined_in = motor_factor_ok_required_defined;
                in margin_in = motor_factor_ok_required_margin;
            }
            calc salt_head_ok_required_screen : 'Offered Capacity Screen' {
                in rating_in = 1.0;
                in demand_in = 0.0;
                in applicable_in = true;
                in conditions_supported_in = steam_transport.salt_head_ok;
                in demand_available_in = true;
            }
            attribute salt_head_ok_required_defined : Real = salt_head_ok_required_screen.evaluation_defined;
            attribute salt_head_ok_required_margin : Real = salt_head_ok_required_screen.margin;
            assert constraint salt_head_ok_required : 'Offered Equipment Capacity' {
                in defined_in = salt_head_ok_required_defined;
                in margin_in = salt_head_ok_required_margin;
            }
            calc salt_flow_regime_ok_required_screen : 'Offered Capacity Screen' {
                in rating_in = 1.0;
                in demand_in = 0.0;
                in applicable_in = true;
                in conditions_supported_in = steam_transport.salt_flow_regime_ok;
                in demand_available_in = true;
            }
            attribute salt_flow_regime_ok_required_defined : Real = salt_flow_regime_ok_required_screen.evaluation_defined;
            attribute salt_flow_regime_ok_required_margin : Real = salt_flow_regime_ok_required_screen.margin;
            assert constraint salt_flow_regime_ok_required : 'Offered Equipment Capacity' {
                in defined_in = salt_flow_regime_ok_required_defined;
                in margin_in = salt_flow_regime_ok_required_margin;
            }
        }
        part steam_return_control {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_return_control owns its selected inputs and exposed calculation outputs. */
            attribute secondary_cp : Real = 1560;
            attribute secondary_inlet : Real = 543.15;
            attribute max_bypass : Real = 0.5;
            attribute tolerance : Real = 1e-06;
            calc evaluate : 'Primary Bypass Control' {
                in ua_in = steam_transport.installed_total_UA_MW_K;
                in primary_flow_in = primary_loop.mdot;
                in primary_cp_in = primary_loop.loop_cp;
                in secondary_flow_in = steam_transport.total_salt_flow_kg_s;
                in secondary_cp_in = secondary_cp;
                in primary_limit_in = primary_loop.T_out;
                in secondary_inlet_in = secondary_inlet;
                in duty_in = primary_loop.q_ihx;
                in required_return_in = primary_loop.T_comp_in;
                in max_bypass_in = max_bypass;
                in tolerance_in = tolerance;
            }
            attribute bypass_fraction : Real = evaluate.bypass_fraction;
            attribute feasible : Real = evaluate.feasible;
            attribute capability_open : Real = evaluate.capability_open;
            attribute capability_at_solution : Real = evaluate.capability_at_solution;
            attribute exchanger_primary_flow : Real = evaluate.exchanger_primary_flow;
            attribute exchanger_return : Real = evaluate.exchanger_return;
            attribute mixed_return : Real = evaluate.mixed_return;
            attribute return_residual : Real = evaluate.return_residual;
            attribute return_residual_magnitude : Real = evaluate.return_residual_magnitude;
            attribute effectiveness_at_solution : Real = evaluate.effectiveness_at_solution;
            attribute ntu_at_solution : Real = evaluate.ntu_at_solution;
        }
        part steam_boundary {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_boundary owns its selected inputs and exposed calculation outputs. */
            attribute total_flow_rating : Real = 4000.0;
            attribute exchanger_flow_rating : Real = 4000.0;
            attribute bypass_flow_rating : Real = 2000.0;
            attribute pressure_rating : Real = 8000000.0;
            attribute temperature_rating : Real = 800.0;
            attribute added_dp_rating : Real = 100000.0;
            attribute salt_cp : Real = 1560.0;
            attribute actuation : Real = 0.1;
            attribute gross_electric : Real = 0.0;
            attribute net_shaft : Real = 0.0;
            attribute imported_electric : Real = 0.0;
            attribute cycle_rejection : Real = 0.0;
            calc evaluate : 'Controlled Conversion Boundary' {
                in available_in = primary_loop.q_ihx;
                in capability_open_in = steam_return_control.capability_open;
                in raw_heat_in = steam_return_control.capability_at_solution;
                in feasible_in = steam_return_control.feasible;
                in return_residual_in = steam_return_control.return_residual;
                in primary_flow_in = primary_loop.mdot;
                in exchanger_flow_in = steam_return_control.exchanger_primary_flow;
                in bypass_fraction_in = steam_return_control.bypass_fraction;
                in pressure_in = primary_loop.loop_p;
                in hot_temperature_in = primary_loop.T_out;
                in dp_in = primary_loop.dp_loop;
                in loss_factor_in = primary_loop.f_loss;
                in total_flow_rating_in = total_flow_rating;
                in exchanger_flow_rating_in = exchanger_flow_rating;
                in bypass_flow_rating_in = bypass_flow_rating;
                in max_bypass_in = steam_return_control.max_bypass;
                in pressure_rating_in = pressure_rating;
                in temperature_rating_in = temperature_rating;
                in added_dp_rating_in = added_dp_rating;
                in salt_flow_in = steam_transport.total_salt_flow_kg_s;
                in salt_cp_in = salt_cp;
                in salt_shaft_in = steam_transport.salt_shaft_MW;
                in salt_electric_in = steam_transport.salt_electric_MW;
                in actuation_in = actuation;
                in gross_electric_in = gross_electric;
                in net_shaft_in = net_shaft;
                in imported_electric_in = imported_electric;
                in cycle_rejection_in = cycle_rejection;
            }
            attribute converged : Real = evaluate.converged;
            attribute actual_heat : Real = evaluate.actual_heat;
            attribute unremoved_heat : Real = evaluate.unremoved_heat;
            attribute duty_correction : Real = evaluate.duty_correction;
            attribute raw_heat_residual : Real = evaluate.raw_heat_residual;
            attribute raw_return_residual : Real = evaluate.raw_return_residual;
            attribute salt_hot : Real = evaluate.salt_hot;
            attribute salt_return : Real = evaluate.salt_return;
            attribute steam_heat : Real = evaluate.steam_heat;
            attribute bypass_flow : Real = evaluate.bypass_flow;
            attribute added_dp : Real = evaluate.added_dp;
            attribute total_flow_margin : Real = evaluate.total_flow_margin;
            attribute exchanger_flow_margin : Real = evaluate.exchanger_flow_margin;
            attribute bypass_flow_margin : Real = evaluate.bypass_flow_margin;
            attribute bypass_fraction_margin : Real = evaluate.bypass_fraction_margin;
            attribute pressure_margin : Real = evaluate.pressure_margin;
            attribute temperature_margin : Real = evaluate.temperature_margin;
            attribute added_dp_margin : Real = evaluate.added_dp_margin;
            attribute controller_capacity_ok : Real = evaluate.controller_capacity_ok;
            attribute source_adequate : Real = evaluate.source_adequate;
            attribute generator_loss : Real = evaluate.generator_loss;
            attribute motor_import_loss : Real = evaluate.motor_import_loss;
            attribute salt_motor_loss : Real = evaluate.salt_motor_loss;
            attribute rejection_load : Real = evaluate.rejection_load;
            assert constraint source_adequate_ok : 'Required Flag' {
                in flag_in = source_adequate;
            }
            assert constraint controller_capacity_ok_ok : 'Required Flag' {
                in flag_in = controller_capacity_ok;
            }
            assert constraint total_flow_margin_ok : 'Nonnegative Margin' {
                in margin_in = total_flow_margin;
            }
            assert constraint exchanger_flow_margin_ok : 'Nonnegative Margin' {
                in margin_in = exchanger_flow_margin;
            }
            assert constraint bypass_flow_margin_ok : 'Nonnegative Margin' {
                in margin_in = bypass_flow_margin;
            }
            assert constraint bypass_fraction_margin_ok : 'Nonnegative Margin' {
                in margin_in = bypass_fraction_margin;
            }
            assert constraint pressure_margin_ok : 'Nonnegative Margin' {
                in margin_in = pressure_margin;
            }
            assert constraint temperature_margin_ok : 'Nonnegative Margin' {
                in margin_in = temperature_margin;
            }
            assert constraint added_dp_margin_ok : 'Nonnegative Margin' {
                in margin_in = added_dp_margin;
            }
        }
        part gas_boundary {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. gas_boundary owns its selected inputs and exposed calculation outputs. */
            attribute total_flow_rating : Real = 4000.0;
            attribute exchanger_flow_rating : Real = 4000.0;
            attribute bypass_flow_rating : Real = 2000.0;
            attribute pressure_rating : Real = 8000000.0;
            attribute temperature_rating : Real = 800.0;
            attribute added_dp_rating : Real = 100000.0;
            attribute salt_flow : Real = 0.0;
            attribute salt_cp : Real = 1560.0;
            attribute salt_shaft : Real = 0.0;
            attribute salt_electric : Real = 0.0;
            attribute actuation : Real = 0.1;
            attribute gross_electric : Real = 0.0;
            attribute net_shaft : Real = 0.0;
            attribute imported_electric : Real = 0.0;
            attribute cycle_rejection : Real = 0.0;
            calc evaluate : 'Controlled Conversion Boundary' {
                in available_in = primary_loop.q_ihx;
                in capability_open_in = return_control.capability_open;
                in raw_heat_in = return_control.capability_at_solution;
                in feasible_in = return_control.feasible;
                in return_residual_in = return_control.return_residual;
                in primary_flow_in = primary_loop.mdot;
                in exchanger_flow_in = return_control.exchanger_primary_flow;
                in bypass_fraction_in = return_control.bypass_fraction;
                in pressure_in = primary_loop.loop_p;
                in hot_temperature_in = primary_loop.T_out;
                in dp_in = primary_loop.dp_loop;
                in loss_factor_in = primary_loop.f_loss;
                in total_flow_rating_in = total_flow_rating;
                in exchanger_flow_rating_in = exchanger_flow_rating;
                in bypass_flow_rating_in = bypass_flow_rating;
                in max_bypass_in = return_control.max_bypass;
                in pressure_rating_in = pressure_rating;
                in temperature_rating_in = temperature_rating;
                in added_dp_rating_in = added_dp_rating;
                in salt_flow_in = salt_flow;
                in salt_cp_in = salt_cp;
                in salt_shaft_in = salt_shaft;
                in salt_electric_in = salt_electric;
                in actuation_in = actuation;
                in gross_electric_in = gross_electric;
                in net_shaft_in = net_shaft;
                in imported_electric_in = imported_electric;
                in cycle_rejection_in = cycle_rejection;
            }
            attribute converged : Real = evaluate.converged;
            attribute actual_heat : Real = evaluate.actual_heat;
            attribute unremoved_heat : Real = evaluate.unremoved_heat;
            attribute duty_correction : Real = evaluate.duty_correction;
            attribute raw_heat_residual : Real = evaluate.raw_heat_residual;
            attribute raw_return_residual : Real = evaluate.raw_return_residual;
            attribute salt_hot : Real = evaluate.salt_hot;
            attribute salt_return : Real = evaluate.salt_return;
            attribute steam_heat : Real = evaluate.steam_heat;
            attribute bypass_flow : Real = evaluate.bypass_flow;
            attribute added_dp : Real = evaluate.added_dp;
            attribute total_flow_margin : Real = evaluate.total_flow_margin;
            attribute exchanger_flow_margin : Real = evaluate.exchanger_flow_margin;
            attribute bypass_flow_margin : Real = evaluate.bypass_flow_margin;
            attribute bypass_fraction_margin : Real = evaluate.bypass_fraction_margin;
            attribute pressure_margin : Real = evaluate.pressure_margin;
            attribute temperature_margin : Real = evaluate.temperature_margin;
            attribute added_dp_margin : Real = evaluate.added_dp_margin;
            attribute controller_capacity_ok : Real = evaluate.controller_capacity_ok;
            attribute source_adequate : Real = evaluate.source_adequate;
            attribute generator_loss : Real = evaluate.generator_loss;
            attribute motor_import_loss : Real = evaluate.motor_import_loss;
            attribute salt_motor_loss : Real = evaluate.salt_motor_loss;
            attribute rejection_load : Real = evaluate.rejection_load;
            assert constraint source_adequate_ok : 'Required Flag' {
                in flag_in = source_adequate;
            }
            assert constraint controller_capacity_ok_ok : 'Required Flag' {
                in flag_in = controller_capacity_ok;
            }
            assert constraint total_flow_margin_ok : 'Nonnegative Margin' {
                in margin_in = total_flow_margin;
            }
            assert constraint exchanger_flow_margin_ok : 'Nonnegative Margin' {
                in margin_in = exchanger_flow_margin;
            }
            assert constraint bypass_flow_margin_ok : 'Nonnegative Margin' {
                in margin_in = bypass_flow_margin;
            }
            assert constraint bypass_fraction_margin_ok : 'Nonnegative Margin' {
                in margin_in = bypass_fraction_margin;
            }
            assert constraint pressure_margin_ok : 'Nonnegative Margin' {
                in margin_in = pressure_margin;
            }
            assert constraint temperature_margin_ok : 'Nonnegative Margin' {
                in margin_in = temperature_margin;
            }
            assert constraint added_dp_margin_ok : 'Nonnegative Margin' {
                in margin_in = added_dp_margin;
            }
        }
        part steam_cycle {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_cycle owns its selected inputs and exposed calculation outputs. */
            attribute enabled : Real = 1;
            attribute salt_cp_kJ_kgK : Real = 1.56;
            attribute main_pressure_MPa : Real = 6.2;
            attribute extraction_pressure_MPa : Real = 0.8;
            attribute steam_temperature_C : Real = 445;
            attribute reheat_temperature_C : Real = 445;
            attribute condenser_temperature_C : Real = 42;
            attribute eta_hp : Real = 0.9;
            attribute eta_lp : Real = 0.9;
            attribute eta_condensate_pump : Real = 0.8;
            attribute eta_feedwater_pump : Real = 0.8;
            attribute eta_pump_motor : Real = 0.95;
            attribute eta_mechanical : Real = 0.99;
            attribute eta_generator : Real = 0.98;
            calc evaluate : 'Matched Steam Cycle' {
                in enabled_in = enabled;
                in heat_available_MW_in = steam_boundary.steam_heat;
                in source_heat_MW_in = steam_boundary.actual_heat;
                in selected_recovered_MW_in = steam_transport.salt_shaft_MW;
                in salt_flow_per_circuit_in = steam_transport.salt_flow;
                in salt_circuit_count_in = steam_transport.n_loops;
                in salt_hot_C_in = steam_boundary.salt_hot;
                in salt_return_C_in = steam_boundary.salt_return;
                in salt_cp_kJ_kgK_in = salt_cp_kJ_kgK;
                in main_pressure_MPa_in = main_pressure_MPa;
                in extraction_pressure_MPa_in = extraction_pressure_MPa;
                in steam_temperature_C_in = steam_temperature_C;
                in reheat_temperature_C_in = reheat_temperature_C;
                in condenser_temperature_C_in = condenser_temperature_C;
                in eta_hp_in = eta_hp;
                in eta_lp_in = eta_lp;
                in eta_condensate_pump_in = eta_condensate_pump;
                in eta_feedwater_pump_in = eta_feedwater_pump;
                in eta_pump_motor_in = eta_pump_motor;
                in eta_mechanical_in = eta_mechanical;
                in eta_generator_in = eta_generator;
            }
            attribute p_feed_MPa : Real = evaluate.p_feed_MPa;
            attribute h_feed_kJ_kg : Real = evaluate.h_feed_kJ_kg;
            attribute mdot_feed_kg_s : Real = evaluate.mdot_feed_kg_s;
            attribute t_feed_C : Real = evaluate.t_feed_C;
            attribute s_feed_kJ_kgK : Real = evaluate.s_feed_kJ_kgK;
            attribute p_main_MPa : Real = evaluate.p_main_MPa;
            attribute h_main_kJ_kg : Real = evaluate.h_main_kJ_kg;
            attribute mdot_main_kg_s : Real = evaluate.mdot_main_kg_s;
            attribute t_main_C : Real = evaluate.t_main_C;
            attribute s_main_kJ_kgK : Real = evaluate.s_main_kJ_kgK;
            attribute p_hp_MPa : Real = evaluate.p_hp_MPa;
            attribute h_hp_kJ_kg : Real = evaluate.h_hp_kJ_kg;
            attribute mdot_hp_kg_s : Real = evaluate.mdot_hp_kg_s;
            attribute t_hp_C : Real = evaluate.t_hp_C;
            attribute s_hp_kJ_kgK : Real = evaluate.s_hp_kJ_kgK;
            attribute p_reheat_MPa : Real = evaluate.p_reheat_MPa;
            attribute h_reheat_kJ_kg : Real = evaluate.h_reheat_kJ_kg;
            attribute mdot_reheat_kg_s : Real = evaluate.mdot_reheat_kg_s;
            attribute t_reheat_C : Real = evaluate.t_reheat_C;
            attribute s_reheat_kJ_kgK : Real = evaluate.s_reheat_kJ_kgK;
            attribute p_lp_MPa : Real = evaluate.p_lp_MPa;
            attribute h_lp_kJ_kg : Real = evaluate.h_lp_kJ_kg;
            attribute mdot_lp_kg_s : Real = evaluate.mdot_lp_kg_s;
            attribute t_lp_C : Real = evaluate.t_lp_C;
            attribute s_lp_kJ_kgK : Real = evaluate.s_lp_kJ_kgK;
            attribute p_condensate_MPa : Real = evaluate.p_condensate_MPa;
            attribute h_condensate_kJ_kg : Real = evaluate.h_condensate_kJ_kg;
            attribute mdot_condensate_kg_s : Real = evaluate.mdot_condensate_kg_s;
            attribute t_condensate_C : Real = evaluate.t_condensate_C;
            attribute s_condensate_kJ_kgK : Real = evaluate.s_condensate_kJ_kgK;
            attribute p_condensate_pumped_MPa : Real = evaluate.p_condensate_pumped_MPa;
            attribute h_condensate_pumped_kJ_kg : Real = evaluate.h_condensate_pumped_kJ_kg;
            attribute mdot_condensate_pumped_kg_s : Real = evaluate.mdot_condensate_pumped_kg_s;
            attribute p_heater_MPa : Real = evaluate.p_heater_MPa;
            attribute h_heater_kJ_kg : Real = evaluate.h_heater_kJ_kg;
            attribute mdot_heater_kg_s : Real = evaluate.mdot_heater_kg_s;
            attribute t_heater_C : Real = evaluate.t_heater_C;
            attribute s_heater_kJ_kgK : Real = evaluate.s_heater_kJ_kgK;
            attribute bleed_fraction : Real = evaluate.bleed_fraction;
            attribute mdot_bleed_kg_s : Real = evaluate.mdot_bleed_kg_s;
            attribute salt_flow_total_kg_s : Real = evaluate.salt_flow_total_kg_s;
            attribute salt_main_flow_kg_s : Real = evaluate.salt_main_flow_kg_s;
            attribute salt_reheat_flow_kg_s : Real = evaluate.salt_reheat_flow_kg_s;
            attribute q_main_MW : Real = evaluate.q_main_MW;
            attribute q_reheat_MW : Real = evaluate.q_reheat_MW;
            attribute q_condenser_MW : Real = evaluate.q_condenser_MW;
            attribute p_hp_shaft_MW : Real = evaluate.p_hp_shaft_MW;
            attribute p_lp_shaft_MW : Real = evaluate.p_lp_shaft_MW;
            attribute p_condensate_shaft_MW : Real = evaluate.p_condensate_shaft_MW;
            attribute p_feedwater_shaft_MW : Real = evaluate.p_feedwater_shaft_MW;
            attribute p_condensate_electric_MW : Real = evaluate.p_condensate_electric_MW;
            attribute p_feedwater_electric_MW : Real = evaluate.p_feedwater_electric_MW;
            attribute p_cycle_pumps_MW : Real = evaluate.p_cycle_pumps_MW;
            attribute p_gross_MW : Real = evaluate.p_gross_MW;
            attribute eta_gross : Real = evaluate.eta_gross;
            attribute p_cycle_net_before_cooling_MW : Real = evaluate.p_cycle_net_before_cooling_MW;
            attribute q_mechanical_loss_MW : Real = evaluate.q_mechanical_loss_MW;
            attribute q_generator_loss_MW : Real = evaluate.q_generator_loss_MW;
            attribute q_pump_motor_loss_MW : Real = evaluate.q_pump_motor_loss_MW;
            attribute q_rejection_before_cooling_MW : Real = evaluate.q_rejection_before_cooling_MW;
            attribute lp_quality : Real = evaluate.lp_quality;
            attribute lp_moisture_fraction : Real = evaluate.lp_moisture_fraction;
            attribute main_min_gap_K : Real = evaluate.main_min_gap_K;
            attribute reheat_min_gap_K : Real = evaluate.reheat_min_gap_K;
            attribute main_UA_MW_K : Real = evaluate.main_UA_MW_K;
            attribute reheat_UA_MW_K : Real = evaluate.reheat_UA_MW_K;
            attribute salt_heat_residual_MW : Real = evaluate.salt_heat_residual_MW;
            attribute heater_mass_residual_kg_s : Real = evaluate.heater_mass_residual_kg_s;
            attribute heater_energy_residual_MW : Real = evaluate.heater_energy_residual_MW;
            attribute cycle_shaft_residual_MW : Real = evaluate.cycle_shaft_residual_MW;
            attribute cycle_electric_residual_MW : Real = evaluate.cycle_electric_residual_MW;
            attribute active : Boolean = evaluate.active;
            attribute main_UA_available : Boolean = evaluate.main_UA_available;
            attribute reheat_UA_available : Boolean = evaluate.reheat_UA_available;
            attribute main_admission_ok : Boolean = evaluate.main_admission_ok;
            attribute reheat_admission_ok : Boolean = evaluate.reheat_admission_ok;
            attribute turbine_equipment_qualified : Boolean = evaluate.turbine_equipment_qualified;
            attribute installed_sg_capacity_qualified : Boolean = evaluate.installed_sg_capacity_qualified;
            calc main_UA_available_required_screen : 'Offered Capacity Screen' {
                in rating_in = 1.0;
                in demand_in = 0.0;
                in applicable_in = true;
                in conditions_supported_in = steam_cycle.main_UA_available;
                in demand_available_in = true;
            }
            attribute main_UA_available_required_defined : Real = main_UA_available_required_screen.evaluation_defined;
            attribute main_UA_available_required_margin : Real = main_UA_available_required_screen.margin;
            assert constraint main_UA_available_required : 'Offered Equipment Capacity' {
                in defined_in = main_UA_available_required_defined;
                in margin_in = main_UA_available_required_margin;
            }
            calc reheat_UA_available_required_screen : 'Offered Capacity Screen' {
                in rating_in = 1.0;
                in demand_in = 0.0;
                in applicable_in = true;
                in conditions_supported_in = steam_cycle.reheat_UA_available;
                in demand_available_in = true;
            }
            attribute reheat_UA_available_required_defined : Real = reheat_UA_available_required_screen.evaluation_defined;
            attribute reheat_UA_available_required_margin : Real = reheat_UA_available_required_screen.margin;
            assert constraint reheat_UA_available_required : 'Offered Equipment Capacity' {
                in defined_in = reheat_UA_available_required_defined;
                in margin_in = reheat_UA_available_required_margin;
            }
            calc main_admission_ok_required_screen : 'Offered Capacity Screen' {
                in rating_in = 1.0;
                in demand_in = 0.0;
                in applicable_in = true;
                in conditions_supported_in = steam_cycle.main_admission_ok;
                in demand_available_in = true;
            }
            attribute main_admission_ok_required_defined : Real = main_admission_ok_required_screen.evaluation_defined;
            attribute main_admission_ok_required_margin : Real = main_admission_ok_required_screen.margin;
            assert constraint main_admission_ok_required : 'Offered Equipment Capacity' {
                in defined_in = main_admission_ok_required_defined;
                in margin_in = main_admission_ok_required_margin;
            }
            calc reheat_admission_ok_required_screen : 'Offered Capacity Screen' {
                in rating_in = 1.0;
                in demand_in = 0.0;
                in applicable_in = true;
                in conditions_supported_in = steam_cycle.reheat_admission_ok;
                in demand_available_in = true;
            }
            attribute reheat_admission_ok_required_defined : Real = reheat_admission_ok_required_screen.evaluation_defined;
            attribute reheat_admission_ok_required_margin : Real = reheat_admission_ok_required_screen.margin;
            assert constraint reheat_admission_ok_required : 'Offered Equipment Capacity' {
                in defined_in = reheat_admission_ok_required_defined;
                in margin_in = reheat_admission_ok_required_margin;
            }
        }
        part steam_losses {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_losses owns its selected inputs and exposed calculation outputs. */
            attribute available : Real = 0.0;
            attribute capability_open : Real = 0.0;
            attribute raw_heat : Real = 0.0;
            attribute feasible : Real = 0.0;
            attribute return_residual : Real = 0.0;
            attribute primary_flow : Real = 0.0;
            attribute exchanger_flow : Real = 0.0;
            attribute bypass_fraction : Real = 0.0;
            attribute pressure : Real = 0.0;
            attribute hot_temperature : Real = 0.0;
            attribute dp : Real = 0.0;
            attribute loss_factor : Real = 1.1;
            attribute total_flow_rating : Real = 4000.0;
            attribute exchanger_flow_rating : Real = 4000.0;
            attribute bypass_flow_rating : Real = 2000.0;
            attribute max_bypass : Real = 0.5;
            attribute pressure_rating : Real = 8000000.0;
            attribute temperature_rating : Real = 800.0;
            attribute added_dp_rating : Real = 100000.0;
            attribute salt_flow : Real = 0.0;
            attribute salt_cp : Real = 1560.0;
            attribute gross_electric : Real = 0.0;
            attribute net_shaft : Real = 0.0;
            attribute imported_electric : Real = 0.0;
            calc evaluate : 'Controlled Conversion Boundary' {
                in available_in = available;
                in capability_open_in = capability_open;
                in raw_heat_in = raw_heat;
                in feasible_in = feasible;
                in return_residual_in = return_residual;
                in primary_flow_in = primary_flow;
                in exchanger_flow_in = exchanger_flow;
                in bypass_fraction_in = bypass_fraction;
                in pressure_in = pressure;
                in hot_temperature_in = hot_temperature;
                in dp_in = dp;
                in loss_factor_in = loss_factor;
                in total_flow_rating_in = total_flow_rating;
                in exchanger_flow_rating_in = exchanger_flow_rating;
                in bypass_flow_rating_in = bypass_flow_rating;
                in max_bypass_in = max_bypass;
                in pressure_rating_in = pressure_rating;
                in temperature_rating_in = temperature_rating;
                in added_dp_rating_in = added_dp_rating;
                in salt_flow_in = salt_flow;
                in salt_cp_in = salt_cp;
                in salt_shaft_in = steam_transport.salt_shaft_MW;
                in salt_electric_in = steam_transport.salt_electric_MW;
                in actuation_in = steam_boundary.actuation;
                in gross_electric_in = gross_electric;
                in net_shaft_in = net_shaft;
                in imported_electric_in = imported_electric;
                in cycle_rejection_in = steam_cycle.q_rejection_before_cooling_MW;
            }
            attribute converged : Real = evaluate.converged;
            attribute actual_heat : Real = evaluate.actual_heat;
            attribute unremoved_heat : Real = evaluate.unremoved_heat;
            attribute duty_correction : Real = evaluate.duty_correction;
            attribute raw_heat_residual : Real = evaluate.raw_heat_residual;
            attribute raw_return_residual : Real = evaluate.raw_return_residual;
            attribute salt_hot : Real = evaluate.salt_hot;
            attribute salt_return : Real = evaluate.salt_return;
            attribute steam_heat : Real = evaluate.steam_heat;
            attribute bypass_flow : Real = evaluate.bypass_flow;
            attribute added_dp : Real = evaluate.added_dp;
            attribute total_flow_margin : Real = evaluate.total_flow_margin;
            attribute exchanger_flow_margin : Real = evaluate.exchanger_flow_margin;
            attribute bypass_flow_margin : Real = evaluate.bypass_flow_margin;
            attribute bypass_fraction_margin : Real = evaluate.bypass_fraction_margin;
            attribute pressure_margin : Real = evaluate.pressure_margin;
            attribute temperature_margin : Real = evaluate.temperature_margin;
            attribute added_dp_margin : Real = evaluate.added_dp_margin;
            attribute controller_capacity_ok : Real = evaluate.controller_capacity_ok;
            attribute source_adequate : Real = evaluate.source_adequate;
            attribute generator_loss : Real = evaluate.generator_loss;
            attribute motor_import_loss : Real = evaluate.motor_import_loss;
            attribute salt_motor_loss : Real = evaluate.salt_motor_loss;
            attribute rejection_load : Real = evaluate.rejection_load;
        }
        part gas_losses {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. gas_losses owns its selected inputs and exposed calculation outputs. */
            attribute available : Real = 0.0;
            attribute capability_open : Real = 0.0;
            attribute raw_heat : Real = 0.0;
            attribute feasible : Real = 0.0;
            attribute return_residual : Real = 0.0;
            attribute primary_flow : Real = 0.0;
            attribute exchanger_flow : Real = 0.0;
            attribute bypass_fraction : Real = 0.0;
            attribute pressure : Real = 0.0;
            attribute hot_temperature : Real = 0.0;
            attribute dp : Real = 0.0;
            attribute loss_factor : Real = 1.1;
            attribute total_flow_rating : Real = 4000.0;
            attribute exchanger_flow_rating : Real = 4000.0;
            attribute bypass_flow_rating : Real = 2000.0;
            attribute max_bypass : Real = 0.5;
            attribute pressure_rating : Real = 8000000.0;
            attribute temperature_rating : Real = 800.0;
            attribute added_dp_rating : Real = 100000.0;
            attribute salt_flow : Real = 0.0;
            attribute salt_cp : Real = 1560.0;
            attribute salt_shaft : Real = 0.0;
            attribute salt_electric : Real = 0.0;
            attribute cycle_rejection : Real = 0.0;
            calc evaluate : 'Controlled Conversion Boundary' {
                in available_in = available;
                in capability_open_in = capability_open;
                in raw_heat_in = raw_heat;
                in feasible_in = feasible;
                in return_residual_in = return_residual;
                in primary_flow_in = primary_flow;
                in exchanger_flow_in = exchanger_flow;
                in bypass_fraction_in = bypass_fraction;
                in pressure_in = pressure;
                in hot_temperature_in = hot_temperature;
                in dp_in = dp;
                in loss_factor_in = loss_factor;
                in total_flow_rating_in = total_flow_rating;
                in exchanger_flow_rating_in = exchanger_flow_rating;
                in bypass_flow_rating_in = bypass_flow_rating;
                in max_bypass_in = max_bypass;
                in pressure_rating_in = pressure_rating;
                in temperature_rating_in = temperature_rating;
                in added_dp_rating_in = added_dp_rating;
                in salt_flow_in = salt_flow;
                in salt_cp_in = salt_cp;
                in salt_shaft_in = salt_shaft;
                in salt_electric_in = salt_electric;
                in actuation_in = gas_boundary.actuation;
                in gross_electric_in = electrical.gross_electric;
                in net_shaft_in = electrical.net_shaft;
                in imported_electric_in = electrical.shaft_import;
                in cycle_rejection_in = cycle_rejection;
            }
            attribute converged : Real = evaluate.converged;
            attribute actual_heat : Real = evaluate.actual_heat;
            attribute unremoved_heat : Real = evaluate.unremoved_heat;
            attribute duty_correction : Real = evaluate.duty_correction;
            attribute raw_heat_residual : Real = evaluate.raw_heat_residual;
            attribute raw_return_residual : Real = evaluate.raw_return_residual;
            attribute salt_hot : Real = evaluate.salt_hot;
            attribute salt_return : Real = evaluate.salt_return;
            attribute steam_heat : Real = evaluate.steam_heat;
            attribute bypass_flow : Real = evaluate.bypass_flow;
            attribute added_dp : Real = evaluate.added_dp;
            attribute total_flow_margin : Real = evaluate.total_flow_margin;
            attribute exchanger_flow_margin : Real = evaluate.exchanger_flow_margin;
            attribute bypass_flow_margin : Real = evaluate.bypass_flow_margin;
            attribute bypass_fraction_margin : Real = evaluate.bypass_fraction_margin;
            attribute pressure_margin : Real = evaluate.pressure_margin;
            attribute temperature_margin : Real = evaluate.temperature_margin;
            attribute added_dp_margin : Real = evaluate.added_dp_margin;
            attribute controller_capacity_ok : Real = evaluate.controller_capacity_ok;
            attribute source_adequate : Real = evaluate.source_adequate;
            attribute generator_loss : Real = evaluate.generator_loss;
            attribute motor_import_loss : Real = evaluate.motor_import_loss;
            attribute salt_motor_loss : Real = evaluate.salt_motor_loss;
            attribute rejection_load : Real = evaluate.rejection_load;
        }
        part steam_water {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_water owns its selected inputs and exposed calculation outputs. */
            attribute enabled : Real = 1;
            attribute cycle_active : Real = 1;
            attribute condenser_temperature_C : Real = 42;
            attribute water_inlet_C : Real = 25;
            attribute water_outlet_C : Real = 35;
            attribute head_m : Real = 20;
            attribute eta_pump : Real = 0.8;
            attribute eta_motor : Real = 0.95;
            calc evaluate : 'Cooling Water Rejection' {
                in enabled_in = enabled;
                in cycle_active_in = cycle_active;
                in q_rejection_before_cooling_MW_in = steam_losses.rejection_load;
                in condenser_temperature_C_in = condenser_temperature_C;
                in water_inlet_C_in = water_inlet_C;
                in water_outlet_C_in = water_outlet_C;
                in head_m_in = head_m;
                in eta_pump_in = eta_pump;
                in eta_motor_in = eta_motor;
            }
            attribute water_flow_kg_s : Real = evaluate.water_flow_kg_s;
            attribute p_cooling_pump_shaft_MW : Real = evaluate.p_cooling_pump_shaft_MW;
            attribute p_cooling_pump_electric_MW : Real = evaluate.p_cooling_pump_electric_MW;
            attribute q_cooling_motor_loss_MW : Real = evaluate.q_cooling_motor_loss_MW;
            attribute q_total_rejection_MW : Real = evaluate.q_total_rejection_MW;
            attribute water_pump_rise_K : Real = evaluate.water_pump_rise_K;
            attribute condenser_water_gap_K : Real = evaluate.condenser_water_gap_K;
            attribute water_energy_residual_MW : Real = evaluate.water_energy_residual_MW;
            attribute denominator_kJ_kg : Real = evaluate.denominator_kJ_kg;
            attribute active : Boolean = evaluate.active;
            attribute reference_scenario : Boolean = evaluate.reference_scenario;
            attribute site_qualified : Boolean = evaluate.site_qualified;
            attribute cooling_approach_ok : Boolean = evaluate.cooling_approach_ok;
            calc cooling_approach_ok_required_screen : 'Offered Capacity Screen' {
                in rating_in = 1.0;
                in demand_in = 0.0;
                in applicable_in = true;
                in conditions_supported_in = steam_water.cooling_approach_ok;
                in demand_available_in = true;
            }
            attribute cooling_approach_ok_required_defined : Real = cooling_approach_ok_required_screen.evaluation_defined;
            attribute cooling_approach_ok_required_margin : Real = cooling_approach_ok_required_screen.margin;
            assert constraint cooling_approach_ok_required : 'Offered Equipment Capacity' {
                in defined_in = cooling_approach_ok_required_defined;
                in margin_in = cooling_approach_ok_required_margin;
            }
        }
        part gas_loss_water {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. gas_loss_water owns its selected inputs and exposed calculation outputs. */
            attribute enabled : Real = 1;
            attribute cycle_active : Real = 1;
            attribute condenser_temperature_C : Real = 42;
            attribute water_inlet_C : Real = 25;
            attribute water_outlet_C : Real = 35;
            attribute head_m : Real = 20;
            attribute eta_pump : Real = 0.8;
            attribute eta_motor : Real = 0.95;
            calc evaluate : 'Cooling Water Rejection' {
                in enabled_in = enabled;
                in cycle_active_in = cycle_active;
                in q_rejection_before_cooling_MW_in = gas_losses.rejection_load;
                in condenser_temperature_C_in = condenser_temperature_C;
                in water_inlet_C_in = water_inlet_C;
                in water_outlet_C_in = water_outlet_C;
                in head_m_in = head_m;
                in eta_pump_in = eta_pump;
                in eta_motor_in = eta_motor;
            }
            attribute water_flow_kg_s : Real = evaluate.water_flow_kg_s;
            attribute p_cooling_pump_shaft_MW : Real = evaluate.p_cooling_pump_shaft_MW;
            attribute p_cooling_pump_electric_MW : Real = evaluate.p_cooling_pump_electric_MW;
            attribute q_cooling_motor_loss_MW : Real = evaluate.q_cooling_motor_loss_MW;
            attribute q_total_rejection_MW : Real = evaluate.q_total_rejection_MW;
            attribute water_pump_rise_K : Real = evaluate.water_pump_rise_K;
            attribute condenser_water_gap_K : Real = evaluate.condenser_water_gap_K;
            attribute water_energy_residual_MW : Real = evaluate.water_energy_residual_MW;
            attribute denominator_kJ_kg : Real = evaluate.denominator_kJ_kg;
            attribute active : Boolean = evaluate.active;
            attribute reference_scenario : Boolean = evaluate.reference_scenario;
            attribute site_qualified : Boolean = evaluate.site_qualified;
            attribute cooling_approach_ok : Boolean = evaluate.cooling_approach_ok;
            calc cooling_approach_ok_required_screen : 'Offered Capacity Screen' {
                in rating_in = 1.0;
                in demand_in = 0.0;
                in applicable_in = true;
                in conditions_supported_in = gas_loss_water.cooling_approach_ok;
                in demand_available_in = true;
            }
            attribute cooling_approach_ok_required_defined : Real = cooling_approach_ok_required_screen.evaluation_defined;
            attribute cooling_approach_ok_required_margin : Real = cooling_approach_ok_required_screen.margin;
            assert constraint cooling_approach_ok_required : 'Offered Equipment Capacity' {
                in defined_in = cooling_approach_ok_required_defined;
                in margin_in = cooling_approach_ok_required_margin;
            }
        }
        part water_ic1 {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. water_ic1 owns its selected inputs and exposed calculation outputs. */
            attribute ua : Real = 25.0;
            attribute water_inlet_C : Real = 25.0;
            attribute head : Real = 20.0;
            attribute eta_p : Real = 0.8;
            attribute eta_motor : Real = 0.95;
            attribute flow_rating : Real = 100000.0;
            attribute power_rating : Real = 30.0;
            attribute duty_rating : Real = 2000.0;
            calc evaluate : 'Finite Water Cooler' {
                in gas_inlet_K_in = compressor_1.temperature_out;
                in gas_outlet_K_in = intercooler_1.temperature_out;
                in gas_heat_into_fluid_in = intercooler_1.heat_into_fluid;
                in ua_in = ua;
                in water_inlet_C_in = water_inlet_C;
                in head_in = head;
                in eta_p_in = eta_p;
                in eta_motor_in = eta_motor;
                in flow_rating_in = flow_rating;
                in power_rating_in = power_rating;
                in duty_rating_in = duty_rating;
            }
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute failure_code : Real = evaluate.failure_code;
            attribute duty : Real = evaluate.duty;
            attribute water_inlet_after_C : Real = evaluate.water_inlet_after_C;
            attribute water_outlet_C : Real = evaluate.water_outlet_C;
            attribute water_flow : Real = evaluate.water_flow;
            attribute pump_electric : Real = evaluate.pump_electric;
            attribute total_rejection : Real = evaluate.total_rejection;
            attribute min_gap : Real = evaluate.min_gap;
            attribute required_ua : Real = evaluate.required_ua;
            attribute ua_residual : Real = evaluate.ua_residual;
            attribute energy_residual : Real = evaluate.energy_residual;
            attribute flow_margin : Real = evaluate.flow_margin;
            attribute power_margin : Real = evaluate.power_margin;
            attribute duty_margin : Real = evaluate.duty_margin;
            attribute bracket_low_ua : Real = evaluate.bracket_low_ua;
            attribute bracket_high_ua : Real = evaluate.bracket_high_ua;
            attribute iterations : Real = evaluate.iterations;
            assert constraint evaluation_defined_ok : 'Required Flag' {
                in flag_in = evaluation_defined;
            }
            assert constraint flow_margin_ok : 'Nonnegative Margin' {
                in margin_in = flow_margin;
            }
            assert constraint power_margin_ok : 'Nonnegative Margin' {
                in margin_in = power_margin;
            }
            assert constraint duty_margin_ok : 'Nonnegative Margin' {
                in margin_in = duty_margin;
            }
        }
        part water_ic2 {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. water_ic2 owns its selected inputs and exposed calculation outputs. */
            attribute ua : Real = 25.0;
            attribute water_inlet_C : Real = 25.0;
            attribute head : Real = 20.0;
            attribute eta_p : Real = 0.8;
            attribute eta_motor : Real = 0.95;
            attribute flow_rating : Real = 100000.0;
            attribute power_rating : Real = 30.0;
            attribute duty_rating : Real = 2000.0;
            calc evaluate : 'Finite Water Cooler' {
                in gas_inlet_K_in = compressor_2.temperature_out;
                in gas_outlet_K_in = intercooler_2.temperature_out;
                in gas_heat_into_fluid_in = intercooler_2.heat_into_fluid;
                in ua_in = ua;
                in water_inlet_C_in = water_inlet_C;
                in head_in = head;
                in eta_p_in = eta_p;
                in eta_motor_in = eta_motor;
                in flow_rating_in = flow_rating;
                in power_rating_in = power_rating;
                in duty_rating_in = duty_rating;
            }
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute failure_code : Real = evaluate.failure_code;
            attribute duty : Real = evaluate.duty;
            attribute water_inlet_after_C : Real = evaluate.water_inlet_after_C;
            attribute water_outlet_C : Real = evaluate.water_outlet_C;
            attribute water_flow : Real = evaluate.water_flow;
            attribute pump_electric : Real = evaluate.pump_electric;
            attribute total_rejection : Real = evaluate.total_rejection;
            attribute min_gap : Real = evaluate.min_gap;
            attribute required_ua : Real = evaluate.required_ua;
            attribute ua_residual : Real = evaluate.ua_residual;
            attribute energy_residual : Real = evaluate.energy_residual;
            attribute flow_margin : Real = evaluate.flow_margin;
            attribute power_margin : Real = evaluate.power_margin;
            attribute duty_margin : Real = evaluate.duty_margin;
            attribute bracket_low_ua : Real = evaluate.bracket_low_ua;
            attribute bracket_high_ua : Real = evaluate.bracket_high_ua;
            attribute iterations : Real = evaluate.iterations;
            assert constraint evaluation_defined_ok : 'Required Flag' {
                in flag_in = evaluation_defined;
            }
            assert constraint flow_margin_ok : 'Nonnegative Margin' {
                in margin_in = flow_margin;
            }
            assert constraint power_margin_ok : 'Nonnegative Margin' {
                in margin_in = power_margin;
            }
            assert constraint duty_margin_ok : 'Nonnegative Margin' {
                in margin_in = duty_margin;
            }
        }
        part water_pre {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. water_pre owns its selected inputs and exposed calculation outputs. */
            attribute ua : Real = 25.0;
            attribute water_inlet_C : Real = 25.0;
            attribute head : Real = 20.0;
            attribute eta_p : Real = 0.8;
            attribute eta_motor : Real = 0.95;
            attribute flow_rating : Real = 100000.0;
            attribute power_rating : Real = 30.0;
            attribute duty_rating : Real = 2000.0;
            calc evaluate : 'Finite Water Cooler' {
                in gas_inlet_K_in = recuperator.hot_out;
                in gas_outlet_K_in = precooler.temperature_out;
                in gas_heat_into_fluid_in = precooler.heat_into_fluid;
                in ua_in = ua;
                in water_inlet_C_in = water_inlet_C;
                in head_in = head;
                in eta_p_in = eta_p;
                in eta_motor_in = eta_motor;
                in flow_rating_in = flow_rating;
                in power_rating_in = power_rating;
                in duty_rating_in = duty_rating;
            }
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute failure_code : Real = evaluate.failure_code;
            attribute duty : Real = evaluate.duty;
            attribute water_inlet_after_C : Real = evaluate.water_inlet_after_C;
            attribute water_outlet_C : Real = evaluate.water_outlet_C;
            attribute water_flow : Real = evaluate.water_flow;
            attribute pump_electric : Real = evaluate.pump_electric;
            attribute total_rejection : Real = evaluate.total_rejection;
            attribute min_gap : Real = evaluate.min_gap;
            attribute required_ua : Real = evaluate.required_ua;
            attribute ua_residual : Real = evaluate.ua_residual;
            attribute energy_residual : Real = evaluate.energy_residual;
            attribute flow_margin : Real = evaluate.flow_margin;
            attribute power_margin : Real = evaluate.power_margin;
            attribute duty_margin : Real = evaluate.duty_margin;
            attribute bracket_low_ua : Real = evaluate.bracket_low_ua;
            attribute bracket_high_ua : Real = evaluate.bracket_high_ua;
            attribute iterations : Real = evaluate.iterations;
            assert constraint evaluation_defined_ok : 'Required Flag' {
                in flag_in = evaluation_defined;
            }
            assert constraint flow_margin_ok : 'Nonnegative Margin' {
                in margin_in = flow_margin;
            }
            assert constraint power_margin_ok : 'Nonnegative Margin' {
                in margin_in = power_margin;
            }
            assert constraint duty_margin_ok : 'Nonnegative Margin' {
                in margin_in = duty_margin;
            }
        }
        part steam_conditions {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_conditions owns its selected inputs and exposed calculation outputs. */
            attribute enabled : Boolean = true;
            attribute rated_main_pressure_MPa : Real = 6.2;
            attribute rated_extraction_pressure_MPa : Real = 0.8;
            attribute rated_steam_C : Real = 445;
            attribute rated_reheat_C : Real = 445;
            attribute rated_condenser_C : Real = 42;
            attribute rated_salt_hot_C : Real = 465;
            attribute rated_salt_return_C : Real = 269.6647299145299;
            attribute rated_salt_cp : Real = 1.56;
            calc evaluate : 'Steam Offered Conditions' {
                in enabled_in = enabled;
                in actual_main_pressure_MPa_in = steam_cycle.main_pressure_MPa;
                in rated_main_pressure_MPa_in = rated_main_pressure_MPa;
                in actual_extraction_pressure_MPa_in = steam_cycle.extraction_pressure_MPa;
                in rated_extraction_pressure_MPa_in = rated_extraction_pressure_MPa;
                in actual_steam_C_in = steam_cycle.steam_temperature_C;
                in rated_steam_C_in = rated_steam_C;
                in actual_reheat_C_in = steam_cycle.reheat_temperature_C;
                in rated_reheat_C_in = rated_reheat_C;
                in actual_condenser_C_in = steam_cycle.condenser_temperature_C;
                in rated_condenser_C_in = rated_condenser_C;
                in actual_salt_hot_C_in = steam_boundary.salt_hot;
                in rated_salt_hot_C_in = rated_salt_hot_C;
                in actual_salt_return_C_in = steam_boundary.salt_return;
                in rated_salt_return_C_in = rated_salt_return_C;
                in actual_salt_cp_in = steam_cycle.salt_cp_kJ_kgK;
                in rated_salt_cp_in = rated_salt_cp;
            }
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            calc supported_required_screen : 'Offered Capacity Screen' {
                in rating_in = 1.0;
                in demand_in = 0.0;
                in applicable_in = true;
                in conditions_supported_in = steam_conditions.supported;
                in demand_available_in = true;
            }
            attribute supported_required_defined : Real = supported_required_screen.evaluation_defined;
            attribute supported_required_margin : Real = supported_required_screen.margin;
            assert constraint supported_required : 'Offered Equipment Capacity' {
                in defined_in = supported_required_defined;
                in margin_in = supported_required_margin;
            }
        }
        part steam_gross_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_gross_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 1219.9981701764736;
            attribute selected_applicable : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = steam_cycle.p_gross_MW;
                in applicable_in = selected_applicable;
                in conditions_supported_in = steam_conditions.supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part steam_main_ua_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_main_ua_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 41.07437838721364;
            attribute selected_applicable : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = steam_cycle.main_UA_MW_K;
                in applicable_in = selected_applicable;
                in conditions_supported_in = steam_conditions.supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part steam_reheat_ua_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_reheat_ua_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 11.18676341684029;
            attribute selected_applicable : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = steam_cycle.reheat_UA_MW_K;
                in applicable_in = selected_applicable;
                in conditions_supported_in = steam_conditions.supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part steam_hp_flow_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_hp_flow_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 1108.5733942490049;
            attribute selected_applicable : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = steam_cycle.mdot_hp_kg_s;
                in applicable_in = selected_applicable;
                in conditions_supported_in = steam_conditions.supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part steam_hp_shaft_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_hp_shaft_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 507.1088862154872;
            attribute selected_applicable : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = steam_cycle.p_hp_shaft_MW;
                in applicable_in = selected_applicable;
                in conditions_supported_in = steam_conditions.supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part steam_lp_flow_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_lp_flow_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 881.3051322292799;
            attribute selected_applicable : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = steam_cycle.mdot_lp_kg_s;
                in applicable_in = selected_applicable;
                in conditions_supported_in = steam_conditions.supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part steam_lp_shaft_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_lp_shaft_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 750.3619138014925;
            attribute selected_applicable : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = steam_cycle.p_lp_shaft_MW;
                in applicable_in = selected_applicable;
                in conditions_supported_in = steam_conditions.supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part steam_condenser_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_condenser_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 2058.639911447174;
            attribute selected_applicable : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = steam_cycle.q_condenser_MW;
                in applicable_in = selected_applicable;
                in conditions_supported_in = steam_conditions.supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part steam_condensate_flow_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_condensate_flow_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 881.3051322292799;
            attribute selected_applicable : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = steam_cycle.mdot_condensate_kg_s;
                in applicable_in = selected_applicable;
                in conditions_supported_in = steam_conditions.supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part steam_condensate_electric_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_condensate_electric_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 0.9261383157389033;
            attribute selected_applicable : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = steam_cycle.p_condensate_electric_MW;
                in applicable_in = selected_applicable;
                in conditions_supported_in = steam_conditions.supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part steam_feed_flow_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_feed_flow_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 1108.5733942490049;
            attribute selected_applicable : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = steam_cycle.mdot_feed_kg_s;
                in applicable_in = selected_applicable;
                in conditions_supported_in = steam_conditions.supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part steam_feed_electric_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_feed_electric_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 8.780822331904837;
            attribute selected_applicable : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = steam_cycle.p_feedwater_electric_MW;
                in applicable_in = selected_applicable;
                in conditions_supported_in = steam_conditions.supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part steam_condensate_pressure {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_condensate_pressure owns its selected inputs and exposed calculation outputs. */
            attribute active : Boolean = true;
            calc evaluate : 'Pump Pressure Rise' {
                in active_in = active;
                in outlet_MPa_in = steam_cycle.p_condensate_pumped_MPa;
                in inlet_MPa_in = steam_cycle.p_condensate_MPa;
            }
            attribute demand : Real = evaluate.demand;
        }
        part steam_condensate_pressure_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_condensate_pressure_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 0.7917904366;
            attribute selected_applicable : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = steam_condensate_pressure.demand;
                in applicable_in = selected_applicable;
                in conditions_supported_in = steam_conditions.supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part steam_feed_pressure {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_feed_pressure owns its selected inputs and exposed calculation outputs. */
            attribute active : Boolean = true;
            calc evaluate : 'Pump Pressure Rise' {
                in active_in = active;
                in outlet_MPa_in = steam_cycle.p_feed_MPa;
                in inlet_MPa_in = steam_cycle.p_heater_MPa;
            }
            attribute demand : Real = evaluate.demand;
        }
        part steam_feed_pressure_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_feed_pressure_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 5.4;
            attribute selected_applicable : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = steam_feed_pressure.demand;
                in applicable_in = selected_applicable;
                in conditions_supported_in = steam_conditions.supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part salt_fill_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. salt_fill_capacity owns its selected inputs and exposed calculation outputs. */
            attribute selected_applicable : Boolean = true;
            attribute conditions_supported : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = steam_transport.salt_purchased_mass_kg;
                in demand_in = steam_transport.salt_required_fill_mass_kg;
                in applicable_in = selected_applicable;
                in conditions_supported_in = conditions_supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part salt_flow_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. salt_flow_capacity owns its selected inputs and exposed calculation outputs. */
            attribute selected_applicable : Boolean = true;
            attribute conditions_supported : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = steam_transport.salt_design_flow_kg_s;
                in demand_in = steam_transport.salt_pump_flow;
                in applicable_in = selected_applicable;
                in conditions_supported_in = conditions_supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part salt_shaft_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. salt_shaft_capacity owns its selected inputs and exposed calculation outputs. */
            attribute selected_applicable : Boolean = true;
            attribute conditions_supported : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = steam_transport.salt_design_shaft_MW;
                in demand_in = steam_transport.salt_pump_shaft_MW;
                in applicable_in = selected_applicable;
                in conditions_supported_in = conditions_supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part salt_electric_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. salt_electric_capacity owns its selected inputs and exposed calculation outputs. */
            attribute selected_applicable : Boolean = true;
            attribute conditions_supported : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = steam_transport.salt_design_electric_MW;
                in demand_in = steam_transport.salt_pump_electric_MW;
                in applicable_in = selected_applicable;
                in conditions_supported_in = conditions_supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part steam_water_flow_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_water_flow_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 50463.801850311946;
            attribute selected_applicable : Boolean = true;
            attribute conditions_supported : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = steam_water.water_flow_kg_s;
                in applicable_in = selected_applicable;
                in conditions_supported_in = conditions_supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part steam_water_electric_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_water_electric_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 13.023180063562146;
            attribute selected_applicable : Boolean = true;
            attribute conditions_supported : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = steam_water.p_cooling_pump_electric_MW;
                in applicable_in = selected_applicable;
                in conditions_supported_in = conditions_supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part steam_rejection_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_rejection_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 2109.621069383624;
            attribute selected_applicable : Boolean = true;
            attribute conditions_supported : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = steam_water.q_total_rejection_MW;
                in applicable_in = selected_applicable;
                in conditions_supported_in = conditions_supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part gas_loss_flow_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. gas_loss_flow_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 3000;
            attribute selected_applicable : Boolean = true;
            attribute conditions_supported : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = gas_loss_water.water_flow_kg_s;
                in applicable_in = selected_applicable;
                in conditions_supported_in = conditions_supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part gas_loss_electric_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. gas_loss_electric_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 1;
            attribute selected_applicable : Boolean = true;
            attribute conditions_supported : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = gas_loss_water.p_cooling_pump_electric_MW;
                in applicable_in = selected_applicable;
                in conditions_supported_in = conditions_supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part gas_loss_duty_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. gas_loss_duty_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 100;
            attribute selected_applicable : Boolean = true;
            attribute conditions_supported : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = gas_losses.rejection_load;
                in applicable_in = selected_applicable;
                in conditions_supported_in = conditions_supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part recuperator_duty_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. recuperator_duty_capacity owns its selected inputs and exposed calculation outputs. */
            attribute rating : Real = 4000;
            attribute selected_applicable : Boolean = true;
            attribute conditions_supported : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = rating;
                in demand_in = recuperator.recovered_heat;
                in applicable_in = selected_applicable;
                in conditions_supported_in = conditions_supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
        part source_checks {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. */
            assert constraint flow_ok : 'Loop Capacity' { in mdot_loop_in = primary_loop.mdot_loop; in mdot_loop_rated_in = primary_loop.mdot_loop_rated; }
            assert constraint pressure_ok : 'Loop Pressure Margin' { in p_loop_margin_in = primary_loop.p_loop_margin; }
        }
        part salt_capital {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. salt_capital owns its selected inputs and exposed calculation outputs. */
            attribute amount8 : Real = 0;
            calc evaluate : 'Eight Amount Sum' {
                in amount1_in = steam_transport.hx_purchase;
                in amount2_in = steam_transport.hx_installation;
                in amount3_in = steam_transport.secondary_vendor;
                in amount4_in = steam_transport.secondary_installation;
                in amount5_in = steam_transport.secondary_pipe_purchase;
                in amount6_in = steam_transport.secondary_pipe_installation;
                in amount7_in = steam_transport.secondary_spare;
                in amount8_in = amount8;
            }
            attribute total : Real = evaluate.total;
        }
        part bundle_sum {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. bundle_sum owns its selected inputs and exposed calculation outputs. */
            attribute amount4 : Real = 0;
            attribute amount5 : Real = 0;
            attribute amount6 : Real = 0;
            attribute amount7 : Real = 0;
            attribute amount8 : Real = 0;
            calc evaluate : 'Eight Amount Sum' {
                in amount1_in = steam_transport.bundle_event_purchase;
                in amount2_in = steam_transport.bundle_event_installation;
                in amount3_in = steam_transport.bundle_event_removal;
                in amount4_in = amount4;
                in amount5_in = amount5;
                in amount6_in = amount6;
                in amount7_in = amount7;
                in amount8_in = amount8;
            }
            attribute total : Real = evaluate.total;
        }
        part salt_replaced_capital {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. salt_replaced_capital owns its selected inputs and exposed calculation outputs. */
            attribute amount5 : Real = 0;
            attribute amount6 : Real = 0;
            attribute amount7 : Real = 0;
            attribute amount8 : Real = 0;
            calc evaluate : 'Eight Amount Sum' {
                in amount1_in = steam_transport.secondary_vendor;
                in amount2_in = steam_transport.secondary_installation;
                in amount3_in = steam_transport.bundle_event_purchase;
                in amount4_in = steam_transport.bundle_event_installation;
                in amount5_in = amount5;
                in amount6_in = amount6;
                in amount7_in = amount7;
                in amount8_in = amount8;
            }
            attribute total : Real = evaluate.total;
        }
        part steam_ledger {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. steam_ledger owns its selected inputs and exposed calculation outputs. */
            attribute shaft_import : Real = 0.0;
            attribute water2 : Real = 0.0;
            attribute water3 : Real = 0.0;
            attribute water4 : Real = 0.0;
            attribute rejected2 : Real = 0.0;
            attribute rejected3 : Real = 0.0;
            attribute rejected4 : Real = 0.0;
            attribute capital3 : Real = 247464428.83859593;
            attribute capital4 : Real = 115939531.80564217;
            attribute capital5 : Real = 0.0;
            attribute capital6 : Real = 0.0;
            attribute capital7 : Real = 0.0;
            attribute capital8 : Real = 0.0;
            attribute capital9 : Real = 0.0;
            attribute capital10 : Real = 0.0;
            attribute currency_factor : Real = 1.0;
            attribute controller_capital : Real = 10000000.0;
            attribute machine_life : Real = 10.0;
            attribute bundle_life : Real = 15.0;
            attribute makeup_fraction : Real = 0.001;
            attribute annual_service_fraction : Real = 0.02;
            attribute replacement_fraction : Real = 0.2;
            attribute replacement_year : Real = 15.0;
            attribute rate : Real = 0.05;
            attribute years : Real = 30.0;
            attribute availability : Real = 0.85;
            attribute scope_correction : Real = 0.0;
            attribute common_source_pv : Real = 0.0;
            calc evaluate : 'Conversion Subsystem Ledger' {
                in available_heat_in = primary_loop.q_ihx;
                in actual_heat_in = steam_boundary.actual_heat;
                in gross_in = steam_cycle.p_gross_MW;
                in shaft_import_in = shaft_import;
                in steam_pumps_in = steam_cycle.p_cycle_pumps_MW;
                in salt_pumps_in = steam_transport.salt_electric_MW;
                in water1_in = steam_water.p_cooling_pump_electric_MW;
                in water2_in = water2;
                in water3_in = water3;
                in water4_in = water4;
                in controller_electric_in = steam_boundary.actuation;
                in rejected1_in = steam_water.q_total_rejection_MW;
                in rejected2_in = rejected2;
                in rejected3_in = rejected3;
                in rejected4_in = rejected4;
                in capital1_in = salt_capital.total;
                in capital2_in = steam_transport.salt_inventory_cost;
                in capital3_in = capital3;
                in capital4_in = capital4;
                in capital5_in = capital5;
                in capital6_in = capital6;
                in capital7_in = capital7;
                in capital8_in = capital8;
                in capital9_in = capital9;
                in capital10_in = capital10;
                in currency_factor_in = currency_factor;
                in controller_capital_in = controller_capital;
                in separately_replaced_capital_in = salt_replaced_capital.total;
                in salt_vendor_in = steam_transport.salt_machine_event_purchase;
                in salt_installation_in = steam_transport.salt_machine_event_installation;
                in salt_removal_in = steam_transport.salt_machine_event_removal;
                in bundle_event_in = bundle_sum.total;
                in salt_stock_cost_in = steam_transport.salt_inventory_cost;
                in machine_life_in = machine_life;
                in bundle_life_in = bundle_life;
                in makeup_fraction_in = makeup_fraction;
                in annual_service_fraction_in = annual_service_fraction;
                in replacement_fraction_in = replacement_fraction;
                in replacement_year_in = replacement_year;
                in rate_in = rate;
                in years_in = years;
                in availability_in = availability;
                in scope_correction_in = scope_correction;
                in common_source_pv_in = common_source_pv;
            }
            attribute gross_electric : Real = evaluate.gross_electric;
            attribute electrical_load : Real = evaluate.electrical_load;
            attribute net_electric : Real = evaluate.net_electric;
            attribute total_rejected : Real = evaluate.total_rejected;
            attribute unremoved_heat : Real = evaluate.unremoved_heat;
            attribute energy_residual : Real = evaluate.energy_residual;
            attribute conversion_energy_residual : Real = evaluate.conversion_energy_residual;
            attribute capital_total : Real = evaluate.capital_total;
            attribute recurring_base : Real = evaluate.recurring_base;
            attribute annual_service : Real = evaluate.annual_service;
            attribute annual_makeup : Real = evaluate.annual_makeup;
            attribute machine_replacement_pv : Real = evaluate.machine_replacement_pv;
            attribute bundle_replacement_pv : Real = evaluate.bundle_replacement_pv;
            attribute conversion_replacement_pv : Real = evaluate.conversion_replacement_pv;
            attribute replacement_pv : Real = evaluate.replacement_pv;
            attribute annuity_factor : Real = evaluate.annuity_factor;
            attribute annual_energy : Real = evaluate.annual_energy;
            attribute discounted_energy : Real = evaluate.discounted_energy;
            attribute accounted_pv : Real = evaluate.accounted_pv;
            attribute corrected_pv : Real = evaluate.corrected_pv;
            attribute cost_per_net_MWh : Real = evaluate.cost_per_net_MWh;
            attribute economic_defined : Real = evaluate.economic_defined;
            attribute energy_tolerance : Real = evaluate.energy_tolerance;
            attribute capital_1 : Real = evaluate.capital_1;
            attribute capital_2 : Real = evaluate.capital_2;
            attribute capital_3 : Real = evaluate.capital_3;
            attribute capital_4 : Real = evaluate.capital_4;
            attribute capital_5 : Real = evaluate.capital_5;
            attribute capital_6 : Real = evaluate.capital_6;
            attribute capital_7 : Real = evaluate.capital_7;
            attribute capital_8 : Real = evaluate.capital_8;
            attribute capital_9 : Real = evaluate.capital_9;
            attribute capital_10 : Real = evaluate.capital_10;
            assert constraint net_positive : 'Net Power Positive' {
                in net_electric = evaluate.net_electric;
            }
            assert constraint balance : 'Numerical Residual' {
                in residual_in = conversion_energy_residual;
                in tolerance_in = energy_tolerance;
            }
        }
        part gas_ledger {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. gas_ledger owns its selected inputs and exposed calculation outputs. */
            attribute steam_pumps : Real = 0.0;
            attribute salt_pumps : Real = 0.0;
            attribute capital1 : Real = 0.0;
            attribute capital2 : Real = 0.0;
            attribute capital9 : Real = 85933000;
            attribute currency_factor : Real = 1.7040762308099522;
            attribute controller_capital : Real = 10000000.0;
            attribute separately_replaced_capital : Real = 0.0;
            attribute salt_vendor : Real = 0.0;
            attribute salt_installation : Real = 0.0;
            attribute salt_removal : Real = 0.0;
            attribute bundle_event : Real = 0.0;
            attribute salt_stock_cost : Real = 0.0;
            attribute machine_life : Real = 10.0;
            attribute bundle_life : Real = 15.0;
            attribute makeup_fraction : Real = 0.001;
            attribute annual_service_fraction : Real = 0.02;
            attribute replacement_fraction : Real = 0.2;
            attribute replacement_year : Real = 15.0;
            attribute rate : Real = 0.05;
            attribute years : Real = 30.0;
            attribute availability : Real = 0.85;
            attribute scope_correction : Real = 0.0;
            attribute common_source_pv : Real = 0.0;
            calc evaluate : 'Conversion Subsystem Ledger' {
                in available_heat_in = primary_loop.q_ihx;
                in actual_heat_in = heat_exchangers.accepted_heat;
                in gross_in = electrical.gross_electric;
                in shaft_import_in = electrical.shaft_import;
                in steam_pumps_in = steam_pumps;
                in salt_pumps_in = salt_pumps;
                in water1_in = water_ic1.pump_electric;
                in water2_in = water_ic2.pump_electric;
                in water3_in = water_pre.pump_electric;
                in water4_in = gas_loss_water.p_cooling_pump_electric_MW;
                in controller_electric_in = gas_boundary.actuation;
                in rejected1_in = water_ic1.total_rejection;
                in rejected2_in = water_ic2.total_rejection;
                in rejected3_in = water_pre.total_rejection;
                in rejected4_in = gas_loss_water.q_total_rejection_MW;
                in capital1_in = capital1;
                in capital2_in = capital2;
                in capital3_in = compressor_equipment.estimated_cost;
                in capital4_in = turbine_equipment.estimated_cost;
                in capital5_in = generator_equipment.estimated_cost;
                in capital6_in = he_hx.estimated_cost;
                in capital7_in = he_duty_equipment.estimated_cost;
                in capital8_in = conversion_services.estimated_cost;
                in capital9_in = capital9;
                in capital10_in = heat_rejection_equipment.estimated_cost;
                in currency_factor_in = currency_factor;
                in controller_capital_in = controller_capital;
                in separately_replaced_capital_in = separately_replaced_capital;
                in salt_vendor_in = salt_vendor;
                in salt_installation_in = salt_installation;
                in salt_removal_in = salt_removal;
                in bundle_event_in = bundle_event;
                in salt_stock_cost_in = salt_stock_cost;
                in machine_life_in = machine_life;
                in bundle_life_in = bundle_life;
                in makeup_fraction_in = makeup_fraction;
                in annual_service_fraction_in = annual_service_fraction;
                in replacement_fraction_in = replacement_fraction;
                in replacement_year_in = replacement_year;
                in rate_in = rate;
                in years_in = years;
                in availability_in = availability;
                in scope_correction_in = scope_correction;
                in common_source_pv_in = common_source_pv;
            }
            attribute gross_electric : Real = evaluate.gross_electric;
            attribute electrical_load : Real = evaluate.electrical_load;
            attribute net_electric : Real = evaluate.net_electric;
            attribute total_rejected : Real = evaluate.total_rejected;
            attribute unremoved_heat : Real = evaluate.unremoved_heat;
            attribute energy_residual : Real = evaluate.energy_residual;
            attribute conversion_energy_residual : Real = evaluate.conversion_energy_residual;
            attribute capital_total : Real = evaluate.capital_total;
            attribute recurring_base : Real = evaluate.recurring_base;
            attribute annual_service : Real = evaluate.annual_service;
            attribute annual_makeup : Real = evaluate.annual_makeup;
            attribute machine_replacement_pv : Real = evaluate.machine_replacement_pv;
            attribute bundle_replacement_pv : Real = evaluate.bundle_replacement_pv;
            attribute conversion_replacement_pv : Real = evaluate.conversion_replacement_pv;
            attribute replacement_pv : Real = evaluate.replacement_pv;
            attribute annuity_factor : Real = evaluate.annuity_factor;
            attribute annual_energy : Real = evaluate.annual_energy;
            attribute discounted_energy : Real = evaluate.discounted_energy;
            attribute accounted_pv : Real = evaluate.accounted_pv;
            attribute corrected_pv : Real = evaluate.corrected_pv;
            attribute cost_per_net_MWh : Real = evaluate.cost_per_net_MWh;
            attribute economic_defined : Real = evaluate.economic_defined;
            attribute energy_tolerance : Real = evaluate.energy_tolerance;
            attribute capital_1 : Real = evaluate.capital_1;
            attribute capital_2 : Real = evaluate.capital_2;
            attribute capital_3 : Real = evaluate.capital_3;
            attribute capital_4 : Real = evaluate.capital_4;
            attribute capital_5 : Real = evaluate.capital_5;
            attribute capital_6 : Real = evaluate.capital_6;
            attribute capital_7 : Real = evaluate.capital_7;
            attribute capital_8 : Real = evaluate.capital_8;
            attribute capital_9 : Real = evaluate.capital_9;
            attribute capital_10 : Real = evaluate.capital_10;
            assert constraint net_positive : 'Net Power Positive' {
                in net_electric = evaluate.net_electric;
            }
            assert constraint balance : 'Numerical Residual' {
                in residual_in = conversion_energy_residual;
                in tolerance_in = energy_tolerance;
            }
        }
        part rejection_capacity {
            doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. rejection_capacity owns its selected inputs and exposed calculation outputs. */
            attribute selected_rating : Real = 5000;
            attribute selected_applicable : Boolean = true;
            attribute conditions_supported : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = selected_rating;
                in demand_in = gas_ledger.total_rejected;
                in applicable_in = selected_applicable;
                in conditions_supported_in = conditions_supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute applicable : Boolean = evaluate.applicable;
            attribute supported : Boolean = evaluate.supported;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            attribute capacity_ok : Boolean = evaluate.capacity_ok;
            assert constraint capacity_requirement : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
    }
}
