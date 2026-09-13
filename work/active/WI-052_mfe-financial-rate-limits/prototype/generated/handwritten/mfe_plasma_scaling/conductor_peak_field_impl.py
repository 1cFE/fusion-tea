"""Auto-generated implementation for Conductor_Peak_Field.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:419

SysML Expressions:
    bore_factor = R_in / (R_in - a_coil_in)
    bore_factor_ref = R_ref_in / (R_ref_in - a_coil_ref_in)
    bore_norm = bore_factor / bore_factor_ref
    B_peak = B_axis_in * peak_ratio_in * bore_norm
    
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
R a1(C) / sqrt(A_wp) is NOT carried: a1(C) is unprinted and the corpus
offers no second anchor to separate it from a0(C) (WI-044 design D2).
a_coil is the coil-centre minor radius from the radial build
('MFE Radial Build' r_coil_centre; WI-044 design D1). Disclosed limit:
the peak/axis ratio at another geometry is the anchored shape's
prediction, not a printed fact; a changed coil count or shape is a
different configuration C.

Kept as a calc, not an inline plant expression, so the product is a
module-graph edge the study tooling can trace; the factors are
intermediate attributes so the executed arithmetic is exactly
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
*Basis**: peak-on-winding = axis field x printed coil-set ratio x the
eq.-39 bore factor normalised at the reference geometry; the
configuration coefficients absorbed by the anchor; MFE-generic
"""

AUTO_IMPLEMENTED = True

from wi052_probe.modules.mfe_plasma_scaling.conductor_peak_field import Conductor_Peak_FieldInput


def run_conductor_peak_field(inputs: Conductor_Peak_FieldInput) -> float:
    """Execute Conductor_Peak_Field calculation.

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
R a1(C) / sqrt(A_wp) is NOT carried: a1(C) is unprinted and the corpus
offers no second anchor to separate it from a0(C) (WI-044 design D2).
a_coil is the coil-centre minor radius from the radial build
('MFE Radial Build' r_coil_centre; WI-044 design D1). Disclosed limit:
the peak/axis ratio at another geometry is the anchored shape's
prediction, not a printed fact; a changed coil count or shape is a
different configuration C.

Kept as a calc, not an inline plant expression, so the product is a
module-graph edge the study tooling can trace; the factors are
intermediate attributes so the executed arithmetic is exactly
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
*Basis**: peak-on-winding = axis field x printed coil-set ratio x the
eq.-39 bore factor normalised at the reference geometry; the
configuration coefficients absorbed by the anchor; MFE-generic

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:419

SysML Expressions:
    bore_factor = R_in / (R_in - a_coil_in)
    bore_factor_ref = R_ref_in / (R_ref_in - a_coil_ref_in)
    bore_norm = bore_factor / bore_factor_ref
    B_peak = B_axis_in * peak_ratio_in * bore_norm
    
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
R a1(C) / sqrt(A_wp) is NOT carried: a1(C) is unprinted and the corpus
offers no second anchor to separate it from a0(C) (WI-044 design D2).
a_coil is the coil-centre minor radius from the radial build
('MFE Radial Build' r_coil_centre; WI-044 design D1). Disclosed limit:
the peak/axis ratio at another geometry is the anchored shape's
prediction, not a printed fact; a changed coil count or shape is a
different configuration C.

Kept as a calc, not an inline plant expression, so the product is a
module-graph edge the study tooling can trace; the factors are
intermediate attributes so the executed arithmetic is exactly
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
*Basis**: peak-on-winding = axis field x printed coil-set ratio x the
eq.-39 bore factor normalised at the reference geometry; the
configuration coefficients absorbed by the anchor; MFE-generic

Args:
    inputs: Input parameters validated against Conductor_Peak_FieldInput schema

Returns:
    float: B_peak

Example:
    >>> inputs = Conductor_Peak_FieldInput(...)
    >>> result = run_conductor_peak_field(inputs)
    """
    bore_factor = (inputs.R_in / (inputs.R_in - inputs.a_coil_in))
    bore_factor_ref = (inputs.R_ref_in / (inputs.R_ref_in - inputs.a_coil_ref_in))
    bore_norm = (bore_factor / bore_factor_ref)
    return ((inputs.B_axis_in * inputs.peak_ratio_in) * bore_norm)
