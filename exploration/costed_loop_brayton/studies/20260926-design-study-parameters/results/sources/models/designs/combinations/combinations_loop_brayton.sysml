package combinations_loop_brayton {
    doc /*
    C-1: the Stellaris helium primary loop ('Primary Coolant Loop' at the Stellaris circuit values, supplied blanket heat)
    as the only heat source of the ARIES three-stage intercooled recuperated Brayton chain, with the ARIES capacity screens.
    Existing definitions only; every binding is a new case binding (WI-093 design § 2). The two idle exchanger stages are a
    representation quirk of a closure that always reads three branches: positive dummy flow, cp and limit with UA 0 and
    available heat 0 transfer nothing (network_heat_driven_closure_impl.py:31-40). No quantity is sized from demand.
    **Source**: work/active/WI-093_combination-assemblies/design.md **Reference**: goal design-space-combinations, map row H1
    **Basis**: [INHERITED: Stellaris] loop values from models/designs/stellarator_09/stellarator_plant.sysml:1226-1321 and the
    documented baseline; [INHERITED: ARIES] cycle, component and rating values from models/designs/aries_cs_integrated/plant.sysml;
    [ASSUMED] cycle flow 2500 kg/s and the re-selected ratings used by cases. **Last Updated**: 2026-09-26
    */
    private import ScalarValues::*;
    private import mfe_primary_loop::*;
    private import integrated_heat_electricity::*;
    private import integrated_equipment_costs::*;
    private import ideal_gas_brayton_components::*;
    private import mfe_viability::*;

    part loop_brayton {
        doc /* Root occurrence of the combinations_loop_brayton assembly (the generator renders output aliases by part path, so each assembly needs its own root part; the Stellaris nesting shape). */
        part blanket_source {
            doc /* Supplied blanket heat delivered to the loop. **Basis**: [INHERITED: Stellaris baseline blanket__source_heat__q_source, MW]; chosen here, no blanket model assembled. */
            attribute q_source : Real = 3125.9322770825056;
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
            attribute f_loss : Real = 1.0;
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
            attribute mdot : Real = evaluate.mdot;
            attribute T_out : Real = evaluate.T_out;
            attribute mdot_loop : Real = evaluate.mdot_loop;
            attribute dp_loop : Real = evaluate.dp_loop;
            attribute p_elec : Real = evaluate.p_elec;
            attribute q_ihx : Real = evaluate.q_ihx;
            attribute capacity_margin : Real = evaluate.capacity_margin;
            attribute p_pump_total : Real = evaluate.p_pump_total;
            attribute q_recovered_total : Real = evaluate.q_recovered_total;
        }
        part cycle {
            doc /* ARIES cycle operating choices; selected_flow re-selected for the lower-temperature source. **Basis**: [INHERITED: ARIES plant.sysml:142-151] except selected_flow [ASSUMED: 2500 kg/s, inside the round-1 screen's feasible range]. */
            attribute selected_flow : Real = 2500.0;
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
            doc /* Installed exchanger conductance from the selected area and assumed U. **Basis**: [INHERITED: ARIES plant.sysml he_hx]. */
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
            doc /* 'Plant Electrical Balance' with the loop's own pump electricity and recovered friction; the auxiliary demands are the ARIES A-register values on a Stellaris loop (disclosed); no fuel chain in C-1, so the exhaust-driven fuel term is 0. **Basis**: [INHERITED: ARIES plant.sysml:377-424]. */
            attribute auxiliary_heat : Real = 20.0;
            attribute heating_efficiency : Real = 0.5;
            attribute generator_efficiency : Real = 0.98;
            attribute motor_efficiency : Real = 0.95;
            attribute cryo : Real = 10.0;
            attribute fuel_base : Real = 5.0;
            attribute fuel_coefficient : Real = 1e-22;
            attribute fuel_exhaust : Real = 0.0;
            attribute control : Real = 5.0;
            attribute other_electric : Real = 5.0;
            calc evaluate : 'Plant Electrical Balance' {
                in turbine_work_in = turbine.shaft_produced;
                in compressor_1_in = compressor_1.shaft_demand;
                in compressor_2_in = compressor_2.shaft_demand;
                in compressor_3_in = compressor_3.shaft_demand;
                in auxiliary_heat_in = auxiliary_heat;
                in pump_electric_in = primary_loop.p_elec;
                in pump_recovered_in = primary_loop.q_recovered_total;
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
        part he_capacity {
            doc /* Helium duty package rating against the loop's delivered heat. **Basis**: [INHERITED: ARIES 1500 MW]; cases re-select. */
            attribute selected_rating : Real = 1500.0;
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
        part rejection_capacity {
            doc /* Heat rejection package rating against the cycle's rejected heat. The demand is an assembly expression reproducing the ledger's cycle_rejection formula (integrated_plant_ledger_impl.py:31) because the ledger is not assembled here. **Basis**: [INHERITED: ARIES 2500 MW]; cases re-select. */
            attribute selected_rating : Real = 2500.0;
            attribute assumed_supported : Boolean = true;
            attribute scenario_applicable : Boolean = true;
            attribute demand_available : Boolean = true;
            attribute rejected_heat : Real = -(intercooler_1.heat_into_fluid + intercooler_2.heat_into_fluid + precooler.heat_into_fluid);
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = selected_rating;
                in demand_in = rejected_heat;
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
            doc /* Heat removal, net power and loop rated-flow requirements on the assembled chain. **Basis**: energy_tolerance [ASSUMED: 1e-6 MW, the floor of the ledger body's rule max(1e-6, 1e-9 x supplied heat), integrated_plant_ledger_impl.py:43; the ledger is not assembled here]. */
            attribute energy_tolerance : Real = 1e-6;
            assert constraint heat_removal_ok : 'Heat Removal Adequate' {
                in unmet_in = heat_exchangers.unmet_heat;
                in tolerance_in = energy_tolerance;
            }
            assert constraint net_positive : 'Net Power Positive' {
                in net_electric = electrical.net_electric;
            }
            assert constraint loop_capacity_ok : 'Loop Capacity' {
                in mdot_loop_in = primary_loop.mdot_loop;
                in mdot_loop_rated_in = primary_loop.mdot_loop_rated;
            }
        }
    }
}
