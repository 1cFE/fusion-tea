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
sigma_wp = 1000 * k_sigma * B_peak * sqrt(I_coil * j_wp).
At fixed peak field and density, stress grows as sqrt(I_coil).
When peak field follows current at fixed geometry, it grows as
I_coil^(3/2) at fixed density. The factor 1000 follows the side's
millimetre-to-metre conversion; it is not a calibration coefficient.

Domain: I_coil and j_wp are finite magnitudes, with I_coil >= 0
and j_wp > 0. Native typed manual completion raises ValueError
before evaluating the sizing equation for an invalid domain (WI-055).
I_coil = 0 gives local side = 0, not a de-energized finite coil model.
The composed stress and plasma equations enforce their own nonzero
denominators. Source coil values are examples, not universal bounds.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: images/page_022_table_0.png (Table 8: I total amp-turns
15.4/14.6/13.8/12.9/12.5/11.2 MA; j_WP 119/112/120/112/122/124
A/mm^2; cross-section side 360/360/340/340/320/300 mm --
image-verified; the markdown extraction of this table is garbled)
*Basis**: winding-pack area = coil current / winding-pack current
density; concept-agnostic (MR-3) -- all values bound by instances

Inputs:
    - j_wp: j_wp parameter
    - I_coil: I_coil parameter

Outputs:
    - wp_side: wp_side result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:91

SysML Source: root-0/analyses/mfe_magnet_field.sysml:91

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_magnet_field/winding_pack_sizing_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Winding_Pack_SizingInput(BaseModel):
    """Input model for Winding_Pack_SizingModule.

    Attributes:
        j_wp: j_wp input
        I_coil: I_coil input
    """
    j_wp: float = Field(..., description="j_wp input")
    I_coil: float = Field(..., description="I_coil input")


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
sigma_wp = 1000 * k_sigma * B_peak * sqrt(I_coil * j_wp).
At fixed peak field and density, stress grows as sqrt(I_coil).
When peak field follows current at fixed geometry, it grows as
I_coil^(3/2) at fixed density. The factor 1000 follows the side's
millimetre-to-metre conversion; it is not a calibration coefficient.

Domain: I_coil and j_wp are finite magnitudes, with I_coil >= 0
and j_wp > 0. Native typed manual completion raises ValueError
before evaluating the sizing equation for an invalid domain (WI-055).
I_coil = 0 gives local side = 0, not a de-energized finite coil model.
The composed stress and plasma equations enforce their own nonzero
denominators. Source coil values are examples, not universal bounds.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: images/page_022_table_0.png (Table 8: I total amp-turns
15.4/14.6/13.8/12.9/12.5/11.2 MA; j_WP 119/112/120/112/122/124
A/mm^2; cross-section side 360/360/340/340/320/300 mm --
image-verified; the markdown extraction of this table is garbled)
*Basis**: winding-pack area = coil current / winding-pack current
density; concept-agnostic (MR-3) -- all values bound by instances

Inputs:
    - j_wp: j_wp parameter
    - I_coil: I_coil parameter

Outputs:
    - wp_side: wp_side result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:91

    SysML Source: root-0/analyses/mfe_magnet_field.sysml:91

    Calculation Specification:
        See documentation:
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
sigma_wp = 1000 * k_sigma * B_peak * sqrt(I_coil * j_wp).
At fixed peak field and density, stress grows as sqrt(I_coil).
When peak field follows current at fixed geometry, it grows as
I_coil^(3/2) at fixed density. The factor 1000 follows the side's
millimetre-to-metre conversion; it is not a calibration coefficient.

Domain: I_coil and j_wp are finite magnitudes, with I_coil >= 0
and j_wp > 0. Native typed manual completion raises ValueError
before evaluating the sizing equation for an invalid domain (WI-055).
I_coil = 0 gives local side = 0, not a de-energized finite coil model.
The composed stress and plasma equations enforce their own nonzero
denominators. Source coil values are examples, not universal bounds.

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
        self, j_wp: float, I_coil: float    ) -> Winding_Pack_SizingInput:
        """Validate inputs and fill defaults.

        Args:
            j_wp: j_wp input
            I_coil: I_coil input

        Returns:
            Validated input model
        """
        return Winding_Pack_SizingInput(j_wp=j_wp, I_coil=I_coil)

    def run(
        self, j_wp: float, I_coil: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            j_wp: j_wp input
            I_coil: I_coil input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(j_wp, I_coil)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_magnet_field.winding_pack_sizing_impl import (
            run_winding_pack_sizing,
        )

        # Execute implementation - returns single value
        wp_side = run_winding_pack_sizing(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(wp_side))
