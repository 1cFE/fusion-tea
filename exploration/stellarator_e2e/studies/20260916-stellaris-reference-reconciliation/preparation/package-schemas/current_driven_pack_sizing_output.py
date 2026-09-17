from pydantic import Field
from simkit.config.schema import MultiOutput

class Current_Driven_Pack_SizingOutput(MultiOutput):
    """Multi-output container for Current_Driven_Pack_Sizing.

Optional continuous reference-conductor inventory sizing, using the unchanged WI-062 conditional performance law: Ia=reference_tape_current*(tape_width/0.004)*(B_peak/20)^(-0.6)*material_factor*orientation_factor*cabling_factor*degradation_factor*sharing_factor [A]. At=tape_width*tape_thickness [m^2]; ft=1-f_copper-f_solder-f_steel-f_helium. Nreq=turn_current/(allowable_fraction*Ia); Acond=Nreq*At/ft [m^2]; Apack=(I_coil/turn_current)*Acond [m^2]; jreq=I_coil/(Apack*1e6) [A/mm^2]. Mode0 selects legacy_effective_density exactly; mode1 selects jreq/inventory_multiplier. Multiplier >=1 adds physical inventory without changing acceptance. Mode is exactly0/1. All positive inputs/intermediates finite and positive, non-tape fractions nonnegative, ft in(0,1]. Retention/allowance in(0,1]. Same 20 K, 56 micrometre composite, 4..6 mm, 20..32 T domain; above24 T requires extrapolation permission. Refuse arithmetic overflow/underflow. Actual independent allocation determines peak field first; no geometry feedback. Continuous counts and conditional material transfer do not qualify a manufactured winding. Legacy grade diagnostics remain unchanged.
*Source**: work/active/WI-064_current-driven-magnet-inventory-sizing/spec.md; work/orchestration/goals/absolute-conductor-current-margin/evidence/performance-research.md
*Reference**: work/active/WI-064_current-driven-magnet-inventory-sizing/spec.md; work/orchestration/goals/joint-magnet-sizing-feasibility/evidence/source-design-review.md; work/orchestration/goals/absolute-conductor-current-margin/evidence/performance-research.md
*Last Updated**: 2026-09-15

SysML Source: root-0/analyses/mfe_conductor_current.sysml:39
    """
    required_tapes: float = Field(description="required_tapes output")
    required_conductor_area: float = Field(description="required_conductor_area output")
    required_pack_area: float = Field(description="required_pack_area output")
    required_effective_density: float = Field(description="required_effective_density output")
    selected_effective_density: float = Field(description="selected_effective_density output")
    tape_available_current: float = Field(description="tape_available_current output")
