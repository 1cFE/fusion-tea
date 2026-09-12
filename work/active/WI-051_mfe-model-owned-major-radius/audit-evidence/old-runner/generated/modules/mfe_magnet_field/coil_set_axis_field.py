"""Coil_Set_Axis_FieldModule Module Wrapper

TEAx module for Coil_Set_Axis_Field calculation.

Axis-averaged on-axis field [T] from the coil set's current and
geometry (WI-035, inversion ruling 2026-08-30):

  B_axis = mu0 * k_link * n_coils * I_coil / (two_pi * R0)

k_link is a held coil-set transfer fact (float64 of the printed set),
bundling two printed facts: the per-coil current distribution
(set mean / peak = 643.2/739.2 = 0.870, Table 8 image) and the
axis-linkage of the total (571.5/643.2 = 0.888) -- the modular-coil
shaping current that does not link the magnetic axis (WI-032:
Ampere's law on axis is a lower bound for modular QI coils). At the
Stellaris design set (48 coils, 15.4 MA, R0 12.7 m) the computed
B_axis is 9.0 T minus one ulp; no float64 k_link reproduces 9.0
exactly (+/-6-ulp search), and the low side is bound deliberately so
the conductor-ceiling verdict cannot flip on rounding.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
work/completed/20260827_WI-032_cold-volume-basis/spec.md
*Ref**: images/page_002_table_0.png (Table 2: axis av. field 9.0 T,
peak coil current 15.4 MA, 48 coils, R 12.7 m);
images/page_022_table_0.png (Table 8: per-coil ampere-turns);
WI-032 spec sec. "What G is" (the linkage decomposition)
*Basis**: Ampere's law on the axis with a held, sourced coil-set
linkage fact; concept-agnostic (MR-3) -- all values bound by instances

Inputs:
    - n_coils: n_coils parameter
    - two_pi: two_pi parameter
    - R0: R0 parameter
    - I_coil: I_coil parameter
    - k_link: k_link parameter
    - mu0: mu0 parameter

Outputs:
    - B_axis: B_axis result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:4

SysML Source: root-0/analyses/mfe_magnet_field.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_magnet_field/coil_set_axis_field_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Coil_Set_Axis_FieldInput(BaseModel):
    """Input model for Coil_Set_Axis_FieldModule.

    Attributes:
        n_coils: n_coils input
        two_pi: two_pi input
        R0: R0 input
        I_coil: I_coil input
        k_link: k_link input
        mu0: mu0 input
    """
    n_coils: float = Field(..., description="n_coils input")
    two_pi: float = Field(..., description="two_pi input")
    R0: float = Field(..., description="R0 input")
    I_coil: float = Field(..., description="I_coil input")
    k_link: float = Field(..., description="k_link input")
    mu0: float = Field(..., description="mu0 input")


class Coil_Set_Axis_FieldModule(ModuleBase[Coil_Set_Axis_FieldInput, Float]):
    """TEAx module for Coil_Set_Axis_Field calculation.

Axis-averaged on-axis field [T] from the coil set's current and
geometry (WI-035, inversion ruling 2026-08-30):

  B_axis = mu0 * k_link * n_coils * I_coil / (two_pi * R0)

k_link is a held coil-set transfer fact (float64 of the printed set),
bundling two printed facts: the per-coil current distribution
(set mean / peak = 643.2/739.2 = 0.870, Table 8 image) and the
axis-linkage of the total (571.5/643.2 = 0.888) -- the modular-coil
shaping current that does not link the magnetic axis (WI-032:
Ampere's law on axis is a lower bound for modular QI coils). At the
Stellaris design set (48 coils, 15.4 MA, R0 12.7 m) the computed
B_axis is 9.0 T minus one ulp; no float64 k_link reproduces 9.0
exactly (+/-6-ulp search), and the low side is bound deliberately so
the conductor-ceiling verdict cannot flip on rounding.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
work/completed/20260827_WI-032_cold-volume-basis/spec.md
*Ref**: images/page_002_table_0.png (Table 2: axis av. field 9.0 T,
peak coil current 15.4 MA, 48 coils, R 12.7 m);
images/page_022_table_0.png (Table 8: per-coil ampere-turns);
WI-032 spec sec. "What G is" (the linkage decomposition)
*Basis**: Ampere's law on the axis with a held, sourced coil-set
linkage fact; concept-agnostic (MR-3) -- all values bound by instances

Inputs:
    - n_coils: n_coils parameter
    - two_pi: two_pi parameter
    - R0: R0 parameter
    - I_coil: I_coil parameter
    - k_link: k_link parameter
    - mu0: mu0 parameter

Outputs:
    - B_axis: B_axis result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:4

    SysML Source: root-0/analyses/mfe_magnet_field.sysml:4

    Calculation Specification:
        mu0 = 1.25663706212e-06
        two_pi = 6.283185307179586
        B_axis = mu0 * k_link * n_coils * I_coil / (two_pi * R0)
        
Documentation:
Axis-averaged on-axis field [T] from the coil set's current and
geometry (WI-035, inversion ruling 2026-08-30):

  B_axis = mu0 * k_link * n_coils * I_coil / (two_pi * R0)

k_link is a held coil-set transfer fact (float64 of the printed set),
bundling two printed facts: the per-coil current distribution
(set mean / peak = 643.2/739.2 = 0.870, Table 8 image) and the
axis-linkage of the total (571.5/643.2 = 0.888) -- the modular-coil
shaping current that does not link the magnetic axis (WI-032:
Ampere's law on axis is a lower bound for modular QI coils). At the
Stellaris design set (48 coils, 15.4 MA, R0 12.7 m) the computed
B_axis is 9.0 T minus one ulp; no float64 k_link reproduces 9.0
exactly (+/-6-ulp search), and the low side is bound deliberately so
the conductor-ceiling verdict cannot flip on rounding.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
work/completed/20260827_WI-032_cold-volume-basis/spec.md
*Ref**: images/page_002_table_0.png (Table 2: axis av. field 9.0 T,
peak coil current 15.4 MA, 48 coils, R 12.7 m);
images/page_022_table_0.png (Table 8: per-coil ampere-turns);
WI-032 spec sec. "What G is" (the linkage decomposition)
*Basis**: Ampere's law on the axis with a held, sourced coil-set
linkage fact; concept-agnostic (MR-3) -- all values bound by instances

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_magnet_field.coil_set_axis_field_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Coil_Set_Axis_FieldModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, n_coils: float, two_pi: float, R0: float, I_coil: float, k_link: float, mu0: float    ) -> Coil_Set_Axis_FieldInput:
        """Validate inputs and fill defaults.

        Args:
            n_coils: n_coils input
            two_pi: two_pi input
            R0: R0 input
            I_coil: I_coil input
            k_link: k_link input
            mu0: mu0 input

        Returns:
            Validated input model
        """
        return Coil_Set_Axis_FieldInput(n_coils=n_coils, two_pi=two_pi, R0=R0, I_coil=I_coil, k_link=k_link, mu0=mu0)

    def run(
        self, n_coils: float, two_pi: float, R0: float, I_coil: float, k_link: float, mu0: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            n_coils: n_coils input
            two_pi: two_pi input
            R0: R0 input
            I_coil: I_coil input
            k_link: k_link input
            mu0: mu0 input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(n_coils, two_pi, R0, I_coil, k_link, mu0)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_magnet_field.coil_set_axis_field_impl import (
            run_coil_set_axis_field,
        )

        # Execute implementation - returns single value
        B_axis = run_coil_set_axis_field(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(B_axis))
