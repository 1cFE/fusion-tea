"""Winding_Pack_Casing_FitModule Module Wrapper

TEAx module for Winding_Pack_Casing_Fit calculation.

Conditional local centered and aligned rectangular envelope fit. x is the plasma-face normal approximated as radial; y is transverse/Phi, both normal to conductor centreline. Nominal area wp_side^2 retains the published homogenized envelope; internal sheet inclusion is unresolved. This does not establish bare conductor geometry or global nonplanar alignment.
Normative equations: nominal_x=wp_side*sqrt(aspect_ratio), nominal_y=wp_side/sqrt(aspect_ratio); internal_x=nominal_x*internal_fraction_x and analogously y; pack=nominal+internal; insulated=pack+2*ground_insulation; required=insulated+2*assembly_clearance. cavity_x=radial_allocation-2*wall_thickness; cavity_y=interior_y; exterior_x=radial_allocation; exterior_y=interior_y+2*wall_thickness; margin=cavity-required; minimum_margin=min(margin_x,margin_y). All lengths m; aspect ratio and internal fractions dimensionless.
All inputs/outputs finite; wp_side, aspect_ratio, radial_allocation, interior_y, wall_thickness and cavity_x positive; fractions and other allowances nonnegative. Refuse arithmetic overflow or underflow of positive multiplicative terms deliberately with quantity-named ValueError. Negative finite margins are valid failure results; zero margin passes.
Internal fractions represent excluded-sheet continuous pitch; external ground insulation and assembly allowances are separate, counted per opposing face exactly once. Casing geometry does not reprice wall mass or insulation, resize total supports, or replace inherited thermal-area/stress proxies. Independent coil radial allocation is not resized to fit demand. Common nominal undeformed state only; no contraction, offsets, fillets, route, stress or manufacturing qualification.
*Source**: work/orchestration/goals/winding-pack-casing-fit/evidence/geometry-research.md
*Reference**: Stellaris original PDF pp.22-23 Fig.40/Table8; WI-061 design.md reviewed equations and conditional scenario.
*Last Updated**: 2026-09-15

Inputs:
    - internal_fraction_x: internal_fraction_x parameter
    - wall_thickness: wall_thickness parameter
    - assembly_clearance: assembly_clearance parameter
    - radial_allocation: radial_allocation parameter
    - internal_fraction_y: internal_fraction_y parameter
    - wp_side: wp_side parameter
    - ground_insulation: ground_insulation parameter
    - aspect_ratio: aspect_ratio parameter
    - interior_y: interior_y parameter

Outputs:
    - required_y: required_y result
    - nominal_y: nominal_y result
    - minimum_margin: minimum_margin result
    - margin_x: margin_x result
    - internal_y: internal_y result
    - pack_x: pack_x result
    - exterior_x: exterior_x result
    - cavity_x: cavity_x result
    - nominal_x: nominal_x result
    - cavity_y: cavity_y result
    - exterior_y: exterior_y result
    - insulated_y: insulated_y result
    - margin_y: margin_y result
    - internal_x: internal_x result
    - pack_y: pack_y result
    - required_x: required_x result
    - insulated_x: insulated_x result

SysML Source: root-0/analyses/mfe_winding_pack_fit.sysml:3

SysML Source: root-0/analyses/mfe_winding_pack_fit.sysml:3

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_winding_pack_fit/winding_pack_casing_fit_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float
from stellarator_tea.schemas.winding_pack_casing_fit_output import Winding_Pack_Casing_FitOutput


class Winding_Pack_Casing_FitInput(BaseModel):
    """Input model for Winding_Pack_Casing_FitModule.

    Attributes:
        internal_fraction_x: internal_fraction_x input
        wall_thickness: wall_thickness input
        assembly_clearance: assembly_clearance input
        radial_allocation: radial_allocation input
        internal_fraction_y: internal_fraction_y input
        wp_side: wp_side input
        ground_insulation: ground_insulation input
        aspect_ratio: aspect_ratio input
        interior_y: interior_y input
    """
    internal_fraction_x: float = Field(..., description="internal_fraction_x input")
    wall_thickness: float = Field(..., description="wall_thickness input")
    assembly_clearance: float = Field(..., description="assembly_clearance input")
    radial_allocation: float = Field(..., description="radial_allocation input")
    internal_fraction_y: float = Field(..., description="internal_fraction_y input")
    wp_side: float = Field(..., description="wp_side input")
    ground_insulation: float = Field(..., description="ground_insulation input")
    aspect_ratio: float = Field(..., description="aspect_ratio input")
    interior_y: float = Field(..., description="interior_y input")


class Winding_Pack_Casing_FitModule(ModuleBase[Winding_Pack_Casing_FitInput, Winding_Pack_Casing_FitOutput]):
    """TEAx module for Winding_Pack_Casing_Fit calculation.

Conditional local centered and aligned rectangular envelope fit. x is the plasma-face normal approximated as radial; y is transverse/Phi, both normal to conductor centreline. Nominal area wp_side^2 retains the published homogenized envelope; internal sheet inclusion is unresolved. This does not establish bare conductor geometry or global nonplanar alignment.
Normative equations: nominal_x=wp_side*sqrt(aspect_ratio), nominal_y=wp_side/sqrt(aspect_ratio); internal_x=nominal_x*internal_fraction_x and analogously y; pack=nominal+internal; insulated=pack+2*ground_insulation; required=insulated+2*assembly_clearance. cavity_x=radial_allocation-2*wall_thickness; cavity_y=interior_y; exterior_x=radial_allocation; exterior_y=interior_y+2*wall_thickness; margin=cavity-required; minimum_margin=min(margin_x,margin_y). All lengths m; aspect ratio and internal fractions dimensionless.
All inputs/outputs finite; wp_side, aspect_ratio, radial_allocation, interior_y, wall_thickness and cavity_x positive; fractions and other allowances nonnegative. Refuse arithmetic overflow or underflow of positive multiplicative terms deliberately with quantity-named ValueError. Negative finite margins are valid failure results; zero margin passes.
Internal fractions represent excluded-sheet continuous pitch; external ground insulation and assembly allowances are separate, counted per opposing face exactly once. Casing geometry does not reprice wall mass or insulation, resize total supports, or replace inherited thermal-area/stress proxies. Independent coil radial allocation is not resized to fit demand. Common nominal undeformed state only; no contraction, offsets, fillets, route, stress or manufacturing qualification.
*Source**: work/orchestration/goals/winding-pack-casing-fit/evidence/geometry-research.md
*Reference**: Stellaris original PDF pp.22-23 Fig.40/Table8; WI-061 design.md reviewed equations and conditional scenario.
*Last Updated**: 2026-09-15

Inputs:
    - internal_fraction_x: internal_fraction_x parameter
    - wall_thickness: wall_thickness parameter
    - assembly_clearance: assembly_clearance parameter
    - radial_allocation: radial_allocation parameter
    - internal_fraction_y: internal_fraction_y parameter
    - wp_side: wp_side parameter
    - ground_insulation: ground_insulation parameter
    - aspect_ratio: aspect_ratio parameter
    - interior_y: interior_y parameter

Outputs:
    - required_y: required_y result
    - nominal_y: nominal_y result
    - minimum_margin: minimum_margin result
    - margin_x: margin_x result
    - internal_y: internal_y result
    - pack_x: pack_x result
    - exterior_x: exterior_x result
    - cavity_x: cavity_x result
    - nominal_x: nominal_x result
    - cavity_y: cavity_y result
    - exterior_y: exterior_y result
    - insulated_y: insulated_y result
    - margin_y: margin_y result
    - internal_x: internal_x result
    - pack_y: pack_y result
    - required_x: required_x result
    - insulated_x: insulated_x result

SysML Source: root-0/analyses/mfe_winding_pack_fit.sysml:3

    SysML Source: root-0/analyses/mfe_winding_pack_fit.sysml:3

    Calculation Specification:
        See documentation:
Conditional local centered and aligned rectangular envelope fit. x is the plasma-face normal approximated as radial; y is transverse/Phi, both normal to conductor centreline. Nominal area wp_side^2 retains the published homogenized envelope; internal sheet inclusion is unresolved. This does not establish bare conductor geometry or global nonplanar alignment.
Normative equations: nominal_x=wp_side*sqrt(aspect_ratio), nominal_y=wp_side/sqrt(aspect_ratio); internal_x=nominal_x*internal_fraction_x and analogously y; pack=nominal+internal; insulated=pack+2*ground_insulation; required=insulated+2*assembly_clearance. cavity_x=radial_allocation-2*wall_thickness; cavity_y=interior_y; exterior_x=radial_allocation; exterior_y=interior_y+2*wall_thickness; margin=cavity-required; minimum_margin=min(margin_x,margin_y). All lengths m; aspect ratio and internal fractions dimensionless.
All inputs/outputs finite; wp_side, aspect_ratio, radial_allocation, interior_y, wall_thickness and cavity_x positive; fractions and other allowances nonnegative. Refuse arithmetic overflow or underflow of positive multiplicative terms deliberately with quantity-named ValueError. Negative finite margins are valid failure results; zero margin passes.
Internal fractions represent excluded-sheet continuous pitch; external ground insulation and assembly allowances are separate, counted per opposing face exactly once. Casing geometry does not reprice wall mass or insulation, resize total supports, or replace inherited thermal-area/stress proxies. Independent coil radial allocation is not resized to fit demand. Common nominal undeformed state only; no contraction, offsets, fillets, route, stress or manufacturing qualification.
*Source**: work/orchestration/goals/winding-pack-casing-fit/evidence/geometry-research.md
*Reference**: Stellaris original PDF pp.22-23 Fig.40/Table8; WI-061 design.md reviewed equations and conditional scenario.
*Last Updated**: 2026-09-15

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_winding_pack_fit.winding_pack_casing_fit_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts required_y, nominal_y, minimum_margin, margin_x, internal_y, pack_x, exterior_x, cavity_x, nominal_x, cavity_y, exterior_y, insulated_y, margin_y, internal_x, pack_y, required_x, insulated_x fields to separate channels.
    """

    name: str = "Winding_Pack_Casing_FitModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, internal_fraction_x: float, wall_thickness: float, assembly_clearance: float, radial_allocation: float, internal_fraction_y: float, wp_side: float, ground_insulation: float, aspect_ratio: float, interior_y: float    ) -> Winding_Pack_Casing_FitInput:
        """Validate inputs and fill defaults.

        Args:
            internal_fraction_x: internal_fraction_x input
            wall_thickness: wall_thickness input
            assembly_clearance: assembly_clearance input
            radial_allocation: radial_allocation input
            internal_fraction_y: internal_fraction_y input
            wp_side: wp_side input
            ground_insulation: ground_insulation input
            aspect_ratio: aspect_ratio input
            interior_y: interior_y input

        Returns:
            Validated input model
        """
        return Winding_Pack_Casing_FitInput(internal_fraction_x=internal_fraction_x, wall_thickness=wall_thickness, assembly_clearance=assembly_clearance, radial_allocation=radial_allocation, internal_fraction_y=internal_fraction_y, wp_side=wp_side, ground_insulation=ground_insulation, aspect_ratio=aspect_ratio, interior_y=interior_y)

    def run(
        self, internal_fraction_x: float, wall_thickness: float, assembly_clearance: float, radial_allocation: float, internal_fraction_y: float, wp_side: float, ground_insulation: float, aspect_ratio: float, interior_y: float    ) -> ModuleResult[Winding_Pack_Casing_FitOutput]:
        """Execute calculation.

        Args:
            internal_fraction_x: internal_fraction_x input
            wall_thickness: wall_thickness input
            assembly_clearance: assembly_clearance input
            radial_allocation: radial_allocation input
            internal_fraction_y: internal_fraction_y input
            wp_side: wp_side input
            ground_insulation: ground_insulation input
            aspect_ratio: aspect_ratio input
            interior_y: interior_y input

        Returns:
            Module result with Winding_Pack_Casing_FitOutput (required_y, nominal_y, minimum_margin, margin_x, internal_y, pack_x, exterior_x, cavity_x, nominal_x, cavity_y, exterior_y, insulated_y, margin_y, internal_x, pack_y, required_x, insulated_x)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(internal_fraction_x, wall_thickness, assembly_clearance, radial_allocation, internal_fraction_y, wp_side, ground_insulation, aspect_ratio, interior_y)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_winding_pack_fit.winding_pack_casing_fit_impl import (
            run_winding_pack_casing_fit,
        )

        # Execute implementation - returns tuple of values
        required_y, nominal_y, minimum_margin, margin_x, internal_y, pack_x, exterior_x, cavity_x, nominal_x, cavity_y, exterior_y, insulated_y, margin_y, internal_x, pack_y, required_x, insulated_x = run_winding_pack_casing_fit(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Winding_Pack_Casing_FitOutput(
                required_y=required_y,
                nominal_y=nominal_y,
                minimum_margin=minimum_margin,
                margin_x=margin_x,
                internal_y=internal_y,
                pack_x=pack_x,
                exterior_x=exterior_x,
                cavity_x=cavity_x,
                nominal_x=nominal_x,
                cavity_y=cavity_y,
                exterior_y=exterior_y,
                insulated_y=insulated_y,
                margin_y=margin_y,
                internal_x=internal_x,
                pack_y=pack_y,
                required_x=required_x,
                insulated_x=insulated_x,
            )
        )
