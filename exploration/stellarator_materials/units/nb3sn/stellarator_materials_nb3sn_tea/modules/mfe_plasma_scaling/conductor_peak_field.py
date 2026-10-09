"""Conductor_Peak_FieldModule Module Wrapper

TEAx module for Conductor_Peak_Field calculation.

Peak magnetic field on the winding pack [T] from the axis-averaged field,
the coil set's peak/axis ratio at its reference geometry, and the coil
bore (WI-030; geometry-aware since WI-044):

  bore_factor     = R / (R - a_coil)
  bore_factor_ref = R_ref / (R_ref - a_coil_ref)
  B_peak = B_axis * peak_ratio * (bore_factor / bore_factor_ref)

The shape is Lion 2021 eq. 39, B_max = mu0 I N / (R - a_coil) x
(a0(C) + R a1(C) / sqrt(A_wp)): the field on the coil rises as the coil
bore a_coil approaches the major radius R. With B_axis ~ N I / R
('Coil Set Axis Field'), the peak/axis ratio carries the factor
R / (R - a_coil) times the configuration term in parentheses. The
configuration coefficients a0(C), a1(C) are not printed for any
instance in the corpus, so the ratio is ANCHORED: peak_ratio is the
printed peak/axis pair at the reference geometry (R_ref, a_coil_ref),
and the eq.-39 factor is applied normalised to that geometry, so the
anchor reproduces the printed peak to the double and only the bore
dependence responds away from it. The winding-pack term
R a1(C) / sqrt(A_wp) is carried only through the optional arm slot, off by
default: a1(C) is unprinted and the corpus offers no second anchor to
separate it from a0(C) (WI-044 design D2). Arm slot (WI-100 design
section 2.2; plant contract r4 section 3.2): x = R / wp_side for a square
pack (sqrt(A_wp) = wp_side); ratio_eff = peak_ratio + arm_slope * (x - arm_x_ref);
B_peak = (B_axis * ratio_eff) * bore_norm. At arm_slope = 0 the result equals
the constant-ratio form bit for bit for any finite arm_x_ref. Arm domain:
finite arm inputs, wp_side > 0 and ratio_eff > 0, refused after the two
clearance checks.
a_coil is the coil-centre minor radius from the radial build
('MFE Radial Build' r_coil_centre; WI-044 design D1). Disclosed limit:
the peak/axis ratio at another geometry is the anchored shape's
prediction, not a printed fact; a changed coil count or shape is a
different configuration C.

Kept as a calc, not an inline plant expression, so the product is a
module-graph edge the study tooling can trace; the manual completion evaluates factors in the documented order
so the executed arithmetic is exactly
(B_axis * peak_ratio) * bore_norm, and bore_norm evaluates to exactly
1.0 at the reference geometry (the two factors are the same
expression on the same floats).

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/;
/home/reid/1cfe/1costingfe/src/costingfe/defaults.py (pin 0254385)
*Ref**: images/page_002_table_0.png (Table 2: axis av. 9.0 T, peak
    conductor 24.9 T); images/lion_2021_nf_stellarator_process.pdf-0009-19.png
    (eq. 39) with output.md L455 (a_coil "the average minor coil
    radius", N the number of coils, A_wp the winding-pack area);
    defaults.py:597-603 (MagnetProperties.b_max, "peak field ceiling
    at the conductor" -- the bounded quantity)
Domain: R_in - a_coil_in > 0 and R_ref_in - a_coil_ref_in > 0.
Native manual completion enforces both before any bore arithmetic.
An invalid domain raises ValueError; a valid computed field remains a
signed diagnostic evaluated separately by the conductor-field limit.

*Basis**: peak-on-winding = axis field x printed coil-set ratio x the
eq.-39 bore factor normalised at the reference geometry; the
configuration coefficients absorbed by the anchor; MFE-generic

Inputs:
    - B_axis_in: B_axis_in parameter
    - wp_side_in: wp_side_in parameter
    - peak_ratio_in: peak_ratio_in parameter
    - arm_x_ref_in: arm_x_ref_in parameter
    - a_coil_ref_in: a_coil_ref_in parameter
    - arm_slope_in: arm_slope_in parameter
    - R_ref_in: R_ref_in parameter
    - R_in: R_in parameter
    - a_coil_in: a_coil_in parameter

Outputs:
    - B_peak: B_peak result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:420

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:420

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plasma_scaling/conductor_peak_field_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float


class Conductor_Peak_FieldInput(BaseModel):
    """Input model for Conductor_Peak_FieldModule.

    Attributes:
        B_axis_in: B_axis_in input
        wp_side_in: wp_side_in input
        peak_ratio_in: peak_ratio_in input
        arm_x_ref_in: arm_x_ref_in input
        a_coil_ref_in: a_coil_ref_in input
        arm_slope_in: arm_slope_in input
        R_ref_in: R_ref_in input
        R_in: R_in input
        a_coil_in: a_coil_in input
    """
    B_axis_in: float = Field(..., description="B_axis_in input")
    wp_side_in: float = Field(..., description="wp_side_in input")
    peak_ratio_in: float = Field(..., description="peak_ratio_in input")
    arm_x_ref_in: float = Field(..., description="arm_x_ref_in input")
    a_coil_ref_in: float = Field(..., description="a_coil_ref_in input")
    arm_slope_in: float = Field(..., description="arm_slope_in input")
    R_ref_in: float = Field(..., description="R_ref_in input")
    R_in: float = Field(..., description="R_in input")
    a_coil_in: float = Field(..., description="a_coil_in input")


class Conductor_Peak_FieldModule(ModuleBase[Conductor_Peak_FieldInput, Float]):
    """TEAx module for Conductor_Peak_Field calculation.

Peak magnetic field on the winding pack [T] from the axis-averaged field,
the coil set's peak/axis ratio at its reference geometry, and the coil
bore (WI-030; geometry-aware since WI-044):

  bore_factor     = R / (R - a_coil)
  bore_factor_ref = R_ref / (R_ref - a_coil_ref)
  B_peak = B_axis * peak_ratio * (bore_factor / bore_factor_ref)

The shape is Lion 2021 eq. 39, B_max = mu0 I N / (R - a_coil) x
(a0(C) + R a1(C) / sqrt(A_wp)): the field on the coil rises as the coil
bore a_coil approaches the major radius R. With B_axis ~ N I / R
('Coil Set Axis Field'), the peak/axis ratio carries the factor
R / (R - a_coil) times the configuration term in parentheses. The
configuration coefficients a0(C), a1(C) are not printed for any
instance in the corpus, so the ratio is ANCHORED: peak_ratio is the
printed peak/axis pair at the reference geometry (R_ref, a_coil_ref),
and the eq.-39 factor is applied normalised to that geometry, so the
anchor reproduces the printed peak to the double and only the bore
dependence responds away from it. The winding-pack term
R a1(C) / sqrt(A_wp) is carried only through the optional arm slot, off by
default: a1(C) is unprinted and the corpus offers no second anchor to
separate it from a0(C) (WI-044 design D2). Arm slot (WI-100 design
section 2.2; plant contract r4 section 3.2): x = R / wp_side for a square
pack (sqrt(A_wp) = wp_side); ratio_eff = peak_ratio + arm_slope * (x - arm_x_ref);
B_peak = (B_axis * ratio_eff) * bore_norm. At arm_slope = 0 the result equals
the constant-ratio form bit for bit for any finite arm_x_ref. Arm domain:
finite arm inputs, wp_side > 0 and ratio_eff > 0, refused after the two
clearance checks.
a_coil is the coil-centre minor radius from the radial build
('MFE Radial Build' r_coil_centre; WI-044 design D1). Disclosed limit:
the peak/axis ratio at another geometry is the anchored shape's
prediction, not a printed fact; a changed coil count or shape is a
different configuration C.

Kept as a calc, not an inline plant expression, so the product is a
module-graph edge the study tooling can trace; the manual completion evaluates factors in the documented order
so the executed arithmetic is exactly
(B_axis * peak_ratio) * bore_norm, and bore_norm evaluates to exactly
1.0 at the reference geometry (the two factors are the same
expression on the same floats).

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/;
/home/reid/1cfe/1costingfe/src/costingfe/defaults.py (pin 0254385)
*Ref**: images/page_002_table_0.png (Table 2: axis av. 9.0 T, peak
    conductor 24.9 T); images/lion_2021_nf_stellarator_process.pdf-0009-19.png
    (eq. 39) with output.md L455 (a_coil "the average minor coil
    radius", N the number of coils, A_wp the winding-pack area);
    defaults.py:597-603 (MagnetProperties.b_max, "peak field ceiling
    at the conductor" -- the bounded quantity)
Domain: R_in - a_coil_in > 0 and R_ref_in - a_coil_ref_in > 0.
Native manual completion enforces both before any bore arithmetic.
An invalid domain raises ValueError; a valid computed field remains a
signed diagnostic evaluated separately by the conductor-field limit.

*Basis**: peak-on-winding = axis field x printed coil-set ratio x the
eq.-39 bore factor normalised at the reference geometry; the
configuration coefficients absorbed by the anchor; MFE-generic

Inputs:
    - B_axis_in: B_axis_in parameter
    - wp_side_in: wp_side_in parameter
    - peak_ratio_in: peak_ratio_in parameter
    - arm_x_ref_in: arm_x_ref_in parameter
    - a_coil_ref_in: a_coil_ref_in parameter
    - arm_slope_in: arm_slope_in parameter
    - R_ref_in: R_ref_in parameter
    - R_in: R_in parameter
    - a_coil_in: a_coil_in parameter

Outputs:
    - B_peak: B_peak result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:420

    SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:420

    Calculation Specification:
        wp_side_in = 1.0
        arm_slope_in = 0.0
        arm_x_ref_in = 0.0
        
Documentation:
Peak magnetic field on the winding pack [T] from the axis-averaged field,
the coil set's peak/axis ratio at its reference geometry, and the coil
bore (WI-030; geometry-aware since WI-044):

  bore_factor     = R / (R - a_coil)
  bore_factor_ref = R_ref / (R_ref - a_coil_ref)
  B_peak = B_axis * peak_ratio * (bore_factor / bore_factor_ref)

The shape is Lion 2021 eq. 39, B_max = mu0 I N / (R - a_coil) x
(a0(C) + R a1(C) / sqrt(A_wp)): the field on the coil rises as the coil
bore a_coil approaches the major radius R. With B_axis ~ N I / R
('Coil Set Axis Field'), the peak/axis ratio carries the factor
R / (R - a_coil) times the configuration term in parentheses. The
configuration coefficients a0(C), a1(C) are not printed for any
instance in the corpus, so the ratio is ANCHORED: peak_ratio is the
printed peak/axis pair at the reference geometry (R_ref, a_coil_ref),
and the eq.-39 factor is applied normalised to that geometry, so the
anchor reproduces the printed peak to the double and only the bore
dependence responds away from it. The winding-pack term
R a1(C) / sqrt(A_wp) is carried only through the optional arm slot, off by
default: a1(C) is unprinted and the corpus offers no second anchor to
separate it from a0(C) (WI-044 design D2). Arm slot (WI-100 design
section 2.2; plant contract r4 section 3.2): x = R / wp_side for a square
pack (sqrt(A_wp) = wp_side); ratio_eff = peak_ratio + arm_slope * (x - arm_x_ref);
B_peak = (B_axis * ratio_eff) * bore_norm. At arm_slope = 0 the result equals
the constant-ratio form bit for bit for any finite arm_x_ref. Arm domain:
finite arm inputs, wp_side > 0 and ratio_eff > 0, refused after the two
clearance checks.
a_coil is the coil-centre minor radius from the radial build
('MFE Radial Build' r_coil_centre; WI-044 design D1). Disclosed limit:
the peak/axis ratio at another geometry is the anchored shape's
prediction, not a printed fact; a changed coil count or shape is a
different configuration C.

Kept as a calc, not an inline plant expression, so the product is a
module-graph edge the study tooling can trace; the manual completion evaluates factors in the documented order
so the executed arithmetic is exactly
(B_axis * peak_ratio) * bore_norm, and bore_norm evaluates to exactly
1.0 at the reference geometry (the two factors are the same
expression on the same floats).

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/;
/home/reid/1cfe/1costingfe/src/costingfe/defaults.py (pin 0254385)
*Ref**: images/page_002_table_0.png (Table 2: axis av. 9.0 T, peak
    conductor 24.9 T); images/lion_2021_nf_stellarator_process.pdf-0009-19.png
    (eq. 39) with output.md L455 (a_coil "the average minor coil
    radius", N the number of coils, A_wp the winding-pack area);
    defaults.py:597-603 (MagnetProperties.b_max, "peak field ceiling
    at the conductor" -- the bounded quantity)
Domain: R_in - a_coil_in > 0 and R_ref_in - a_coil_ref_in > 0.
Native manual completion enforces both before any bore arithmetic.
An invalid domain raises ValueError; a valid computed field remains a
signed diagnostic evaluated separately by the conductor-field limit.

*Basis**: peak-on-winding = axis field x printed coil-set ratio x the
eq.-39 bore factor normalised at the reference geometry; the
configuration coefficients absorbed by the anchor; MFE-generic

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.mfe_plasma_scaling.conductor_peak_field_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Conductor_Peak_FieldModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, B_axis_in: float, wp_side_in: float, peak_ratio_in: float, arm_x_ref_in: float, a_coil_ref_in: float, arm_slope_in: float, R_ref_in: float, R_in: float, a_coil_in: float    ) -> Conductor_Peak_FieldInput:
        """Validate inputs and fill defaults.

        Args:
            B_axis_in: B_axis_in input
            wp_side_in: wp_side_in input
            peak_ratio_in: peak_ratio_in input
            arm_x_ref_in: arm_x_ref_in input
            a_coil_ref_in: a_coil_ref_in input
            arm_slope_in: arm_slope_in input
            R_ref_in: R_ref_in input
            R_in: R_in input
            a_coil_in: a_coil_in input

        Returns:
            Validated input model
        """
        return Conductor_Peak_FieldInput(B_axis_in=B_axis_in, wp_side_in=wp_side_in, peak_ratio_in=peak_ratio_in, arm_x_ref_in=arm_x_ref_in, a_coil_ref_in=a_coil_ref_in, arm_slope_in=arm_slope_in, R_ref_in=R_ref_in, R_in=R_in, a_coil_in=a_coil_in)

    def run(
        self, B_axis_in: float, wp_side_in: float, peak_ratio_in: float, arm_x_ref_in: float, a_coil_ref_in: float, arm_slope_in: float, R_ref_in: float, R_in: float, a_coil_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            B_axis_in: B_axis_in input
            wp_side_in: wp_side_in input
            peak_ratio_in: peak_ratio_in input
            arm_x_ref_in: arm_x_ref_in input
            a_coil_ref_in: a_coil_ref_in input
            arm_slope_in: arm_slope_in input
            R_ref_in: R_ref_in input
            R_in: R_in input
            a_coil_in: a_coil_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(B_axis_in, wp_side_in, peak_ratio_in, arm_x_ref_in, a_coil_ref_in, arm_slope_in, R_ref_in, R_in, a_coil_in)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.mfe_plasma_scaling.conductor_peak_field_impl import (
            run_conductor_peak_field,
        )

        # Execute implementation - returns single value
        B_peak = run_conductor_peak_field(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(B_peak))
