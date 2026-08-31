package mfe_magnet_field {
    private import ScalarValues::*;

    calc def 'Coil Set Axis Field' {
        doc /*
        Axis-averaged on-axis field [T] from the coil set's current and
        geometry (WI-035, inversion ruling 2026-08-30):

          B_axis = mu0 * k_link * n_coils * I_coil / (two_pi * R0)

        k_link is a held coil-set transfer fact (float64 of the printed set),
        bundling two printed facts: the per-coil current distribution
        (set mean / peak = 643.2/739.2 = 0.870, Table 8 image) and the
        axis-linkage of the total (571.5/643.2 = 0.888) -- the modular-coil
        shaping current that does not link the magnetic axis (WI-032:
        Ampere's law on axis is a lower bound for modular QI coils). At the
        Stellaris design set (48 coils, 15.4 MA, R0 12.7 m) the computed
        B_axis is 9.0 T minus one ulp; no float64 k_link reproduces 9.0
        exactly (+/-6-ulp search), and the low side is bound deliberately so
        the conductor-ceiling verdict cannot flip on rounding.

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
            work/completed/20260827_WI-032_cold-volume-basis/spec.md
        **Ref**: images/page_002_table_0.png (Table 2: axis av. field 9.0 T,
            peak coil current 15.4 MA, 48 coils, R 12.7 m);
            images/page_022_table_0.png (Table 8: per-coil ampere-turns);
            WI-032 spec sec. "What G is" (the linkage decomposition)
        **Basis**: Ampere's law on the axis with a held, sourced coil-set
            linkage fact; concept-agnostic (MR-3) -- all values bound by instances
        */

        // number of field coils [1]
        in attribute n_coils : Real;
        // peak single-coil current [A]
        in attribute I_coil : Real;
        // coil-set transfer fact [1] (set distribution x axis linkage)
        in attribute k_link : Real;
        // major radius [m]
        in attribute R0 : Real;
        // vacuum permeability [T*m/A]. Source: cas22.py:92 (_MU0 = 4*pi*1e-7).
        in attribute mu0 : Real default 1.25663706212e-6;
        // 2*pi as float64
        in attribute two_pi : Real default 6.283185307179586;

        out attribute B_axis : Real = mu0 * k_link * n_coils * I_coil / (two_pi * R0);
    }

    calc def 'Winding Pack Stress' {
        doc /*
        Mean winding-pack stress scale [Pa] in the J x B x d form (WI-035):

          sigma_wp = k_sigma * I_coil * B_peak_in / wp_side

        Force density (current x field) over the load-bearing dimension --
        the standard mean-stress scale for a winding. k_sigma is a held
        coil-set structural concentration fact (float64 anchored at the
        printed worst-coil pair: <650 MPa at I 15.4 MA, B_peak 24.9 T,
        side 0.36 m; the printed "<650" bound is taken AS the value,
        conservative). The operand responds as I * B_peak / side --
        quadratic in coil current once B_peak follows the derived field --
        so the paired limit pushes back on both field choice and winding-pack
        sizing (rubric Row 3 P3).

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: images/page_022_table_0.png (Table 8: "Peak stress on WP
            [MPa] <650"; I, side lengths); raw.pdf sec. 2.9 structural
            analysis (peak stresses ~600 MPa, axisymmetric I x B model)
        **Basis**: J x B x d mean-stress scale with a held, sourced
            concentration fact; concept-agnostic (MR-3)
        */

        // peak single-coil current [A]
        in attribute I_coil : Real;
        // peak field on the winding [T]
        in attribute B_peak_in : Real;
        // winding-pack cross-section side, worst coil [m]
        in attribute wp_side : Real;
        // stress concentration transfer fact [1] (coil-set structural fact)
        in attribute k_sigma : Real;

        out attribute sigma_wp : Real = k_sigma * I_coil * B_peak_in / wp_side;
    }
}
