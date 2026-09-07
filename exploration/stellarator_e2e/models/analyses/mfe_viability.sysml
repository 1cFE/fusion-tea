package mfe_viability {
    private import ScalarValues::*;

    constraint def 'Net Power Positive' {
        doc /*
        Hard physics bound: the plant must produce positive net electric power
        (equivalently engineering Q > 1, recirculating fraction < 1). A design
        that fails this consumes more power than it generates and is not a power
        plant at all.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/validation.py
        **Ref**: validation.py:500-505 (p_net non-positive check)
        **Basis**: Net electric > 0 is the unambiguous physics viability floor
        */

        in attribute net_electric : Real;

        net_electric > 0.0
    }

    constraint def 'Economic Recirculating Threshold' {
        doc /*
        Economic viability knee: the recirculating power fraction should stay at
        or below a threshold (default 0.5). Above ~0.5, parasitic power load is
        excessive and the plant's economics deteriorate sharply. The threshold
        is an adjustable, documented parameter (not a hard physics bound) — the
        default matches the 1costingFE "excessive parasitic power load" warning.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/validation.py
        **Ref**: validation.py:512-515 (rec_frac > 0.5 excessive-parasitic knee)
        **Basis**: DI-001-analogue for MFE — recirculating fraction knee at 0.5
        */

        in attribute rec_frac : Real;
        in attribute threshold : Real default 0.5;

        rec_frac <= threshold
    }

    constraint def 'Beta Limit' {
        doc /*
        Plasma stability bound: the volume-averaged plasma pressure ratio (beta)
        must stay at or below the configuration's beta limit. Above it the plasma
        loses MHD equilibrium/stability. For a stellarator the limit is the
        configuration's design/optimization target (Stellaris: <beta>_V = 5% at
        which the QI equilibrium and coils were optimized); the operating point
        must sit at or below it.

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: line 273 (coils + boundary optimized at targeted <beta>_V = 5%)
        **Basis**: MHD beta limit — operating beta must not exceed the design beta
        */

        in attribute beta_in : Real;
        in attribute beta_limit_in : Real;

        beta_in <= beta_limit_in
    }

    constraint def 'Neutron Wall Load Limit' {
        doc /*
        First-wall peak-load bound: the PEAK neutron wall load [MW/m^2] must stay
        at or below the first-wall design limit, which is itself a peak on the
        same wall basis. Excessive neutron flux drives displacement damage (DPA)
        and shortens the first-wall replacement interval below viability; the
        source and its cited method set that lifetime by the peak load. Pair
        with 'Neutron Wall Load Peak' (mfe_plasma_scaling): the forward-computed
        circular-torus average put on the source's peak basis by a source-
        anchored calibration (WI-041). Comparing the AVERAGE with a peak limit,
        as the model did before WI-041, compares two different quantities.

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: Table 2 image (images/page_002_table_0.png: peak neutron wall load 4.05 MW/m^2); Table 6 image (images/page_020_table_0.png: peak DPA 10.7 DPA/FPY -> first-wall lifetime ~4-6 FPY); lines 1757-1766 and 1811-1813 (DPA-limited first-wall lifetime)
        **Basis**: Peak neutron wall load must not exceed the first-wall peak design limit
        */

        in attribute wall_load : Real;
        in attribute wall_load_limit_in : Real;

        wall_load <= wall_load_limit_in
    }

    constraint def 'TBR Floor' {
        doc /*
        Tritium self-sufficiency bound: the tritium breeding ratio (TBR) must be
        at or above a floor (typically ~1.05) so the plant breeds enough tritium
        to refuel itself plus margin for losses, decay, and startup inventory.
        Below the floor the D-T fuel cycle is not self-sustaining.

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: line 1530 (TBR > 1.05 target), line 1659 (achieved TBR 1.074)
        **Basis**: D-T tritium self-sufficiency floor
        */

        in attribute tbr_in : Real;
        in attribute tbr_floor_in : Real;

        tbr_in >= tbr_floor_in
    }

    constraint def 'Conductor Peak Field Limit' {
        doc /*
        Conductor-technology bound: the peak field on the winding pack must not
        exceed the conductor's field ceiling. Above it the superconductor cannot
        carry the design current (REBCO ~23 T engineering ceiling, Nb3Sn ~13 T,
        NbTi ~9 T per 1costingFE's MAGNET_TABLE). Pair with 'Conductor Peak
        Field' (mfe_plasma_scaling), which forward-computes B_peak from the
        axis field and the coil set's peak/axis ratio. B_max is bound per
        instance and is the technology lever of a magnet A/B.

        **Source**: /home/reid/1cfe/1costingfe/src/costingfe/defaults.py (pin 0254385);
            knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: defaults.py:605-614 (MAGNET_TABLE b_max: rebco_hts 23.0, nb3sn 13.0,
            nbti 9.0, "engineering ceilings"); images/page_002_table_0.png (Table 2:
            24.9 T peak conductor field, the Stellaris design value)
        **Basis**: peak field on the conductor <= conductor ceiling
        */

        // peak field on the conductor [T]
        in attribute B_peak : Real;
        // conductor peak-field ceiling [T]
        in attribute B_max_in : Real;

        B_peak <= B_max_in
    }

    constraint def 'Conductor Strain Limit' {
        doc /*
        Conductor bound (WI-036): the strain in the HTS tape stack must not
        exceed the conductor's strain limit. This is a SECOND check, distinct
        from 'Winding Pack Stress Limit', because the structure and the
        conductor fail in different ways at different limits -- every surveyed
        HTS fusion design, including the Stellaris source itself, performs
        both, and this model previously performed only the structural one.
        REBCO is brittle and its performance is governed by strain.

        Pair with 'Conductor Strain' (mfe_magnet_field), which forward-computes
        the operand from the winding-pack stress, the pack's effective modulus,
        and a sourced load-sharing factor -- a computed operand against a held
        sourced limit.

        The limit is bound per instance and is settable, because the band
        practitioners enforce spans 0.2% to 0.4%: measurements show no
        discernible strain effect below 0.4%, while the weakest measured
        commercial tape reaches its irreversible limit at 0.45%, and some
        projects choose 0.2% for margin.

        NAMED GAP, declared rather than valued (MR-WI036-7): REBCO's mechanical
        limit is strongly anisotropic and this constraint covers only the axial
        direction. Through-thickness tension delaminates the tape stack at
        about 3.6 MPa -- two orders of magnitude below the axial limit -- and
        transverse compression is limited to roughly 200 MPa on bare tape.
        This model computes no through-thickness or transverse stress, so it
        asserts no such constraint and must not be read as checking one.

        **Source**: knowledge/sources/electro_mechanical_properties_of_rebco_coated_conductors/;
            knowledge/sources/conceptual_design_of_hts_magnets_for_fusion_nuclear_science/;
            knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: output.md:173,197 (irreversible strain by manufacturer at
            4.2 K/19 T: Bruker 0.70-0.72%, SuNAM 0.67-0.69%, SuperPower
            0.66-0.68%, Fujikura 0.55-0.57%, SuperOx 0.45-0.47%; "Remaining
            below 0.4% strain, there are no discernible differences");
            Zhai et al. FNSF (transverse load limit ~200 MPa on the tape);
            raw.pdf p. 24 (Stellaris HTS stack strain below 0.2%)
        **Basis**: axial conductor strain <= irreversible strain limit
        */

        // strain in the HTS tape stack [1]
        in attribute eps_cond : Real;
        // conductor strain limit [1]
        in attribute eps_cond_allow_in : Real;

        eps_cond <= eps_cond_allow_in
    }

    constraint def 'Winding Pack Stress Limit' {
        doc /*
        Structural bound (WI-035): the computed winding-pack stress must not
        exceed the structural allowable. Pair with 'Winding Pack Stress'
        (mfe_magnet_field), which forward-computes the operand from coil
        current, the derived peak field, and the winding-pack side -- a
        computed operand against a held sourced limit (the ladder working,
        grading note G6), unlike the retired held-vs-held pattern.

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: raw.pdf sec. 2.10 (design stress limit 800 MPa for cryogenic
            AISI 316LN, von Mises as membrane+bending proxy, ASME BPVC VIII-2 /
            Eurocode framing; Fig. 49 caption); sec. 2.9 (WP peak ~600-650 MPa,
            "well below the imposed stress limit of 800 MPa")
        **Basis**: winding-pack stress <= structural design allowable
        */

        // computed winding-pack stress [Pa]
        in attribute sigma_in : Real;
        // structural allowable stress [Pa]
        in attribute sigma_allow_in : Real;

        sigma_in <= sigma_allow_in
    }

    constraint def 'Sustainment Limit' {
        doc /*
        Operating-point power bound (WI-037): the required sustained
        plasma-coupled heating computed by 'Plasma Sustainment'
        (mfe_plasma_sustainment) must not exceed the installed plasma-coupled
        heating power. A fully computed operand -- it responds to field
        (~B^-2.15 through the ISS04 closed form), heating, density,
        temperature, and geometry -- against a held sourced installed power:
        the rubric Row 1 P3 anchor's power-limit pushback, and the structural
        close of the field-never-rewarded pathology (discovery row
        20260823-magnet-technology-ab#4).

        What the installed side IS (WI-043; goal burn-control): Table 2's
        "Required plasma-coupled ECRH power 50" is what the source installs to
        REACH its design point along a start-up path ("about 50 MW of auxiliary
        heating power would need to be installed to reach the desired operation
        point", raw PDF p. 9); the design point itself runs IGNITED, with fusion
        gain infinity and 0 MW of auxiliary power at the operation point
        (Table 5, raw PDF p. 10). This limit reads the number in the source's
        point-B sense -- a DRIVEN operating point held under the installed
        heating (point B: fusion gain 182 at 14.77 MW) -- and says nothing about
        reaching the point from cold: the access requirement is not modelled
        (goal burn-control, goal.md section Limits). The installed side is not
        moved by that reading. Pair with 'Burn Hold' (below) for the lower half
        of the operating-point condition 0 <= p_aux_required <= installed.

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: images/page_031_eq_1.png / page_031_eq_2.png (Eq. A.2/A.3,
            the steady-state balance the operand rearranges);
            images/page_002_table_0.png (Table 2: "Required plasma-coupled
            ECRH power [MW] 50" -- the installed side, coupled-to-coupled);
            raw PDF p. 9 (the start-up path and the 50 MW to reach point A) and
            p. 10 (Table 5: fusion gain infinity / 182, aux. power at operation
            point 0 / 14.77 MW for points A / B -- read from the page render,
            work/orchestration/goals/burn-control/evidence/grounding_sources_table5.png;
            the extracted table is corrupted)
        **Basis**: p_aux_required <= installed plasma-coupled heating (the upper
            half of 0 <= p_aux_required <= installed; 'Burn Hold' is the lower)
        */

        // required sustained plasma-coupled heating [MW] (computed)
        in attribute p_aux_required_in : Real;
        // installed plasma-coupled heating [MW]
        in attribute p_aux_installed_in : Real;

        p_aux_required_in <= p_aux_installed_in
    }

    constraint def 'Burn Hold' {
        doc /*
        Operating-point hold bound (WI-043; goal burn-control): the required
        sustained plasma-coupled heating computed by 'Plasma Sustainment'
        (mfe_plasma_sustainment) must not be NEGATIVE. Pair with 'Sustainment
        Limit' on the same operand: together they say an operating point is one
        whose power balance closes with an auxiliary heating that is zero or
        positive and no larger than what is installed.

        What a negative requirement means, and why it is a bound: alpha heating
        alone exceeds every loss at the chosen density and temperature. A point
        with a negative requirement has no heating authority -- no non-negative
        heating closes its balance -- and left alone at its density the plasma
        as modeled settles far outside the other limits (the grounding probe:
        20-41 keV, the wall peak at 2.3-5.4x its limit; goal burn-control
        evidence/grounding_probe/summary.md section Reading (b)). The model has
        no burn-control mechanism (fuelling, impurity seeding, confinement
        degradation) that would arrest that, and no admissible source quantifies
        one (evidence/grounding_sources.md section Q2). So this bound is the
        HOLD condition: the point is one the installed heating system can hold.
        Where a DRIVEN point sits on the ignition curve decides HOW it is held,
        not whether: measured over the committed window at this pin (study
        20260907-burn-control, the branch column), the 13 and 14.63 keV rows sit
        on the falling branch everywhere (d p_aux_required / d T below zero: a
        temperature rise needs less heating, so the point is held by feedback on
        its own auxiliary power), while at 16-18 keV and low density (n_e0
        0.6-0.8x) 84 driven points sit on the rising branch (a temperature rise
        needs more heating: stable under fixed heating); every ignited point
        measured is on the falling branch. The bound rests on the first
        sentence, not on the branch (goal burn-control, goal.md Amendment
        2026-09-07; WI-043 spec Amendment 2026-09-07).

        It is NOT a statement that ignition is infeasible. The sister systems
        codes define an ignited design point as the solution of the same
        balance with P_aux = 0 exactly (an equality; "Require ignited design
        points, Q ~ infinity"), and leave the over-ignited region outside the
        described space; this bound is the inequality form of that practice.
        The design source's own point A is such an ignited point (Table 5:
        fusion gain infinity, auxiliary power at the operation point 0 MW).

        **Source**: knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/output.md
            (Lion et al. 2021, the PROCESS stellarator version);
            knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/output.md
            (Lion 2023);
            knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
            (Stellaris; Table 5 read from the raw PDF page render, the extracted
            table is corrupted -- goal burn-control evidence/grounding_sources_table5.png)
        **Ref**: Lion 2021 output.md L164 ("imposes a power balance as an
            equality constraint"), L211, Eq. 7 image (P_loss =! ... + P_aux);
            Lion 2023 Tables 4.2 / 4.5 / 4.7 ("Require ignited design points,
            Q ~ infinity"), L2154 (the over-ignited points "would be ignited,
            given the imposed models"); Stellaris raw PDF p. 9 (Fig. 15 caption:
            white where "the plasma would ignite (high T, high n)"), p. 10
            (Table 5: fusion gain infinity / 182; aux. power at operation point
            0 / 14.77 MW for points A / B)
        **Basis**: 0 <= p_aux_required, the lower half of the operating-point
            condition 0 <= p_aux_required <= installed coupled heating; the
            literal zero is the balance's own closing value, not a sourced
            number, and is not an entry point
        */

        // required sustained plasma-coupled heating [MW] (computed)
        in attribute p_aux_required_in : Real;

        p_aux_required_in >= 0.0
    }
}
