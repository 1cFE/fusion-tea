package mfe_winding_pack_fit {
    private import ScalarValues::*;
    calc def 'Winding Pack Casing Fit' {
        doc /* Conditional local centered and aligned rectangular envelope fit. x is the plasma-face normal approximated as radial; y is transverse/Phi, both normal to conductor centreline. Nominal area wp_side^2 retains the published homogenized envelope; internal sheet inclusion is unresolved. This does not establish bare conductor geometry or global nonplanar alignment.
        Normative equations: nominal_x=wp_side*sqrt(aspect_ratio), nominal_y=wp_side/sqrt(aspect_ratio); internal_x=nominal_x*internal_fraction_x and analogously y; pack=nominal+internal; insulated=pack+2*ground_insulation; required=insulated+2*assembly_clearance. cavity_x=radial_allocation-2*wall_thickness; cavity_y=interior_y; exterior_x=radial_allocation; exterior_y=interior_y+2*wall_thickness; margin=cavity-required; minimum_margin=min(margin_x,margin_y). All lengths m; aspect ratio and internal fractions dimensionless.
        All inputs/outputs finite; wp_side, aspect_ratio, radial_allocation, interior_y, wall_thickness and cavity_x positive; fractions and other allowances nonnegative. Refuse arithmetic overflow or underflow of positive multiplicative terms deliberately with quantity-named ValueError. Negative finite margins are valid failure results; zero margin passes.
        Internal fractions represent excluded-sheet continuous pitch; external ground insulation and assembly allowances are separate, counted per opposing face exactly once. Casing geometry does not reprice wall mass or insulation, resize total supports, or replace inherited thermal-area/stress proxies. Independent coil radial allocation is not resized to fit demand. Common nominal undeformed state only; no contraction, offsets, fillets, route, stress or manufacturing qualification.
        **Source**: work/orchestration/goals/winding-pack-casing-fit/evidence/geometry-research.md
        **Reference**: Stellaris original PDF pp.22-23 Fig.40/Table8; WI-061 design.md reviewed equations and conditional scenario.
        **Last Updated**: 2026-09-15 */
        in attribute wp_side : Real;
        in attribute aspect_ratio : Real;
        in attribute internal_fraction_x : Real;
        in attribute internal_fraction_y : Real;
        in attribute ground_insulation : Real;
        in attribute radial_allocation : Real;
        in attribute interior_y : Real;
        in attribute wall_thickness : Real;
        in attribute assembly_clearance : Real;
        out attribute nominal_x : Real;
        out attribute nominal_y : Real;
        out attribute internal_x : Real;
        out attribute internal_y : Real;
        out attribute pack_x : Real;
        out attribute pack_y : Real;
        out attribute insulated_x : Real;
        out attribute insulated_y : Real;
        out attribute required_x : Real;
        out attribute required_y : Real;
        out attribute cavity_x : Real;
        out attribute cavity_y : Real;
        out attribute exterior_x : Real;
        out attribute exterior_y : Real;
        out attribute margin_x : Real;
        out attribute margin_y : Real;
        out attribute minimum_margin : Real;
    }
    constraint def 'Winding Pack Fits Casing' {
        doc /* Both full-width margins nonnegative, exact contact allowed. Source: WI-061 design.md; local geometric screen only. */
        in attribute minimum_margin_in : Real;
        minimum_margin_in >= 0.0
    }
}
