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

        in attribute R : Real;
        in attribute a : Real;
        in attribute kappa : Real;

        // pi as a defaulted input (codegen-safe; no transcendental call).
        // Source: mathematical constant; matches jnp.pi in tokamak.py:174.
        in attribute pi : Real default 3.14159265358979;

        // Shape/packing factor. Default 1.0 = pure elongated torus (tokamak;
        // 1costingFE torus geometry). A shaped stellarator sets f_shape < 1.
        // Source: concept geometry; WI-020.
        in attribute f_shape : Real default 1.0;

        out attribute V : Real =
            2.0 * (pi ** 2) * R * (a ** 2) * kappa * f_shape;
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
        (owner Option 1, WI-021) — engineered annuli are sized by the radial
        build, not the plasma cross-section. ARIES/Starfire-lineage geometry,
        admissible per PROTOCOL.md section 3.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py
        **Ref**: geometry.py:67-81 (torus shell + surface area), 106-118
            (cumulative radii), 156-170 (per-layer volumes); model.py:1205-1208
            (CAS22 aggregation)
        **Basis**: forward radial build; torus branch; MFE-generic
        */

        in attribute R : Real;
        in attribute a : Real;           // minor radius = plasma_t
        in attribute kappa : Real;

        // pi as a defaulted input (codegen-safe; no transcendental call).
        in attribute pi : Real default 3.14159265358979;

        // Radial-build layer thicknesses [m], center -> outboard.
        // Source: geometry.py:19-40 (RadialBuild); concept overrides bind values.
        in attribute vacuum_t : Real;
        in attribute firstwall_t : Real;
        in attribute blanket_t : Real;
        in attribute reflector_t : Real;
        in attribute ht_shield_t : Real;
        in attribute structure_t : Real;
        in attribute gap1_t : Real;
        in attribute vessel_t : Real;
        in attribute coil_t : Real;
        in attribute gap2_t : Real;
        in attribute lt_shield_t : Real;

        // Cumulative radii from the plasma minor radius outward.
        attribute vacuum_or : Real = a + vacuum_t;
        attribute firstwall_or : Real = vacuum_or + firstwall_t;
        attribute blanket_or : Real = firstwall_or + blanket_t;
        attribute reflector_or : Real = blanket_or + reflector_t;
        attribute ht_shield_or : Real = reflector_or + ht_shield_t;
        attribute structure_or : Real = ht_shield_or + structure_t;
        attribute gap1_or : Real = structure_or + gap1_t;
        attribute vessel_or : Real = gap1_or + vessel_t;
        attribute coil_or : Real = vessel_or + coil_t;
        attribute gap2_or : Real = coil_or + gap2_t;
        attribute lt_shield_or : Real = gap2_or + lt_shield_t;

        // Torus-shell coefficient C = kappa * 2*pi^2 * R.
        attribute C : Real = kappa * 2.0 * (pi ** 2) * R;

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
        out attribute wall_area : Real = kappa * 4.0 * (pi ** 2) * R * vacuum_or;
        out attribute r_coil : Real = vessel_or;
    }

    calc def 'DT Fusion Power' {
        doc /*
        D-T fusion power [MW] from density, reactivity, and plasma volume.

          P_fus = (1/4) * n_e^2 * <sigma*v> * E_fus * V * 1e-6   [W -> MW]

        The factor 1/4 = n_D*n_T / n_e^2 for a 50/50 D-T mix. Reactivity
        <sigma*v> enters as the input `sigma_v` [m^3/s] — the Bosch-Hale
        temperature fit is NOT reproduced here (it needs exp(), outside the
        codegen envelope). E_fus is the per-event D-T fusion energy in Joules
        (an input; = 17.58 MeV * 1.602176634e-13 J/MeV in the source).

        Fusion power rises with n_e and with V (hence with R via 'Plasma
        Geometry'), satisfying SV-017. Density and reactivity are inputs;
        the machine -> density closure is a downstream design-layer concern.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py
        **Ref**: tokamak.py:102-114 (compute_fusion_power)
        **Basis**: Standard 0D D-T fusion power; MFE-generic
        */

        in attribute n_e : Real;
        in attribute sigma_v : Real;
        in attribute E_fus : Real;
        in attribute V : Real;

        // 0.25 = n_D*n_T/n_e^2 for 50/50 DT (tokamak.py:114).
        // 1.0e-6 = W -> MW (tokamak.py:114).
        out attribute p_fus : Real =
            0.25 * (n_e ** 2) * sigma_v * E_fus * V * 1.0e-6;
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

        // Charged-particle (ash) fraction of D-T fusion energy. Source:
        // physics.py:31 (3.52/17.58 = 0.2002). Defaulted; a concept overrides
        // it for a non-D-T fuel.
        in attribute ash_frac : Real default 0.2002;

        in attribute wall_area : Real;

        out attribute wall_load : Real =
            p_fus * (1.0 - ash_frac) / wall_area;
    }
}
