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
        First-wall lifetime bound: the neutron wall load [MW/m^2] must stay at or
        below the first-wall material/design limit. Excessive neutron flux drives
        displacement damage (DPA) and shortens the first-wall replacement
        interval below viability. Pair with 'Neutron Wall Load' (mfe_plasma_
        scaling), which forward-computes the load from fusion power and wall area.

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: Table 2 image (images/page_002_table_0.png: peak neutron wall load 4.05 MW/m^2), lines 1757-1766 (DPA-limited first-wall lifetime)
        **Basis**: Neutron wall load must not exceed the first-wall design limit
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

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
        **Ref**: images/page_031_eq_1.png / page_031_eq_2.png (Eq. A.2/A.3,
            the steady-state balance the operand rearranges);
            images/page_002_table_0.png (Table 2: "Required plasma-coupled
            ECRH power [MW] 50" -- the installed side, coupled-to-coupled)
        **Basis**: p_aux_required <= installed plasma-coupled heating
        */

        // required sustained plasma-coupled heating [MW] (computed)
        in attribute p_aux_required_in : Real;
        // installed plasma-coupled heating [MW]
        in attribute p_aux_installed_in : Real;

        p_aux_required_in <= p_aux_installed_in
    }
}
