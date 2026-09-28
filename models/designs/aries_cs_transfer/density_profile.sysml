package aries_cs_density_profile {
    private import ScalarValues::*;
    private import radial_density_profile::*;

    part plasma_profile {
        doc /* Comparison-specific local density profile; no whole-plasma prediction.
        Behavior: evaluate the radial density distribution at the supplied rho.
        Amplitude is an arbitrary demonstration coefficient, not source axis,
        maximum or average density. Later source prose equating edge/axis to 0.1
        does not identify the Eq. (3) coefficient: the equation gives center=0.694*A.
        **Source**: knowledge/holdout/aries-cs/08-FST-Lyon.pdf
        **Reference**: printed p701 Eq. (3) and following reference parameters;
        .project/active/aries-comparison-preparation/post-reveal-preparation/mapping/evidence/lyon-p701.png;
        work/active/WI-081_aries-hollow-finite-edge-density-profile/spec.md R1-R5
        **Last Updated**: 2026-09-21 */
        attribute amplitude : Real = 1.0; // [m^-3], arbitrary demonstration choice.
        attribute rho : Real = 0.5; // [1], arbitrary evaluation coordinate.
        attribute radial_exponent : Real = 12.0; // Eq. (3) reference expn.
        attribute profile_exponent : Real = 1.0; // Eq. (3) reference alpha_n.
        attribute hollowness : Real = 0.66; // Eq. (3) reference x_mind.
        attribute edge_ratio : Real = 0.1; // Eq. (3) n_edge/n_e0, not edge/axis.
        attribute edge_density : Real = amplitude * edge_ratio; // [m^-3].
        calc profile : 'Radial Density Profile' {
            in amplitude_in = amplitude;
            in edge_density_in = edge_density;
            in rho_in = rho;
            in radial_exponent_in = radial_exponent;
            in profile_exponent_in = profile_exponent;
            in hollowness_in = hollowness;
        }
        attribute density : Real = profile.density; // [m^-3], local output.
    }
}
