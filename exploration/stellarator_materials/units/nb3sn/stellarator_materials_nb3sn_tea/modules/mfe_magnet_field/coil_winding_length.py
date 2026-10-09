"""Coil_Winding_LengthModule Module Wrapper

TEAx module for Coil_Winding_Length calculation.

Typical coil winding circumference [m] from the coil bore (WI-058):

  c_coil = c_coil_ref * (a_coil / a_coil_ref)

The coil's size is stated on its bore: Stellaris prints the coils as
"approximate size of 7 x 5 x 10 m, with a typical circumference of
25 m", around a coil-centre minor radius of 3.15 m in this radial
build. A coil of fixed shape scaled to its bore has a circumference
proportional to the bore radius, so the length is the printed
circumference at the reference bore times the bore ratio -- exactly
1.0 at the design point (the same float over itself), so the anchor
reproduces to the double and only the bore dependence responds away
from it. a_coil is the coil-centre minor radius ('MFE Radial Build'
r_coil_centre, WI-044 D1), the same bore the peak field, the stored
energy and the casing mass read.

The major radius does NOT enter (WI-058 D3). PROCESS-stellarator
(Lion 2021 sec. 2) holds "the coil number and the coil shapes" fixed
and scales "only the overall size of the coils" with the machine,
varying the plasma minor radius "at constant coil radius"; this
radial build instead moves the coil bore with the plasma (a plus a
fixed layer stack), so here the coil's size IS its bore. The two
readings coincide only when the normalized coil-bore and major-radius
ratios agree. Fixed plasma aspect ratio alone does not ensure that
equality with the held1.85m non-plasma radial stack. What
grows with R at fixed bore is the toroidal coil-coil spacing, which
PROCESS checks as a clearance (d_min(C) scaling with R, sec. 3.10),
not a length; this model carries no such check -- disclosed, not
modelled. Supersedes WI-036 D3 (c_coil = k_coil * R0), whose R-form
agrees with this form under that normalized-ratio equality.

The residual held quantity is the printed 25 m itself (c_coil_ref),
"typical but approximate" -- the weak link WI-036 carried. The
implied shape factor c_coil_ref / (2 pi a_coil_ref) = 1.2631... is
the coil's departure from a circle at its centre radius (a 7 x 5 m
face against a 6.3 m circle) and is disclosed here, not bound.
Per-coil circumferences are unprinted; one typical value carries
the set.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/output.md
*Ref**: stellaris-design-details.md L1862 / raw.pdf sec. 2.9
("approximate size of 7 x 5 x 10 m, with a typical
circumference of 25 m"); Lion 2021 output.md L118-120 (the
scaling prescription: coil shapes fixed, overall coil size
scaled, a at constant coil radius), L621 (sec. 3.10, the
coil-coil clearance d_min(C) scaling with R); WI-044 design D1
(the coil-centre bore)
*Basis**: fixed-shape coil scaled to its bore, anchored at the
printed circumference; concept-agnostic (MR-3)

Inputs:
    - c_coil_ref: c_coil_ref parameter
    - a_coil: a_coil parameter
    - a_coil_ref: a_coil_ref parameter

Outputs:
    - c_coil: c_coil result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:154

SysML Source: root-0/analyses/mfe_magnet_field.sysml:154

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_magnet_field/coil_winding_length_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float


class Coil_Winding_LengthInput(BaseModel):
    """Input model for Coil_Winding_LengthModule.

    Attributes:
        c_coil_ref: c_coil_ref input
        a_coil: a_coil input
        a_coil_ref: a_coil_ref input
    """
    c_coil_ref: float = Field(..., description="c_coil_ref input")
    a_coil: float = Field(..., description="a_coil input")
    a_coil_ref: float = Field(..., description="a_coil_ref input")


class Coil_Winding_LengthModule(ModuleBase[Coil_Winding_LengthInput, Float]):
    """TEAx module for Coil_Winding_Length calculation.

Typical coil winding circumference [m] from the coil bore (WI-058):

  c_coil = c_coil_ref * (a_coil / a_coil_ref)

The coil's size is stated on its bore: Stellaris prints the coils as
"approximate size of 7 x 5 x 10 m, with a typical circumference of
25 m", around a coil-centre minor radius of 3.15 m in this radial
build. A coil of fixed shape scaled to its bore has a circumference
proportional to the bore radius, so the length is the printed
circumference at the reference bore times the bore ratio -- exactly
1.0 at the design point (the same float over itself), so the anchor
reproduces to the double and only the bore dependence responds away
from it. a_coil is the coil-centre minor radius ('MFE Radial Build'
r_coil_centre, WI-044 D1), the same bore the peak field, the stored
energy and the casing mass read.

The major radius does NOT enter (WI-058 D3). PROCESS-stellarator
(Lion 2021 sec. 2) holds "the coil number and the coil shapes" fixed
and scales "only the overall size of the coils" with the machine,
varying the plasma minor radius "at constant coil radius"; this
radial build instead moves the coil bore with the plasma (a plus a
fixed layer stack), so here the coil's size IS its bore. The two
readings coincide only when the normalized coil-bore and major-radius
ratios agree. Fixed plasma aspect ratio alone does not ensure that
equality with the held1.85m non-plasma radial stack. What
grows with R at fixed bore is the toroidal coil-coil spacing, which
PROCESS checks as a clearance (d_min(C) scaling with R, sec. 3.10),
not a length; this model carries no such check -- disclosed, not
modelled. Supersedes WI-036 D3 (c_coil = k_coil * R0), whose R-form
agrees with this form under that normalized-ratio equality.

The residual held quantity is the printed 25 m itself (c_coil_ref),
"typical but approximate" -- the weak link WI-036 carried. The
implied shape factor c_coil_ref / (2 pi a_coil_ref) = 1.2631... is
the coil's departure from a circle at its centre radius (a 7 x 5 m
face against a 6.3 m circle) and is disclosed here, not bound.
Per-coil circumferences are unprinted; one typical value carries
the set.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/output.md
*Ref**: stellaris-design-details.md L1862 / raw.pdf sec. 2.9
("approximate size of 7 x 5 x 10 m, with a typical
circumference of 25 m"); Lion 2021 output.md L118-120 (the
scaling prescription: coil shapes fixed, overall coil size
scaled, a at constant coil radius), L621 (sec. 3.10, the
coil-coil clearance d_min(C) scaling with R); WI-044 design D1
(the coil-centre bore)
*Basis**: fixed-shape coil scaled to its bore, anchored at the
printed circumference; concept-agnostic (MR-3)

Inputs:
    - c_coil_ref: c_coil_ref parameter
    - a_coil: a_coil parameter
    - a_coil_ref: a_coil_ref parameter

Outputs:
    - c_coil: c_coil result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:154

    SysML Source: root-0/analyses/mfe_magnet_field.sysml:154

    Calculation Specification:
        c_coil = c_coil_ref * (a_coil / a_coil_ref)
        
Documentation:
Typical coil winding circumference [m] from the coil bore (WI-058):

  c_coil = c_coil_ref * (a_coil / a_coil_ref)

The coil's size is stated on its bore: Stellaris prints the coils as
"approximate size of 7 x 5 x 10 m, with a typical circumference of
25 m", around a coil-centre minor radius of 3.15 m in this radial
build. A coil of fixed shape scaled to its bore has a circumference
proportional to the bore radius, so the length is the printed
circumference at the reference bore times the bore ratio -- exactly
1.0 at the design point (the same float over itself), so the anchor
reproduces to the double and only the bore dependence responds away
from it. a_coil is the coil-centre minor radius ('MFE Radial Build'
r_coil_centre, WI-044 D1), the same bore the peak field, the stored
energy and the casing mass read.

The major radius does NOT enter (WI-058 D3). PROCESS-stellarator
(Lion 2021 sec. 2) holds "the coil number and the coil shapes" fixed
and scales "only the overall size of the coils" with the machine,
varying the plasma minor radius "at constant coil radius"; this
radial build instead moves the coil bore with the plasma (a plus a
fixed layer stack), so here the coil's size IS its bore. The two
readings coincide only when the normalized coil-bore and major-radius
ratios agree. Fixed plasma aspect ratio alone does not ensure that
equality with the held1.85m non-plasma radial stack. What
grows with R at fixed bore is the toroidal coil-coil spacing, which
PROCESS checks as a clearance (d_min(C) scaling with R, sec. 3.10),
not a length; this model carries no such check -- disclosed, not
modelled. Supersedes WI-036 D3 (c_coil = k_coil * R0), whose R-form
agrees with this form under that normalized-ratio equality.

The residual held quantity is the printed 25 m itself (c_coil_ref),
"typical but approximate" -- the weak link WI-036 carried. The
implied shape factor c_coil_ref / (2 pi a_coil_ref) = 1.2631... is
the coil's departure from a circle at its centre radius (a 7 x 5 m
face against a 6.3 m circle) and is disclosed here, not bound.
Per-coil circumferences are unprinted; one typical value carries
the set.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/output.md
*Ref**: stellaris-design-details.md L1862 / raw.pdf sec. 2.9
("approximate size of 7 x 5 x 10 m, with a typical
circumference of 25 m"); Lion 2021 output.md L118-120 (the
scaling prescription: coil shapes fixed, overall coil size
scaled, a at constant coil radius), L621 (sec. 3.10, the
coil-coil clearance d_min(C) scaling with R); WI-044 design D1
(the coil-centre bore)
*Basis**: fixed-shape coil scaled to its bore, anchored at the
printed circumference; concept-agnostic (MR-3)

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.mfe_magnet_field.coil_winding_length_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Coil_Winding_LengthModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, c_coil_ref: float, a_coil: float, a_coil_ref: float    ) -> Coil_Winding_LengthInput:
        """Validate inputs and fill defaults.

        Args:
            c_coil_ref: c_coil_ref input
            a_coil: a_coil input
            a_coil_ref: a_coil_ref input

        Returns:
            Validated input model
        """
        return Coil_Winding_LengthInput(c_coil_ref=c_coil_ref, a_coil=a_coil, a_coil_ref=a_coil_ref)

    def run(
        self, c_coil_ref: float, a_coil: float, a_coil_ref: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            c_coil_ref: c_coil_ref input
            a_coil: a_coil input
            a_coil_ref: a_coil_ref input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(c_coil_ref, a_coil, a_coil_ref)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.mfe_magnet_field.coil_winding_length_impl import (
            run_coil_winding_length,
        )

        # Execute implementation - returns single value
        c_coil = run_coil_winding_length(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(c_coil))
