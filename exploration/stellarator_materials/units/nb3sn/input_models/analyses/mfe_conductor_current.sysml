package mfe_conductor_current {
    private import ScalarValues::*;
    calc def 'REBCO Conductor Current' {
        doc /* Conditional 20 K perpendicular-field REBCO current estimate. Reference current is A per 4 mm width at 20 T; full composite thickness fixed 56 micrometres. Width transfer is linear from 4 to 6 mm. Ic_tape=reference_tape_current*(tape_width/0.004)*(B_peak/20)^(-0.6)*material_factor*orientation_factor. Exponent 0.6 is independently source-based, not the selected-envelope sizing exponent. N_set=tape_length/conductor_length; N_ref=N_set*f_set/f_wp_vol. Critical currents=N*Ic_tape*cabling_factor*degradation_factor*sharing_factor; operating fractions=turn_current/critical_current. allowable_current=allowable_fraction*critical_current_reference; margin_fraction=allowable_fraction-operating_fraction_reference; margin_current=allowable_current-turn_current. All currents A; lengths m; temperature K; field T; fractions dimensionless. Series turns cancel in length ratios. Reference-conductor estimate is not a worst-coil or weakest-tape guarantee.
        Typed manual completion enforces finite positive inputs and positive arithmetic, 20 K, 56e-6 m thickness, width 0.004..0.006 m, 20..32 T, retention factors and allowance in (0,1], switch exactly 0/1. Above 24 T requires switch 1 and emits field_extrapolated=1; 32 T is an engineering cutoff, not measurement authority. Refuse overflow/underflow. Finite negative margins are valid failures; exact zero passes. Material/orientation are positive assumed multipliers; retention factors act once on capacity, allowance only on allowable current/margins.
        Nominal 200 A is a rounded manufacturing inference from 175 A times 1.13, not a measured 56 micrometre product guarantee. 20..24 T is an approximate empirical prediction; construction/criterion transfer and ideal sharing remain unqualified. No temperature law or local angle/strain model is implied.
        Gate (WI-100 design section 2.1): enabled selects the law. At 1 the equations, domain refusals and outputs are unchanged and evaluation_defined is 1; at 0 every output, evaluation_defined included, is 0.0, returned before any domain check; any other value is refused (WI-080 gating pattern, mfe_viability.sysml:106-118).
        **Source**: work/orchestration/goals/absolute-conductor-current-margin/evidence/performance-research.md
        **Reference**: Molodyk et al. 2021 doi:10.1038/s41598-021-81559-z pp.4,5,7 Fig.4; WI-062 design.md and source-design-review.md.
        **Last Updated**: 2026-09-15 */
        in attribute B_peak : Real;
        in attribute temperature : Real;
        in attribute tape_width : Real;
        in attribute tape_thickness : Real;
        in attribute tape_length : Real;
        in attribute conductor_length : Real;
        in attribute f_set : Real;
        in attribute f_wp_vol : Real;
        in attribute turn_current : Real;
        in attribute reference_tape_current : Real;
        in attribute material_factor : Real;
        in attribute orientation_factor : Real;
        in attribute cabling_factor : Real;
        in attribute degradation_factor : Real;
        in attribute sharing_factor : Real;
        in attribute allowable_fraction : Real;
        in attribute allow_field_extrapolation : Real;
        in attribute enabled : Real default 1.0;
        out attribute parallel_tapes_set : Real;
        out attribute parallel_tapes_reference : Real;
        out attribute tape_critical_current : Real;
        out attribute critical_current_reference : Real;
        out attribute critical_current_set : Real;
        out attribute operating_fraction_reference : Real;
        out attribute operating_fraction_set : Real;
        out attribute allowable_current : Real;
        out attribute margin_fraction : Real;
        out attribute margin_current : Real;
        out attribute field_extrapolated : Real;
        out attribute evaluation_defined : Real;
    }
    calc def 'Current Driven Pack Sizing' {
        doc /* Optional continuous reference-conductor inventory sizing, using the unchanged WI-062 conditional performance law: Ia=reference_tape_current*(tape_width/0.004)*(B_peak/20)^(-0.6)*material_factor*orientation_factor*cabling_factor*degradation_factor*sharing_factor [A]. At=tape_width*tape_thickness [m^2]; ft=1-f_copper-f_solder-f_steel-f_helium. Nreq=turn_current/(allowable_fraction*Ia); Acond=Nreq*At/ft [m^2]; Apack=(I_coil/turn_current)*Acond [m^2]; jreq=I_coil/(Apack*1e6) [A/mm^2]. Mode0 selects legacy_effective_density exactly; mode1 selects jreq/inventory_multiplier. Multiplier >=1 adds physical inventory without changing acceptance. Mode is exactly0/1. All positive inputs/intermediates finite and positive, non-tape fractions nonnegative, ft in(0,1]. Retention/allowance in(0,1]. Same 20 K, 56 micrometre composite, 4..6 mm, 20..32 T domain; above24 T requires extrapolation permission. Refuse arithmetic overflow/underflow. Actual independent allocation determines peak field first; no geometry feedback. Continuous counts and conditional material transfer do not qualify a manufactured winding. Legacy grade diagnostics remain unchanged.
        **Source**: work/active/WI-064_current-driven-magnet-inventory-sizing/spec.md; work/orchestration/goals/absolute-conductor-current-margin/evidence/performance-research.md
        **Reference**: work/active/WI-064_current-driven-magnet-inventory-sizing/spec.md; work/orchestration/goals/joint-magnet-sizing-feasibility/evidence/source-design-review.md; work/orchestration/goals/absolute-conductor-current-margin/evidence/performance-research.md
        **Last Updated**: 2026-09-15 */
        in attribute sizing_mode : Real;
        in attribute inventory_multiplier : Real;
        in attribute legacy_effective_density : Real;
        in attribute I_coil : Real;
        in attribute turn_current : Real;
        in attribute f_copper : Real;
        in attribute f_solder : Real;
        in attribute f_steel : Real;
        in attribute f_helium : Real;
        in attribute tape_width : Real;
        in attribute tape_thickness : Real;
        in attribute B_peak : Real;
        in attribute temperature : Real;
        in attribute reference_tape_current : Real;
        in attribute material_factor : Real;
        in attribute orientation_factor : Real;
        in attribute cabling_factor : Real;
        in attribute degradation_factor : Real;
        in attribute sharing_factor : Real;
        in attribute allowable_fraction : Real;
        in attribute allow_field_extrapolation : Real;
        out attribute required_tapes : Real;
        out attribute required_conductor_area : Real;
        out attribute required_pack_area : Real;
        out attribute required_effective_density : Real;
        out attribute selected_effective_density : Real;
        out attribute tape_available_current : Real;
    }
    constraint def 'Reference Conductor Current Margin' {
        doc /* Conditional reference-conductor estimate only; exact boundary accepted. **Source**: WI-062 design.md **Reference**: work/active/WI-062_absolute-conductor-current-margin/design.md **Last Updated**: 2026-09-15 */
        in attribute margin_fraction_in : Real;
        margin_fraction_in >= 0.0
    }
}
