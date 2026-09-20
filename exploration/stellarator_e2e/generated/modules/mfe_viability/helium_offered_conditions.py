"""Helium_Offered_ConditionsModule Module Wrapper

TEAx module for Helium_Offered_Conditions calculation.

Point-rating applicability: finite actual/supplied values match when equal or separated by at most 8*max(ulp(actual),ulp(supplied)); fixed numerical identity only, no public tolerance or physical envelope. Disabled returns unsupported/undefined; no inferred envelope. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: round2/architecture-review.md; entering-model checkpoint 53a0366a. **Basis**: [AGENT] assumed offered capability at declared conditions; captured design, not vendor qualification. **Last Updated**: 2026-09-20

Inputs:
    - actual_suction_K_in: actual_suction_K_in parameter
    - mode_in: mode_in parameter
    - actual_suction_Pa_in: actual_suction_Pa_in parameter
    - actual_hot_K_in: actual_hot_K_in parameter
    - rated_hot_K_in: rated_hot_K_in parameter
    - actual_gamma_in: actual_gamma_in parameter
    - enabled_in: enabled_in parameter
    - rated_gamma_in: rated_gamma_in parameter
    - actual_discharge_Pa_in: actual_discharge_Pa_in parameter
    - rated_discharge_Pa_in: rated_discharge_Pa_in parameter
    - rated_suction_K_in: rated_suction_K_in parameter
    - rated_suction_Pa_in: rated_suction_Pa_in parameter
    - rated_cp_in: rated_cp_in parameter
    - actual_cp_in: actual_cp_in parameter

Outputs:
    - evaluation_defined: evaluation_defined result
    - supported: supported result
    - applicable: applicable result

SysML Source: root-0/analyses/mfe_viability.sysml:4

SysML Source: root-0/analyses/mfe_viability.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_viability/helium_offered_conditions_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float
from stellarator_tea.schemas.helium_offered_conditions_output import Helium_Offered_ConditionsOutput


class Helium_Offered_ConditionsInput(BaseModel):
    """Input model for Helium_Offered_ConditionsModule.

    Attributes:
        actual_suction_K_in: actual_suction_K_in input
        mode_in: mode_in input
        actual_suction_Pa_in: actual_suction_Pa_in input
        actual_hot_K_in: actual_hot_K_in input
        rated_hot_K_in: rated_hot_K_in input
        actual_gamma_in: actual_gamma_in input
        enabled_in: enabled_in input
        rated_gamma_in: rated_gamma_in input
        actual_discharge_Pa_in: actual_discharge_Pa_in input
        rated_discharge_Pa_in: rated_discharge_Pa_in input
        rated_suction_K_in: rated_suction_K_in input
        rated_suction_Pa_in: rated_suction_Pa_in input
        rated_cp_in: rated_cp_in input
        actual_cp_in: actual_cp_in input
    """
    actual_suction_K_in: float = Field(..., description="actual_suction_K_in input")
    mode_in: float = Field(..., description="mode_in input")
    actual_suction_Pa_in: float = Field(..., description="actual_suction_Pa_in input")
    actual_hot_K_in: float = Field(..., description="actual_hot_K_in input")
    rated_hot_K_in: float = Field(..., description="rated_hot_K_in input")
    actual_gamma_in: float = Field(..., description="actual_gamma_in input")
    enabled_in: bool = Field(..., description="enabled_in input")
    rated_gamma_in: float = Field(..., description="rated_gamma_in input")
    actual_discharge_Pa_in: float = Field(..., description="actual_discharge_Pa_in input")
    rated_discharge_Pa_in: float = Field(..., description="rated_discharge_Pa_in input")
    rated_suction_K_in: float = Field(..., description="rated_suction_K_in input")
    rated_suction_Pa_in: float = Field(..., description="rated_suction_Pa_in input")
    rated_cp_in: float = Field(..., description="rated_cp_in input")
    actual_cp_in: float = Field(..., description="actual_cp_in input")


class Helium_Offered_ConditionsModule(ModuleBase[Helium_Offered_ConditionsInput, Helium_Offered_ConditionsOutput]):
    """TEAx module for Helium_Offered_Conditions calculation.

Point-rating applicability: finite actual/supplied values match when equal or separated by at most 8*max(ulp(actual),ulp(supplied)); fixed numerical identity only, no public tolerance or physical envelope. Disabled returns unsupported/undefined; no inferred envelope. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: round2/architecture-review.md; entering-model checkpoint 53a0366a. **Basis**: [AGENT] assumed offered capability at declared conditions; captured design, not vendor qualification. **Last Updated**: 2026-09-20

Inputs:
    - actual_suction_K_in: actual_suction_K_in parameter
    - mode_in: mode_in parameter
    - actual_suction_Pa_in: actual_suction_Pa_in parameter
    - actual_hot_K_in: actual_hot_K_in parameter
    - rated_hot_K_in: rated_hot_K_in parameter
    - actual_gamma_in: actual_gamma_in parameter
    - enabled_in: enabled_in parameter
    - rated_gamma_in: rated_gamma_in parameter
    - actual_discharge_Pa_in: actual_discharge_Pa_in parameter
    - rated_discharge_Pa_in: rated_discharge_Pa_in parameter
    - rated_suction_K_in: rated_suction_K_in parameter
    - rated_suction_Pa_in: rated_suction_Pa_in parameter
    - rated_cp_in: rated_cp_in parameter
    - actual_cp_in: actual_cp_in parameter

Outputs:
    - evaluation_defined: evaluation_defined result
    - supported: supported result
    - applicable: applicable result

SysML Source: root-0/analyses/mfe_viability.sysml:4

    SysML Source: root-0/analyses/mfe_viability.sysml:4

    Calculation Specification:
        See documentation:
Point-rating applicability: finite actual/supplied values match when equal or separated by at most 8*max(ulp(actual),ulp(supplied)); fixed numerical identity only, no public tolerance or physical envelope. Disabled returns unsupported/undefined; no inferred envelope. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: round2/architecture-review.md; entering-model checkpoint 53a0366a. **Basis**: [AGENT] assumed offered capability at declared conditions; captured design, not vendor qualification. **Last Updated**: 2026-09-20

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_viability.helium_offered_conditions_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts evaluation_defined, supported, applicable fields to separate channels.
    """

    name: str = "Helium_Offered_ConditionsModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, actual_suction_K_in: float, mode_in: float, actual_suction_Pa_in: float, actual_hot_K_in: float, rated_hot_K_in: float, actual_gamma_in: float, enabled_in: bool, rated_gamma_in: float, actual_discharge_Pa_in: float, rated_discharge_Pa_in: float, rated_suction_K_in: float, rated_suction_Pa_in: float, rated_cp_in: float, actual_cp_in: float    ) -> Helium_Offered_ConditionsInput:
        """Validate inputs and fill defaults.

        Args:
            actual_suction_K_in: actual_suction_K_in input
            mode_in: mode_in input
            actual_suction_Pa_in: actual_suction_Pa_in input
            actual_hot_K_in: actual_hot_K_in input
            rated_hot_K_in: rated_hot_K_in input
            actual_gamma_in: actual_gamma_in input
            enabled_in: enabled_in input
            rated_gamma_in: rated_gamma_in input
            actual_discharge_Pa_in: actual_discharge_Pa_in input
            rated_discharge_Pa_in: rated_discharge_Pa_in input
            rated_suction_K_in: rated_suction_K_in input
            rated_suction_Pa_in: rated_suction_Pa_in input
            rated_cp_in: rated_cp_in input
            actual_cp_in: actual_cp_in input

        Returns:
            Validated input model
        """
        return Helium_Offered_ConditionsInput(actual_suction_K_in=actual_suction_K_in, mode_in=mode_in, actual_suction_Pa_in=actual_suction_Pa_in, actual_hot_K_in=actual_hot_K_in, rated_hot_K_in=rated_hot_K_in, actual_gamma_in=actual_gamma_in, enabled_in=enabled_in, rated_gamma_in=rated_gamma_in, actual_discharge_Pa_in=actual_discharge_Pa_in, rated_discharge_Pa_in=rated_discharge_Pa_in, rated_suction_K_in=rated_suction_K_in, rated_suction_Pa_in=rated_suction_Pa_in, rated_cp_in=rated_cp_in, actual_cp_in=actual_cp_in)

    def run(
        self, actual_suction_K_in: float, mode_in: float, actual_suction_Pa_in: float, actual_hot_K_in: float, rated_hot_K_in: float, actual_gamma_in: float, enabled_in: bool, rated_gamma_in: float, actual_discharge_Pa_in: float, rated_discharge_Pa_in: float, rated_suction_K_in: float, rated_suction_Pa_in: float, rated_cp_in: float, actual_cp_in: float    ) -> ModuleResult[Helium_Offered_ConditionsOutput]:
        """Execute calculation.

        Args:
            actual_suction_K_in: actual_suction_K_in input
            mode_in: mode_in input
            actual_suction_Pa_in: actual_suction_Pa_in input
            actual_hot_K_in: actual_hot_K_in input
            rated_hot_K_in: rated_hot_K_in input
            actual_gamma_in: actual_gamma_in input
            enabled_in: enabled_in input
            rated_gamma_in: rated_gamma_in input
            actual_discharge_Pa_in: actual_discharge_Pa_in input
            rated_discharge_Pa_in: rated_discharge_Pa_in input
            rated_suction_K_in: rated_suction_K_in input
            rated_suction_Pa_in: rated_suction_Pa_in input
            rated_cp_in: rated_cp_in input
            actual_cp_in: actual_cp_in input

        Returns:
            Module result with Helium_Offered_ConditionsOutput (evaluation_defined, supported, applicable)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(actual_suction_K_in, mode_in, actual_suction_Pa_in, actual_hot_K_in, rated_hot_K_in, actual_gamma_in, enabled_in, rated_gamma_in, actual_discharge_Pa_in, rated_discharge_Pa_in, rated_suction_K_in, rated_suction_Pa_in, rated_cp_in, actual_cp_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_viability.helium_offered_conditions_impl import (
            run_helium_offered_conditions,
        )

        # Execute implementation - returns tuple of values
        evaluation_defined, supported, applicable = run_helium_offered_conditions(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Helium_Offered_ConditionsOutput(
                evaluation_defined=evaluation_defined,
                supported=supported,
                applicable=applicable,
            )
        )
