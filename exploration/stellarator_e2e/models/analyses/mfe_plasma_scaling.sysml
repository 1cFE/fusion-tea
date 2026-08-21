package mfe_plasma_scaling {
    private import ScalarValues::*;

    calc def 'Plasma Geometry' {
        doc /*
        Plasma volume [m^3].

          V = 2 * pi^2 * R * a^2 * kappa * f_shape

        The elongated-torus term (2*pi^2*R*a^2*kappa) is the smooth-torus
        volume. f_shape is a dimensionless shape/packing factor: 1.0 for a pure
        torus (tokamak, and the 1costingFE torus geometry), < 1 for a shaped
        stellarator plasma whose twisted, non-circular cross-section encloses
        less volume than the torus of the same R, a, kappa. Concept-agnostic:
        R is major radius, a is minor radius, kappa is elongation, and the
        concept sets f_shape (default 1.0 leaves any existing torus consumer
        and the Anchor A handshake unchanged).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py
        **Ref**: tokamak.py:172-174 (_plasma_volume, the f_shape = 1.0 torus term)
        **Basis**: elongated-torus volume with a concept shape factor; MFE-generic
        */

        in attribute R_in : Real;
        in attribute a_in : Real;
        in attribute kappa_in : Real;

        // Shape/packing factor. Default 1.0 = pure elongated torus (tokamak;
        // 1costingFE torus geometry). A shaped stellarator sets f_shape < 1.
        // Source: concept geometry; WI-020.
        in attribute f_shape_in : Real default 1.0;

        // pi as a defaulted input (codegen-safe; no transcendental call).
        // Source: mathematical constant; matches jnp.pi in tokamak.py:174.
        // Declared last: a usage binds the formals above by name and leaves pi
        // at its default; the exact route lays formals out positionally, so a
        // skipped default must not precede a bound formal (migration ledger).
        in attribute pi : Real default 3.14159265358979;

        out attribute V : Real =
            2.0 * (pi ** 2) * R_in * (a_in ** 2) * kappa_in * f_shape_in;
    }

    calc def 'MFE Radial Build' {
        doc /*
        Forward radial build [m, m^2, m^3] for an MFE torus: cumulative layer
        radii from the plasma minor radius outward, then torus-shell volumes and
        the first-wall surface area.

          or_i      = or_{i-1} + t_i                              (cumulative radii)
          layer_vol = kappa * 2*pi^2 * R * (or_out^2 - or_in^2)   (torus shell)
          wall_area = kappa * 4*pi^2 * R * vacuum_or              (first-wall SA)

        Aggregates match 1costingFE's CAS22 grouping (model.py:1205-1208):
        blanket = firstwall+blanket+reflector; shield = ht+lt; structure; vessel.
        Concept-agnostic: R major radius, a minor radius (= plasma_t), kappa
        elongation, per-layer thicknesses. Pure torus shells, no shape factor
        (owner Option 1, WI-021) -- engineered annuli are sized by the radial
        build, not the plasma cross-section. ARIES/Starfire-lineage geometry,
        admissible per PROTOCOL.md section 3.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py
        **Ref**: geometry.py:67-81 (torus shell + surface area), 106-118
            (cumulative radii), 156-170 (per-layer volumes); model.py:1205-1208
            (CAS22 aggregation)
        **Basis**: forward radial build; torus branch; MFE-generic
        */

        in attribute R_in : Real;
        // minor radius = plasma_t
        in attribute a_in : Real;
        in attribute kappa_in : Real;

        // Radial-build layer thicknesses [m], center -> outboard.
        // Source: geometry.py:19-40 (RadialBuild); concept overrides bind values.
        in attribute vacuum_t_in : Real;
        in attribute firstwall_t_in : Real;
        in attribute blanket_t_in : Real;
        in attribute reflector_t_in : Real;
        in attribute ht_shield_t_in : Real;
        in attribute structure_t_in : Real;
        in attribute gap1_t_in : Real;
        in attribute vessel_t_in : Real;
        in attribute coil_t_in : Real;
        in attribute gap2_t_in : Real;
        in attribute lt_shield_t_in : Real;

        // pi as a defaulted input (codegen-safe; no transcendental call).
        // Declared last: usages bind the formals above by name and leave pi at
        // its default; a skipped default must not precede a bound formal on the
        // exact route (migration ledger).
        in attribute pi : Real default 3.14159265358979;

        // Cumulative radii from the plasma minor radius outward.
        attribute vacuum_or : Real = a_in + vacuum_t_in;
        attribute firstwall_or : Real = vacuum_or + firstwall_t_in;
        attribute blanket_or : Real = firstwall_or + blanket_t_in;
        attribute reflector_or : Real = blanket_or + reflector_t_in;
        attribute ht_shield_or : Real = reflector_or + ht_shield_t_in;
        attribute structure_or : Real = ht_shield_or + structure_t_in;
        attribute gap1_or : Real = structure_or + gap1_t_in;
        attribute vessel_or : Real = gap1_or + vessel_t_in;
        attribute coil_or : Real = vessel_or + coil_t_in;
        attribute gap2_or : Real = coil_or + gap2_t_in;
        attribute lt_shield_or : Real = gap2_or + lt_shield_t_in;

        // Torus-shell coefficient C = kappa * 2*pi^2 * R.
        attribute C : Real = kappa_in * 2.0 * (pi ** 2) * R_in;

        // Per-layer torus-shell volumes.
        attribute firstwall_vol : Real = C * ((firstwall_or ** 2) - (vacuum_or ** 2));
        attribute blanket_layer_vol : Real = C * ((blanket_or ** 2) - (firstwall_or ** 2));
        attribute reflector_vol : Real = C * ((reflector_or ** 2) - (blanket_or ** 2));
        attribute ht_shield_vol : Real = C * ((ht_shield_or ** 2) - (reflector_or ** 2));
        attribute lt_shield_vol : Real = C * ((lt_shield_or ** 2) - (gap2_or ** 2));

        // CAS22 aggregate volumes [m^3].
        out attribute blanket_vol : Real =
            firstwall_vol + blanket_layer_vol + reflector_vol;
        out attribute shield_vol : Real = ht_shield_vol + lt_shield_vol;
        out attribute structure_vol : Real =
            C * ((structure_or ** 2) - (ht_shield_or ** 2));
        out attribute vessel_vol : Real =
            C * ((vessel_or ** 2) - (gap1_or ** 2));

        // First-wall area [m^2] (standoff radius vacuum_or, not a) and
        // coil-bore radius [m] = vessel outer radius.
        out attribute wall_area : Real = kappa_in * 4.0 * (pi ** 2) * R_in * vacuum_or;
        out attribute r_coil : Real = vessel_or;
    }

    calc def 'DT Fusion Power' {
        doc /*
        D-T fusion power [MW] -- 0D bypass or profile-integrated (WI-022).

        MODE (bypass rule, selected by sigma_v alone):
          sigma_v > 0  ->  0D form (exact legacy contract):
              p_fus = 0.25 * n_e^2 * sigma_v * E_fus * V * 1e-6   [W -> MW]
          sigma_v = 0 (default)  ->  profile-integrated form:
              p_fus = n_D0 * n_T0 * I * E_fus * V * 1e-6
              I = integral_0^1  u^(2*alpha_n) * sigv_dt(T_i0 * u^alpha_T) du
          with u = 1 - rho^2 (dV/V = 2*rho*d(rho), so the rho-integral of the
          profile product reduces to the u-integral above), profiles
          n(rho) = n0*(1-rho^2)^alpha_n and T(rho) = T0*(1-rho^2)^alpha_T
          (Stellaris Eqs. 2-3, image-verified). The fuel term is n_D*n_T with
          the *diluted peak fuel densities* -- NOT 0.25*n_e^2, which would
          double-count helium ash and impurities. If sigma_v > 0 and profile
          inputs are also bound, the bypass wins.

        EXECUTABLE SEMANTIC (Rung B, WI-022): the Bosch-Hale curve needs
        exp(), so this calc is routed to the handwritten codegen stage
        (manual_required); the generated handwritten impl is normative and is
        guarded bit-exact by the oracle (verify_stellaris.py). Discretization
        contract for the impl and oracle: trapezoidal rule in rho over [0,1],
        N = 200,000 intervals, temperature floor 1e-6 keV, pure-Python
        float64. The intermediates below state the Bosch-Hale evaluation at
        T_i0 (sigv_peak) in the model itself; e^x is written as e ** x
        because the KerML standard library has sqrt but no exp.

        Fusion power rises with n_e / the fuel densities and with V (hence
        with R via 'Plasma Geometry'), satisfying SV-017. Densities,
        temperature, and exponents are inputs; the machine -> profile closure
        (ISS04 confinement solve) is out of scope (Rung C).

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py;
            /home/reid/1cfe/1costingfe/src/costingfe/layers/reactivity.py
        **Ref**: tokamak.py:102-114 (compute_fusion_power, the 0D bypass
            form); reactivity.py:54-70 (sigv_dt Bosch-Hale D-T coefficients);
            knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/
            stellaris-design-details/images/page_007_eq_0.png and
            page_007_eq_1.png (Eqs. 2-3 profile forms, image-verified);
            stellaris-design-details.md Appendix A line 2912 (the source's own
            0.5D volume-integrated power balance this reproduces)
        **Basis**: profile-integrated D-T fusion power over (1-rho^2)^alpha
            profiles with an exact 0D bypass; MFE-generic (flat/0D concepts
            bind sigma_v > 0 and ignore the profile inputs)

        EXACT-ROUTE FORM (stellarator-model-migration, 2026-08-21; Class B,
        marked for revert -- see models/stellarator_migration_ledger.md): the
        pinned codegen admits no function invocation in an executable
        expression, so the model-resident Bosch-Hale peak statement that used
        to sit in the body is carried here verbatim and the output is declared
        without an expression (a manual interface; the handwritten impl above
        is the executable meaning either way):
          theta     = T_i0 / (1 - T_i0*(1.51361e-2 + T_i0*(4.60643e-3 + T_i0*-1.06750e-4))
                             / (1 + T_i0*(7.51886e-2 + T_i0*(1.35000e-2 + T_i0*1.36600e-5))))
          xi        = ((34.3827^2) / (4*theta))^(1/3)
          sigv_peak = 1.17302e-9 * theta * sqrt(xi / (1124656 * T_i0^3)) * e^(-3*xi) * 1e-6
          p_fus     = n_D0 * n_T0 * sigv_peak * E_fus * V * 1e-6     (peak-form statement)
        */

        // vol-avg electron density [m^-3] (0D path only)
        in attribute n_e_in : Real;
        // 0D-effective reactivity [m^3/s]; > 0 selects the 0D bypass
        in attribute sigma_v_in : Real default 0.0;
        // per-event D-T fusion energy [J]
        in attribute E_fus_in : Real;
        // plasma volume [m^3]
        in attribute V : Real;

        // Profile inputs (WI-022). Inert on the 0D bypass path. T_i0 defaults
        // to 1.0 (not 0) so the dormant Bosch-Hale intermediates below stay
        // numerically defined; the mode is selected by sigma_v, never by T_i0.
        // peak deuterium density [m^-3]
        in attribute n_D0_in : Real default 0.0;
        // peak tritium density [m^-3]
        in attribute n_T0_in : Real default 0.0;
        // peak ion temperature [keV]
        in attribute T_i0_in : Real default 1.0;
        // density profile exponent
        in attribute alpha_n_in : Real default 0.0;
        // temperature profile exponent
        in attribute alpha_T_in : Real default 0.0;

        // Manual interface on the exact route (see EXACT-ROUTE FORM in the doc):
        // the handwritten impl computes the doc-specified bypass/integral
        // semantic and is the executable meaning (guarded by the oracle).
        out attribute p_fus : Real;
    }

    calc def 'Neutron Wall Load' {
        doc /*
        First-wall neutron wall load [MW/m^2] from fusion power and wall area.

          wall_load = p_fus * (1 - ash_frac) / wall_area

        The neutron power is the fusion power times the neutron energy fraction
        (1 - ash_frac). ash_frac is the charged-particle (alpha/ash) share of the
        D-T fusion energy: 0.2002 = E_alpha / Q = 3.52 MeV / 17.58 MeV. wall_load
        is the neutron power divided by the load-bearing wall area, the standard
        first-wall damage/lifetime driver. Concept-agnostic: any MFE first wall.

        This makes neutron wall load forward-computable from the power balance
        (p_fus) and the plasma/first-wall geometry (wall_area), so the viability
        'Neutron Wall Load Limit' can be checked without an injected value.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py
        **Ref**: physics.py:31 (E_ALPHA_DT=3.52, Q_DT=17.58), physics.py:177-179
            (ash_frac = (E_total-E_neutron)/E_total; p_neutron = p_fus*(1-ash_frac))
        **Basis**: Neutron wall load = neutron power / wall area; MFE-generic
        */

        in attribute p_fus : Real;
        in attribute wall_area : Real;

        // Charged-particle (ash) fraction of D-T fusion energy. Source:
        // physics.py:31 (3.52/17.58 = 0.2002). Defaulted; a concept overrides
        // it for a non-D-T fuel. Declared last: usages bind p_fus and wall_area
        // by name and leave this at its default; a skipped default must not
        // precede a bound formal on the exact route (migration ledger).
        in attribute ash_frac_in : Real default 0.2002;

        out attribute wall_load : Real =
            p_fus * (1.0 - ash_frac_in) / wall_area;
    }
}
