"""Winding_Pack_SizingModule Module Wrapper

TEAx module for Winding_Pack_Sizing calculation.

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

Inputs:
    - I_coil: I_coil parameter
    - j_wp: j_wp parameter

Outputs:
    - wp_side: wp_side result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:84

SysML Source: root-0/analyses/mfe_magnet_field.sysml:84

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_magnet_field/winding_pack_sizing_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Winding_Pack_SizingInput(BaseModel):
    """Input model for Winding_Pack_SizingModule.

    Attributes:
        I_coil: I_coil input
        j_wp: j_wp input
    """
    I_coil: float = Field(..., description="I_coil input")
    j_wp: float = Field(..., description="j_wp input")


class Winding_Pack_SizingModule(ModuleBase[Winding_Pack_SizingInput, Float]):
    """TEAx module for Winding_Pack_Sizing calculation.

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

Inputs:
    - I_coil: I_coil parameter
    - j_wp: j_wp parameter

Outputs:
    - wp_side: wp_side result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:84

    SysML Source: root-0/analyses/mfe_magnet_field.sysml:84

    Calculation Specification:
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

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_magnet_field.winding_pack_sizing_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Winding_Pack_SizingModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, I_coil: float, j_wp: float    ) -> Winding_Pack_SizingInput:
        """Validate inputs and fill defaults.

        Args:
            I_coil: I_coil input
            j_wp: j_wp input

        Returns:
            Validated input model
        """
        return Winding_Pack_SizingInput(I_coil=I_coil, j_wp=j_wp)

    def run(
        self, I_coil: float, j_wp: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            I_coil: I_coil input
            j_wp: j_wp input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(I_coil, j_wp)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_magnet_field.winding_pack_sizing_impl import (
            run_winding_pack_sizing,
        )

        # Execute implementation - returns single value
        wp_side = run_winding_pack_sizing(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(wp_side))
