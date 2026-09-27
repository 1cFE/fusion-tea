"""Comparison_DifferenceModule Module Wrapper

TEAx module for Comparison_Difference calculation.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

Inputs:
    - right_in: right_in parameter
    - left_in: left_in parameter

Outputs:
    - difference: difference result

SysML Source: root-0/integrated_equipment_costs.sysml:98

SysML Source: root-0/integrated_equipment_costs.sysml:98

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/integrated_equipment_costs/comparison_difference_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from exchanger_architecture_thermal_tea.primitives import Float


class Comparison_DifferenceInput(BaseModel):
    """Input model for Comparison_DifferenceModule.

    Attributes:
        right_in: right_in input
        left_in: left_in input
    """
    right_in: float = Field(..., description="right_in input")
    left_in: float = Field(..., description="left_in input")


class Comparison_DifferenceModule(ModuleBase[Comparison_DifferenceInput, Float]):
    """TEAx module for Comparison_Difference calculation.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

Inputs:
    - right_in: right_in parameter
    - left_in: left_in parameter

Outputs:
    - difference: difference result

SysML Source: root-0/integrated_equipment_costs.sysml:98

    SysML Source: root-0/integrated_equipment_costs.sysml:98

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

    IMPLEMENTATION: See exchanger_architecture_thermal_tea.handwritten.integrated_equipment_costs.comparison_difference_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Comparison_DifferenceModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, right_in: float, left_in: float    ) -> Comparison_DifferenceInput:
        """Validate inputs and fill defaults.

        Args:
            right_in: right_in input
            left_in: left_in input

        Returns:
            Validated input model
        """
        return Comparison_DifferenceInput(right_in=right_in, left_in=left_in)

    def run(
        self, right_in: float, left_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            right_in: right_in input
            left_in: left_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(right_in, left_in)

        # Import handwritten implementation
        from exchanger_architecture_thermal_tea.handwritten.integrated_equipment_costs.comparison_difference_impl import (
            run_comparison_difference,
        )

        # Execute implementation - returns single value
        difference = run_comparison_difference(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(difference))
