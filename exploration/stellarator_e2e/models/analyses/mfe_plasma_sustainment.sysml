package mfe_plasma_sustainment {
    private import ScalarValues::*;

    calc def 'Plasma Sustainment' {
        doc /*
        Operating-point sustainment chain (WI-037): from the machine (a, R,
        iota_2/3, axis field B), the operating-point levers (peak electron
        density n_e0, peak ion temperature T_i0), and installed physics facts,
        compute the required sustained plasma-coupled heating power and the
        forward ash/fuel state. Temperature and density remain design levers;
        the machine pushes back through the paired 'Sustainment Limit'
        (mfe_viability.sysml) on the computed p_aux_required.

        CHAIN (each stage an output; all evaluated at the same lever point):

          T_e0     = T_i0 / r_TiTe                                  [keV]
          n_bar19  = n_e0 * I_line(alpha_n_e) / 1e19                [1e19 m^-3]
                     I_line = integral_0^1 (1-rho^2)^alpha_n_e d rho
                     (line-averaged density -- ISS04's n19 takes its "usual
                     meaning"; the vol-av reading misses the printed tau_E
                     by -23%, goal learning L-001)
          ASH FIXED POINT (A.5/A.6, peak form, damped):
            n_D0 = n_T0 = (n_e0 - 2*n_He0) / 2      (quasi-neutrality;
                     trace W at f_W ~ 1e-5 neglected in the charge sum)
            W_th   = 1.5e-6 * e_keV * V * ( n_e0*T_e0/(1+alpha_n_e+alpha_T)
                     + (n_D0+n_T0+n_He0)*T_i0/(1+alpha_n+alpha_T) )   [MJ]
            tau_E  = (C * W_th^-0.61)^(1/0.39)                        [s]
                     C = 0.134*f_ren*a^2.28*B^0.84*iota_23^0.41
                         *n_bar19^0.54*R^0.64
                     (ISS04 Eq. A.7 with the source's own P = W/tau_E
                     substitution -- the closed form behind Eq. A.8)
            n_He0 <- f_suppr * tau_ratio * tau_E * n_D0*n_T0*sigv_dt(T_i0)
                     (Eq. A.5 helium balance x Eq. A.6 suppression)
          RADIATION (composed; profile-integrated over the model's own
          (1-rho^2)^alpha profiles):
            p_brems = 5.35e-37 * Z_eff * n_e0^2 * V
                      * int (1-rho^2)^(2*alpha_n_e) * sqrt(T_e(rho)) dV' [MW]
            p_line  = f_W * n_e0^2 * V
                      * int (1-rho^2)^(2*alpha_n_e) * L_z_W(T_e(rho)) dV' [MW]
                      (L_z_W: piecewise coronal cooling-curve fit)
            p_sync  = Albajar (2001) formula at kappa_sync, R_w_sync       [MW]
            p_rad   = p_brems + p_line + p_sync
          BALANCE (Eq. A.2/A.3):
            p_alpha_heat   = f_alpha * ash_frac * p_fus_internal          [MW]
                     p_fus_internal: the identical profile-integrated
                     Bosch-Hale evaluation as 'DT Fusion Power' at
                     (n_D0, n_T0, T_i0) -- same algorithm, same contract
            p_aux_required = p_rad + W_th/tau_E - p_alpha_heat            [MW]

        EXECUTABLE SEMANTIC (Rung B, WI-022 pattern): exp(), numerical
        integrals, and the damped fixed point route this calc to the
        handwritten codegen stage (manual_required); the generated handwritten
        impl is normative and is guarded bit-exact by the oracle.
        Discretization/convergence contract (mirrored exactly in the oracle):
        trapezoidal rule in rho over [0,1], N = 200,000 intervals, temperature
        floor 1e-6 keV, pure-Python float64; ash fixed point by damped
        half-step iteration n_He0 <- 0.5*(n_He0 + F(n_He0)) from n_He0 = 0,
        absolute tolerance 1e12 m^-3, iteration cap 200; non-convergence,
        non-positive fuel density, or a non-finite intermediate RAISES --
        fail loudly, never clamp (amended MR-WI037-2).

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
            (equations; every value image-verified -- the iter-01 AND iter-02
            text tables are corrupted, the raw PDF and page images govern);
            /home/reid/1cfe/1costingfe/src/costingfe/layers/radiation.py (pin 0254385);
            /home/reid/1cfe/1costingfe/src/costingfe/layers/reactivity.py (pin 0254385)
        **Ref**: images/page_031_eq_6.png (Eq. A.7 ISS04), page_031_eq_7.png
            (Eq. A.8, the P = W/tau_E rewriting this closed form reproduces);
            page_031_eq_1.png / page_031_eq_2.png (Eq. A.2/A.3 balance);
            page_031_eq_4.png / page_031_eq_5.png (Eq. A.5 helium balance,
            A.6 suppression); iter-02 raw PDF appendix A text ("replace the
            heating power by the ratio of plasma energy divided by the energy
            confinement time"); radiation.py:260,275 (bremsstrahlung
            5.35e-37*Z_eff*n^2*sqrt(T)), radiation.py:83-96 (W cooling-curve
            fit), radiation.py:180-241 (Albajar synchrotron, eqs 13/15 of
            Albajar 2001); reactivity.py:54-70 (Bosch-Hale sigv_dt);
            goal evidence work/orchestration/goals/operating-point-closure/
            evidence/T-002_prototype/NOTES.md (cross-checks: tau_E -0.1%,
            p_rad -0.1%, n_He0 +3.6%, p_fus +0.7% vs printed point A)
        **Basis**: steady-state 0D power balance over (1-rho^2)^alpha profiles
            with ISS04 confinement in the source's own closed form, printed
            ash chain, and composed radiation; concept-agnostic (MR-3) --
            machine values, levers, and quality facts bound by instances
        */

        // peak electron density [m^-3] (operating-point lever)
        in attribute n_e0_in : Real;
        // peak ion temperature [keV] (operating-point lever)
        in attribute T_i0_in : Real;
        // plasma volume [m^3]
        in attribute V : Real;
        // minor radius [m]
        in attribute a_in : Real;
        // major radius [m]
        in attribute R_in : Real;
        // axis-averaged field [T] (the derived field, WI-035)
        in attribute B_in : Real;
        // fuel/ash density profile exponent [1]
        in attribute alpha_n_in : Real;
        // electron density profile exponent [1]
        in attribute alpha_n_e_in : Real;
        // temperature profile exponent [1]
        in attribute alpha_T_in : Real;
        // per-event D-T fusion energy [J]
        in attribute E_fus_in : Real;
        // rotational transform at s = 2/3 [1] (held sourced machine fact)
        in attribute iota_23_in : Real;
        // ISS04 renormalization multiplier [1] (held sourced quality fact)
        in attribute f_ren_in : Real;
        // fast-particle (alpha) confinement fraction [1]
        in attribute f_alpha_in : Real;
        // particle-to-energy confinement time ratio tau_star/tau_E [1]
        in attribute tau_ratio_in : Real;
        // helium suppression factor [1] (Eq. A.6)
        in attribute f_suppr_in : Real;
        // core effective charge [1]
        in attribute Z_eff_in : Real;
        // core tungsten fraction n_W/n_e [1]
        in attribute f_W_in : Real;
        // ion-to-electron temperature ratio T_i0/T_e0 [1]
        in attribute r_TiTe_in : Real;

        // Charged-particle (ash) fraction of D-T fusion energy. Source:
        // physics.py:31 (3.52/17.58). Same convention as 'Neutron Wall Load'.
        in attribute ash_frac_in : Real default 0.2002;
        // Synchrotron wall reflectivity [1]. Source: radiation.py:187 (R_w
        // default 0.6, metallic walls).
        in attribute R_w_sync_in : Real default 0.6;
        // Albajar elongation parameter [1]; 1.0 is the disclosed stellarator
        // reading of the tokamak-fit formula (design D5).
        in attribute kappa_sync_in : Real default 1.0;

        // Manual interface (see EXECUTABLE SEMANTIC): the handwritten impl
        // computes the doc-specified chain and is the executable meaning.
        // line-averaged electron density [1e19 m^-3]
        out attribute n_bar19 : Real;
        // converged peak helium-ash density [m^-3]
        out attribute n_He0 : Real;
        // quasi-neutral peak deuterium density [m^-3]
        out attribute n_D0 : Real;
        // quasi-neutral peak tritium density [m^-3]
        out attribute n_T0 : Real;
        // peak electron temperature [keV] (= T_i0 / r_TiTe)
        out attribute T_e0 : Real;
        // stored thermal plasma energy [MJ]
        out attribute W_th : Real;
        // ISS04 energy confinement time, closed form [s]
        out attribute tau_E : Real;
        // bremsstrahlung radiation [MW]
        out attribute p_brems : Real;
        // impurity (W) line radiation [MW]
        out attribute p_line : Real;
        // synchrotron radiation [MW]
        out attribute p_sync : Real;
        // total composed radiation [MW]
        out attribute p_rad : Real;
        // absorbed alpha heating f_alpha * ash_frac * p_fus [MW]
        out attribute p_alpha_heat : Real;
        // required sustained plasma-coupled heating [MW]
        out attribute p_aux_required : Real;
    }
}
