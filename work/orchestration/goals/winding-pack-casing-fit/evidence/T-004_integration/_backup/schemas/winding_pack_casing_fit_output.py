from pydantic import Field
from simkit.config.schema import MultiOutput

class Winding_Pack_Casing_FitOutput(MultiOutput):
    """Multi-output container for Winding_Pack_Casing_Fit.

Conditional local centered and aligned rectangular envelope fit. x is the plasma-face normal approximated as radial; y is transverse/Phi, both normal to conductor centreline. Nominal area wp_side^2 retains the published homogenized envelope; internal sheet inclusion is unresolved. This does not establish bare conductor geometry or global nonplanar alignment.
Normative equations: nominal_x=wp_side*sqrt(aspect_ratio), nominal_y=wp_side/sqrt(aspect_ratio); internal_x=nominal_x*internal_fraction_x and analogously y; pack=nominal+internal; insulated=pack+2*ground_insulation; required=insulated+2*assembly_clearance. cavity_x=radial_allocation-2*wall_thickness; cavity_y=interior_y; exterior_x=radial_allocation; exterior_y=interior_y+2*wall_thickness; margin=cavity-required; minimum_margin=min(margin_x,margin_y). All lengths m; aspect ratio and internal fractions dimensionless.
All inputs/outputs finite; wp_side, aspect_ratio, radial_allocation, interior_y, wall_thickness and cavity_x positive; fractions and other allowances nonnegative. Refuse arithmetic overflow or underflow of positive multiplicative terms deliberately with quantity-named ValueError. Negative finite margins are valid failure results; zero margin passes.
Internal fractions represent excluded-sheet continuous pitch; external ground insulation and assembly allowances are separate, counted per opposing face exactly once. Casing geometry does not reprice wall mass or insulation, resize total supports, or replace inherited thermal-area/stress proxies. Independent coil radial allocation is not resized to fit demand. Common nominal undeformed state only; no contraction, offsets, fillets, route, stress or manufacturing qualification.
*Source**: work/orchestration/goals/winding-pack-casing-fit/evidence/geometry-research.md
*Reference**: Stellaris original PDF pp.22-23 Fig.40/Table8; WI-061 design.md reviewed equations and conditional scenario.
*Last Updated**: 2026-09-15

SysML Source: root-0/analyses/mfe_winding_pack_fit.sysml:3
    """
    required_y: float = Field(description="required_y output")
    nominal_y: float = Field(description="nominal_y output")
    minimum_margin: float = Field(description="minimum_margin output")
    margin_x: float = Field(description="margin_x output")
    internal_y: float = Field(description="internal_y output")
    pack_x: float = Field(description="pack_x output")
    exterior_x: float = Field(description="exterior_x output")
    cavity_x: float = Field(description="cavity_x output")
    nominal_x: float = Field(description="nominal_x output")
    cavity_y: float = Field(description="cavity_y output")
    exterior_y: float = Field(description="exterior_y output")
    insulated_y: float = Field(description="insulated_y output")
    margin_y: float = Field(description="margin_y output")
    internal_x: float = Field(description="internal_x output")
    pack_y: float = Field(description="pack_y output")
    required_x: float = Field(description="required_x output")
    insulated_x: float = Field(description="insulated_x output")
