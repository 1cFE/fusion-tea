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
    - c_coil: c_coil parameter
    - vol_extra: vol_extra parameter
    - f_wp_vol: f_wp_vol parameter
    - wp_side: wp_side parameter
    - n_coils: n_coils parameter

Outputs:
    - vol_cold_total: vol_cold_total result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:154

SysML Source: root-0/analyses/mfe_magnet_field.sysml:154

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_magnet_field/winding_pack_cold_volume_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Winding_Pack_Cold_VolumeInput(BaseModel):
    """Input model for Winding_Pack_Cold_VolumeModule.

    Attributes:
        c_coil: c_coil input
        vol_extra: vol_extra input
        f_wp_vol: f_wp_vol input
        wp_side: wp_side input
        n_coils: n_coils input
    """
    c_coil: float = Field(..., description="c_coil input")
    vol_extra: float = Field(..., description="vol_extra input")
    f_wp_vol: float = Field(..., description="f_wp_vol input")
    wp_side: float = Field(..., description="wp_side input")
    n_coils: float = Field(..., description="n_coils input")


class Winding_Pack_Cold_VolumeModule(ModuleBase[Winding_Pack_Cold_VolumeInput, Float]):
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
    - c_coil: c_coil parameter
    - vol_extra: vol_extra parameter
    - f_wp_vol: f_wp_vol parameter
    - wp_side: wp_side parameter
    - n_coils: n_coils parameter

Outputs:
    - vol_cold_total: vol_cold_total result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:154

    SysML Source: root-0/analyses/mfe_magnet_field.sysml:154

    Calculation Specification:
        vol_extra = 0.0
        vol_cold_total = f_wp_vol * n_coils * wp_side * wp_side * c_coil + vol_extra
        
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

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_magnet_field.winding_pack_cold_volume_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Winding_Pack_Cold_VolumeModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, c_coil: float, vol_extra: float, f_wp_vol: float, wp_side: float, n_coils: float    ) -> Winding_Pack_Cold_VolumeInput:
        """Validate inputs and fill defaults.

        Args:
            c_coil: c_coil input
            vol_extra: vol_extra input
            f_wp_vol: f_wp_vol input
            wp_side: wp_side input
            n_coils: n_coils input

        Returns:
            Validated input model
        """
        return Winding_Pack_Cold_VolumeInput(c_coil=c_coil, vol_extra=vol_extra, f_wp_vol=f_wp_vol, wp_side=wp_side, n_coils=n_coils)

    def run(
        self, c_coil: float, vol_extra: float, f_wp_vol: float, wp_side: float, n_coils: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            c_coil: c_coil input
            vol_extra: vol_extra input
            f_wp_vol: f_wp_vol input
            wp_side: wp_side input
            n_coils: n_coils input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(c_coil, vol_extra, f_wp_vol, wp_side, n_coils)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_magnet_field.winding_pack_cold_volume_impl import (
            run_winding_pack_cold_volume,
        )

        # Execute implementation - returns single value
        vol_cold_total = run_winding_pack_cold_volume(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(vol_cold_total))
