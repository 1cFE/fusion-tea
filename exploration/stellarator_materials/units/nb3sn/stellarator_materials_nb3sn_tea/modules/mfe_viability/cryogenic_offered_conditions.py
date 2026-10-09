"""Cryogenic_Offered_ConditionsModule Module Wrapper

TEAx module for Cryogenic_Offered_Conditions calculation.

Point-rating applicability: finite actual/supplied values match when equal or separated by at most 8*max(ulp(actual),ulp(supplied)); fixed numerical identity only, no public tolerance or physical envelope. Disabled returns unsupported/undefined; no inferred envelope. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: round2/architecture-review.md; entering-model checkpoint 53a0366a. **Basis**: [AGENT] assumed offered capability at declared conditions; captured design, not vendor qualification. **Last Updated**: 2026-09-20

Inputs:
    - rated_ambient_K_in: rated_ambient_K_in parameter
    - rated_cold_K_in: rated_cold_K_in parameter
    - actual_ambient_K_in: actual_ambient_K_in parameter
    - actual_cold_K_in: actual_cold_K_in parameter
    - rated_intercept_K_in: rated_intercept_K_in parameter
    - enabled_in: enabled_in parameter
    - actual_intercept_K_in: actual_intercept_K_in parameter

Outputs:
    - supported: supported result
    - evaluation_defined: evaluation_defined result
    - applicable: applicable result

SysML Source: root-0/analyses/mfe_viability.sysml:74

SysML Source: root-0/analyses/mfe_viability.sysml:74

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_viability/cryogenic_offered_conditions_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float
from stellarator_materials_nb3sn_tea.schemas.cryogenic_offered_conditions_output import Cryogenic_Offered_ConditionsOutput


class Cryogenic_Offered_ConditionsInput(BaseModel):
    """Input model for Cryogenic_Offered_ConditionsModule.

    Attributes:
        rated_ambient_K_in: rated_ambient_K_in input
        rated_cold_K_in: rated_cold_K_in input
        actual_ambient_K_in: actual_ambient_K_in input
        actual_cold_K_in: actual_cold_K_in input
        rated_intercept_K_in: rated_intercept_K_in input
        enabled_in: enabled_in input
        actual_intercept_K_in: actual_intercept_K_in input
    """
    rated_ambient_K_in: float = Field(..., description="rated_ambient_K_in input")
    rated_cold_K_in: float = Field(..., description="rated_cold_K_in input")
    actual_ambient_K_in: float = Field(..., description="actual_ambient_K_in input")
    actual_cold_K_in: float = Field(..., description="actual_cold_K_in input")
    rated_intercept_K_in: float = Field(..., description="rated_intercept_K_in input")
    enabled_in: bool = Field(..., description="enabled_in input")
    actual_intercept_K_in: float = Field(..., description="actual_intercept_K_in input")


class Cryogenic_Offered_ConditionsModule(ModuleBase[Cryogenic_Offered_ConditionsInput, Cryogenic_Offered_ConditionsOutput]):
    """TEAx module for Cryogenic_Offered_Conditions calculation.

Point-rating applicability: finite actual/supplied values match when equal or separated by at most 8*max(ulp(actual),ulp(supplied)); fixed numerical identity only, no public tolerance or physical envelope. Disabled returns unsupported/undefined; no inferred envelope. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: round2/architecture-review.md; entering-model checkpoint 53a0366a. **Basis**: [AGENT] assumed offered capability at declared conditions; captured design, not vendor qualification. **Last Updated**: 2026-09-20

Inputs:
    - rated_ambient_K_in: rated_ambient_K_in parameter
    - rated_cold_K_in: rated_cold_K_in parameter
    - actual_ambient_K_in: actual_ambient_K_in parameter
    - actual_cold_K_in: actual_cold_K_in parameter
    - rated_intercept_K_in: rated_intercept_K_in parameter
    - enabled_in: enabled_in parameter
    - actual_intercept_K_in: actual_intercept_K_in parameter

Outputs:
    - supported: supported result
    - evaluation_defined: evaluation_defined result
    - applicable: applicable result

SysML Source: root-0/analyses/mfe_viability.sysml:74

    SysML Source: root-0/analyses/mfe_viability.sysml:74

    Calculation Specification:
        See documentation:
Point-rating applicability: finite actual/supplied values match when equal or separated by at most 8*max(ulp(actual),ulp(supplied)); fixed numerical identity only, no public tolerance or physical envelope. Disabled returns unsupported/undefined; no inferred envelope. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: round2/architecture-review.md; entering-model checkpoint 53a0366a. **Basis**: [AGENT] assumed offered capability at declared conditions; captured design, not vendor qualification. **Last Updated**: 2026-09-20

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.mfe_viability.cryogenic_offered_conditions_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts supported, evaluation_defined, applicable fields to separate channels.
    """

    name: str = "Cryogenic_Offered_ConditionsModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, rated_ambient_K_in: float, rated_cold_K_in: float, actual_ambient_K_in: float, actual_cold_K_in: float, rated_intercept_K_in: float, enabled_in: bool, actual_intercept_K_in: float    ) -> Cryogenic_Offered_ConditionsInput:
        """Validate inputs and fill defaults.

        Args:
            rated_ambient_K_in: rated_ambient_K_in input
            rated_cold_K_in: rated_cold_K_in input
            actual_ambient_K_in: actual_ambient_K_in input
            actual_cold_K_in: actual_cold_K_in input
            rated_intercept_K_in: rated_intercept_K_in input
            enabled_in: enabled_in input
            actual_intercept_K_in: actual_intercept_K_in input

        Returns:
            Validated input model
        """
        return Cryogenic_Offered_ConditionsInput(rated_ambient_K_in=rated_ambient_K_in, rated_cold_K_in=rated_cold_K_in, actual_ambient_K_in=actual_ambient_K_in, actual_cold_K_in=actual_cold_K_in, rated_intercept_K_in=rated_intercept_K_in, enabled_in=enabled_in, actual_intercept_K_in=actual_intercept_K_in)

    def run(
        self, rated_ambient_K_in: float, rated_cold_K_in: float, actual_ambient_K_in: float, actual_cold_K_in: float, rated_intercept_K_in: float, enabled_in: bool, actual_intercept_K_in: float    ) -> ModuleResult[Cryogenic_Offered_ConditionsOutput]:
        """Execute calculation.

        Args:
            rated_ambient_K_in: rated_ambient_K_in input
            rated_cold_K_in: rated_cold_K_in input
            actual_ambient_K_in: actual_ambient_K_in input
            actual_cold_K_in: actual_cold_K_in input
            rated_intercept_K_in: rated_intercept_K_in input
            enabled_in: enabled_in input
            actual_intercept_K_in: actual_intercept_K_in input

        Returns:
            Module result with Cryogenic_Offered_ConditionsOutput (supported, evaluation_defined, applicable)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(rated_ambient_K_in, rated_cold_K_in, actual_ambient_K_in, actual_cold_K_in, rated_intercept_K_in, enabled_in, actual_intercept_K_in)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.mfe_viability.cryogenic_offered_conditions_impl import (
            run_cryogenic_offered_conditions,
        )

        # Execute implementation - returns tuple of values
        supported, evaluation_defined, applicable = run_cryogenic_offered_conditions(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Cryogenic_Offered_ConditionsOutput(
                supported=supported,
                evaluation_defined=evaluation_defined,
                applicable=applicable,
            )
        )
