"""Conductor_Field_CapabilityModule Module Wrapper

TEAx module for Conductor_Field_Capability calculation.

Relative conductor quantity for a selected design field envelope, distinct from actual peak-field demand. Normative manual equations: quantity_factor = (B_design / B_reference)^field_exponent; j_wp_effective = j_reference / quantity_factor.
Inputs: B_design and B_reference T, field_exponent dimensionless, j_reference A/mm^2. Outputs: quantity_factor dimensionless and j_wp_effective A/mm^2. The enlarged fixed-composition pack determines purchased tape volume; this calculation carries no price. Hold tape construction, temperature, angular assumption and composition fixed for the relative-envelope interpretation.
Changing reference density on unchanged tape changes operating current per tape. Lower density purchases more tape; higher density consumes unknown current margin. Manufacturing-performance improvement, packing changes and grading require different scenario evidence. Reference-coil loading is j_wp_effective * tape_area / tape_fraction; set-effective loading also includes f_set/f_wp_vol because current and pack-volume distribution factors are distinct transfer approximations. No absolute current margin, qualified field capability or pack/casing fit is established by this model.
The source's approximate 20 K exponent has no stated fit interval; Fig. 1a measurements extend to approximately 24 T, below the 24.9 T reference. The selected 20-30 T sensitivity is extrapolative. Numerical domain: finite positive inputs, field ratio, quantity factor and effective density. Typed completion raises calculation- and quantity-named ValueError for invalid inputs, overflow and positive-output underflow. Equal fields give quantity_factor exactly one.
*Source**: knowledge/sources/development_and_large_volume_production_of_extremely_high/raw.pdf
*Reference**: Molodyk et al. (2021), printed p. 5 (approximate critical-current field exponent 0.6 at 20 K); Fig. 1 (tape-level field measurements). Inverse relative-current-density law at fixed operating fraction; uniform fixed-composition pack enlargement and unchanged reference unit-tape economics are agent assumptions.
*Last Updated**: 2026-09-15

Inputs:
    - B_reference: B_reference parameter
    - field_exponent: field_exponent parameter
    - j_reference: j_reference parameter
    - B_design: B_design parameter

Outputs:
    - quantity_factor: quantity_factor result
    - j_wp_effective: j_wp_effective result

SysML Source: root-0/analyses/mfe_conductor_grade.sysml:4

SysML Source: root-0/analyses/mfe_conductor_grade.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_conductor_grade/conductor_field_capability_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float
from stellarator_tea.schemas.conductor_field_capability_output import Conductor_Field_CapabilityOutput


class Conductor_Field_CapabilityInput(BaseModel):
    """Input model for Conductor_Field_CapabilityModule.

    Attributes:
        B_reference: B_reference input
        field_exponent: field_exponent input
        j_reference: j_reference input
        B_design: B_design input
    """
    B_reference: float = Field(..., description="B_reference input")
    field_exponent: float = Field(..., description="field_exponent input")
    j_reference: float = Field(..., description="j_reference input")
    B_design: float = Field(..., description="B_design input")


class Conductor_Field_CapabilityModule(ModuleBase[Conductor_Field_CapabilityInput, Conductor_Field_CapabilityOutput]):
    """TEAx module for Conductor_Field_Capability calculation.

Relative conductor quantity for a selected design field envelope, distinct from actual peak-field demand. Normative manual equations: quantity_factor = (B_design / B_reference)^field_exponent; j_wp_effective = j_reference / quantity_factor.
Inputs: B_design and B_reference T, field_exponent dimensionless, j_reference A/mm^2. Outputs: quantity_factor dimensionless and j_wp_effective A/mm^2. The enlarged fixed-composition pack determines purchased tape volume; this calculation carries no price. Hold tape construction, temperature, angular assumption and composition fixed for the relative-envelope interpretation.
Changing reference density on unchanged tape changes operating current per tape. Lower density purchases more tape; higher density consumes unknown current margin. Manufacturing-performance improvement, packing changes and grading require different scenario evidence. Reference-coil loading is j_wp_effective * tape_area / tape_fraction; set-effective loading also includes f_set/f_wp_vol because current and pack-volume distribution factors are distinct transfer approximations. No absolute current margin, qualified field capability or pack/casing fit is established by this model.
The source's approximate 20 K exponent has no stated fit interval; Fig. 1a measurements extend to approximately 24 T, below the 24.9 T reference. The selected 20-30 T sensitivity is extrapolative. Numerical domain: finite positive inputs, field ratio, quantity factor and effective density. Typed completion raises calculation- and quantity-named ValueError for invalid inputs, overflow and positive-output underflow. Equal fields give quantity_factor exactly one.
*Source**: knowledge/sources/development_and_large_volume_production_of_extremely_high/raw.pdf
*Reference**: Molodyk et al. (2021), printed p. 5 (approximate critical-current field exponent 0.6 at 20 K); Fig. 1 (tape-level field measurements). Inverse relative-current-density law at fixed operating fraction; uniform fixed-composition pack enlargement and unchanged reference unit-tape economics are agent assumptions.
*Last Updated**: 2026-09-15

Inputs:
    - B_reference: B_reference parameter
    - field_exponent: field_exponent parameter
    - j_reference: j_reference parameter
    - B_design: B_design parameter

Outputs:
    - quantity_factor: quantity_factor result
    - j_wp_effective: j_wp_effective result

SysML Source: root-0/analyses/mfe_conductor_grade.sysml:4

    SysML Source: root-0/analyses/mfe_conductor_grade.sysml:4

    Calculation Specification:
        See documentation:
Relative conductor quantity for a selected design field envelope, distinct from actual peak-field demand. Normative manual equations: quantity_factor = (B_design / B_reference)^field_exponent; j_wp_effective = j_reference / quantity_factor.
Inputs: B_design and B_reference T, field_exponent dimensionless, j_reference A/mm^2. Outputs: quantity_factor dimensionless and j_wp_effective A/mm^2. The enlarged fixed-composition pack determines purchased tape volume; this calculation carries no price. Hold tape construction, temperature, angular assumption and composition fixed for the relative-envelope interpretation.
Changing reference density on unchanged tape changes operating current per tape. Lower density purchases more tape; higher density consumes unknown current margin. Manufacturing-performance improvement, packing changes and grading require different scenario evidence. Reference-coil loading is j_wp_effective * tape_area / tape_fraction; set-effective loading also includes f_set/f_wp_vol because current and pack-volume distribution factors are distinct transfer approximations. No absolute current margin, qualified field capability or pack/casing fit is established by this model.
The source's approximate 20 K exponent has no stated fit interval; Fig. 1a measurements extend to approximately 24 T, below the 24.9 T reference. The selected 20-30 T sensitivity is extrapolative. Numerical domain: finite positive inputs, field ratio, quantity factor and effective density. Typed completion raises calculation- and quantity-named ValueError for invalid inputs, overflow and positive-output underflow. Equal fields give quantity_factor exactly one.
*Source**: knowledge/sources/development_and_large_volume_production_of_extremely_high/raw.pdf
*Reference**: Molodyk et al. (2021), printed p. 5 (approximate critical-current field exponent 0.6 at 20 K); Fig. 1 (tape-level field measurements). Inverse relative-current-density law at fixed operating fraction; uniform fixed-composition pack enlargement and unchanged reference unit-tape economics are agent assumptions.
*Last Updated**: 2026-09-15

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_conductor_grade.conductor_field_capability_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts quantity_factor, j_wp_effective fields to separate channels.
    """

    name: str = "Conductor_Field_CapabilityModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, B_reference: float, field_exponent: float, j_reference: float, B_design: float    ) -> Conductor_Field_CapabilityInput:
        """Validate inputs and fill defaults.

        Args:
            B_reference: B_reference input
            field_exponent: field_exponent input
            j_reference: j_reference input
            B_design: B_design input

        Returns:
            Validated input model
        """
        return Conductor_Field_CapabilityInput(B_reference=B_reference, field_exponent=field_exponent, j_reference=j_reference, B_design=B_design)

    def run(
        self, B_reference: float, field_exponent: float, j_reference: float, B_design: float    ) -> ModuleResult[Conductor_Field_CapabilityOutput]:
        """Execute calculation.

        Args:
            B_reference: B_reference input
            field_exponent: field_exponent input
            j_reference: j_reference input
            B_design: B_design input

        Returns:
            Module result with Conductor_Field_CapabilityOutput (quantity_factor, j_wp_effective)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(B_reference, field_exponent, j_reference, B_design)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_conductor_grade.conductor_field_capability_impl import (
            run_conductor_field_capability,
        )

        # Execute implementation - returns tuple of values
        quantity_factor, j_wp_effective = run_conductor_field_capability(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Conductor_Field_CapabilityOutput(
                quantity_factor=quantity_factor,
                j_wp_effective=j_wp_effective,
            )
        )
