"""MFE_Radial_BuildModule Module Wrapper

TEAx module for MFE_Radial_Build calculation.

Forward radial build [m, m^2, m^3] for an MFE torus: cumulative layer
radii from the plasma minor radius outward, then torus-shell volumes and
the first-wall surface area.

  or_i      = or_{i-1} + t_i                              (cumulative radii)
  layer_vol = kappa * 2*pi^2 * R * (or_out^2 - or_in^2)   (torus shell)
  wall_area = kappa * 4*pi^2 * R * vacuum_or              (first-wall SA)

Aggregates match 1costingFE's CAS22 grouping (model.py:1205-1208):
blanket = firstwall+blanket+reflector; shield = ht+lt; structure; vessel.
Concept-agnostic: R major radius, a minor radius (= plasma_t), kappa
elongation, per-layer thicknesses. Pure torus shells, no shape factor
(owner Option 1, WI-021) -- engineered annuli are sized by the radial
build, not the plasma cross-section. ARIES/Starfire-lineage geometry,
admissible per PROTOCOL.md section 3.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py
*Ref**: geometry.py:67-81 (torus shell + surface area), 106-118
(cumulative radii), 156-170 (per-layer volumes); model.py:1205-1208
(CAS22 aggregation)
*Basis**: forward radial build; torus branch; MFE-generic

Inputs:
    - reflector_t_in: reflector_t_in parameter
    - lt_shield_t_in: lt_shield_t_in parameter
    - gap2_t_in: gap2_t_in parameter
    - vacuum_t_in: vacuum_t_in parameter
    - gap1_t_in: gap1_t_in parameter
    - vessel_t_in: vessel_t_in parameter
    - kappa_in: kappa_in parameter
    - blanket_t_in: blanket_t_in parameter
    - R_in: R_in parameter
    - firstwall_t_in: firstwall_t_in parameter
    - coil_t_in: coil_t_in parameter
    - structure_t_in: structure_t_in parameter
    - a_in: a_in parameter
    - pi: pi parameter
    - ht_shield_t_in: ht_shield_t_in parameter

Outputs:
    - wall_area: wall_area result
    - shield_vol: shield_vol result
    - structure_vol: structure_vol result
    - r_coil: r_coil result
    - blanket_vol: blanket_vol result
    - vessel_vol: vessel_vol result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:44

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:44

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plasma_scaling/mfe_radial_build_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float
from stellarator_tea.schemas.mfe_radial_build_output import MFE_Radial_BuildOutput


class MFE_Radial_BuildInput(BaseModel):
    """Input model for MFE_Radial_BuildModule.

    Attributes:
        reflector_t_in: reflector_t_in input
        lt_shield_t_in: lt_shield_t_in input
        gap2_t_in: gap2_t_in input
        vacuum_t_in: vacuum_t_in input
        gap1_t_in: gap1_t_in input
        vessel_t_in: vessel_t_in input
        kappa_in: kappa_in input
        blanket_t_in: blanket_t_in input
        R_in: R_in input
        firstwall_t_in: firstwall_t_in input
        coil_t_in: coil_t_in input
        structure_t_in: structure_t_in input
        a_in: a_in input
        pi: pi input
        ht_shield_t_in: ht_shield_t_in input
    """
    reflector_t_in: float = Field(..., description="reflector_t_in input")
    lt_shield_t_in: float = Field(..., description="lt_shield_t_in input")
    gap2_t_in: float = Field(..., description="gap2_t_in input")
    vacuum_t_in: float = Field(..., description="vacuum_t_in input")
    gap1_t_in: float = Field(..., description="gap1_t_in input")
    vessel_t_in: float = Field(..., description="vessel_t_in input")
    kappa_in: float = Field(..., description="kappa_in input")
    blanket_t_in: float = Field(..., description="blanket_t_in input")
    R_in: float = Field(..., description="R_in input")
    firstwall_t_in: float = Field(..., description="firstwall_t_in input")
    coil_t_in: float = Field(..., description="coil_t_in input")
    structure_t_in: float = Field(..., description="structure_t_in input")
    a_in: float = Field(..., description="a_in input")
    pi: float = Field(..., description="pi input")
    ht_shield_t_in: float = Field(..., description="ht_shield_t_in input")


class MFE_Radial_BuildModule(ModuleBase[MFE_Radial_BuildInput, MFE_Radial_BuildOutput]):
    """TEAx module for MFE_Radial_Build calculation.

Forward radial build [m, m^2, m^3] for an MFE torus: cumulative layer
radii from the plasma minor radius outward, then torus-shell volumes and
the first-wall surface area.

  or_i      = or_{i-1} + t_i                              (cumulative radii)
  layer_vol = kappa * 2*pi^2 * R * (or_out^2 - or_in^2)   (torus shell)
  wall_area = kappa * 4*pi^2 * R * vacuum_or              (first-wall SA)

Aggregates match 1costingFE's CAS22 grouping (model.py:1205-1208):
blanket = firstwall+blanket+reflector; shield = ht+lt; structure; vessel.
Concept-agnostic: R major radius, a minor radius (= plasma_t), kappa
elongation, per-layer thicknesses. Pure torus shells, no shape factor
(owner Option 1, WI-021) -- engineered annuli are sized by the radial
build, not the plasma cross-section. ARIES/Starfire-lineage geometry,
admissible per PROTOCOL.md section 3.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py
*Ref**: geometry.py:67-81 (torus shell + surface area), 106-118
(cumulative radii), 156-170 (per-layer volumes); model.py:1205-1208
(CAS22 aggregation)
*Basis**: forward radial build; torus branch; MFE-generic

Inputs:
    - reflector_t_in: reflector_t_in parameter
    - lt_shield_t_in: lt_shield_t_in parameter
    - gap2_t_in: gap2_t_in parameter
    - vacuum_t_in: vacuum_t_in parameter
    - gap1_t_in: gap1_t_in parameter
    - vessel_t_in: vessel_t_in parameter
    - kappa_in: kappa_in parameter
    - blanket_t_in: blanket_t_in parameter
    - R_in: R_in parameter
    - firstwall_t_in: firstwall_t_in parameter
    - coil_t_in: coil_t_in parameter
    - structure_t_in: structure_t_in parameter
    - a_in: a_in parameter
    - pi: pi parameter
    - ht_shield_t_in: ht_shield_t_in parameter

Outputs:
    - wall_area: wall_area result
    - shield_vol: shield_vol result
    - structure_vol: structure_vol result
    - r_coil: r_coil result
    - blanket_vol: blanket_vol result
    - vessel_vol: vessel_vol result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:44

    SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:44

    Calculation Specification:
        pi = 3.14159265358979
        vacuum_or = a_in + vacuum_t_in
        firstwall_or = vacuum_or + firstwall_t_in
        blanket_or = firstwall_or + blanket_t_in
        reflector_or = blanket_or + reflector_t_in
        ht_shield_or = reflector_or + ht_shield_t_in
        structure_or = ht_shield_or + structure_t_in
        gap1_or = structure_or + gap1_t_in
        vessel_or = gap1_or + vessel_t_in
        coil_or = vessel_or + coil_t_in
        gap2_or = coil_or + gap2_t_in
        lt_shield_or = gap2_or + lt_shield_t_in
        C = kappa_in * 2.0 * pi ** 2 * R_in
        firstwall_vol = C * (firstwall_or ** 2 - vacuum_or ** 2)
        blanket_layer_vol = C * (blanket_or ** 2 - firstwall_or ** 2)
        reflector_vol = C * (reflector_or ** 2 - blanket_or ** 2)
        ht_shield_vol = C * (ht_shield_or ** 2 - reflector_or ** 2)
        lt_shield_vol = C * (lt_shield_or ** 2 - gap2_or ** 2)
        blanket_vol = firstwall_vol + blanket_layer_vol + reflector_vol
        shield_vol = ht_shield_vol + lt_shield_vol
        structure_vol = C * (structure_or ** 2 - ht_shield_or ** 2)
        vessel_vol = C * (vessel_or ** 2 - gap1_or ** 2)
        wall_area = kappa_in * 4.0 * pi ** 2 * R_in * vacuum_or
        r_coil = vessel_or
        
Documentation:
Forward radial build [m, m^2, m^3] for an MFE torus: cumulative layer
radii from the plasma minor radius outward, then torus-shell volumes and
the first-wall surface area.

  or_i      = or_{i-1} + t_i                              (cumulative radii)
  layer_vol = kappa * 2*pi^2 * R * (or_out^2 - or_in^2)   (torus shell)
  wall_area = kappa * 4*pi^2 * R * vacuum_or              (first-wall SA)

Aggregates match 1costingFE's CAS22 grouping (model.py:1205-1208):
blanket = firstwall+blanket+reflector; shield = ht+lt; structure; vessel.
Concept-agnostic: R major radius, a minor radius (= plasma_t), kappa
elongation, per-layer thicknesses. Pure torus shells, no shape factor
(owner Option 1, WI-021) -- engineered annuli are sized by the radial
build, not the plasma cross-section. ARIES/Starfire-lineage geometry,
admissible per PROTOCOL.md section 3.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py
*Ref**: geometry.py:67-81 (torus shell + surface area), 106-118
(cumulative radii), 156-170 (per-layer volumes); model.py:1205-1208
(CAS22 aggregation)
*Basis**: forward radial build; torus branch; MFE-generic

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plasma_scaling.mfe_radial_build_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts wall_area, shield_vol, structure_vol, r_coil, blanket_vol, vessel_vol fields to separate channels.
    """

    name: str = "MFE_Radial_BuildModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, reflector_t_in: float, lt_shield_t_in: float, gap2_t_in: float, vacuum_t_in: float, gap1_t_in: float, vessel_t_in: float, kappa_in: float, blanket_t_in: float, R_in: float, firstwall_t_in: float, coil_t_in: float, structure_t_in: float, a_in: float, pi: float, ht_shield_t_in: float    ) -> MFE_Radial_BuildInput:
        """Validate inputs and fill defaults.

        Args:
            reflector_t_in: reflector_t_in input
            lt_shield_t_in: lt_shield_t_in input
            gap2_t_in: gap2_t_in input
            vacuum_t_in: vacuum_t_in input
            gap1_t_in: gap1_t_in input
            vessel_t_in: vessel_t_in input
            kappa_in: kappa_in input
            blanket_t_in: blanket_t_in input
            R_in: R_in input
            firstwall_t_in: firstwall_t_in input
            coil_t_in: coil_t_in input
            structure_t_in: structure_t_in input
            a_in: a_in input
            pi: pi input
            ht_shield_t_in: ht_shield_t_in input

        Returns:
            Validated input model
        """
        return MFE_Radial_BuildInput(reflector_t_in=reflector_t_in, lt_shield_t_in=lt_shield_t_in, gap2_t_in=gap2_t_in, vacuum_t_in=vacuum_t_in, gap1_t_in=gap1_t_in, vessel_t_in=vessel_t_in, kappa_in=kappa_in, blanket_t_in=blanket_t_in, R_in=R_in, firstwall_t_in=firstwall_t_in, coil_t_in=coil_t_in, structure_t_in=structure_t_in, a_in=a_in, pi=pi, ht_shield_t_in=ht_shield_t_in)

    def run(
        self, reflector_t_in: float, lt_shield_t_in: float, gap2_t_in: float, vacuum_t_in: float, gap1_t_in: float, vessel_t_in: float, kappa_in: float, blanket_t_in: float, R_in: float, firstwall_t_in: float, coil_t_in: float, structure_t_in: float, a_in: float, pi: float, ht_shield_t_in: float    ) -> ModuleResult[MFE_Radial_BuildOutput]:
        """Execute calculation.

        Args:
            reflector_t_in: reflector_t_in input
            lt_shield_t_in: lt_shield_t_in input
            gap2_t_in: gap2_t_in input
            vacuum_t_in: vacuum_t_in input
            gap1_t_in: gap1_t_in input
            vessel_t_in: vessel_t_in input
            kappa_in: kappa_in input
            blanket_t_in: blanket_t_in input
            R_in: R_in input
            firstwall_t_in: firstwall_t_in input
            coil_t_in: coil_t_in input
            structure_t_in: structure_t_in input
            a_in: a_in input
            pi: pi input
            ht_shield_t_in: ht_shield_t_in input

        Returns:
            Module result with MFE_Radial_BuildOutput (wall_area, shield_vol, structure_vol, r_coil, blanket_vol, vessel_vol)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(reflector_t_in, lt_shield_t_in, gap2_t_in, vacuum_t_in, gap1_t_in, vessel_t_in, kappa_in, blanket_t_in, R_in, firstwall_t_in, coil_t_in, structure_t_in, a_in, pi, ht_shield_t_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plasma_scaling.mfe_radial_build_impl import (
            run_mfe_radial_build,
        )

        # Execute implementation - returns tuple of values
        wall_area, shield_vol, structure_vol, r_coil, blanket_vol, vessel_vol = run_mfe_radial_build(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=MFE_Radial_BuildOutput(
                wall_area=wall_area,
                shield_vol=shield_vol,
                structure_vol=structure_vol,
                r_coil=r_coil,
                blanket_vol=blanket_vol,
                vessel_vol=vessel_vol,
            )
        )
