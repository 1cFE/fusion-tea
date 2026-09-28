package whole_plant_conversion {
    doc /* **Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. */
    private import ScalarValues::*;
    private import whole_plant_conversion_accounts::*;
    private import mfe_fuel_cycle::*;
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
            attribute q_source : Real = source_basis.q_source_MW;
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
                in q_source_in = source_basis.q_source_MW;
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
            assert constraint main_ua_available_required : 'Offered Equipment Capacity' {
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
            assert constraint reheat_ua_available_required : 'Offered Equipment Capacity' {
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
            attribute rate : Real = finance.rate;
            attribute years : Real = finance.years;
            attribute availability : Real = finance.availability;
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
            attribute conversion_energy_residual_magnitude : Real = evaluate.conversion_energy_residual_magnitude;
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
                in residual_in = conversion_energy_residual_magnitude;
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
            attribute rate : Real = finance.rate;
            attribute years : Real = finance.years;
            attribute availability : Real = finance.availability;
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
            attribute conversion_energy_residual_magnitude : Real = evaluate.conversion_energy_residual_magnitude;
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
                in residual_in = conversion_energy_residual_magnitude;
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
        part finance {
            attribute rate : Real = 0.05;
            attribute years : Real = 30.0;
            attribute availability : Real = 0.8;
            attribute construction_years : Real = 8.0;
            attribute contingency_rate : Real = 0.1;
            attribute indirect_rate : Real = 0.2;
            attribute freight_rate : Real = 0.015;
            attribute general_spares_rate : Real = 0.02;
            attribute tax_rate : Real = 0.01;
            attribute insurance_rate : Real = 0.015;
            attribute commissioning_rate : Real = 0.005;
        }
        part source_basis {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. */
            attribute q_source_MW : Real = 2500.0;
            attribute deposited_heating_MW : Real = 50.0;
            attribute neutron_multiplier : Real = 1.2;
            attribute heating_source_efficiency : Real = 0.5;
            attribute heating_coupling_efficiency : Real = 1.0;
            attribute heating_coupled_rating : Real = 50.0;
            attribute heating_wall_rating : Real = 100.0;
            attribute fusion_envelope_MW : Real = 2652.5632625175904;
            attribute wall_reference : Real = 3.9788448937763854;
            attribute wall_fusion_reference : Real = 2652.5632625175904;
            attribute divertor_limit : Real = 10.0;
            attribute alpha_proxy : Real = 0.2002;
            attribute alpha_retention : Real = 0.95;
            attribute radiation_fraction : Real = 0.9;
            attribute divertor_peaking : Real = 9.5;
            attribute divertor_area : Real = 50.0;
            calc evaluate : 'Supplied Source Basis' {
                in q_source_MW_in = q_source_MW;
                in deposited_heating_MW_in = deposited_heating_MW;
                in neutron_multiplier_in = neutron_multiplier;
                in heating_source_efficiency_in = heating_source_efficiency;
                in heating_coupling_efficiency_in = heating_coupling_efficiency;
                in heating_coupled_rating_in = heating_coupled_rating;
                in heating_wall_rating_in = heating_wall_rating;
                in fusion_envelope_MW_in = fusion_envelope_MW;
                in wall_reference_in = wall_reference;
                in wall_fusion_reference_in = wall_fusion_reference;
                in divertor_limit_in = divertor_limit;
                in alpha_proxy_in = alpha_proxy;
                in alpha_retention_in = alpha_retention;
                in radiation_fraction_in = radiation_fraction;
                in divertor_peaking_in = divertor_peaking;
                in divertor_area_in = divertor_area;
            }
            attribute fusion_MW : Real = evaluate.fusion_MW;
            attribute reconstructed_source_MW : Real = evaluate.reconstructed_source_MW;
            attribute source_residual : Real = evaluate.source_residual;
            attribute source_qualified : Real = evaluate.source_qualified;
            attribute heating_wall_MW : Real = evaluate.heating_wall_MW;
            attribute heating_loss_MW : Real = evaluate.heating_loss_MW;
            attribute heating_coupled_margin : Real = evaluate.heating_coupled_margin;
            attribute heating_wall_margin : Real = evaluate.heating_wall_margin;
            attribute wall_load : Real = evaluate.wall_load;
            attribute divertor_load : Real = evaluate.divertor_load;
            attribute divertor_margin : Real = evaluate.divertor_margin;
            attribute fusion_envelope_margin : Real = evaluate.fusion_envelope_margin;
            attribute domain_supported : Real = evaluate.domain_supported;
            assert constraint heating_coupled_margin_ok : 'Whole Plant Nonnegative' { in metric_in = heating_coupled_margin; }
            assert constraint heating_wall_margin_ok : 'Whole Plant Nonnegative' { in metric_in = heating_wall_margin; }
            assert constraint divertor_margin_ok : 'Whole Plant Nonnegative' { in metric_in = divertor_margin; }
            assert constraint fusion_envelope_margin_ok : 'Whole Plant Nonnegative' { in metric_in = fusion_envelope_margin; }
            assert constraint domain_supported_ok : 'Whole Plant Supported' { in metric_in = domain_supported; }
        }
        part cryogenic_offer {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Independently selected capacities and installed quote; immutable capture remains reference evidence. */
            attribute cold_rating_W : Real = 40000.0;
            attribute intercept_rating_W : Real = 60000.0;
            attribute quote_USD2025 : Real = 62957384.24217385;
        }
        part supplied_core {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. */
            attribute capture_id : Real = 48001.0;
            calc evaluate : 'Captured Reactor Offer' {
                in capture_id_in = capture_id;
            }
            attribute magnet_capital : Real = evaluate.magnet_capital;
            attribute tape_cost : Real = evaluate.tape_cost;
            attribute material_cost : Real = evaluate.material_cost;
            attribute insulation_cost : Real = evaluate.insulation_cost;
            attribute winding_cost : Real = evaluate.winding_cost;
            attribute support_cost : Real = evaluate.support_cost;
            attribute coil_drive_MW : Real = evaluate.coil_drive_MW;
            attribute refrigeration_MW : Real = evaluate.refrigeration_MW;
            attribute cold_W : Real = evaluate.cold_W;
            attribute intercept_W : Real = evaluate.intercept_W;
            attribute fit_margin : Real = evaluate.fit_margin;
            attribute current_margin : Real = evaluate.current_margin;
            attribute peak_field : Real = evaluate.peak_field;
            attribute strain : Real = evaluate.strain;
            attribute stress_Pa : Real = evaluate.stress_Pa;
            attribute field_extrapolated : Real = evaluate.field_extrapolated;
            attribute cold_rating_W : Real = evaluate.cold_rating_W;
            attribute intercept_rating_W : Real = evaluate.intercept_rating_W;
            attribute axis_field : Real = evaluate.axis_field;
            attribute turn_current_A : Real = evaluate.turn_current_A;
            attribute nuclear_heating_W_m3 : Real = evaluate.nuclear_heating_W_m3;
            attribute nuclear_transport_qualified : Real = evaluate.nuclear_transport_qualified;
            attribute global_construction_qualified : Real = evaluate.global_construction_qualified;
            attribute cold_volume_m3 : Real = evaluate.cold_volume_m3;
            attribute inventory_cold_W : Real = evaluate.inventory_cold_W;
            attribute fixed_cold_MW : Real = evaluate.fixed_cold_MW;
            attribute intercept_inventory_W : Real = evaluate.intercept_inventory_W;
            attribute cold_temperature_K : Real = evaluate.cold_temperature_K;
            attribute intercept_temperature_K : Real = evaluate.intercept_temperature_K;
            attribute ambient_temperature_K : Real = evaluate.ambient_temperature_K;
            attribute cold_carnot_fraction : Real = evaluate.cold_carnot_fraction;
            attribute intercept_carnot_fraction : Real = evaluate.intercept_carnot_fraction;
            attribute cold_margin_W : Real = evaluate.cold_margin_W;
            attribute intercept_margin_W : Real = evaluate.intercept_margin_W;
            attribute field_margin_T : Real = evaluate.field_margin_T;
            attribute strain_margin : Real = evaluate.strain_margin;
            attribute stress_margin_Pa : Real = evaluate.stress_margin_Pa;
            attribute identity_supported : Real = evaluate.identity_supported;
            assert constraint fit_margin_ok : 'Whole Plant Nonnegative' { in metric_in = fit_margin; }
            assert constraint current_margin_ok : 'Whole Plant Nonnegative' { in metric_in = current_margin; }
            assert constraint field_margin_t_ok : 'Whole Plant Nonnegative' { in metric_in = field_margin_T; }
            assert constraint strain_margin_ok : 'Whole Plant Nonnegative' { in metric_in = strain_margin; }
            assert constraint stress_margin_pa_ok : 'Whole Plant Nonnegative' { in metric_in = stress_margin_Pa; }
            assert constraint identity_supported_ok : 'Whole Plant Supported' { in metric_in = identity_supported; }
        }
        part cryogenic_demand {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. */
            attribute q_nuc_W_m3 : Real = 35.5;
            attribute extra_cold_W : Real = 0.0;
            calc evaluate : 'Conditional Cryogenic Demand' {
                in q_nuc_W_m3_in = q_nuc_W_m3;
                in extra_cold_W_in = extra_cold_W;
                in cold_volume_m3_in = supplied_core.cold_volume_m3;
                in inventory_cold_W_in = supplied_core.inventory_cold_W;
                in fixed_cold_MW_in = supplied_core.fixed_cold_MW;
                in intercept_inventory_W_in = supplied_core.intercept_inventory_W;
                in cold_temperature_K_in = supplied_core.cold_temperature_K;
                in intercept_temperature_K_in = supplied_core.intercept_temperature_K;
                in ambient_temperature_K_in = supplied_core.ambient_temperature_K;
                in cold_carnot_fraction_in = supplied_core.cold_carnot_fraction;
                in intercept_carnot_fraction_in = supplied_core.intercept_carnot_fraction;
                in cold_rating_W_in = cryogenic_offer.cold_rating_W;
                in intercept_rating_W_in = cryogenic_offer.intercept_rating_W;
            }
            attribute cold_W : Real = evaluate.cold_W;
            attribute intercept_W : Real = evaluate.intercept_W;
            attribute cold_electric_MW : Real = evaluate.cold_electric_MW;
            attribute intercept_electric_MW : Real = evaluate.intercept_electric_MW;
            attribute refrigeration_MW : Real = evaluate.refrigeration_MW;
            attribute cold_margin_W : Real = evaluate.cold_margin_W;
            attribute intercept_margin_W : Real = evaluate.intercept_margin_W;
            attribute q_nuc_capacity_W_m3 : Real = evaluate.q_nuc_capacity_W_m3;
            attribute extra_cold_capacity_W : Real = evaluate.extra_cold_capacity_W;
            attribute nuclear_transport_qualified : Real = evaluate.nuclear_transport_qualified;
            attribute domain_supported : Real = evaluate.domain_supported;
            assert constraint cold_margin_w_ok : 'Whole Plant Nonnegative' { in metric_in = cold_margin_W; }
            assert constraint intercept_margin_w_ok : 'Whole Plant Nonnegative' { in metric_in = intercept_margin_W; }
            assert constraint domain_supported_ok : 'Whole Plant Supported' { in metric_in = domain_supported; }
        }
        part fuel_accounts {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. */
            attribute burn_fraction : Real = 0.05;
            attribute recycle : Real = 0.99;
            attribute tbr : Real = 1.1980739195540366;
            attribute extraction : Real = 1.0;
            attribute stock_kg : Real = 5.0;
            attribute processing_capacity_kg_s : Real = 0.00015;
            attribute decay : Real = 1.782785958230312e-09;
            attribute seconds_year : Real = 31536000.0;
            attribute m_T : Real = 5.008267663228036e-27;
            attribute m_D : Real = 3.3435837768e-27;
            attribute m_Li6 : Real = 9.988346405448768e-27;
            attribute q_eff : Real = 17.58;
            attribute MeV_J : Real = 1.602176634e-13;
            attribute tritium_price : Real = 51122286.92429857;
            attribute deuterium_price : Real = 2175.0;
            attribute li6_price : Real = 1000.0;
            calc evaluate : 'Fuel Supply Accounts' {
                in fusion_MW_in = source_basis.fusion_MW;
                in availability_in = finance.availability;
                in burn_fraction_in = burn_fraction;
                in recycle_in = recycle;
                in tbr_in = tbr;
                in extraction_in = extraction;
                in stock_kg_in = stock_kg;
                in startup_required_kg_in = fuel_inventory.startup_conservative_kg;
                in processing_capacity_kg_s_in = processing_capacity_kg_s;
                in decay_in = decay;
                in seconds_year_in = seconds_year;
                in m_T_in = m_T;
                in m_D_in = m_D;
                in m_Li6_in = m_Li6;
                in q_eff_in = q_eff;
                in MeV_J_in = MeV_J;
                in tritium_price_in = tritium_price;
                in deuterium_price_in = deuterium_price;
                in li6_price_in = li6_price;
            }
            attribute reaction_rate : Real = evaluate.reaction_rate;
            attribute burn_kg_s : Real = evaluate.burn_kg_s;
            attribute loss_kg_s : Real = evaluate.loss_kg_s;
            attribute processing_kg_s : Real = evaluate.processing_kg_s;
            attribute stock_margin : Real = evaluate.stock_margin;
            attribute processing_margin : Real = evaluate.processing_margin;
            attribute annual_T_need : Real = evaluate.annual_T_need;
            attribute annual_T_bred : Real = evaluate.annual_T_bred;
            attribute annual_T_external : Real = evaluate.annual_T_external;
            attribute annual_T_surplus : Real = evaluate.annual_T_surplus;
            attribute annual_D_kg : Real = evaluate.annual_D_kg;
            attribute annual_Li6_kg : Real = evaluate.annual_Li6_kg;
            attribute annual_T_cost : Real = evaluate.annual_T_cost;
            attribute annual_D_cost : Real = evaluate.annual_D_cost;
            attribute annual_Li6_cost : Real = evaluate.annual_Li6_cost;
            attribute annual_fuel : Real = evaluate.annual_fuel;
            attribute initial_T_cost : Real = evaluate.initial_T_cost;
            attribute self_sufficiency_margin : Real = evaluate.self_sufficiency_margin;
            attribute D_atom_residual : Real = evaluate.D_atom_residual;
            attribute T_atom_residual : Real = evaluate.T_atom_residual;
            attribute Li6_atom_residual : Real = evaluate.Li6_atom_residual;
            attribute domain_supported : Real = evaluate.domain_supported;
            assert constraint stock_margin_ok : 'Whole Plant Nonnegative' { in metric_in = stock_margin; }
            assert constraint processing_margin_ok : 'Whole Plant Nonnegative' { in metric_in = processing_margin; }
            assert constraint domain_supported_ok : 'Whole Plant Supported' { in metric_in = domain_supported; }
        }
        part fuel_inventory {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. */
            attribute enabled : Boolean = true;
            attribute held_inventory : Real = 0.0;
            attribute breeding_defined : Real = 1.0;
            attribute G_stock : Real = 0.0;
            attribute plasma_volume : Real = 425.0000143721807;
            attribute n_T0 : Real = 1.9256443867349644e+20;
            attribute alpha_n : Real = 0.33;
            attribute tau_feed : Real = 1200.0;
            attribute tau_process : Real = 14400.0;
            attribute tau_blanket : Real = 86400.0;
            attribute tau_extract : Real = 86400.0;
            attribute tau_buffer : Real = 0.0;
            attribute tau_reserve : Real = 86400.0;
            attribute startup_extension : Real = 0.0;
            attribute shutdown_duration : Real = 86400.0;
            attribute reserve_fraction : Real = 0.25;
            calc evaluate : 'Fuel Inventory' {
                in enabled_in = enabled;
                in held_inventory_in = held_inventory;
                in p_fus_in = source_basis.fusion_MW;
                in q_eff_in = fuel_accounts.q_eff;
                in mev_to_joules_in = fuel_accounts.MeV_J;
                in burn_fraction_in = fuel_accounts.burn_fraction;
                in t_recycle_in = fuel_accounts.recycle;
                in tbr_available_in = fuel_accounts.tbr;
                in breeding_defined_in = breeding_defined;
                in eta_extract_in = fuel_accounts.extraction;
                in lambda_T_in = fuel_accounts.decay;
                in G_stock_in = G_stock;
                in m_T_kg_in = fuel_accounts.m_T;
                in m_D_kg_in = fuel_accounts.m_D;
                in plasma_volume_in = plasma_volume;
                in n_T0_in = n_T0;
                in alpha_n_in = alpha_n;
                in tau_feed_in = tau_feed;
                in tau_process_in = tau_process;
                in tau_blanket_in = tau_blanket;
                in tau_extract_in = tau_extract;
                in tau_buffer_in = tau_buffer;
                in tau_reserve_in = tau_reserve;
                in startup_extension_in = startup_extension;
                in shutdown_duration_in = shutdown_duration;
                in reserve_fraction_in = reserve_fraction;
                in availability_in = finance.availability;
                in s_per_year_in = fuel_accounts.seconds_year;
            }
            attribute feed_atoms : Real = evaluate.feed_atoms;
            attribute feed_kg : Real = evaluate.feed_kg;
            attribute plasma_atoms : Real = evaluate.plasma_atoms;
            attribute plasma_kg : Real = evaluate.plasma_kg;
            attribute processor_atoms : Real = evaluate.processor_atoms;
            attribute processor_kg : Real = evaluate.processor_kg;
            attribute blanket_atoms : Real = evaluate.blanket_atoms;
            attribute blanket_kg : Real = evaluate.blanket_kg;
            attribute extraction_atoms : Real = evaluate.extraction_atoms;
            attribute extraction_kg : Real = evaluate.extraction_kg;
            attribute buffer_atoms : Real = evaluate.buffer_atoms;
            attribute buffer_kg : Real = evaluate.buffer_kg;
            attribute reserve_atoms : Real = evaluate.reserve_atoms;
            attribute reserve_kg : Real = evaluate.reserve_kg;
            attribute working_atoms : Real = evaluate.working_atoms;
            attribute working_kg : Real = evaluate.working_kg;
            attribute total_atoms : Real = evaluate.total_atoms;
            attribute total_kg : Real = evaluate.total_kg;
            attribute prefill_atoms : Real = evaluate.prefill_atoms;
            attribute prefill_kg : Real = evaluate.prefill_kg;
            attribute startup_deficit_atoms : Real = evaluate.startup_deficit_atoms;
            attribute startup_deficit_kg : Real = evaluate.startup_deficit_kg;
            attribute startup_minimum_atoms : Real = evaluate.startup_minimum_atoms;
            attribute startup_minimum_kg : Real = evaluate.startup_minimum_kg;
            attribute startup_decay_allowance_atoms : Real = evaluate.startup_decay_allowance_atoms;
            attribute startup_decay_allowance_kg : Real = evaluate.startup_decay_allowance_kg;
            attribute startup_conservative_atoms : Real = evaluate.startup_conservative_atoms;
            attribute startup_conservative_kg : Real = evaluate.startup_conservative_kg;
            attribute recycle_delay_s : Real = evaluate.recycle_delay_s;
            attribute breeding_delay_s : Real = evaluate.breeding_delay_s;
            attribute startup_horizon_s : Real = evaluate.startup_horizon_s;
            attribute max_decay_residence : Real = evaluate.max_decay_residence;
            attribute burn_kg_s : Real = evaluate.burn_kg_s;
            attribute burn_kg_day : Real = evaluate.burn_kg_day;
            attribute annual_burn_kg : Real = evaluate.annual_burn_kg;
            attribute injection_kg_s : Real = evaluate.injection_kg_s;
            attribute injection_kg_day : Real = evaluate.injection_kg_day;
            attribute annual_injection_kg : Real = evaluate.annual_injection_kg;
            attribute exhaust_kg_s : Real = evaluate.exhaust_kg_s;
            attribute exhaust_kg_day : Real = evaluate.exhaust_kg_day;
            attribute annual_exhaust_kg : Real = evaluate.annual_exhaust_kg;
            attribute recycle_kg_s : Real = evaluate.recycle_kg_s;
            attribute recycle_kg_day : Real = evaluate.recycle_kg_day;
            attribute annual_recycle_kg : Real = evaluate.annual_recycle_kg;
            attribute production_kg_s : Real = evaluate.production_kg_s;
            attribute production_kg_day : Real = evaluate.production_kg_day;
            attribute annual_production_kg : Real = evaluate.annual_production_kg;
            attribute extracted_kg_s : Real = evaluate.extracted_kg_s;
            attribute extracted_kg_day : Real = evaluate.extracted_kg_day;
            attribute annual_extracted_kg : Real = evaluate.annual_extracted_kg;
            attribute recycle_loss_kg_s : Real = evaluate.recycle_loss_kg_s;
            attribute recycle_loss_kg_day : Real = evaluate.recycle_loss_kg_day;
            attribute annual_recycle_loss_kg : Real = evaluate.annual_recycle_loss_kg;
            attribute extraction_loss_kg_s : Real = evaluate.extraction_loss_kg_s;
            attribute extraction_loss_kg_day : Real = evaluate.extraction_loss_kg_day;
            attribute annual_extraction_loss_kg : Real = evaluate.annual_extraction_loss_kg;
            attribute dt_injection_kg_s : Real = evaluate.dt_injection_kg_s;
            attribute dt_injection_kg_day : Real = evaluate.dt_injection_kg_day;
            attribute dt_processor_kg_s : Real = evaluate.dt_processor_kg_s;
            attribute dt_processor_kg_day : Real = evaluate.dt_processor_kg_day;
            attribute decay_kg_s : Real = evaluate.decay_kg_s;
            attribute makeup_signed_kg_s : Real = evaluate.makeup_signed_kg_s;
            attribute external_shortfall_kg_s : Real = evaluate.external_shortfall_kg_s;
            attribute calendar_processor_kg_s : Real = evaluate.calendar_processor_kg_s;
            attribute annual_decay_kg : Real = evaluate.annual_decay_kg;
            attribute annual_makeup_signed_kg : Real = evaluate.annual_makeup_signed_kg;
            attribute annual_external_shortfall_kg : Real = evaluate.annual_external_shortfall_kg;
            attribute shutdown_remaining_kg : Real = evaluate.shutdown_remaining_kg;
            attribute shutdown_decay_loss_kg : Real = evaluate.shutdown_decay_loss_kg;
            attribute defined_flag : Real = evaluate.defined_flag;
        }
        part fuel_flows {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. */
            attribute G_stock : Real = 0.0;
            calc evaluate : 'Fuel Cycle Flows' {
                in p_fus_in = source_basis.fusion_MW;
                in q_eff_in = fuel_accounts.q_eff;
                in mev_to_joules_in = fuel_accounts.MeV_J;
                in burn_fraction_in = fuel_accounts.burn_fraction;
                in t_recycle_in = fuel_accounts.recycle;
                in tbr_available_in = fuel_accounts.tbr;
                in eta_extract_in = fuel_accounts.extraction;
                in lambda_T_in = fuel_accounts.decay;
                in I_total_in = fuel_inventory.total_atoms;
                in G_stock_in = G_stock;
                in m_T_kg_in = fuel_accounts.m_T;
                in s_per_fpy_in = fuel_accounts.seconds_year;
            }
            attribute burn_rate : Real = evaluate.burn_rate;
            attribute inject_rate : Real = evaluate.inject_rate;
            attribute exhaust_rate : Real = evaluate.exhaust_rate;
            attribute loss_rate : Real = evaluate.loss_rate;
            attribute tbr_required : Real = evaluate.tbr_required;
            attribute tbr_margin : Real = evaluate.tbr_margin;
            attribute burn_kg_per_fpy : Real = evaluate.burn_kg_per_fpy;
        }
        part land_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 16901536.908759248;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part facilities_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 799758795.94032;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part magnet_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = supplied_core.magnet_capital; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part heating_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 264145000.0;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part divertor_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 109109123.15593052;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part blanket_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 719155016.1966425;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part shield_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 452529516.99448603;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part structure_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 32373952.820015125;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part vessel_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 113317730.12762633;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part power_supplies_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 86013482.74180616;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part remote_handling_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 157969959.25281796;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part installation_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 509887983.2968712;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part primary_circulators_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 442174444.74911624;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part primary_pipes_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 2974043934.3757505;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part primary_spares_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 12020446.033021579;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part primary_helium_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 1409367.527367595;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part cryoplant_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = cryogenic_offer.quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part auxiliary_rejection_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 50000000.0;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part waste_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 6481502.633743829;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part fuel_processing_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 22811717.720117148;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part other_reactor_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 10098565.14458109;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part reactor_controls_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 81921417.18593018;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part shared_electrical_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 105407841.90324733;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part miscellaneous_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 64159703.76958075;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part pbl_initial_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 23815042.059888843;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part owner_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 37985982.20350555;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part digital_twin_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 5000000.0;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part source_installation_allowance_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute quote_USD2025 : Real = 200000000.0;
            attribute price_factor : Real = 1.0;
            calc purchase : 'Scaled Amount' { in amount_in = quote_USD2025; in factor_in = price_factor; }
            attribute cost : Real = purchase.amount;
            :>> capital_cost = purchase.amount;
        }
        part tritium_initial_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "22";
            attribute cost : Real = fuel_accounts.initial_T_cost;
            :>> capital_cost = fuel_accounts.initial_T_cost;
        }
        part steam_capital_1_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = steam_ledger.capital_1;
            :>> capital_cost = steam_ledger.capital_1;
        }
        part steam_capital_2_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = steam_ledger.capital_2;
            :>> capital_cost = steam_ledger.capital_2;
        }
        part steam_capital_3_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = steam_ledger.capital_3;
            :>> capital_cost = steam_ledger.capital_3;
        }
        part steam_capital_4_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = steam_ledger.capital_4;
            :>> capital_cost = steam_ledger.capital_4;
        }
        part steam_capital_5_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = steam_ledger.capital_5;
            :>> capital_cost = steam_ledger.capital_5;
        }
        part steam_capital_6_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = steam_ledger.capital_6;
            :>> capital_cost = steam_ledger.capital_6;
        }
        part steam_capital_7_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = steam_ledger.capital_7;
            :>> capital_cost = steam_ledger.capital_7;
        }
        part steam_capital_8_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = steam_ledger.capital_8;
            :>> capital_cost = steam_ledger.capital_8;
        }
        part steam_capital_9_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = steam_ledger.capital_9;
            :>> capital_cost = steam_ledger.capital_9;
        }
        part steam_capital_10_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = steam_ledger.capital_10;
            :>> capital_cost = steam_ledger.capital_10;
        }
        part steam_controller_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = steam_ledger.controller_capital;
            :>> capital_cost = steam_ledger.controller_capital;
        }
        part steam_overheads {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. */
            attribute steam_branch : Real = 1.0;
            calc evaluate : 'Whole Plant Capital Accounts' {
                in land_in = land_account.cost;
                in facilities_in = facilities_account.cost;
                in magnet_in = magnet_account.cost;
                in heating_in = heating_account.cost;
                in divertor_in = divertor_account.cost;
                in blanket_in = blanket_account.cost;
                in shield_in = shield_account.cost;
                in structure_in = structure_account.cost;
                in vessel_in = vessel_account.cost;
                in power_supplies_in = power_supplies_account.cost;
                in remote_handling_in = remote_handling_account.cost;
                in installation_in = installation_account.cost;
                in primary_circulators_in = primary_circulators_account.cost;
                in primary_pipes_in = primary_pipes_account.cost;
                in primary_spares_in = primary_spares_account.cost;
                in primary_helium_in = primary_helium_account.cost;
                in cryoplant_in = cryoplant_account.cost;
                in auxiliary_rejection_in = auxiliary_rejection_account.cost;
                in waste_in = waste_account.cost;
                in fuel_processing_in = fuel_processing_account.cost;
                in other_reactor_in = other_reactor_account.cost;
                in reactor_controls_in = reactor_controls_account.cost;
                in shared_electrical_in = shared_electrical_account.cost;
                in miscellaneous_in = miscellaneous_account.cost;
                in pbl_initial_in = pbl_initial_account.cost;
                in owner_in = owner_account.cost;
                in digital_twin_in = digital_twin_account.cost;
                in source_installation_allowance_in = source_installation_allowance_account.cost;
                in tritium_initial_in = tritium_initial_account.cost;
                in capital_1_in = steam_capital_1_account.cost;
                in capital_2_in = steam_capital_2_account.cost;
                in capital_3_in = steam_capital_3_account.cost;
                in capital_4_in = steam_capital_4_account.cost;
                in capital_5_in = steam_capital_5_account.cost;
                in capital_6_in = steam_capital_6_account.cost;
                in capital_7_in = steam_capital_7_account.cost;
                in capital_8_in = steam_capital_8_account.cost;
                in capital_9_in = steam_capital_9_account.cost;
                in capital_10_in = steam_capital_10_account.cost;
                in controller_capital_in = steam_controller_account.cost;
                in salt_spare_in = steam_transport.secondary_spare;
                in salt_vendor_in = steam_transport.secondary_vendor;
                in steam_branch_in = steam_branch;
                in contingency_rate_in = finance.contingency_rate;
                in indirect_rate_in = finance.indirect_rate;
                in freight_rate_in = finance.freight_rate;
                in general_spares_rate_in = finance.general_spares_rate;
                in tax_rate_in = finance.tax_rate;
                in insurance_rate_in = finance.insurance_rate;
                in commissioning_rate_in = finance.commissioning_rate;
                in construction_years_in = finance.construction_years;
            }
            attribute common_purchases : Real = evaluate.common_purchases;
            attribute branch_purchases : Real = evaluate.branch_purchases;
            attribute direct_base : Real = evaluate.direct_base;
            attribute equipment_base : Real = evaluate.equipment_base;
            attribute freight_base : Real = evaluate.freight_base;
            attribute general_spares_base : Real = evaluate.general_spares_base;
            attribute tax_base : Real = evaluate.tax_base;
            attribute insurance_base : Real = evaluate.insurance_base;
            attribute overhaul_base : Real = evaluate.overhaul_base;
            attribute salvage_base : Real = evaluate.salvage_base;
            attribute contingency : Real = evaluate.contingency;
            attribute indirect : Real = evaluate.indirect;
            attribute freight : Real = evaluate.freight;
            attribute general_spares : Real = evaluate.general_spares;
            attribute tax : Real = evaluate.tax;
            attribute insurance : Real = evaluate.insurance;
            attribute nonfuel_commissioning : Real = evaluate.nonfuel_commissioning;
            attribute cas20 : Real = evaluate.cas20;
            attribute cas30 : Real = evaluate.cas30;
            attribute cas50 : Real = evaluate.cas50;
            attribute initial_capital : Real = evaluate.initial_capital;
            attribute reconciliation_residual : Real = evaluate.reconciliation_residual;
            attribute domain_supported : Real = evaluate.domain_supported;
            assert constraint domain_supported_ok : 'Whole Plant Supported' { in metric_in = domain_supported; }
        }
        part steam_contingency_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "29";
            attribute cost : Real = steam_overheads.contingency;
            :>> capital_cost = steam_overheads.contingency;
        }
        part steam_indirect_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "30";
            attribute cost : Real = steam_overheads.indirect;
            :>> capital_cost = steam_overheads.indirect;
        }
        part steam_freight_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "50";
            attribute cost : Real = steam_overheads.freight;
            :>> capital_cost = steam_overheads.freight;
        }
        part steam_general_spares_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "50";
            attribute cost : Real = steam_overheads.general_spares;
            :>> capital_cost = steam_overheads.general_spares;
        }
        part steam_tax_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "50";
            attribute cost : Real = steam_overheads.tax;
            :>> capital_cost = steam_overheads.tax;
        }
        part steam_insurance_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "50";
            attribute cost : Real = steam_overheads.insurance;
            :>> capital_cost = steam_overheads.insurance;
        }
        part steam_nonfuel_commissioning_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "50";
            attribute cost : Real = steam_overheads.nonfuel_commissioning;
            :>> capital_cost = steam_overheads.nonfuel_commissioning;
        }
        part steam_operating {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. */
            attribute tf_cooling_MW : Real = 15.0;
            attribute pf_cooling_MW : Real = 0.0;
            attribute fuel_vacuum_MW : Real = 10.0;
            attribute house_MW : Real = 4.0;
            attribute reactor_controls_MW : Real = 36.5999451053;
            attribute residual_MW : Real = 5.0;
            attribute auxiliary_electric_MW : Real = 2.0;
            attribute auxiliary_rating_MW : Real = 200.0;
            attribute auxiliary_water_C : Real = 25.0;
            attribute import_price : Real = 50.0;
            calc evaluate : 'Whole Plant Operating Ledger' {
                in conversion_net_MW_in = steam_ledger.net_electric;
                in primary_electric_MW_in = primary_loop.p_elec;
                in primary_fluid_MW_in = primary_loop.w_fluid;
                in heating_wall_MW_in = source_basis.heating_wall_MW;
                in deposited_heating_MW_in = source_basis.deposited_heating_MW;
                in coil_drive_MW_in = supplied_core.coil_drive_MW;
                in refrigeration_MW_in = cryogenic_demand.refrigeration_MW;
                in cold_W_in = cryogenic_demand.cold_W;
                in intercept_W_in = cryogenic_demand.intercept_W;
                in tf_cooling_MW_in = tf_cooling_MW;
                in pf_cooling_MW_in = pf_cooling_MW;
                in fuel_vacuum_MW_in = fuel_vacuum_MW;
                in house_MW_in = house_MW;
                in reactor_controls_MW_in = reactor_controls_MW;
                in residual_MW_in = residual_MW;
                in auxiliary_electric_MW_in = auxiliary_electric_MW;
                in auxiliary_rating_MW_in = auxiliary_rating_MW;
                in auxiliary_water_C_in = auxiliary_water_C;
                in availability_in = finance.availability;
                in import_price_in = import_price;
            }
            attribute upstream_electric_MW : Real = evaluate.upstream_electric_MW;
            attribute net_export_MW : Real = evaluate.net_export_MW;
            attribute standby_MW : Real = evaluate.standby_MW;
            attribute annual_export_MWh : Real = evaluate.annual_export_MWh;
            attribute annual_import_MWh : Real = evaluate.annual_import_MWh;
            attribute annual_net_grid_MWh : Real = evaluate.annual_net_grid_MWh;
            attribute annual_import_cost : Real = evaluate.annual_import_cost;
            attribute auxiliary_heat_MW : Real = evaluate.auxiliary_heat_MW;
            attribute auxiliary_margin_MW : Real = evaluate.auxiliary_margin_MW;
            attribute primary_motor_loss_MW : Real = evaluate.primary_motor_loss_MW;
            attribute power_residual : Real = evaluate.power_residual;
            attribute domain_supported : Real = evaluate.domain_supported;
            assert constraint net_export_mw_ok : 'Whole Plant Positive' { in metric_in = net_export_MW; }
            assert constraint annual_net_grid_mwh_ok : 'Whole Plant Positive' { in metric_in = annual_net_grid_MWh; }
            assert constraint auxiliary_margin_mw_ok : 'Whole Plant Nonnegative' { in metric_in = auxiliary_margin_MW; }
            assert constraint domain_supported_ok : 'Whole Plant Supported' { in metric_in = domain_supported; }
        }
        part steam_whole {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. */
            attribute routine_om : Real = 50617243.27603046;
            attribute routine_fraction : Real = 0.8;
            attribute wall_life : Real = 18.0;
            attribute magnet_life : Real = 10.0;
            attribute blanket_outage : Real = 0.5833333333333334;
            attribute magnet_outage : Real = 1.0;
            attribute other_outage : Real = 0.5;
            attribute blanket_removal_fraction : Real = 0.1;
            attribute magnet_removal_fraction : Real = 0.1;
            attribute pbl_refill_fraction : Real = 1.0;
            attribute primary_event : Real = 546492750.26688;
            attribute primary_life : Real = 10.0;
            attribute helium_makeup_fraction : Real = 0.001;
            attribute overhaul_fraction : Real = 0.05;
            attribute overhaul_year : Real = 20.0;
            attribute dismantle_fraction : Real = 0.1;
            attribute salvage_fraction : Real = 0.02;
            calc evaluate : 'Whole Plant Lifecycle Ledger' {
                in initial_capital_in = steam_overheads.initial_capital;
                in salvage_base_in = steam_overheads.salvage_base;
                in overhaul_base_in = steam_overheads.overhaul_base;
                in magnet_capital_in = magnet_account.cost;
                in blanket_capital_in = blanket_account.cost;
                in divertor_capital_in = divertor_account.cost;
                in pbl_capital_in = pbl_initial_account.cost;
                in helium_capital_in = primary_helium_account.cost;
                in wall_load_in = source_basis.wall_load;
                in annual_export_MWh_in = steam_operating.annual_export_MWh;
                in annual_net_grid_MWh_in = steam_operating.annual_net_grid_MWh;
                in annual_import_cost_in = steam_operating.annual_import_cost;
                in annual_fuel_in = fuel_accounts.annual_fuel;
                in conversion_annual_service_in = steam_ledger.annual_service;
                in conversion_annual_makeup_in = steam_ledger.annual_makeup;
                in conversion_replacement_pv_in = steam_ledger.replacement_pv;
                in rate_in = finance.rate;
                in years_in = finance.years;
                in availability_in = finance.availability;
                in construction_years_in = finance.construction_years;
                in routine_om_in = routine_om;
                in routine_fraction_in = routine_fraction;
                in wall_life_in = wall_life;
                in magnet_life_in = magnet_life;
                in blanket_outage_in = blanket_outage;
                in magnet_outage_in = magnet_outage;
                in other_outage_in = other_outage;
                in blanket_removal_fraction_in = blanket_removal_fraction;
                in magnet_removal_fraction_in = magnet_removal_fraction;
                in pbl_refill_fraction_in = pbl_refill_fraction;
                in primary_event_in = primary_event;
                in primary_life_in = primary_life;
                in helium_makeup_fraction_in = helium_makeup_fraction;
                in overhaul_fraction_in = overhaul_fraction;
                in overhaul_year_in = overhaul_year;
                in dismantle_fraction_in = dismantle_fraction;
                in salvage_fraction_in = salvage_fraction;
            }
            attribute initial_financed_capital : Real = evaluate.initial_financed_capital;
            attribute annual_source_service : Real = evaluate.annual_source_service;
            attribute annual_service : Real = evaluate.annual_service;
            attribute annual_makeup : Real = evaluate.annual_makeup;
            attribute annual_expense : Real = evaluate.annual_expense;
            attribute blanket_life_years : Real = evaluate.blanket_life_years;
            attribute magnet_life_years : Real = evaluate.magnet_life_years;
            attribute blanket_events : Real = evaluate.blanket_events;
            attribute magnet_events : Real = evaluate.magnet_events;
            attribute primary_events : Real = evaluate.primary_events;
            attribute blanket_replacement_pv : Real = evaluate.blanket_replacement_pv;
            attribute magnet_replacement_pv : Real = evaluate.magnet_replacement_pv;
            attribute primary_replacement_pv : Real = evaluate.primary_replacement_pv;
            attribute overhaul_pv : Real = evaluate.overhaul_pv;
            attribute source_replacement_pv : Real = evaluate.source_replacement_pv;
            attribute conversion_replacement_pv : Real = evaluate.conversion_replacement_pv;
            attribute terminal_pv : Real = evaluate.terminal_pv;
            attribute annual_expense_pv : Real = evaluate.annual_expense_pv;
            attribute total_cost_pv : Real = evaluate.total_cost_pv;
            attribute energy_pv : Real = evaluate.energy_pv;
            attribute lcoe_USD2025_MWh : Real = evaluate.lcoe_USD2025_MWh;
            attribute outage_years : Real = evaluate.outage_years;
            attribute outage_margin : Real = evaluate.outage_margin;
            attribute domain_supported : Real = evaluate.domain_supported;
            attribute economic_defined : Real = evaluate.economic_defined;
            attribute cost_residual : Real = evaluate.cost_residual;
            assert constraint outage_margin_ok : 'Whole Plant Nonnegative' { in metric_in = outage_margin; }
            assert constraint economic_defined_ok : 'Whole Plant Supported' { in metric_in = economic_defined; }
            assert constraint domain_supported_ok : 'Whole Plant Supported' { in metric_in = domain_supported; }
        }
        part steam_actual_approach {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. */
            calc evaluate : 'Actual Exchanger Approaches' {
                in primary_hot_in = primary_loop.T_out;
                in primary_exchanger_return_in = steam_return_control.exchanger_return;
                in secondary_in_in = steam_return_control.secondary_inlet;
                in secondary_out_in = steam_secondary_temperature.value;
            }
            attribute hot_gap : Real = evaluate.hot_gap;
            attribute cold_gap : Real = evaluate.cold_gap;
            assert constraint hot_gap_ok : 'Whole Plant Positive' { in metric_in = hot_gap; }
            assert constraint cold_gap_ok : 'Whole Plant Positive' { in metric_in = cold_gap; }
        }
        part gas_capital_1_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = gas_ledger.capital_1;
            :>> capital_cost = gas_ledger.capital_1;
        }
        part gas_capital_2_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = gas_ledger.capital_2;
            :>> capital_cost = gas_ledger.capital_2;
        }
        part gas_capital_3_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = gas_ledger.capital_3;
            :>> capital_cost = gas_ledger.capital_3;
        }
        part gas_capital_4_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = gas_ledger.capital_4;
            :>> capital_cost = gas_ledger.capital_4;
        }
        part gas_capital_5_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = gas_ledger.capital_5;
            :>> capital_cost = gas_ledger.capital_5;
        }
        part gas_capital_6_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = gas_ledger.capital_6;
            :>> capital_cost = gas_ledger.capital_6;
        }
        part gas_capital_7_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = gas_ledger.capital_7;
            :>> capital_cost = gas_ledger.capital_7;
        }
        part gas_capital_8_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = gas_ledger.capital_8;
            :>> capital_cost = gas_ledger.capital_8;
        }
        part gas_capital_9_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = gas_ledger.capital_9;
            :>> capital_cost = gas_ledger.capital_9;
        }
        part gas_capital_10_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = gas_ledger.capital_10;
            :>> capital_cost = gas_ledger.capital_10;
        }
        part gas_controller_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "23";
            attribute cost : Real = gas_ledger.controller_capital;
            :>> capital_cost = gas_ledger.controller_capital;
        }
        part gas_overheads {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. */
            attribute salt_spare : Real = 0.0;
            attribute salt_vendor : Real = 0.0;
            attribute steam_branch : Real = 0.0;
            calc evaluate : 'Whole Plant Capital Accounts' {
                in land_in = land_account.cost;
                in facilities_in = facilities_account.cost;
                in magnet_in = magnet_account.cost;
                in heating_in = heating_account.cost;
                in divertor_in = divertor_account.cost;
                in blanket_in = blanket_account.cost;
                in shield_in = shield_account.cost;
                in structure_in = structure_account.cost;
                in vessel_in = vessel_account.cost;
                in power_supplies_in = power_supplies_account.cost;
                in remote_handling_in = remote_handling_account.cost;
                in installation_in = installation_account.cost;
                in primary_circulators_in = primary_circulators_account.cost;
                in primary_pipes_in = primary_pipes_account.cost;
                in primary_spares_in = primary_spares_account.cost;
                in primary_helium_in = primary_helium_account.cost;
                in cryoplant_in = cryoplant_account.cost;
                in auxiliary_rejection_in = auxiliary_rejection_account.cost;
                in waste_in = waste_account.cost;
                in fuel_processing_in = fuel_processing_account.cost;
                in other_reactor_in = other_reactor_account.cost;
                in reactor_controls_in = reactor_controls_account.cost;
                in shared_electrical_in = shared_electrical_account.cost;
                in miscellaneous_in = miscellaneous_account.cost;
                in pbl_initial_in = pbl_initial_account.cost;
                in owner_in = owner_account.cost;
                in digital_twin_in = digital_twin_account.cost;
                in source_installation_allowance_in = source_installation_allowance_account.cost;
                in tritium_initial_in = tritium_initial_account.cost;
                in capital_1_in = gas_capital_1_account.cost;
                in capital_2_in = gas_capital_2_account.cost;
                in capital_3_in = gas_capital_3_account.cost;
                in capital_4_in = gas_capital_4_account.cost;
                in capital_5_in = gas_capital_5_account.cost;
                in capital_6_in = gas_capital_6_account.cost;
                in capital_7_in = gas_capital_7_account.cost;
                in capital_8_in = gas_capital_8_account.cost;
                in capital_9_in = gas_capital_9_account.cost;
                in capital_10_in = gas_capital_10_account.cost;
                in controller_capital_in = gas_controller_account.cost;
                in salt_spare_in = salt_spare;
                in salt_vendor_in = salt_vendor;
                in steam_branch_in = steam_branch;
                in contingency_rate_in = finance.contingency_rate;
                in indirect_rate_in = finance.indirect_rate;
                in freight_rate_in = finance.freight_rate;
                in general_spares_rate_in = finance.general_spares_rate;
                in tax_rate_in = finance.tax_rate;
                in insurance_rate_in = finance.insurance_rate;
                in commissioning_rate_in = finance.commissioning_rate;
                in construction_years_in = finance.construction_years;
            }
            attribute common_purchases : Real = evaluate.common_purchases;
            attribute branch_purchases : Real = evaluate.branch_purchases;
            attribute direct_base : Real = evaluate.direct_base;
            attribute equipment_base : Real = evaluate.equipment_base;
            attribute freight_base : Real = evaluate.freight_base;
            attribute general_spares_base : Real = evaluate.general_spares_base;
            attribute tax_base : Real = evaluate.tax_base;
            attribute insurance_base : Real = evaluate.insurance_base;
            attribute overhaul_base : Real = evaluate.overhaul_base;
            attribute salvage_base : Real = evaluate.salvage_base;
            attribute contingency : Real = evaluate.contingency;
            attribute indirect : Real = evaluate.indirect;
            attribute freight : Real = evaluate.freight;
            attribute general_spares : Real = evaluate.general_spares;
            attribute tax : Real = evaluate.tax;
            attribute insurance : Real = evaluate.insurance;
            attribute nonfuel_commissioning : Real = evaluate.nonfuel_commissioning;
            attribute cas20 : Real = evaluate.cas20;
            attribute cas30 : Real = evaluate.cas30;
            attribute cas50 : Real = evaluate.cas50;
            attribute initial_capital : Real = evaluate.initial_capital;
            attribute reconciliation_residual : Real = evaluate.reconciliation_residual;
            attribute domain_supported : Real = evaluate.domain_supported;
            assert constraint domain_supported_ok : 'Whole Plant Supported' { in metric_in = domain_supported; }
        }
        part gas_contingency_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "29";
            attribute cost : Real = gas_overheads.contingency;
            :>> capital_cost = gas_overheads.contingency;
        }
        part gas_indirect_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "30";
            attribute cost : Real = gas_overheads.indirect;
            :>> capital_cost = gas_overheads.indirect;
        }
        part gas_freight_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "50";
            attribute cost : Real = gas_overheads.freight;
            :>> capital_cost = gas_overheads.freight;
        }
        part gas_general_spares_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "50";
            attribute cost : Real = gas_overheads.general_spares;
            :>> capital_cost = gas_overheads.general_spares;
        }
        part gas_tax_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "50";
            attribute cost : Real = gas_overheads.tax;
            :>> capital_cost = gas_overheads.tax;
        }
        part gas_insurance_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "50";
            attribute cost : Real = gas_overheads.insurance;
            :>> capital_cost = gas_overheads.insurance;
        }
        part gas_nonfuel_commissioning_account : 'Supplied Plant Account' {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Selected procurement, independent of demand; disjoint membership in configuration.md. */
            :>> cas_code = "50";
            attribute cost : Real = gas_overheads.nonfuel_commissioning;
            :>> capital_cost = gas_overheads.nonfuel_commissioning;
        }
        part gas_operating {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. */
            calc evaluate : 'Whole Plant Operating Ledger' {
                in conversion_net_MW_in = gas_ledger.net_electric;
                in primary_electric_MW_in = primary_loop.p_elec;
                in primary_fluid_MW_in = primary_loop.w_fluid;
                in heating_wall_MW_in = source_basis.heating_wall_MW;
                in deposited_heating_MW_in = source_basis.deposited_heating_MW;
                in coil_drive_MW_in = supplied_core.coil_drive_MW;
                in refrigeration_MW_in = cryogenic_demand.refrigeration_MW;
                in cold_W_in = cryogenic_demand.cold_W;
                in intercept_W_in = cryogenic_demand.intercept_W;
                in tf_cooling_MW_in = steam_operating.tf_cooling_MW;
                in pf_cooling_MW_in = steam_operating.pf_cooling_MW;
                in fuel_vacuum_MW_in = steam_operating.fuel_vacuum_MW;
                in house_MW_in = steam_operating.house_MW;
                in reactor_controls_MW_in = steam_operating.reactor_controls_MW;
                in residual_MW_in = steam_operating.residual_MW;
                in auxiliary_electric_MW_in = steam_operating.auxiliary_electric_MW;
                in auxiliary_rating_MW_in = steam_operating.auxiliary_rating_MW;
                in auxiliary_water_C_in = steam_operating.auxiliary_water_C;
                in availability_in = finance.availability;
                in import_price_in = steam_operating.import_price;
            }
            attribute upstream_electric_MW : Real = evaluate.upstream_electric_MW;
            attribute net_export_MW : Real = evaluate.net_export_MW;
            attribute standby_MW : Real = evaluate.standby_MW;
            attribute annual_export_MWh : Real = evaluate.annual_export_MWh;
            attribute annual_import_MWh : Real = evaluate.annual_import_MWh;
            attribute annual_net_grid_MWh : Real = evaluate.annual_net_grid_MWh;
            attribute annual_import_cost : Real = evaluate.annual_import_cost;
            attribute auxiliary_heat_MW : Real = evaluate.auxiliary_heat_MW;
            attribute auxiliary_margin_MW : Real = evaluate.auxiliary_margin_MW;
            attribute primary_motor_loss_MW : Real = evaluate.primary_motor_loss_MW;
            attribute power_residual : Real = evaluate.power_residual;
            attribute domain_supported : Real = evaluate.domain_supported;
            assert constraint net_export_mw_ok : 'Whole Plant Positive' { in metric_in = net_export_MW; }
            assert constraint annual_net_grid_mwh_ok : 'Whole Plant Positive' { in metric_in = annual_net_grid_MWh; }
            assert constraint auxiliary_margin_mw_ok : 'Whole Plant Nonnegative' { in metric_in = auxiliary_margin_MW; }
            assert constraint domain_supported_ok : 'Whole Plant Supported' { in metric_in = domain_supported; }
        }
        part gas_whole {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. */
            calc evaluate : 'Whole Plant Lifecycle Ledger' {
                in initial_capital_in = gas_overheads.initial_capital;
                in salvage_base_in = gas_overheads.salvage_base;
                in overhaul_base_in = gas_overheads.overhaul_base;
                in magnet_capital_in = magnet_account.cost;
                in blanket_capital_in = blanket_account.cost;
                in divertor_capital_in = divertor_account.cost;
                in pbl_capital_in = pbl_initial_account.cost;
                in helium_capital_in = primary_helium_account.cost;
                in wall_load_in = source_basis.wall_load;
                in annual_export_MWh_in = gas_operating.annual_export_MWh;
                in annual_net_grid_MWh_in = gas_operating.annual_net_grid_MWh;
                in annual_import_cost_in = gas_operating.annual_import_cost;
                in annual_fuel_in = fuel_accounts.annual_fuel;
                in conversion_annual_service_in = gas_ledger.annual_service;
                in conversion_annual_makeup_in = gas_ledger.annual_makeup;
                in conversion_replacement_pv_in = gas_ledger.replacement_pv;
                in rate_in = finance.rate;
                in years_in = finance.years;
                in availability_in = finance.availability;
                in construction_years_in = finance.construction_years;
                in routine_om_in = steam_whole.routine_om;
                in routine_fraction_in = steam_whole.routine_fraction;
                in wall_life_in = steam_whole.wall_life;
                in magnet_life_in = steam_whole.magnet_life;
                in blanket_outage_in = steam_whole.blanket_outage;
                in magnet_outage_in = steam_whole.magnet_outage;
                in other_outage_in = steam_whole.other_outage;
                in blanket_removal_fraction_in = steam_whole.blanket_removal_fraction;
                in magnet_removal_fraction_in = steam_whole.magnet_removal_fraction;
                in pbl_refill_fraction_in = steam_whole.pbl_refill_fraction;
                in primary_event_in = steam_whole.primary_event;
                in primary_life_in = steam_whole.primary_life;
                in helium_makeup_fraction_in = steam_whole.helium_makeup_fraction;
                in overhaul_fraction_in = steam_whole.overhaul_fraction;
                in overhaul_year_in = steam_whole.overhaul_year;
                in dismantle_fraction_in = steam_whole.dismantle_fraction;
                in salvage_fraction_in = steam_whole.salvage_fraction;
            }
            attribute initial_financed_capital : Real = evaluate.initial_financed_capital;
            attribute annual_source_service : Real = evaluate.annual_source_service;
            attribute annual_service : Real = evaluate.annual_service;
            attribute annual_makeup : Real = evaluate.annual_makeup;
            attribute annual_expense : Real = evaluate.annual_expense;
            attribute blanket_life_years : Real = evaluate.blanket_life_years;
            attribute magnet_life_years : Real = evaluate.magnet_life_years;
            attribute blanket_events : Real = evaluate.blanket_events;
            attribute magnet_events : Real = evaluate.magnet_events;
            attribute primary_events : Real = evaluate.primary_events;
            attribute blanket_replacement_pv : Real = evaluate.blanket_replacement_pv;
            attribute magnet_replacement_pv : Real = evaluate.magnet_replacement_pv;
            attribute primary_replacement_pv : Real = evaluate.primary_replacement_pv;
            attribute overhaul_pv : Real = evaluate.overhaul_pv;
            attribute source_replacement_pv : Real = evaluate.source_replacement_pv;
            attribute conversion_replacement_pv : Real = evaluate.conversion_replacement_pv;
            attribute terminal_pv : Real = evaluate.terminal_pv;
            attribute annual_expense_pv : Real = evaluate.annual_expense_pv;
            attribute total_cost_pv : Real = evaluate.total_cost_pv;
            attribute energy_pv : Real = evaluate.energy_pv;
            attribute lcoe_USD2025_MWh : Real = evaluate.lcoe_USD2025_MWh;
            attribute outage_years : Real = evaluate.outage_years;
            attribute outage_margin : Real = evaluate.outage_margin;
            attribute domain_supported : Real = evaluate.domain_supported;
            attribute economic_defined : Real = evaluate.economic_defined;
            attribute cost_residual : Real = evaluate.cost_residual;
            assert constraint outage_margin_ok : 'Whole Plant Nonnegative' { in metric_in = outage_margin; }
            assert constraint economic_defined_ok : 'Whole Plant Supported' { in metric_in = economic_defined; }
            assert constraint domain_supported_ok : 'Whole Plant Supported' { in metric_in = domain_supported; }
        }
        part gas_actual_approach {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. */
            calc evaluate : 'Actual Exchanger Approaches' {
                in primary_hot_in = primary_loop.T_out;
                in primary_exchanger_return_in = return_control.exchanger_return;
                in secondary_in_in = heat_exchangers.he_secondary_in;
                in secondary_out_in = heat_exchangers.turbine_temperature;
            }
            attribute hot_gap : Real = evaluate.hot_gap;
            attribute cold_gap : Real = evaluate.cold_gap;
            assert constraint hot_gap_ok : 'Whole Plant Positive' { in metric_in = hot_gap; }
            assert constraint cold_gap_ok : 'Whole Plant Positive' { in metric_in = cold_gap; }
        }
        part steam_secondary_temperature {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. */
            calc evaluate : 'Temperature Kelvin' {
                in celsius_in = steam_boundary.salt_hot;
            }
            attribute value : Real = evaluate.value;
        }
        part primary_offer {
            doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. */
            attribute pressure_rating_Pa : Real = 300319.8958872855;
            attribute electric_rating_MW : Real = 175.28093440448808;
            attribute path_flow_rating : Real = 225.07777777777778;
            calc evaluate : 'Supplied Primary Capacity' {
                in pressure_rating_Pa_in = pressure_rating_Pa;
                in pressure_demand_Pa_in = primary_loop.dp_loop;
                in electric_rating_MW_in = electric_rating_MW;
                in electric_demand_MW_in = primary_loop.p_elec;
                in path_flow_rating_in = path_flow_rating;
                in path_flow_demand_in = primary_loop.mdot_loop;
                in path_count_in = primary_loop.n_loops;
            }
            attribute pressure_margin_Pa : Real = evaluate.pressure_margin_Pa;
            attribute electric_margin_MW : Real = evaluate.electric_margin_MW;
            attribute flow_margin_kg_s : Real = evaluate.flow_margin_kg_s;
            attribute inventory_supported : Real = evaluate.inventory_supported;
            assert constraint pressure_margin_pa_ok : 'Whole Plant Nonnegative' { in metric_in = pressure_margin_Pa; }
            assert constraint electric_margin_mw_ok : 'Whole Plant Nonnegative' { in metric_in = electric_margin_MW; }
            assert constraint flow_margin_kg_s_ok : 'Whole Plant Nonnegative' { in metric_in = flow_margin_kg_s; }
            assert constraint inventory_supported_ok : 'Whole Plant Supported' { in metric_in = inventory_supported; }
        }

    }
}
