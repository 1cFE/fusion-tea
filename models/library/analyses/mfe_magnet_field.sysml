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

    calc def 'Winding Pack Sizing' {
        doc /*
        Winding-pack cross-section side [m] from the current the pack must
        carry (WI-036, D1):

          wp_side = sqrt(I_coil / j_wp) / 1000

        The pack is sized by its current at a chosen winding-pack current
        density, not held while current varies. The relation is the one the
        source's own coil set satisfies: across all six unique Stellaris
        coils, j_wp * side^2 reproduces the printed total amp-turns to
        better than 1% (-0.58% .. +0.52%). j_wp is the design lever -- the
        source varies it 112..124 A/mm^2 across its coil set -- and is bound
        per instance as the float64 that reproduces the printed pair exactly.

        Unit note: j_wp is in A/mm^2 and I_coil in A, so I_coil/j_wp is an
        area in mm^2; the 1000 divisor converts the side to metres.

        Consequence for the paired stress calc: substituting gives
        sigma_wp = k_sigma * B_peak * sqrt(I_coil * j_wp), so winding stress
        grows as the square root of coil current rather than linearly once
        the pack is allowed to size itself.

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: images/page_022_table_0.png (Table 8: I total amp-turns
            15.4/14.6/13.8/12.9/12.5/11.2 MA; j_WP 119/112/120/112/122/124
            A/mm^2; cross-section side 360/360/340/340/320/300 mm --
            image-verified; the markdown extraction of this table is garbled)
        **Basis**: winding-pack area = coil current / winding-pack current
            density; concept-agnostic (MR-3) -- all values bound by instances
        */

        // peak single-coil current [A]
        in attribute I_coil : Real;
        // winding-pack current density [A/mm^2] -- the design lever
        in attribute j_wp : Real;

        out attribute wp_side : Real = (I_coil / j_wp) ** 0.5 / 1000.0;
    }

    calc def 'Coil Winding Length' {
        doc /*
        Typical coil winding circumference [m] from machine scale (WI-036, D3):

          c_coil = k_coil * R0

        Winding length is the sole length term in the magnet conductor cost,
        and was previously a held printed constant that did not respond to
        machine size. Per-coil circumferences are unprinted, so what the
        source supports is a held *shape* factor with the *scale* responding
        -- the trade the WI-036 mint record predicted ("one held constant
        traded for a smaller one"). k_coil is the residual held quantity and
        is named rather than buried.

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: raw.pdf sec. 2.9 ("typical circumference of 25 m"; coils
            approximately 7 x 5 x 10 m); images/page_002_table_0.png
            (Table 2: major radius 12.7 m)
        **Basis**: coil circumference scales with major radius at a held
            coil-shape factor; concept-agnostic (MR-3)
        */

        // major radius [m]
        in attribute R0 : Real;
        // coil-shape factor [1] = typical circumference / major radius
        in attribute k_coil : Real;

        out attribute c_coil : Real = k_coil * R0;
    }

    calc def 'Winding Pack Cold Volume' {
        doc /*
        Total winding-pack cold volume [m^3] across the coil set
        (WI-036, D2):

          vol_cold_total = f_wp_vol * n_coils * wp_side^2 * c_coil + vol_extra

        vol_extra is additional cold volume beyond the winding pack, kept as a
        live settable slot so that modelling the winding-pack chain does not
        retire the instance's cold-volume input (WI-032 owner ruling); it is
        zero for a machine whose printed cold mass is the winding pack.

        The model carries one winding pack (the worst coil) while the machine
        has six unique cross-sections. f_wp_vol is a held set-distribution
        fact -- the ratio of the printed total volume to the worst-coil-uniform
        reference -- exactly the shape of the existing f_set coil-current
        distribution fact. This moves the six-cross-section arithmetic out of
        an instance doc comment and into model content, and gives a wider
        winding pack a real cold-mass consequence through the cryoplant chain.

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: images/page_022_table_0.png (Table 8: cross-section side
            lengths 360/360/340/340/320/300 mm, image-verified); raw.pdf
            sec. 2.9 (48 coils = 4 periods x 12, so 8 occurrences of each of
            six unique coils; typical circumference 25 m)
        **Basis**: sum of per-coil winding-pack volumes expressed as a held
            distribution factor on the worst coil; concept-agnostic (MR-3)
        */

        // number of field coils [1]
        in attribute n_coils : Real;
        // winding-pack cross-section side, worst coil [m]
        in attribute wp_side : Real;
        // typical winding circumference [m]
        in attribute c_coil : Real;
        // winding-pack set-distribution factor [1]
        in attribute f_wp_vol : Real;
        // additional cold volume beyond the winding pack [m^3]
        in attribute vol_extra : Real default 0.0;

        out attribute vol_cold_total : Real = f_wp_vol * n_coils * wp_side * wp_side * c_coil + vol_extra;
    }

    calc def 'Conductor Strain' {
        doc /*
        Strain in the HTS tape stack [1] (WI-036, D4):

          eps_cond = f_cond * sigma_wp / E_wp

        The conductor is checked separately from the structure because every
        surveyed HTS fusion design -- the Stellaris source included -- runs
        two checks, a stress check against the structure and a strain check
        against the conductor, and this model previously ran only the first.
        REBCO is brittle; its performance is governed by strain.

        f_cond is a load-sharing factor calibrated from the source's own
        reported pair: the winding pack peaks at ~600 MPa von Mises while the
        HTS stack strain stays below 0.2%, so the stack sees about two-thirds
        of the pack-average strain -- the soldered Cu jacket offloads it.
        Both anchors are printed *bounds* taken as values, so the operand
        over-estimates strain; that conservatism is disclosed, not corrected.

        Honest limit: von Mises is not uniaxial stress and a pack-level stress
        is not local tape stress. This is a composition standing in for a
        finite-element result the source does not publish, calibrated from the
        source's own numbers rather than assumed (the k_sigma convention
        applied to a second quantity).

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
            knowledge/sources/electro_mechanical_properties_of_rebco_coated_conductors/
        **Ref**: raw.pdf p. 24 (winding-pack peak von Mises ~600 MPa; HTS
            stack peak strain below 0.2% "within acceptable limits, even when
            adding strain from bending"); output.md:173,197 (Barth, Mondonico
            & Senatore 2015: irreversible strain by manufacturer at 4.2 K/19 T,
            SuperOx 0.45-0.47% the lowest of five; "Remaining below 0.4%
            strain, there are no discernible differences")
        **Basis**: pack-average strain scaled by a sourced load-sharing
            factor; concept-agnostic (MR-3)
        */

        // winding-pack stress [Pa]
        in attribute sigma_wp : Real;
        // winding-pack effective elastic modulus [Pa]
        in attribute E_wp : Real;
        // conductor load-sharing factor [1] (stack strain / pack-average strain)
        in attribute f_cond : Real;

        out attribute eps_cond : Real = f_cond * sigma_wp / E_wp;
    }
}
