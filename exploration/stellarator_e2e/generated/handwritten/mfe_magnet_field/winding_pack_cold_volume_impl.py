"""Auto-generated implementation for Winding_Pack_Cold_Volume.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_magnet_field.sysml:154

SysML Expressions:
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
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_magnet_field.winding_pack_cold_volume import Winding_Pack_Cold_VolumeInput


def run_winding_pack_cold_volume(inputs: Winding_Pack_Cold_VolumeInput) -> float:
    """Execute Winding_Pack_Cold_Volume calculation.

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

SysML Source: root-0/analyses/mfe_magnet_field.sysml:154

SysML Expressions:
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

Args:
    inputs: Input parameters validated against Winding_Pack_Cold_VolumeInput schema

Returns:
    float: vol_cold_total

Example:
    >>> inputs = Winding_Pack_Cold_VolumeInput(...)
    >>> result = run_winding_pack_cold_volume(inputs)
    """
    return (((((inputs.f_wp_vol * inputs.n_coils) * inputs.wp_side) * inputs.wp_side) * inputs.c_coil) + inputs.vol_extra)
