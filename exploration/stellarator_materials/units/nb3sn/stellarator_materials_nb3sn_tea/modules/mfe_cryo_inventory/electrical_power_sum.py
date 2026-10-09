"""Electrical_Power_SumModule Module Wrapper

TEAx module for Electrical_Power_Sum calculation.

Sum electrical MW with no category conversion.
*Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md **Reference**: D3/D5.
*Basis**: additive electrical balance. **Last Updated**: 2026-09-15

Inputs:
    - p_a: p_a parameter
    - p_b: p_b parameter

Outputs:
    - total: total result

SysML Source: root-0/analyses/mfe_cryo_inventory.sysml:81

SysML Source: root-0/analyses/mfe_cryo_inventory.sysml:81

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_cryo_inventory/electrical_power_sum_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float


class Electrical_Power_SumInput(BaseModel):
    """Input model for Electrical_Power_SumModule.

    Attributes:
        p_a: p_a input
        p_b: p_b input
    """
    p_a: float = Field(..., description="p_a input")
    p_b: float = Field(..., description="p_b input")


class Electrical_Power_SumModule(ModuleBase[Electrical_Power_SumInput, Float]):
    """TEAx module for Electrical_Power_Sum calculation.

Sum electrical MW with no category conversion.
*Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md **Reference**: D3/D5.
*Basis**: additive electrical balance. **Last Updated**: 2026-09-15

Inputs:
    - p_a: p_a parameter
    - p_b: p_b parameter

Outputs:
    - total: total result

SysML Source: root-0/analyses/mfe_cryo_inventory.sysml:81

    SysML Source: root-0/analyses/mfe_cryo_inventory.sysml:81

    Calculation Specification:
        p_a = 0.0
        p_b = 0.0
        total = p_a + p_b
        
Documentation:
Sum electrical MW with no category conversion.
*Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md **Reference**: D3/D5.
*Basis**: additive electrical balance. **Last Updated**: 2026-09-15

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.mfe_cryo_inventory.electrical_power_sum_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Electrical_Power_SumModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, p_a: float, p_b: float    ) -> Electrical_Power_SumInput:
        """Validate inputs and fill defaults.

        Args:
            p_a: p_a input
            p_b: p_b input

        Returns:
            Validated input model
        """
        return Electrical_Power_SumInput(p_a=p_a, p_b=p_b)

    def run(
        self, p_a: float, p_b: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            p_a: p_a input
            p_b: p_b input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(p_a, p_b)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.mfe_cryo_inventory.electrical_power_sum_impl import (
            run_electrical_power_sum,
        )

        # Execute implementation - returns single value
        total = run_electrical_power_sum(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(total))
