"""Winding_Pack_StressModule Module Wrapper

TEAx module for Winding_Pack_Stress calculation.

Mean winding-pack stress scale [Pa] in the J x B x d form (WI-035):

  sigma_wp = k_sigma * I_coil * B_peak_in / wp_side

Domain: wp_side != 0. Native typed manual completion raises
ValueError for a zero denominator before evaluating the stated equation.
A locally zero-sized pack has no defined stress in this expression.

Force density (current x field) over the load-bearing dimension --
the standard mean-stress scale for a winding. k_sigma is a held
coil-set structural concentration fact (float64 anchored at the
printed worst-coil pair: <650 MPa at I 15.4 MA, B_peak 24.9 T,
side 0.36 m; the printed "<650" bound is taken AS the value,
conservative). The operand responds as I * B_peak / side --
quadratic at fixed side once B_peak follows the derived field --
so the paired limit pushes back on both field choice and winding-pack
sizing (rubric Row 3 P3).

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: images/page_022_table_0.png (Table 8: "Peak stress on WP
[MPa] <650"; I, side lengths); raw.pdf sec. 2.9 structural
analysis (peak stresses ~600 MPa, axisymmetric I x B model)
*Basis**: J x B x d mean-stress scale with a held, sourced
concentration fact; concept-agnostic (MR-3)

Inputs:
    - B_peak_in: B_peak_in parameter
    - k_sigma: k_sigma parameter
    - wp_side: wp_side parameter
    - I_coil: I_coil parameter

Outputs:
    - sigma_wp: sigma_wp result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:60

SysML Source: root-0/analyses/mfe_magnet_field.sysml:60

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_magnet_field/winding_pack_stress_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_reference_tea.primitives import Float


class Winding_Pack_StressInput(BaseModel):
    """Input model for Winding_Pack_StressModule.

    Attributes:
        B_peak_in: B_peak_in input
        k_sigma: k_sigma input
        wp_side: wp_side input
        I_coil: I_coil input
    """
    B_peak_in: float = Field(..., description="B_peak_in input")
    k_sigma: float = Field(..., description="k_sigma input")
    wp_side: float = Field(..., description="wp_side input")
    I_coil: float = Field(..., description="I_coil input")


class Winding_Pack_StressModule(ModuleBase[Winding_Pack_StressInput, Float]):
    """TEAx module for Winding_Pack_Stress calculation.

Mean winding-pack stress scale [Pa] in the J x B x d form (WI-035):

  sigma_wp = k_sigma * I_coil * B_peak_in / wp_side

Domain: wp_side != 0. Native typed manual completion raises
ValueError for a zero denominator before evaluating the stated equation.
A locally zero-sized pack has no defined stress in this expression.

Force density (current x field) over the load-bearing dimension --
the standard mean-stress scale for a winding. k_sigma is a held
coil-set structural concentration fact (float64 anchored at the
printed worst-coil pair: <650 MPa at I 15.4 MA, B_peak 24.9 T,
side 0.36 m; the printed "<650" bound is taken AS the value,
conservative). The operand responds as I * B_peak / side --
quadratic at fixed side once B_peak follows the derived field --
so the paired limit pushes back on both field choice and winding-pack
sizing (rubric Row 3 P3).

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: images/page_022_table_0.png (Table 8: "Peak stress on WP
[MPa] <650"; I, side lengths); raw.pdf sec. 2.9 structural
analysis (peak stresses ~600 MPa, axisymmetric I x B model)
*Basis**: J x B x d mean-stress scale with a held, sourced
concentration fact; concept-agnostic (MR-3)

Inputs:
    - B_peak_in: B_peak_in parameter
    - k_sigma: k_sigma parameter
    - wp_side: wp_side parameter
    - I_coil: I_coil parameter

Outputs:
    - sigma_wp: sigma_wp result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:60

    SysML Source: root-0/analyses/mfe_magnet_field.sysml:60

    Calculation Specification:
        See documentation:
Mean winding-pack stress scale [Pa] in the J x B x d form (WI-035):

  sigma_wp = k_sigma * I_coil * B_peak_in / wp_side

Domain: wp_side != 0. Native typed manual completion raises
ValueError for a zero denominator before evaluating the stated equation.
A locally zero-sized pack has no defined stress in this expression.

Force density (current x field) over the load-bearing dimension --
the standard mean-stress scale for a winding. k_sigma is a held
coil-set structural concentration fact (float64 anchored at the
printed worst-coil pair: <650 MPa at I 15.4 MA, B_peak 24.9 T,
side 0.36 m; the printed "<650" bound is taken AS the value,
conservative). The operand responds as I * B_peak / side --
quadratic at fixed side once B_peak follows the derived field --
so the paired limit pushes back on both field choice and winding-pack
sizing (rubric Row 3 P3).

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: images/page_022_table_0.png (Table 8: "Peak stress on WP
[MPa] <650"; I, side lengths); raw.pdf sec. 2.9 structural
analysis (peak stresses ~600 MPa, axisymmetric I x B model)
*Basis**: J x B x d mean-stress scale with a held, sourced
concentration fact; concept-agnostic (MR-3)

    IMPLEMENTATION: See stellarator_materials_reference_tea.handwritten.mfe_magnet_field.winding_pack_stress_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Winding_Pack_StressModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, B_peak_in: float, k_sigma: float, wp_side: float, I_coil: float    ) -> Winding_Pack_StressInput:
        """Validate inputs and fill defaults.

        Args:
            B_peak_in: B_peak_in input
            k_sigma: k_sigma input
            wp_side: wp_side input
            I_coil: I_coil input

        Returns:
            Validated input model
        """
        return Winding_Pack_StressInput(B_peak_in=B_peak_in, k_sigma=k_sigma, wp_side=wp_side, I_coil=I_coil)

    def run(
        self, B_peak_in: float, k_sigma: float, wp_side: float, I_coil: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            B_peak_in: B_peak_in input
            k_sigma: k_sigma input
            wp_side: wp_side input
            I_coil: I_coil input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(B_peak_in, k_sigma, wp_side, I_coil)

        # Import handwritten implementation
        from stellarator_materials_reference_tea.handwritten.mfe_magnet_field.winding_pack_stress_impl import (
            run_winding_pack_stress,
        )

        # Execute implementation - returns single value
        sigma_wp = run_winding_pack_stress(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(sigma_wp))
