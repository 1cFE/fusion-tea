"""Winding_Pack_Cold_VolumeModule Module Wrapper

TEAx module for Winding_Pack_Cold_Volume calculation.

Total winding-pack cold volume [m^3] across the coil set
(WI-036, D2):

  vol_cold_total = f_wp_vol * n_coils * wp_side^2 * c_coil + vol_extra

vol_extra is additional cold volume beyond the winding pack, kept as a
live settable slot so that modelling the winding-pack chain does not
retire the instance's cold-volume input (WI-032 owner ruling); it is
zero for a machine whose printed cold mass is the winding pack.

The model carries one winding pack (the worst coil) while the machine
has six unique cross-sections. f_wp_vol is a held set-distribution
fact -- the ratio of the printed total volume to the worst-coil-uniform
reference -- exactly the shape of the existing f_set coil-current
distribution fact. This moves the six-cross-section arithmetic out of
an instance doc comment and into model content, and gives a wider
winding pack a real cold-mass consequence through the cryoplant chain.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: images/page_022_table_0.png (Table 8: cross-section side
lengths 360/360/340/340/320/300 mm, image-verified); raw.pdf
sec. 2.9 (48 coils = 4 periods x 12, so 8 occurrences of each of
six unique coils; typical circumference 25 m)
*Basis**: sum of per-coil winding-pack volumes expressed as a held
distribution factor on the worst coil; concept-agnostic (MR-3)

Inputs:
    - vol_extra: vol_extra parameter
    - n_coils: n_coils parameter
    - c_coil: c_coil parameter
    - f_wp_vol: f_wp_vol parameter
    - wp_side: wp_side parameter

Outputs:
    - vol_winding_pack: vol_winding_pack result
    - vol_cold_total: vol_cold_total result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:218

SysML Source: root-0/analyses/mfe_magnet_field.sysml:218

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_magnet_field/winding_pack_cold_volume_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.primitives import Float
from stellarator_materials_rebco_tea.schemas.winding_pack_cold_volume_output import Winding_Pack_Cold_VolumeOutput


class Winding_Pack_Cold_VolumeInput(BaseModel):
    """Input model for Winding_Pack_Cold_VolumeModule.

    Attributes:
        vol_extra: vol_extra input
        n_coils: n_coils input
        c_coil: c_coil input
        f_wp_vol: f_wp_vol input
        wp_side: wp_side input
    """
    vol_extra: float = Field(..., description="vol_extra input")
    n_coils: float = Field(..., description="n_coils input")
    c_coil: float = Field(..., description="c_coil input")
    f_wp_vol: float = Field(..., description="f_wp_vol input")
    wp_side: float = Field(..., description="wp_side input")


class Winding_Pack_Cold_VolumeModule(ModuleBase[Winding_Pack_Cold_VolumeInput, Winding_Pack_Cold_VolumeOutput]):
    """TEAx module for Winding_Pack_Cold_Volume calculation.

Total winding-pack cold volume [m^3] across the coil set
(WI-036, D2):

  vol_cold_total = f_wp_vol * n_coils * wp_side^2 * c_coil + vol_extra

vol_extra is additional cold volume beyond the winding pack, kept as a
live settable slot so that modelling the winding-pack chain does not
retire the instance's cold-volume input (WI-032 owner ruling); it is
zero for a machine whose printed cold mass is the winding pack.

The model carries one winding pack (the worst coil) while the machine
has six unique cross-sections. f_wp_vol is a held set-distribution
fact -- the ratio of the printed total volume to the worst-coil-uniform
reference -- exactly the shape of the existing f_set coil-current
distribution fact. This moves the six-cross-section arithmetic out of
an instance doc comment and into model content, and gives a wider
winding pack a real cold-mass consequence through the cryoplant chain.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: images/page_022_table_0.png (Table 8: cross-section side
lengths 360/360/340/340/320/300 mm, image-verified); raw.pdf
sec. 2.9 (48 coils = 4 periods x 12, so 8 occurrences of each of
six unique coils; typical circumference 25 m)
*Basis**: sum of per-coil winding-pack volumes expressed as a held
distribution factor on the worst coil; concept-agnostic (MR-3)

Inputs:
    - vol_extra: vol_extra parameter
    - n_coils: n_coils parameter
    - c_coil: c_coil parameter
    - f_wp_vol: f_wp_vol parameter
    - wp_side: wp_side parameter

Outputs:
    - vol_winding_pack: vol_winding_pack result
    - vol_cold_total: vol_cold_total result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:218

    SysML Source: root-0/analyses/mfe_magnet_field.sysml:218

    Calculation Specification:
        vol_extra = 0.0
        vol_cold_total = f_wp_vol * n_coils * wp_side * wp_side * c_coil + vol_extra
        vol_winding_pack = f_wp_vol * n_coils * wp_side * wp_side * c_coil
        
Documentation:
Total winding-pack cold volume [m^3] across the coil set
(WI-036, D2):

  vol_cold_total = f_wp_vol * n_coils * wp_side^2 * c_coil + vol_extra

vol_extra is additional cold volume beyond the winding pack, kept as a
live settable slot so that modelling the winding-pack chain does not
retire the instance's cold-volume input (WI-032 owner ruling); it is
zero for a machine whose printed cold mass is the winding pack.

The model carries one winding pack (the worst coil) while the machine
has six unique cross-sections. f_wp_vol is a held set-distribution
fact -- the ratio of the printed total volume to the worst-coil-uniform
reference -- exactly the shape of the existing f_set coil-current
distribution fact. This moves the six-cross-section arithmetic out of
an instance doc comment and into model content, and gives a wider
winding pack a real cold-mass consequence through the cryoplant chain.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: images/page_022_table_0.png (Table 8: cross-section side
lengths 360/360/340/340/320/300 mm, image-verified); raw.pdf
sec. 2.9 (48 coils = 4 periods x 12, so 8 occurrences of each of
six unique coils; typical circumference 25 m)
*Basis**: sum of per-coil winding-pack volumes expressed as a held
distribution factor on the worst coil; concept-agnostic (MR-3)

    IMPLEMENTATION: See stellarator_materials_rebco_tea.handwritten.mfe_magnet_field.winding_pack_cold_volume_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts vol_winding_pack, vol_cold_total fields to separate channels.
    """

    name: str = "Winding_Pack_Cold_VolumeModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, vol_extra: float, n_coils: float, c_coil: float, f_wp_vol: float, wp_side: float    ) -> Winding_Pack_Cold_VolumeInput:
        """Validate inputs and fill defaults.

        Args:
            vol_extra: vol_extra input
            n_coils: n_coils input
            c_coil: c_coil input
            f_wp_vol: f_wp_vol input
            wp_side: wp_side input

        Returns:
            Validated input model
        """
        return Winding_Pack_Cold_VolumeInput(vol_extra=vol_extra, n_coils=n_coils, c_coil=c_coil, f_wp_vol=f_wp_vol, wp_side=wp_side)

    def run(
        self, vol_extra: float, n_coils: float, c_coil: float, f_wp_vol: float, wp_side: float    ) -> ModuleResult[Winding_Pack_Cold_VolumeOutput]:
        """Execute calculation.

        Args:
            vol_extra: vol_extra input
            n_coils: n_coils input
            c_coil: c_coil input
            f_wp_vol: f_wp_vol input
            wp_side: wp_side input

        Returns:
            Module result with Winding_Pack_Cold_VolumeOutput (vol_winding_pack, vol_cold_total)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(vol_extra, n_coils, c_coil, f_wp_vol, wp_side)

        # Import handwritten implementation
        from stellarator_materials_rebco_tea.handwritten.mfe_magnet_field.winding_pack_cold_volume_impl import (
            run_winding_pack_cold_volume,
        )

        # Execute implementation - returns tuple of values
        vol_winding_pack, vol_cold_total = run_winding_pack_cold_volume(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Winding_Pack_Cold_VolumeOutput(
                vol_winding_pack=vol_winding_pack,
                vol_cold_total=vol_cold_total,
            )
        )
