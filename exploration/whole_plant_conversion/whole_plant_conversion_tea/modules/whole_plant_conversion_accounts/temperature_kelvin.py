"""Temperature_KelvinModule Module Wrapper

TEAx module for Temperature_Kelvin calculation.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/temperature_kelvin_impl.py; reviewed equations in design/configuration.

Inputs:
    - celsius_in: celsius_in parameter

Outputs:
    - value: value result

SysML Source: root-0/whole_plant_conversion_accounts.sysml:173

SysML Source: root-0/whole_plant_conversion_accounts.sysml:173

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/whole_plant_conversion_accounts/temperature_kelvin_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.primitives import Float


class Temperature_KelvinInput(BaseModel):
    """Input model for Temperature_KelvinModule.

    Attributes:
        celsius_in: celsius_in input
    """
    celsius_in: float = Field(..., description="celsius_in input")


class Temperature_KelvinModule(ModuleBase[Temperature_KelvinInput, Float]):
    """TEAx module for Temperature_Kelvin calculation.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/temperature_kelvin_impl.py; reviewed equations in design/configuration.

Inputs:
    - celsius_in: celsius_in parameter

Outputs:
    - value: value result

SysML Source: root-0/whole_plant_conversion_accounts.sysml:173

    SysML Source: root-0/whole_plant_conversion_accounts.sysml:173

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/temperature_kelvin_impl.py; reviewed equations in design/configuration.

    IMPLEMENTATION: See whole_plant_conversion_tea.handwritten.whole_plant_conversion_accounts.temperature_kelvin_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Temperature_KelvinModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, celsius_in: float    ) -> Temperature_KelvinInput:
        """Validate inputs and fill defaults.

        Args:
            celsius_in: celsius_in input

        Returns:
            Validated input model
        """
        return Temperature_KelvinInput(celsius_in=celsius_in)

    def run(
        self, celsius_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            celsius_in: celsius_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(celsius_in)

        # Import handwritten implementation
        from whole_plant_conversion_tea.handwritten.whole_plant_conversion_accounts.temperature_kelvin_impl import (
            run_temperature_kelvin,
        )

        # Execute implementation - returns single value
        value = run_temperature_kelvin(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(value))
