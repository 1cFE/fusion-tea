"""Actual_Exchanger_ApproachesModule Module Wrapper

TEAx module for Actual_Exchanger_Approaches calculation.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/actual_exchanger_approaches_impl.py; reviewed equations in design/configuration.

Inputs:
    - secondary_in_in: secondary_in_in parameter
    - primary_hot_in: primary_hot_in parameter
    - primary_exchanger_return_in: primary_exchanger_return_in parameter
    - secondary_out_in: secondary_out_in parameter

Outputs:
    - cold_gap: cold_gap result
    - hot_gap: hot_gap result

SysML Source: root-0/whole_plant_conversion_accounts.sysml:5

SysML Source: root-0/whole_plant_conversion_accounts.sysml:5

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/whole_plant_conversion_accounts/actual_exchanger_approaches_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.primitives import Float
from whole_plant_conversion_tea.schemas.actual_exchanger_approaches_output import Actual_Exchanger_ApproachesOutput


class Actual_Exchanger_ApproachesInput(BaseModel):
    """Input model for Actual_Exchanger_ApproachesModule.

    Attributes:
        secondary_in_in: secondary_in_in input
        primary_hot_in: primary_hot_in input
        primary_exchanger_return_in: primary_exchanger_return_in input
        secondary_out_in: secondary_out_in input
    """
    secondary_in_in: float = Field(..., description="secondary_in_in input")
    primary_hot_in: float = Field(..., description="primary_hot_in input")
    primary_exchanger_return_in: float = Field(..., description="primary_exchanger_return_in input")
    secondary_out_in: float = Field(..., description="secondary_out_in input")


class Actual_Exchanger_ApproachesModule(ModuleBase[Actual_Exchanger_ApproachesInput, Actual_Exchanger_ApproachesOutput]):
    """TEAx module for Actual_Exchanger_Approaches calculation.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/actual_exchanger_approaches_impl.py; reviewed equations in design/configuration.

Inputs:
    - secondary_in_in: secondary_in_in parameter
    - primary_hot_in: primary_hot_in parameter
    - primary_exchanger_return_in: primary_exchanger_return_in parameter
    - secondary_out_in: secondary_out_in parameter

Outputs:
    - cold_gap: cold_gap result
    - hot_gap: hot_gap result

SysML Source: root-0/whole_plant_conversion_accounts.sysml:5

    SysML Source: root-0/whole_plant_conversion_accounts.sysml:5

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/actual_exchanger_approaches_impl.py; reviewed equations in design/configuration.

    IMPLEMENTATION: See whole_plant_conversion_tea.handwritten.whole_plant_conversion_accounts.actual_exchanger_approaches_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts cold_gap, hot_gap fields to separate channels.
    """

    name: str = "Actual_Exchanger_ApproachesModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, secondary_in_in: float, primary_hot_in: float, primary_exchanger_return_in: float, secondary_out_in: float    ) -> Actual_Exchanger_ApproachesInput:
        """Validate inputs and fill defaults.

        Args:
            secondary_in_in: secondary_in_in input
            primary_hot_in: primary_hot_in input
            primary_exchanger_return_in: primary_exchanger_return_in input
            secondary_out_in: secondary_out_in input

        Returns:
            Validated input model
        """
        return Actual_Exchanger_ApproachesInput(secondary_in_in=secondary_in_in, primary_hot_in=primary_hot_in, primary_exchanger_return_in=primary_exchanger_return_in, secondary_out_in=secondary_out_in)

    def run(
        self, secondary_in_in: float, primary_hot_in: float, primary_exchanger_return_in: float, secondary_out_in: float    ) -> ModuleResult[Actual_Exchanger_ApproachesOutput]:
        """Execute calculation.

        Args:
            secondary_in_in: secondary_in_in input
            primary_hot_in: primary_hot_in input
            primary_exchanger_return_in: primary_exchanger_return_in input
            secondary_out_in: secondary_out_in input

        Returns:
            Module result with Actual_Exchanger_ApproachesOutput (cold_gap, hot_gap)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(secondary_in_in, primary_hot_in, primary_exchanger_return_in, secondary_out_in)

        # Import handwritten implementation
        from whole_plant_conversion_tea.handwritten.whole_plant_conversion_accounts.actual_exchanger_approaches_impl import (
            run_actual_exchanger_approaches,
        )

        # Execute implementation - returns tuple of values
        cold_gap, hot_gap = run_actual_exchanger_approaches(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Actual_Exchanger_ApproachesOutput(
                cold_gap=cold_gap,
                hot_gap=hot_gap,
            )
        )
