"""property_valueModule Module Wrapper

TEAx module for property_value calculation.

Outputs:
    - property_value: property_value result

SysML Source: root-0/probe.sysml:23

SysML Source: root-0/probe.sysml:23

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/probe/turbine/property_value_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from probe_selector.primitives import Float


class property_valueInput(BaseModel):
    """Input model for property_valueModule.

    Attributes:
    """


class property_valueModule(ModuleBase[property_valueInput, Float]):
    """TEAx module for property_value calculation.

Outputs:
    - property_value: property_value result

SysML Source: root-0/probe.sysml:23

    SysML Source: root-0/probe.sysml:23

    Calculation Specification:

    IMPLEMENTATION: See probe_selector.handwritten.probe.turbine.property_value_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "property_valueModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self,     ) -> property_valueInput:
        """Validate inputs and fill defaults.

        Args:

        Returns:
            Validated input model
        """
        return property_valueInput()

    def run(
        self,     ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default()

        # Import handwritten implementation
        from probe_selector.handwritten.probe.turbine.property_value_impl import (
            run_property_value,
        )

        # Execute implementation - returns single value
        property_value = run_property_value(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(property_value))
