"""MatchModule Module Wrapper

TEAx module for Match calculation.

Inputs:
    - property_in: property_in parameter
    - enabled_in: enabled_in parameter
    - legacy_in: legacy_in parameter

Outputs:
    - gross_out: gross_out result
    - state_h: state_h result
    - pump_out: pump_out result

SysML Source: root-0/probe.sysml:7

SysML Source: root-0/probe.sysml:7

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/probe/match_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from probe_selector.primitives import Float
from probe_selector.schemas.match_output import MatchOutput


class MatchInput(BaseModel):
    """Input model for MatchModule.

    Attributes:
        property_in: property_in input
        enabled_in: enabled_in input
        legacy_in: legacy_in input
    """
    property_in: float = Field(..., description="property_in input")
    enabled_in: float = Field(..., description="enabled_in input")
    legacy_in: float = Field(..., description="legacy_in input")


class MatchModule(ModuleBase[MatchInput, MatchOutput]):
    """TEAx module for Match calculation.

Inputs:
    - property_in: property_in parameter
    - enabled_in: enabled_in parameter
    - legacy_in: legacy_in parameter

Outputs:
    - gross_out: gross_out result
    - state_h: state_h result
    - pump_out: pump_out result

SysML Source: root-0/probe.sysml:7

    SysML Source: root-0/probe.sysml:7

    Calculation Specification:

    IMPLEMENTATION: See probe_selector.handwritten.probe.match_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts gross_out, state_h, pump_out fields to separate channels.
    """

    name: str = "MatchModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, property_in: float, enabled_in: float, legacy_in: float    ) -> MatchInput:
        """Validate inputs and fill defaults.

        Args:
            property_in: property_in input
            enabled_in: enabled_in input
            legacy_in: legacy_in input

        Returns:
            Validated input model
        """
        return MatchInput(property_in=property_in, enabled_in=enabled_in, legacy_in=legacy_in)

    def run(
        self, property_in: float, enabled_in: float, legacy_in: float    ) -> ModuleResult[MatchOutput]:
        """Execute calculation.

        Args:
            property_in: property_in input
            enabled_in: enabled_in input
            legacy_in: legacy_in input

        Returns:
            Module result with MatchOutput (gross_out, state_h, pump_out)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(property_in, enabled_in, legacy_in)

        # Import handwritten implementation
        from probe_selector.handwritten.probe.match_impl import (
            run_match,
        )

        # Execute implementation - returns tuple of values
        gross_out, state_h, pump_out = run_match(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=MatchOutput(
                gross_out=gross_out,
                state_h=state_h,
                pump_out=pump_out,
            )
        )
