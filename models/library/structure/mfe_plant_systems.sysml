package mfe_plant_systems {
    private import ScalarValues::*;
    private import mfe_interfaces::*;
    private import mfe_vacuum::*;
    private import mfe_primary_loop::*;
    private import mfe_fuel_cycle::*;
    private import mfe_cryo_plant::*;
    private import mfe_account_costs::*;

    part def 'Primary Heat Transport' {
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
        attribute mdot_loop_ref : Real;
        attribute dp_loop_ref : Real;
        attribute f_loss : Real default 1.0;
        attribute eta_is : Real;
        attribute eta_drive : Real default 1.0;
        // C220200 coolant (two-term, plant-total).
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
        attribute coolant_cost : Real = coolant.cost;
        attribute mdot_loop : Real = primary_loop.mdot_loop;
        attribute p_loop_margin : Real = primary_loop.p_loop_margin;
        attribute p_pump_total : Real = primary_loop.p_pump_total;
        attribute q_recovered_total : Real = primary_loop.q_recovered_total;
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
            in dp_loop_ref_in = dp_loop_ref;
            in f_loss_in = f_loss;
            in eta_is_in = eta_is;
            in eta_drive_in = eta_drive;
            in loop_live_in = loop_live;
            in p_pump_direct_in = p_pump_direct;
            in eta_p_direct_in = eta_p_direct;
        }
        calc coolant : 'Coolant Cost' {
            in primary_base = coolant_primary_base;
            in p_net = 'Primary Heat Transport'::p_net;
            in intermediate_base = coolant_intermediate_base;
            in p_th_in = p_th;
            in n_mod_in = n_mod;
        }
    }

    part def 'Cryoplant' {
        doc /*
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
        attribute aux_cryo_base : Real;
        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----
        attribute aux_per_mw : Real;   // <- 'MFE Power Plant'::aux_per_mw
        attribute n_mod : Real;   // <- 'MFE Power Plant'::n_mod
        attribute p_th : Real;   // <- pb.p_th
        attribute q_nuc_cryo : Real;   // <- magnet.winding_pack.q_nuc_cryo
        attribute vol_cold_total : Real;   // <- magnet.vol_cold_total
        // ---- EXPOSEs (WI-057): this part's calc outputs, readable outside as <part>.<name> ----
        attribute aux_cooling_cost : Real = aux_cooling.cost;
        attribute cryo_cost : Real = aux_cooling.cryo_cost;
        attribute p_elec : Real = cryo_elec.p_elec;
        // ---- template calcs (WI-057): the analyses this part owns ----
        calc cryo_elec : 'Cryoplant Electrical Power' {
            in q_nuc = q_nuc_cryo;
            // WI-036: the cold volume is now computed from the sized winding
            // pack, with vol_cold_cryo carried into that calc as an additive
            // settable term (see the wp_volume usage above).
            in vol_cold = vol_cold_total;
            in p_fixed = p_fixed_cryo;
            in f_uplift = f_uplift_cryo;
            in T_cold = T_cold_cryo;
            in T_amb = T_amb_cryo;
            in f_carnot = f_carnot_cryo;
            in p_direct = p_cryo;
        }
        calc aux_cooling : 'Aux Cooling Cost' {
            in aux_per_mw_in = aux_per_mw;
            in p_th_in = p_th;
            in cryo_base = aux_cryo_base;
            in p_cryo = cryo_elec.p_elec;
            in n_mod_in = n_mod;
        }
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
        // cost prices; the margin is reported, never asserted (the recovery
        // semantics are an owner decision -- see the instance). Dormant-safe by
        // the WI-024 pattern: a concept binding nothing gets a lossless loop.
        // recovery fraction of the unburned tritium stream [1]
        attribute t_recycle : Real default 1.0;
        // breeder-to-supply extraction efficiency [1]
        attribute eta_extract : Real default 1.0;
        // tritium decay constant [1/s]
        attribute lambda_T : Real default 0.0;
        // held tritium inventory [atoms]
        attribute I_total : Real default 0.0;
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
        attribute exhaust_rate : Real = fuel.exhaust_rate;
        attribute fuel_handling_cost : Real = fuel_handling.cost;
        // ---- template calcs (WI-057): the analyses this part owns ----
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
        calc fuel_handling : 'Plant Power-Law Cost' {
            in base = fuel_handling_base; in power = p_net; in n_mod_in = n_mod;
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
