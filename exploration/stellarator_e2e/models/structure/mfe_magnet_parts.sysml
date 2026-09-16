package mfe_magnet_parts {
    private import ScalarValues::*;

    part def 'Modular Coil' {
        doc /*
        One of the modular non-planar HTS coils (50 in the source, 6 unique shapes, 5-fold
        symmetry): the coil-set current and its distribution facts, the coil geometry facts
        (major radius, geometry factor, winding circumference and its printed reference at the reference bore, the radial
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
        // typical winding circumference [m] (computed from the coil bore, WI-058)
        attribute c_coil : Real;
        // printed typical winding circumference [m] at the reference bore a_coil_ref
        // (WI-058; replaces the WI-036 shape factor k_coil over the major radius)
        attribute c_coil_ref : Real;
        // Legacy comparison-only conductor rate [dollars/(kA m)].
        // Existing ungraded comparison accounts continue to consume this rate.
        attribute cost_per_kAm : Real;
        // Effective operating current per composite-conductor turn [A].
        attribute turn_current : Real;
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
        The coil's winding pack: REBCO tape stacks in a copper jacket (9 % tape, 35 % Cu,
        12 % solder, 36 % steel, 8 % helium by volume in the Table 7 image), sized by the
        current it carries (WI-036). Owns the current density, the pack-volume distribution
        and fabrication factors, the conductor's modulus, load share and strain limit, the
        conductor field ceiling, the peak-stress transfer fact and the mean nuclear heating the
        cryoplant removes. WI-057: regrouped from 'Magnet System' without change of meaning.
        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/output.md
        **Reference**: sec. 2.10; images/page_021_table_0.png (Table 7 composition); images/page_022_table_0.png (Table 8 sizing). The text extraction of Table 7 is incorrect. Inter-pancake insulation has no quantified fraction here.
        **Basis**: the winding pack as the owner of the conductor and pack facts
        **Last Updated**: 2026-09-13
        */
        // WI-040 non-tape volume fractions [1]; residual volume is composite tape.
        attribute f_copper : Real;
        attribute f_solder : Real;
        attribute f_steel : Real;
        attribute f_helium : Real;
        // Material densities [kg/m^3]; helium is calculated from its state.
        attribute rho_copper : Real;
        attribute rho_solder : Real;
        attribute rho_steel : Real;
        // Procurement prices [dollars/kg]; explicit year/proxy basis in the instance.
        attribute price_copper : Real;
        attribute price_solder : Real;
        attribute price_steel : Real;
        attribute price_helium : Real;
        attribute helium_pressure : Real; // Pa
        attribute T_inventory : Real; // K, bound to cryoplant temperature
        attribute helium_gas_constant : Real; // J/(kg K)
        attribute winding_rate_1990 : Real; // dollars1990/m of composite conductor
        attribute cost_escalation : Real; // dimensionless year conversion
        attribute nonplanar_factor : Real; // dimensionless transfer assumption
        // Reference winding-pack current density [A/mm^2] at B_grade_ref.
        // Fixed-construction changes alter operating current per tape; absolute margin remains unknown.
        attribute j_wp : Real;
        attribute B_grade_ref : Real; // reference purchased envelope [T]
        attribute field_exponent : Real; // positive relative field exponent [1]
        // Derived capability quantities, bound by the magnet-owned analysis.
        attribute conductor_quantity_factor : Real;
        attribute j_wp_effective : Real; // selected physical sizing density [A/mm^2]
        attribute sizing_mode : Real default 0.0; // WI-064: legacy0, current-driven1
        attribute inventory_multiplier : Real default 1.0; // WI-064 additional physical inventory >=1
        attribute tape_width : Real; // full purchased tape width [m]
        attribute tape_thickness : Real; // full composite thickness, including stabilizer [m]
        attribute reference_tape_current : Real default 200.0; // WI-062 conditional performance scenario
        attribute material_factor : Real default 1.0; // WI-062 conditional performance scenario
        attribute orientation_factor : Real default 1.0; // WI-062 conditional performance scenario
        attribute cabling_factor : Real default 1.0; // WI-062 conditional performance scenario
        attribute degradation_factor : Real default 1.0; // WI-062 conditional performance scenario
        attribute sharing_factor : Real default 1.0; // WI-062 conditional performance scenario
        attribute allowable_fraction : Real default 0.8; // WI-062 conditional performance scenario
        attribute allow_field_extrapolation : Real default 1.0; // WI-062 conditional performance scenario
        attribute tape_price_per_m : Real; // dollars per metre of this width/construction
        // winding-pack cross-section side, worst coil [m]
        attribute wp_side : Real;
        // WI-061 conditional local fit inputs; fractions dimensionless, ground m per face.
        attribute fit_aspect_ratio : Real default 1.0;
        attribute internal_build_x : Real default 0.0;
        attribute internal_build_y : Real default 0.0;
        attribute ground_insulation : Real default 0.0;
        // winding-pack set-distribution factor [1] (WI-036 cold volume)
        attribute f_wp_vol : Real;
        // WI-063 mean side/reference side; separate from the area distribution factor.
        attribute f_wp_perimeter : Real default 1.0;
        attribute insulation_sheet_thickness : Real default 0.0005; // m; quantity assumption
        attribute insulation_sheet_price : Real default 0.0; // dollars/m^2; disabled incremental scenario

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
        // Purchased conductor field envelope [T]; checked against actual peak field.
        // WI-038 prices a relative quantity consequence, not a certified critical field.
        attribute B_max : Real;
        // Cryoplant heat-load chain (WI-024). Dormant by default: a concept that
        // knows its cryo electrical directly binds p_cryo (the direct term) and
        // leaves these unbound; a concept deriving it binds the chain and zeroes
        // p_cryo.
        attribute q_nuc_cryo : Real default 0.0;
    }

    part def 'Coil Casing' {
        // Independent local cavity/allowances [m]; not derived from mass or thermal surface.
        attribute interior_y : Real default 0.40;
        attribute wall_thickness : Real default 0.025;
        attribute assembly_clearance : Real default 0.0;
        doc /*
        The cast steel casing around each winding pack (AISI 316LN, 63-200 t each in the
        source). WI-059 nominal pricing uses total electromagnetic supports exclusively;
        this casing mass is a reference-floor diagnostic, not an additional charge.
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
        // Historical all-in rate component [$/kg]; unknown price year/qualification.
        attribute steel_price : Real;
        // Historical rate-composition factor [1]; no measured fabrication split.
        attribute f_steel_fab : Real;
        // structural allowable stress [Pa]
        attribute sigma_allow : Real;
    }
}
