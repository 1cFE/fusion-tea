package mfe_plasma_sustainment {
    private import ScalarValues::*;

    calc def 'Plasma Sustainment' {
        doc /*
        Operating-point sustainment chain (WI-037; profiles WI-042): from the
        machine (a, R, iota_2/3, axis field B), the operating-point levers
        (peak electron density n_e0, peak ion temperature T_i0), and installed
        physics facts, compute the required sustained plasma-coupled heating
        power and the forward ash/fuel state. Temperature and density remain
        design levers; the machine pushes back through the paired
        'Sustainment Limit' (mfe_viability.sysml) on the computed
        p_aux_required.

        PROFILES (Stellaris Eqs. 2-3 and the source's own ash rule; WI-042):
          u        = 1 - rho^2;  dV/V = 2 rho d(rho)
          T_i(rho) = T_i0 * u^alpha_T;   T_e(rho) = T_e0 * u^alpha_T
          n_D(rho) = n_T(rho) = n_D0 * u^alpha_n           (the fuel exponent)
          S(rho)   = u^(2 alpha_n) * sigv_dt(T_i(rho)) / sigv_dt(T_i0)
                     (the fusion-rate shape, S(0) = 1)
          n_He(rho) = n_He0 * S(rho)
                     -- Eq. A.5 applied pointwise with the particle-to-energy
                     confinement ratio uniform in rho ("helium ash profiles are
                     obtained using a fixed ratio of particle-to-energy
                     confinement time", raw PDF p. 9): the ash follows the
                     fusion-rate profile, scaled to the converged peak below.
                     NEVER a bound exponent -- the shape is computed from the
                     rule at every lever point, so it holds for any geometry
                     [OWNER 2026-09-05: "make sure this scales up for larger
                     stellarators"].
          n_e(rho) = n_D + n_T + 2 n_He = 2 n_D0 u^alpha_n + 2 n_He0 S(rho)
                     (quasi-neutrality pointwise; trace W at f_W ~ 1e-5
                     neglected in the charge sum; n_e(0) = n_e0, the lever)

        CHAIN (each stage an output; all evaluated at the same lever point):

          T_e0     = T_i0 / r_TiTe                                  [keV]
          I_line_n = integral_0^1 u^alpha_n d rho
          I_line_S = integral_0^1 S(rho) d rho
          I_W_S    = integral_0^1 S(rho) u^alpha_T 2 rho d rho   ( = <S u^alpha_T>_V )
          I_vol_S  = integral_0^1 S(rho) 2 rho d rho             ( = <S>_V )
          n_bar19  = (2 n_D0 I_line_n + 2 n_He0 I_line_S) / 1e19  [1e19 m^-3]
                     (line-averaged density of the DERIVED electron profile --
                     ISS04's n19 takes its "usual meaning"; the vol-av reading
                     misses the printed tau_E by -23%, goal learning L-001)
          ASH FIXED POINT (A.5/A.6, peak form, damped):
            n_D0 = n_T0 = (n_e0 - 2*n_He0) / 2      (quasi-neutrality at the peak)
            p_avg  = e_keV * ( 2 n_D0 (T_e0 + T_i0) / (1+alpha_n+alpha_T)
                             + n_He0 (2 T_e0 + T_i0) * I_W_S )          [Pa]
                     -- the ONE volume-averaged thermal pressure of the plant:
                     <n_e T_e + (n_D + n_T + n_He) T_i>_V over the derived
                     profiles; 'Volume-Averaged Beta' reads it (WI-042 D2)
            W_th   = 1.5e-6 * p_avg * V                                 [MJ]
                     (W = 3/2 <p>_V V, the sister code's definition: Lion 2021
                     Eqs. 8-11 / Lion 2023 Eqs. 2.10-2.13, thermal, species sum,
                     effective-radius element -- linked to this source by its
                     Appendix A ancestry, never cited as this source's own)
            tau_E  = (C * W_th^-0.61)^(1/0.39)                          [s]
                     C = 0.134*f_ren*a^2.28*B^0.84*iota_23^0.41
                         *n_bar19^0.54*R^0.64
                     (ISS04 Eq. A.7 with the source's own P = W/tau_E
                     substitution -- the closed form behind Eq. A.8; C is
                     re-evaluated at every iterate because n_bar19 now
                     depends on the ash, WI-042 D3)
            n_He0 <- f_suppr * tau_ratio * tau_E * n_D0*n_T0*sigv_dt(T_i0)
                     (Eq. A.5 helium balance x Eq. A.6 suppression; with tau*
                     uniform in rho the peak and the shape are one equation)
          DERIVED PROFILE DIAGNOSTICS (outputs; nothing downstream reads them):
            n_e_volav     = 2 n_D0 / (1+alpha_n) + 2 n_He0 I_vol_S      [m^-3]
            alpha_n_e_eff = n_e0 / n_e_volav - 1                        [1]
                     (the vol-av/peak relation <n>/n0 = 1/(1+alpha) that bound
                     the retired point-A exponent 0.596 from the printed pair
                     3.17/5.06; here derived, 0.5953 at point A)
            alpha_He_eff  = least-squares slope of ln S(rho_k) on ln u_k over
                     the 1,700 nodes rho_k = k/2000, k = 1..1700 (rho <= 0.85)
                     -- the ash shape's effective power-law exponent (4.05 at
                     point A; 4.7 at 10 keV, 3.5 at 20 keV: it moves with T_i0)
          RADIATION (composed; profile-integrated over the DERIVED n_e(rho)):
            p_brems = 5.35e-37 * Z_eff * V
                      * int n_e(rho)^2 * sqrt(T_e(rho)) dV'             [MW]
            p_line  = f_W * V * int n_e(rho)^2 * L_z_W(T_e(rho)) dV'    [MW]
                      (L_z_W: piecewise coronal cooling-curve fit)
            p_sync  = Albajar (2001) formula at kappa_sync, R_w_sync with the
                      density-profile parameter alpha_n_e_eff (WI-042 D4) [MW]
            p_rad   = p_brems + p_line + p_sync
          BALANCE (Eq. A.2/A.3):
            p_alpha_heat   = f_alpha * ash_frac * p_fus_internal          [MW]
                     p_fus_internal: the identical profile-integrated
                     Bosch-Hale evaluation as 'DT Fusion Power' at
                     (n_D0, n_T0, T_i0) -- same algorithm, same contract
            p_aux_required = p_rad + W_th/tau_E - p_alpha_heat            [MW]

        DORMANT (no-ash) CASE (WI-042 D6): an instance binding tau_ratio = 0
        or f_suppr = 0 converges to n_He0 = 0 at the first iterate; then
        n_e = 2 n_D0 u^alpha_n, every ash-weighted term vanishes, p_avg and
        W_th reduce to the fuel-only closed form Sigma_s n_s0 T_s0 /
        (1 + alpha_n + alpha_T), and alpha_n_e_eff = alpha_n. No switch.

        EXECUTABLE SEMANTIC (Rung B, WI-022 pattern): exp(), numerical
        integrals, and the damped fixed point route this calc to the
        handwritten codegen stage (manual_required); the generated handwritten
        impl is normative and is guarded bit-exact by the oracle.
        Discretization/convergence contract (mirrored exactly in the oracle):
        trapezoidal rule in rho over [0,1], N = 200,000 intervals for every
        profile integral (the fusion integral, I_line_n, I_line_S, I_W_S,
        I_vol_S, the radiation integrals), temperature floor 1e-6 keV,
        pure-Python float64; ash fixed point by damped half-step iteration
        n_He0 <- 0.5*(n_He0 + F(n_He0)) from n_He0 = 0, absolute tolerance
        1e12 m^-3, iteration cap 200; non-convergence, non-positive fuel
        density, or a non-finite intermediate RAISES -- fail loudly, never
        clamp (amended MR-WI037-2).

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
            (equations; every value image-verified -- the iter-01 AND iter-02
            text tables are corrupted, the raw PDF and page images govern);
            knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf
            (p. 9, p. 32 Appendix A, read from page renders -- WI-042);
            knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/
            (Lion et al. 2021, Eqs. 8-11: the W definition) and
            knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/
            (Lion 2023, Eqs. 2.10-2.13), both registered at d4059ef1;
            /home/reid/1cfe/1costingfe/src/costingfe/layers/radiation.py (pin 0254385);
            /home/reid/1cfe/1costingfe/src/costingfe/layers/reactivity.py (pin 0254385)
        **Ref**: images/page_031_eq_6.png (Eq. A.7 ISS04), page_031_eq_7.png
            (Eq. A.8, the P = W/tau_E rewriting this closed form reproduces);
            page_031_eq_1.png / page_031_eq_2.png (Eq. A.2/A.3 balance);
            page_031_eq_4.png / page_031_eq_5.png (Eq. A.5 helium balance,
            A.6 suppression); raw PDF p. 9 col. 2 ("Helium ash profiles are
            obtained using a fixed ratio of particle-to-energy confinement
            time") and p. 32 ("tau*_alpha = rho* tau_E, where we use rho* ~ 8"),
            the pointwise reading of A.5 (WI-042); iter-02 raw PDF appendix A
            text ("replace the heating power by the ratio of plasma energy
            divided by the energy confinement time"); radiation.py:260,275
            (bremsstrahlung 5.35e-37*Z_eff*n^2*sqrt(T)), radiation.py:83-96
            (W cooling-curve fit), radiation.py:180-241 (Albajar synchrotron,
            eqs 13/15 of Albajar 2001); reactivity.py:54-70 (Bosch-Hale
            sigv_dt); goal evidence work/orchestration/goals/
            stored-energy-basis/evidence/w_counterfactual/
            attribution_sourced_definition.json at 5cc30ac0 (the rule at the
            printed peaks reproduces n_e0 5.04 / <n_e> 3.16 vs printed
            5.06 / 3.17, W 524.5 MJ at the model's exponents; learnings
            L-002/L-003) and work/active/WI-042_sourced-helium-ash-profile/
            prototype/ (cross-checks at point A after WI-042: W +3.0 % vs the
            printed 504.65, <n_e> +0.1 %, p_fus -1.8 %, tau_E +6.6 %, n_He0
            +8 % -- the printed (W, tau_E) pair does not close the source's
            own balance, L-002; nothing tuned)
        **Basis**: steady-state 0D power balance over the source's own profile
            rules -- power-law fuel and temperature profiles, the ash on the
            fusion-rate profile (A.5 pointwise), electrons by quasi-neutrality
            -- with ISS04 confinement in the source's own closed form, the
            printed ash chain, and composed radiation; concept-agnostic (MR-3)
            -- machine values, levers, and quality facts bound by instances
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
        // fuel density profile exponent [1] (the ash and the electrons are
        // derived from it and the temperature profile, WI-042)
        in attribute alpha_n_in : Real;
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
        // line-averaged electron density of the derived profile [1e19 m^-3]
        out attribute n_bar19 : Real;
        // converged peak helium-ash density [m^-3]
        out attribute n_He0 : Real;
        // quasi-neutral peak deuterium density [m^-3]
        out attribute n_D0 : Real;
        // quasi-neutral peak tritium density [m^-3]
        out attribute n_T0 : Real;
        // peak electron temperature [keV] (= T_i0 / r_TiTe)
        out attribute T_e0 : Real;
        // stored thermal plasma energy [MJ] (= 1.5 p_avg V)
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
        // volume-averaged thermal pressure [Pa] -- the plant's one pressure
        // integral; 'Volume-Averaged Beta' reads it (WI-042)
        out attribute p_avg : Real;
        // volume-averaged electron density of the derived profile [m^-3] (WI-042)
        out attribute n_e_volav : Real;
        // effective electron density exponent n_e0 / n_e_volav - 1 [1] (WI-042)
        out attribute alpha_n_e_eff : Real;
        // effective helium-ash profile exponent of S(rho) [1], a diagnostic (WI-042)
        out attribute alpha_He_eff : Real;
    }
}
