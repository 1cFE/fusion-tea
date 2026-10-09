from pydantic import Field
from simkit.config.schema import MultiOutput

class REBCO_Conductor_CurrentOutput(MultiOutput):
    """Multi-output container for REBCO_Conductor_Current.

Conditional 20 K perpendicular-field REBCO current estimate. Reference current is A per 4 mm width at 20 T; full composite thickness fixed 56 micrometres. Width transfer is linear from 4 to 6 mm. Ic_tape=reference_tape_current*(tape_width/0.004)*(B_peak/20)^(-0.6)*material_factor*orientation_factor. Exponent 0.6 is independently source-based, not the selected-envelope sizing exponent. N_set=tape_length/conductor_length; N_ref=N_set*f_set/f_wp_vol. Critical currents=N*Ic_tape*cabling_factor*degradation_factor*sharing_factor; operating fractions=turn_current/critical_current. allowable_current=allowable_fraction*critical_current_reference; margin_fraction=allowable_fraction-operating_fraction_reference; margin_current=allowable_current-turn_current. All currents A; lengths m; temperature K; field T; fractions dimensionless. Series turns cancel in length ratios. Reference-conductor estimate is not a worst-coil or weakest-tape guarantee.
Typed manual completion enforces finite positive inputs and positive arithmetic, 20 K, 56e-6 m thickness, width 0.004..0.006 m, 20..32 T, retention factors and allowance in (0,1], switch exactly 0/1. Above 24 T requires switch 1 and emits field_extrapolated=1; 32 T is an engineering cutoff, not measurement authority. Refuse overflow/underflow. Finite negative margins are valid failures; exact zero passes. Material/orientation are positive assumed multipliers; retention factors act once on capacity, allowance only on allowable current/margins.
Nominal 200 A is a rounded manufacturing inference from 175 A times 1.13, not a measured 56 micrometre product guarantee. 20..24 T is an approximate empirical prediction; construction/criterion transfer and ideal sharing remain unqualified. No temperature law or local angle/strain model is implied.
Gate (WI-100 design section 2.1): enabled selects the law. At 1 the equations, domain refusals and outputs are unchanged and evaluation_defined is 1; at 0 every output, evaluation_defined included, is 0.0, returned before any domain check; any other value is refused (WI-080 gating pattern, mfe_viability.sysml:106-118).
*Source**: work/orchestration/goals/absolute-conductor-current-margin/evidence/performance-research.md
*Reference**: Molodyk et al. 2021 doi:10.1038/s41598-021-81559-z pp.4,5,7 Fig.4; WI-062 design.md and source-design-review.md.
*Last Updated**: 2026-09-15

SysML Source: root-0/analyses/mfe_conductor_current.sysml:3
    """
    critical_current_reference: float = Field(description="critical_current_reference output")
    critical_current_set: float = Field(description="critical_current_set output")
    parallel_tapes_reference: float = Field(description="parallel_tapes_reference output")
    operating_fraction_set: float = Field(description="operating_fraction_set output")
    parallel_tapes_set: float = Field(description="parallel_tapes_set output")
    field_extrapolated: float = Field(description="field_extrapolated output")
    margin_fraction: float = Field(description="margin_fraction output")
    tape_critical_current: float = Field(description="tape_critical_current output")
    allowable_current: float = Field(description="allowable_current output")
    margin_current: float = Field(description="margin_current output")
    operating_fraction_reference: float = Field(description="operating_fraction_reference output")
    evaluation_defined: float = Field(description="evaluation_defined output")
