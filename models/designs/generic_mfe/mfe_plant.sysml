package mfe_plant {
    private import ScalarValues::*;
    private import mfe_power_core::*;
    private import mfe_subsystems::*;
    private import mfe_plasma_scaling::*;
    private import mfe_power_balance::*;
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
        }
        part heating : 'Heating and CD' {
            :>> capital_cost = heating_cost.cost;
        }
        part divertor : 'Divertor' {
            :>> capital_cost = divertor_cost.cost;
        }

        // Shared power core (mfe_subsystems).
        part blanket : 'Blanket' {
            :>> capital_cost = blanket_cost.cost;
        }
        part shield : 'Shield' {
            :>> capital_cost = shield_cost.cost;
        }
        part structure : 'Primary Structure' {
            :>> capital_cost = structure_cost.cost;
        }
        part vessel : 'Vacuum Vessel' {
            :>> capital_cost = vessel_cost.cost;
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

        // Pass-through direct accounts (initial-model limitation; capital set
        // directly by WI-011, in $).
        part buildings : 'Buildings';                 // CAS21
        attribute preconstruction_capital : Real;      // CAS10/20 pass-through
        attribute special_materials_capital : Real;    // CAS27 pass-through

        // =====================================================================
        // PHYSICS SPINE  (Plasma Geometry -> DT Fusion Power -> Power Balance)
        // =====================================================================

        // Plasma geometry inputs (WI-011).
        attribute R : Real;       // major radius [m]
        attribute a : Real;       // minor radius [m]
        attribute kappa : Real;   // elongation

        calc geom : 'Plasma Geometry' {
            in R = R;
            in a = a;
            in kappa = kappa;
        }

        // Fusion-power inputs (WI-011 sets density directly for the stellarator;
        // no density closure here).
        attribute n_e : Real;     // electron density [m^-3]
        attribute sigma_v : Real; // D-T reactivity <sigma*v> [m^3/s]
        attribute E_fus : Real;   // per-event D-T fusion energy [J]

        calc fusion : 'DT Fusion Power' {
            in n_e = n_e;
            in sigma_v = sigma_v;
            in E_fus = E_fus;
            in V = geom.V;
        }

        // Power-balance inputs (WI-011).
        attribute p_input : Real;   // plasma heating power [MW]
        attribute mn : Real;        // neutron energy multiplier
        attribute eta_th : Real;    // thermal-to-electric efficiency
        attribute eta_p : Real;     // pumping-power capture efficiency
        attribute eta_pin : Real;   // input-power wall-plug efficiency
        attribute fpcppf : Real;    // primary coolant pumping-power fraction
        attribute f_sub : Real;     // subsystem/control fraction
        attribute p_tf : Real;      // TF coil power [MW]
        attribute p_pf : Real;      // PF coil power [MW]
        attribute p_tfcool : Real;  // TF coil cooling [MW]
        attribute p_pfcool : Real;  // PF coil cooling [MW]
        attribute p_trit : Real;    // tritium systems [MW]
        attribute p_house : Real;   // housekeeping [MW]
        attribute p_cryo : Real;    // cryogenic pumping [MW]

        calc pb : 'MFE Power Balance Calc' {
            in p_nrl = fusion.p_fus;
            in p_input = p_input;
            in mn = mn;
            in eta_th = eta_th;
            in eta_p = eta_p;
            in eta_pin = eta_pin;
            in fpcppf = fpcppf;
            in f_sub = f_sub;
            in p_tf = p_tf;
            in p_pf = p_pf;
            in p_tfcool = p_tfcool;
            in p_pfcool = p_pfcool;
            in p_trit = p_trit;
            in p_house = p_house;
            in p_cryo = p_cryo;
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
            in r_coil = magnet.r_coil;
            in cost_per_kAm = magnet.cost_per_kAm;
            in coil_markup = magnet.coil_markup;
        }

        // Blanket (CAS22.1.1).
        calc blanket_cost : 'Blanket Cost' {
            in unit_cost = blanket.unit_cost;
            in structure_factor = blanket.structure_factor;
            in blanket_vol = blanket.blanket_vol;
            in p_th = p_th;
        }

        // Shield (CAS22.1.2).
        calc shield_cost : 'Shield Cost' {
            in unit_cost = shield.unit_cost;
            in shield_vol = shield.shield_vol;
            in shield_scale = shield.shield_scale;
            in p_th = p_th;
        }

        // Primary structure (CAS22.1.5).
        calc structure_cost : 'Structure Cost' {
            in unit_cost = structure.unit_cost;
            in structure_vol = structure.structure_vol;
            in p_et = p_et;
        }

        // Vacuum vessel (CAS22.1.6, shell term).
        calc vessel_cost : 'Vessel Cost' {
            in unit_cost = vessel.unit_cost;
            in vessel_vol = vessel.vessel_vol;
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

        // =====================================================================
        // CAPITAL ROLLUP  (all $)
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

        // Direct-cost subtotal (modeled + pass-through direct accounts).
        attribute direct_capital : Real =
            powercore_capital + bop_capital + buildings.capital_cost
            + preconstruction_capital + special_materials_capital;

        // Contingency (CAS29) on the direct subtotal.
        attribute contingency_rate : Real;  // FOAK 0.10 / NOAK 0.0 (WI-011)
        calc contingency : 'Contingency Cost' {
            in contingency_rate = contingency_rate;
            in direct_subtotal = direct_capital;
        }
        attribute contingency_capital : Real = contingency.cost;

        // Indirect service costs (CAS30) as a fraction of direct cost.
        attribute indirect_fraction : Real;   // 0.20 of direct (WI-011)
        attribute construction_years : Real;  // Yc [yr] (shared with LCOE + CAS30)
        calc indirect : 'Indirect Cost' {
            in indirect_fraction = indirect_fraction;
            in direct_cost = direct_capital;
            in construction_time = construction_years;
        }
        attribute indirect_capital : Real = indirect.cost;

        // Total overnight capital [$].
        attribute total_capital : Real =
            direct_capital + contingency_capital + indirect_capital;

        // =====================================================================
        // LCOE  (WI-009 'LCOE DCF' core)
        // =====================================================================

        attribute annual_om : Real;          // CAS70 O&M pass-through [$/yr] (WI-011)
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
