"""Auto-generated implementation for Coil_Winding_Length.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_magnet_field.sysml:124

SysML Expressions:
    c_coil = k_coil * R0
    
Documentation:
Typical coil winding circumference [m] from machine scale (WI-036, D3):

  c_coil = k_coil * R0

Winding length is the sole length term in the magnet conductor cost,
and was previously a held printed constant that did not respond to
machine size. Per-coil circumferences are unprinted, so what the
source supports is a held *shape* factor with the *scale* responding
-- the trade the WI-036 mint record predicted ("one held constant
traded for a smaller one"). k_coil is the residual held quantity and
is named rather than buried.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: raw.pdf sec. 2.9 ("typical circumference of 25 m"; coils
approximately 7 x 5 x 10 m); images/page_002_table_0.png
(Table 2: major radius 12.7 m)
*Basis**: coil circumference scales with major radius at a held
coil-shape factor; concept-agnostic (MR-3)
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_magnet_field.coil_winding_length import Coil_Winding_LengthInput


def run_coil_winding_length(inputs: Coil_Winding_LengthInput) -> float:
    """Execute Coil_Winding_Length calculation.

Typical coil winding circumference [m] from machine scale (WI-036, D3):

  c_coil = k_coil * R0

Winding length is the sole length term in the magnet conductor cost,
and was previously a held printed constant that did not respond to
machine size. Per-coil circumferences are unprinted, so what the
source supports is a held *shape* factor with the *scale* responding
-- the trade the WI-036 mint record predicted ("one held constant
traded for a smaller one"). k_coil is the residual held quantity and
is named rather than buried.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: raw.pdf sec. 2.9 ("typical circumference of 25 m"; coils
approximately 7 x 5 x 10 m); images/page_002_table_0.png
(Table 2: major radius 12.7 m)
*Basis**: coil circumference scales with major radius at a held
coil-shape factor; concept-agnostic (MR-3)

SysML Source: root-0/analyses/mfe_magnet_field.sysml:124

SysML Expressions:
    c_coil = k_coil * R0
    
Documentation:
Typical coil winding circumference [m] from machine scale (WI-036, D3):

  c_coil = k_coil * R0

Winding length is the sole length term in the magnet conductor cost,
and was previously a held printed constant that did not respond to
machine size. Per-coil circumferences are unprinted, so what the
source supports is a held *shape* factor with the *scale* responding
-- the trade the WI-036 mint record predicted ("one held constant
traded for a smaller one"). k_coil is the residual held quantity and
is named rather than buried.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: raw.pdf sec. 2.9 ("typical circumference of 25 m"; coils
approximately 7 x 5 x 10 m); images/page_002_table_0.png
(Table 2: major radius 12.7 m)
*Basis**: coil circumference scales with major radius at a held
coil-shape factor; concept-agnostic (MR-3)

Args:
    inputs: Input parameters validated against Coil_Winding_LengthInput schema

Returns:
    float: c_coil

Example:
    >>> inputs = Coil_Winding_LengthInput(...)
    >>> result = run_coil_winding_length(inputs)
    """
    return (inputs.k_coil * inputs.R0)
