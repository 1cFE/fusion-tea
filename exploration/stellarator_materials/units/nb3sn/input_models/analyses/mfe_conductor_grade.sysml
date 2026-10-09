package mfe_conductor_grade {
    private import ScalarValues::*;

    calc def 'Conductor Field Capability' {
        doc /*
        Relative conductor quantity for a selected design field envelope, distinct from actual peak-field demand. Normative manual equations: quantity_factor = (B_design / B_reference)^field_exponent; j_wp_effective = j_reference / quantity_factor.
        Inputs: B_design and B_reference T, field_exponent dimensionless, j_reference A/mm^2. Outputs: quantity_factor dimensionless and j_wp_effective A/mm^2. The enlarged fixed-composition pack determines purchased tape volume; this calculation carries no price. Hold tape construction, temperature, angular assumption and composition fixed for the relative-envelope interpretation.
        Changing reference density on unchanged tape changes operating current per tape. Lower density purchases more tape; higher density consumes unknown current margin. Manufacturing-performance improvement, packing changes and grading require different scenario evidence. Reference-coil loading is j_wp_effective * tape_area / tape_fraction; set-effective loading also includes f_set/f_wp_vol because current and pack-volume distribution factors are distinct transfer approximations. No absolute current margin, qualified field capability or pack/casing fit is established by this model.
        The source's approximate 20 K exponent has no stated fit interval; Fig. 1a measurements extend to approximately 24 T, below the 24.9 T reference. The selected 20-30 T sensitivity is extrapolative. Numerical domain: finite positive inputs, field ratio, quantity factor and effective density. Typed completion raises calculation- and quantity-named ValueError for invalid inputs, overflow and positive-output underflow. Equal fields give quantity_factor exactly one.
        **Source**: knowledge/sources/development_and_large_volume_production_of_extremely_high/raw.pdf
        **Reference**: Molodyk et al. (2021), printed p. 5 (approximate critical-current field exponent 0.6 at 20 K); Fig. 1 (tape-level field measurements). Inverse relative-current-density law at fixed operating fraction; uniform fixed-composition pack enlargement and unchanged reference unit-tape economics are agent assumptions.
        **Last Updated**: 2026-09-15
        */
        in attribute B_design : Real;
        in attribute B_reference : Real;
        in attribute field_exponent : Real;
        in attribute j_reference : Real;
        out attribute quantity_factor : Real;
        out attribute j_wp_effective : Real;
    }
}
