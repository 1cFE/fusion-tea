package mfe_magnet_parts {
    private import ScalarValues::*;

    part def 'Modular Coil' {
        doc /*
        One of the modular non-planar HTS coils (50 in the source, 6 unique shapes, 5-fold
        symmetry): the coil-set current and its distribution facts, the coil geometry facts
        (major radius, geometry factor, winding circumference and shape factor, the radial
        thickness of the coil in the build), the conductor cost rate and manufacturing markup,
        the peak-to-axis field ratio and the WI-044 reference anchors, and the coil dose life.
        WI-057: regrouped from 'Magnet System' without change of meaning.
        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/output.md
        **Ref**: sec. 2.10 (coils; Table 8 image page_022_table_0.png)
        **Basis**: the coil as the owner of the current, geometry and conductor-cost facts
        */
        // ------- WI-035 coil-set current, limit, and cost-decomposition -------
        // parameters (all concept-set; see mfe_magnet_field / mfe_magnet_cost)
        // number of field coils [1]
        attribute n_coils : Real;
        // peak single-coil current [A]
        attribute I_coil : Real;
        // coil-set transfer fact [1] (set distribution x axis linkage, WI-035)
        attribute k_link : Real;
        // set-mean over peak coil current ratio [1]
        attribute f_set : Real;
        attribute R0 : Real;
        attribute G : Real;
        // typical winding circumference [m]
        attribute c_coil : Real;
        // coil-shape factor [1] = typical circumference / major radius (WI-036)
        attribute k_coil : Real;
        attribute cost_per_kAm : Real;
        attribute coil_markup : Real;
        // peak-on-winding / axis-averaged field ratio at the reference geometry
        // [1] (coil-set geometry fact, WI-030; the eq.-39 bore factor normalised
        // at (R_ref, a_coil_ref) multiplies it since WI-044)
        attribute peak_ratio : Real;
        // reference peak single-coil current [A]
        attribute I_ref : Real;
        // reference major radius [m]
        attribute R_ref : Real;
        // reference coil-centre minor radius [m] (the radial build's
        // r_coil_centre at the reference minor radius)
        attribute a_coil_ref : Real;
        attribute coil_t : Real default 0.30;
        // coil dose life [FPY] (instance binds) -- a reported margin's reference
        attribute coil_life_fpy : Real;
    }

    part def 'Winding Pack' {
        doc /*
        The coil's winding pack: REBCO tape stacks in a copper jacket (15 % conductor, 10 % Cu,
        45 % insulation, 26 % steel, 4 % helium in the source's composition), sized by the
        current it carries (WI-036). Owns the current density, the pack-volume distribution
        and fabrication factors, the conductor's modulus, load share and strain limit, the
        conductor field ceiling, the peak-stress transfer fact and the mean nuclear heating the
        cryoplant removes. WI-057: regrouped from 'Magnet System' without change of meaning.
        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/output.md
        **Ref**: sec. 2.10 (winding pack composition; Table 8 image page_022_table_0.png)
        **Basis**: the winding pack as the owner of the conductor and pack facts
        */
        // winding-pack current density [A/mm^2] -- the WI-036 sizing lever
        attribute j_wp : Real;
        // winding-pack cross-section side, worst coil [m]
        attribute wp_side : Real;
        // winding-pack set-distribution factor [1] (WI-036 cold volume)
        attribute f_wp_vol : Real;
        // winding-pack effective elastic modulus [Pa] (WI-036 conductor strain)
        attribute E_wp : Real;
        // conductor load-sharing factor [1] (WI-036 conductor strain)
        attribute f_cond : Real;
        // conductor strain limit [1] (WI-036)
        attribute eps_cond_allow : Real;
        // winding fabrication markup [1]
        attribute f_wp_fab : Real;
        // stress concentration transfer fact [1] (coil-set structural fact)
        attribute k_sigma : Real;
        // conductor peak-field ceiling [T] (conductor technology fact, WI-030)
        attribute B_max : Real;
        // Cryoplant heat-load chain (WI-024). Dormant by default: a concept that
        // knows its cryo electrical directly binds p_cryo (the direct term) and
        // leaves these unbound; a concept deriving it binds the chain and zeroes
        // p_cryo.
        attribute q_nuc_cryo : Real default 0.0;
    }

    part def 'Coil Casing' {
        doc /*
        The cast steel casing around each winding pack (AISI 316LN, 63-200 t each in the
        source), the part the structure-cost account prices (WI-035 D5: casings only; the
        inter-coil plates and support rings are the plant's 'Primary Structure', CAS22.1.5).
        Owns the casing mass (computed since WI-044), its reference anchors, the steel price,
        the fabrication markup and the structural allowable stress. WI-057: regrouped from
        'Magnet System' without change of meaning.
        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/output.md
        **Ref**: sec. 2.10 (casings; the 800 MPa design limit)
        **Basis**: the casing as the owner of the structural-mass and steel-cost facts
        */
        // casing steel mass per coil [kg] -- COMPUTED since WI-044 by
        // 'Magnet Casing Mass' from the stored energy (the generic plant binds
        // it by reference, the WI-036 wp_side pattern); m_casing_ref below is
        // the settable anchor
        attribute m_casing : Real;
        // ------- WI-044 coil-bore anchors: the reference point at which the
        // peak/axis ratio, the stored energy and the casing mass were read;
        // every sourced shape is normalised to exactly 1.0 there -------
        // reference casing steel mass per coil [kg] at W_mag_ref
        attribute m_casing_ref : Real;
        // reference coil-set stored magnetic energy [J] at (I_ref, a_coil_ref, R_ref)
        attribute W_mag_ref : Real;
        // fabricated structural steel price [$/kg]
        attribute steel_price : Real;
        // casing fabrication markup [1]
        attribute f_steel_fab : Real;
        // structural allowable stress [Pa]
        attribute sigma_allow : Real;
    }
}
