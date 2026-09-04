"""Conductor_Peak_FieldModule Module Wrapper

TEAx module for Conductor_Peak_Field calculation.

Peak magnetic field on the winding pack [T] from the axis-averaged field
and the coil set's peak/axis ratio (WI-030):

  B_peak = B_axis * peak_ratio

peak_ratio is a coil-geometry fact bound per instance (Stellaris:
24.9 T peak on the conductor at 9.0 T axis-averaged, Table 2 image);
it is the quantity a conductor ceiling ('Conductor Peak Field Limit')
is compared against. Kept as a calc, not an inline plant expression,
so the product is a module-graph edge the study tooling can trace and
no plant-level derived expression is introduced.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
/home/reid/1cfe/1costingfe/src/costingfe/defaults.py (pin 0254385)
*Ref**: images/page_002_table_0.png (Table 2: axis av. 9.0 T, peak
conductor 24.9 T); defaults.py:597-603 (MagnetProperties.b_max,
"peak field ceiling at the conductor" -- the bounded quantity)
*Basis**: peak-on-winding = axis field x coil-set ratio; MFE-generic

Inputs:
    - peak_ratio_in: peak_ratio_in parameter
    - B_axis_in: B_axis_in parameter

Outputs:
    - B_peak: B_peak result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:422

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:422

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plasma_scaling/conductor_peak_field_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Conductor_Peak_FieldInput(BaseModel):
    """Input model for Conductor_Peak_FieldModule.

    Attributes:
        peak_ratio_in: peak_ratio_in input
        B_axis_in: B_axis_in input
    """
    peak_ratio_in: float = Field(..., description="peak_ratio_in input")
    B_axis_in: float = Field(..., description="B_axis_in input")


class Conductor_Peak_FieldModule(ModuleBase[Conductor_Peak_FieldInput, Float]):
    """TEAx module for Conductor_Peak_Field calculation.

Peak magnetic field on the winding pack [T] from the axis-averaged field
and the coil set's peak/axis ratio (WI-030):

  B_peak = B_axis * peak_ratio

peak_ratio is a coil-geometry fact bound per instance (Stellaris:
24.9 T peak on the conductor at 9.0 T axis-averaged, Table 2 image);
it is the quantity a conductor ceiling ('Conductor Peak Field Limit')
is compared against. Kept as a calc, not an inline plant expression,
so the product is a module-graph edge the study tooling can trace and
no plant-level derived expression is introduced.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
/home/reid/1cfe/1costingfe/src/costingfe/defaults.py (pin 0254385)
*Ref**: images/page_002_table_0.png (Table 2: axis av. 9.0 T, peak
conductor 24.9 T); defaults.py:597-603 (MagnetProperties.b_max,
"peak field ceiling at the conductor" -- the bounded quantity)
*Basis**: peak-on-winding = axis field x coil-set ratio; MFE-generic

Inputs:
    - peak_ratio_in: peak_ratio_in parameter
    - B_axis_in: B_axis_in parameter

Outputs:
    - B_peak: B_peak result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:422

    SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:422

    Calculation Specification:
        B_peak = B_axis_in * peak_ratio_in
        
Documentation:
Peak magnetic field on the winding pack [T] from the axis-averaged field
and the coil set's peak/axis ratio (WI-030):

  B_peak = B_axis * peak_ratio

peak_ratio is a coil-geometry fact bound per instance (Stellaris:
24.9 T peak on the conductor at 9.0 T axis-averaged, Table 2 image);
it is the quantity a conductor ceiling ('Conductor Peak Field Limit')
is compared against. Kept as a calc, not an inline plant expression,
so the product is a module-graph edge the study tooling can trace and
no plant-level derived expression is introduced.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
/home/reid/1cfe/1costingfe/src/costingfe/defaults.py (pin 0254385)
*Ref**: images/page_002_table_0.png (Table 2: axis av. 9.0 T, peak
conductor 24.9 T); defaults.py:597-603 (MagnetProperties.b_max,
"peak field ceiling at the conductor" -- the bounded quantity)
*Basis**: peak-on-winding = axis field x coil-set ratio; MFE-generic

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plasma_scaling.conductor_peak_field_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Conductor_Peak_FieldModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, peak_ratio_in: float, B_axis_in: float    ) -> Conductor_Peak_FieldInput:
        """Validate inputs and fill defaults.

        Args:
            peak_ratio_in: peak_ratio_in input
            B_axis_in: B_axis_in input

        Returns:
            Validated input model
        """
        return Conductor_Peak_FieldInput(peak_ratio_in=peak_ratio_in, B_axis_in=B_axis_in)

    def run(
        self, peak_ratio_in: float, B_axis_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            peak_ratio_in: peak_ratio_in input
            B_axis_in: B_axis_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(peak_ratio_in, B_axis_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plasma_scaling.conductor_peak_field_impl import (
            run_conductor_peak_field,
        )

        # Execute implementation - returns single value
        B_peak = run_conductor_peak_field(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(B_peak))
