"""Already_Financed_DurationModule Module Wrapper

TEAx module for Already_Financed_Duration calculation.

*Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: source comparison financing-once invariant; focused independent review. **Basis**: supplied already-financed capital permits exactly zero additional construction duration. **Last Updated**: 2026-09-22.

Inputs:
    - years_in: years_in parameter

Outputs:
    - years: years result

SysML Source: root-0/integrated_lifecycle_costs.sysml:79

SysML Source: root-0/integrated_lifecycle_costs.sysml:79

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/integrated_lifecycle_costs/already_financed_duration_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from exchanger_architecture_thermal_tea.primitives import Float


class Already_Financed_DurationInput(BaseModel):
    """Input model for Already_Financed_DurationModule.

    Attributes:
        years_in: years_in input
    """
    years_in: float = Field(..., description="years_in input")


class Already_Financed_DurationModule(ModuleBase[Already_Financed_DurationInput, Float]):
    """TEAx module for Already_Financed_Duration calculation.

*Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: source comparison financing-once invariant; focused independent review. **Basis**: supplied already-financed capital permits exactly zero additional construction duration. **Last Updated**: 2026-09-22.

Inputs:
    - years_in: years_in parameter

Outputs:
    - years: years result

SysML Source: root-0/integrated_lifecycle_costs.sysml:79

    SysML Source: root-0/integrated_lifecycle_costs.sysml:79

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: source comparison financing-once invariant; focused independent review. **Basis**: supplied already-financed capital permits exactly zero additional construction duration. **Last Updated**: 2026-09-22.

    IMPLEMENTATION: See exchanger_architecture_thermal_tea.handwritten.integrated_lifecycle_costs.already_financed_duration_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Already_Financed_DurationModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, years_in: float    ) -> Already_Financed_DurationInput:
        """Validate inputs and fill defaults.

        Args:
            years_in: years_in input

        Returns:
            Validated input model
        """
        return Already_Financed_DurationInput(years_in=years_in)

    def run(
        self, years_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            years_in: years_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(years_in)

        # Import handwritten implementation
        from exchanger_architecture_thermal_tea.handwritten.integrated_lifecycle_costs.already_financed_duration_impl import (
            run_already_financed_duration,
        )

        # Execute implementation - returns single value
        years = run_already_financed_duration(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(years))
