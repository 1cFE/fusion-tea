"""Auto-generated implementation for Winding_Pack_Sizing.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_magnet_field.sysml:84

SysML Expressions:
    wp_side = (I_coil / j_wp) ** 0.5 / 1000.0
    
Documentation:
Winding-pack cross-section side [m] from the current the pack must
carry (WI-036, D1):

  wp_side = sqrt(I_coil / j_wp) / 1000

The pack is sized by its current at a chosen winding-pack current
density, not held while current varies. The relation is the one the
source's own coil set satisfies: across all six unique Stellaris
coils, j_wp * side^2 reproduces the printed total amp-turns to
better than 1% (-0.58% .. +0.52%). j_wp is the design lever -- the
source varies it 112..124 A/mm^2 across its coil set -- and is bound
per instance as the float64 that reproduces the printed pair exactly.

Unit note: j_wp is in A/mm^2 and I_coil in A, so I_coil/j_wp is an
area in mm^2; the 1000 divisor converts the side to metres.

Consequence for the paired stress calc: substituting gives
sigma_wp = k_sigma * B_peak * sqrt(I_coil * j_wp), so winding stress
grows as the square root of coil current rather than linearly once
the pack is allowed to size itself.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: images/page_022_table_0.png (Table 8: I total amp-turns
15.4/14.6/13.8/12.9/12.5/11.2 MA; j_WP 119/112/120/112/122/124
A/mm^2; cross-section side 360/360/340/340/320/300 mm --
image-verified; the markdown extraction of this table is garbled)
*Basis**: winding-pack area = coil current / winding-pack current
density; concept-agnostic (MR-3) -- all values bound by instances
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_magnet_field.winding_pack_sizing import Winding_Pack_SizingInput


def run_winding_pack_sizing(inputs: Winding_Pack_SizingInput) -> float:
    """Execute Winding_Pack_Sizing calculation.

Winding-pack cross-section side [m] from the current the pack must
carry (WI-036, D1):

  wp_side = sqrt(I_coil / j_wp) / 1000

The pack is sized by its current at a chosen winding-pack current
density, not held while current varies. The relation is the one the
source's own coil set satisfies: across all six unique Stellaris
coils, j_wp * side^2 reproduces the printed total amp-turns to
better than 1% (-0.58% .. +0.52%). j_wp is the design lever -- the
source varies it 112..124 A/mm^2 across its coil set -- and is bound
per instance as the float64 that reproduces the printed pair exactly.

Unit note: j_wp is in A/mm^2 and I_coil in A, so I_coil/j_wp is an
area in mm^2; the 1000 divisor converts the side to metres.

Consequence for the paired stress calc: substituting gives
sigma_wp = k_sigma * B_peak * sqrt(I_coil * j_wp), so winding stress
grows as the square root of coil current rather than linearly once
the pack is allowed to size itself.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: images/page_022_table_0.png (Table 8: I total amp-turns
15.4/14.6/13.8/12.9/12.5/11.2 MA; j_WP 119/112/120/112/122/124
A/mm^2; cross-section side 360/360/340/340/320/300 mm --
image-verified; the markdown extraction of this table is garbled)
*Basis**: winding-pack area = coil current / winding-pack current
density; concept-agnostic (MR-3) -- all values bound by instances

SysML Source: root-0/analyses/mfe_magnet_field.sysml:84

SysML Expressions:
    wp_side = (I_coil / j_wp) ** 0.5 / 1000.0
    
Documentation:
Winding-pack cross-section side [m] from the current the pack must
carry (WI-036, D1):

  wp_side = sqrt(I_coil / j_wp) / 1000

The pack is sized by its current at a chosen winding-pack current
density, not held while current varies. The relation is the one the
source's own coil set satisfies: across all six unique Stellaris
coils, j_wp * side^2 reproduces the printed total amp-turns to
better than 1% (-0.58% .. +0.52%). j_wp is the design lever -- the
source varies it 112..124 A/mm^2 across its coil set -- and is bound
per instance as the float64 that reproduces the printed pair exactly.

Unit note: j_wp is in A/mm^2 and I_coil in A, so I_coil/j_wp is an
area in mm^2; the 1000 divisor converts the side to metres.

Consequence for the paired stress calc: substituting gives
sigma_wp = k_sigma * B_peak * sqrt(I_coil * j_wp), so winding stress
grows as the square root of coil current rather than linearly once
the pack is allowed to size itself.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: images/page_022_table_0.png (Table 8: I total amp-turns
15.4/14.6/13.8/12.9/12.5/11.2 MA; j_WP 119/112/120/112/122/124
A/mm^2; cross-section side 360/360/340/340/320/300 mm --
image-verified; the markdown extraction of this table is garbled)
*Basis**: winding-pack area = coil current / winding-pack current
density; concept-agnostic (MR-3) -- all values bound by instances

Args:
    inputs: Input parameters validated against Winding_Pack_SizingInput schema

Returns:
    float: wp_side

Example:
    >>> inputs = Winding_Pack_SizingInput(...)
    >>> result = run_winding_pack_sizing(inputs)
    """
    return (((inputs.I_coil / inputs.j_wp) ** 0.5) / 1000.0)
