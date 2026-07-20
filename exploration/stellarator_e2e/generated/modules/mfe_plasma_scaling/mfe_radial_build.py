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
(owner Option 1, WI-021) — engineered annuli are sized by the radial
build, not the plasma cross-section. ARIES/Starfire-lineage geometry,
admissible per PROTOCOL.md section 3.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py
*Ref**: geometry.py:67-81 (torus shell + surface area), 106-118
(cumulative radii), 156-170 (per-layer volumes); model.py:1205-1208
(CAS22 aggregation)
*Basis**: forward radial build; torus branch; MFE-generic

Inputs:
    - R: R parameter
    - a: a parameter
    - kappa: kappa parameter
    - pi: pi parameter
    - vacuum_t: vacuum_t parameter
    - firstwall_t: firstwall_t parameter
    - blanket_t: blanket_t parameter
    - reflector_t: reflector_t parameter
    - ht_shield_t: ht_shield_t parameter
    - structure_t: structure_t parameter
    - gap1_t: gap1_t parameter
    - vessel_t: vessel_t parameter
    - coil_t: coil_t parameter
    - gap2_t: gap2_t parameter
    - lt_shield_t: lt_shield_t parameter

Outputs:
    - blanket_vol: blanket_vol result
    - shield_vol: shield_vol result
    - structure_vol: structure_vol result
    - vessel_vol: vessel_vol result
    - wall_area: wall_area result
    - r_coil: r_coil result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:41

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:41

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
        R: R input
        a: a input
        kappa: kappa input
        pi: pi input
        vacuum_t: vacuum_t input
        firstwall_t: firstwall_t input
        blanket_t: blanket_t input
        reflector_t: reflector_t input
        ht_shield_t: ht_shield_t input
        structure_t: structure_t input
        gap1_t: gap1_t input
        vessel_t: vessel_t input
        coil_t: coil_t input
        gap2_t: gap2_t input
        lt_shield_t: lt_shield_t input
    """
    R: float = Field(..., description="R input")
    a: float = Field(..., description="a input")
    kappa: float = Field(..., description="kappa input")
    pi: float = Field(..., description="pi input")
    vacuum_t: float = Field(..., description="vacuum_t input")
    firstwall_t: float = Field(..., description="firstwall_t input")
    blanket_t: float = Field(..., description="blanket_t input")
    reflector_t: float = Field(..., description="reflector_t input")
    ht_shield_t: float = Field(..., description="ht_shield_t input")
    structure_t: float = Field(..., description="structure_t input")
    gap1_t: float = Field(..., description="gap1_t input")
    vessel_t: float = Field(..., description="vessel_t input")
    coil_t: float = Field(..., description="coil_t input")
    gap2_t: float = Field(..., description="gap2_t input")
    lt_shield_t: float = Field(..., description="lt_shield_t input")


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
(owner Option 1, WI-021) — engineered annuli are sized by the radial
build, not the plasma cross-section. ARIES/Starfire-lineage geometry,
admissible per PROTOCOL.md section 3.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py
*Ref**: geometry.py:67-81 (torus shell + surface area), 106-118
(cumulative radii), 156-170 (per-layer volumes); model.py:1205-1208
(CAS22 aggregation)
*Basis**: forward radial build; torus branch; MFE-generic

Inputs:
    - R: R parameter
    - a: a parameter
    - kappa: kappa parameter
    - pi: pi parameter
    - vacuum_t: vacuum_t parameter
    - firstwall_t: firstwall_t parameter
    - blanket_t: blanket_t parameter
    - reflector_t: reflector_t parameter
    - ht_shield_t: ht_shield_t parameter
    - structure_t: structure_t parameter
    - gap1_t: gap1_t parameter
    - vessel_t: vessel_t parameter
    - coil_t: coil_t parameter
    - gap2_t: gap2_t parameter
    - lt_shield_t: lt_shield_t parameter

Outputs:
    - blanket_vol: blanket_vol result
    - shield_vol: shield_vol result
    - structure_vol: structure_vol result
    - vessel_vol: vessel_vol result
    - wall_area: wall_area result
    - r_coil: r_coil result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:41

    SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:41

    Calculation Specification:
        pi = 3.14159265358979
        vacuum_or = a + vacuum_t
        firstwall_or = vacuum_or + firstwall_t
        blanket_or = firstwall_or + blanket_t
        reflector_or = blanket_or + reflector_t
        ht_shield_or = reflector_or + ht_shield_t
        structure_or = ht_shield_or + structure_t
        gap1_or = structure_or + gap1_t
        vessel_or = gap1_or + vessel_t
        coil_or = vessel_or + coil_t
        gap2_or = coil_or + gap2_t
        lt_shield_or = gap2_or + lt_shield_t
        C = kappa * 2.0 * pi ** 2 * R
        firstwall_vol = C * (firstwall_or ** 2 - vacuum_or ** 2)
        blanket_layer_vol = C * (blanket_or ** 2 - firstwall_or ** 2)
        reflector_vol = C * (reflector_or ** 2 - blanket_or ** 2)
        ht_shield_vol = C * (ht_shield_or ** 2 - reflector_or ** 2)
        lt_shield_vol = C * (lt_shield_or ** 2 - gap2_or ** 2)
        blanket_vol = firstwall_vol + blanket_layer_vol + reflector_vol
        shield_vol = ht_shield_vol + lt_shield_vol
        structure_vol = C * (structure_or ** 2 - ht_shield_or ** 2)
        vessel_vol = C * (vessel_or ** 2 - gap1_or ** 2)
        wall_area = kappa * 4.0 * pi ** 2 * R * vacuum_or
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
(owner Option 1, WI-021) — engineered annuli are sized by the radial
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
    TEAx automatically extracts blanket_vol, shield_vol, structure_vol, vessel_vol, wall_area, r_coil fields to separate channels.
    """

    name: str = "MFE_Radial_BuildModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, R: float, a: float, kappa: float, pi: float, vacuum_t: float, firstwall_t: float, blanket_t: float, reflector_t: float, ht_shield_t: float, structure_t: float, gap1_t: float, vessel_t: float, coil_t: float, gap2_t: float, lt_shield_t: float    ) -> MFE_Radial_BuildInput:
        """Validate inputs and fill defaults.

        Args:
            R: R input
            a: a input
            kappa: kappa input
            pi: pi input
            vacuum_t: vacuum_t input
            firstwall_t: firstwall_t input
            blanket_t: blanket_t input
            reflector_t: reflector_t input
            ht_shield_t: ht_shield_t input
            structure_t: structure_t input
            gap1_t: gap1_t input
            vessel_t: vessel_t input
            coil_t: coil_t input
            gap2_t: gap2_t input
            lt_shield_t: lt_shield_t input

        Returns:
            Validated input model
        """
        return MFE_Radial_BuildInput(R=R, a=a, kappa=kappa, pi=pi, vacuum_t=vacuum_t, firstwall_t=firstwall_t, blanket_t=blanket_t, reflector_t=reflector_t, ht_shield_t=ht_shield_t, structure_t=structure_t, gap1_t=gap1_t, vessel_t=vessel_t, coil_t=coil_t, gap2_t=gap2_t, lt_shield_t=lt_shield_t)

    def run(
        self, R: float, a: float, kappa: float, pi: float, vacuum_t: float, firstwall_t: float, blanket_t: float, reflector_t: float, ht_shield_t: float, structure_t: float, gap1_t: float, vessel_t: float, coil_t: float, gap2_t: float, lt_shield_t: float    ) -> ModuleResult[MFE_Radial_BuildOutput]:
        """Execute calculation.

        Args:
            R: R input
            a: a input
            kappa: kappa input
            pi: pi input
            vacuum_t: vacuum_t input
            firstwall_t: firstwall_t input
            blanket_t: blanket_t input
            reflector_t: reflector_t input
            ht_shield_t: ht_shield_t input
            structure_t: structure_t input
            gap1_t: gap1_t input
            vessel_t: vessel_t input
            coil_t: coil_t input
            gap2_t: gap2_t input
            lt_shield_t: lt_shield_t input

        Returns:
            Module result with MFE_Radial_BuildOutput (blanket_vol, shield_vol, structure_vol, vessel_vol, wall_area, r_coil)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(R, a, kappa, pi, vacuum_t, firstwall_t, blanket_t, reflector_t, ht_shield_t, structure_t, gap1_t, vessel_t, coil_t, gap2_t, lt_shield_t)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plasma_scaling.mfe_radial_build_impl import (
            run_mfe_radial_build,
        )

        # Execute implementation - returns tuple of values
        blanket_vol, shield_vol, structure_vol, vessel_vol, wall_area, r_coil = run_mfe_radial_build(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=MFE_Radial_BuildOutput(
                blanket_vol=blanket_vol,
                shield_vol=shield_vol,
                structure_vol=structure_vol,
                vessel_vol=vessel_vol,
                wall_area=wall_area,
                r_coil=r_coil,
            )
        )
