"""absent_boundary_exchange_mwModule Module Wrapper

TEAx module for absent_boundary_exchange_mw calculation.

Inputs:
    - transferred_heat_mw: transferred_heat_mw parameter

Outputs:
    - absent_boundary_exchange_mw: absent_boundary_exchange_mw result

SysML Source: root-0/dual_blanket_heat.sysml:10

SysML Source: root-0/dual_blanket_heat.sysml:10

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/aries_dual_blanket_heat/inter_coolant_exchange/absent_boundary_exchange_mw_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from heat_tea.primitives import Float


class absent_boundary_exchange_mwInput(BaseModel):
    """Input model for absent_boundary_exchange_mwModule.

    Attributes:
        transferred_heat_mw: transferred_heat_mw input
    """
    transferred_heat_mw: float = Field(..., description="transferred_heat_mw input")


class absent_boundary_exchange_mwModule(ModuleBase[absent_boundary_exchange_mwInput, Float]):
    """TEAx module for absent_boundary_exchange_mw calculation.

Inputs:
    - transferred_heat_mw: transferred_heat_mw parameter

Outputs:
    - absent_boundary_exchange_mw: absent_boundary_exchange_mw result

SysML Source: root-0/dual_blanket_heat.sysml:10

    SysML Source: root-0/dual_blanket_heat.sysml:10

    Calculation Specification:

    IMPLEMENTATION: See heat_tea.handwritten.aries_dual_blanket_heat.inter_coolant_exchange.absent_boundary_exchange_mw_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "absent_boundary_exchange_mwModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, transferred_heat_mw: float    ) -> absent_boundary_exchange_mwInput:
        """Validate inputs and fill defaults.

        Args:
            transferred_heat_mw: transferred_heat_mw input

        Returns:
            Validated input model
        """
        return absent_boundary_exchange_mwInput(transferred_heat_mw=transferred_heat_mw)

    def run(
        self, transferred_heat_mw: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            transferred_heat_mw: transferred_heat_mw input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(transferred_heat_mw)

        # Import handwritten implementation
        from heat_tea.handwritten.aries_dual_blanket_heat.inter_coolant_exchange.absent_boundary_exchange_mw_impl import (
            run_absent_boundary_exchange_mw,
        )

        # Execute implementation - returns single value
        absent_boundary_exchange_mw = run_absent_boundary_exchange_mw(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(absent_boundary_exchange_mw))
