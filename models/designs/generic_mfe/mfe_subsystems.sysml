package mfe_subsystems {
    private import mfe_facilities::*;
    private import mfe_facilities_parts::*;
    private import ScalarValues::*;
    private import mfe_interfaces::*;
    private import mfe_power_cycle::*;
    private import mfe_matched_steam_cycle::*;
    private import mfe_steam_cycle_components::*;
    private import mfe_power_balance::*;
    private import mfe_account_costs::*;
    private import mfe_cryo_inventory::*;
    private import mfe_tritium_breeding::*;
    private import cas_hierarchy::*;
    private import economic_parameter::'CAS Scope';
    private import mfe_radial_build_parts::*;

    // =========================================================================
    // Shared power-core and balance-of-plant costed components for the generic
    // MFE plant. These are the concept-agnostic accounts NOT already defined by
    // WI-009's mfe_power_core (which owns the mfe-divergent 'Magnet System',
    // 'Heating and CD', 'Divertor'). Each specializes a cas_hierarchy account
    // type and carries its cost-driver attributes, mirroring the WI-009 magnet
    // pattern and the ife_subsystems costed-component idiom. All attributes are
    // concept inputs (WI-011); `capital_cost` (inherited from 'Costed
    // Component') is populated by the matching mfe_account_costs calc, bound in
    // the plant. No concept-specific values here (MR-3).
    //
    // CAS numbering note: this file follows the project cas_hierarchy
    // (CAS23 turbine, CAS24 electric, CAS25 heat rejection, CAS26 misc). The
    // 1costingFE source swaps 25/26 (CAS25 misc, CAS26 heat rejection); the
    // account_name and cost basis are preserved, only the CAS integer follows
    // the project convention.
    // =========================================================================

    // --- Shared power-core sub-accounts (CAS22.1.x, scope = shared) ---

    part def 'Blanket' :> 'CAS22 Power Core' {
        // ---- ports (WI-057): the exchanges this part takes part in; declarative, see mfe_interfaces ----
        port neutron_in : ~'Neutron Port';   // <- plasma.neutron_out
        port heat_in : ~'Thermal Port';   // <- heating.power_to_plasma is accounted here (source_heat.p_input_in = p_coupled)
        port coolant : 'Thermal Port';   // -> heat_transport.hot_in. the connection where the coolant premise lives structurally: the model's loop is WI-045's representative helium circuit (Moscato 2017, EU DEMO HCLL balance of plant); the Stellaris source cools the breeding zone with water at PWR conditions and the first wall with helium at 8 MPa (stellaris-design-details output.md lines 1490-1491, 1534-1536) -- goal structural-decomposition fact 6, surfaced and carried as a follow-on, not changed by WI-057
        port tritium_out : 'Material Port';   // -> fuel_cycle.tritium_in (fuel.tbr_available_in = blanket.tbr)
        // WI-057: the blanket's own facts, moved from the plant (formerly plant-level inputs)
        attribute blanket_t : Real default 0.70;
        attribute reflector_t : Real default 0.20;
        // Power-balance inputs (WI-011).
        // neutron energy multiplier
        attribute mn : Real;
        // achieved tritium breeding ratio [1] -- a concept's source-conditioned value;
        // dormant 1.0 (no breeding claim). Declared here so the fuel flows can read
        // it on the generic plant; an instance redefines it (WI-047; before, the
        // Stellaris instance declared it alone for its own tbr_ok fence).
        attribute tbr : Real default 1.0;
        // WI-057: the first wall is a part of the blanket module (the C220101 account prices both)
        part first_wall : 'First Wall';
        doc /*
        CAS22.1.1 First wall + breeding blanket + neutron multiplier.
        Concept-agnostic shared power-core account. Cost drivers below feed
        'Blanket Cost' (mfe_account_costs); WI-011 sets the values.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:252-254 (c220101)
        **Basis**: DI-002 -- blanket is a shared (concept-agnostic) CAS22 account
        */
        :>> scope = 'CAS Scope'::shared;

        attribute unit_cost : Real;
        attribute structure_factor : Real;
        attribute blanket_vol : Real;
        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----
        attribute p_coupled : Real;   // <- operating_heat.p_coupled (WI-050: the operating demand)
        attribute p_fus : Real;   // <- plasma.p_fus
        attribute p_th : Real;   // <- pb.p_th
        // ---- EXPOSEs (WI-057): this part's calc outputs, readable outside as <part>.<name> ----
        attribute q_source : Real = source_heat.q_source;
        attribute calibration : Real = first_wall.calibration;   // the first wall's, re-exposed
        attribute wall_load : Real = first_wall.wall_load;   // the first wall's, re-exposed
        attribute wall_load_peak : Real = first_wall.wall_load_peak;   // the first wall's, re-exposed
        :>> capital_cost = blanket_cost.cost;
        // ---- template calcs (WI-057): the analyses this part owns ----
        // Blanket (CAS22.1.1).
        // WI-050: retained power-scaled equipment costs are design-point sizing
        // estimates, including blanket/shield/structure/vessel/supplies/divertor,
        // turbine/electric/rejection/miscellaneous, buildings and CAS22 tail.
        // Their operating-power operands are retained under the reviewed cost
        // classification; heating procurement alone follows installed delivery.
        calc blanket_cost : 'Blanket Cost' {
            in unit_cost = 'Blanket'::unit_cost;
            in structure_factor = 'Blanket'::structure_factor;
            in blanket_vol = 'Blanket'::blanket_vol;
            in p_th_in = p_th;
        }
        // WI-045: the reactor's source heat (no pump credit), the representative
        // primary loop and the temperature-compatible cycle, upstream of the
        // power balance. Dataflow: fusion, heat -> source_heat -> primary_loop -> cycle -> pb.
        calc source_heat : 'Reactor Source Heat' {
            in p_nrl = p_fus;
            in p_input_in = p_coupled;
            in mn_in = mn;
        }
    }

    part def 'Transport Calculated Blanket' :> 'Blanket' {
        doc /* Blanket specialization with its own computed breeding response. The base Blanket keeps its held tbr interface for other concepts. Geometry owned by sibling parts enters through explicit attributes; material/source assumptions remain in the immutable response manifest. All breeding-derived outputs and raw downstream fuel margins are undefined when breeding_defined is zero.
        **Source**: work/active/WI-066_computed-tritium-breeding/design.md
        **Reference**: work/active/WI-066_computed-tritium-breeding/evidence/interface-probe.md
        **Last Updated**: 2026-09-18 */
        attribute breeding_R : Real;
        attribute breeding_a : Real;
        attribute breeding_kappa : Real;
        attribute breeding_ht_shield_t : Real;
        attribute breeding_structure_t : Real;
        attribute breeding_gap1_t : Real;
        attribute breeding_vessel_t : Real;
        calc breeding : 'Blanket Tritium Breeding' {
            in blanket_t_in = blanket_t;
            in R_in = breeding_R;
            in a_in = breeding_a;
            in kappa_in = breeding_kappa;
            in vacuum_t_in = first_wall.vacuum_t;
            in firstwall_t_in = first_wall.firstwall_t;
            in reflector_t_in = reflector_t;
            in ht_shield_t_in = breeding_ht_shield_t;
            in structure_t_in = breeding_structure_t;
            in gap1_t_in = breeding_gap1_t;
            in vessel_t_in = breeding_vessel_t;
        }
        :>> tbr = breeding.tbr_mean;
        attribute tbr_li6 : Real = breeding.tbr_li6;
        attribute tbr_li7 : Real = breeding.tbr_li7;
        attribute tbr_std_error : Real = breeding.tbr_std_error;
        attribute interpolation_allowance : Real = breeding.interpolation_allowance;
        attribute tbr_lower : Real = breeding.tbr_lower;
        attribute breeding_defined : Real = breeding.defined_flag;
    }

    part def 'Shield' :> 'CAS22 Power Core' {
        // WI-057: the shield's own facts, moved from the plant (formerly plant-level inputs)
        attribute ht_shield_t : Real default 0.20;
        attribute lt_shield_t : Real default 0.15;
        doc /*
        CAS22.1.2 Shield (high-temperature + low-temperature + bioshield).
        Concept-agnostic shared power-core account. Cost drivers feed
        'Shield Cost'.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:267-269 (c220102)
        **Basis**: DI-002 -- shield is a shared (concept-agnostic) CAS22 account
        */
        :>> scope = 'CAS Scope'::shared;

        attribute unit_cost : Real;
        attribute shield_scale : Real;
        attribute shield_vol : Real;
        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----
        attribute p_th : Real;   // <- pb.p_th
        :>> capital_cost = shield_cost.cost;
        // ---- template calcs (WI-057): the analyses this part owns ----
        // Shield (CAS22.1.2).
        calc shield_cost : 'Shield Cost' {
            in unit_cost = 'Shield'::unit_cost;
            in shield_vol = 'Shield'::shield_vol;
            in shield_scale = 'Shield'::shield_scale;
            in p_th_in = p_th;
        }
    }

    part def 'Primary Structure' :> 'CAS22 Power Core' {
        // WI-057: the structure's own facts, moved from the plant (formerly plant-level inputs)
        attribute structure_t : Real default 0.15;
        attribute residual_fraction : Real default 1.0;
        attribute legacy_cost : Real = structure_cost.legacy_cost;
        doc /*
        CAS22.1.5 Primary structure and support (gravity supports, thermal
        shields, inter-coil structure, machine base) in legacy mode. WI-059
        total-support instances explicitly reallocate a residual_fraction budget
        to nonmagnet infrastructure; this is not a measured split. Cost drivers feed
        'Structure Cost'.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:501 (c220105)
        **Basis**: DI-002 -- primary structure is a shared CAS22 account
        */
        :>> scope = 'CAS Scope'::shared;

        attribute unit_cost : Real;
        attribute structure_vol : Real;
        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----
        attribute p_et : Real;   // <- pb.p_et
        :>> capital_cost = structure_cost.cost;
        // ---- template calcs (WI-057): the analyses this part owns ----
        // Primary structure (CAS22.1.5).
        calc structure_cost : 'Structure Cost' {
            in residual_fraction = 'Primary Structure'::residual_fraction;
            in unit_cost = 'Primary Structure'::unit_cost;
            in structure_vol = 'Primary Structure'::structure_vol;
            in p_et_in = p_et;
        }
    }

    part def 'Vacuum Vessel' :> 'CAS22 Power Core' {
        // WI-057: the vessel's own facts, moved from the plant (formerly plant-level inputs)
        attribute vessel_t : Real default 0.10;
        attribute gap1_t : Real default 0.10;
        doc /*
        CAS22.1.6 Vacuum vessel (double-walled SS chamber, ports, gauges).
        Cost drivers feed 'Vessel Cost' (vessel-shell term only; the gas-load
        pumping term is a Stage-3 deepening item).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:515 (c220106_vessel)
        **Basis**: DI-002 -- vacuum vessel is a shared CAS22 account
        */
        :>> scope = 'CAS Scope'::shared;

        attribute unit_cost : Real;
        attribute vessel_vol : Real;
        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----
        attribute p_et : Real;   // <- pb.p_et
        :>> capital_cost = vessel_cost.cost;
        // ---- template calcs (WI-057): the analyses this part owns ----
        // Vacuum vessel (CAS22.1.6, shell term).
        calc vessel_cost : 'Vessel Cost' {
            in unit_cost = 'Vacuum Vessel'::unit_cost;
            in vessel_vol = 'Vacuum Vessel'::vessel_vol;
            in p_et_in = p_et;
        }
    }

    part def 'Power Supplies' :> 'CAS22 Power Core' {
        // ---- ports (WI-057): the exchanges this part takes part in; declarative, see mfe_interfaces ----
        port electric_in : ~'Electric Port';   // <- electric_plant.recirculating (pb.p_tf_in, p_pf_in)
        // WI-057: the power_supplies's own facts, moved from the plant (formerly plant-level inputs)
        // TF coil power [MW]
        attribute p_tf : Real;
        attribute p_tf_extra : Real default 0.0;
        attribute p_tf_total : Real = tf_power.total;
        calc tf_power : 'Electrical Power Sum' {
            in p_a = p_tf;
            in p_b = p_tf_extra;
        }
        // PF coil power [MW]
        attribute p_pf : Real;
        doc /*
        CAS22.1.7 Power supplies (steady-state: high-current DC for SC magnets,
        switchgear). Cost driver feeds 'Power Supplies Cost'. This is a demand-matched aggregate price proxy driven by gross electric output, not an evaluation of a supplied converter rating or installed power-supply adequacy.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
        **Ref**: cas22.py:554 (c220107 steady-state)
        **Basis**: DI-002 -- power supplies is a shared CAS22 account
        */
        :>> scope = 'CAS Scope'::shared;

        attribute base : Real;
        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----
        attribute p_et : Real;   // <- pb.p_et
        :>> capital_cost = power_supplies_cost.cost;
        // ---- template calcs (WI-057): the analyses this part owns ----
        // Power supplies (CAS22.1.7).
        calc power_supplies_cost : 'Power Supplies Cost' {
            in base = 'Power Supplies'::base;
            in p_et_in = p_et;
        }
    }

    // --- Balance-of-plant accounts (CAS23-26, scope = shared) ---

    part def 'Turbine Plant' :> 'CAS23 Turbine Plant' {
        // ---- ports (WI-057): the exchanges this part takes part in; declarative, see mfe_interfaces ----
        port coolant : ~'Thermal Port';   // <- heat_transport.hot_out
        port gross_electric : 'Electric Port';   // -> electric_plant.gross_in (pb.eta_th_in -> p_et)
        // WI-057: the turbine's own facts, moved from the plant (formerly plant-level inputs)
        attribute cycle_live : Real default 0.0;
        attribute eta_th_direct : Real default 0.0;
        // fit facts (instance-bound)
        attribute dT_approach : Real;
        attribute a_fit : Real;
        attribute b_fit : Real;
        attribute T_offset_fit : Real;
        attribute T2_min : Real;
        attribute T2_max : Real;
        attribute delta_eta : Real default 0.0;
        doc /*
        WI-078/MR-7 scope: capital_cost is a demand-matched equipment cost proxy driven by computed gross thermal-electric output. It does not price an independently supplied turbine nameplate or evaluate installed turbine/steam-generator capacity. Matched-cycle steam flow, shaft work and required UA describe the operating point, not installed ratings; turbine and steam-generator equipment qualification remain absent.

        CAS23 Turbine plant equipment (steam TG, condenser, feedwater). Linear
        in thermal-electric power; cost driver feeds 'Linear Power Cost' with
        power = p_the.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
        **Ref**: costs.py:154 (cas23_turbine)
        **Basis**: Concept-agnostic thermal conversion, power-cycle-set $/MW
        */
        :>> scope = 'CAS Scope'::shared;

        attribute cost_per_mw : Real;
        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----
        attribute T_out : Real;   // <- heat_transport.T_out
        attribute n_mod : Real;   // <- 'MFE Power Plant'::n_mod
        attribute p_the : Real;   // <- pb.p_the
        // ---- EXPOSEs (WI-057): this part's calc outputs, readable outside as <part>.<name> ----
        attribute domain_product : Real = cycle.domain_product;
        // WI-067: inherited fit argument, not a solved salt/steam inlet state.
        attribute cycle_argument : Real = cycle.T2_C;
        attribute eta_th : Real = cycle_selection.eta_selected;
        :>> capital_cost = turbine_cost.cost;
        // ---- template calcs (WI-057): the analyses this part owns ----
        calc cycle : 'Power Cycle Efficiency' {
            in T_hot_in = T_out;
            in dT_approach_in = dT_approach;
            in a_fit_in = a_fit;
            in b_fit_in = b_fit;
            in T_offset_fit_in = T_offset_fit;
            in T2_min_in = T2_min;
            in T2_max_in = T2_max;
            in delta_eta_in = delta_eta;
            in cycle_live_in = cycle_live;
            in eta_th_direct_in = eta_th_direct;
        }
        // WI-073 matched state calculation; generic inactive before property evaluation.
        attribute matched_cycle_enabled : Real default 0.0;
        attribute pump_motor_efficiency : Real default 0.0;
        port pump_electric_in : ~'Electric Port';
        port cycle_rejection : 'Heat Duty Port';
        port conversion_losses : 'Heat Duty Port';
        // Conversion-loss boundary collects mechanical, generator and pump-motor losses.
        // Total rejection is q_rejection_before_cooling_MW, not condenser duty alone.
        attribute cycle_heat_available_MW : Real default 0.0;
        attribute cycle_source_heat_MW : Real default 0.0;
        attribute cycle_selected_recovered_MW : Real default 0.0;
        attribute cycle_salt_flow_per_circuit : Real default 0.0;
        attribute cycle_salt_circuit_count : Real default 0.0;
        attribute cycle_salt_hot_C : Real default 0.0;
        attribute cycle_salt_return_C : Real default 0.0;
        attribute cycle_salt_cp_kJ_kgK : Real default 0.0;
        attribute p_feed_MPa : Real = matched_cycle.p_feed_MPa;
        attribute h_feed_kJ_kg : Real = matched_cycle.h_feed_kJ_kg;
        attribute mdot_feed_kg_s : Real = matched_cycle.mdot_feed_kg_s;
        attribute t_feed_C : Real = matched_cycle.t_feed_C;
        attribute s_feed_kJ_kgK : Real = matched_cycle.s_feed_kJ_kgK;
        attribute p_main_MPa : Real = matched_cycle.p_main_MPa;
        attribute h_main_kJ_kg : Real = matched_cycle.h_main_kJ_kg;
        attribute mdot_main_kg_s : Real = matched_cycle.mdot_main_kg_s;
        attribute t_main_C : Real = matched_cycle.t_main_C;
        attribute s_main_kJ_kgK : Real = matched_cycle.s_main_kJ_kgK;
        attribute p_hp_MPa : Real = matched_cycle.p_hp_MPa;
        attribute h_hp_kJ_kg : Real = matched_cycle.h_hp_kJ_kg;
        attribute mdot_hp_kg_s : Real = matched_cycle.mdot_hp_kg_s;
        attribute t_hp_C : Real = matched_cycle.t_hp_C;
        attribute s_hp_kJ_kgK : Real = matched_cycle.s_hp_kJ_kgK;
        attribute p_reheat_MPa : Real = matched_cycle.p_reheat_MPa;
        attribute h_reheat_kJ_kg : Real = matched_cycle.h_reheat_kJ_kg;
        attribute mdot_reheat_kg_s : Real = matched_cycle.mdot_reheat_kg_s;
        attribute t_reheat_C : Real = matched_cycle.t_reheat_C;
        attribute s_reheat_kJ_kgK : Real = matched_cycle.s_reheat_kJ_kgK;
        attribute p_lp_MPa : Real = matched_cycle.p_lp_MPa;
        attribute h_lp_kJ_kg : Real = matched_cycle.h_lp_kJ_kg;
        attribute mdot_lp_kg_s : Real = matched_cycle.mdot_lp_kg_s;
        attribute t_lp_C : Real = matched_cycle.t_lp_C;
        attribute s_lp_kJ_kgK : Real = matched_cycle.s_lp_kJ_kgK;
        attribute p_condensate_MPa : Real = matched_cycle.p_condensate_MPa;
        attribute h_condensate_kJ_kg : Real = matched_cycle.h_condensate_kJ_kg;
        attribute mdot_condensate_kg_s : Real = matched_cycle.mdot_condensate_kg_s;
        attribute t_condensate_C : Real = matched_cycle.t_condensate_C;
        attribute s_condensate_kJ_kgK : Real = matched_cycle.s_condensate_kJ_kgK;
        attribute p_condensate_pumped_MPa : Real = matched_cycle.p_condensate_pumped_MPa;
        attribute h_condensate_pumped_kJ_kg : Real = matched_cycle.h_condensate_pumped_kJ_kg;
        attribute mdot_condensate_pumped_kg_s : Real = matched_cycle.mdot_condensate_pumped_kg_s;
        attribute p_heater_MPa : Real = matched_cycle.p_heater_MPa;
        attribute h_heater_kJ_kg : Real = matched_cycle.h_heater_kJ_kg;
        attribute mdot_heater_kg_s : Real = matched_cycle.mdot_heater_kg_s;
        attribute t_heater_C : Real = matched_cycle.t_heater_C;
        attribute s_heater_kJ_kgK : Real = matched_cycle.s_heater_kJ_kgK;
        attribute bleed_fraction : Real = matched_cycle.bleed_fraction;
        attribute mdot_bleed_kg_s : Real = matched_cycle.mdot_bleed_kg_s;
        attribute salt_flow_total_kg_s : Real = matched_cycle.salt_flow_total_kg_s;
        attribute salt_main_flow_kg_s : Real = matched_cycle.salt_main_flow_kg_s;
        attribute salt_reheat_flow_kg_s : Real = matched_cycle.salt_reheat_flow_kg_s;
        attribute q_main_MW : Real = matched_cycle.q_main_MW;
        attribute q_reheat_MW : Real = matched_cycle.q_reheat_MW;
        attribute q_condenser_MW : Real = matched_cycle.q_condenser_MW;
        attribute p_hp_shaft_MW : Real = matched_cycle.p_hp_shaft_MW;
        attribute p_lp_shaft_MW : Real = matched_cycle.p_lp_shaft_MW;
        attribute p_condensate_shaft_MW : Real = matched_cycle.p_condensate_shaft_MW;
        attribute p_feedwater_shaft_MW : Real = matched_cycle.p_feedwater_shaft_MW;
        attribute p_condensate_electric_MW : Real = matched_cycle.p_condensate_electric_MW;
        attribute p_feedwater_electric_MW : Real = matched_cycle.p_feedwater_electric_MW;
        attribute p_cycle_pumps_MW : Real = matched_cycle.p_cycle_pumps_MW;
        attribute p_gross_MW : Real = matched_cycle.p_gross_MW;
        attribute eta_gross : Real = matched_cycle.eta_gross;
        attribute p_cycle_net_before_cooling_MW : Real = matched_cycle.p_cycle_net_before_cooling_MW;
        attribute q_mechanical_loss_MW : Real = matched_cycle.q_mechanical_loss_MW;
        attribute q_generator_loss_MW : Real = matched_cycle.q_generator_loss_MW;
        attribute q_pump_motor_loss_MW : Real = matched_cycle.q_pump_motor_loss_MW;
        attribute q_rejection_before_cooling_MW : Real = matched_cycle.q_rejection_before_cooling_MW;
        attribute lp_quality : Real = matched_cycle.lp_quality;
        attribute lp_moisture_fraction : Real = matched_cycle.lp_moisture_fraction;
        attribute main_min_gap_K : Real = matched_cycle.main_min_gap_K;
        attribute reheat_min_gap_K : Real = matched_cycle.reheat_min_gap_K;
        attribute main_UA_MW_K : Real = matched_cycle.main_UA_MW_K;
        attribute reheat_UA_MW_K : Real = matched_cycle.reheat_UA_MW_K;
        attribute salt_heat_residual_MW : Real = matched_cycle.salt_heat_residual_MW;
        attribute heater_mass_residual_kg_s : Real = matched_cycle.heater_mass_residual_kg_s;
        attribute heater_energy_residual_MW : Real = matched_cycle.heater_energy_residual_MW;
        attribute cycle_shaft_residual_MW : Real = matched_cycle.cycle_shaft_residual_MW;
        attribute cycle_electric_residual_MW : Real = matched_cycle.cycle_electric_residual_MW;
        attribute matched_active : Boolean = matched_cycle.active;
        attribute matched_main_UA_available : Boolean = matched_cycle.main_UA_available;
        attribute matched_reheat_UA_available : Boolean = matched_cycle.reheat_UA_available;
        attribute matched_main_admission_ok : Boolean = matched_cycle.main_admission_ok;
        attribute matched_reheat_admission_ok : Boolean = matched_cycle.reheat_admission_ok;
        attribute matched_turbine_equipment_qualified : Boolean = matched_cycle.turbine_equipment_qualified;
        attribute matched_installed_sg_capacity_qualified : Boolean = matched_cycle.installed_sg_capacity_qualified;
        part main_steam_generator : 'Steam Heat Exchanger' {
            attribute temperature_in_C : Real = 'Turbine Plant'::t_feed_C;
            attribute entropy_in_kJ_kgK : Real = 'Turbine Plant'::s_feed_kJ_kgK;
            attribute temperature_out_C : Real = 'Turbine Plant'::t_main_C;
            attribute entropy_out_kJ_kgK : Real = 'Turbine Plant'::s_main_kJ_kgK;
            :>> p_in_MPa = 'Turbine Plant'::p_feed_MPa;
            :>> h_in_kJ_kg = 'Turbine Plant'::h_feed_kJ_kg;
            :>> flow_in_kg_s = 'Turbine Plant'::mdot_feed_kg_s;
            :>> p_out_MPa = 'Turbine Plant'::p_main_MPa;
            :>> h_out_kJ_kg = 'Turbine Plant'::h_main_kJ_kg;
            :>> flow_out_kg_s = 'Turbine Plant'::mdot_main_kg_s;
            :>> heat_MW = 'Turbine Plant'::q_main_MW;
            :>> minimum_gap_K = 'Turbine Plant'::main_min_gap_K;
            :>> required_UA_MW_K = 'Turbine Plant'::main_UA_MW_K;
            :>> salt_flow_kg_s = 'Turbine Plant'::salt_main_flow_kg_s;
            :>> pressure_MPa default 0.0;
            :>> outlet_temperature_C default 0.0;
        }
        part hp_turbine : 'Steam Expansion' {
            attribute temperature_in_C : Real = 'Turbine Plant'::t_main_C;
            attribute entropy_in_kJ_kgK : Real = 'Turbine Plant'::s_main_kJ_kgK;
            attribute temperature_out_C : Real = 'Turbine Plant'::t_hp_C;
            attribute entropy_out_kJ_kgK : Real = 'Turbine Plant'::s_hp_kJ_kgK;
            :>> p_in_MPa = 'Turbine Plant'::p_main_MPa;
            :>> h_in_kJ_kg = 'Turbine Plant'::h_main_kJ_kg;
            :>> flow_in_kg_s = 'Turbine Plant'::mdot_main_kg_s;
            :>> p_out_MPa = 'Turbine Plant'::p_hp_MPa;
            :>> h_out_kJ_kg = 'Turbine Plant'::h_hp_kJ_kg;
            :>> flow_out_kg_s = 'Turbine Plant'::mdot_hp_kg_s;
            :>> shaft_MW = 'Turbine Plant'::p_hp_shaft_MW;
            :>> efficiency default 0.0;
        }
        part reheater : 'Steam Heat Exchanger' {
            attribute temperature_in_C : Real = 'Turbine Plant'::t_hp_C;
            attribute entropy_in_kJ_kgK : Real = 'Turbine Plant'::s_hp_kJ_kgK;
            attribute temperature_out_C : Real = 'Turbine Plant'::t_reheat_C;
            attribute entropy_out_kJ_kgK : Real = 'Turbine Plant'::s_reheat_kJ_kgK;
            :>> p_in_MPa = 'Turbine Plant'::p_hp_MPa;
            :>> h_in_kJ_kg = 'Turbine Plant'::h_hp_kJ_kg;
            :>> flow_in_kg_s = 'Turbine Plant'::mdot_reheat_kg_s;
            :>> p_out_MPa = 'Turbine Plant'::p_reheat_MPa;
            :>> h_out_kJ_kg = 'Turbine Plant'::h_reheat_kJ_kg;
            :>> flow_out_kg_s = 'Turbine Plant'::mdot_reheat_kg_s;
            :>> heat_MW = 'Turbine Plant'::q_reheat_MW;
            :>> minimum_gap_K = 'Turbine Plant'::reheat_min_gap_K;
            :>> required_UA_MW_K = 'Turbine Plant'::reheat_UA_MW_K;
            :>> salt_flow_kg_s = 'Turbine Plant'::salt_reheat_flow_kg_s;
            :>> pressure_MPa = 'Turbine Plant'::p_reheat_MPa;
            :>> outlet_temperature_C default 0.0;
        }
        part lp_turbine : 'Steam Expansion' {
            attribute temperature_in_C : Real = 'Turbine Plant'::t_reheat_C;
            attribute entropy_in_kJ_kgK : Real = 'Turbine Plant'::s_reheat_kJ_kgK;
            attribute temperature_out_C : Real = 'Turbine Plant'::t_lp_C;
            attribute entropy_out_kJ_kgK : Real = 'Turbine Plant'::s_lp_kJ_kgK;
            :>> p_in_MPa = 'Turbine Plant'::p_reheat_MPa;
            :>> h_in_kJ_kg = 'Turbine Plant'::h_reheat_kJ_kg;
            :>> flow_in_kg_s = 'Turbine Plant'::mdot_reheat_kg_s;
            :>> p_out_MPa = 'Turbine Plant'::p_lp_MPa;
            :>> h_out_kJ_kg = 'Turbine Plant'::h_lp_kJ_kg;
            :>> flow_out_kg_s = 'Turbine Plant'::mdot_lp_kg_s;
            :>> shaft_MW = 'Turbine Plant'::p_lp_shaft_MW;
            :>> efficiency default 0.0;
        }
        part open_feedwater_heater : 'Steam Feed Heater' {
            attribute temperature_out_C : Real = 'Turbine Plant'::t_heater_C;
            attribute entropy_out_kJ_kgK : Real = 'Turbine Plant'::s_heater_kJ_kgK;
            :>> p_in_MPa = 'Turbine Plant'::p_condensate_pumped_MPa;
            :>> h_in_kJ_kg = 'Turbine Plant'::h_condensate_pumped_kJ_kg;
            :>> flow_in_kg_s = 'Turbine Plant'::mdot_condensate_pumped_kg_s;
            :>> p_out_MPa = 'Turbine Plant'::p_heater_MPa;
            :>> h_out_kJ_kg = 'Turbine Plant'::h_heater_kJ_kg;
            :>> flow_out_kg_s = 'Turbine Plant'::mdot_heater_kg_s;
            :>> bleed_flow_kg_s = 'Turbine Plant'::mdot_bleed_kg_s;
            :>> bleed_h_kJ_kg = 'Turbine Plant'::h_hp_kJ_kg;
            :>> mass_residual_kg_s = 'Turbine Plant'::heater_mass_residual_kg_s;
            :>> energy_residual_MW = 'Turbine Plant'::heater_energy_residual_MW;
            :>> pressure_MPa default 0.0;
        }
        part condenser : 'Steam Condenser' {
            attribute temperature_in_C : Real = 'Turbine Plant'::t_lp_C;
            attribute entropy_in_kJ_kgK : Real = 'Turbine Plant'::s_lp_kJ_kgK;
            attribute temperature_out_C : Real = 'Turbine Plant'::t_condensate_C;
            attribute entropy_out_kJ_kgK : Real = 'Turbine Plant'::s_condensate_kJ_kgK;
            :>> p_in_MPa = 'Turbine Plant'::p_lp_MPa;
            :>> h_in_kJ_kg = 'Turbine Plant'::h_lp_kJ_kg;
            :>> flow_in_kg_s = 'Turbine Plant'::mdot_lp_kg_s;
            :>> p_out_MPa = 'Turbine Plant'::p_condensate_MPa;
            :>> h_out_kJ_kg = 'Turbine Plant'::h_condensate_kJ_kg;
            :>> flow_out_kg_s = 'Turbine Plant'::mdot_condensate_kg_s;
            :>> rejected_MW = 'Turbine Plant'::q_condenser_MW;
            :>> temperature_C default 0.0;
        }
        part condensate_pump : 'Steam Liquid Pump' {
            attribute temperature_in_C : Real = 'Turbine Plant'::t_condensate_C;
            attribute entropy_in_kJ_kgK : Real = 'Turbine Plant'::s_condensate_kJ_kgK;
            :>> p_in_MPa = 'Turbine Plant'::p_condensate_MPa;
            :>> h_in_kJ_kg = 'Turbine Plant'::h_condensate_kJ_kg;
            :>> flow_in_kg_s = 'Turbine Plant'::mdot_condensate_kg_s;
            :>> p_out_MPa = 'Turbine Plant'::p_condensate_pumped_MPa;
            :>> h_out_kJ_kg = 'Turbine Plant'::h_condensate_pumped_kJ_kg;
            :>> flow_out_kg_s = 'Turbine Plant'::mdot_condensate_pumped_kg_s;
            :>> shaft_MW = 'Turbine Plant'::p_condensate_shaft_MW;
            :>> electric_MW = 'Turbine Plant'::p_condensate_electric_MW;
            :>> efficiency default 0.0;
        }
        part feedwater_pump : 'Steam Liquid Pump' {
            attribute temperature_in_C : Real = 'Turbine Plant'::t_heater_C;
            attribute entropy_in_kJ_kgK : Real = 'Turbine Plant'::s_heater_kJ_kgK;
            attribute temperature_out_C : Real = 'Turbine Plant'::t_feed_C;
            attribute entropy_out_kJ_kgK : Real = 'Turbine Plant'::s_feed_kJ_kgK;
            :>> p_in_MPa = 'Turbine Plant'::p_heater_MPa;
            :>> h_in_kJ_kg = 'Turbine Plant'::h_heater_kJ_kg;
            :>> flow_in_kg_s = 'Turbine Plant'::mdot_heater_kg_s;
            :>> p_out_MPa = 'Turbine Plant'::p_feed_MPa;
            :>> h_out_kJ_kg = 'Turbine Plant'::h_feed_kJ_kg;
            :>> flow_out_kg_s = 'Turbine Plant'::mdot_feed_kg_s;
            :>> shaft_MW = 'Turbine Plant'::p_feedwater_shaft_MW;
            :>> electric_MW = 'Turbine Plant'::p_feedwater_electric_MW;
            :>> efficiency default 0.0;
        }
        part generator : 'Steam Generator Machine' {
            :>> hp_shaft_MW = 'Turbine Plant'::p_hp_shaft_MW;
            :>> lp_shaft_MW = 'Turbine Plant'::p_lp_shaft_MW;
            :>> gross_MW = 'Turbine Plant'::p_gross_MW;
            :>> mechanical_loss_MW = 'Turbine Plant'::q_mechanical_loss_MW;
            :>> generator_loss_MW = 'Turbine Plant'::q_generator_loss_MW;
            :>> mechanical_efficiency default 0.0;
            :>> generator_efficiency default 0.0;
        }
        part extraction_splitter : 'Steam Extraction Splitter' {
            :>> total_flow_kg_s = 'Turbine Plant'::mdot_hp_kg_s;
            :>> reheat_flow_kg_s = 'Turbine Plant'::mdot_reheat_kg_s;
            :>> bleed_flow_kg_s = 'Turbine Plant'::mdot_bleed_kg_s;
            :>> pressure_MPa = 'Turbine Plant'::p_hp_MPa;
            :>> enthalpy_kJ_kg = 'Turbine Plant'::h_hp_kJ_kg;
        }
        part salt_distributor : 'Salt Branch Distributor' {
            :>> total_flow_kg_s = 'Turbine Plant'::salt_flow_total_kg_s;
            :>> main_flow_kg_s = 'Turbine Plant'::salt_main_flow_kg_s;
            :>> reheat_flow_kg_s = 'Turbine Plant'::salt_reheat_flow_kg_s;
            :>> hot_C = 'Turbine Plant'::cycle_salt_hot_C;
            :>> return_C = 'Turbine Plant'::cycle_salt_return_C;
        }
        calc matched_cycle : 'Matched Steam Cycle' {
            in enabled_in = matched_cycle_enabled;
            in heat_available_MW_in = cycle_heat_available_MW;
            in source_heat_MW_in = cycle_source_heat_MW;
            in selected_recovered_MW_in = cycle_selected_recovered_MW;
            in salt_flow_per_circuit_in = cycle_salt_flow_per_circuit;
            in salt_circuit_count_in = cycle_salt_circuit_count;
            in salt_hot_C_in = cycle_salt_hot_C;
            in salt_return_C_in = cycle_salt_return_C;
            in salt_cp_kJ_kgK_in = cycle_salt_cp_kJ_kgK;
            in main_pressure_MPa_in = main_steam_generator.pressure_MPa;
            in extraction_pressure_MPa_in = open_feedwater_heater.pressure_MPa;
            in steam_temperature_C_in = main_steam_generator.outlet_temperature_C;
            in reheat_temperature_C_in = reheater.outlet_temperature_C;
            in condenser_temperature_C_in = condenser.temperature_C;
            in eta_hp_in = hp_turbine.efficiency;
            in eta_lp_in = lp_turbine.efficiency;
            in eta_condensate_pump_in = condensate_pump.efficiency;
            in eta_feedwater_pump_in = feedwater_pump.efficiency;
            in eta_pump_motor_in = pump_motor_efficiency;
            in eta_mechanical_in = generator.mechanical_efficiency;
            in eta_generator_in = generator.generator_efficiency;
        }
        calc cycle_selection : 'Cycle Mode Selection' {
            in matched_enabled_in = matched_cycle_enabled;
            in legacy_eta_in = cycle.eta_th;
            in matched_eta_in = matched_cycle.eta_gross;
            in legacy_domain_product_in = cycle.domain_product;
        }
        attribute legacy_domain_applicable : Boolean = cycle_selection.legacy_domain_applicable;
        attribute matched_domain_applicable : Boolean = cycle_selection.matched_domain_applicable;
        connect main_steam_generator.outlet to hp_turbine.inlet;
        connect hp_turbine.outlet to extraction_splitter.inlet;
        connect extraction_splitter.reheat_out to reheater.inlet;
        connect extraction_splitter.bleed_out to open_feedwater_heater.bleed_in;
        connect reheater.outlet to lp_turbine.inlet;
        connect lp_turbine.outlet to condenser.inlet;
        connect condenser.outlet to condensate_pump.inlet;
        connect condensate_pump.outlet to open_feedwater_heater.inlet;
        connect open_feedwater_heater.outlet to feedwater_pump.inlet;
        connect feedwater_pump.outlet to main_steam_generator.inlet;
        connect hp_turbine.shaft_out to generator.hp_shaft;
        connect lp_turbine.shaft_out to generator.lp_shaft;
        // Parallel salt branches share hot/return conditions; solver conserves their mass and heat.
        connect coolant to salt_distributor.supply_return;
        connect generator.electric_out to gross_electric;
        // Total boundary rejection includes condenser and conversion losses exactly once.
        connect condenser.rejection to cycle_rejection;
        connect conversion_losses to cycle_rejection;
        connect pump_electric_in to condensate_pump.electric_in;
        connect pump_electric_in to feedwater_pump.electric_in;
        connect salt_distributor.main_branch to main_steam_generator.salt;
        connect salt_distributor.reheat_branch to reheater.salt;
        calc turbine_cost : 'Linear Power Cost' {
            in power = p_the;
            in cost_per_mw = 'Turbine Plant'::cost_per_mw;
            in n_mod_in = n_mod;
        }
    }

    part def 'Electric Plant' :> 'CAS24 Electric Plant' {
        doc /*
        WI-078/MR-7 scope: capital_cost is a demand-matched electrical equipment proxy driven by computed gross electric output. The model has no independently supplied switchyard, transformer or cable capacity and no installed electrical-equipment adequacy check. Operating electric power is not an installed rating.

        CAS24 Electric plant equipment (switchyard, transformers, cabling).
        Linear in gross electric; feeds 'Linear Power Cost' with power = p_et.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
        **Ref**: costs.py:162 (cas24_electrical)
        **Basis**: Concept-agnostic electric plant, scales with gross electric
        */
        // ---- ports (WI-057): the exchanges this part takes part in; declarative, see mfe_interfaces ----
        port gross_in : ~'Electric Port';   // <- turbine.gross_electric
        port grid : 'Electric Port';   // the net electric output; unconnected -- the model has no grid part (design D7)
        port recirculating : 'Electric Port';   // -> heating, heat_transport, cryoplant, power_supplies, fuel_cycle (pb's recirculating terms)
        :>> scope = 'CAS Scope'::shared;

        attribute cost_per_mw : Real;
        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----
        attribute n_mod : Real;   // <- 'MFE Power Plant'::n_mod
        attribute p_et : Real;   // <- pb.p_et
        :>> capital_cost = electric_cost.cost;
        // ---- template calcs (WI-057): the analyses this part owns ----
        calc electric_cost : 'Linear Power Cost' {
            in power = p_et;
            in cost_per_mw = 'Electric Plant'::cost_per_mw;
            in n_mod_in = n_mod;
        }
    }

    part def 'Heat Rejection' :> 'CAS25 Heat Rejection' {
        doc /*
        WI-078/MR-7 scope: capital_cost is a demand-matched heat-rejection equipment proxy driven by total thermal power, not a price for a selected cooling-water pump or tower. Water flow and pump work solve the declared operating heat balance; they are not installed ratings. Installed heat-rejection capacity and site suitability are not evaluated.

        CAS25 Heat rejection (cooling towers, circulating water). Linear in
        total thermal power; feeds 'Linear Power Cost' with power = p_th.
        (1costingFE numbers this account CAS26 -- see file header note.)

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
        **Ref**: costs.py:179 (cas26_heat_rejection)
        **Basis**: Concept-agnostic heat rejection, scales with thermal power
        */
        :>> scope = 'CAS Scope'::shared;

        attribute cost_per_mw : Real;
        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----
        attribute n_mod : Real;   // <- 'MFE Power Plant'::n_mod
        attribute p_th : Real;   // <- pb.p_th
        :>> capital_cost = heat_rejection_cost.cost;
        // ---- template calcs (WI-057): the analyses this part owns ----
        attribute cooling_water_enabled : Real default 0.0;
        attribute matched_cycle_mode : Real default 0.0;
        attribute cycle_rejection_MW : Real default 0.0;
        attribute cycle_condenser_C : Real default 0.0;
        attribute water_inlet_C : Real default 0.0;
        attribute water_outlet_C : Real default 0.0;
        attribute water_flow_kg_s : Real = cooling_water.water_flow_kg_s;
        attribute p_cooling_pump_shaft_MW : Real = cooling_water.p_cooling_pump_shaft_MW;
        attribute p_cooling_pump_electric_MW : Real = cooling_water.p_cooling_pump_electric_MW;
        attribute q_cooling_motor_loss_MW : Real = cooling_water.q_cooling_motor_loss_MW;
        attribute q_total_rejection_MW : Real = cooling_water.q_total_rejection_MW;
        attribute water_pump_rise_K : Real = cooling_water.water_pump_rise_K;
        attribute condenser_water_gap_K : Real = cooling_water.condenser_water_gap_K;
        attribute water_energy_residual_MW : Real = cooling_water.water_energy_residual_MW;
        attribute denominator_kJ_kg : Real = cooling_water.denominator_kJ_kg;
        attribute cooling_active : Boolean = cooling_water.active;
        attribute cooling_reference_scenario : Boolean = cooling_water.reference_scenario;
        attribute cooling_site_qualified : Boolean = cooling_water.site_qualified;
        attribute cooling_cooling_approach_ok : Boolean = cooling_water.cooling_approach_ok;
        port cycle_heat_in : ~'Heat Duty Port';
        port environmental_heat : 'Heat Duty Port';
        port electric_in : ~'Electric Port';
        part circulating_water_pump : 'Circulating Water Pump' {
            :>> head_m default 0.0;
            :>> efficiency default 0.0;
            :>> motor_efficiency default 0.0;
            :>> flow_kg_s = 'Heat Rejection'::water_flow_kg_s;
            :>> shaft_MW = 'Heat Rejection'::p_cooling_pump_shaft_MW;
            :>> electric_MW = 'Heat Rejection'::p_cooling_pump_electric_MW;
        }
        connect electric_in to circulating_water_pump.electric_in;
        calc cooling_water : 'Cooling Water Rejection' {
            in enabled_in = cooling_water_enabled;
            in cycle_active_in = matched_cycle_mode;
            in q_rejection_before_cooling_MW_in = cycle_rejection_MW;
            in condenser_temperature_C_in = cycle_condenser_C;
            in water_inlet_C_in = water_inlet_C;
            in water_outlet_C_in = water_outlet_C;
            in head_m_in = circulating_water_pump.head_m;
            in eta_pump_in = circulating_water_pump.efficiency;
            in eta_motor_in = circulating_water_pump.motor_efficiency;
        }
        calc heat_rejection_cost : 'Linear Power Cost' {
            in power = p_th;
            in cost_per_mw = 'Heat Rejection'::cost_per_mw;
            in n_mod_in = n_mod;
        }
    }

    part def 'Miscellaneous Plant' :> 'CAS26 Miscellaneous' {
        doc /*
        CAS26 Miscellaneous plant equipment (fire protection, compressed air,
        HVAC). Linear in gross electric; feeds 'Linear Power Cost' with
        power = p_et. (1costingFE numbers this account CAS25 -- see header note.) This demand-matched aggregate price proxy does not select or evaluate independently supplied fire-protection, compressed-air or HVAC equipment capacities.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
        **Ref**: costs.py:170 (cas25_misc)
        **Basis**: Concept-agnostic miscellaneous plant, scales with gross electric
        */
        :>> scope = 'CAS Scope'::shared;

        attribute cost_per_mw : Real;
        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----
        attribute n_mod : Real;   // <- 'MFE Power Plant'::n_mod
        attribute p_et : Real;   // <- pb.p_et
        :>> capital_cost = misc_cost.cost;
        // ---- template calcs (WI-057): the analyses this part owns ----
        calc misc_cost : 'Linear Power Cost' {
            in power = p_et;
            in cost_per_mw = 'Miscellaneous Plant'::cost_per_mw;
            in n_mod_in = n_mod;
        }
    }

    // --- Buildings (CAS21, physical facilities with a preserved legacy selector) ---

    part def 'Buildings' :> 'CAS21 Structures' {
        // WI-068: Source: work/active/WI-068_layout-based-facilities/design.md; layout-capacity-design.md; evidence/facility-contract.md. Ref: released geometry, capacity, exact civil takeoff and account boundary. Basis: conditional conceptual scenario; unqualified shielding/loading/transport and explicit provisional equipment envelopes.
        attribute facilities_enabled : Boolean default false;
        // WI-076 supplied design interface: m, except selected package count.
        attribute selected_reactor_hall_length : Real default 0.0;
        attribute selected_reactor_hall_width : Real default 0.0;
        attribute selected_reactor_hall_height : Real default 0.0;
        attribute selected_sector_wing_east_length : Real default 0.0;
        attribute selected_sector_wing_east_width : Real default 0.0;
        attribute selected_sector_wing_east_height : Real default 0.0;
        attribute selected_sector_wing_north_length : Real default 0.0;
        attribute selected_sector_wing_north_width : Real default 0.0;
        attribute selected_sector_wing_north_height : Real default 0.0;
        attribute selected_sector_wing_west_length : Real default 0.0;
        attribute selected_sector_wing_west_width : Real default 0.0;
        attribute selected_sector_wing_west_height : Real default 0.0;
        attribute selected_sector_wing_south_length : Real default 0.0;
        attribute selected_sector_wing_south_width : Real default 0.0;
        attribute selected_sector_wing_south_height : Real default 0.0;
        attribute selected_sector_link_east_length : Real default 0.0;
        attribute selected_sector_link_east_width : Real default 0.0;
        attribute selected_sector_link_east_height : Real default 0.0;
        attribute selected_sector_link_north_length : Real default 0.0;
        attribute selected_sector_link_north_width : Real default 0.0;
        attribute selected_sector_link_north_height : Real default 0.0;
        attribute selected_sector_link_west_length : Real default 0.0;
        attribute selected_sector_link_west_width : Real default 0.0;
        attribute selected_sector_link_west_height : Real default 0.0;
        attribute selected_sector_link_south_length : Real default 0.0;
        attribute selected_sector_link_south_width : Real default 0.0;
        attribute selected_sector_link_south_height : Real default 0.0;
        attribute selected_cooling_hall_length : Real default 0.0;
        attribute selected_cooling_hall_width : Real default 0.0;
        attribute selected_cooling_hall_height : Real default 0.0;
        attribute selected_cooling_annex_length : Real default 0.0;
        attribute selected_cooling_annex_width : Real default 0.0;
        attribute selected_cooling_annex_height : Real default 0.0;
        attribute selected_cooling_link_length : Real default 0.0;
        attribute selected_cooling_link_width : Real default 0.0;
        attribute selected_cooling_link_height : Real default 0.0;
        attribute selected_turbine_hall_length : Real default 0.0;
        attribute selected_turbine_hall_width : Real default 0.0;
        attribute selected_turbine_hall_height : Real default 0.0;
        attribute selected_cryo_coldbox_length : Real default 0.0;
        attribute selected_cryo_coldbox_width : Real default 0.0;
        attribute selected_cryo_coldbox_height : Real default 0.0;
        attribute selected_cryo_compressors_length : Real default 0.0;
        attribute selected_cryo_compressors_width : Real default 0.0;
        attribute selected_cryo_compressors_height : Real default 0.0;
        attribute selected_fuel_building_length : Real default 0.0;
        attribute selected_fuel_building_width : Real default 0.0;
        attribute selected_fuel_building_height : Real default 0.0;
        attribute selected_reactor_auxiliaries_length : Real default 0.0;
        attribute selected_reactor_auxiliaries_width : Real default 0.0;
        attribute selected_reactor_auxiliaries_height : Real default 0.0;
        attribute selected_power_supply_building_length : Real default 0.0;
        attribute selected_power_supply_building_width : Real default 0.0;
        attribute selected_power_supply_building_height : Real default 0.0;
        attribute selected_electrical_building_length : Real default 0.0;
        attribute selected_electrical_building_width : Real default 0.0;
        attribute selected_electrical_building_height : Real default 0.0;
        attribute selected_service_water_building_length : Real default 0.0;
        attribute selected_service_water_building_width : Real default 0.0;
        attribute selected_service_water_building_height : Real default 0.0;
        attribute selected_maintenance_shop_length : Real default 0.0;
        attribute selected_maintenance_shop_width : Real default 0.0;
        attribute selected_maintenance_shop_height : Real default 0.0;
        attribute selected_site_services_building_length : Real default 0.0;
        attribute selected_site_services_building_width : Real default 0.0;
        attribute selected_site_services_building_height : Real default 0.0;
        attribute selected_administration_length : Real default 0.0;
        attribute selected_administration_width : Real default 0.0;
        attribute selected_administration_height : Real default 0.0;
        attribute selected_control_length : Real default 0.0;
        attribute selected_control_width : Real default 0.0;
        attribute selected_control_height : Real default 0.0;
        attribute selected_security_length : Real default 0.0;
        attribute selected_security_width : Real default 0.0;
        attribute selected_security_height : Real default 0.0;
        attribute selected_cooling_helium_store_width : Real default 0.0;
        attribute selected_cooling_salt_store_width : Real default 0.0;
        attribute selected_cooling_bundle_store_width : Real default 0.0;
        attribute selected_cooling_annex_north_depth : Real default 0.0;
        attribute selected_blanket_packages_per_sector : Real default 0.0;
        // WI-076 signed translation from the documented entering coordinate datum [m].
        attribute parcel_origin_x_offset : Real default 0.0;
        attribute parcel_origin_y_offset : Real default 0.0;
        attribute selected_parcel_x_min : Real default 0.0;
        attribute selected_parcel_y_min : Real default 0.0;
        attribute selected_parcel_length : Real default 0.0;
        attribute selected_parcel_width : Real default 0.0;

        attribute facilities_cost_mode : Real default 0.0;
        attribute sector_count : Real default 4.0;
        attribute sector_bays : Real default 4.0;
        attribute sector_service_teams : Real default 2.0;
        attribute exterior_allowance : Real default 2.0;
        attribute sector_route_clearance : Real default 6.0;
        attribute sector_headroom : Real default 3.0;
        attribute component_width : Real default 4.0;
        attribute component_height : Real default 2.0;
        attribute component_length : Real default 2.0;
        attribute component_handling_margin : Real default 0.5;
        attribute component_material_fraction : Real default 0.5;
        attribute divertor_packages_per_sector : Real default 4.0;
        attribute waste_package_yield : Real default 1.0;
        attribute component_remove_days : Real default 0.5;
        attribute component_install_days : Real default 0.5;
        attribute sector_clean_days : Real default 7.0;
        attribute sector_test_days : Real default 7.0;
        attribute sector_split_days : Real default 7.0;
        attribute sector_join_days : Real default 7.0;
        attribute sector_transport_days : Real default 2.0;
        attribute cooldown_days : Real default 30.0;
        attribute recommission_days : Real default 30.0;
        attribute initial_receipt_lead_days : Real default 180.0;
        attribute initial_sector_start_days : Real default -120.0;
        attribute component_receipt_lead_days : Real default 90.0;
        attribute component_prepare_days : Real default 1.0;
        attribute component_process_days : Real default 1.0;
        attribute component_hold_days : Real default 365.25;
        attribute clean_positions : Real default 36.0;
        attribute dirty_buffer_positions : Real default 18.0;
        attribute dirty_store_positions : Real default 36.0;
        attribute cooling_initial_receipt_lead_days : Real default 180.0;
        attribute cooling_initial_handoff_days : Real default -30.0;
        attribute cooling_receipt_lead_days : Real default 90.0;
        attribute cooling_hold_days : Real default 365.25;
        attribute cooling_prepare_stations : Real default 2.0;
        attribute cooling_machine_stations : Real default 2.0;
        attribute cooling_bundle_stations : Real default 2.0;
        attribute cooling_prepare_machine_days : Real default 0.5;
        attribute cooling_prepare_bundle_days : Real default 1.0;
        attribute cooling_machine_process_days : Real default 2.0;
        attribute cooling_bundle_process_days : Real default 5.0;
        attribute cooling_field_cycle_days : Real default 0.2;
        attribute cooling_internal_move_days : Real default 0.1;
        attribute cooling_clean_helium_positions : Real default 29.0;
        attribute cooling_clean_salt_positions : Real default 29.0;
        attribute cooling_clean_bundle_positions : Real default 14.0;
        attribute cooling_dirty_helium_positions : Real default 28.0;
        attribute cooling_dirty_salt_positions : Real default 28.0;
        attribute cooling_dirty_bundle_positions : Real default 14.0;
        attribute helium_package_length : Real default 6.0;
        attribute helium_package_width : Real default 3.0;
        attribute helium_package_height : Real default 4.0;
        attribute salt_package_length : Real default 3.0;
        attribute salt_package_width : Real default 2.0;
        attribute salt_package_height : Real default 3.0;
        attribute hx_end_allowance : Real default 2.0;
        attribute cooling_package_margin : Real default 1.0;
        attribute cooling_aisle_width : Real default 6.0;
        attribute cooling_cross_width : Real default 17.0;
        attribute cooling_headroom : Real default 9.0;
        attribute cooling_airlock_length : Real default 17.0;
        attribute nuclear_wall : Real default 2.0;
        attribute nuclear_floor : Real default 1.0;
        attribute nuclear_roof : Real default 1.0;
        attribute nuclear_rebar_density : Real default 150.0;
        attribute conventional_wall : Real default 0.3;
        attribute conventional_floor : Real default 0.3;
        attribute conventional_roof : Real default 0.2;
        attribute conventional_rebar_density : Real default 100.0;
        attribute building_separation : Real default 10.0;
        attribute external_access_width : Real default 12.0;
        attribute provisional_envelope_scale : Real default 1.0;
        attribute administration_occupants : Real default 200.0;
        attribute control_occupants : Real default 30.0;
        attribute security_occupants : Real default 10.0;
        attribute administration_area_per_person : Real default 12.0;
        attribute control_area_per_person : Real default 15.0;
        attribute security_area_per_person : Real default 12.0;
        attribute occupancy_circulation_factor : Real default 1.3;
        attribute occupancy_height : Real default 4.0;
        attribute heat_rejection_length : Real default 100.0;
        attribute heat_rejection_width : Real default 60.0;
        attribute turbine_length : Real default 60.0;
        attribute turbine_width : Real default 20.0;
        attribute turbine_height : Real default 15.0;
        attribute cryo_coldbox_length : Real default 20.0;
        attribute cryo_coldbox_width : Real default 12.0;
        attribute cryo_coldbox_height : Real default 10.0;
        attribute cryo_compressors_length : Real default 30.0;
        attribute cryo_compressors_width : Real default 12.0;
        attribute cryo_compressors_height : Real default 8.0;
        attribute fuel_length : Real default 30.0;
        attribute fuel_width : Real default 20.0;
        attribute fuel_height : Real default 8.0;
        attribute reactor_aux_length : Real default 30.0;
        attribute reactor_aux_width : Real default 20.0;
        attribute reactor_aux_height : Real default 10.0;
        attribute power_supply_length : Real default 20.0;
        attribute power_supply_width : Real default 10.0;
        attribute power_supply_height : Real default 8.0;
        attribute onsite_ac_length : Real default 16.0;
        attribute onsite_ac_width : Real default 8.0;
        attribute onsite_ac_height : Real default 6.0;
        attribute service_water_length : Real default 20.0;
        attribute service_water_width : Real default 15.0;
        attribute service_water_height : Real default 8.0;
        attribute conventional_shop_length : Real default 20.0;
        attribute conventional_shop_width : Real default 15.0;
        attribute conventional_shop_height : Real default 8.0;
        attribute site_services_length : Real default 20.0;
        attribute site_services_width : Real default 10.0;
        attribute site_services_height : Real default 6.0;
        attribute sub_concrete_rate : Real default 444.0233350945057;
        attribute sub_formwork_rate : Real default 700.0942889733001;
        attribute sub_rebar_rate : Real default 4.726624780628814;
        attribute super_concrete_rate : Real default 611.6152342453729;
        attribute super_formwork_rate : Real default 716.6635281988968;
        attribute super_rebar_rate : Real default 5.4683224473628815;
        attribute civil_cpi_ratio : Real default 1.2819593787335721;
        attribute civil_rate_multiplier : Real default 1.0;
        attribute tonne_interpretation_kg : Real default 907.18474;
        attribute ventilation_coefficient : Real default 1000.0;
        attribute ventilation_exponent : Real default 0.8;
        attribute ventilation_cpi_ratio : Real default 2.462892119357307;
        attribute land_rate_per_acre : Real default 10000.0;
        attribute retained_site_improvements : Real default 85000000.0;
        attribute n_mod : Real default 0.0;
        attribute major_radius : Real default 0.0;
        attribute minor_outer_radius : Real default 0.0;
        attribute blanket_volume : Real default 0.0;
        attribute calendar_q : Real default 0.0;
        attribute calendar_fluence : Real default 0.0;
        attribute calendar_years : Real default 0.0;
        attribute calendar_outage : Real default 0.0;
        attribute calendar_unplanned : Real default 0.0;
        attribute calendar_mode : Real default 0.0;
        attribute calendar_life : Real default 0.0;
        attribute calendar_count : Real default 0.0;
        attribute calendar_availability : Real default 0.0;
        attribute cooling_circuits : Real default 0.0;
        attribute cooling_helium_count : Real default 0.0;
        attribute cooling_salt_count : Real default 0.0;
        attribute cooling_bundle_count : Real default 0.0;
        attribute cooling_machine_life : Real default 0.0;
        attribute cooling_bundle_life : Real default 0.0;
        attribute hx_shell_bore : Real default 0.0;
        attribute hx_shell_wall : Real default 0.0;
        attribute hx_shell_length : Real default 0.0;
        attribute hx_tube_length : Real default 0.0;
        calc layout : 'Facility Layout' {

            in facilities_enabled_in = facilities_enabled;
            in facilities_cost_mode_in = facilities_cost_mode;
            in sector_count_in = sector_count;
            in sector_bays_in = sector_bays;
            in sector_service_teams_in = sector_service_teams;
            in exterior_allowance_in = exterior_allowance;
            in sector_route_clearance_in = sector_route_clearance;
            in sector_headroom_in = sector_headroom;
            in component_width_in = component_width;
            in component_height_in = component_height;
            in component_length_in = component_length;
            in component_handling_margin_in = component_handling_margin;
            in component_material_fraction_in = component_material_fraction;
            in divertor_packages_per_sector_in = divertor_packages_per_sector;
            in waste_package_yield_in = waste_package_yield;
            in component_remove_days_in = component_remove_days;
            in component_install_days_in = component_install_days;
            in sector_clean_days_in = sector_clean_days;
            in sector_test_days_in = sector_test_days;
            in sector_split_days_in = sector_split_days;
            in sector_join_days_in = sector_join_days;
            in sector_transport_days_in = sector_transport_days;
            in cooldown_days_in = cooldown_days;
            in recommission_days_in = recommission_days;
            in initial_receipt_lead_days_in = initial_receipt_lead_days;
            in initial_sector_start_days_in = initial_sector_start_days;
            in component_receipt_lead_days_in = component_receipt_lead_days;
            in component_prepare_days_in = component_prepare_days;
            in component_process_days_in = component_process_days;
            in component_hold_days_in = component_hold_days;
            in clean_positions_in = clean_positions;
            in dirty_buffer_positions_in = dirty_buffer_positions;
            in dirty_store_positions_in = dirty_store_positions;
            in cooling_initial_receipt_lead_days_in = cooling_initial_receipt_lead_days;
            in cooling_initial_handoff_days_in = cooling_initial_handoff_days;
            in cooling_receipt_lead_days_in = cooling_receipt_lead_days;
            in cooling_hold_days_in = cooling_hold_days;
            in cooling_prepare_stations_in = cooling_prepare_stations;
            in cooling_machine_stations_in = cooling_machine_stations;
            in cooling_bundle_stations_in = cooling_bundle_stations;
            in cooling_prepare_machine_days_in = cooling_prepare_machine_days;
            in cooling_prepare_bundle_days_in = cooling_prepare_bundle_days;
            in cooling_machine_process_days_in = cooling_machine_process_days;
            in cooling_bundle_process_days_in = cooling_bundle_process_days;
            in cooling_field_cycle_days_in = cooling_field_cycle_days;
            in cooling_internal_move_days_in = cooling_internal_move_days;
            in cooling_clean_helium_positions_in = cooling_clean_helium_positions;
            in cooling_clean_salt_positions_in = cooling_clean_salt_positions;
            in cooling_clean_bundle_positions_in = cooling_clean_bundle_positions;
            in cooling_dirty_helium_positions_in = cooling_dirty_helium_positions;
            in cooling_dirty_salt_positions_in = cooling_dirty_salt_positions;
            in cooling_dirty_bundle_positions_in = cooling_dirty_bundle_positions;
            in helium_package_length_in = helium_package_length;
            in helium_package_width_in = helium_package_width;
            in helium_package_height_in = helium_package_height;
            in salt_package_length_in = salt_package_length;
            in salt_package_width_in = salt_package_width;
            in salt_package_height_in = salt_package_height;
            in hx_end_allowance_in = hx_end_allowance;
            in cooling_package_margin_in = cooling_package_margin;
            in cooling_aisle_width_in = cooling_aisle_width;
            in cooling_cross_width_in = cooling_cross_width;
            in cooling_headroom_in = cooling_headroom;
            in cooling_airlock_length_in = cooling_airlock_length;
            in nuclear_wall_in = nuclear_wall;
            in nuclear_floor_in = nuclear_floor;
            in nuclear_roof_in = nuclear_roof;
            in nuclear_rebar_density_in = nuclear_rebar_density;
            in conventional_wall_in = conventional_wall;
            in conventional_floor_in = conventional_floor;
            in conventional_roof_in = conventional_roof;
            in conventional_rebar_density_in = conventional_rebar_density;
            in building_separation_in = building_separation;
            in external_access_width_in = external_access_width;
            in provisional_envelope_scale_in = provisional_envelope_scale;
            in administration_occupants_in = administration_occupants;
            in control_occupants_in = control_occupants;
            in security_occupants_in = security_occupants;
            in administration_area_per_person_in = administration_area_per_person;
            in control_area_per_person_in = control_area_per_person;
            in security_area_per_person_in = security_area_per_person;
            in occupancy_circulation_factor_in = occupancy_circulation_factor;
            in occupancy_height_in = occupancy_height;
            in heat_rejection_length_in = heat_rejection_length;
            in heat_rejection_width_in = heat_rejection_width;
            in turbine_length_in = turbine_length;
            in turbine_width_in = turbine_width;
            in turbine_height_in = turbine_height;
            in cryo_coldbox_length_in = cryo_coldbox_length;
            in cryo_coldbox_width_in = cryo_coldbox_width;
            in cryo_coldbox_height_in = cryo_coldbox_height;
            in cryo_compressors_length_in = cryo_compressors_length;
            in cryo_compressors_width_in = cryo_compressors_width;
            in cryo_compressors_height_in = cryo_compressors_height;
            in fuel_length_in = fuel_length;
            in fuel_width_in = fuel_width;
            in fuel_height_in = fuel_height;
            in reactor_aux_length_in = reactor_aux_length;
            in reactor_aux_width_in = reactor_aux_width;
            in reactor_aux_height_in = reactor_aux_height;
            in power_supply_length_in = power_supply_length;
            in power_supply_width_in = power_supply_width;
            in power_supply_height_in = power_supply_height;
            in onsite_ac_length_in = onsite_ac_length;
            in onsite_ac_width_in = onsite_ac_width;
            in onsite_ac_height_in = onsite_ac_height;
            in service_water_length_in = service_water_length;
            in service_water_width_in = service_water_width;
            in service_water_height_in = service_water_height;
            in conventional_shop_length_in = conventional_shop_length;
            in conventional_shop_width_in = conventional_shop_width;
            in conventional_shop_height_in = conventional_shop_height;
            in site_services_length_in = site_services_length;
            in site_services_width_in = site_services_width;
            in site_services_height_in = site_services_height;
            in n_mod_in = n_mod;
            in major_radius_in = major_radius;
            in minor_outer_radius_in = minor_outer_radius;
            in blanket_volume_in = blanket_volume;
            in calendar_q_in = calendar_q;
            in calendar_fluence_in = calendar_fluence;
            in calendar_years_in = calendar_years;
            in calendar_outage_in = calendar_outage;
            in calendar_unplanned_in = calendar_unplanned;
            in calendar_mode_in = calendar_mode;
            in calendar_life_in = calendar_life;
            in calendar_count_in = calendar_count;
            in calendar_availability_in = calendar_availability;
            in cooling_circuits_in = cooling_circuits;
            in cooling_helium_count_in = cooling_helium_count;
            in cooling_salt_count_in = cooling_salt_count;
            in cooling_bundle_count_in = cooling_bundle_count;
            in cooling_machine_life_in = cooling_machine_life;
            in cooling_bundle_life_in = cooling_bundle_life;
            in hx_shell_bore_in = hx_shell_bore;
            in hx_shell_wall_in = hx_shell_wall;
            in hx_shell_length_in = hx_shell_length;
            in hx_tube_length_in = hx_tube_length;
            in selected_reactor_hall_length_in = selected_reactor_hall_length;
            in selected_reactor_hall_width_in = selected_reactor_hall_width;
            in selected_reactor_hall_height_in = selected_reactor_hall_height;
            in selected_sector_wing_east_length_in = selected_sector_wing_east_length;
            in selected_sector_wing_east_width_in = selected_sector_wing_east_width;
            in selected_sector_wing_east_height_in = selected_sector_wing_east_height;
            in selected_sector_wing_north_length_in = selected_sector_wing_north_length;
            in selected_sector_wing_north_width_in = selected_sector_wing_north_width;
            in selected_sector_wing_north_height_in = selected_sector_wing_north_height;
            in selected_sector_wing_west_length_in = selected_sector_wing_west_length;
            in selected_sector_wing_west_width_in = selected_sector_wing_west_width;
            in selected_sector_wing_west_height_in = selected_sector_wing_west_height;
            in selected_sector_wing_south_length_in = selected_sector_wing_south_length;
            in selected_sector_wing_south_width_in = selected_sector_wing_south_width;
            in selected_sector_wing_south_height_in = selected_sector_wing_south_height;
            in selected_sector_link_east_length_in = selected_sector_link_east_length;
            in selected_sector_link_east_width_in = selected_sector_link_east_width;
            in selected_sector_link_east_height_in = selected_sector_link_east_height;
            in selected_sector_link_north_length_in = selected_sector_link_north_length;
            in selected_sector_link_north_width_in = selected_sector_link_north_width;
            in selected_sector_link_north_height_in = selected_sector_link_north_height;
            in selected_sector_link_west_length_in = selected_sector_link_west_length;
            in selected_sector_link_west_width_in = selected_sector_link_west_width;
            in selected_sector_link_west_height_in = selected_sector_link_west_height;
            in selected_sector_link_south_length_in = selected_sector_link_south_length;
            in selected_sector_link_south_width_in = selected_sector_link_south_width;
            in selected_sector_link_south_height_in = selected_sector_link_south_height;
            in selected_cooling_hall_length_in = selected_cooling_hall_length;
            in selected_cooling_hall_width_in = selected_cooling_hall_width;
            in selected_cooling_hall_height_in = selected_cooling_hall_height;
            in selected_cooling_annex_length_in = selected_cooling_annex_length;
            in selected_cooling_annex_width_in = selected_cooling_annex_width;
            in selected_cooling_annex_height_in = selected_cooling_annex_height;
            in selected_cooling_link_length_in = selected_cooling_link_length;
            in selected_cooling_link_width_in = selected_cooling_link_width;
            in selected_cooling_link_height_in = selected_cooling_link_height;
            in selected_turbine_hall_length_in = selected_turbine_hall_length;
            in selected_turbine_hall_width_in = selected_turbine_hall_width;
            in selected_turbine_hall_height_in = selected_turbine_hall_height;
            in selected_cryo_coldbox_length_in = selected_cryo_coldbox_length;
            in selected_cryo_coldbox_width_in = selected_cryo_coldbox_width;
            in selected_cryo_coldbox_height_in = selected_cryo_coldbox_height;
            in selected_cryo_compressors_length_in = selected_cryo_compressors_length;
            in selected_cryo_compressors_width_in = selected_cryo_compressors_width;
            in selected_cryo_compressors_height_in = selected_cryo_compressors_height;
            in selected_fuel_building_length_in = selected_fuel_building_length;
            in selected_fuel_building_width_in = selected_fuel_building_width;
            in selected_fuel_building_height_in = selected_fuel_building_height;
            in selected_reactor_auxiliaries_length_in = selected_reactor_auxiliaries_length;
            in selected_reactor_auxiliaries_width_in = selected_reactor_auxiliaries_width;
            in selected_reactor_auxiliaries_height_in = selected_reactor_auxiliaries_height;
            in selected_power_supply_building_length_in = selected_power_supply_building_length;
            in selected_power_supply_building_width_in = selected_power_supply_building_width;
            in selected_power_supply_building_height_in = selected_power_supply_building_height;
            in selected_electrical_building_length_in = selected_electrical_building_length;
            in selected_electrical_building_width_in = selected_electrical_building_width;
            in selected_electrical_building_height_in = selected_electrical_building_height;
            in selected_service_water_building_length_in = selected_service_water_building_length;
            in selected_service_water_building_width_in = selected_service_water_building_width;
            in selected_service_water_building_height_in = selected_service_water_building_height;
            in selected_maintenance_shop_length_in = selected_maintenance_shop_length;
            in selected_maintenance_shop_width_in = selected_maintenance_shop_width;
            in selected_maintenance_shop_height_in = selected_maintenance_shop_height;
            in selected_site_services_building_length_in = selected_site_services_building_length;
            in selected_site_services_building_width_in = selected_site_services_building_width;
            in selected_site_services_building_height_in = selected_site_services_building_height;
            in selected_administration_length_in = selected_administration_length;
            in selected_administration_width_in = selected_administration_width;
            in selected_administration_height_in = selected_administration_height;
            in selected_control_length_in = selected_control_length;
            in selected_control_width_in = selected_control_width;
            in selected_control_height_in = selected_control_height;
            in selected_security_length_in = selected_security_length;
            in selected_security_width_in = selected_security_width;
            in selected_security_height_in = selected_security_height;
            in selected_cooling_helium_store_width_in = selected_cooling_helium_store_width;
            in selected_cooling_salt_store_width_in = selected_cooling_salt_store_width;
            in selected_cooling_bundle_store_width_in = selected_cooling_bundle_store_width;
            in selected_cooling_annex_north_depth_in = selected_cooling_annex_north_depth;
            in selected_blanket_packages_per_sector_in = selected_blanket_packages_per_sector;
            in selected_parcel_x_min_in = selected_parcel_x_min;
            in selected_parcel_y_min_in = selected_parcel_y_min;
            in selected_parcel_length_in = selected_parcel_length;
            in selected_parcel_width_in = selected_parcel_width;
        }
        attribute active : Real = layout.active;
        attribute geometry_fit_margin_m : Real = layout.geometry_fit_margin_m;
        attribute occupancy_area_margin_m2 : Real = layout.occupancy_area_margin_m2;
        attribute parcel_fit_margin_m : Real = layout.parcel_fit_margin_m;
        attribute blanket_packages_required_per_sector : Real = layout.blanket_packages_required_per_sector;
        attribute required_parcel_x_min : Real = layout.required_parcel_x_min;
        attribute required_parcel_y_min : Real = layout.required_parcel_y_min;
        attribute required_parcel_x_max : Real = layout.required_parcel_x_max;
        attribute required_parcel_y_max : Real = layout.required_parcel_y_max;
        attribute reactor_hall_required_length : Real = layout.reactor_hall_required_length;
        attribute reactor_hall_required_width : Real = layout.reactor_hall_required_width;
        attribute reactor_hall_required_height : Real = layout.reactor_hall_required_height;
        attribute sector_wing_east_required_length : Real = layout.sector_wing_east_required_length;
        attribute sector_wing_east_required_width : Real = layout.sector_wing_east_required_width;
        attribute sector_wing_east_required_height : Real = layout.sector_wing_east_required_height;
        attribute sector_wing_north_required_length : Real = layout.sector_wing_north_required_length;
        attribute sector_wing_north_required_width : Real = layout.sector_wing_north_required_width;
        attribute sector_wing_north_required_height : Real = layout.sector_wing_north_required_height;
        attribute sector_wing_west_required_length : Real = layout.sector_wing_west_required_length;
        attribute sector_wing_west_required_width : Real = layout.sector_wing_west_required_width;
        attribute sector_wing_west_required_height : Real = layout.sector_wing_west_required_height;
        attribute sector_wing_south_required_length : Real = layout.sector_wing_south_required_length;
        attribute sector_wing_south_required_width : Real = layout.sector_wing_south_required_width;
        attribute sector_wing_south_required_height : Real = layout.sector_wing_south_required_height;
        attribute sector_link_east_required_length : Real = layout.sector_link_east_required_length;
        attribute sector_link_east_required_width : Real = layout.sector_link_east_required_width;
        attribute sector_link_east_required_height : Real = layout.sector_link_east_required_height;
        attribute sector_link_north_required_length : Real = layout.sector_link_north_required_length;
        attribute sector_link_north_required_width : Real = layout.sector_link_north_required_width;
        attribute sector_link_north_required_height : Real = layout.sector_link_north_required_height;
        attribute sector_link_west_required_length : Real = layout.sector_link_west_required_length;
        attribute sector_link_west_required_width : Real = layout.sector_link_west_required_width;
        attribute sector_link_west_required_height : Real = layout.sector_link_west_required_height;
        attribute sector_link_south_required_length : Real = layout.sector_link_south_required_length;
        attribute sector_link_south_required_width : Real = layout.sector_link_south_required_width;
        attribute sector_link_south_required_height : Real = layout.sector_link_south_required_height;
        attribute cooling_hall_required_length : Real = layout.cooling_hall_required_length;
        attribute cooling_hall_required_width : Real = layout.cooling_hall_required_width;
        attribute cooling_hall_required_height : Real = layout.cooling_hall_required_height;
        attribute cooling_annex_required_length : Real = layout.cooling_annex_required_length;
        attribute cooling_annex_required_width : Real = layout.cooling_annex_required_width;
        attribute cooling_annex_required_height : Real = layout.cooling_annex_required_height;
        attribute cooling_link_required_length : Real = layout.cooling_link_required_length;
        attribute cooling_link_required_width : Real = layout.cooling_link_required_width;
        attribute cooling_link_required_height : Real = layout.cooling_link_required_height;
        attribute turbine_hall_required_length : Real = layout.turbine_hall_required_length;
        attribute turbine_hall_required_width : Real = layout.turbine_hall_required_width;
        attribute turbine_hall_required_height : Real = layout.turbine_hall_required_height;
        attribute cryo_coldbox_required_length : Real = layout.cryo_coldbox_required_length;
        attribute cryo_coldbox_required_width : Real = layout.cryo_coldbox_required_width;
        attribute cryo_coldbox_required_height : Real = layout.cryo_coldbox_required_height;
        attribute cryo_compressors_required_length : Real = layout.cryo_compressors_required_length;
        attribute cryo_compressors_required_width : Real = layout.cryo_compressors_required_width;
        attribute cryo_compressors_required_height : Real = layout.cryo_compressors_required_height;
        attribute fuel_building_required_length : Real = layout.fuel_building_required_length;
        attribute fuel_building_required_width : Real = layout.fuel_building_required_width;
        attribute fuel_building_required_height : Real = layout.fuel_building_required_height;
        attribute reactor_auxiliaries_required_length : Real = layout.reactor_auxiliaries_required_length;
        attribute reactor_auxiliaries_required_width : Real = layout.reactor_auxiliaries_required_width;
        attribute reactor_auxiliaries_required_height : Real = layout.reactor_auxiliaries_required_height;
        attribute power_supply_building_required_length : Real = layout.power_supply_building_required_length;
        attribute power_supply_building_required_width : Real = layout.power_supply_building_required_width;
        attribute power_supply_building_required_height : Real = layout.power_supply_building_required_height;
        attribute electrical_building_required_length : Real = layout.electrical_building_required_length;
        attribute electrical_building_required_width : Real = layout.electrical_building_required_width;
        attribute electrical_building_required_height : Real = layout.electrical_building_required_height;
        attribute service_water_building_required_length : Real = layout.service_water_building_required_length;
        attribute service_water_building_required_width : Real = layout.service_water_building_required_width;
        attribute service_water_building_required_height : Real = layout.service_water_building_required_height;
        attribute maintenance_shop_required_length : Real = layout.maintenance_shop_required_length;
        attribute maintenance_shop_required_width : Real = layout.maintenance_shop_required_width;
        attribute maintenance_shop_required_height : Real = layout.maintenance_shop_required_height;
        attribute site_services_building_required_length : Real = layout.site_services_building_required_length;
        attribute site_services_building_required_width : Real = layout.site_services_building_required_width;
        attribute site_services_building_required_height : Real = layout.site_services_building_required_height;
        attribute administration_required_area : Real = layout.administration_required_area;
        attribute administration_required_height : Real = layout.administration_required_height;
        attribute control_required_area : Real = layout.control_required_area;
        attribute control_required_height : Real = layout.control_required_height;
        attribute security_required_area : Real = layout.security_required_area;
        attribute security_required_height : Real = layout.security_required_height;

        attribute cost_mode : Real = layout.cost_mode;
        attribute sector_length : Real = layout.sector_length;
        attribute sector_width : Real = layout.sector_width;
        attribute sector_height : Real = layout.sector_height;
        attribute parcel_area : Real = layout.parcel_area;
        attribute controlled_air_volume : Real = layout.controlled_air_volume;
        attribute total_clear_area : Real = layout.total_clear_area;
        attribute total_gross_area : Real = layout.total_gross_area;
        attribute total_air_volume : Real = layout.total_air_volume;
        attribute blanket_packages_per_sector : Real = layout.blanket_packages_per_sector;
        attribute packages_per_sector : Real = layout.packages_per_sector;
        attribute material_capacity_volume : Real = layout.material_capacity_volume;
        attribute unused_material_capacity : Real = layout.unused_material_capacity;
        attribute initial_clean_required : Real = layout.initial_clean_required;
        attribute dirty_buffer_required : Real = layout.dirty_buffer_required;
        attribute dirty_store_required : Real = layout.dirty_store_required;
        attribute initial_ready_margin_days : Real = layout.initial_ready_margin_days;
        attribute replacement_ready_margin_days : Real = layout.replacement_ready_margin_days;
        attribute outage_required_days : Real = layout.outage_required_days;
        attribute outage_allowed_days : Real = layout.outage_allowed_days;
        attribute outage_margin_days : Real = layout.outage_margin_days;
        attribute calendar_event_count : Real = layout.calendar_event_count;
        attribute calendar_first_event_year : Real = layout.calendar_first_event_year;
        attribute calendar_last_event_year : Real = layout.calendar_last_event_year;
        attribute cooling_clean_helium_required : Real = layout.cooling_clean_helium_required;
        attribute cooling_clean_salt_required : Real = layout.cooling_clean_salt_required;
        attribute cooling_clean_bundle_required : Real = layout.cooling_clean_bundle_required;
        attribute cooling_dirty_helium_required : Real = layout.cooling_dirty_helium_required;
        attribute cooling_dirty_salt_required : Real = layout.cooling_dirty_salt_required;
        attribute cooling_dirty_bundle_required : Real = layout.cooling_dirty_bundle_required;
        attribute cooling_helium_queue_peak : Real = layout.cooling_helium_queue_peak;
        attribute cooling_salt_queue_peak : Real = layout.cooling_salt_queue_peak;
        attribute cooling_bundle_queue_peak : Real = layout.cooling_bundle_queue_peak;
        attribute cooling_initial_ready_margin_days : Real = layout.cooling_initial_ready_margin_days;
        attribute cooling_replacement_ready_margin_days : Real = layout.cooling_replacement_ready_margin_days;
        attribute cooling_jobs_after_shutdown : Real = layout.cooling_jobs_after_shutdown;
        attribute cooling_last_release_year : Real = layout.cooling_last_release_year;
        attribute cooling_carrier_moves : Real = layout.cooling_carrier_moves;
        attribute clean_positions_allocated : Real = layout.clean_positions_allocated;
        attribute dirty_buffer_positions_allocated : Real = layout.dirty_buffer_positions_allocated;
        attribute dirty_store_positions_allocated : Real = layout.dirty_store_positions_allocated;
        attribute cooling_clean_helium_allocated : Real = layout.cooling_clean_helium_allocated;
        attribute cooling_clean_salt_allocated : Real = layout.cooling_clean_salt_allocated;
        attribute cooling_clean_bundle_allocated : Real = layout.cooling_clean_bundle_allocated;
        attribute cooling_dirty_helium_allocated : Real = layout.cooling_dirty_helium_allocated;
        attribute cooling_dirty_salt_allocated : Real = layout.cooling_dirty_salt_allocated;
        attribute cooling_dirty_bundle_allocated : Real = layout.cooling_dirty_bundle_allocated;
        attribute initial_margin_days : Real = layout.initial_margin_days;
        attribute readiness_margin_days : Real = layout.readiness_margin_days;
        attribute capacity_margin_units : Real = layout.capacity_margin_units;
        attribute route_margin_m : Real = layout.route_margin_m;
        attribute exterior_envelope_qualified : Real = layout.exterior_envelope_qualified;
        attribute sector_load_qualified : Real = layout.sector_load_qualified;
        attribute contamination_procedure_qualified : Real = layout.contamination_procedure_qualified;
        attribute cooling_outage_basis_resolved : Real = layout.cooling_outage_basis_resolved;
        attribute provisional_room_count : Real = layout.provisional_room_count;
        attribute reactor_hall_clear_length : Real = layout.reactor_hall_clear_length;
        attribute reactor_hall_clear_width : Real = layout.reactor_hall_clear_width;
        attribute reactor_hall_clear_height : Real = layout.reactor_hall_clear_height;
        attribute reactor_hall_clear_area : Real = layout.reactor_hall_clear_area;
        attribute reactor_hall_gross_area : Real = layout.reactor_hall_gross_area;
        attribute reactor_hall_air_volume : Real = layout.reactor_hall_air_volume;
        attribute reactor_hall_sub_concrete : Real = layout.reactor_hall_sub_concrete;
        attribute reactor_hall_super_concrete : Real = layout.reactor_hall_super_concrete;
        attribute reactor_hall_sub_formwork : Real = layout.reactor_hall_sub_formwork;
        attribute reactor_hall_super_formwork : Real = layout.reactor_hall_super_formwork;
        attribute reactor_hall_sub_rebar : Real = layout.reactor_hall_sub_rebar;
        attribute reactor_hall_super_rebar : Real = layout.reactor_hall_super_rebar;
        attribute sector_wing_east_clear_length : Real = layout.sector_wing_east_clear_length;
        attribute sector_wing_east_clear_width : Real = layout.sector_wing_east_clear_width;
        attribute sector_wing_east_clear_height : Real = layout.sector_wing_east_clear_height;
        attribute sector_wing_east_clear_area : Real = layout.sector_wing_east_clear_area;
        attribute sector_wing_east_gross_area : Real = layout.sector_wing_east_gross_area;
        attribute sector_wing_east_air_volume : Real = layout.sector_wing_east_air_volume;
        attribute sector_wing_east_sub_concrete : Real = layout.sector_wing_east_sub_concrete;
        attribute sector_wing_east_super_concrete : Real = layout.sector_wing_east_super_concrete;
        attribute sector_wing_east_sub_formwork : Real = layout.sector_wing_east_sub_formwork;
        attribute sector_wing_east_super_formwork : Real = layout.sector_wing_east_super_formwork;
        attribute sector_wing_east_sub_rebar : Real = layout.sector_wing_east_sub_rebar;
        attribute sector_wing_east_super_rebar : Real = layout.sector_wing_east_super_rebar;
        attribute sector_wing_north_clear_length : Real = layout.sector_wing_north_clear_length;
        attribute sector_wing_north_clear_width : Real = layout.sector_wing_north_clear_width;
        attribute sector_wing_north_clear_height : Real = layout.sector_wing_north_clear_height;
        attribute sector_wing_north_clear_area : Real = layout.sector_wing_north_clear_area;
        attribute sector_wing_north_gross_area : Real = layout.sector_wing_north_gross_area;
        attribute sector_wing_north_air_volume : Real = layout.sector_wing_north_air_volume;
        attribute sector_wing_north_sub_concrete : Real = layout.sector_wing_north_sub_concrete;
        attribute sector_wing_north_super_concrete : Real = layout.sector_wing_north_super_concrete;
        attribute sector_wing_north_sub_formwork : Real = layout.sector_wing_north_sub_formwork;
        attribute sector_wing_north_super_formwork : Real = layout.sector_wing_north_super_formwork;
        attribute sector_wing_north_sub_rebar : Real = layout.sector_wing_north_sub_rebar;
        attribute sector_wing_north_super_rebar : Real = layout.sector_wing_north_super_rebar;
        attribute sector_wing_west_clear_length : Real = layout.sector_wing_west_clear_length;
        attribute sector_wing_west_clear_width : Real = layout.sector_wing_west_clear_width;
        attribute sector_wing_west_clear_height : Real = layout.sector_wing_west_clear_height;
        attribute sector_wing_west_clear_area : Real = layout.sector_wing_west_clear_area;
        attribute sector_wing_west_gross_area : Real = layout.sector_wing_west_gross_area;
        attribute sector_wing_west_air_volume : Real = layout.sector_wing_west_air_volume;
        attribute sector_wing_west_sub_concrete : Real = layout.sector_wing_west_sub_concrete;
        attribute sector_wing_west_super_concrete : Real = layout.sector_wing_west_super_concrete;
        attribute sector_wing_west_sub_formwork : Real = layout.sector_wing_west_sub_formwork;
        attribute sector_wing_west_super_formwork : Real = layout.sector_wing_west_super_formwork;
        attribute sector_wing_west_sub_rebar : Real = layout.sector_wing_west_sub_rebar;
        attribute sector_wing_west_super_rebar : Real = layout.sector_wing_west_super_rebar;
        attribute sector_wing_south_clear_length : Real = layout.sector_wing_south_clear_length;
        attribute sector_wing_south_clear_width : Real = layout.sector_wing_south_clear_width;
        attribute sector_wing_south_clear_height : Real = layout.sector_wing_south_clear_height;
        attribute sector_wing_south_clear_area : Real = layout.sector_wing_south_clear_area;
        attribute sector_wing_south_gross_area : Real = layout.sector_wing_south_gross_area;
        attribute sector_wing_south_air_volume : Real = layout.sector_wing_south_air_volume;
        attribute sector_wing_south_sub_concrete : Real = layout.sector_wing_south_sub_concrete;
        attribute sector_wing_south_super_concrete : Real = layout.sector_wing_south_super_concrete;
        attribute sector_wing_south_sub_formwork : Real = layout.sector_wing_south_sub_formwork;
        attribute sector_wing_south_super_formwork : Real = layout.sector_wing_south_super_formwork;
        attribute sector_wing_south_sub_rebar : Real = layout.sector_wing_south_sub_rebar;
        attribute sector_wing_south_super_rebar : Real = layout.sector_wing_south_super_rebar;
        attribute sector_link_east_clear_length : Real = layout.sector_link_east_clear_length;
        attribute sector_link_east_clear_width : Real = layout.sector_link_east_clear_width;
        attribute sector_link_east_clear_height : Real = layout.sector_link_east_clear_height;
        attribute sector_link_east_clear_area : Real = layout.sector_link_east_clear_area;
        attribute sector_link_east_gross_area : Real = layout.sector_link_east_gross_area;
        attribute sector_link_east_air_volume : Real = layout.sector_link_east_air_volume;
        attribute sector_link_east_sub_concrete : Real = layout.sector_link_east_sub_concrete;
        attribute sector_link_east_super_concrete : Real = layout.sector_link_east_super_concrete;
        attribute sector_link_east_sub_formwork : Real = layout.sector_link_east_sub_formwork;
        attribute sector_link_east_super_formwork : Real = layout.sector_link_east_super_formwork;
        attribute sector_link_east_sub_rebar : Real = layout.sector_link_east_sub_rebar;
        attribute sector_link_east_super_rebar : Real = layout.sector_link_east_super_rebar;
        attribute sector_link_north_clear_length : Real = layout.sector_link_north_clear_length;
        attribute sector_link_north_clear_width : Real = layout.sector_link_north_clear_width;
        attribute sector_link_north_clear_height : Real = layout.sector_link_north_clear_height;
        attribute sector_link_north_clear_area : Real = layout.sector_link_north_clear_area;
        attribute sector_link_north_gross_area : Real = layout.sector_link_north_gross_area;
        attribute sector_link_north_air_volume : Real = layout.sector_link_north_air_volume;
        attribute sector_link_north_sub_concrete : Real = layout.sector_link_north_sub_concrete;
        attribute sector_link_north_super_concrete : Real = layout.sector_link_north_super_concrete;
        attribute sector_link_north_sub_formwork : Real = layout.sector_link_north_sub_formwork;
        attribute sector_link_north_super_formwork : Real = layout.sector_link_north_super_formwork;
        attribute sector_link_north_sub_rebar : Real = layout.sector_link_north_sub_rebar;
        attribute sector_link_north_super_rebar : Real = layout.sector_link_north_super_rebar;
        attribute sector_link_west_clear_length : Real = layout.sector_link_west_clear_length;
        attribute sector_link_west_clear_width : Real = layout.sector_link_west_clear_width;
        attribute sector_link_west_clear_height : Real = layout.sector_link_west_clear_height;
        attribute sector_link_west_clear_area : Real = layout.sector_link_west_clear_area;
        attribute sector_link_west_gross_area : Real = layout.sector_link_west_gross_area;
        attribute sector_link_west_air_volume : Real = layout.sector_link_west_air_volume;
        attribute sector_link_west_sub_concrete : Real = layout.sector_link_west_sub_concrete;
        attribute sector_link_west_super_concrete : Real = layout.sector_link_west_super_concrete;
        attribute sector_link_west_sub_formwork : Real = layout.sector_link_west_sub_formwork;
        attribute sector_link_west_super_formwork : Real = layout.sector_link_west_super_formwork;
        attribute sector_link_west_sub_rebar : Real = layout.sector_link_west_sub_rebar;
        attribute sector_link_west_super_rebar : Real = layout.sector_link_west_super_rebar;
        attribute sector_link_south_clear_length : Real = layout.sector_link_south_clear_length;
        attribute sector_link_south_clear_width : Real = layout.sector_link_south_clear_width;
        attribute sector_link_south_clear_height : Real = layout.sector_link_south_clear_height;
        attribute sector_link_south_clear_area : Real = layout.sector_link_south_clear_area;
        attribute sector_link_south_gross_area : Real = layout.sector_link_south_gross_area;
        attribute sector_link_south_air_volume : Real = layout.sector_link_south_air_volume;
        attribute sector_link_south_sub_concrete : Real = layout.sector_link_south_sub_concrete;
        attribute sector_link_south_super_concrete : Real = layout.sector_link_south_super_concrete;
        attribute sector_link_south_sub_formwork : Real = layout.sector_link_south_sub_formwork;
        attribute sector_link_south_super_formwork : Real = layout.sector_link_south_super_formwork;
        attribute sector_link_south_sub_rebar : Real = layout.sector_link_south_sub_rebar;
        attribute sector_link_south_super_rebar : Real = layout.sector_link_south_super_rebar;
        attribute cooling_hall_clear_length : Real = layout.cooling_hall_clear_length;
        attribute cooling_hall_clear_width : Real = layout.cooling_hall_clear_width;
        attribute cooling_hall_clear_height : Real = layout.cooling_hall_clear_height;
        attribute cooling_hall_clear_area : Real = layout.cooling_hall_clear_area;
        attribute cooling_hall_gross_area : Real = layout.cooling_hall_gross_area;
        attribute cooling_hall_air_volume : Real = layout.cooling_hall_air_volume;
        attribute cooling_hall_sub_concrete : Real = layout.cooling_hall_sub_concrete;
        attribute cooling_hall_super_concrete : Real = layout.cooling_hall_super_concrete;
        attribute cooling_hall_sub_formwork : Real = layout.cooling_hall_sub_formwork;
        attribute cooling_hall_super_formwork : Real = layout.cooling_hall_super_formwork;
        attribute cooling_hall_sub_rebar : Real = layout.cooling_hall_sub_rebar;
        attribute cooling_hall_super_rebar : Real = layout.cooling_hall_super_rebar;
        attribute cooling_annex_clear_length : Real = layout.cooling_annex_clear_length;
        attribute cooling_annex_clear_width : Real = layout.cooling_annex_clear_width;
        attribute cooling_annex_clear_height : Real = layout.cooling_annex_clear_height;
        attribute cooling_annex_clear_area : Real = layout.cooling_annex_clear_area;
        attribute cooling_annex_gross_area : Real = layout.cooling_annex_gross_area;
        attribute cooling_annex_air_volume : Real = layout.cooling_annex_air_volume;
        attribute cooling_annex_sub_concrete : Real = layout.cooling_annex_sub_concrete;
        attribute cooling_annex_super_concrete : Real = layout.cooling_annex_super_concrete;
        attribute cooling_annex_sub_formwork : Real = layout.cooling_annex_sub_formwork;
        attribute cooling_annex_super_formwork : Real = layout.cooling_annex_super_formwork;
        attribute cooling_annex_sub_rebar : Real = layout.cooling_annex_sub_rebar;
        attribute cooling_annex_super_rebar : Real = layout.cooling_annex_super_rebar;
        attribute cooling_link_clear_length : Real = layout.cooling_link_clear_length;
        attribute cooling_link_clear_width : Real = layout.cooling_link_clear_width;
        attribute cooling_link_clear_height : Real = layout.cooling_link_clear_height;
        attribute cooling_link_clear_area : Real = layout.cooling_link_clear_area;
        attribute cooling_link_gross_area : Real = layout.cooling_link_gross_area;
        attribute cooling_link_air_volume : Real = layout.cooling_link_air_volume;
        attribute cooling_link_sub_concrete : Real = layout.cooling_link_sub_concrete;
        attribute cooling_link_super_concrete : Real = layout.cooling_link_super_concrete;
        attribute cooling_link_sub_formwork : Real = layout.cooling_link_sub_formwork;
        attribute cooling_link_super_formwork : Real = layout.cooling_link_super_formwork;
        attribute cooling_link_sub_rebar : Real = layout.cooling_link_sub_rebar;
        attribute cooling_link_super_rebar : Real = layout.cooling_link_super_rebar;
        attribute turbine_hall_clear_length : Real = layout.turbine_hall_clear_length;
        attribute turbine_hall_clear_width : Real = layout.turbine_hall_clear_width;
        attribute turbine_hall_clear_height : Real = layout.turbine_hall_clear_height;
        attribute turbine_hall_clear_area : Real = layout.turbine_hall_clear_area;
        attribute turbine_hall_gross_area : Real = layout.turbine_hall_gross_area;
        attribute turbine_hall_air_volume : Real = layout.turbine_hall_air_volume;
        attribute turbine_hall_sub_concrete : Real = layout.turbine_hall_sub_concrete;
        attribute turbine_hall_super_concrete : Real = layout.turbine_hall_super_concrete;
        attribute turbine_hall_sub_formwork : Real = layout.turbine_hall_sub_formwork;
        attribute turbine_hall_super_formwork : Real = layout.turbine_hall_super_formwork;
        attribute turbine_hall_sub_rebar : Real = layout.turbine_hall_sub_rebar;
        attribute turbine_hall_super_rebar : Real = layout.turbine_hall_super_rebar;
        attribute cryo_coldbox_clear_length : Real = layout.cryo_coldbox_clear_length;
        attribute cryo_coldbox_clear_width : Real = layout.cryo_coldbox_clear_width;
        attribute cryo_coldbox_clear_height : Real = layout.cryo_coldbox_clear_height;
        attribute cryo_coldbox_clear_area : Real = layout.cryo_coldbox_clear_area;
        attribute cryo_coldbox_gross_area : Real = layout.cryo_coldbox_gross_area;
        attribute cryo_coldbox_air_volume : Real = layout.cryo_coldbox_air_volume;
        attribute cryo_coldbox_sub_concrete : Real = layout.cryo_coldbox_sub_concrete;
        attribute cryo_coldbox_super_concrete : Real = layout.cryo_coldbox_super_concrete;
        attribute cryo_coldbox_sub_formwork : Real = layout.cryo_coldbox_sub_formwork;
        attribute cryo_coldbox_super_formwork : Real = layout.cryo_coldbox_super_formwork;
        attribute cryo_coldbox_sub_rebar : Real = layout.cryo_coldbox_sub_rebar;
        attribute cryo_coldbox_super_rebar : Real = layout.cryo_coldbox_super_rebar;
        attribute cryo_compressors_clear_length : Real = layout.cryo_compressors_clear_length;
        attribute cryo_compressors_clear_width : Real = layout.cryo_compressors_clear_width;
        attribute cryo_compressors_clear_height : Real = layout.cryo_compressors_clear_height;
        attribute cryo_compressors_clear_area : Real = layout.cryo_compressors_clear_area;
        attribute cryo_compressors_gross_area : Real = layout.cryo_compressors_gross_area;
        attribute cryo_compressors_air_volume : Real = layout.cryo_compressors_air_volume;
        attribute cryo_compressors_sub_concrete : Real = layout.cryo_compressors_sub_concrete;
        attribute cryo_compressors_super_concrete : Real = layout.cryo_compressors_super_concrete;
        attribute cryo_compressors_sub_formwork : Real = layout.cryo_compressors_sub_formwork;
        attribute cryo_compressors_super_formwork : Real = layout.cryo_compressors_super_formwork;
        attribute cryo_compressors_sub_rebar : Real = layout.cryo_compressors_sub_rebar;
        attribute cryo_compressors_super_rebar : Real = layout.cryo_compressors_super_rebar;
        attribute fuel_building_clear_length : Real = layout.fuel_building_clear_length;
        attribute fuel_building_clear_width : Real = layout.fuel_building_clear_width;
        attribute fuel_building_clear_height : Real = layout.fuel_building_clear_height;
        attribute fuel_building_clear_area : Real = layout.fuel_building_clear_area;
        attribute fuel_building_gross_area : Real = layout.fuel_building_gross_area;
        attribute fuel_building_air_volume : Real = layout.fuel_building_air_volume;
        attribute fuel_building_sub_concrete : Real = layout.fuel_building_sub_concrete;
        attribute fuel_building_super_concrete : Real = layout.fuel_building_super_concrete;
        attribute fuel_building_sub_formwork : Real = layout.fuel_building_sub_formwork;
        attribute fuel_building_super_formwork : Real = layout.fuel_building_super_formwork;
        attribute fuel_building_sub_rebar : Real = layout.fuel_building_sub_rebar;
        attribute fuel_building_super_rebar : Real = layout.fuel_building_super_rebar;
        attribute reactor_auxiliaries_clear_length : Real = layout.reactor_auxiliaries_clear_length;
        attribute reactor_auxiliaries_clear_width : Real = layout.reactor_auxiliaries_clear_width;
        attribute reactor_auxiliaries_clear_height : Real = layout.reactor_auxiliaries_clear_height;
        attribute reactor_auxiliaries_clear_area : Real = layout.reactor_auxiliaries_clear_area;
        attribute reactor_auxiliaries_gross_area : Real = layout.reactor_auxiliaries_gross_area;
        attribute reactor_auxiliaries_air_volume : Real = layout.reactor_auxiliaries_air_volume;
        attribute reactor_auxiliaries_sub_concrete : Real = layout.reactor_auxiliaries_sub_concrete;
        attribute reactor_auxiliaries_super_concrete : Real = layout.reactor_auxiliaries_super_concrete;
        attribute reactor_auxiliaries_sub_formwork : Real = layout.reactor_auxiliaries_sub_formwork;
        attribute reactor_auxiliaries_super_formwork : Real = layout.reactor_auxiliaries_super_formwork;
        attribute reactor_auxiliaries_sub_rebar : Real = layout.reactor_auxiliaries_sub_rebar;
        attribute reactor_auxiliaries_super_rebar : Real = layout.reactor_auxiliaries_super_rebar;
        attribute power_supply_building_clear_length : Real = layout.power_supply_building_clear_length;
        attribute power_supply_building_clear_width : Real = layout.power_supply_building_clear_width;
        attribute power_supply_building_clear_height : Real = layout.power_supply_building_clear_height;
        attribute power_supply_building_clear_area : Real = layout.power_supply_building_clear_area;
        attribute power_supply_building_gross_area : Real = layout.power_supply_building_gross_area;
        attribute power_supply_building_air_volume : Real = layout.power_supply_building_air_volume;
        attribute power_supply_building_sub_concrete : Real = layout.power_supply_building_sub_concrete;
        attribute power_supply_building_super_concrete : Real = layout.power_supply_building_super_concrete;
        attribute power_supply_building_sub_formwork : Real = layout.power_supply_building_sub_formwork;
        attribute power_supply_building_super_formwork : Real = layout.power_supply_building_super_formwork;
        attribute power_supply_building_sub_rebar : Real = layout.power_supply_building_sub_rebar;
        attribute power_supply_building_super_rebar : Real = layout.power_supply_building_super_rebar;
        attribute electrical_building_clear_length : Real = layout.electrical_building_clear_length;
        attribute electrical_building_clear_width : Real = layout.electrical_building_clear_width;
        attribute electrical_building_clear_height : Real = layout.electrical_building_clear_height;
        attribute electrical_building_clear_area : Real = layout.electrical_building_clear_area;
        attribute electrical_building_gross_area : Real = layout.electrical_building_gross_area;
        attribute electrical_building_air_volume : Real = layout.electrical_building_air_volume;
        attribute electrical_building_sub_concrete : Real = layout.electrical_building_sub_concrete;
        attribute electrical_building_super_concrete : Real = layout.electrical_building_super_concrete;
        attribute electrical_building_sub_formwork : Real = layout.electrical_building_sub_formwork;
        attribute electrical_building_super_formwork : Real = layout.electrical_building_super_formwork;
        attribute electrical_building_sub_rebar : Real = layout.electrical_building_sub_rebar;
        attribute electrical_building_super_rebar : Real = layout.electrical_building_super_rebar;
        attribute service_water_building_clear_length : Real = layout.service_water_building_clear_length;
        attribute service_water_building_clear_width : Real = layout.service_water_building_clear_width;
        attribute service_water_building_clear_height : Real = layout.service_water_building_clear_height;
        attribute service_water_building_clear_area : Real = layout.service_water_building_clear_area;
        attribute service_water_building_gross_area : Real = layout.service_water_building_gross_area;
        attribute service_water_building_air_volume : Real = layout.service_water_building_air_volume;
        attribute service_water_building_sub_concrete : Real = layout.service_water_building_sub_concrete;
        attribute service_water_building_super_concrete : Real = layout.service_water_building_super_concrete;
        attribute service_water_building_sub_formwork : Real = layout.service_water_building_sub_formwork;
        attribute service_water_building_super_formwork : Real = layout.service_water_building_super_formwork;
        attribute service_water_building_sub_rebar : Real = layout.service_water_building_sub_rebar;
        attribute service_water_building_super_rebar : Real = layout.service_water_building_super_rebar;
        attribute maintenance_shop_clear_length : Real = layout.maintenance_shop_clear_length;
        attribute maintenance_shop_clear_width : Real = layout.maintenance_shop_clear_width;
        attribute maintenance_shop_clear_height : Real = layout.maintenance_shop_clear_height;
        attribute maintenance_shop_clear_area : Real = layout.maintenance_shop_clear_area;
        attribute maintenance_shop_gross_area : Real = layout.maintenance_shop_gross_area;
        attribute maintenance_shop_air_volume : Real = layout.maintenance_shop_air_volume;
        attribute maintenance_shop_sub_concrete : Real = layout.maintenance_shop_sub_concrete;
        attribute maintenance_shop_super_concrete : Real = layout.maintenance_shop_super_concrete;
        attribute maintenance_shop_sub_formwork : Real = layout.maintenance_shop_sub_formwork;
        attribute maintenance_shop_super_formwork : Real = layout.maintenance_shop_super_formwork;
        attribute maintenance_shop_sub_rebar : Real = layout.maintenance_shop_sub_rebar;
        attribute maintenance_shop_super_rebar : Real = layout.maintenance_shop_super_rebar;
        attribute site_services_building_clear_length : Real = layout.site_services_building_clear_length;
        attribute site_services_building_clear_width : Real = layout.site_services_building_clear_width;
        attribute site_services_building_clear_height : Real = layout.site_services_building_clear_height;
        attribute site_services_building_clear_area : Real = layout.site_services_building_clear_area;
        attribute site_services_building_gross_area : Real = layout.site_services_building_gross_area;
        attribute site_services_building_air_volume : Real = layout.site_services_building_air_volume;
        attribute site_services_building_sub_concrete : Real = layout.site_services_building_sub_concrete;
        attribute site_services_building_super_concrete : Real = layout.site_services_building_super_concrete;
        attribute site_services_building_sub_formwork : Real = layout.site_services_building_sub_formwork;
        attribute site_services_building_super_formwork : Real = layout.site_services_building_super_formwork;
        attribute site_services_building_sub_rebar : Real = layout.site_services_building_sub_rebar;
        attribute site_services_building_super_rebar : Real = layout.site_services_building_super_rebar;
        attribute administration_clear_length : Real = layout.administration_clear_length;
        attribute administration_clear_width : Real = layout.administration_clear_width;
        attribute administration_clear_height : Real = layout.administration_clear_height;
        attribute administration_clear_area : Real = layout.administration_clear_area;
        attribute administration_gross_area : Real = layout.administration_gross_area;
        attribute administration_air_volume : Real = layout.administration_air_volume;
        attribute administration_sub_concrete : Real = layout.administration_sub_concrete;
        attribute administration_super_concrete : Real = layout.administration_super_concrete;
        attribute administration_sub_formwork : Real = layout.administration_sub_formwork;
        attribute administration_super_formwork : Real = layout.administration_super_formwork;
        attribute administration_sub_rebar : Real = layout.administration_sub_rebar;
        attribute administration_super_rebar : Real = layout.administration_super_rebar;
        attribute control_clear_length : Real = layout.control_clear_length;
        attribute control_clear_width : Real = layout.control_clear_width;
        attribute control_clear_height : Real = layout.control_clear_height;
        attribute control_clear_area : Real = layout.control_clear_area;
        attribute control_gross_area : Real = layout.control_gross_area;
        attribute control_air_volume : Real = layout.control_air_volume;
        attribute control_sub_concrete : Real = layout.control_sub_concrete;
        attribute control_super_concrete : Real = layout.control_super_concrete;
        attribute control_sub_formwork : Real = layout.control_sub_formwork;
        attribute control_super_formwork : Real = layout.control_super_formwork;
        attribute control_sub_rebar : Real = layout.control_sub_rebar;
        attribute control_super_rebar : Real = layout.control_super_rebar;
        attribute security_clear_length : Real = layout.security_clear_length;
        attribute security_clear_width : Real = layout.security_clear_width;
        attribute security_clear_height : Real = layout.security_clear_height;
        attribute security_clear_area : Real = layout.security_clear_area;
        attribute security_gross_area : Real = layout.security_gross_area;
        attribute security_air_volume : Real = layout.security_air_volume;
        attribute security_sub_concrete : Real = layout.security_sub_concrete;
        attribute security_super_concrete : Real = layout.security_super_concrete;
        attribute security_sub_formwork : Real = layout.security_sub_formwork;
        attribute security_super_formwork : Real = layout.security_super_formwork;
        attribute security_sub_rebar : Real = layout.security_sub_rebar;
        attribute security_super_rebar : Real = layout.security_super_rebar;
        part reactor_hall : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = reactor_hall_clear_length;
            :>> clear_width = reactor_hall_clear_width;
            :>> clear_height = reactor_hall_clear_height;
            :>> clear_area = reactor_hall_clear_area;
            :>> gross_area = reactor_hall_gross_area;
            :>> air_volume = reactor_hall_air_volume;
            :>> sub_concrete = reactor_hall_sub_concrete;
            :>> super_concrete = reactor_hall_super_concrete;
            :>> sub_formwork = reactor_hall_sub_formwork;
            :>> super_formwork = reactor_hall_super_formwork;
            :>> sub_rebar = reactor_hall_sub_rebar;
            :>> super_rebar = reactor_hall_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part sector_wing_east : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = sector_wing_east_clear_length;
            :>> clear_width = sector_wing_east_clear_width;
            :>> clear_height = sector_wing_east_clear_height;
            :>> clear_area = sector_wing_east_clear_area;
            :>> gross_area = sector_wing_east_gross_area;
            :>> air_volume = sector_wing_east_air_volume;
            :>> sub_concrete = sector_wing_east_sub_concrete;
            :>> super_concrete = sector_wing_east_super_concrete;
            :>> sub_formwork = sector_wing_east_sub_formwork;
            :>> super_formwork = sector_wing_east_super_formwork;
            :>> sub_rebar = sector_wing_east_sub_rebar;
            :>> super_rebar = sector_wing_east_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part sector_wing_north : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = sector_wing_north_clear_length;
            :>> clear_width = sector_wing_north_clear_width;
            :>> clear_height = sector_wing_north_clear_height;
            :>> clear_area = sector_wing_north_clear_area;
            :>> gross_area = sector_wing_north_gross_area;
            :>> air_volume = sector_wing_north_air_volume;
            :>> sub_concrete = sector_wing_north_sub_concrete;
            :>> super_concrete = sector_wing_north_super_concrete;
            :>> sub_formwork = sector_wing_north_sub_formwork;
            :>> super_formwork = sector_wing_north_super_formwork;
            :>> sub_rebar = sector_wing_north_sub_rebar;
            :>> super_rebar = sector_wing_north_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part sector_wing_west : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = sector_wing_west_clear_length;
            :>> clear_width = sector_wing_west_clear_width;
            :>> clear_height = sector_wing_west_clear_height;
            :>> clear_area = sector_wing_west_clear_area;
            :>> gross_area = sector_wing_west_gross_area;
            :>> air_volume = sector_wing_west_air_volume;
            :>> sub_concrete = sector_wing_west_sub_concrete;
            :>> super_concrete = sector_wing_west_super_concrete;
            :>> sub_formwork = sector_wing_west_sub_formwork;
            :>> super_formwork = sector_wing_west_super_formwork;
            :>> sub_rebar = sector_wing_west_sub_rebar;
            :>> super_rebar = sector_wing_west_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part sector_wing_south : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = sector_wing_south_clear_length;
            :>> clear_width = sector_wing_south_clear_width;
            :>> clear_height = sector_wing_south_clear_height;
            :>> clear_area = sector_wing_south_clear_area;
            :>> gross_area = sector_wing_south_gross_area;
            :>> air_volume = sector_wing_south_air_volume;
            :>> sub_concrete = sector_wing_south_sub_concrete;
            :>> super_concrete = sector_wing_south_super_concrete;
            :>> sub_formwork = sector_wing_south_sub_formwork;
            :>> super_formwork = sector_wing_south_super_formwork;
            :>> sub_rebar = sector_wing_south_sub_rebar;
            :>> super_rebar = sector_wing_south_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part sector_link_east : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = sector_link_east_clear_length;
            :>> clear_width = sector_link_east_clear_width;
            :>> clear_height = sector_link_east_clear_height;
            :>> clear_area = sector_link_east_clear_area;
            :>> gross_area = sector_link_east_gross_area;
            :>> air_volume = sector_link_east_air_volume;
            :>> sub_concrete = sector_link_east_sub_concrete;
            :>> super_concrete = sector_link_east_super_concrete;
            :>> sub_formwork = sector_link_east_sub_formwork;
            :>> super_formwork = sector_link_east_super_formwork;
            :>> sub_rebar = sector_link_east_sub_rebar;
            :>> super_rebar = sector_link_east_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part sector_link_north : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = sector_link_north_clear_length;
            :>> clear_width = sector_link_north_clear_width;
            :>> clear_height = sector_link_north_clear_height;
            :>> clear_area = sector_link_north_clear_area;
            :>> gross_area = sector_link_north_gross_area;
            :>> air_volume = sector_link_north_air_volume;
            :>> sub_concrete = sector_link_north_sub_concrete;
            :>> super_concrete = sector_link_north_super_concrete;
            :>> sub_formwork = sector_link_north_sub_formwork;
            :>> super_formwork = sector_link_north_super_formwork;
            :>> sub_rebar = sector_link_north_sub_rebar;
            :>> super_rebar = sector_link_north_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part sector_link_west : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = sector_link_west_clear_length;
            :>> clear_width = sector_link_west_clear_width;
            :>> clear_height = sector_link_west_clear_height;
            :>> clear_area = sector_link_west_clear_area;
            :>> gross_area = sector_link_west_gross_area;
            :>> air_volume = sector_link_west_air_volume;
            :>> sub_concrete = sector_link_west_sub_concrete;
            :>> super_concrete = sector_link_west_super_concrete;
            :>> sub_formwork = sector_link_west_sub_formwork;
            :>> super_formwork = sector_link_west_super_formwork;
            :>> sub_rebar = sector_link_west_sub_rebar;
            :>> super_rebar = sector_link_west_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part sector_link_south : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = sector_link_south_clear_length;
            :>> clear_width = sector_link_south_clear_width;
            :>> clear_height = sector_link_south_clear_height;
            :>> clear_area = sector_link_south_clear_area;
            :>> gross_area = sector_link_south_gross_area;
            :>> air_volume = sector_link_south_air_volume;
            :>> sub_concrete = sector_link_south_sub_concrete;
            :>> super_concrete = sector_link_south_super_concrete;
            :>> sub_formwork = sector_link_south_sub_formwork;
            :>> super_formwork = sector_link_south_super_formwork;
            :>> sub_rebar = sector_link_south_sub_rebar;
            :>> super_rebar = sector_link_south_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part cooling_hall : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = cooling_hall_clear_length;
            :>> clear_width = cooling_hall_clear_width;
            :>> clear_height = cooling_hall_clear_height;
            :>> clear_area = cooling_hall_clear_area;
            :>> gross_area = cooling_hall_gross_area;
            :>> air_volume = cooling_hall_air_volume;
            :>> sub_concrete = cooling_hall_sub_concrete;
            :>> super_concrete = cooling_hall_super_concrete;
            :>> sub_formwork = cooling_hall_sub_formwork;
            :>> super_formwork = cooling_hall_super_formwork;
            :>> sub_rebar = cooling_hall_sub_rebar;
            :>> super_rebar = cooling_hall_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part cooling_annex : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = cooling_annex_clear_length;
            :>> clear_width = cooling_annex_clear_width;
            :>> clear_height = cooling_annex_clear_height;
            :>> clear_area = cooling_annex_clear_area;
            :>> gross_area = cooling_annex_gross_area;
            :>> air_volume = cooling_annex_air_volume;
            :>> sub_concrete = cooling_annex_sub_concrete;
            :>> super_concrete = cooling_annex_super_concrete;
            :>> sub_formwork = cooling_annex_sub_formwork;
            :>> super_formwork = cooling_annex_super_formwork;
            :>> sub_rebar = cooling_annex_sub_rebar;
            :>> super_rebar = cooling_annex_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part cooling_link : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = cooling_link_clear_length;
            :>> clear_width = cooling_link_clear_width;
            :>> clear_height = cooling_link_clear_height;
            :>> clear_area = cooling_link_clear_area;
            :>> gross_area = cooling_link_gross_area;
            :>> air_volume = cooling_link_air_volume;
            :>> sub_concrete = cooling_link_sub_concrete;
            :>> super_concrete = cooling_link_super_concrete;
            :>> sub_formwork = cooling_link_sub_formwork;
            :>> super_formwork = cooling_link_super_formwork;
            :>> sub_rebar = cooling_link_sub_rebar;
            :>> super_rebar = cooling_link_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part turbine_hall : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = turbine_hall_clear_length;
            :>> clear_width = turbine_hall_clear_width;
            :>> clear_height = turbine_hall_clear_height;
            :>> clear_area = turbine_hall_clear_area;
            :>> gross_area = turbine_hall_gross_area;
            :>> air_volume = turbine_hall_air_volume;
            :>> sub_concrete = turbine_hall_sub_concrete;
            :>> super_concrete = turbine_hall_super_concrete;
            :>> sub_formwork = turbine_hall_sub_formwork;
            :>> super_formwork = turbine_hall_super_formwork;
            :>> sub_rebar = turbine_hall_sub_rebar;
            :>> super_rebar = turbine_hall_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part cryo_coldbox : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = cryo_coldbox_clear_length;
            :>> clear_width = cryo_coldbox_clear_width;
            :>> clear_height = cryo_coldbox_clear_height;
            :>> clear_area = cryo_coldbox_clear_area;
            :>> gross_area = cryo_coldbox_gross_area;
            :>> air_volume = cryo_coldbox_air_volume;
            :>> sub_concrete = cryo_coldbox_sub_concrete;
            :>> super_concrete = cryo_coldbox_super_concrete;
            :>> sub_formwork = cryo_coldbox_sub_formwork;
            :>> super_formwork = cryo_coldbox_super_formwork;
            :>> sub_rebar = cryo_coldbox_sub_rebar;
            :>> super_rebar = cryo_coldbox_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part cryo_compressors : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = cryo_compressors_clear_length;
            :>> clear_width = cryo_compressors_clear_width;
            :>> clear_height = cryo_compressors_clear_height;
            :>> clear_area = cryo_compressors_clear_area;
            :>> gross_area = cryo_compressors_gross_area;
            :>> air_volume = cryo_compressors_air_volume;
            :>> sub_concrete = cryo_compressors_sub_concrete;
            :>> super_concrete = cryo_compressors_super_concrete;
            :>> sub_formwork = cryo_compressors_sub_formwork;
            :>> super_formwork = cryo_compressors_super_formwork;
            :>> sub_rebar = cryo_compressors_sub_rebar;
            :>> super_rebar = cryo_compressors_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part fuel_building : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = fuel_building_clear_length;
            :>> clear_width = fuel_building_clear_width;
            :>> clear_height = fuel_building_clear_height;
            :>> clear_area = fuel_building_clear_area;
            :>> gross_area = fuel_building_gross_area;
            :>> air_volume = fuel_building_air_volume;
            :>> sub_concrete = fuel_building_sub_concrete;
            :>> super_concrete = fuel_building_super_concrete;
            :>> sub_formwork = fuel_building_sub_formwork;
            :>> super_formwork = fuel_building_super_formwork;
            :>> sub_rebar = fuel_building_sub_rebar;
            :>> super_rebar = fuel_building_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part reactor_auxiliaries : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = reactor_auxiliaries_clear_length;
            :>> clear_width = reactor_auxiliaries_clear_width;
            :>> clear_height = reactor_auxiliaries_clear_height;
            :>> clear_area = reactor_auxiliaries_clear_area;
            :>> gross_area = reactor_auxiliaries_gross_area;
            :>> air_volume = reactor_auxiliaries_air_volume;
            :>> sub_concrete = reactor_auxiliaries_sub_concrete;
            :>> super_concrete = reactor_auxiliaries_super_concrete;
            :>> sub_formwork = reactor_auxiliaries_sub_formwork;
            :>> super_formwork = reactor_auxiliaries_super_formwork;
            :>> sub_rebar = reactor_auxiliaries_sub_rebar;
            :>> super_rebar = reactor_auxiliaries_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part power_supply_building : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = power_supply_building_clear_length;
            :>> clear_width = power_supply_building_clear_width;
            :>> clear_height = power_supply_building_clear_height;
            :>> clear_area = power_supply_building_clear_area;
            :>> gross_area = power_supply_building_gross_area;
            :>> air_volume = power_supply_building_air_volume;
            :>> sub_concrete = power_supply_building_sub_concrete;
            :>> super_concrete = power_supply_building_super_concrete;
            :>> sub_formwork = power_supply_building_sub_formwork;
            :>> super_formwork = power_supply_building_super_formwork;
            :>> sub_rebar = power_supply_building_sub_rebar;
            :>> super_rebar = power_supply_building_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part electrical_building : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = electrical_building_clear_length;
            :>> clear_width = electrical_building_clear_width;
            :>> clear_height = electrical_building_clear_height;
            :>> clear_area = electrical_building_clear_area;
            :>> gross_area = electrical_building_gross_area;
            :>> air_volume = electrical_building_air_volume;
            :>> sub_concrete = electrical_building_sub_concrete;
            :>> super_concrete = electrical_building_super_concrete;
            :>> sub_formwork = electrical_building_sub_formwork;
            :>> super_formwork = electrical_building_super_formwork;
            :>> sub_rebar = electrical_building_sub_rebar;
            :>> super_rebar = electrical_building_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part service_water_building : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = service_water_building_clear_length;
            :>> clear_width = service_water_building_clear_width;
            :>> clear_height = service_water_building_clear_height;
            :>> clear_area = service_water_building_clear_area;
            :>> gross_area = service_water_building_gross_area;
            :>> air_volume = service_water_building_air_volume;
            :>> sub_concrete = service_water_building_sub_concrete;
            :>> super_concrete = service_water_building_super_concrete;
            :>> sub_formwork = service_water_building_sub_formwork;
            :>> super_formwork = service_water_building_super_formwork;
            :>> sub_rebar = service_water_building_sub_rebar;
            :>> super_rebar = service_water_building_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part maintenance_shop : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = maintenance_shop_clear_length;
            :>> clear_width = maintenance_shop_clear_width;
            :>> clear_height = maintenance_shop_clear_height;
            :>> clear_area = maintenance_shop_clear_area;
            :>> gross_area = maintenance_shop_gross_area;
            :>> air_volume = maintenance_shop_air_volume;
            :>> sub_concrete = maintenance_shop_sub_concrete;
            :>> super_concrete = maintenance_shop_super_concrete;
            :>> sub_formwork = maintenance_shop_sub_formwork;
            :>> super_formwork = maintenance_shop_super_formwork;
            :>> sub_rebar = maintenance_shop_sub_rebar;
            :>> super_rebar = maintenance_shop_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part site_services_building : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = site_services_building_clear_length;
            :>> clear_width = site_services_building_clear_width;
            :>> clear_height = site_services_building_clear_height;
            :>> clear_area = site_services_building_clear_area;
            :>> gross_area = site_services_building_gross_area;
            :>> air_volume = site_services_building_air_volume;
            :>> sub_concrete = site_services_building_sub_concrete;
            :>> super_concrete = site_services_building_super_concrete;
            :>> sub_formwork = site_services_building_sub_formwork;
            :>> super_formwork = site_services_building_super_formwork;
            :>> sub_rebar = site_services_building_sub_rebar;
            :>> super_rebar = site_services_building_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part administration : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = administration_clear_length;
            :>> clear_width = administration_clear_width;
            :>> clear_height = administration_clear_height;
            :>> clear_area = administration_clear_area;
            :>> gross_area = administration_gross_area;
            :>> air_volume = administration_air_volume;
            :>> sub_concrete = administration_sub_concrete;
            :>> super_concrete = administration_super_concrete;
            :>> sub_formwork = administration_sub_formwork;
            :>> super_formwork = administration_super_formwork;
            :>> sub_rebar = administration_sub_rebar;
            :>> super_rebar = administration_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part control : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = control_clear_length;
            :>> clear_width = control_clear_width;
            :>> clear_height = control_clear_height;
            :>> clear_area = control_clear_area;
            :>> gross_area = control_gross_area;
            :>> air_volume = control_air_volume;
            :>> sub_concrete = control_sub_concrete;
            :>> super_concrete = control_super_concrete;
            :>> sub_formwork = control_sub_formwork;
            :>> super_formwork = control_super_formwork;
            :>> sub_rebar = control_sub_rebar;
            :>> super_rebar = control_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        part security : 'Facility Building' {
            :>> enabled = facilities_enabled;
            :>> clear_length = security_clear_length;
            :>> clear_width = security_clear_width;
            :>> clear_height = security_clear_height;
            :>> clear_area = security_clear_area;
            :>> gross_area = security_gross_area;
            :>> air_volume = security_air_volume;
            :>> sub_concrete = security_sub_concrete;
            :>> super_concrete = security_super_concrete;
            :>> sub_formwork = security_sub_formwork;
            :>> super_formwork = security_super_formwork;
            :>> sub_rebar = security_sub_rebar;
            :>> super_rebar = security_super_rebar;
            :>> sub_concrete_rate = 'Buildings'::sub_concrete_rate;
            :>> sub_formwork_rate = 'Buildings'::sub_formwork_rate;
            :>> sub_rebar_rate = 'Buildings'::sub_rebar_rate;
            :>> super_concrete_rate = 'Buildings'::super_concrete_rate;
            :>> super_formwork_rate = 'Buildings'::super_formwork_rate;
            :>> super_rebar_rate = 'Buildings'::super_rebar_rate;
            :>> civil_cpi_ratio = 'Buildings'::civil_cpi_ratio;
            :>> civil_rate_multiplier = 'Buildings'::civil_rate_multiplier;
            :>> tonne_interpretation_kg = 'Buildings'::tonne_interpretation_kg;
        }
        calc ventilation : 'Facility Ventilation Cost' {
            in served_volume_in = controlled_air_volume;
            in coefficient_in = ventilation_coefficient;
            in exponent_in = ventilation_exponent;
            in cpi_ratio_in = ventilation_cpi_ratio;
        }
        part nuclear_ventilation : 'Facility Service Account' { :>> capital_cost = ventilation.cost_2025; }
        calc site_allowance : 'Facility Site Allowance' {
            in active_in = active;
            in amount_in = retained_site_improvements;
        }
        part site_improvements : 'Facility Service Account' { :>> capital_cost = site_allowance.cost; }
        calc civil_rollup : 'Facility Civil Rollup' {
            in reactor_hall_in = reactor_hall.capital_cost;
            in sector_wing_east_in = sector_wing_east.capital_cost;
            in sector_wing_north_in = sector_wing_north.capital_cost;
            in sector_wing_west_in = sector_wing_west.capital_cost;
            in sector_wing_south_in = sector_wing_south.capital_cost;
            in sector_link_east_in = sector_link_east.capital_cost;
            in sector_link_north_in = sector_link_north.capital_cost;
            in sector_link_west_in = sector_link_west.capital_cost;
            in sector_link_south_in = sector_link_south.capital_cost;
            in cooling_hall_in = cooling_hall.capital_cost;
            in cooling_annex_in = cooling_annex.capital_cost;
            in cooling_link_in = cooling_link.capital_cost;
            in turbine_hall_in = turbine_hall.capital_cost;
            in cryo_coldbox_in = cryo_coldbox.capital_cost;
            in cryo_compressors_in = cryo_compressors.capital_cost;
            in fuel_building_in = fuel_building.capital_cost;
            in reactor_auxiliaries_in = reactor_auxiliaries.capital_cost;
            in power_supply_building_in = power_supply_building.capital_cost;
            in electrical_building_in = electrical_building.capital_cost;
            in service_water_building_in = service_water_building.capital_cost;
            in maintenance_shop_in = maintenance_shop.capital_cost;
            in site_services_building_in = site_services_building.capital_cost;
            in administration_in = administration.capital_cost;
            in control_in = control.capital_cost;
            in security_in = security.capital_cost;
        }
        attribute civil_capital : Real = civil_rollup.civil_capital;
        calc facility_accounts : 'Facility Account Selection' {
            in civil_in = civil_capital;
            in ventilation_in = nuclear_ventilation.capital_cost;
            in site_in = site_improvements.capital_cost;
            in legacy_in = buildings_cost.cost;
            in mode_in = cost_mode;
        }
        attribute installed_facility_capital : Real = facility_accounts.installed_facility_capital;
        attribute layout_buildings_capital : Real = facility_accounts.layout_buildings_capital;
        calc facility_land : 'Facility Land Cost' {
            in parcel_area_in = parcel_area;
            in rate_per_acre_in = land_rate_per_acre;
        }
        attribute layout_land_cost : Real = facility_land.cost;
        // WI-057: the buildings's own facts, moved from the plant (formerly plant-level inputs)
        // CAS21 grouped base-cost sums [$] (WI-025 D1; instance binds -- fuel-keyed).
        attribute bldg_fixed_base : Real;
        attribute bldg_fus_base : Real;
        attribute bldg_staff_base : Real;
        attribute bldg_the_base : Real;
        attribute bldg_th_base : Real;
        attribute bldg_et_base : Real;
        doc /*
        CAS21 buildings and site facilities. Active WI-068 mode sums the25
        physical civil components, nuclear ventilation and the identified site
        allowance. Equipment geometry and dated maintenance demand size their
        spaces; installation/service omissions remain explicit in the design.
        Legacy mode preserves the six grouped 1costingFE scaling expressions.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
        **Ref**: costs.py:97-152; work/active/WI-068_layout-based-facilities/design.md
        **Basis**: Reviewed conceptual facility quantities and commodity prices;
        legacy grouping retained for matched controls and dormant designs.
        */
        :>> scope = 'CAS Scope'::shared;
        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----
        attribute p_et : Real;   // <- pb.p_et
        attribute p_fus : Real;   // <- plasma.p_fus
        attribute p_th : Real;   // <- pb.p_th
        attribute p_the : Real;   // <- pb.p_the
        :>> capital_cost = facility_accounts.cost;
        // ---- template calcs (WI-057): the analyses this part owns ----
        calc buildings_cost : 'Buildings Cost' {
            in fixed_base = bldg_fixed_base;
            in fus_base = bldg_fus_base;
            in staff_base = bldg_staff_base;
            in the_base = bldg_the_base;
            in th_base = bldg_th_base;
            in et_base = bldg_et_base;
            in p_fus = 'Buildings'::p_fus;
            in p_the_in = p_the;
            in p_th_in = p_th;
            in p_et_in = p_et;
        }
    }
}
