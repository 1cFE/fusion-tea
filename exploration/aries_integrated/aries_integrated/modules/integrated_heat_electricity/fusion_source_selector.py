"""Fusion_Source_SelectorModule Module Wrapper

TEAx module for Fusion_Source_Selector calculation.

*Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: accepted WI-089 design and source/assumption register; generic fusion source selector. Normative equations, units and operating domains are in the named design sections; typed native completion enforces them. MW/K/MPa/kg/s/J per kg K/atoms per s as documented; dimensionless flags use 0/1. **Last Updated**: 2026-09-22.

Inputs:
    - mode_in: mode_in parameter
    - calculated_power_in: calculated_power_in parameter
    - reference_power_in: reference_power_in parameter

Outputs:
    - selected_power: selected_power result
    - selected_mode: selected_mode result

SysML Source: root-0/integrated_heat_electricity.sysml:3

SysML Source: root-0/integrated_heat_electricity.sysml:3

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/integrated_heat_electricity/fusion_source_selector_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from aries_integrated.primitives import Float
from aries_integrated.schemas.fusion_source_selector_output import Fusion_Source_SelectorOutput


class Fusion_Source_SelectorInput(BaseModel):
    """Input model for Fusion_Source_SelectorModule.

    Attributes:
        mode_in: mode_in input
        calculated_power_in: calculated_power_in input
        reference_power_in: reference_power_in input
    """
    mode_in: float = Field(..., description="mode_in input")
    calculated_power_in: float = Field(..., description="calculated_power_in input")
    reference_power_in: float = Field(..., description="reference_power_in input")


class Fusion_Source_SelectorModule(ModuleBase[Fusion_Source_SelectorInput, Fusion_Source_SelectorOutput]):
    """TEAx module for Fusion_Source_Selector calculation.

*Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: accepted WI-089 design and source/assumption register; generic fusion source selector. Normative equations, units and operating domains are in the named design sections; typed native completion enforces them. MW/K/MPa/kg/s/J per kg K/atoms per s as documented; dimensionless flags use 0/1. **Last Updated**: 2026-09-22.

Inputs:
    - mode_in: mode_in parameter
    - calculated_power_in: calculated_power_in parameter
    - reference_power_in: reference_power_in parameter

Outputs:
    - selected_power: selected_power result
    - selected_mode: selected_mode result

SysML Source: root-0/integrated_heat_electricity.sysml:3

    SysML Source: root-0/integrated_heat_electricity.sysml:3

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: accepted WI-089 design and source/assumption register; generic fusion source selector. Normative equations, units and operating domains are in the named design sections; typed native completion enforces them. MW/K/MPa/kg/s/J per kg K/atoms per s as documented; dimensionless flags use 0/1. **Last Updated**: 2026-09-22.

    IMPLEMENTATION: See aries_integrated.handwritten.integrated_heat_electricity.fusion_source_selector_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts selected_power, selected_mode fields to separate channels.
    """

    name: str = "Fusion_Source_SelectorModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, mode_in: float, calculated_power_in: float, reference_power_in: float    ) -> Fusion_Source_SelectorInput:
        """Validate inputs and fill defaults.

        Args:
            mode_in: mode_in input
            calculated_power_in: calculated_power_in input
            reference_power_in: reference_power_in input

        Returns:
            Validated input model
        """
        return Fusion_Source_SelectorInput(mode_in=mode_in, calculated_power_in=calculated_power_in, reference_power_in=reference_power_in)

    def run(
        self, mode_in: float, calculated_power_in: float, reference_power_in: float    ) -> ModuleResult[Fusion_Source_SelectorOutput]:
        """Execute calculation.

        Args:
            mode_in: mode_in input
            calculated_power_in: calculated_power_in input
            reference_power_in: reference_power_in input

        Returns:
            Module result with Fusion_Source_SelectorOutput (selected_power, selected_mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(mode_in, calculated_power_in, reference_power_in)

        # Import handwritten implementation
        from aries_integrated.handwritten.integrated_heat_electricity.fusion_source_selector_impl import (
            run_fusion_source_selector,
        )

        # Execute implementation - returns tuple of values
        selected_power, selected_mode = run_fusion_source_selector(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Fusion_Source_SelectorOutput(
                selected_power=selected_power,
                selected_mode=selected_mode,
            )
        )
