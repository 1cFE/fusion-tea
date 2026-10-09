from pydantic import Field
from simkit.config.schema import MultiOutput

class Winding_Turn_Area_ScreenOutput(MultiOutput):
    """Multi-output container for Winding_Turn_Area_Screen.

Sums the supplied per-turn component areas and compares the gross area with the envelope; separately computes the allowance-rule requirements at the evaluated duty and compares them with the supplied areas. It never resizes an area. cable = element_area/cabling_factor/(1 - cable_void); net = cable + cu_space + steel_area + misc_area + solder_area; gross = net/(1 - ins_fraction); fit_margin = available_area - gross; fit_margin_fraction = fit_margin/available_area; required_envelope_J = I/gross (A/mm2). Copper rule: if J_cu_rule > 0, cu_required = max(0, I/J_cu_rule - element_copper_area)/(1 - cu_void), else cu_required = cu_per_kA_rule*I/1000. Steel rule: steel_required = steel_per_kA_rule*(I/1000)*(B/B_steel_ref if steel_B_scaling = 1, else 1). Margins are supplied minus required; pass flags are 1 when the margin is >= 0. Protection and structural adequacy are allowance rules, not evaluated physics. **Source**: knowledge/sources/eu_demo_rw_tf_coil_conductor_dematte_bruzzone/raw.pdf; knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png **Reference**: Demattè & Bruzzone Table I and pp.2-4 (output.md:106, :139); Stellaris Table 7; work/active/WI-099_magnet-conductor-alternatives/design.md section 2.3; contract section 4 (constructions P and C). **Basis**: [AGENT] allowance-rule construction calibrated to reproduce EU DEMO layer 1 and Stellaris Table 7; scaling steel with B at fixed geometry is a bounded assumption. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/winding_turn_area_screen_impl.py. **Last Updated**: 2026-09-29

SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:97
    """
    net_area: float = Field(description="net_area output")
    fit_margin: float = Field(description="fit_margin output")
    steel_margin: float = Field(description="steel_margin output")
    fit_margin_fraction: float = Field(description="fit_margin_fraction output")
    steel_pass: float = Field(description="steel_pass output")
    cu_required: float = Field(description="cu_required output")
    cu_pass: float = Field(description="cu_pass output")
    steel_required: float = Field(description="steel_required output")
    gross_area: float = Field(description="gross_area output")
    cable_area: float = Field(description="cable_area output")
    cu_margin: float = Field(description="cu_margin output")
    required_envelope_J: float = Field(description="required_envelope_J output")
    fit_pass: float = Field(description="fit_pass output")
