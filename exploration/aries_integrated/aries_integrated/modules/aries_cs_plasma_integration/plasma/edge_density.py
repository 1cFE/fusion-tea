"""edge_densityModule Module Wrapper

TEAx module for edge_density calculation.

Inputs:
    - amplitude: amplitude parameter
    - edge_ratio: edge_ratio parameter

Outputs:
    - edge_density: edge_density result

SysML Source: root-0/plasma_integration.sysml:19

SysML Source: root-0/plasma_integration.sysml:19

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/aries_cs_plasma_integration/plasma/edge_density_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from aries_integrated.primitives import Float


class edge_densityInput(BaseModel):
    """Input model for edge_densityModule.

    Attributes:
        amplitude: amplitude input
        edge_ratio: edge_ratio input
    """
    amplitude: float = Field(..., description="amplitude input")
    edge_ratio: float = Field(..., description="edge_ratio input")


class edge_densityModule(ModuleBase[edge_densityInput, Float]):
    """TEAx module for edge_density calculation.

Inputs:
    - amplitude: amplitude parameter
    - edge_ratio: edge_ratio parameter

Outputs:
    - edge_density: edge_density result

SysML Source: root-0/plasma_integration.sysml:19

    SysML Source: root-0/plasma_integration.sysml:19

    Calculation Specification:

    IMPLEMENTATION: See aries_integrated.handwritten.aries_cs_plasma_integration.plasma.edge_density_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "edge_densityModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, amplitude: float, edge_ratio: float    ) -> edge_densityInput:
        """Validate inputs and fill defaults.

        Args:
            amplitude: amplitude input
            edge_ratio: edge_ratio input

        Returns:
            Validated input model
        """
        return edge_densityInput(amplitude=amplitude, edge_ratio=edge_ratio)

    def run(
        self, amplitude: float, edge_ratio: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            amplitude: amplitude input
            edge_ratio: edge_ratio input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(amplitude, edge_ratio)

        # Import handwritten implementation
        from aries_integrated.handwritten.aries_cs_plasma_integration.plasma.edge_density_impl import (
            run_edge_density,
        )

        # Execute implementation - returns single value
        edge_density = run_edge_density(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(edge_density))
