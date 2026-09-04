package mfe_plant {
    private import ScalarValues::*;
    private import mfe_power_core::*;
    private import mfe_subsystems::*;
    private import mfe_plasma_scaling::*;
    private import mfe_plasma_sustainment::*;
    private import mfe_power_balance::*;
    private import mfe_cryo_plant::*;
    private import mfe_heating_chain::*;
    private import mfe_magnet_cost::*;
    private import mfe_magnet_field::*;
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
        part magnet : 'Magnet System' {
            :>> capital_cost = magnet_capital_rollup.capital_cost;   // WI-035: decomposed rollup
            :>> r_coil = rb.r_coil;   // coil bore = radial-build vessel_or (WI-021)
            // WI-035: the axis field is COMPUTED from the coil-set current
            // (reference redefinition, WI-021 pattern); B is no longer settable.
            :>> B = field_calc.B_axis;
            // WI-036: the winding-pack side and the winding length are now
            // COMPUTED too -- the pack is sized by the current it carries and
            // the length follows machine scale. j_wp and k_coil are the
            // settable levers that replaced them.
            :>> wp_side = wp_sizing.wp_side;
            :>> c_coil = coil_length.c_coil;
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
        // CAS27 pass-through
        attribute special_materials_capital : Real;

        // =====================================================================
        // PHYSICS SPINE  (Plasma Geometry -> DT Fusion Power -> Power Balance)
        // =====================================================================

        // Plasma geometry inputs (WI-011).
        // major radius [m]
        attribute R : Real;
        // minor radius [m]
        attribute a : Real;
        // elongation
        attribute kappa : Real;
        // Shape/packing factor (WI-020). Default 1.0 = pure elongated torus
        // (tokamak); a shaped stellarator instance overrides it.
        attribute f_shape : Real default 1.0;

        calc geom : 'Plasma Geometry' {
            in R_in = R;
            in a_in = a;
            in kappa_in = kappa;
            in f_shape_in = f_shape;
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
            in R_in = R;
            in a_in = a;
            in kappa_in = kappa;
            in vacuum_t_in = vacuum_t;
            in firstwall_t_in = firstwall_t;
            in blanket_t_in = blanket_t;
            in reflector_t_in = reflector_t;
            in ht_shield_t_in = ht_shield_t;
            in structure_t_in = structure_t;
            in gap1_t_in = gap1_t;
            in vessel_t_in = vessel_t;
            in coil_t_in = coil_t;
            in gap2_t_in = gap2_t;
            in lt_shield_t_in = lt_shield_t;
        }

        // Fusion-power inputs (WI-011 sets density directly for the stellarator;
        // no density closure here). WI-022: sigma_v > 0 selects the exact 0D
        // bypass; sigma_v = 0 (default) computes the profile integral from the
        // five profile inputs below (defaults mirror the calc def -- a 0D/flat
        // concept binds sigma_v only and leaves the profile inputs dormant).
        // electron density [m^-3]
        attribute n_e : Real;
        // 0D-effective reactivity [m^3/s]; > 0 = bypass
        attribute sigma_v : Real default 0.0;
        // per-event D-T fusion energy [J]
        attribute E_fus : Real;
        // WI-037: n_D0 and n_T0 retired as plant attributes -- the fuel peaks
        // are computed by the sustainment chain (quasi-neutrality with the
        // converged ash), wired below. The operating-point levers are n_e0
        // and T_i0.
        // peak ion temperature [keV]
        attribute T_i0 : Real default 1.0;
        // density profile exponent
        attribute alpha_n : Real default 0.0;
        // temperature profile exponent
        attribute alpha_T : Real default 0.0;

        // Beta inputs (WI-030). No defaults: a beta without its peaks is not a
        // beta. WI-037: T_e0 and n_He0 retired as plant attributes -- both are
        // computed by the sustainment chain below (T_e0 from the held ratio,
        // n_He0 from the converged A.5/A.6 ash balance).
        // peak electron density [m^-3] (operating-point lever)
        attribute n_e0 : Real;
        // electron density profile exponent [1]
        attribute alpha_n_e : Real;

        // Sustainment held facts (WI-037). No defaults for the physics facts:
        // a sustainment without its machine and quality facts is not a
        // sustainment (the WI-030 no-defaults precedent) -- every MFE concept
        // binds them from source.
        // rotational transform at s = 2/3 [1]
        attribute iota_23 : Real;
        // ISS04 renormalization multiplier [1]
        attribute f_ren : Real;
        // fast-particle (alpha) confinement fraction [1]
        attribute f_alpha_fast : Real;
        // particle-to-energy confinement time ratio tau_star/tau_E [1]
        attribute tau_ratio_ash : Real;
        // helium suppression factor [1]
        attribute f_suppr_ash : Real;
        // core effective charge [1]
        attribute Z_eff_core : Real;
        // core tungsten fraction n_W/n_e [1]
        attribute f_W_core : Real;
        // ion-to-electron temperature ratio T_i0/T_e0 [1]
        attribute Ti_over_Te : Real;

        // Operating-point sustainment chain (WI-037): line-averaged density,
        // ISS04 tau_E (closed form), converged ash + quasi-neutral fuel,
        // composed radiation, and the required sustained coupled heating.
        // Reads the derived field (WI-035) through magnet.B; its computed
        // fuel/ash/T_e0 feed fusion and beta below by reference redefinition.
        calc sustain : 'Plasma Sustainment' {
            in n_e0_in = n_e0;
            in T_i0_in = T_i0;
            in V = geom.V;
            in a_in = a;
            in R_in = R;
            in B_in = magnet.B;
            in alpha_n_in = alpha_n;
            in alpha_n_e_in = alpha_n_e;
            in alpha_T_in = alpha_T;
            in E_fus_in = E_fus;
            in iota_23_in = iota_23;
            in f_ren_in = f_ren;
            in f_alpha_in = f_alpha_fast;
            in tau_ratio_in = tau_ratio_ash;
            in f_suppr_in = f_suppr_ash;
            in Z_eff_in = Z_eff_core;
            in f_W_in = f_W_core;
            in r_TiTe_in = Ti_over_Te;
        }

        // Volume-averaged beta (WI-030): B enters the physics here, read from
        // the magnet part the way magnet_cost reads it.
        calc beta_calc : 'Volume-Averaged Beta' {
            in n_e0_in = n_e0;
            in T_e0_in = sustain.T_e0;
            in n_D0_in = sustain.n_D0;
            in n_T0_in = sustain.n_T0;
            in n_He0_in = sustain.n_He0;
            in T_i0_in = T_i0;
            in alpha_n_in = alpha_n;
            in alpha_n_e_in = alpha_n_e;
            in alpha_T_in = alpha_T;
            in B_in = magnet.B;
        }

        // Peak field on the winding (WI-030), compared against the conductor
        // ceiling by peak_field_ok below.
        // WI-035: axis field derived from the coil-set current (inversion
        // ruling 2026-08-30); EXPOSEd into magnet.B above, so beta_calc,
        // peak_field_calc, and magnet_cost read the computed field unchanged.
        calc field_calc : 'Coil Set Axis Field' {
            in n_coils = magnet.n_coils;
            in I_coil = magnet.I_coil;
            in k_link = magnet.k_link;
            in R0 = magnet.R0;
        }

        calc peak_field_calc : 'Conductor Peak Field' {
            in B_axis_in = magnet.B;
            in peak_ratio_in = magnet.peak_ratio;
        }

        // WI-036: the winding pack is sized by the current it carries, so
        // wp_side stops being an entry point and becomes a consequence of
        // coil current and the chosen winding-pack current density.
        calc wp_sizing : 'Winding Pack Sizing' {
            in I_coil = magnet.I_coil;
            in j_wp = magnet.j_wp;
        }

        // WI-036: winding length responds to machine scale through a held
        // coil-shape factor, instead of resting on a printed constant.
        calc coil_length : 'Coil Winding Length' {
            in R0 = magnet.R0;
            in k_coil = magnet.k_coil;
        }

        // WI-036: a wider winding pack now costs cold mass -- this feeds the
        // WI-024 cryoplant chain, which already reaches cryoplant capital.
        calc wp_volume : 'Winding Pack Cold Volume' {
            in n_coils = magnet.n_coils;
            in wp_side = wp_sizing.wp_side;
            in c_coil = coil_length.c_coil;
            in f_wp_vol = magnet.f_wp_vol;
            // WI-036: vol_cold_cryo stays a live settable slot and enters here
            // as an ADDITIVE term, so modelling the winding-pack chain does not
            // retire it (the standing [OWNER 2026-08-27] WI-032 ruling bars
            // retiring the input, not modelling the chain behind it).
            in vol_extra = vol_cold_cryo;
        }

        // WI-035 stress operand, now consuming the WI-036 computed wp_side.
        calc wp_stress : 'Winding Pack Stress' {
            in I_coil = magnet.I_coil;
            in B_peak_in = peak_field_calc.B_peak;
            in wp_side = wp_sizing.wp_side;
            in k_sigma = magnet.k_sigma;
        }

        // WI-036: the conductor's own operand, checked separately from the
        // structure's -- the second of the two checks every surveyed HTS
        // fusion design performs.
        calc cond_strain : 'Conductor Strain' {
            in sigma_wp = wp_stress.sigma_wp;
            in E_wp = magnet.E_wp;
            in f_cond = magnet.f_cond;
        }

        calc fusion : 'DT Fusion Power' {
            in n_e_in = n_e;
            in sigma_v_in = sigma_v;
            in E_fus_in = E_fus;
            in V = geom.V;
            in n_D0_in = sustain.n_D0;
            in n_T0_in = sustain.n_T0;
            in T_i0_in = T_i0;
            in alpha_n_in = alpha_n;
            in alpha_T_in = alpha_T;
        }

        // Power-balance inputs (WI-011).
        // neutron energy multiplier
        attribute mn : Real;
        // thermal-to-electric efficiency
        attribute eta_th : Real;
        // pumping-power capture efficiency
        attribute eta_p : Real;
        // primary coolant pumping power [MW]
        attribute p_pump : Real;
        // subsystem/control fraction
        attribute f_sub : Real;
        // TF coil power [MW]
        attribute p_tf : Real;
        // PF coil power [MW]
        attribute p_pf : Real;
        // TF coil cooling [MW]
        attribute p_tfcool : Real;
        // PF coil cooling [MW]
        attribute p_pfcool : Real;
        // tritium systems [MW]
        attribute p_trit : Real;
        // housekeeping [MW]
        attribute p_house : Real;
        // directly-specified cryoplant electrical [MW] (additive direct term, WI-024)
        attribute p_cryo : Real default 0.0;

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
            // WI-036: the cold volume is now computed from the sized winding
            // pack, with vol_cold_cryo carried into that calc as an additive
            // settable term (see the wp_volume usage above).
            in vol_cold = wp_volume.vol_cold_total;
            in p_fixed = p_fixed_cryo;
            in f_uplift = f_uplift_cryo;
            in T_cold = T_cold_cryo;
            in T_amb = T_amb_cryo;
            in f_carnot = f_carnot_cryo;
            in p_direct = p_cryo;
        }

        // Heating power chain (WI-039). Dormant by default, on the WI-024
        // cryoplant pattern: a concept that knows its heating powers outright
        // binds the direct terms and leaves the chain unbound; a concept
        // deriving them binds the chain and zeroes the direct terms. The
        // efficiencies default to 1.0 (not 0) so a dormant chain's effective
        // efficiency stays defined -- the mode is selected by the powers,
        // never by an efficiency.
        // installed wall-plug electrical power for heating [MW]
        attribute p_wallplug_heat : Real default 0.0;
        // wall-plug -> source output conversion efficiency [1]
        attribute eta_source_heat : Real default 1.0;
        // source output -> plasma-coupled fraction [1] (deposition assumption)
        attribute eta_couple_heat : Real default 1.0;
        // directly-specified source-output heating power [MW] (dormant path)
        attribute p_delivered_direct_heat : Real default 0.0;
        // directly-specified plasma-coupled heating power [MW] (dormant path)
        attribute p_coupled_direct_heat : Real default 0.0;

        calc heat : 'Heating Power Chain' {
            in p_wallplug = p_wallplug_heat;
            in eta_source = eta_source_heat;
            in eta_couple = eta_couple_heat;
            in p_delivered_direct = p_delivered_direct_heat;
            in p_coupled_direct = p_coupled_direct_heat;
        }

        calc pb : 'MFE Power Balance Calc' {
            in p_nrl = fusion.p_fus;
            in p_input_in = heat.p_coupled;
            in mn_in = mn;
            in eta_th_in = eta_th;
            in eta_p_in = eta_p;
            in p_wallplug_in = heat.p_wallplug_total;
            in p_pump_in = p_pump;
            in f_sub_in = f_sub;
            in p_tf_in = p_tf;
            in p_pf_in = p_pf;
            in p_tfcool_in = p_tfcool;
            in p_pfcool_in = p_pfcool;
            in p_trit_in = p_trit;
            in p_house_in = p_house;
            in p_cryo = cryo_elec.p_elec;
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

        // Magnet (CAS22.1.3). WI-035: 'Magnet Coil Cost' is retained as the
        // 1cfe-form COMPARISON channel (magnet_capital_1cfe); the rollup reads
        // the decomposed sub-accounts below.
        calc magnet_cost : 'Magnet Coil Cost' {
            in G = magnet.G;
            in B = magnet.B;
            in R0 = magnet.R0;
            in r_coil = rb.r_coil;
            in cost_per_kAm = magnet.cost_per_kAm;
            in coil_markup = magnet.coil_markup;
        }

        // Winding-pack account (real winding length, WI-035 D4).
        calc winding_pack_cost : 'Winding Pack Cost' {
            in n_coils = magnet.n_coils;
            in I_coil = magnet.I_coil;
            in f_set = magnet.f_set;
            in c_coil = magnet.c_coil;
            in cost_per_kAm = magnet.cost_per_kAm;
            in f_wp_fab = magnet.f_wp_fab;
        }

        // Magnet casing-structure account (WI-035 D5; casings only --
        // inter-coil plates/rings/legs stay CAS22.1.5).
        calc magnet_structure_cost : 'Magnet Structure Cost' {
            in n_coils = magnet.n_coils;
            in m_casing = magnet.m_casing;
            in steel_price = magnet.steel_price;
            in f_steel_fab = magnet.f_steel_fab;
        }

        // CAS22.1.3 rollup (WI-035 D6): reference-binding envelope.
        calc magnet_capital_rollup : 'Magnet Capital' {
            in winding_cost = winding_pack_cost.cost;
            in structure_cost_in = magnet_structure_cost.cost;
        }

        // Blanket (CAS22.1.1).
        calc blanket_cost : 'Blanket Cost' {
            in unit_cost = blanket.unit_cost;
            in structure_factor = blanket.structure_factor;
            in blanket_vol = rb.blanket_vol;
            in p_th_in = p_th;
        }

        // Shield (CAS22.1.2).
        calc shield_cost : 'Shield Cost' {
            in unit_cost = shield.unit_cost;
            in shield_vol = rb.shield_vol;
            in shield_scale = shield.shield_scale;
            in p_th_in = p_th;
        }

        // Primary structure (CAS22.1.5).
        calc structure_cost : 'Structure Cost' {
            in unit_cost = structure.unit_cost;
            in structure_vol = rb.structure_vol;
            in p_et_in = p_et;
        }

        // Vacuum vessel (CAS22.1.6, shell term).
        calc vessel_cost : 'Vessel Cost' {
            in unit_cost = vessel.unit_cost;
            in vessel_vol = rb.vessel_vol;
            in p_et_in = p_et;
        }

        // Power supplies (CAS22.1.7).
        calc power_supplies_cost : 'Power Supplies Cost' {
            in base = power_supplies.base;
            in p_et_in = p_et;
        }

        // Divertor (CAS22.1.8) -- WI-009 carrier has no drivers; supplied here.
        // divertor cost at 1 GWth [$] (WI-011)
        attribute divertor_base : Real;
        calc divertor_cost : 'Divertor Cost' {
            in base = divertor_base;
            in p_th_in = p_th;
        }

        // Heating & CD (CAS22.1.4) -- WI-009 carrier has no drivers; the heating
        // mix (per-MW rates + delivered powers) is supplied here (WI-011).
        attribute heating_nbi_per_mw : Real;
        attribute p_nbi : Real;
        attribute heating_icrf_per_mw : Real;
        attribute p_icrf : Real;
        attribute heating_ecrh_per_mw : Real;
        attribute heating_lhcd_per_mw : Real;
        attribute p_lhcd : Real;
        calc heating_cost : 'Heating Cost' {
            in nbi_per_mw = heating_nbi_per_mw;
            in p_nbi_in = p_nbi;
            in icrf_per_mw = heating_icrf_per_mw;
            in p_icrf_in = p_icrf;
            in ecrh_per_mw = heating_ecrh_per_mw;
            in p_ecrh_in = heat.p_delivered;
            in lhcd_per_mw = heating_lhcd_per_mw;
            in p_lhcd_in = p_lhcd;
        }

        // Balance-of-plant (CAS23 turbine, CAS24 electric, CAS25 heat rej,
        // CAS26 misc) -- one 'Linear Power Cost' calc each.
        // module count; single-module demo
        attribute n_mod : Real default 1.0;
        calc turbine_cost : 'Linear Power Cost' {
            in power = p_the;
            in cost_per_mw = turbine.cost_per_mw;
            in n_mod_in = n_mod;
        }
        calc electric_cost : 'Linear Power Cost' {
            in power = p_et;
            in cost_per_mw = electric_plant.cost_per_mw;
            in n_mod_in = n_mod;
        }
        calc heat_rejection_cost : 'Linear Power Cost' {
            in power = p_th;
            in cost_per_mw = heat_rejection.cost_per_mw;
            in n_mod_in = n_mod;
        }
        calc misc_cost : 'Linear Power Cost' {
            in power = p_et;
            in cost_per_mw = misc_plant.cost_per_mw;
            in n_mod_in = n_mod;
        }

        // CAS21 grouped base-cost sums [$] (WI-025 D1; instance binds -- fuel-keyed).
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
            in p_the_in = p_the;
            in p_th_in = p_th;
            in p_et_in = p_et;
        }

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
        // C220200 coolant (two-term, plant-total).
        // 166.0 M$ -> $
        attribute coolant_primary_base : Real;
        // 40.6 M$ -> $
        attribute coolant_intermediate_base : Real;
        calc coolant : 'Coolant Cost' {
            in primary_base = coolant_primary_base;
            in p_net = pb.p_net;
            in intermediate_base = coolant_intermediate_base;
            in p_th_in = p_th;
            in n_mod_in = n_mod;
        }
        // C220300 aux cooling (plant-total p_th) + cryoplant (per-module p_cryo).
        // 1.10e-3 M$/MW -> $/MW
        attribute aux_per_mw : Real;
        // 200.0 M$ -> $
        attribute aux_cryo_base : Real;
        calc aux_cooling : 'Aux Cooling Cost' {
            in aux_per_mw_in = aux_per_mw;
            in p_th_in = p_th;
            in cryo_base = aux_cryo_base;
            in p_cryo = cryo_elec.p_elec;
            in n_mod_in = n_mod;
        }
        // C220400 waste (a=1.0), C220500 fuel, C220600 other, C220700 I&C:
        // shared 'Plant Power-Law Cost'. Account-structural ref/alpha literal;
        // base bound at instance.
        // 1.96 M$ -> $
        attribute waste_base : Real;
        calc waste : 'Plant Power-Law Cost' {
            in base = waste_base; in power = p_th; in n_mod_in = n_mod;
            in ref_power = 1000.0; in alpha = 1.0;
        }
        // fh_base[fuel] [$]
        attribute fuel_handling_base : Real;
        calc fuel_handling : 'Plant Power-Law Cost' {
            in base = fuel_handling_base; in power = pb.p_net; in n_mod_in = n_mod;
            in ref_power = 1000.0; in alpha = 0.7;
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

        calc fuel_calc : 'DT Fuel Cost' {
            in p_fus = fusion.p_fus;
            in n_mod_in = n_mod;
            in availability_in = availability;
            in cost_per_rxn = fuel_cost_per_rxn;
            in q_eff = fuel_q_eff;
            in mev_to_joules_in = mev_to_joules;
            in burn_fraction_in = burn_fraction;
            in fuel_recovery_in = fuel_recovery;
        }
        calc cas80_calc : 'Levelized Annual Cost' {
            // Read the fuel producer directly. A bare `annual_fuel = fuel_calc.annual_fuel`
            // alias resolves at part-def scope and mints no instance params key
            // (the WI-028 bare-alias class); fuel_calc__annual_fuel is already a
            // channel, so the A-2 row reads it without the alias.
            in annual_cost = fuel_calc.annual_fuel;
            in interest_rate = discount_rate;
            in inflation_rate_in = inflation_rate;
            in operational_years_in = operational_years;
            in project_time = construction_years;
        }
        // expose for producer aggregation
        attribute cas80_annual : Real = cas80_calc.levelized;

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
            in ash_frac_in = ash_frac;
            in firstwall_area = rb.wall_area;
            in fluence_limit_in = fluence_limit;
            in availability_in = availability;
            in interest_rate = discount_rate;
            in operational_years_in = operational_years;
        }
        // expose_pure channel for A-2
        attribute cas72_annual : Real = cas72_calc.cost;

        // CAS70 = CAS71 + CAS72, and the LCOE numerator total = CAS70 + CAS80.
        // Behind a calc so both sums are PRODUCER channels the LCOE cores can
        // read (WI-029 codegen-mechanics adaptation; inputs read the calc
        // outputs directly, the `in cas30 = indirect.cost` idiom).
        calc cas70_calc : 'Annual Cost Rollup' {
            in cas71 = cas71_calc.levelized;
            in cas72 = cas72_calc.cost;
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
        // capacity factor [0..1]
        attribute availability : Real;
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
            in B_peak = peak_field_calc.B_peak;
            in B_max_in = magnet.B_max;
        }

        // WI-035: computed stress operand vs held sourced allowable (800 MPa).
        assert constraint wp_stress_ok : 'Winding Pack Stress Limit' {
            in sigma_in = wp_stress.sigma_wp;
            in sigma_allow_in = magnet.sigma_allow;
        }

        // WI-036: the conductor's own check, distinct from the structure's.
        // The structural operand above is a PEAK stress quantity (its k_sigma
        // is anchored to the source's printed "Peak stress on WP" row), and
        // the ITER criteria carry 666 MPa primary membrane against 1.0-1.333
        // GPa peak; sigma_allow stays at the source's own 800 MPa design limit
        // and is not re-categorised to open feasibility (WI-036 MR-6).
        assert constraint cond_strain_ok : 'Conductor Strain Limit' {
            in eps_cond = cond_strain.eps_cond;
            in eps_cond_allow_in = magnet.eps_cond_allow;
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
        attribute magnet_capital_1cfe : Real = magnet_cost.capital_cost;
        attribute cryoplant_capital : Real = aux_cooling.cryo_cost;
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
