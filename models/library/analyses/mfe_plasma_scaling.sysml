package mfe_plasma_scaling {
    private import ScalarValues::*;

    calc def 'Plasma Geometry' {
        doc /*
        Plasma volume of an elongated torus [m^3].

          V = 2 * pi^2 * R * a^2 * kappa

        Concept-agnostic geometry: applies to any toroidal MFE plasma
        (tokamak or stellarator). R is major radius, a is minor radius,
        kappa is elongation.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py
        **Ref**: tokamak.py:172-174 (_plasma_volume)
        **Basis**: Standard elongated-torus volume; MFE-generic
        */

        in attribute R : Real;
        in attribute a : Real;
        in attribute kappa : Real;

        // pi as a defaulted input (codegen-safe; no transcendental call).
        // Source: mathematical constant; matches jnp.pi in tokamak.py:174.
        in attribute pi : Real default 3.14159265358979;

        out attribute V : Real =
            2.0 * (pi ** 2) * R * (a ** 2) * kappa;
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
