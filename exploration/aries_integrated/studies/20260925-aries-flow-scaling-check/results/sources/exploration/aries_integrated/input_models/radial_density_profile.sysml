package radial_density_profile {
    private import ScalarValues::*;

    calc def 'Radial Density Profile' {
        doc /* Local density [m^-3] at a supplied normalized radial coordinate.
        amplitude_in is an equation coefficient, not an axis, peak or mean density.
        density=(amplitude-edge)*(1-rho^p)^q*(h+(1-h)*rho^2)+edge.
        The typed manual completion enforces finite inputs, amplitude>0,
        0<=edge<=amplitude, 0<=rho<=1, p>0, q>0 and 0<=h<=1;
        nonfinite intermediates or output are refused. This mathematical domain
        is not an empirical plasma validity claim. All six inputs are supplied
        choices; the calculation selects no profile amplitude or hardware.
        Source equation is used here for the authorized post-reveal comparison;
        no ARIES-specific shape or amplitude is embedded in this reusable logic.
        **Source**: work/active/WI-081_aries-hollow-finite-edge-density-profile/spec.md
        **Reference**: Lyon 2008 Eq. (3), printed p701; retained primary image
        .project/active/aries-comparison-preparation/post-reveal-preparation/mapping/evidence/lyon-p701.png;
        work/orchestration/aries-transfer-experiment/evidence/profile-review.md
        **Last Updated**: 2026-09-21 */
        in attribute amplitude_in : Real;
        in attribute edge_density_in : Real;
        in attribute rho_in : Real;
        in attribute radial_exponent_in : Real;
        in attribute profile_exponent_in : Real;
        in attribute hollowness_in : Real;
        out attribute density : Real =
            (amplitude_in - edge_density_in)
            * (1.0 - rho_in ** radial_exponent_in) ** profile_exponent_in
            * (hollowness_in + (1.0 - hollowness_in) * rho_in ** 2.0)
            + edge_density_in;
    }
}
