package mfe_plant {
    private import ScalarValues::*;
    private import mfe_power_core::*;
    private import mfe_subsystems::*;
    private import mfe_plasma_scaling::*;
    private import mfe_power_balance::*;
    private import mfe_cryo_plant::*;
    private import mfe_magnet_cost::*;
    private import mfe_account_costs::*;
    private import mfe_lcoe_dcf::*;
    private import mfe_viability::*;

    abstract part def 'MFE Power Plant' {
        doc /*
        Confinement-agnostic magnetic-fusion power plant. Composes the WI-009
        power-core subsystems and the shared/BOP costed components, wires the
        physics -> cost -> LCOE calc pipeline, and asserts the two viability
        constraints. The MFE analogue of ife_plant's 'IFE Power Plant', one
        level richer (a full physics spine and a bottom-up CAS rollup).

        Abstract: WI-011 specializes it with concept-09 (stellarator) values and
        the family density closure. All parameters here are inputs or defaulted
        calibration constants — no concept-specific values (MR-3).

        MONEY UNIT: the whole rollup and LCOE are in DOLLARS ($). WI-009's
        'Magnet Coil Cost' omits the 1costingFE /1e6 M$ conversion, so it yields
        $; to stay consistent, every account unit-cost input (blanket unit cost,
        per-MW BOP rates, power-supply/divertor bases, pass-through capitals) and
        annual O&M must be supplied in $ by WI-011 (1costingFE constants are M$;
        multiply by 1e6). total_capital [$], annual_om [$/yr] -> lcoe [$/MWh].

        PHYSICS-SPINE / COST-SPINE: WI-009's 'MFE Power Balance Calc' exposes
        p_th, p_the, p_et as outputs (alongside p_net, q_eng, rec_frac), so the
        volume/power-scaled account costs read the forward-computed powers
        directly via `pb.p_th` etc. — the full forward pass (geometry -> fusion
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
        part magnet : 'Magnet System' {
            :>> capital_cost = magnet_cost.capital_cost;
            :>> r_coil = rb.r_coil;   // coil bore = radial-build vessel_or (WI-021)
        }
        part heating : 'Heating and CD' {
            :>> capital_cost = heating_cost.cost;
        }
        part divertor : 'Divertor' {
            :>> capital_cost = divertor_cost.cost;
        }

        // Shared power core (mfe_subsystems). Material volumes forward-computed
        // from the radial build (WI-021), replacing the injected constants.
        part blanket : 'Blanket' {
            :>> capital_cost = blanket_cost.cost;
            :>> blanket_vol = rb.blanket_vol;
        }
        part shield : 'Shield' {
            :>> capital_cost = shield_cost.cost;
            :>> shield_vol = rb.shield_vol;
        }
        part structure : 'Primary Structure' {
            :>> capital_cost = structure_cost.cost;
            :>> structure_vol = rb.structure_vol;
        }
        part vessel : 'Vacuum Vessel' {
            :>> capital_cost = vessel_cost.cost;
            :>> vessel_vol = rb.vessel_vol;
        }
        part power_supplies : 'Power Supplies' {
            :>> capital_cost = power_supplies_cost.cost;
        }

        // Balance of plant (mfe_subsystems).
        part turbine : 'Turbine Plant' {
            :>> capital_cost = turbine_cost.cost;
        }
        part electric_plant : 'Electric Plant' {
            :>> capital_cost = electric_cost.cost;
        }
        part heat_rejection : 'Heat Rejection' {
            :>> capital_cost = heat_rejection_cost.cost;
        }
        part misc_plant : 'Miscellaneous Plant' {
            :>> capital_cost = misc_cost.cost;
        }

        // Forward-computed direct accounts (WI-025): CAS21 via buildings_cost,
        // CAS10 via precon_cost; CAS27 remains a pass-through (WI-011, in $).
        part buildings : 'Buildings' {
            :>> capital_cost = buildings_cost.cost;
        }
        attribute preconstruction_capital : Real = precon_cost.cost;
        attribute special_materials_capital : Real;    // CAS27 pass-through

        // =====================================================================
        // PHYSICS SPINE  (Plasma Geometry -> DT Fusion Power -> Power Balance)
        // =====================================================================

        // Plasma geometry inputs (WI-011).
        attribute R : Real;       // major radius [m]
        attribute a : Real;       // minor radius [m]
        attribute kappa : Real;   // elongation
        // Shape/packing factor (WI-020). Default 1.0 = pure elongated torus
        // (tokamak); a shaped stellarator instance overrides it.
        attribute f_shape : Real default 1.0;

        calc geom : 'Plasma Geometry' {
            in R = R;
            in a = a;
            in kappa = kappa;
            in f_shape = f_shape;
        }

        // Radial-build layer thicknesses [m] (WI-021). Generic-plant machinery:
        // the radial-build pattern is shared; concept instances override values.
        // Defaults are the 1costingFE RadialBuild defaults (geometry.py:19-40).
        attribute vacuum_t : Real default 0.10;
        attribute firstwall_t : Real default 0.05;
        attribute blanket_t : Real default 0.70;
        attribute reflector_t : Real default 0.20;
        attribute ht_shield_t : Real default 0.20;
        attribute structure_t : Real default 0.15;
        attribute gap1_t : Real default 0.10;
        attribute vessel_t : Real default 0.10;
        attribute coil_t : Real default 0.30;
        attribute gap2_t : Real default 0.10;
        attribute lt_shield_t : Real default 0.15;

        // Forward radial build (WI-021): cumulative radii -> torus-shell volumes,
        // first-wall area, coil-bore radius. Replaces the injected material-volume
        // constants; shares the plant's R/a/kappa with geom.
        calc rb : 'MFE Radial Build' {
            in R = R;
            in a = a;
            in kappa = kappa;
            in vacuum_t = vacuum_t;
            in firstwall_t = firstwall_t;
            in blanket_t = blanket_t;
            in reflector_t = reflector_t;
            in ht_shield_t = ht_shield_t;
            in structure_t = structure_t;
            in gap1_t = gap1_t;
            in vessel_t = vessel_t;
            in coil_t = coil_t;
            in gap2_t = gap2_t;
            in lt_shield_t = lt_shield_t;
        }

        // Fusion-power inputs (WI-011 sets density directly for the stellarator;
        // no density closure here). WI-022: sigma_v > 0 selects the exact 0D
        // bypass; sigma_v = 0 (default) computes the profile integral from the
        // five profile inputs below (defaults mirror the calc def — a 0D/flat
        // concept binds sigma_v only and leaves the profile inputs dormant).
        attribute n_e : Real;                    // electron density [m^-3]
        attribute sigma_v : Real default 0.0;    // 0D-effective reactivity [m^3/s]; > 0 = bypass
        attribute E_fus : Real;                  // per-event D-T fusion energy [J]
        attribute n_D0 : Real default 0.0;       // peak deuterium density [m^-3]
        attribute n_T0 : Real default 0.0;       // peak tritium density [m^-3]
        attribute T_i0 : Real default 1.0;       // peak ion temperature [keV]
        attribute alpha_n : Real default 0.0;    // density profile exponent
        attribute alpha_T : Real default 0.0;    // temperature profile exponent

        calc fusion : 'DT Fusion Power' {
            in n_e = n_e;
            in sigma_v = sigma_v;
            in E_fus = E_fus;
            in V = geom.V;
            in n_D0 = n_D0;
            in n_T0 = n_T0;
            in T_i0 = T_i0;
            in alpha_n = alpha_n;
            in alpha_T = alpha_T;
        }

        // Power-balance inputs (WI-011).
        attribute p_input : Real;   // plasma heating power [MW]
        attribute mn : Real;        // neutron energy multiplier
        attribute eta_th : Real;    // thermal-to-electric efficiency
        attribute eta_p : Real;     // pumping-power capture efficiency
        attribute eta_pin : Real;   // input-power wall-plug efficiency
        attribute p_pump : Real;    // primary coolant pumping power [MW]
        attribute f_sub : Real;     // subsystem/control fraction
        attribute p_tf : Real;      // TF coil power [MW]
        attribute p_pf : Real;      // PF coil power [MW]
        attribute p_tfcool : Real;  // TF coil cooling [MW]
        attribute p_pfcool : Real;  // PF coil cooling [MW]
        attribute p_trit : Real;    // tritium systems [MW]
        attribute p_house : Real;   // housekeeping [MW]
        attribute p_cryo : Real default 0.0;  // directly-specified cryoplant electrical [MW] (additive direct term, WI-024)

        // Cryoplant heat-load chain (WI-024). Dormant by default: a concept that
        // knows its cryo electrical directly binds p_cryo (the direct term) and
        // leaves these unbound; a concept deriving it binds the chain and zeroes
        // p_cryo.
        attribute q_nuc_cryo : Real default 0.0;
        attribute vol_cold_cryo : Real default 0.0;
        attribute p_fixed_cryo : Real default 0.0;
        attribute f_uplift_cryo : Real default 1.0;
        attribute T_cold_cryo : Real default 20.0;
        attribute T_amb_cryo : Real default 300.0;
        attribute f_carnot_cryo : Real default 1.0;

        calc cryo_elec : 'Cryoplant Electrical Power' {
            in q_nuc = q_nuc_cryo;
            in vol_cold = vol_cold_cryo;
            in p_fixed = p_fixed_cryo;
            in f_uplift = f_uplift_cryo;
            in T_cold = T_cold_cryo;
            in T_amb = T_amb_cryo;
            in f_carnot = f_carnot_cryo;
            in p_direct = p_cryo;
        }

        calc pb : 'MFE Power Balance Calc' {
            in p_nrl = fusion.p_fus;
            in p_input = p_input;
            in mn = mn;
            in eta_th = eta_th;
            in eta_p = eta_p;
            in eta_pin = eta_pin;
            in p_pump = p_pump;
            in f_sub = f_sub;
            in p_tf = p_tf;
            in p_pf = p_pf;
            in p_tfcool = p_tfcool;
            in p_pfcool = p_pfcool;
            in p_trit = p_trit;
            in p_house = p_house;
            in p_cryo = cryo_elec.p_elec;
        }

        // Cost-spine power aliases: read directly from the power balance so the
        // cost accounts scale with the forward-computed powers (WI-009 exposes
        // p_th/p_the/p_et as outputs). No external input — keeps the forward pass.
        attribute p_th : Real = pb.p_th;    // total thermal power [MW]
        attribute p_the : Real = pb.p_the;  // thermal-electric power [MW]
        attribute p_et : Real = pb.p_et;    // gross electric power [MW]

        // =====================================================================
        // ACCOUNT COST CALCS  (bind subsystem drivers + spine powers -> cost)
        // =====================================================================

        // Magnet (CAS22.1.3) — WI-009 'Magnet Coil Cost'.
        calc magnet_cost : 'Magnet Coil Cost' {
            in G = magnet.G;
            in B = magnet.B;
            in R0 = magnet.R0;
            in r_coil = rb.r_coil;
            in cost_per_kAm = magnet.cost_per_kAm;
            in coil_markup = magnet.coil_markup;
        }

        // Blanket (CAS22.1.1).
        calc blanket_cost : 'Blanket Cost' {
            in unit_cost = blanket.unit_cost;
            in structure_factor = blanket.structure_factor;
            in blanket_vol = rb.blanket_vol;
            in p_th = p_th;
        }

        // Shield (CAS22.1.2).
        calc shield_cost : 'Shield Cost' {
            in unit_cost = shield.unit_cost;
            in shield_vol = rb.shield_vol;
            in shield_scale = shield.shield_scale;
            in p_th = p_th;
        }

        // Primary structure (CAS22.1.5).
        calc structure_cost : 'Structure Cost' {
            in unit_cost = structure.unit_cost;
            in structure_vol = rb.structure_vol;
            in p_et = p_et;
        }

        // Vacuum vessel (CAS22.1.6, shell term).
        calc vessel_cost : 'Vessel Cost' {
            in unit_cost = vessel.unit_cost;
            in vessel_vol = rb.vessel_vol;
            in p_et = p_et;
        }

        // Power supplies (CAS22.1.7).
        calc power_supplies_cost : 'Power Supplies Cost' {
            in base = power_supplies.base;
            in p_et = p_et;
        }

        // Divertor (CAS22.1.8) — WI-009 carrier has no drivers; supplied here.
        attribute divertor_base : Real;   // divertor cost at 1 GWth [$] (WI-011)
        calc divertor_cost : 'Divertor Cost' {
            in base = divertor_base;
            in p_th = p_th;
        }

        // Heating & CD (CAS22.1.4) — WI-009 carrier has no drivers; the heating
        // mix (per-MW rates + delivered powers) is supplied here (WI-011).
        attribute heating_nbi_per_mw : Real;
        attribute p_nbi : Real;
        attribute heating_icrf_per_mw : Real;
        attribute p_icrf : Real;
        attribute heating_ecrh_per_mw : Real;
        attribute p_ecrh : Real;
        attribute heating_lhcd_per_mw : Real;
        attribute p_lhcd : Real;
        calc heating_cost : 'Heating Cost' {
            in nbi_per_mw = heating_nbi_per_mw;
            in p_nbi = p_nbi;
            in icrf_per_mw = heating_icrf_per_mw;
            in p_icrf = p_icrf;
            in ecrh_per_mw = heating_ecrh_per_mw;
            in p_ecrh = p_ecrh;
            in lhcd_per_mw = heating_lhcd_per_mw;
            in p_lhcd = p_lhcd;
        }

        // Balance-of-plant (CAS23 turbine, CAS24 electric, CAS25 heat rej,
        // CAS26 misc) — one 'Linear Power Cost' calc each.
        attribute n_mod : Real default 1.0;  // module count; single-module demo
        calc turbine_cost : 'Linear Power Cost' {
            in power = p_the;
            in cost_per_mw = turbine.cost_per_mw;
            in n_mod = n_mod;
        }
        calc electric_cost : 'Linear Power Cost' {
            in power = p_et;
            in cost_per_mw = electric_plant.cost_per_mw;
            in n_mod = n_mod;
        }
        calc heat_rejection_cost : 'Linear Power Cost' {
            in power = p_th;
            in cost_per_mw = heat_rejection.cost_per_mw;
            in n_mod = n_mod;
        }
        calc misc_cost : 'Linear Power Cost' {
            in power = p_et;
            in cost_per_mw = misc_plant.cost_per_mw;
            in n_mod = n_mod;
        }

        // CAS21 grouped base-cost sums [$] (WI-025 D1; instance binds — fuel-keyed).
        attribute bldg_fixed_base : Real;
        attribute bldg_fus_base : Real;
        attribute bldg_staff_base : Real;
        attribute bldg_the_base : Real;
        attribute bldg_th_base : Real;
        attribute bldg_et_base : Real;
        calc buildings_cost : 'Buildings Cost' {
            in fixed_base = bldg_fixed_base;
            in fus_base = bldg_fus_base;
            in staff_base = bldg_staff_base;
            in the_base = bldg_the_base;
            in th_base = bldg_th_base;
            in et_base = bldg_et_base;
            in p_fus = fusion.p_fus;
            in p_the = p_the;
            in p_th = p_th;
            in p_et = p_et;
        }

        // CAS10 fixed preconstruction adders [$] (WI-025; instance binds — fuel/FOAK-keyed).
        attribute precon_fixed_base : Real;
        calc precon_cost : 'Preconstruction Cost' {
            in fixed_precon = precon_fixed_base;
            in p_net = pb.p_net;
        }

        // CAS70 annual O&M at reference power [$/yr] (WI-025; instance binds — fuel-keyed).
        attribute om_annual_ref : Real;
        calc om_cost : 'Annual OM Cost' {
            in om_ref = om_annual_ref;
            in p_net = pb.p_net;
        }

        // =====================================================================
        // CAPITAL ROLLUP  (all $) — 1cfe overnight assembly (WI-028 D2)
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

        // ---- CAS22 tail accounts (WI-028 D1/D5; bases bound at instance) ----
        // C220110 remote handling (per-module p_et; concept-scaled).
        attribute remote_handling_base : Real;   // rh_base[fuel] [$]
        attribute concept_scale : Real;          // 1.0 toroidal / 0.55 end-access
        calc remote_handling : 'Remote Handling Cost' {
            in base = remote_handling_base;
            in concept_scale = concept_scale;
            in p_et = p_et;
        }
        attribute remote_handling_capital : Real = remote_handling.cost;  // expose for producer aggregation
        // C220111 installation labor = frac * Sigma(C220101..C220110).
        // reactor_subtotal via an intermediate attribute (WI-025 rollup pattern:
        // calc inputs bind to a single attribute, not a mixed expression).
        attribute installation_frac : Real;      // 0.14 (cas22.py:664)
        attribute reactor_equipment_subtotal : Real =
            powercore_capital + remote_handling_capital;
        calc installation : 'Installation Labor Cost' {
            in installation_frac = installation_frac;
            in reactor_subtotal = reactor_equipment_subtotal;
        }
        // C220200 coolant (two-term, plant-total).
        attribute coolant_primary_base : Real;       // 166.0 M$ -> $
        attribute coolant_intermediate_base : Real;  // 40.6 M$ -> $
        calc coolant : 'Coolant Cost' {
            in primary_base = coolant_primary_base;
            in p_net = pb.p_net;
            in intermediate_base = coolant_intermediate_base;
            in p_th = p_th;
            in n_mod = n_mod;
        }
        // C220300 aux cooling (plant-total p_th) + cryoplant (per-module p_cryo).
        attribute aux_per_mw : Real;             // 1.10e-3 M$/MW -> $/MW
        attribute aux_cryo_base : Real;          // 200.0 M$ -> $
        calc aux_cooling : 'Aux Cooling Cost' {
            in aux_per_mw = aux_per_mw;
            in p_th = p_th;
            in cryo_base = aux_cryo_base;
            in p_cryo = cryo_elec.p_elec;
            in n_mod = n_mod;
        }
        // C220400 waste (a=1.0), C220500 fuel, C220600 other, C220700 I&C:
        // shared 'Plant Power-Law Cost'. Account-structural ref/alpha literal;
        // base bound at instance.
        attribute waste_base : Real;             // 1.96 M$ -> $
        calc waste : 'Plant Power-Law Cost' {
            in base = waste_base; in power = p_th; in n_mod = n_mod;
            in ref_power = 1000.0; in alpha = 1.0;
        }
        attribute fuel_handling_base : Real;     // fh_base[fuel] [$]
        calc fuel_handling : 'Plant Power-Law Cost' {
            in base = fuel_handling_base; in power = pb.p_net; in n_mod = n_mod;
            in ref_power = 1000.0; in alpha = 0.7;
        }
        attribute other_rpe_base : Real;         // 11.5 M$ -> $
        calc other_rpe : 'Plant Power-Law Cost' {
            in base = other_rpe_base; in power = pb.p_net; in n_mod = n_mod;
            in ref_power = 1000.0; in alpha = 0.8;
        }
        attribute inc_base : Real;               // 85.0 M$ -> $  (I&C)
        calc inc_cost : 'Plant Power-Law Cost' {
            in base = inc_base; in power = p_th; in n_mod = n_mod;
            in ref_power = 3500.0; in alpha = 0.65;
        }

        // Expose each tail calc cost as a sibling attribute so cas22_tail_capital
        // is a sum-of-siblings aggregation producer (not expose_computed).
        // remote_handling_capital is exposed above (installation subtotal).
        attribute installation_capital : Real = installation.cost;
        attribute coolant_capital : Real = coolant.cost;
        attribute aux_cooling_capital : Real = aux_cooling.cost;
        attribute waste_capital : Real = waste.cost;
        attribute fuel_handling_capital : Real = fuel_handling.cost;
        attribute other_rpe_capital : Real = other_rpe.cost;
        attribute inc_capital : Real = inc_cost.cost;
        // CAS22 tail folded directly into cas22_capital: powercore_capital
        // references parts (magnet.capital_cost ...), so cas22_capital compiles
        // instance-scoped and resolves the sibling tail exposures within its
        // aggregation (the intermediate cas22_tail_capital would compile at
        // part-def scope — no part reference — and dead-end the instance leaves).
        attribute cas22_capital : Real =
            powercore_capital + remote_handling_capital + installation_capital
            + coolant_capital + aux_cooling_capital + waste_capital
            + fuel_handling_capital + other_rpe_capital + inc_capital;

        // CAS28 digital twin — fed design input (WI-028 F-2).
        attribute cas28_capital : Real;          // 5.0 M$ -> $

        // ---- CAS20 series: cas2x -> contingency -> cas20 -> indirect -> cas30 ----
        // cas2x pre-contingency direct sum (1cfe cas2x; CAS10 NOT included).
        attribute cas2x_pre_contingency : Real =
            buildings.capital_cost + cas22_capital + bop_capital
            + special_materials_capital + cas28_capital;

        // Contingency (CAS29) on cas2x (WI-028: rebased off the CAS10-inclusive
        // direct sum -> cas2x, F-3).
        attribute contingency_rate : Real;  // FOAK 0.10 / NOAK 0.0 (WI-011)
        calc contingency : 'Contingency Cost' {
            in contingency_rate = contingency_rate;
            in direct_subtotal = cas2x_pre_contingency;
        }
        attribute contingency_capital : Real = contingency.cost;
        attribute cas20_capital : Real = cas2x_pre_contingency + contingency_capital;  // c20

        // Indirect (CAS30) on cas20 (post-contingency), construction-time scaled
        // (WI-028: rebased from the pre-contingency direct sum -> cas20, F-3).
        attribute indirect_fraction : Real;   // 0.20 of cas20 (WI-011)
        attribute construction_years : Real;  // Yc [yr] (shared with LCOE + CAS30)
        calc indirect : 'Indirect Cost' {
            in indirect_fraction = indirect_fraction;
            in direct_cost = cas20_capital;
            in construction_time = construction_years;
        }
        attribute cas30_capital : Real = indirect.cost;

        // c23..c28 subtotal — CAS50 spares base (WI-028 F-1).
        attribute cas23_to_28_capital : Real =
            bop_capital + special_materials_capital + cas28_capital;

        // ---- CAS40 owner + CAS50 supplementary at overnight (no CAS29/CAS30) ----
        attribute owner_base : Real;             // owner_cost[fuel] [$]
        calc owner : 'Plant Power-Law Cost' {
            in base = owner_base; in power = pb.p_net; in n_mod = n_mod;
            in ref_power = 1000.0; in alpha = 0.5;
        }
        attribute owner_capital : Real = owner.cost;   // CAS40 (expose calc cost as sibling attr)
        attribute supplementary_spares_frac : Real;    // fuel-keyed
        attribute supplementary_startup_base : Real;   // fuel-keyed [$]
        attribute supplementary_decom_base : Real;     // fuel-keyed [$]
        calc supplementary : 'Supplementary Cost' {
            in spares_frac = supplementary_spares_frac;
            in startup_fuel_base = supplementary_startup_base;
            in decom_base = supplementary_decom_base;
            in cas20 = cas20_capital;
            in cas23_to_28 = cas23_to_28_capital;
            in cas30 = indirect.cost;    // read the CAS30 producer directly (cas30_capital is expose_pure)
            in p_net = pb.p_net;
            in n_mod = n_mod;
        }
        attribute supplementary_capital : Real = supplementary.cost;   // CAS50 (expose calc cost as sibling attr)

        // Overnight capital [$] — CAS10 (preconstruction) enters HERE per 1cfe:
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
            in construction_years = construction_years;
            in overnight_cost = overnight_capital;
        }
        attribute idc_capital : Real = idc.cost;   // CAS60 reported line (not in total_capital)

        // Total capital [$] — Option C: equals overnight_capital (idc NOT summed
        // in). Written as the overnight aggregation of sibling attributes (not a
        // bare alias) so codegen emits a total_capital producer channel for the
        // untouched lcoe_calc input.
        attribute total_capital : Real =
            preconstruction_capital + cas20_capital + cas30_capital
            + owner_capital + supplementary_capital;

        // =====================================================================
        // ANNUAL-COST SIDE — CAS71 / CAS72 / CAS80 (WI-029 D1/D2)
        //   CAS71 = levelized O&M; CAS72 = levelized scheduled replacement of
        //   the fluence-limited in-vessel accounts; CAS80 = levelized DT fuel.
        //   CAS70 = CAS71 + CAS72. One levelization wrapper serves CAS71 and
        //   CAS80 (MR-3, 'Levelized Annual Cost' used twice).
        // =====================================================================

        // Escalation rate g for the levelization (instance binds; 1cfe 0.02).
        attribute inflation_rate : Real;

        // CAS71 — levelized annual O&M [$/yr]. Tc = construction_years (NOAK).
        calc cas71_calc : 'Levelized Annual Cost' {
            in annual_cost = om_cost.annual_om;
            in interest_rate = discount_rate;
            in inflation_rate = inflation_rate;
            in operational_years = operational_years;
            in project_time = construction_years;
        }
        attribute cas71_annual : Real = cas71_calc.levelized;   // expose for producer aggregation

        // ---- CAS80 DT fuel: raw annual, then the same levelization wrapper ----
        // Fuel chemistry constants are instance inputs (MR-3) — no library defaults.
        attribute fuel_cost_per_rxn : Real;   // M_D*u_D + M_Li6*u_Li6 [$/rxn]
        attribute fuel_q_eff : Real;          // per-reaction energy [MeV]
        attribute mev_to_joules : Real;       // MeV -> J
        attribute burn_fraction : Real;
        attribute fuel_recovery : Real;

        calc fuel_calc : 'DT Fuel Cost' {
            in p_fus = fusion.p_fus;
            in n_mod = n_mod;
            in availability = availability;
            in cost_per_rxn = fuel_cost_per_rxn;
            in q_eff = fuel_q_eff;
            in mev_to_joules = mev_to_joules;
            in burn_fraction = burn_fraction;
            in fuel_recovery = fuel_recovery;
        }
        calc cas80_calc : 'Levelized Annual Cost' {
            // Read the fuel producer directly. A bare `annual_fuel = fuel_calc.annual_fuel`
            // alias resolves at part-def scope and mints no instance params key
            // (the WI-028 bare-alias class); fuel_calc__annual_fuel is already a
            // channel, so the A-2 row reads it without the alias.
            in annual_cost = fuel_calc.annual_fuel;
            in interest_rate = discount_rate;
            in inflation_rate = inflation_rate;
            in operational_years = operational_years;
            in project_time = construction_years;
        }
        attribute cas80_annual : Real = cas80_calc.levelized;   // expose for producer aggregation

        // ---- CAS72 scheduled replacement (Rung B, handwritten impl) ----------
        // Replaceable set = the fluence-limited in-vessel accounts C220101
        // (blanket/first wall) + C220108 (divertor), plant-total (x n_mod).
        // Source: defaults.py:299 (replaceable_accounts), pin 0254385.
        attribute replacement_cost_per_event : Real =
            (blanket.capital_cost + divertor.capital_cost) * n_mod;

        // Charged-particle (ash) share of the fusion energy; the neutron power
        // that damages the first wall is the complement. Default 0.2002 is the
        // rounded model value; the exact 1cfe constant is E_ALPHA_DT / Q_DT =
        // 3.52 / 17.58. Source: physics.py:31, :177-179 (pin 0254385).
        attribute ash_frac : Real default 0.2002;

        // Core fluence limit [MW-yr/m^2] (instance binds; DT 18.0, defaults.py:291).
        attribute fluence_limit : Real;

        calc cas72_calc : 'Levelized Replacement Cost' {
            in cost_per_event = replacement_cost_per_event;
            in p_fus = fusion.p_fus;
            in ash_frac = ash_frac;
            in firstwall_area = rb.wall_area;
            in fluence_limit = fluence_limit;
            in availability = availability;
            in interest_rate = discount_rate;
            in operational_years = operational_years;
        }
        attribute cas72_annual : Real = cas72_calc.cost;   // expose_pure channel for A-2

        // CAS70 = CAS71 + CAS72, and the LCOE numerator total = CAS70 + CAS80.
        // Behind a calc so both sums are PRODUCER channels the LCOE cores can
        // read (WI-029 codegen-mechanics adaptation; inputs read the calc
        // outputs directly, the `in cas30 = indirect.cost` idiom).
        calc cas70_calc : 'Annual Cost Rollup' {
            in cas71 = cas71_calc.levelized;
            in cas72 = cas72_calc.cost;
            in cas80 = cas80_calc.levelized;
        }
        attribute cas70_annual : Real = cas70_calc.cas70;   // expose_pure channel for A-2

        // =====================================================================
        // LCOE  (WI-009 'LCOE DCF' core)
        // =====================================================================

        // WI-029: the DCF headline now takes the LEVELIZED annual-cost side —
        // CAS70 (= CAS71 levelized O&M + CAS72 levelized replacement) + CAS80
        // levelized fuel — replacing the unlevelized WI-025 O&M line that used
        // to be bound here. The headline CONVENTION is unchanged (Option ii:
        // idc_factor and total_capital = overnight_capital both untouched);
        // only the annual-cost numerator becomes complete.
        attribute annual_om : Real = cas70_calc.annual_total;  // CAS70+CAS80 levelized [$/yr]
        attribute availability : Real;       // capacity factor [0..1]
        attribute discount_rate : Real;      // discount / interest rate [1/yr]
        attribute operational_years : Real;  // operating lifetime N [yr]

        calc lcoe_calc : 'LCOE DCF' {
            in total_capital = total_capital;
            in annual_om = annual_om;
            in net_electric_mw = pb.p_net;
            in availability = availability;
            in discount_rate = discount_rate;
            in construction_years = construction_years;
            in operational_years = operational_years;
        }

        // ---- 1cfe-form CAS90 / LCOE COMPARISON channels (WI-029, Option ii) --
        // Owner ruling 2026-07-25: the DCF headline above stays untouched; these
        // two channels restate the same plant in 1costingFE's financing form so
        // the end-to-end LCOE can be compared account-for-account under A-2.
        //   cas90_1cfe = CRF * (overnight_capital + CAS60)
        //   lcoe_1cfe  = (cas90_1cfe + CAS70 + CAS80) / annual energy
        // CAS60 is the Item-3 'IDC Closed-Form Cost' REPORTED line (idc_capital)
        // — no new IDC arithmetic — and CRF is reused from cas71_calc, which
        // computes it from the same discount_rate / operational_years the DCF
        // core uses. total_capital stays == overnight_capital (Option C), so
        // CAS60 cannot enter the headline capital base: the two channels coexist
        // without double-counting. Comparison only — NOT the design-point headline.
        // Source: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
        // Ref: costs.py:547-556 (cas90 = CRF*total_capital); economics.py:88-92 (lcoe)
        calc cas90_1cfe_calc : '1cfe-Form Capital Charge' {
            in crf = cas71_calc.crf;
            in overnight_cost = overnight_capital;
            in idc_cost = idc.cost;
        }
        attribute cas90_1cfe : Real = cas90_1cfe_calc.cas90;   // expose_pure channel for A-2

        calc lcoe_1cfe_calc : '1cfe-Form LCOE' {
            in cas90 = cas90_1cfe_calc.cas90;
            in cas70 = cas70_calc.cas70;
            in cas80 = cas80_calc.levelized;
            in net_electric_mw = pb.p_net;
            in n_mod = n_mod;
            in availability = availability;
        }
        attribute lcoe_1cfe : Real = lcoe_1cfe_calc.lcoe;      // expose_pure channel for A-2

        // =====================================================================
        // VIABILITY CONSTRAINTS  (WI-009 mfe_viability)
        // =====================================================================

        assert constraint net_positive : 'Net Power Positive' {
            in net_electric = pb.p_net;
        }

        assert constraint recirc_ok : 'Economic Recirculating Threshold' {
            in rec_frac = pb.rec_frac;
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
