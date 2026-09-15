package mfe_plant {
    private import ScalarValues::*;
    private import mfe_power_core::*;
    private import mfe_plasma::*;
    private import mfe_magnet_parts::*;
    private import mfe_radial_build_parts::*;
    private import mfe_plant_systems::*;
    private import mfe_interfaces::*;
    private import mfe_subsystems::*;
    private import mfe_plasma_scaling::*;
    private import mfe_plasma_sustainment::*;
    private import mfe_power_balance::*;
    private import mfe_cryo_plant::*;
    private import mfe_heating_chain::*;
    private import mfe_primary_loop::*;
    private import mfe_power_cycle::*;
    private import mfe_magnet_cost::*;
    private import mfe_magnet_field::*;
    private import mfe_account_costs::*;
    private import mfe_lcoe_dcf::*;
    private import mfe_lifecycle::*;
    private import mfe_fuel_cycle::*;
    private import mfe_divertor_heat::*;
    private import mfe_vacuum::*;
    private import mfe_viability::*;

    abstract part def 'MFE Power Plant' {
        doc /*
        Confinement-agnostic magnetic-fusion power plant. Composes the WI-009
        power-core subsystems and the shared/BOP costed components, wires the
        physics -> cost -> LCOE calc pipeline, and asserts power, heating,
        magnet, primary-loop, cycle-domain and divertor viability constraints.
        Instance-specific assertions extend these; the generated constraint
        catalog records the executable set. The MFE analogue of ife_plant's 'IFE Power Plant', one
        level richer (a full physics spine and a bottom-up CAS rollup).

        Abstract: WI-011 specializes it with concept-09 (stellarator) values and
        the family density closure. All parameters here are inputs or defaulted
        calibration constants -- no concept-specific values (MR-3).

        MONEY UNIT: the whole rollup and LCOE are in DOLLARS ($). WI-009's
        'Magnet Coil Cost' omits the 1costingFE /1e6 M$ conversion, so it yields
        $; to stay consistent, every account unit-cost input (blanket unit cost,
        per-MW BOP rates, power-supply/divertor bases, pass-through capitals) and
        annual O&M must be supplied in $ by WI-011 (1costingFE constants are M$;
        multiply by 1e6). total_capital [$], annual_om [$/yr] -> lcoe [$/MWh].

        PHYSICS-SPINE / COST-SPINE: WI-009's 'MFE Power Balance Calc' exposes
        p_th, p_the, p_et as outputs (alongside p_net, q_eng, rec_frac), so the
        volume/power-scaled account costs read the forward-computed powers
        directly via `pb.p_th` etc. -- the full forward pass (geometry -> fusion
        power -> power balance -> per-account cost -> LCOE) stays intact with no
        externally injected power values.

        **Source**: models/designs/generic_ife/ife_plant.sysml
        **Ref**: 'IFE Power Plant' (subsystem composition + calc-wired LCOE idiom)
        **Basis**: WI-009 design Layer 2 plant idiom; MFE physics->cost->LCOE spine
        */

        // =====================================================================
        // SUBSYSTEMS
        // =====================================================================

        // MFE-divergent power core (WI-009 mfe_power_core).
        // WI-057: the plasma and the plant systems the calcs already model, as parts.
        part plasma : 'Plasma' {
            // WI-057: inputs the plant wires from the parts and calcs that produce them
            :>> B = magnet.B;
        }
        part heat_transport : 'Primary Heat Transport' {
            // WI-057: inputs the plant wires from the parts and calcs that produce them
            :>> n_mod = 'MFE Power Plant'::n_mod;
            :>> p_net = pb.p_net;
            :>> p_th = pb.p_th;
            :>> q_source = blanket.q_source;
        }
        part cryoplant : 'Cryoplant' {
            // WI-057: inputs the plant wires from the parts and calcs that produce them
            :>> aux_per_mw = 'MFE Power Plant'::aux_per_mw;
            :>> n_mod = 'MFE Power Plant'::n_mod;
            :>> p_th = pb.p_th;
            :>> q_nuc_cryo = magnet.winding_pack.q_nuc_cryo;
            :>> vol_cold_total = magnet.vol_cold_total;
            :>> n_coils = magnet.coil.n_coils;
            :>> c_coil = magnet.coil.c_coil;
            :>> wp_side = magnet.winding_pack.wp_side;
            :>> I_turn = magnet.coil.turn_current;
            :>> m_support = magnet.m_support;
        }
        part fuel_cycle : 'Fuel Cycle' {
            // WI-057: inputs the plant wires from the parts and calcs that produce them
            :>> availability = calendar.availability;
            :>> n_mod = 'MFE Power Plant'::n_mod;
            :>> p_fus = plasma.p_fus;
            :>> p_net = pb.p_net;
            :>> tbr = blanket.tbr;
        }
        part vacuum_pumping : 'Vacuum Pumping' {
            // WI-057: inputs the plant wires from the parts and calcs that produce them
            :>> burn_rate = fuel_cycle.burn_rate;
            :>> exhaust_rate = fuel_cycle.exhaust_rate;
        }
        part magnet : 'Magnet System' {
            part :>> winding_pack {
                :>> T_inventory = cryoplant.T_cold_cryo;
            }
            :>> r_coil = rb.r_coil;   // coil bore = radial-build vessel_or (WI-021)
            // WI-036: the winding-pack side and the winding length are now
            // COMPUTED too -- the pack is sized by the current it carries and
            // the length follows the coil bore (WI-058; WI-036 had it follow
            // the major radius). j_wp and c_coil_ref are the settable levers
            // that replaced them.
            // WI-044: the casing mass is COMPUTED from the coil set's stored
            // energy (which sees the coil bore); m_casing_ref is the settable
            // anchor that replaced the held mass.
            // WI-057: inputs the plant wires from the parts and calcs that produce them
            :>> r_coil_centre = rb.r_coil_centre;
            // T-021 (2026-09-11): the coil's major radius rides with the plasma's. WI-057 owns R0 on
            // 'Modular Coil' and R on 'Plasma', so the binding sits on the nested coil part.
            part :>> coil {
                :>> R0 = plasma.R {
                    doc /*
                    Major plasma/axis radius [m], owned by the plant's plasma part (WI-057; was the containing plant).

                    Source: work/analysis/20260911-230953_radius-ownership-evidence/source-meaning.md
                    Ref: ## Model and existing source interpretation; ## Assessment; revision 2f8856b7
                    Basis: [INHERITED: T-021@2f8856b7] Existing model-intent interpretation: one shared plasma/axis scale. This does not equate real modular-coil surfaces; coil-bore and coil-centre minor radii remain distinct.
                    Last Updated: 2026-09-11
                    */
                }
            }
        }
        part heating : 'Heating and CD' {
        }
        part divertor : 'Divertor' {
            // WI-057: inputs the plant wires from the parts and calcs that produce them
            :>> R = plasma.R;
            :>> p_alpha_heat = plasma.p_alpha_heat;
            :>> p_aux_required = plasma.p_aux_required;
            :>> p_coupled = operating_heat.p_coupled;   // WI-050: the operating demand
            :>> p_installed_coupled = heating.p_coupled;   // WI-050: the installed delivery
            :>> p_rad = plasma.p_rad;
            :>> p_th = pb.p_th;
        }

        // Shared power core (mfe_subsystems). Material volumes forward-computed
        // from the radial build (WI-021), replacing the injected constants.
        part blanket : 'Blanket' {
            :>> blanket_vol = rb.blanket_vol;
            // WI-057: inputs the plant wires from the parts and calcs that produce them
            :>> p_coupled = operating_heat.p_coupled;   // WI-050: the operating demand
            :>> p_fus = plasma.p_fus;
            :>> p_th = pb.p_th;
            part :>> first_wall {
                :>> p_fus = plasma.p_fus;
                :>> wall_area = rb.wall_area;
            }
        }
        part shield : 'Shield' {
            :>> shield_vol = rb.shield_vol;
            // WI-057: inputs the plant wires from the parts and calcs that produce them
            :>> p_th = pb.p_th;
        }
        part structure : 'Primary Structure' {
            :>> structure_vol = rb.structure_vol;
            // WI-057: inputs the plant wires from the parts and calcs that produce them
            :>> p_et = pb.p_et;
        }
        part vessel : 'Vacuum Vessel' {
            :>> vessel_vol = rb.vessel_vol;
            // WI-057: inputs the plant wires from the parts and calcs that produce them
            :>> p_et = pb.p_et;
        }
        part power_supplies : 'Power Supplies' {
            :>> p_tf_extra = cryoplant.p_drive;
            // WI-057: inputs the plant wires from the parts and calcs that produce them
            :>> p_et = pb.p_et;
        }

        // Balance of plant (mfe_subsystems).
        part turbine : 'Turbine Plant' {
            // WI-057: inputs the plant wires from the parts and calcs that produce them
            :>> T_out = heat_transport.T_out;
            :>> n_mod = 'MFE Power Plant'::n_mod;
            :>> p_the = pb.p_the;
        }
        part electric_plant : 'Electric Plant' {
            // WI-057: inputs the plant wires from the parts and calcs that produce them
            :>> n_mod = 'MFE Power Plant'::n_mod;
            :>> p_et = pb.p_et;
        }
        part heat_rejection : 'Heat Rejection' {
            // WI-057: inputs the plant wires from the parts and calcs that produce them
            :>> n_mod = 'MFE Power Plant'::n_mod;
            :>> p_th = pb.p_th;
        }
        part misc_plant : 'Miscellaneous Plant' {
            // WI-057: inputs the plant wires from the parts and calcs that produce them
            :>> n_mod = 'MFE Power Plant'::n_mod;
            :>> p_et = pb.p_et;
        }

        // Forward-computed direct accounts (WI-025): CAS21 via buildings_cost,
        // CAS10 via precon_cost; CAS27 remains a pass-through (WI-011, in $).
        part buildings : 'Buildings' {
            // WI-057: inputs the plant wires from the parts and calcs that produce them
            :>> p_et = pb.p_et;
            :>> p_fus = plasma.p_fus;
            :>> p_th = pb.p_th;
            :>> p_the = pb.p_the;
        }
        // =====================================================================
        // ENERGY AND MATERIAL TOPOLOGY (WI-057, design D7 / § 3). Each connection declares an
        // exchange the calcs already compute; the chain is named beside it. Declarative in this
        // pipeline (codegen reads no connection). No flow declarations: the port item types say
        // what moves and no consumer reads an item-level endpoint here (design D7).
        // =====================================================================
        connect plasma.neutron_out to blanket.neutron_in;               // blanket.p_fus <- plasma.p_fus; source_heat, x mn
        connect heating.power_to_plasma to plasma.heat_in;              // operating_heat.p_coupled (WI-050): accounted at the blanket (source_heat.p_input_in), the divertor (divheat) and the balance (pb)
        connect plasma.alpha_out to divertor.heat_in;                   // divertor.p_alpha_heat, p_rad_core, p_aux_required <- plasma
        connect blanket.coolant to heat_transport.hot_in {
            doc /* heat_transport.q_source <- blanket.q_source (primary_loop.q_source_in). the connection where the coolant premise lives structurally: the model's loop is WI-045's representative helium circuit (Moscato 2017, EU DEMO HCLL balance of plant); the Stellaris source cools the breeding zone with water at PWR conditions and the first wall with helium at 8 MPa (stellaris-design-details output.md lines 1490-1491, 1534-1536) -- goal structural-decomposition fact 6, surfaced and carried as a follow-on, not changed by WI-057. */
        }
        connect heat_transport.hot_out to turbine.coolant;              // turbine.T_out <- heat_transport.T_out (cycle); pb.q_recovered_in
        connect turbine.gross_electric to electric_plant.gross_in;      // pb.eta_th_in = turbine.eta_th -> p_et; electric_plant.p_et
        connect electric_plant.recirculating to heating.electric_in;    // pb.p_wallplug_in = operating_heat.p_wallplug (WI-050)
        connect electric_plant.recirculating to heat_transport.electric_in;   // pb.p_pump_total_in = heat_transport.p_pump_total
        connect electric_plant.recirculating to cryoplant.electric_in;  // pb.p_cryo = cryoplant.p_elec; p_tfcool_in, p_pfcool_in
        connect electric_plant.recirculating to power_supplies.electric_in;   // pb.p_tf_in, p_pf_in
        connect electric_plant.recirculating to fuel_cycle.electric_in; // pb.p_trit_in
        connect magnet.cold_mass to cryoplant.heat_load_in;             // cryoplant.q_nuc_cryo <- magnet.winding_pack.q_nuc_cryo; vol_cold_total <- magnet.vol_cold_total
        connect blanket.tritium_out to fuel_cycle.tritium_in;           // fuel_cycle.tbr <- blanket.tbr (fuel.tbr_available_in)
        connect fuel_cycle.fuel_out to plasma.fuel_in;                  // fuel_cycle.p_fus <- plasma.p_fus (the burn the fuelling sustains)
        connect fuel_cycle.exhaust_out to vacuum_pumping.exhaust_in;    // vacuum_pumping.exhaust_rate, burn_rate <- fuel_cycle

        attribute preconstruction_capital : Real = precon_cost.cost;
        // CAS27 pass-through
        attribute special_materials_capital : Real;

        // =====================================================================
        // PHYSICS SPINE  (Plasma Geometry -> DT Fusion Power -> Power Balance)
        // =====================================================================




        // Forward radial build (WI-021): cumulative radii -> torus-shell volumes,
        // first-wall area, coil-bore radius. Replaces the injected material-volume
        // constants; shares the plant's R/a/kappa with geom.
        calc rb : 'MFE Radial Build' {
            in R_in = plasma.R;
            in a_in = plasma.a;
            in kappa_in = plasma.kappa;
            in vacuum_t_in = blanket.first_wall.vacuum_t;
            in firstwall_t_in = blanket.first_wall.firstwall_t;
            in blanket_t_in = blanket.blanket_t;
            in reflector_t_in = blanket.reflector_t;
            in ht_shield_t_in = shield.ht_shield_t;
            in structure_t_in = structure.structure_t;
            in gap1_t_in = vessel.gap1_t;
            in vessel_t_in = vessel.vessel_t;
            in coil_t_in = magnet.coil.coil_t;
            in gap2_t_in = magnet.gap2_t;
            in lt_shield_t_in = shield.lt_shield_t;
        }

















        // subsystem/control fraction
        attribute f_sub : Real;
        // housekeeping [MW]
        attribute p_house : Real;






        // Generic legacy/direct behavior defaults to installed coupled capacity.
        // A sustained concept overrides this exposed demand with its producer.
        // (WI-050; the heating facts live on the heating part since WI-057.)
        attribute p_operating_coupled_heat : Real default heating.p_coupled;
        calc operating_heat : 'Operating Heating Power' {
            in p_required_in = p_operating_coupled_heat;
            in eta_source_in = heating.eta_source_heat;
            in eta_couple_in = heating.eta_couple_heat;
        }
        assert constraint heating_source_positive_ok : 'Heating Efficiency Positive' {
            in efficiency = heating.eta_source_heat;
        }
        assert constraint heating_source_upper_ok : 'Heating Efficiency Upper' {
            in efficiency = heating.eta_source_heat;
        }
        assert constraint heating_couple_positive_ok : 'Heating Efficiency Positive' {
            in efficiency = heating.eta_couple_heat;
        }
        assert constraint heating_couple_upper_ok : 'Heating Efficiency Upper' {
            in efficiency = heating.eta_couple_heat;
        }

        calc pb : 'MFE Power Balance Calc' {
            in p_nrl = plasma.p_fus;
            in p_input_in = operating_heat.p_coupled;
            in mn_in = blanket.mn;
            in eta_th_in = turbine.eta_th;
            in q_recovered_in = heat_transport.q_recovered_total;
            in p_wallplug_in = operating_heat.p_wallplug;
            in p_pump_total_in = heat_transport.p_pump_total;
            in f_sub_in = f_sub;
            in p_tf_in = power_supplies.p_tf_total;
            in p_pf_in = power_supplies.p_pf;
            in p_tfcool_in = cryoplant.p_tfcool;
            in p_pfcool_in = cryoplant.p_pfcool;
            in p_trit_in = fuel_cycle.p_trit;
            in p_house_in = p_house;
            in p_cryo = cryoplant.p_elec;
        }

        // Cost-spine power aliases: read directly from the power balance so the
        // cost accounts scale with the forward-computed powers (WI-009 exposes
        // p_th/p_the/p_et as outputs). No external input -- keeps the forward pass.
        // total thermal power [MW]
        attribute p_th : Real = pb.p_th;
        // thermal-electric power [MW]
        attribute p_the : Real = pb.p_the;
        // gross electric power [MW]
        attribute p_et : Real = pb.p_et;

        // =====================================================================
        // ACCOUNT COST CALCS  (bind subsystem drivers + spine powers -> cost)
        // =====================================================================












        // Balance-of-plant (CAS23 turbine, CAS24 electric, CAS25 heat rej,
        // CAS26 misc) -- one 'Linear Power Cost' calc each.
        // module count; single-module demo
        attribute n_mod : Real default 1.0;


        // CAS10 fixed preconstruction adders [$] (WI-025; instance binds -- fuel/FOAK-keyed).
        attribute precon_fixed_base : Real;
        calc precon_cost : 'Preconstruction Cost' {
            in fixed_precon = precon_fixed_base;
            in p_net = pb.p_net;
        }

        // CAS70 annual O&M at reference power [$/yr] (WI-025; instance binds -- fuel-keyed).
        attribute om_annual_ref : Real;
        calc om_cost : 'Annual OM Cost' {
            in om_ref = om_annual_ref;
            in p_net = pb.p_net;
        }

        // =====================================================================
        // CAPITAL ROLLUP  (all $) -- 1cfe overnight assembly (WI-028 D2)
        //   cas2x -> contingency -> cas20 -> indirect -> cas30 -> overnight.
        //   CAS10 enters at overnight (NOT in cas2x); CAS40/CAS50 at overnight;
        //   CAS60 (idc) Option C: reported line, total_capital = overnight.
        // =====================================================================

        // Power-core capital (CAS22): divergent + shared sub-accounts.
        attribute powercore_capital : Real =
            magnet.capital_cost + heating.capital_cost + divertor.capital_cost
            + blanket.capital_cost + shield.capital_cost + structure.capital_cost
            + vessel.capital_cost + power_supplies.capital_cost;

        // Balance-of-plant capital (CAS23-26).
        attribute bop_capital : Real =
            turbine.capital_cost + electric_plant.capital_cost
            + heat_rejection.capital_cost + misc_plant.capital_cost;

        // Item 10: codegen now compiles this cross-part rollup as an aggregation
        // producer (child :>> capital_cost redefinitions resolve per instance),
        // so the staged twin carries the canonical formula -- byte-identical to
        // models/. The private bridge and harness rollup glue are retired.

        // ---- CAS22 tail accounts (WI-028 D1/D5; bases bound at instance) ----
        // C220110 remote handling (per-module p_et; concept-scaled).
        // rh_base[fuel] [$]
        attribute remote_handling_base : Real;
        // 1.0 toroidal / 0.55 end-access
        attribute concept_scale : Real;
        calc remote_handling : 'Remote Handling Cost' {
            in base = remote_handling_base;
            in concept_scale_in = concept_scale;
            in p_et_in = p_et;
        }
        // expose for producer aggregation
        attribute remote_handling_capital : Real = remote_handling.cost;
        // C220111 installation labor = frac * Sigma(C220101..C220110).
        // reactor_subtotal via an intermediate attribute (WI-025 rollup pattern:
        // calc inputs bind to a single attribute, not a mixed expression).
        // 0.14 (cas22.py:664)
        attribute installation_frac : Real;
        attribute reactor_equipment_subtotal : Real =
            powercore_capital + remote_handling_capital;
        calc installation : 'Installation Labor Cost' {
            in installation_frac_in = installation_frac;
            in reactor_subtotal = reactor_equipment_subtotal;
        }
        // C220300 aux cooling (plant-total p_th) + cryoplant (per-module p_cryo).
        // 1.10e-3 M$/MW -> $/MW
        attribute aux_per_mw : Real;
        // C220400 waste (a=1.0), C220500 fuel, C220600 other, C220700 I&C:
        // shared 'Plant Power-Law Cost'. Account-structural ref/alpha literal;
        // base bound at instance.
        // 1.96 M$ -> $
        attribute waste_base : Real;
        calc waste : 'Plant Power-Law Cost' {
            in base = waste_base; in power = p_th; in n_mod_in = n_mod;
            in ref_power = 1000.0; in alpha = 1.0;
        }
        // 11.5 M$ -> $
        attribute other_rpe_base : Real;
        calc other_rpe : 'Plant Power-Law Cost' {
            in base = other_rpe_base; in power = pb.p_net; in n_mod_in = n_mod;
            in ref_power = 1000.0; in alpha = 0.8;
        }
        // 85.0 M$ -> $  (I&C)
        attribute inc_base : Real;
        calc inc_cost : 'Plant Power-Law Cost' {
            in base = inc_base; in power = p_th; in n_mod_in = n_mod;
            in ref_power = 3500.0; in alpha = 0.65;
        }

        // Expose each tail calc cost as a sibling attribute so cas22_tail_capital
        // is a sum-of-siblings aggregation producer (not expose_computed).
        // remote_handling_capital is exposed above (installation subtotal).
        attribute installation_capital : Real = installation.cost;
        attribute coolant_capital : Real = heat_transport.coolant_cost;
        attribute aux_cooling_capital : Real = cryoplant.aux_cooling_cost;
        attribute waste_capital : Real = waste.cost;
        attribute fuel_handling_capital : Real = fuel_cycle.fuel_handling_cost;
        attribute other_rpe_capital : Real = other_rpe.cost;
        attribute inc_capital : Real = inc_cost.cost;
        // CAS22 tail folded directly into cas22_capital: powercore_capital
        // references parts (magnet.capital_cost ...), so cas22_capital compiles
        // instance-scoped and resolves the sibling tail exposures within its
        // aggregation (the intermediate cas22_tail_capital would compile at
        // part-def scope -- no part reference -- and dead-end the instance leaves).
        attribute cas22_capital : Real =
            powercore_capital + remote_handling_capital + installation_capital
            + coolant_capital + aux_cooling_capital + waste_capital
            + fuel_handling_capital + other_rpe_capital + inc_capital;

        // CAS28 digital twin -- fed design input (WI-028 F-2).
        // 5.0 M$ -> $
        attribute cas28_capital : Real;

        // ---- CAS20 series: cas2x -> contingency -> cas20 -> indirect -> cas30 ----
        // cas2x pre-contingency direct sum (1cfe cas2x; CAS10 NOT included).
        attribute cas2x_pre_contingency : Real =
            buildings.capital_cost + cas22_capital + bop_capital
            + special_materials_capital + cas28_capital;

        // Contingency (CAS29) on cas2x (WI-028: rebased off the CAS10-inclusive
        // direct sum -> cas2x, F-3).
        // FOAK 0.10 / NOAK 0.0 (WI-011)
        attribute contingency_rate : Real;
        calc contingency : 'Contingency Cost' {
            in contingency_rate_in = contingency_rate;
            in direct_subtotal = cas2x_pre_contingency;
        }
        attribute contingency_capital : Real = contingency.cost;
        // c20
        attribute cas20_capital : Real = cas2x_pre_contingency + contingency_capital;

        // Indirect (CAS30) on cas20 (post-contingency), construction-time scaled
        // (WI-028: rebased from the pre-contingency direct sum -> cas20, F-3).
        // 0.20 of cas20 (WI-011)
        attribute indirect_fraction : Real;
        // Yc [yr] (shared with LCOE + CAS30)
        attribute construction_years : Real;
        calc indirect : 'Indirect Cost' {
            in indirect_fraction_in = indirect_fraction;
            in direct_cost = cas20_capital;
            in construction_time = construction_years;
        }
        attribute cas30_capital : Real = indirect.cost;

        // c23..c28 subtotal -- CAS50 spares base (WI-028 F-1).
        attribute cas23_to_28_capital : Real =
            bop_capital + special_materials_capital + cas28_capital;

        // ---- CAS40 owner + CAS50 supplementary at overnight (no CAS29/CAS30) ----
        // owner_cost[fuel] [$]
        attribute owner_base : Real;
        calc owner : 'Plant Power-Law Cost' {
            in base = owner_base; in power = pb.p_net; in n_mod_in = n_mod;
            in ref_power = 1000.0; in alpha = 0.5;
        }
        // CAS40 (expose calc cost as sibling attr)
        attribute owner_capital : Real = owner.cost;
        // fuel-keyed
        attribute supplementary_spares_frac : Real;
        // fuel-keyed [$]
        attribute supplementary_startup_base : Real;
        // fuel-keyed [$]
        attribute supplementary_decom_base : Real;
        calc supplementary : 'Supplementary Cost' {
            in spares_frac = supplementary_spares_frac;
            in startup_fuel_base = supplementary_startup_base;
            in decom_base = supplementary_decom_base;
            in cas20 = cas20_capital;
            in cas23_to_28 = cas23_to_28_capital;
            in cas30 = indirect.cost;    // read the CAS30 producer directly (cas30_capital is expose_pure)
            in p_net = pb.p_net;
            in n_mod_in = n_mod;
        }
        // CAS50 (expose calc cost as sibling attr)
        attribute supplementary_capital : Real = supplementary.cost;

        // Overnight capital [$] -- CAS10 (preconstruction) enters HERE per 1cfe:
        // it receives neither CAS29 contingency nor CAS30 indirect. Aggregates
        // sibling attributes only (owner/supplementary costs exposed above) so
        // codegen emits it as an aggregation producer (not expose_computed).
        attribute overnight_capital : Real =
            preconstruction_capital + cas20_capital + cas30_capital
            + owner_capital + supplementary_capital;

        // ---- CAS60 IDC (Option C, owner-ruled 2026-07-20): reported line, ----
        // ---- EXCLUDED from total_capital; DCF idc_factor untouched.       ----
        calc idc : 'IDC Closed-Form Cost' {
            in interest_rate = discount_rate;
            in construction_years_in = construction_years;
            in overnight_cost = overnight_capital;
        }
        // CAS60 reported line (not in total_capital)
        attribute idc_capital : Real = idc.cost;

        // Item 10: restored to the canonical formula (see direct_capital note).
        // Total capital [$] -- Option C: equals overnight_capital (idc NOT summed
        // in). Written as the overnight aggregation of sibling attributes (not a
        // bare alias) so codegen emits a total_capital producer channel for the
        // untouched lcoe_calc input.
        attribute total_capital : Real =
            preconstruction_capital + cas20_capital + cas30_capital
            + owner_capital + supplementary_capital;

        // =====================================================================
        // ANNUAL-COST SIDE -- CAS71 / CAS72 / CAS80 (WI-029 D1/D2)
        //   CAS71 = levelized O&M; CAS72 = levelized scheduled replacement of
        //   the fluence-limited in-vessel accounts; CAS80 = levelized DT fuel.
        //   CAS70 = CAS71 + CAS72. One levelization wrapper serves CAS71 and
        //   CAS80 (MR-3, 'Levelized Annual Cost' used twice).
        // =====================================================================

        // Escalation rate g for the levelization (instance binds; 1cfe 0.02).
        attribute inflation_rate : Real;

        // CAS71 -- levelized annual O&M [$/yr]. Tc = construction_years (NOAK).
        calc cas71_calc : 'Levelized Annual Cost' {
            in annual_cost = om_cost.annual_om;
            in interest_rate = discount_rate;
            in inflation_rate_in = inflation_rate;
            in operational_years_in = operational_years;
            in project_time = construction_years;
        }
        // expose for producer aggregation
        attribute cas71_annual : Real = cas71_calc.levelized;


        calc cas80_calc : 'Levelized Annual Cost' {
            // Read the fuel producer directly. A bare `annual_fuel = fuel_calc.annual_fuel`
            // alias resolves at part-def scope and mints no instance params key
            // (the WI-028 bare-alias class); fuel_calc__annual_fuel is already a
            // channel, so the A-2 row reads it without the alias.
            in annual_cost = fuel_cycle.annual_fuel;
            in interest_rate = discount_rate;
            in inflation_rate_in = inflation_rate;
            in operational_years_in = operational_years;
            in project_time = construction_years;
        }
        // expose for producer aggregation
        attribute cas80_annual : Real = cas80_calc.levelized;




        // ---- CAS72 and availability from one lifecycle calendar (WI-046) -----
        // Replaceable set = the fluence-limited in-vessel accounts C220101
        // (blanket/first wall) + C220108 (divertor), plant-total (x n_mod), one
        // bundled event. Source: defaults.py:299 (replaceable_accounts), pin 0254385.
        attribute replacement_cost_per_event : Real =
            (blanket.capital_cost + divertor.capital_cost) * n_mod;

        // scheduled outage per bundled replacement [yr] (instance binds)
        attribute outage_years : Real;
        // residual unplanned fraction of scheduled-online time [1] (instance binds)
        attribute unplanned_fraction : Real;
        // held-mode switch: 0 = the live calendar; (0, 1] = the retired periodic
        // chain at that availability (the compatibility bridge; instance binds)
        attribute availability_direct : Real;

        // The lifetime operand is the PEAK wall load (WI-041); the calendar is
        // the one producer of availability and CAS72 (WI-046).
        calc calendar : 'Lifecycle Calendar' {
            in q_n_in = blanket.wall_load_peak;
            in fluence_limit_in = blanket.first_wall.fluence_limit;
            in operational_years_in = operational_years;
            in outage_years_in = outage_years;
            in unplanned_fraction_in = unplanned_fraction;
            in cost_per_event = replacement_cost_per_event;
            in interest_rate = discount_rate;
            in coil_life_fpy_in = magnet.coil.coil_life_fpy;
            in availability_direct_in = availability_direct;
        }
        // expose_pure channel for A-2
        attribute cas72_annual : Real = calendar.cas72_annual;

        calc cas70_calc : 'Annual Cost Rollup' {
            in cas71 = cas71_calc.levelized;
            in cas72 = calendar.cas72_annual;
            in cas80 = cas80_calc.levelized;
        }
        // expose_pure channel for A-2
        attribute cas70_annual : Real = cas70_calc.cas70;

        // =====================================================================
        // LCOE  (WI-009 'LCOE DCF' core)
        // =====================================================================

        // WI-029: the DCF headline now takes the LEVELIZED annual-cost side --
        // CAS70 (= CAS71 levelized O&M + CAS72 levelized replacement) + CAS80
        // levelized fuel -- replacing the unlevelized WI-025 O&M line that used
        // to be bound here. The headline CONVENTION is unchanged (Option ii:
        // idc_factor and total_capital = overnight_capital both untouched);
        // only the annual-cost numerator becomes complete.
        // CAS70+CAS80 levelized [$/yr]
        attribute annual_om : Real = cas70_calc.annual_total;
        // capacity factor [0..1] -- the calendar's output, bound by reference
        // (WI-046; the WI-044 m_casing pattern): one producer, every consumer
        // (fuel_calc, lcoe_calc, lcoe_1cfe_calc) reads it unchanged.
        attribute availability : Real = calendar.availability;
        // discount / interest rate [1/yr]
        attribute discount_rate : Real;
        // operating lifetime N [yr]
        attribute operational_years : Real;

        calc lcoe_calc : 'LCOE DCF' {
            in total_capital_in = total_capital;
            in annual_om_in = annual_om;
            in net_electric_mw = pb.p_net;
            in availability_in = availability;
            in discount_rate_in = discount_rate;
            in construction_years_in = construction_years;
            in operational_years_in = operational_years;
        }

        // ---- 1cfe-form CAS90 / LCOE COMPARISON channels (WI-029, Option ii) --
        // Owner ruling 2026-07-25: the DCF headline above stays untouched; these
        // two channels restate the same plant in 1costingFE's financing form so
        // the end-to-end LCOE can be compared account-for-account under A-2.
        //   cas90_1cfe = CRF * (overnight_capital + CAS60)
        //   lcoe_1cfe  = (cas90_1cfe + CAS70 + CAS80) / annual energy
        // CAS60 is the Item-3 'IDC Closed-Form Cost' REPORTED line (idc_capital)
        // -- no new IDC arithmetic -- and CRF is reused from cas71_calc, which
        // computes it from the same discount_rate / operational_years the DCF
        // core uses. total_capital stays == overnight_capital (Option C), so
        // CAS60 cannot enter the headline capital base: the two channels coexist
        // without double-counting. Comparison only -- NOT the design-point headline.
        // Source: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
        // Ref: costs.py:547-556 (cas90 = CRF*total_capital); economics.py:88-92 (lcoe)
        calc cas90_1cfe_calc : '1cfe-Form Capital Charge' {
            in crf = cas71_calc.crf;
            in overnight_cost = overnight_capital;
            in idc_cost = idc.cost;
        }
        // expose_pure channel for A-2
        attribute cas90_1cfe : Real = cas90_1cfe_calc.cas90;

        calc lcoe_1cfe_calc : '1cfe-Form LCOE' {
            in cas90 = cas90_1cfe_calc.cas90;
            in cas70 = cas70_calc.cas70;
            in cas80 = cas80_calc.levelized;
            in net_electric_mw = pb.p_net;
            in n_mod_in = n_mod;
            in availability_in = availability;
        }
        // expose_pure channel for A-2
        attribute lcoe_1cfe : Real = lcoe_1cfe_calc.lcoe;

        // =====================================================================
        // VIABILITY CONSTRAINTS  (WI-009 mfe_viability)
        // =====================================================================

        assert constraint net_positive : 'Net Power Positive' {
            in net_electric = pb.p_net;
        }

        assert constraint recirc_ok : 'Economic Recirculating Threshold' {
            in rec_frac = pb.rec_frac;
        }

        // Conductor peak-field limit (WI-030): every MFE instance states its
        // coil set's peak/axis ratio and its conductor ceiling on the magnet.
        assert constraint peak_field_ok : 'Conductor Peak Field Limit' {
            in B_peak = magnet.B_peak;
            in B_max_in = magnet.winding_pack.B_max;
        }

        // WI-035: computed stress operand vs held sourced allowable (800 MPa).
        assert constraint wp_stress_ok : 'Winding Pack Stress Limit' {
            in sigma_in = magnet.sigma_wp;
            in sigma_allow_in = magnet.casing.sigma_allow;
        }

        // WI-036: the conductor's own check, distinct from the structure's.
        // The structural operand above is a PEAK stress quantity (its k_sigma
        // is anchored to the source's printed "Peak stress on WP" row), and
        // the ITER criteria carry 666 MPa primary membrane against 1.0-1.333
        // GPa peak; sigma_allow stays at the source's own 800 MPa design limit
        // and is not re-categorised to open feasibility (WI-036 MR-6).
        assert constraint cond_strain_ok : 'Conductor Strain Limit' {
            in eps_cond = magnet.eps_cond;
            in eps_cond_allow_in = magnet.winding_pack.eps_cond_allow;
        }

        // WI-045: the loop's two domain/capacity fences and the cycle's domain fence.
        assert constraint loop_pressure_ok : 'Loop Pressure Margin' {
            in p_loop_margin_in = heat_transport.p_loop_margin;
        }
        assert constraint loop_capacity_ok : 'Loop Capacity' {
            in mdot_loop_in = heat_transport.mdot_loop;
            in mdot_loop_rated_in = heat_transport.mdot_loop_ref;
        }
        assert constraint cycle_domain_ok : 'Cycle Fit Domain' {
            in domain_product_in = turbine.domain_product;
        }

        // WI-047: the divertor target peak (fixed-geometry source case, scaled in
        // load) against the adopted threshold. EXPECTED VIOLATED at the Stellaris
        // baseline on the pessimistic case (10.535 against 10: the model's absorbed
        // heating 554.49 MW is 10.9 % above the source's 500) -- the disclosed,
        // explained verdict change of WI-047, never tuned (the WI-041 precedent).
        assert constraint divertor_heat_ok : 'Divertor Target Heat Limit' {
            in q_target_peak_in = divertor.q_target_peak;
            in q_target_limit_in = divertor.q_target_limit;
        }

        // =====================================================================
        // EXPOSED DERIVED OUTPUTS
        // =====================================================================

        // Headline results.
        attribute net_electric : Real = pb.p_net;
        attribute q_eng : Real = pb.q_eng;
        attribute rec_frac : Real = pb.rec_frac;
        attribute lcoe : Real = lcoe_calc.lcoe;

        // Per-account CAS breakdown (reads each subsystem's capital_cost, $).
        attribute magnet_capital : Real = magnet.capital_cost;
        // WI-035: 1cfe-form comparison channel + the cryoplant sub-account.
        attribute magnet_capital_1cfe : Real = magnet.capital_cost_1cfe;
        attribute cryoplant_capital : Real = cryoplant.cryo_cost;
        attribute heating_capital : Real = heating.capital_cost;
        attribute divertor_capital : Real = divertor.capital_cost;
        attribute blanket_capital : Real = blanket.capital_cost;
        attribute shield_capital : Real = shield.capital_cost;
        attribute structure_capital : Real = structure.capital_cost;
        attribute vessel_capital : Real = vessel.capital_cost;
        attribute power_supplies_capital : Real = power_supplies.capital_cost;
        attribute turbine_capital : Real = turbine.capital_cost;
        attribute electric_capital : Real = electric_plant.capital_cost;
        attribute heat_rejection_capital : Real = heat_rejection.capital_cost;
        attribute misc_capital : Real = misc_plant.capital_cost;
        attribute buildings_capital : Real = buildings.capital_cost;
    }
}
