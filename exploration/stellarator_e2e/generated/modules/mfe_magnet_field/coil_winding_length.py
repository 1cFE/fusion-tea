"""Coil_Winding_LengthModule Module Wrapper

TEAx module for Coil_Winding_Length calculation.

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

Inputs:
    - k_coil: k_coil parameter
    - R0: R0 parameter

Outputs:
    - c_coil: c_coil result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:124

SysML Source: root-0/analyses/mfe_magnet_field.sysml:124

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_magnet_field/coil_winding_length_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Coil_Winding_LengthInput(BaseModel):
    """Input model for Coil_Winding_LengthModule.

    Attributes:
        k_coil: k_coil input
        R0: R0 input
    """
    k_coil: float = Field(..., description="k_coil input")
    R0: float = Field(..., description="R0 input")


class Coil_Winding_LengthModule(ModuleBase[Coil_Winding_LengthInput, Float]):
    """TEAx module for Coil_Winding_Length calculation.

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

Inputs:
    - k_coil: k_coil parameter
    - R0: R0 parameter

Outputs:
    - c_coil: c_coil result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:124

    SysML Source: root-0/analyses/mfe_magnet_field.sysml:124

    Calculation Specification:
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

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_magnet_field.coil_winding_length_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Coil_Winding_LengthModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, k_coil: float, R0: float    ) -> Coil_Winding_LengthInput:
        """Validate inputs and fill defaults.

        Args:
            k_coil: k_coil input
            R0: R0 input

        Returns:
            Validated input model
        """
        return Coil_Winding_LengthInput(k_coil=k_coil, R0=R0)

    def run(
        self, k_coil: float, R0: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            k_coil: k_coil input
            R0: R0 input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(k_coil, R0)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_magnet_field.coil_winding_length_impl import (
            run_coil_winding_length,
        )

        # Execute implementation - returns single value
        c_coil = run_coil_winding_length(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(c_coil))
