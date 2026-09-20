package mfe_plant_systems {
    private import ScalarValues::*;
    private import mfe_viability::*;
    private import costed_component::*;
    private import mfe_cryo_inventory::*;
    private import mfe_interfaces::*;
    private import mfe_vacuum::*;
    private import mfe_primary_loop::*;
    private import mfe_cooling_equipment::*;
    private import mfe_cooling_accounts::*;
    private import mfe_fuel_cycle::*;
    private import mfe_cryo_plant::*;
    private import mfe_account_costs::*;

    part def 'Cooling Machine Account' {
        doc /* Active cooling machines, with independently computed flow, shaft duty and installed package cost.
        Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
        Ref: Equipment and account boundary; Basis: separately engineered child account. */
        attribute count : Real; // active machines
        attribute mass_flow : Real; // kg/s per machine
        attribute shaft_power : Real; // MW per machine
        attribute capital_cost : Real; // installed USD2025 CPI proxy
    }

    part def 'Cooling Pipe Account' {
        doc /* Representative ex-vessel pipe and fitting mass, fabricated price and site installation.
        Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
        Ref: Equipment and account boundary; Basis: separately engineered child account. */
        attribute steel_mass : Real; // kg installed pipe and fittings, plant total
        attribute capital_cost : Real; // installed USD2025 CPI proxy
    }

    part def 'Cooling Exchanger Account' {
        doc /* Fixed geometry helium-to-HITEC exchanger modules and separately calculated required thermal area.
        Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
        Ref: Equipment and account boundary; Basis: separately engineered child account. */
        attribute count : Real; // installed exchanger modules
        attribute installed_area : Real; // m2 per module
        attribute required_area : Real; // m2 per module
        attribute duty : Real; // MW per module
        attribute capital_cost : Real; // installed USD2025 CPI proxy
    }

    part def 'Cooling Inventory Account' {
        doc /* Explicit initial coolant inventory subset; unmeasured in-vessel and conversion inventory remain outside the price.
        Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
        Ref: Equipment and account boundary; Basis: separately engineered child account. */
        attribute helium_mass : Real; // kg priced ex-vessel subset
        attribute salt_mass : Real; // kg priced intermediate subset
        attribute capital_cost : Real; // initial fluid purchases USD2025 CPI proxy
    }

    part def 'Cooling Spares Account' {
        doc /* One initial spare primary package and one salt pump per supported single-module plant; scheduled replacements are separate.
        Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
        Ref: Equipment and account boundary; Basis: separately engineered child account. */
        attribute capital_cost : Real; // uninstalled initial spare purchases USD2025 CPI proxy
    }

    part def 'Primary Heat Transport' {
        attribute rated_helium_suction_K : Real default 0.0; // supplied [K]
        attribute rated_helium_suction_Pa : Real default 0.0; // supplied [Pa]
        attribute rated_helium_discharge_Pa : Real default 0.0; // supplied [Pa]
        attribute rated_helium_hot_K : Real default 0.0; // supplied [K]
        attribute rated_helium_cp : Real default 0.0; // supplied [J/kg/K]
        attribute rated_helium_gamma : Real default 0.0; // supplied [1]
        attribute rated_salt_hot_C : Real default 0.0; // supplied [degC]
        attribute rated_salt_return_C : Real default 0.0; // supplied [degC]
        attribute rated_salt_cp : Real default 0.0; // supplied [kJ/kg/K]
        attribute helium_rated_dp_Pa : Real default 0.0; // supplied [Pa]
        attribute helium_rated_electric_MW : Real default 0.0; // supplied [MWe]
        calc helium_offered_conditions : 'Helium Offered Conditions' {
            in enabled_in = equipment_enabled;
            in mode_in = loop_live;
            in actual_suction_K_in = primary_loop.T_comp_in;
            in rated_suction_K_in = rated_helium_suction_K;
            in actual_suction_Pa_in = equipment.circulator_suction_Pa;
            in rated_suction_Pa_in = rated_helium_suction_Pa;
            in actual_discharge_Pa_in = loop_p;
            in rated_discharge_Pa_in = rated_helium_discharge_Pa;
            in actual_hot_K_in = T_out;
            in rated_hot_K_in = rated_helium_hot_K;
            in actual_cp_in = loop_cp;
            in rated_cp_in = rated_helium_cp;
            in actual_gamma_in = loop_gamma;
            in rated_gamma_in = rated_helium_gamma;
        }
        attribute helium_rating_applicable : Boolean = helium_offered_conditions.applicable;
        attribute helium_rating_supported : Boolean = helium_offered_conditions.supported;
        attribute helium_rating_defined : Real = helium_offered_conditions.evaluation_defined;
        calc salt_offered_conditions : 'Salt Offered Conditions' {
            in enabled_in = equipment_enabled;
            in mode_in = secondary_energy_mode;
            in actual_hot_C_in = salt_hot_C;
            in rated_hot_C_in = rated_salt_hot_C;
            in actual_return_C_in = salt_return_C;
            in rated_return_C_in = rated_salt_return_C;
            in actual_cp_in = salt_cp_kJ_kgK;
            in rated_cp_in = rated_salt_cp;
        }
        attribute salt_rating_applicable : Boolean = salt_offered_conditions.applicable;
        attribute salt_rating_supported : Boolean = salt_offered_conditions.supported;
        attribute salt_rating_defined : Real = salt_offered_conditions.evaluation_defined;
        calc helium_flow_capability : 'Offered Capacity Screen' {
            in rating_in = mdot_loop_rated;
            in demand_in = mdot_loop;
            in applicable_in = helium_rating_applicable;
            in conditions_supported_in = helium_rating_supported;
            in demand_available_in = true;
        }
        attribute helium_flow_margin : Real = helium_flow_capability.margin;
        attribute helium_flow_applicable : Boolean = helium_flow_capability.applicable;
        attribute helium_flow_supported : Boolean = helium_flow_capability.supported;
        attribute helium_flow_defined : Real = helium_flow_capability.evaluation_defined;
        attribute helium_flow_capacity_ok : Boolean = helium_flow_capability.capacity_ok;
        calc helium_pumping_capability : 'Offered Capacity Screen' {
            in rating_in = equipment_helium_design_shaft_MW;
            in demand_in = equipment.circulator_shaft_MW;
            in applicable_in = helium_rating_applicable;
            in conditions_supported_in = helium_rating_supported;
            in demand_available_in = true;
        }
        attribute helium_pumping_margin : Real = helium_pumping_capability.margin;
        attribute helium_pumping_applicable : Boolean = helium_pumping_capability.applicable;
        attribute helium_pumping_supported : Boolean = helium_pumping_capability.supported;
        attribute helium_pumping_defined : Real = helium_pumping_capability.evaluation_defined;
        attribute helium_pumping_capacity_ok : Boolean = helium_pumping_capability.capacity_ok;
        calc helium_pressure_rise_capability : 'Offered Capacity Screen' {
            in rating_in = helium_rated_dp_Pa;
            in demand_in = primary_loop.dp_loop;
            in applicable_in = helium_rating_applicable;
            in conditions_supported_in = helium_rating_supported;
            in demand_available_in = true;
        }
        attribute helium_pressure_rise_margin : Real = helium_pressure_rise_capability.margin;
        attribute helium_pressure_rise_applicable : Boolean = helium_pressure_rise_capability.applicable;
        attribute helium_pressure_rise_supported : Boolean = helium_pressure_rise_capability.supported;
        attribute helium_pressure_rise_defined : Real = helium_pressure_rise_capability.evaluation_defined;
        attribute helium_pressure_rise_capacity_ok : Boolean = helium_pressure_rise_capability.capacity_ok;
        calc helium_electric_capability : 'Offered Capacity Screen' {
            in rating_in = helium_rated_electric_MW;
            in demand_in = equipment.circulator_electric_MW;
            in applicable_in = helium_rating_applicable;
            in conditions_supported_in = helium_rating_supported;
            in demand_available_in = true;
        }
        attribute helium_electric_margin : Real = helium_electric_capability.margin;
        attribute helium_electric_applicable : Boolean = helium_electric_capability.applicable;
        attribute helium_electric_supported : Boolean = helium_electric_capability.supported;
        attribute helium_electric_defined : Real = helium_electric_capability.evaluation_defined;
        attribute helium_electric_capacity_ok : Boolean = helium_electric_capability.capacity_ok;
        calc salt_flow_capability : 'Offered Capacity Screen' {
            in rating_in = equipment_salt_design_flow_kg_s;
            in demand_in = equipment.salt_pump_flow;
            in applicable_in = salt_rating_applicable;
            in conditions_supported_in = salt_rating_supported;
            in demand_available_in = true;
        }
        attribute salt_flow_margin : Real = salt_flow_capability.margin;
        attribute salt_flow_applicable : Boolean = salt_flow_capability.applicable;
        attribute salt_flow_supported : Boolean = salt_flow_capability.supported;
        attribute salt_flow_defined : Real = salt_flow_capability.evaluation_defined;
        attribute salt_flow_capacity_ok : Boolean = salt_flow_capability.capacity_ok;
        calc salt_head_capability : 'Offered Capacity Screen' {
            in rating_in = equipment_salt_design_head_m;
            in demand_in = equipment_secondary_head;
            in applicable_in = salt_rating_applicable;
            in conditions_supported_in = salt_rating_supported;
            in demand_available_in = true;
        }
        attribute salt_head_margin : Real = salt_head_capability.margin;
        attribute salt_head_applicable : Boolean = salt_head_capability.applicable;
        attribute salt_head_supported : Boolean = salt_head_capability.supported;
        attribute salt_head_defined : Real = salt_head_capability.evaluation_defined;
        attribute salt_head_capacity_ok : Boolean = salt_head_capability.capacity_ok;
        calc salt_shaft_capability : 'Offered Capacity Screen' {
            in rating_in = equipment.salt_design_shaft_MW;
            in demand_in = equipment.salt_pump_shaft_MW;
            in applicable_in = salt_rating_applicable;
            in conditions_supported_in = salt_rating_supported;
            in demand_available_in = true;
        }
        attribute salt_shaft_margin : Real = salt_shaft_capability.margin;
        attribute salt_shaft_applicable : Boolean = salt_shaft_capability.applicable;
        attribute salt_shaft_supported : Boolean = salt_shaft_capability.supported;
        attribute salt_shaft_defined : Real = salt_shaft_capability.evaluation_defined;
        attribute salt_shaft_capacity_ok : Boolean = salt_shaft_capability.capacity_ok;
        calc salt_electric_demand_conversion : 'Salt Machine Electric' {
            in active_in = salt_rating_applicable;
            in total_MW_in = equipment.salt_electric_MW;
            in count_in = equipment.salt_pump_count;
        }
        attribute salt_electric_required : Real = salt_electric_demand_conversion.demand;
        calc salt_electric_capability : 'Offered Capacity Screen' {
            in rating_in = equipment.salt_design_electric_MW;
            in demand_in = salt_electric_required;
            in applicable_in = salt_rating_applicable;
            in conditions_supported_in = salt_rating_supported;
            in demand_available_in = true;
        }
        attribute salt_electric_margin : Real = salt_electric_capability.margin;
        attribute salt_electric_applicable : Boolean = salt_electric_capability.applicable;
        attribute salt_electric_supported : Boolean = salt_electric_capability.supported;
        attribute salt_electric_defined : Real = salt_electric_capability.evaluation_defined;
        attribute salt_electric_capacity_ok : Boolean = salt_electric_capability.capacity_ok;

        doc /*
        The primary coolant loop between the blanket and the power cycle. WHAT THE MODEL
        COMPUTES: the representative helium primary circuit of WI-045 (Moscato et al. 2017, the
        EU DEMO HCLL balance of plant), in sized-flow mode with its pumping power. WHAT THE
        SOURCE SAYS: the Stellaris breeding zone is water-cooled at PWR conditions and the first
        wall helium-cooled at 8 MPa (output.md lines 1490-1491, 1534-1536) -- goal
        structural-decomposition fact 6, surfaced and carried as a follow-on, not changed here.
        Owns the loop facts and mode flags and the two coolant cost bases. WI-057.
        **Source**: knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/output.md
        **Ref**: WI-045 design; output.md:79 (helium at 8 MPa)
        **Basis**: the loop as the owner of the circuit facts the primary-loop calc reads
        */
        // ---- ports (WI-057): the exchanges this part takes part in; declarative, see mfe_interfaces ----
        port hot_in : ~'Thermal Port';   // <- blanket.coolant (primary_loop.q_source_in)
        port hot_out : 'Thermal Port';   // -> turbine.coolant (cycle.T_hot_in = T_out; pb.q_recovered_in)
        port electric_in : ~'Electric Port';   // <- electric_plant.recirculating (pb.p_pump_total_in)
        // ---- Primary loop and cycle (WI-045, goal plant-closure) ----
        // The loop and the cycle are computed producers; the five attributes
        // below select the mode. Dormant defaults: a concept that binds no
        // circuit reads no loop and zero efficiency and MUST bind its own direct
        // terms (the WI-039 EI-5 lesson) -- the mode is selected by the flags,
        // never by a fact. Every circuit and fit fact is unbound here (the
        // WI-044 D6 convention) and bound by the concrete instance.
        attribute loop_live : Real default 0.0;
        attribute p_pump_direct : Real default 0.0;
        attribute eta_p_direct : Real default 0.0;
        // circuit facts (instance-bound)
        attribute loop_T_in : Real;
        attribute loop_dT_blanket : Real;
        attribute loop_cp : Real;
        attribute loop_gamma : Real;
        attribute loop_p : Real;
        attribute n_loops : Real;
        attribute mdot_loop_ref : Real; // hydraulic normalization, not capacity
        attribute mdot_loop_rated : Real; // offered scalar circuit ceiling [kg/s]; not a machine map
        attribute equipment_helium_design_shaft_MW : Real; // [MW] supplied price point/stock
        attribute equipment_helium_design_suction_Pa : Real; // [Pa] supplied price point/stock
        attribute equipment_salt_design_flow_kg_s : Real; // [kg/s] supplied price point/stock
        attribute equipment_salt_design_head_m : Real; // [m] supplied price point/stock
        attribute equipment_salt_design_eta_p : Real; // [1] supplied price point/stock
        attribute equipment_salt_design_eta_motor : Real; // [1] supplied price point/stock
        attribute equipment_helium_purchased_mass_kg : Real; // [kg] supplied price point/stock
        attribute equipment_salt_purchased_mass_kg : Real; // [kg] supplied price point/stock

        attribute dp_loop_ref : Real;
        attribute f_loss : Real default 1.0;
        attribute eta_is : Real;
        attribute eta_drive : Real default 1.0;
        // WI-067: selected equipment scenario, independently switched cost and energy effects.
        attribute equipment_enabled : Boolean default false;
        attribute equipment_cost_mode : Real default 0.0;
        attribute secondary_energy_mode : Real default 0.0;
        attribute cooling_years : Real default 30.0;
        attribute cooling_discount : Real default 0.07;
        attribute cooling_cycle_argument : Real default 480.0;
        attribute equipment_layout_multiplier : Real default 1.0; // 1
        attribute equipment_tube_wall : Real default 0.0015; // m
        attribute equipment_shell_wall : Real default 0.2; // m
        attribute equipment_accessory_mass : Real default 10000.0; // kg
        attribute equipment_secondary_head : Real default 40.0; // m
        attribute equipment_eta_p : Real default 0.75; // 1
        attribute equipment_eta_motor : Real default 0.95; // 1
        attribute equipment_machine_life : Real default 10.0; // year
        attribute equipment_bundle_life : Real default 15.0; // year
        attribute equipment_makeup_fraction : Real default 0.001; // 1/year
        attribute equipment_inventory_reserve : Real default 0.1; // 1
        attribute equipment_removal_multiplier : Real default 1.0; // 1
        attribute equipment_saltprice_source_choice : Real default 0.0; // 1
        attribute equipment_costscale : Real default 1.0; // 1
        attribute equipment_stainless_fabrication_usd2017_per_kg : Real default 310 {
            doc /* **Source**: knowledge/sources/anl_2018_report_on_the_update_of_fuel_cycle_cost_algorithms/output.md **Ref**: sections 2.4, 3.6.2-3.6.3, printed 26-27. **Basis**: 310000 USD per metric tonne / 1000 kg per tonne = 310 USD2017/kg, delivered finished stainless fabrication. Shared by initial HX, both pipe bills and future bundle. January2017 source basis uses inherited annual CPI2017=245.1 to CPI2025=321.9 purchasing-power proxy, not equipment escalation. Conditional 240/360 source-family alternatives hold the carbon base fixed at 120 USD2017/kg times 2/3; target transfer and missing scope remain unbounded. **Last Updated**: 2026-09-19 */
        }
        attribute shipping_exclusion : Real = cooling_selection.shipping_exclusion;
        attribute replacement_annual : Real = cooling_selection.replacement_annual;
        attribute consumables_annual : Real = cooling_selection.consumables_annual;
        // C220200 coolant (two-term, plant-total; retained comparison mode).
        // 166.0 M$ -> $
        attribute coolant_primary_base : Real;
        // 40.6 M$ -> $
        attribute coolant_intermediate_base : Real;
        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----
        attribute n_mod : Real;   // <- 'MFE Power Plant'::n_mod
        attribute p_net : Real;   // <- pb.p_net
        attribute p_th : Real;   // <- pb.p_th
        attribute q_source : Real;   // <- blanket.q_source
        // ---- EXPOSEs (WI-057): this part's calc outputs, readable outside as <part>.<name> ----
        attribute T_out : Real = primary_loop.T_out;
        // WI-073: expose existing salt-boundary scenario, not a new technology.
        attribute conversion_heat_MW : Real = equipment.conversion_heat_MW;
        attribute salt_flow_per_circuit : Real = equipment.salt_flow;
        attribute salt_circuit_count : Real = equipment.ihx_count;
        attribute salt_return_C : Real = equipment.salt_return_C;
        attribute salt_hot_C : Real = 465.0 { doc /* **Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Existing WI-067 equipment scenario hot state. */ }
        attribute salt_cp_kJ_kgK : Real = 1.560 { doc /* **Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Existing WI-067 constant salt heat capacity1560J/kg/K, expressed kJ/kg/K. */ }

        attribute coolant_cost : Real = cooling_selection.cost;
        attribute hx_shell_bore : Real = equipment.hx_shell_bore;
        attribute hx_shell_wall : Real = equipment.hx_shell_wall;
        attribute hx_shell_length : Real = equipment.hx_shell_length;
        attribute hx_tube_length : Real = equipment.hx_tube_length;
        attribute helium_machine_count : Real = equipment.circulator_count;
        attribute salt_machine_count : Real = equipment.salt_pump_count;
        attribute exchanger_count : Real = equipment.ihx_count;
        attribute mdot_loop : Real = primary_loop.mdot_loop;
        attribute helium_represented_fill_margin_kg : Real = equipment.helium_represented_fill_margin_kg;
        attribute salt_represented_fill_margin_kg : Real = equipment.salt_represented_fill_margin_kg;
        attribute represented_fill_ok : Boolean = equipment.represented_fill_ok;
        attribute represented_fill_defined : Real = equipment.represented_fill_defined;
        attribute ihx_capacity_margin_m2 : Real = equipment.ihx_capacity_margin_m2;
        attribute ihx_capacity_defined : Real = equipment.ihx_capacity_defined;
        attribute machine_off_design_performance_qualified : Boolean = equipment.machine_off_design_performance_qualified;
        attribute p_loop_margin : Real = primary_loop.p_loop_margin;
        attribute p_pump_total : Real = cooling_energy.electric_total;
        attribute q_recovered_total : Real = cooling_energy.recovered_total;
        // ---- template calcs (WI-057): the analyses this part owns ----
        calc primary_loop : 'Primary Coolant Loop' {
            in q_source_in = q_source;
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
        calc equipment : 'Cooling Equipment' {
            in helium_design_shaft_MW_in = equipment_helium_design_shaft_MW;
            in helium_design_suction_Pa_in = equipment_helium_design_suction_Pa;
            in salt_design_flow_kg_s_in = equipment_salt_design_flow_kg_s;
            in salt_design_head_m_in = equipment_salt_design_head_m;
            in salt_design_eta_p_in = equipment_salt_design_eta_p;
            in salt_design_eta_motor_in = equipment_salt_design_eta_motor;
            in helium_purchased_mass_kg_in = equipment_helium_purchased_mass_kg;
            in salt_purchased_mass_kg_in = equipment_salt_purchased_mass_kg;

            in enabled_in = equipment_enabled;
            in n_mod_in = 'Primary Heat Transport'::n_mod;
            in n_loops_in = 'Primary Heat Transport'::n_loops;
            in mdot_loop_in = primary_loop.mdot_loop;
            in dp_loop_in = primary_loop.dp_loop;
            in helium_suction_K_in = primary_loop.T_comp_in;
            in helium_discharge_Pa_in = loop_p;
            in helium_hot_K_in = primary_loop.T_out;
            in helium_cp_in = loop_cp;
            in helium_gamma_in = loop_gamma;
            in primary_shaft_MW_in = primary_loop.w_fluid;
            in primary_electric_MW_in = primary_loop.p_elec;
            in q_ihx_MW_in = primary_loop.q_ihx;
            in layout_multiplier_in = equipment_layout_multiplier;
            in tube_wall_in = equipment_tube_wall;
            in shell_wall_in = equipment_shell_wall;
            in accessory_mass_in = equipment_accessory_mass;
            in secondary_head_in = equipment_secondary_head;
            in eta_p_in = equipment_eta_p;
            in eta_motor_in = equipment_eta_motor;
            in machine_life_in = equipment_machine_life;
            in bundle_life_in = equipment_bundle_life;
            in years_in = cooling_years;
            in discount_in = cooling_discount;
            in makeup_fraction_in = equipment_makeup_fraction;
            in inventory_reserve_in = equipment_inventory_reserve;
            in removal_multiplier_in = equipment_removal_multiplier;
            in saltprice_source_choice_in = equipment_saltprice_source_choice;
            in costscale_in = equipment_costscale;
            in stainless_fabrication_usd2017_per_kg_in = equipment_stainless_fabrication_usd2017_per_kg;
            in sourcefitargument_C_in = cooling_cycle_argument;
        }
        calc cooling_guard : 'Cooling Scenario Guard' {
            in equipment_enabled_in = equipment_enabled;
            in cost_mode_in = equipment_cost_mode;
            in energy_mode_in = secondary_energy_mode;
        }
        calc cooling_selection : 'Cooling Account Selection' {
            in cost_mode_in = cooling_guard.cost_mode;
            in legacy_cost_in = coolant.cost;
            in equipment_cost_in = equipment.installed_total;
            in delivered_in = equipment.delivered_total;
            in replacements_in = equipment.replacement_annual;
            in consumables_in = equipment.consumables_annual;
        }
        calc cooling_energy : 'Cooling Energy Addition' {
            in secondary_mode_in = cooling_guard.energy_mode;
            in primary_electric_in = primary_loop.p_pump_total;
            in primary_recovered_in = primary_loop.q_recovered_total;
            in salt_electric_in = equipment.salt_electric_MW;
            in salt_shaft_in = equipment.salt_shaft_MW;
        }
        part primary_circulators : 'Cooling Machine Account' {
            // mass_flow and shaft_power below are operating demands, not installed ratings.
            attribute design_shaft_power : Real = equipment.helium_design_shaft_MW;
            attribute design_suction_pressure : Real = equipment.helium_design_suction_Pa;
            :>> count = equipment.circulator_count;
            :>> mass_flow = equipment.circulator_flow;
            :>> shaft_power = equipment.circulator_shaft_MW;
            :>> capital_cost = equipment.primary_circulators_cost;
        }
        part primary_pipes : 'Cooling Pipe Account' {
            :>> steel_mass = equipment.primary_pipe_mass;
            :>> capital_cost = equipment.primary_piping_cost;
        }
        part intermediate_exchangers : 'Cooling Exchanger Account' {
            :>> count = equipment.ihx_count;
            :>> installed_area = equipment.ihx_installed_area;
            :>> required_area = equipment.ihx_required_area;
            :>> duty = equipment.ihx_duty_MW;
            :>> capital_cost = equipment.exchangers_cost;
        }
        part salt_pumps : 'Cooling Machine Account' {
            // mass_flow and shaft_power below are operating demands, not installed ratings.
            attribute design_mass_flow : Real = equipment.salt_design_flow_kg_s;
            attribute design_head : Real = equipment.salt_design_head_m;
            attribute design_shaft_power : Real = equipment.salt_design_shaft_MW;
            :>> count = equipment.salt_pump_count;
            :>> mass_flow = equipment.salt_pump_flow;
            :>> shaft_power = equipment.salt_pump_shaft_MW;
            :>> capital_cost = equipment.secondary_pumps_cost;
        }
        part salt_pipes : 'Cooling Pipe Account' {
            :>> steel_mass = equipment.secondary_pipe_mass;
            :>> capital_cost = equipment.secondary_piping_cost;
        }
        part coolant_inventory : 'Cooling Inventory Account' {
            :>> helium_mass = equipment.helium_inventory_mass;
            :>> salt_mass = equipment.salt_inventory_mass;
            :>> capital_cost = equipment.inventory_cost;
        }
        part initial_spares : 'Cooling Spares Account' {
            :>> capital_cost = equipment.spares_cost;
        }
        attribute legacy_cost_net_class_MWe : Real;
        calc legacy_cost_net_class_MWe_guard : 'Supplied Cost Class' {
            in class_in = legacy_cost_net_class_MWe;
        }
        attribute legacy_cost_net_class_MWe_checked : Real = legacy_cost_net_class_MWe_guard.value;
        attribute legacy_cost_thermal_class_MW : Real;
        calc legacy_cost_thermal_class_MW_guard : 'Supplied Cost Class' {
            in class_in = legacy_cost_thermal_class_MW;
        }
        attribute legacy_cost_thermal_class_MW_checked : Real = legacy_cost_thermal_class_MW_guard.value;
        calc coolant : 'Coolant Cost' {
            in primary_base = coolant_primary_base;
            in p_net = legacy_cost_net_class_MWe_checked;
            in intermediate_base = coolant_intermediate_base;
            in p_th_in = legacy_cost_thermal_class_MW_checked;
            in n_mod_in = n_mod;
        }
    }

    part def 'Cryoplant' {
        attribute rated_cryogenic_cold_K : Real default 0.0; // supplied [K]
        attribute rated_cryogenic_intercept_K : Real default 0.0; // supplied [K]
        attribute rated_cryogenic_ambient_K : Real default 0.0; // supplied [K]
        attribute rated_cold_W : Real default 0.0; // supplied [W]
        attribute rated_intercept_W : Real default 0.0; // supplied [W]
        attribute rated_direct_electric_MW : Real default 0.0; // supplied [MWe]
        calc cryogenic_offered_conditions : 'Cryogenic Offered Conditions' {
            in enabled_in = true;
            in actual_cold_K_in = T_cold_cryo;
            in rated_cold_K_in = rated_cryogenic_cold_K;
            in actual_intercept_K_in = T_shield;
            in rated_intercept_K_in = rated_cryogenic_intercept_K;
            in actual_ambient_K_in = T_amb_cryo;
            in rated_ambient_K_in = rated_cryogenic_ambient_K;
        }
        attribute cryogenic_rating_applicable : Boolean = cryogenic_offered_conditions.applicable;
        attribute cryogenic_rating_supported : Boolean = cryogenic_offered_conditions.supported;
        attribute cryogenic_rating_defined : Real = cryogenic_offered_conditions.evaluation_defined;
        calc cold_load_W_demand_conversion : 'Cold Load Watts' {
            in cold_MW_in = cold_load.p_cold;
        }
        attribute cold_load_W_required : Real = cold_load_W_demand_conversion.demand;
        calc cold_stage_capability : 'Offered Capacity Screen' {
            in rating_in = rated_cold_W;
            in demand_in = cold_load_W_required;
            in applicable_in = cryogenic_rating_applicable;
            in conditions_supported_in = cryogenic_rating_supported;
            in demand_available_in = true;
        }
        attribute cold_stage_margin : Real = cold_stage_capability.margin;
        attribute cold_stage_applicable : Boolean = cold_stage_capability.applicable;
        attribute cold_stage_supported : Boolean = cold_stage_capability.supported;
        attribute cold_stage_defined : Real = cold_stage_capability.evaluation_defined;
        attribute cold_stage_capacity_ok : Boolean = cold_stage_capability.capacity_ok;
        calc intercept_stage_capability : 'Offered Capacity Screen' {
            in rating_in = rated_intercept_W;
            in demand_in = inventory.q_inventory_shield;
            in applicable_in = cryogenic_rating_applicable;
            in conditions_supported_in = cryogenic_rating_supported;
            in demand_available_in = inventory_enabled;
        }
        attribute intercept_stage_margin : Real = intercept_stage_capability.margin;
        attribute intercept_stage_applicable : Boolean = intercept_stage_capability.applicable;
        attribute intercept_stage_supported : Boolean = intercept_stage_capability.supported;
        attribute intercept_stage_defined : Real = intercept_stage_capability.evaluation_defined;
        attribute intercept_stage_capacity_ok : Boolean = intercept_stage_capability.capacity_ok;
        calc direct_electric_capability : 'Offered Capacity Screen' {
            in rating_in = rated_direct_electric_MW;
            in demand_in = p_cryo;
            in applicable_in = true;
            in conditions_supported_in = true;
            in demand_available_in = true;
        }
        attribute direct_electric_margin : Real = direct_electric_capability.margin;
        attribute direct_electric_applicable : Boolean = direct_electric_capability.applicable;
        attribute direct_electric_supported : Boolean = direct_electric_capability.supported;
        attribute direct_electric_defined : Real = direct_electric_capability.evaluation_defined;
        attribute direct_electric_capacity_ok : Boolean = direct_electric_capability.capacity_ok;

        doc /*
        WI-079/MR-7: auxiliary cooling uses an independently selected procurement class; cryogenic capital consumes the supplied package amount. Cold/intercept heat loads and COP determine operating electrical demand separately. Selected capability is evaluated by the companion WI-080 screens.

        The cryogenic plant that holds the magnet cold mass at its operating temperature
        (20 K in the source). Owns the cryoplant chain facts (WI-024: nuclear heating uplift,
        fixed load, Carnot fraction, cold and ambient temperatures, the direct term), the coil
        cooling powers and the cryoplant cost base. WI-057.
        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/output.md
        **Ref**: sec. 2.10 (20 K operation); WI-024 design
        **Basis**: the cryoplant as the owner of the cold-load-to-electrical chain facts
        */
        // ---- ports (WI-057): the exchanges this part takes part in; declarative, see mfe_interfaces ----
        port heat_load_in : ~'Cryogenic Load Port';   // <- magnet.cold_mass (cryo_elec.q_nuc, vol_cold)
        port electric_in : ~'Electric Port';   // <- electric_plant.recirculating (pb.p_cryo, p_tfcool_in, p_pfcool_in)
        // directly-specified cryoplant electrical [MW] (additive direct term, WI-024)
        attribute inventory_enabled : Boolean default false;
        attribute n_coils : Real default 0.0;
        attribute c_coil : Real default 0.0;
        attribute wp_side : Real default 0.0;
        attribute I_turn : Real default 0.0;
        attribute n_leads : Real default 0.0;
        attribute L0 : Real default 0.0;
        attribute f_lead : Real default 1.0;
        attribute T_shield : Real default 77.0;
        attribute f_carnot_shield : Real default 1.0;
        attribute t_case : Real default 0.0;
        attribute shield_area_ratio : Real default 1.0;
        attribute eps_eff : Real default 0.0;
        attribute sigma_SB : Real default 0.0;
        attribute q_MLI : Real default 0.0;
        attribute g_per_coil : Real default 0.0;
        attribute k_c : Real default 0.0;
        attribute k_s : Real default 0.0;
        attribute joint_drive_fraction : Real default 0.0;
        attribute m_support : Real default 0.0;
        attribute q_nuc_structure : Real default 0.0;
        attribute rho_structure : Real default 1.0;
        attribute p_cryo : Real default 0.0;
        attribute p_fixed_cryo : Real default 0.0;
        attribute f_uplift_cryo : Real default 1.0;
        attribute T_cold_cryo : Real default 20.0;
        attribute T_amb_cryo : Real default 300.0;
        attribute f_carnot_cryo : Real default 1.0;
        // TF coil cooling [MW]
        attribute p_tfcool : Real;
        // PF coil cooling [MW]
        attribute p_pfcool : Real;
        // 200.0 M$ -> $
        attribute purchase_cost_per_module : Real;
        attribute aux_cost_thermal_class_MW : Real;
        calc aux_cost_thermal_class_MW_guard : 'Supplied Cost Class' {
            in class_in = aux_cost_thermal_class_MW;
        }
        attribute aux_cost_thermal_class_MW_checked : Real = aux_cost_thermal_class_MW_guard.value;
        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----
        attribute aux_per_mw : Real;   // <- 'MFE Power Plant'::aux_per_mw
        attribute n_mod : Real;   // <- 'MFE Power Plant'::n_mod
        attribute p_th : Real;   // <- pb.p_th
        attribute q_nuc_cryo : Real;   // <- magnet.winding_pack.q_nuc_cryo
        attribute vol_cold_total : Real;   // <- magnet.vol_cold_total
        // ---- EXPOSEs (WI-057): this part's calc outputs, readable outside as <part>.<name> ----
        attribute aux_cooling_cost : Real = aux_cooling.cost;
        attribute cryo_cost : Real = aux_cooling.cryo_cost;
        attribute p_elec : Real = refrigeration_sum.total;
        attribute p_drive : Real = inventory.p_drive;
        calc inventory : 'Coil Thermal Inventory' {
            in inventory_enabled = 'Cryoplant'::inventory_enabled;
            in n_coils = 'Cryoplant'::n_coils;
            in c_coil = 'Cryoplant'::c_coil;
            in wp_side = 'Cryoplant'::wp_side;
            in I_turn = 'Cryoplant'::I_turn;
            in n_leads = 'Cryoplant'::n_leads;
            in L0 = 'Cryoplant'::L0;
            in f_lead = 'Cryoplant'::f_lead;
            in T_cold = T_cold_cryo;
            in T_shield = 'Cryoplant'::T_shield;
            in T_amb = T_amb_cryo;
            in f_carnot_cold = f_carnot_cryo;
            in f_carnot_shield = 'Cryoplant'::f_carnot_shield;
            in t_case = 'Cryoplant'::t_case;
            in shield_area_ratio = 'Cryoplant'::shield_area_ratio;
            in eps_eff = 'Cryoplant'::eps_eff;
            in sigma_SB = 'Cryoplant'::sigma_SB;
            in q_MLI = 'Cryoplant'::q_MLI;
            in g_per_coil = 'Cryoplant'::g_per_coil;
            in k_c = 'Cryoplant'::k_c;
            in k_s = 'Cryoplant'::k_s;
            in p_joint = p_fixed_cryo;
            in joint_drive_fraction = 'Cryoplant'::joint_drive_fraction;
        }
        calc cold_load : 'Cold Load Sum' {
            in q_nuc = q_nuc_cryo;
            in vol_cold = vol_cold_total;
            in p_fixed = p_fixed_cryo;
            in f_uplift = f_uplift_cryo;
            in q_nuc_structure = 'Cryoplant'::q_nuc_structure;
            in m_support = 'Cryoplant'::m_support;
            in rho_structure = 'Cryoplant'::rho_structure;
            in q_inventory_cold = inventory.q_inventory_cold;
        }
        calc shield_elec : 'Intercept Electrical Power' {
            in inventory_enabled = 'Cryoplant'::inventory_enabled;
            in q_shield = inventory.q_inventory_shield;
            in T_shield = 'Cryoplant'::T_shield;
            in T_amb = T_amb_cryo;
            in f_carnot = f_carnot_shield;
        }
        calc refrigeration_sum : 'Electrical Power Sum' {
            in p_a = cryo_elec.p_elec;
            in p_b = shield_elec.p_elec;
        }

        // ---- template calcs (WI-057): the analyses this part owns ----
        calc cryo_elec : 'Cryoplant Electrical Power' {
            in q_nuc = 0.0;
            in vol_cold = 0.0;
            in p_fixed = cold_load.p_cold;
            in f_uplift = 1.0;
            in T_cold = T_cold_cryo;
            in T_amb = T_amb_cryo;
            in f_carnot = f_carnot_cryo;
            in p_direct = p_cryo;
        }
        calc aux_cooling : 'Supplied Auxiliary Cooling Cost' {
            in aux_per_mw_in = aux_per_mw;
            in thermal_class_in = aux_cost_thermal_class_MW_checked;
            in purchase_cost_in = purchase_cost_per_module;
            in n_mod_in = n_mod;
        }
    }

    part def 'Fuel Stock' {
        doc /* Tritium held by one fuel-cycle process or storage policy. atoms [T atoms] and mass_kg [kg T] are nominal stock, not throughput.
        **Source**: work/active/WI-069_fuel-inventory-and-startup/design.md **Reference**: Components and stocks. **Last Updated**: 2026-09-19 */
        attribute atoms : Real;
        attribute mass_kg : Real;
    }

    part def 'Fuel Processing Stock' :> 'Fuel Stock', 'Costed Component' {
        doc /* Per-module tritium stock with a plant-total processing account attached for rollup. Source: work/active/WI-070_throughput-based-fuel-processing-costs/design.md. Basis: mass remains per module; capital is selected whole-plant C220500 including legacy mode, summed only by Fuel Cycle account. */
        attribute equipment_cost : Real;
        attribute installation_cost : Real;
        attribute capacity_kg_s : Real; // supplied per-module D+T throughput
        :>> cas_code = "220500";
    }

    part def 'Fuel Cycle' {
        doc /*
        The tritium fuel cycle: the D-T fuel cost facts and the reduced flows of WI-047 (burn
        fraction, recovery and recycle, extraction efficiency, decay, inventory and stock
        growth), the tritium-systems power and the fuel-handling cost base. Tritium is bred in
        the blanket (see 'Blanket'::tbr) and returned to the plasma. WI-057.
        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/output.md
        **Ref**: blanket and fuel-cycle statements (TBR 1.074, Table 6 image page_021_table_0.png); WI-047 design
        **Basis**: the fuel cycle as the owner of the flow and fuel-cost facts
        */
        // ---- ports (WI-057): the exchanges this part takes part in; declarative, see mfe_interfaces ----
        port tritium_in : ~'Material Port';   // <- blanket.tritium_out
        port fuel_out : 'Material Port';   // -> plasma.fuel_in
        port exhaust_out : 'Material Port';   // -> vacuum_pumping.exhaust_in (vacuum.exhaust_rate_*_in, helium_rate_in)
        port electric_in : ~'Electric Port';   // <- electric_plant.recirculating (pb.p_trit_in)
        // ---- CAS80 DT fuel: raw annual, then the same levelization wrapper ----
        // Fuel chemistry constants are instance inputs (MR-3) -- no library defaults.
        // M_D*u_D + M_Li6*u_Li6 [$/rxn]
        attribute fuel_cost_per_rxn : Real;
        // per-reaction energy [MeV]
        attribute fuel_q_eff : Real;
        // MeV -> J
        attribute mev_to_joules : Real;
        attribute burn_fraction : Real;
        attribute fuel_recovery : Real;
        // ---- Fuel-cycle flows (WI-047): conservation on the same reactions the
        // cost prices; transport-driven instances add a separate conditional
        // adequacy assertion using the exposed requirement. Dormant-safe by
        // the WI-024 pattern: a concept binding nothing gets a lossless loop.
        // recovery fraction of the unburned tritium stream [1]
        attribute t_recycle : Real default 1.0;
        // breeder-to-supply extraction efficiency [1]
        attribute eta_extract : Real default 1.0;
        // tritium decay constant [1/s]
        attribute lambda_T : Real default 0.0;
        // held tritium inventory [atoms]
        attribute I_total : Real = inventory.total_atoms;
        // required stock growth [atoms/s]
        attribute G_stock : Real default 0.0;
        // tritium atomic mass [kg]
        attribute m_T_kg : Real default 0.0;
        // tritium systems [MW]
        attribute p_trit : Real;
        // fh_base[fuel] [$]
        attribute fuel_handling_base : Real;
        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----
        attribute availability : Real;   // <- calendar.availability
        attribute n_mod : Real;   // <- 'MFE Power Plant'::n_mod
        attribute p_fus : Real;   // <- plasma.p_fus
        attribute p_net : Real;   // <- pb.p_net
        attribute tbr : Real;   // <- blanket.tbr
        // ---- EXPOSEs (WI-057): this part's calc outputs, readable outside as <part>.<name> ----
        attribute annual_fuel : Real = fuel_calc.annual_fuel;
        attribute burn_rate : Real = fuel.burn_rate;
        attribute loss_rate : Real = fuel.loss_rate;
        attribute tbr_required : Real = fuel.tbr_required;
        // For computed blankets this raw margin is defined only when the owning plant adequacy flag is 1.
        attribute tbr_margin : Real = fuel.tbr_margin;
        attribute exhaust_rate : Real = fuel.exhaust_rate;
        attribute fuel_handling_cost : Real = processing_cost.cost;
        attribute dt_processing_flow : Real = inventory.dt_processor_kg_s;
        attribute fuel_processing_installation : Real = processing_cost.installation_total;
        attribute fuel_processing_defined : Real = processing_cost.defined_flag;
        attribute processing_capacity_evaluation_defined : Real = processing_cost.capacity_evaluation_defined;
        attribute processing_capacity_margin_kg_s : Real = processing_cost.capacity_margin_kg_s;
        // ---- template calcs (WI-057): the analyses this part owns ----

        // WI-069 dormant generic defaults; stellarator binds the reviewed scenario.
        attribute inventory_enabled : Boolean default := false; // 1; activation
        attribute held_inventory : Real default := 0.0; // T atoms; dormant legacy amount
        attribute breeding_defined : Real default := 1.0; // 1; exact 0/1
        attribute m_D_kg : Real default := 0.0; // kg/D atom
        attribute plasma_volume : Real default := 0.0; // m^3
        attribute n_T0 : Real default := 0.0; // T atoms/m^3
        attribute alpha_n : Real default := 0.0; // 1; > -1
        attribute tau_feed : Real default := 0.0; // s
        attribute tau_process : Real default := 0.0; // s
        attribute tau_blanket : Real default := 0.0; // s
        attribute tau_extract : Real default := 0.0; // s
        attribute tau_buffer : Real default := 0.0; // s
        attribute tau_reserve : Real default := 0.0; // s
        attribute startup_extension : Real default := 0.0; // s
        attribute shutdown_duration : Real default := 0.0; // s
        attribute reserve_fraction : Real default := 0.0; // 1; [0,1]
        attribute s_per_year : Real default := 31536000.0; // s/year; existing model 8760-hour year
        calc inventory : 'Fuel Inventory' {
            in enabled_in = inventory_enabled;
            in held_inventory_in = held_inventory;
            in p_fus_in = p_fus;
            in q_eff_in = fuel_q_eff;
            in mev_to_joules_in = mev_to_joules;
            in burn_fraction_in = burn_fraction;
            in t_recycle_in = t_recycle;
            in tbr_available_in = tbr;
            in breeding_defined_in = breeding_defined;
            in eta_extract_in = eta_extract;
            in lambda_T_in = lambda_T;
            in G_stock_in = G_stock;
            in m_T_kg_in = m_T_kg;
            in m_D_kg_in = m_D_kg;
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
            in availability_in = availability;
            in s_per_year_in = s_per_year;
        }
        part feed_equipment : 'Fuel Stock' {
            doc /* Injection machinery; stream F, residence tau_feed, prefilled. **Source**: work/active/WI-069_fuel-inventory-and-startup/design.md **Reference**: Components and stocks. **Last Updated**: 2026-09-19 */
            :>> atoms = inventory.feed_atoms;
            :>> mass_kg = inventory.feed_kg;
        }
        part plasma_inventory : 'Fuel Stock' {
            doc /* Plasma fuel content; density profile integral, prefilled; F=B+U. **Source**: work/active/WI-069_fuel-inventory-and-startup/design.md **Reference**: Components and stocks. **Last Updated**: 2026-09-19 */
            :>> atoms = inventory.plasma_atoms;
            :>> mass_kg = inventory.plasma_kg;
        }
        part exhaust_processor : 'Fuel Processing Stock' {
            doc /* Combined cleanup and isotope separation; inlet U, residence tau_process; R+L=U at outlet. **Source**: work/active/WI-069_fuel-inventory-and-startup/design.md **Reference**: Components and stocks. **Last Updated**: 2026-09-19 */
            :>> atoms = inventory.processor_atoms;
            :>> mass_kg = inventory.processor_kg;
            // Per-module stock above; plant-total selected cost below, including dormant legacy.
            :>> capital_cost = processing_cost.cost;
            :>> equipment_cost = processing_cost.equipment_total;
            :>> installation_cost = processing_cost.installation_total;
            :>> capacity_kg_s = processing_cost.capacity_kg_s;
        }
        part breeder_zone : 'Fuel Stock' {
            doc /* Release from breeder zone; gross T stream J, residence tau_blanket; starts empty. **Source**: work/active/WI-069_fuel-inventory-and-startup/design.md **Reference**: Components and stocks. **Last Updated**: 2026-09-19 */
            :>> atoms = inventory.blanket_atoms;
            :>> mass_kg = inventory.blanket_kg;
        }
        part extraction_equipment : 'Fuel Stock' {
            doc /* Extraction; gross T stream J, residence tau_extract; S plus extraction loss at outlet; starts empty. **Source**: work/active/WI-069_fuel-inventory-and-startup/design.md **Reference**: Components and stocks. **Last Updated**: 2026-09-19 */
            :>> atoms = inventory.extraction_atoms;
            :>> mass_kg = inventory.extraction_kg;
        }
        part working_storage : 'Fuel Stock' {
            doc /* Usable supply buffer; inlet recycled and extracted T, stock F*tau_buffer; prefilled. **Source**: work/active/WI-069_fuel-inventory-and-startup/design.md **Reference**: Components and stocks. **Last Updated**: 2026-09-19 */
            :>> atoms = inventory.buffer_atoms;
            :>> mass_kg = inventory.buffer_kg;
        }
        part reserve_storage : 'Fuel Stock' {
            doc /* Separate interruption reserve; F*q*tau_reserve, counted once; prefilled. **Source**: work/active/WI-069_fuel-inventory-and-startup/design.md **Reference**: Components and stocks. **Last Updated**: 2026-09-19 */
            :>> atoms = inventory.reserve_atoms;
            :>> mass_kg = inventory.reserve_kg;
        }
        calc fuel : 'Fuel Cycle Flows' {
            in p_fus_in = p_fus;
            in q_eff_in = fuel_q_eff;
            in mev_to_joules_in = mev_to_joules;
            in burn_fraction_in = burn_fraction;
            in t_recycle_in = t_recycle;
            in tbr_available_in = tbr;
            in eta_extract_in = eta_extract;
            in lambda_T_in = lambda_T;
            in I_total_in = I_total;
            in G_stock_in = G_stock;
            in m_T_kg_in = m_T_kg;
        }
        calc fuel_calc : 'DT Fuel Cost' {
            in p_fus = 'Fuel Cycle'::p_fus;
            in n_mod_in = n_mod;
            in availability_in = availability;
            in cost_per_rxn = fuel_cost_per_rxn;
            in q_eff = fuel_q_eff;
            in mev_to_joules_in = mev_to_joules;
            in burn_fraction_in = burn_fraction;
            in fuel_recovery_in = fuel_recovery;
        }

        // WI-070 dormant source placeholders; active source data belong to instance.
        attribute processing_enabled : Boolean default := false;
        attribute processing_source_conditions : Boolean default := false;
        attribute processing_capacity_kg_s : Real default := 0.0;
        attribute processing_price_multiplier : Real default := 1.0;
        attribute processing_reference_flow : Real default := 0.0;
        attribute processing_exponent : Real default := 0.0;
        attribute processing_target_cpi : Real default := 0.0;
        attribute processing_transfer_cpi : Real default := 0.0;
        attribute processing_transfer_capital : Real default := 0.0;
        attribute processing_transfer_installation : Real default := 0.0;
        attribute processing_cleanup_cpi : Real default := 0.0;
        attribute processing_cleanup_capital : Real default := 0.0;
        attribute processing_cleanup_installation : Real default := 0.0;
        attribute processing_distiller_cpi : Real default := 0.0;
        attribute processing_distiller_capital : Real default := 0.0;
        attribute processing_distiller_installation : Real default := 0.0;
        attribute processing_containment_cpi : Real default := 0.0;
        attribute processing_containment_capital : Real default := 0.0;
        attribute processing_containment_installation : Real default := 0.0;
        calc processing_cost : 'Fuel Processing Cost' {
            in flow_in = dt_processing_flow;
            in inventory_enabled_in = inventory_enabled;
            in n_mod_in = n_mod;
            in legacy_cost_in = fuel_handling.cost;
            in enabled_in = processing_enabled;
            in source_conditions_in = processing_source_conditions;
            in capacity_in = processing_capacity_kg_s;
            in price_multiplier_in = processing_price_multiplier;
            in reference_flow_in = processing_reference_flow;
            in exponent_in = processing_exponent;
            in target_cpi_in = processing_target_cpi;
            in transfer_cpi_in = processing_transfer_cpi;
            in transfer_capital_in = processing_transfer_capital;
            in transfer_installation_in = processing_transfer_installation;
            in cleanup_cpi_in = processing_cleanup_cpi;
            in cleanup_capital_in = processing_cleanup_capital;
            in cleanup_installation_in = processing_cleanup_installation;
            in distiller_cpi_in = processing_distiller_cpi;
            in distiller_capital_in = processing_distiller_capital;
            in distiller_installation_in = processing_distiller_installation;
            in containment_cpi_in = processing_containment_cpi;
            in containment_capital_in = processing_containment_capital;
            in containment_installation_in = processing_containment_installation;
        }
        attribute legacy_cost_net_class_MWe : Real;
        calc legacy_cost_net_class_MWe_guard : 'Supplied Cost Class' {
            in class_in = legacy_cost_net_class_MWe;
        }
        attribute legacy_cost_net_class_MWe_checked : Real = legacy_cost_net_class_MWe_guard.value;
        calc fuel_handling : 'Plant Power-Law Cost' {
            in base = fuel_handling_base; in power = legacy_cost_net_class_MWe_checked; in n_mod_in = n_mod;
            in ref_power = 1000.0; in alpha = 0.7;
        }
    }

    part def 'Vacuum Pumping' {
        doc /*
        The torus exhaust pumping: the exhaust gas temperature and pressure the gas-load calc
        reads (WI-047; the source prints neither). WI-057.
        **Source**: work/active/WI-047_fuel-divertor-vacuum-flows/design.md
        **Ref**: the vacuum gas load
        **Basis**: the pumping system as the owner of the exhaust-state facts
        */
        // ---- ports (WI-057): the exchanges this part takes part in; declarative, see mfe_interfaces ----
        port exhaust_in : ~'Material Port';   // <- fuel_cycle.exhaust_out
        // ---- Torus exhaust gas load (WI-047): a 50/50 D-T fuel exhausts equal
        // deuterium and tritium streams; the helium ash is one atom per reaction.
        attribute T_gas : Real default 1.0;
        attribute p_exhaust : Real default 1.0;
        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----
        attribute burn_rate : Real;   // <- fuel_cycle.burn_rate
        attribute exhaust_rate : Real;   // <- fuel_cycle.exhaust_rate
        // ---- template calcs (WI-057): the analyses this part owns ----
        calc vacuum : 'Vacuum Gas Load' {
            in exhaust_rate_D_in = exhaust_rate;
            in exhaust_rate_T_in = exhaust_rate;
            in helium_rate_in = burn_rate;
            in T_gas_in = T_gas;
            in p_exhaust_in = p_exhaust;
        }
    }
}
