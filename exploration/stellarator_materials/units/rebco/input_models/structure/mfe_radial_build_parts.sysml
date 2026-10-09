package mfe_radial_build_parts {
    private import ScalarValues::*;
    private import mfe_plasma_scaling::*;

    part def 'First Wall' {
        doc /*
        The plasma-facing wall of the blanket module. In the source: EUROFER97 with a 2 mm
        tungsten armour, helium-cooled at 8 MPa (350 C in, below 370 C out) on a loop the
        model does not compute separately -- the model carries one primary loop (see
        'Primary Heat Transport'). Owns its radial thickness, the vacuum gap it stands off
        from the plasma, the neutron wall-load peak calibration facts (WI-041) and the
        fluence replacement limit the lifecycle calendar reads (WI-046). WI-057.
        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/output.md
        **Ref**: first-wall section (Fig. 27; lines ~1300-1350); Table 6 image page_021_table_0.png (radial build)
        **Basis**: the first wall as the owner of the wall-load and lifetime quantities
        */
        attribute firstwall_t : Real default 0.05;
        // Radial-build layer thicknesses [m] (WI-021). Generic-plant machinery:
        // the radial-build pattern is shared; concept instances override values.
        // Defaults are the 1costingFE RadialBuild defaults (geometry.py:19-40).
        attribute vacuum_t : Real default 0.10;
        // Reference facts for the peak calibration. Dormant by default (the
        // WI-024 / WI-039 additive-direct-term pattern): a concept with no source
        // peak leaves q_ref at 0 and the direct term at 1.0, so the calibration is
        // 0 x A_ref / p_n_ref + 1.0 = 1.0 and the peak equals the average -- the
        // pre-WI-041 fence semantics exactly. A concept anchoring to a source
        // binds its six printed facts and zeroes the direct term. p_fus_ref
        // defaults to 1.0, never 0, so the dormant division stays defined.
        attribute wall_peak_q_ref : Real default 0.0;
        attribute wall_peak_p_fus_ref : Real default 1.0;
        attribute wall_peak_R_ref : Real default 1.0;
        attribute wall_peak_a_ref : Real default 1.0;
        attribute wall_peak_kappa_ref : Real default 1.0;
        attribute wall_peak_standoff_ref : Real default 0.0;
        attribute wall_peak_calibration_direct : Real default 1.0;
        // Core fluence limit [MW-yr/m^2] (instance binds; DT 18.0, defaults.py:291).
        attribute fluence_limit : Real;
        // ---- inputs the plant wires (WI-057): values produced elsewhere, read here by name ----
        attribute p_fus : Real;   // <- plasma.p_fus
        attribute wall_area : Real;   // <- rb.wall_area
        // ---- EXPOSEs (WI-057): this part's calc outputs, readable outside as <part>.<name> ----
        attribute calibration : Real = wall_peak_cal.calibration;
        attribute wall_load : Real = wall_load_calc.wall_load;
        attribute wall_load_peak : Real = wall_peak_calc.wall_load_peak;
        // ---- template calcs (WI-057): the analyses this part owns ----
        // ---- Neutron wall load: average, source-anchored calibration, peak (WI-041) ----
        // The circular-torus AVERAGE over the model's own first-wall area, and the
        // PEAK that a peak design limit and the fluence-limited lifetime both read.
        // The peak is the average times a calibration computed from a source's
        // own printed peak at its own design point ('Neutron Wall Load Peak
        // Calibration'). Declared in the generic plant so one peak reaches both
        // the concept's fence and the CAS72 lifetime chain below.
        calc wall_load_calc : 'Neutron Wall Load' {
            in p_fus = 'First Wall'::p_fus;
            in wall_area = 'First Wall'::wall_area;
        }
        calc wall_peak_cal : 'Neutron Wall Load Peak Calibration' {
            in q_peak_ref = wall_peak_q_ref;
            in p_fus_ref = wall_peak_p_fus_ref;
            in R_ref = wall_peak_R_ref;
            in a_ref = wall_peak_a_ref;
            in kappa_ref = wall_peak_kappa_ref;
            in standoff_ref = wall_peak_standoff_ref;
            in calibration_direct = wall_peak_calibration_direct;
        }
        calc wall_peak_calc : 'Neutron Wall Load Peak' {
            in wall_load = wall_load_calc.wall_load;
            in calibration_in = wall_peak_cal.calibration;
        }
    }
}
