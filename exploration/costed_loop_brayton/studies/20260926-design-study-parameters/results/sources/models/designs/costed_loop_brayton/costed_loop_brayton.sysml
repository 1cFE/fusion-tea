package costed_loop_brayton {
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
    private import integrated_equipment_parts::*;
    private import costed_component::*;
    private import mfe_fuel_cycle::*;
    private import mfe_account_costs::*;
    private import mfe_lcoe_dcf::*;
    private import integrated_lifecycle_costs::*;

    part plant {
        doc /* Root occurrence of the costed_loop_brayton assembly (the generator renders output aliases by part path, so each assembly needs its own root part; the Stellaris nesting shape). */
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
            doc /* 'Plant Electrical Balance' with the loop's own pump electricity and recovered friction; the auxiliary demands are the ARIES A-register values on a Stellaris loop (disclosed); the exhaust-driven fuel term is held at 0 as in C-1 so the C-1 receipts replay bit-exactly; the assembled fuel chain's exhaust rate feeds only the fuel cost, and the S2 case overrides fuel_exhaust with that stored rate (contract v2 section 3). **Basis**: [INHERITED: ARIES plant.sysml:377-424]. */
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
        part fusion_source {
            doc /* The fusion power whose blanket heat is supplied above; held equal across every point; it feeds only the fuel chain. **Basis**: [INHERITED: Stellaris baseline plasma p_fus 2652.563 MW, the power behind blanket__source_heat__q_source]. */
            attribute p_fus : Real = 2652.5631770825056;
        }
        part fuel {
            doc /* 'Fuel Cycle Flows' on the supplied fusion power, the ARIES fuel conventions; a constant of the sweep. **Basis**: [INHERITED: ARIES plant.sysml:110-141]. */
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
                in p_fus_in = fusion_source.p_fus;
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
        part cost_accounts {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:710-714]. */
            attribute estimate_mode : Real = 0.0;
            attribute one_module : Real = 1.0;
        }
        part cost_schedule {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:715-722, E7/E8]. */
            attribute availability : Real = 0.85;
            attribute plant_years : Real = 40.0;
            attribute replacement_life_fpy : Real = 5.0;
            attribute replacement_factor : Real = 1.0;
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
        part rest_of_plant : 'Selected Equipment' {
            doc /* Held-equal capital for everything this assembly does not price: the ARIES direct source scope at the sealed 423 MW baseline (2,619,603,000 USD2004, direct_source_scope__evaluate__total of case baseline-no-credit, study 20260925-aries-reconciled-alternative-economics) less the seven items priced above at their ARIES reference values (461,372,866.67). An ARIES-scope reactor, buildings, electrical and heat-transport plant standing in for the unpriced Stellaris side; sets absolute LCOE, not the operating ranking. **Basis**: [ASSUMED: held equal; comparison-contract.md section 6]. */
            :>> cas_code = "20-27 remainder";
            attribute selected_quantity : Real = 1.0;
            attribute reference_cost : Real = 2158230133.3333335;
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
        part fuel_inventory : 'Selected Equipment' {
            doc /* Initial tritium stock (capital) and the annual makeup purchased under the no-credit convention (operating); deuterium priced per reaction. **Basis**: [INHERITED: ARIES plant.sysml:1595-1666, E6]. */
            :>> cas_code = "26.fuel";
            attribute selected_tritium_kg : Real = 10.0;
            attribute process_residence_s : Real = 1000.0;
            attribute annual_recovery_kg : Real = 0.0;
            attribute tritium_price : Real = 30000000.0;
            attribute deuterium_price : Real = 1000.0;
            attribute deuterium_atom_kg : Real = 3.3435837724e-27;
            calc atoms : 'Selected Stock Atoms' {
                in stock_kg_in = selected_tritium_kg;
                in atom_mass_in = fuel.tritium_atom_kg;
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
                in atom_mass_in = fuel.tritium_atom_kg;
                in decay_in = fuel.decay_constant_s;
                in seconds_in = fuel.seconds_per_year;
                in availability_in = cost_schedule.availability;
                in burn_in = fuel.burn_rate;
                in loss_in = fuel.loss_rate;
                in exhaust_in = fuel.exhaust_rate;
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
                in p_fus = fusion_source.p_fus;
                in n_mod_in = cost_accounts.one_module;
                in availability_in = cost_schedule.availability;
                in cost_per_rxn = deuterium_per_reaction;
                in q_eff = fuel.reaction_energy_mev;
                in mev_to_joules_in = fuel.mev_joules;
                in burn_fraction_in = fuel.pass_burn_fraction;
                in fuel_recovery_in = fuel.exhaust_recovery;
            }
            attribute annual_deuterium_cost : Real = deuterium.annual_fuel;
        }
        part priced_equipment {
            doc /* The seven items this assembly prices, summed. **Basis**: [INHERITED: ARIES conversion_equipment pattern plant.sysml:1923-1936]. */
            calc evaluate : 'Eight Amount Sum' {
                in amount1_in = compressor_equipment.capital_cost;
                in amount2_in = turbine_equipment.capital_cost;
                in amount3_in = generator_equipment.capital_cost;
                in amount4_in = conversion_services.capital_cost;
                in amount5_in = heat_rejection_equipment.capital_cost;
                in amount6_in = he_duty_equipment.capital_cost;
                in amount7_in = he_hx.capital_cost;
                in amount8_in = 0.0;
            }
            attribute total : Real = evaluate.total;
        }
        part direct_cost {
            doc /* Direct capital: rest of plant + priced equipment + initial tritium stock. **Basis**: [INHERITED: ARIES plant.sysml:1951-1964 pattern]. */
            calc evaluate : 'Eight Amount Sum' {
                in amount1_in = rest_of_plant.capital_cost;
                in amount2_in = priced_equipment.total;
                in amount3_in = fuel_inventory.capital_cost;
                in amount4_in = 0.0;
                in amount5_in = 0.0;
                in amount6_in = 0.0;
                in amount7_in = 0.0;
                in amount8_in = 0.0;
            }
            attribute total : Real = evaluate.total;
        }
        part indirect_cost {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:1965-1975, E9]. */
            attribute fraction : Real = 0.2;
            calc evaluate : 'Indirect Cost' {
                in indirect_fraction_in = fraction;
                in direct_cost = costed_loop_brayton::plant::direct_cost.total;
                in construction_time = 6.0;
                in reference_construction_time = 6.0;
            }
            attribute amount : Real = evaluate.cost;
        }
        part contingency_basis {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:1976-1989]. */
            calc evaluate : 'Eight Amount Sum' {
                in amount1_in = direct_cost.total;
                in amount2_in = indirect_cost.amount;
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
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:1990-1998, E9]. */
            attribute fraction : Real = 0.2;
            calc evaluate : 'Contingency Cost' {
                in contingency_rate_in = fraction;
                in direct_subtotal = contingency_basis.total;
            }
            attribute amount : Real = evaluate.cost;
        }
        part owner_commissioning {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:1999-2007, E9]. */
            attribute fraction : Real = 0.05;
            calc evaluate : 'Scaled Amount' {
                in amount_in = direct_cost.total;
                in factor_in = fraction;
            }
            attribute amount : Real = evaluate.amount;
        }
        part annual_om {
            doc /* Flat O&M allowance. **Basis**: [INHERITED: ARIES plant.sysml:2008-2020, E7]. */
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
        part replacement_scope {
            doc /* Held-equal replacement event scope: the ARIES nominal blanket + divertor + LiPb makeup event (replacement__evaluate__event_cost of the sealed baseline, 72,231,350 USD2004). **Basis**: [ASSUMED: held equal; comparison-contract.md section 3]. */
            attribute selected_event_scope : Real = 72231350.0;
            calc evaluate : 'Scaled Amount' {
                in amount_in = selected_event_scope;
                in factor_in = cost_schedule.replacement_factor;
            }
            attribute amount : Real = evaluate.amount;
        }
        part replacement {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:2051-2066, E8]. */
            calc evaluate : 'Replacement Events' {
                in event_cost_in = replacement_scope.amount;
                in life_fpy_in = cost_schedule.replacement_life_fpy;
                in availability_in = cost_schedule.availability;
                in plant_years_in = cost_schedule.plant_years;
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
            doc /* 'Equipment Cost Ledger' with the assembly's own net electricity; no source-budget comparison in this assembly (the source inputs are 0). **Basis**: [INHERITED: ARIES plant.sysml:2067-2107, E10]. */
            attribute consumables : Real = 5000000.0;
            attribute import_price : Real = 50.0;
            attribute no_source_comparison : Real = 0.0;
            calc evaluate : 'Equipment Cost Ledger' {
                in direct_in = direct_cost.total;
                in source_direct_in = no_source_comparison;
                in source_inclusive_in = no_source_comparison;
                in indirect_in = indirect_cost.amount;
                in contingency_in = contingency.amount;
                in owner_in = owner_commissioning.amount;
                in om_in = annual_om.amount;
                in tritium_in = fuel_inventory.annual_cost;
                in deuterium_in = fuel_inventory.annual_deuterium_cost;
                in consumables_in = consumables;
                in replacement_reserve_in = replacement.annual_reserve;
                in replacement_total_in = replacement.lifetime_total;
                in net_power_in = electrical.net_electric;
                in availability_in = cost_schedule.availability;
                in import_price_in = import_price;
                in source_reactor_gap_in = no_source_comparison;
                in source_core_excess_in = no_source_comparison;
                in source_coil_excess_in = no_source_comparison;
                in currency_year_in = 2004.0;
            }
            attribute direct : Real = evaluate.direct;
            attribute overnight : Real = evaluate.overnight;
            attribute annual_operating : Real = evaluate.annual_operating;
            attribute annual_replacement_reserve : Real = evaluate.annual_replacement_reserve;
            attribute lifetime_replacement : Real = evaluate.lifetime_replacement;
            attribute annual_export_mwh : Real = evaluate.annual_export_mwh;
            attribute annual_import_mwh : Real = evaluate.annual_import_mwh;
            attribute annual_import_cost : Real = evaluate.annual_import_cost;
            attribute currency_year : Real = evaluate.currency_year;
        }
        part finance {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:2108-2117, F1-F9]. */
            attribute discount_rate : Real = 0.05;
            attribute construction_years : Real = 6.0;
            attribute terminal_fraction : Real = 0.1;
            attribute salvage_fraction : Real = 0.02;
            attribute other_overhaul_fraction : Real = 0.05;
            attribute other_overhaul_year : Real = 20.0;
            attribute supply_service_annual : Real = 0.0;
        }
        part operating_levelization {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:2128-2139]. */
            calc evaluate : 'Levelized Annual Cost' {
                in annual_cost = cost_ledger.annual_operating;
                in interest_rate = finance.discount_rate;
                in inflation_rate_in = 0.0;
                in operational_years_in = cost_schedule.plant_years;
                in project_time = 0.0;
            }
            attribute factor : Real = evaluate.crf;
            attribute annual : Real = evaluate.levelized;
        }
        part lifecycle_accounts {
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:2148-2219, WI-091]. */
            calc evaluate : 'Lifecycle Cashflow Accounts' {
                in overnight_in = cost_ledger.overnight;
                in net_power_in = electrical.net_electric;
                in annual_energy_in = cost_ledger.annual_export_mwh;
                in annual_operating_in = cost_ledger.annual_operating;
                in om_in = annual_om.amount;
                in tritium_in = fuel_inventory.annual_cost;
                in deuterium_in = fuel_inventory.annual_deuterium_cost;
                in consumables_in = cost_ledger.consumables;
                in imports_in = cost_ledger.annual_import_cost;
                in supply_service_in = finance.supply_service_annual;
                in crf_in = operating_levelization.factor;
                in discount_in = finance.discount_rate;
                in construction_years_in = finance.construction_years;
                in plant_years_in = cost_schedule.plant_years;
                in availability_in = cost_schedule.availability;
                in event_cost_in = replacement.event_cost;
                in interval_years_in = replacement.interval_years;
                in event_count_in = replacement.event_count;
                in terminal_fraction_in = finance.terminal_fraction;
                in salvage_fraction_in = finance.salvage_fraction;
                in other_overhaul_fraction_in = finance.other_overhaul_fraction;
                in other_overhaul_year_in = finance.other_overhaul_year;
                in annual_burn_in = fuel_inventory.annual_burn;
                in annual_loss_in = fuel_inventory.annual_loss;
                in annual_decay_in = fuel_inventory.annual_decay;
                in annual_feed_in = fuel_inventory.annual_recovery_kg;
                in external_shortfall_in = fuel_inventory.annual_external;
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
            doc /* **Basis**: [INHERITED: ARIES plant.sysml:2220-2232]. */
            calc evaluate : 'LCOE DCF' {
                in total_capital_in = cost_ledger.overnight;
                in annual_om_in = lifecycle_accounts.noncapital_annual;
                in net_electric_mw = electrical.net_electric;
                in availability_in = cost_schedule.availability;
                in discount_rate_in = finance.discount_rate;
                in construction_years_in = finance.construction_years;
                in operational_years_in = cost_schedule.plant_years;
            }
            attribute lcoe : Real = evaluate.lcoe;
        }
    }
}
