package mfe_subsystems {
    private import ScalarValues::*;
    private import mfe_interfaces::*;
    private import mfe_power_cycle::*;
    private import mfe_power_balance::*;
    private import mfe_account_costs::*;
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
        doc /*
        CAS22.1.5 Primary structure and support (gravity supports, thermal
        shields, inter-coil structure, machine base). Cost drivers feed
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
        // PF coil power [MW]
        attribute p_pf : Real;
        doc /*
        CAS22.1.7 Power supplies (steady-state: high-current DC for SC magnets,
        switchgear). Cost driver feeds 'Power Supplies Cost'.

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
        attribute eta_th : Real = cycle.eta_th;
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
        calc turbine_cost : 'Linear Power Cost' {
            in power = p_the;
            in cost_per_mw = 'Turbine Plant'::cost_per_mw;
            in n_mod_in = n_mod;
        }
    }

    part def 'Electric Plant' :> 'CAS24 Electric Plant' {
        doc /*
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
        power = p_et. (1costingFE numbers this account CAS25 -- see header note.)

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

    // --- Buildings (CAS21, pass-through) ---

    part def 'Buildings' :> 'CAS21 Structures' {
        // WI-057: the buildings's own facts, moved from the plant (formerly plant-level inputs)
        // CAS21 grouped base-cost sums [$] (WI-025 D1; instance binds -- fuel-keyed).
        attribute bldg_fixed_base : Real;
        attribute bldg_fus_base : Real;
        attribute bldg_staff_base : Real;
        attribute bldg_the_base : Real;
        attribute bldg_th_base : Real;
        attribute bldg_et_base : Real;
        doc /*
        CAS21 Buildings and site facilities. The 1costingFE building model is a
        per-building dictionary loop with fuel-keyed base costs and per-building
        scaling bases (out of the codegen envelope: needs sum/lookup). Its cost
        is therefore a plant INPUT (`capital_cost` set directly), a documented
        initial-model pass-through for Stage-3 deepening.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
        **Ref**: costs.py:97-152 (cas21_buildings -- dict loop, out of envelope)
        **Basis**: Pass-through; buildings model needs sum/lookup constructs
        */
        :>> scope = 'CAS Scope'::shared;
        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----
        attribute p_et : Real;   // <- pb.p_et
        attribute p_fus : Real;   // <- plasma.p_fus
        attribute p_th : Real;   // <- pb.p_th
        attribute p_the : Real;   // <- pb.p_the
        :>> capital_cost = buildings_cost.cost;
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
