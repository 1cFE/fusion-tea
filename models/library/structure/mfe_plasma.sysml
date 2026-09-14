package mfe_plasma {
    private import ScalarValues::*;
    private import mfe_interfaces::*;
    private import mfe_plasma_sustainment::*;
    private import mfe_plasma_scaling::*;

    part def 'Plasma' {
        doc /*
        The confined D-T plasma, as a part: its geometry (major and minor radius, elongation,
        the stellarator shape factor), its operating point (peak density and ion temperature,
        the profile exponents), and the sustainment facts the source states for the design
        point (rotational transform, ISS04 renormalisation, fast-alpha confinement, the
        particle-to-energy confinement ratio, helium suppression, core impurities, the
        ion-to-electron temperature ratio). Every value is bound by the concept instance with
        its own citation; nothing here is concept-specific (MR-3). WI-057.
        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/output.md
        **Ref**: secs. 2.2-2.5 (the design point, Table 2 image page_002_table_0.png; profiles Fig. 16)
        **Basis**: the plasma as the owner of the quantities the geometry, sustainment, beta and fusion calcs read
        */
        // ---- ports (WI-057): the exchanges this part takes part in; declarative, see mfe_interfaces ----
        port neutron_out : 'Neutron Port';   // -> blanket.neutron_in (source_heat via blanket.p_fus)
        port alpha_out : 'Thermal Port';   // -> divertor.heat_in (divheat via divertor.p_alpha_heat, p_rad_core)
        port heat_in : ~'Thermal Port';   // <- heating.power_to_plasma (the absorbed heating, accounted at the blanket and the divertor)
        port fuel_in : ~'Material Port';   // <- fuel_cycle.fuel_out (the burn the fuelling sustains)
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
        // Operating-point lever (WI-030/WI-037). No default: a plasma without
        // its peak density is not a plasma. WI-037: T_e0 and n_He0 retired as
        // plant attributes -- both are computed by the sustainment chain below
        // (T_e0 from the held ratio, n_He0 from the converged A.5/A.6 ash
        // balance). WI-042: the electron density profile exponent retired too
        // -- the electron profile is derived inside the chain by
        // quasi-neutrality from the fuel profile and the ash on the
        // fusion-rate profile (Eq. A.5 pointwise), never bound at a point.
        // peak electron density [m^-3] (operating-point lever)
        attribute n_e0 : Real;
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
        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----
        attribute B : Real;   // <- magnet.B
        // ---- EXPOSEs (WI-057): this part's calc outputs, readable outside as <part>.<name> ----
        attribute beta : Real = beta_calc.beta;
        attribute p_alpha_heat : Real = sustain.p_alpha_heat;
        attribute p_aux_required : Real = sustain.p_aux_required;
        attribute p_fus : Real = fusion.p_fus;
        attribute p_rad : Real = sustain.p_rad;
        // ---- template calcs (WI-057): the analyses this part owns ----
        calc geom : 'Plasma Geometry' {
            in R_in = R;
            in a_in = a;
            in kappa_in = kappa;
            in f_shape_in = f_shape;
        }
        // Operating-point sustainment chain (WI-037): line-averaged density,
        // ISS04 tau_E (closed form), converged ash + quasi-neutral fuel,
        // composed radiation, and the required sustained coupled heating.
        // Reads the derived field (WI-035) through magnet.B; its computed
        // fuel/ash/T_e0 feed fusion below, and its one volume-averaged
        // pressure feeds beta (WI-042: the electron profile and the ash
        // profile are derived inside from the fuel and temperature profiles).
        calc sustain : 'Plasma Sustainment' {
            in n_e0_in = n_e0;
            in T_i0_in = T_i0;
            in V = geom.V;
            in a_in = a;
            in R_in = R;
            in B_in = B;
            in alpha_n_in = alpha_n;
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
        // the magnet part the way magnet_cost reads it. WI-042: reads the
        // sustainment chain's one volume-averaged pressure -- W and beta can
        // never disagree about the plasma's pressure.
        calc beta_calc : 'Volume-Averaged Beta' {
            in p_avg_in = sustain.p_avg;
            in B_in = B;
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
    }
}
