"""Salt_Offered_ConditionsModule Module Wrapper

TEAx module for Salt_Offered_Conditions calculation.

Point-rating applicability: finite actual/supplied values match when equal or separated by at most 8*max(ulp(actual),ulp(supplied)); fixed numerical identity only, no public tolerance or physical envelope. Disabled returns unsupported/undefined; no inferred envelope. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: round2/architecture-review.md; entering-model checkpoint 53a0366a. **Basis**: [AGENT] assumed offered capability at declared conditions; captured design, not vendor qualification. **Last Updated**: 2026-09-20

Inputs:
    - actual_hot_C_in: actual_hot_C_in parameter
    - rated_return_C_in: rated_return_C_in parameter
    - rated_cp_in: rated_cp_in parameter
    - rated_hot_C_in: rated_hot_C_in parameter
    - actual_cp_in: actual_cp_in parameter
    - mode_in: mode_in parameter
    - enabled_in: enabled_in parameter
    - actual_return_C_in: actual_return_C_in parameter

Outputs:
    - supported: supported result
    - evaluation_defined: evaluation_defined result
    - applicable: applicable result

SysML Source: root-0/analyses/mfe_viability.sysml:24

SysML Source: root-0/analyses/mfe_viability.sysml:24

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_viability/salt_offered_conditions_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float
from stellarator_materials_nb3sn_tea.schemas.salt_offered_conditions_output import Salt_Offered_ConditionsOutput


class Salt_Offered_ConditionsInput(BaseModel):
    """Input model for Salt_Offered_ConditionsModule.

    Attributes:
        actual_hot_C_in: actual_hot_C_in input
        rated_return_C_in: rated_return_C_in input
        rated_cp_in: rated_cp_in input
        rated_hot_C_in: rated_hot_C_in input
        actual_cp_in: actual_cp_in input
        mode_in: mode_in input
        enabled_in: enabled_in input
        actual_return_C_in: actual_return_C_in input
    """
    actual_hot_C_in: float = Field(..., description="actual_hot_C_in input")
    rated_return_C_in: float = Field(..., description="rated_return_C_in input")
    rated_cp_in: float = Field(..., description="rated_cp_in input")
    rated_hot_C_in: float = Field(..., description="rated_hot_C_in input")
    actual_cp_in: float = Field(..., description="actual_cp_in input")
    mode_in: float = Field(..., description="mode_in input")
    enabled_in: bool = Field(..., description="enabled_in input")
    actual_return_C_in: float = Field(..., description="actual_return_C_in input")


class Salt_Offered_ConditionsModule(ModuleBase[Salt_Offered_ConditionsInput, Salt_Offered_ConditionsOutput]):
    """TEAx module for Salt_Offered_Conditions calculation.

Point-rating applicability: finite actual/supplied values match when equal or separated by at most 8*max(ulp(actual),ulp(supplied)); fixed numerical identity only, no public tolerance or physical envelope. Disabled returns unsupported/undefined; no inferred envelope. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: round2/architecture-review.md; entering-model checkpoint 53a0366a. **Basis**: [AGENT] assumed offered capability at declared conditions; captured design, not vendor qualification. **Last Updated**: 2026-09-20

Inputs:
    - actual_hot_C_in: actual_hot_C_in parameter
    - rated_return_C_in: rated_return_C_in parameter
    - rated_cp_in: rated_cp_in parameter
    - rated_hot_C_in: rated_hot_C_in parameter
    - actual_cp_in: actual_cp_in parameter
    - mode_in: mode_in parameter
    - enabled_in: enabled_in parameter
    - actual_return_C_in: actual_return_C_in parameter

Outputs:
    - supported: supported result
    - evaluation_defined: evaluation_defined result
    - applicable: applicable result

SysML Source: root-0/analyses/mfe_viability.sysml:24

    SysML Source: root-0/analyses/mfe_viability.sysml:24

    Calculation Specification:
        See documentation:
Point-rating applicability: finite actual/supplied values match when equal or separated by at most 8*max(ulp(actual),ulp(supplied)); fixed numerical identity only, no public tolerance or physical envelope. Disabled returns unsupported/undefined; no inferred envelope. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: round2/architecture-review.md; entering-model checkpoint 53a0366a. **Basis**: [AGENT] assumed offered capability at declared conditions; captured design, not vendor qualification. **Last Updated**: 2026-09-20

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.mfe_viability.salt_offered_conditions_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts supported, evaluation_defined, applicable fields to separate channels.
    """

    name: str = "Salt_Offered_ConditionsModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, actual_hot_C_in: float, rated_return_C_in: float, rated_cp_in: float, rated_hot_C_in: float, actual_cp_in: float, mode_in: float, enabled_in: bool, actual_return_C_in: float    ) -> Salt_Offered_ConditionsInput:
        """Validate inputs and fill defaults.

        Args:
            actual_hot_C_in: actual_hot_C_in input
            rated_return_C_in: rated_return_C_in input
            rated_cp_in: rated_cp_in input
            rated_hot_C_in: rated_hot_C_in input
            actual_cp_in: actual_cp_in input
            mode_in: mode_in input
            enabled_in: enabled_in input
            actual_return_C_in: actual_return_C_in input

        Returns:
            Validated input model
        """
        return Salt_Offered_ConditionsInput(actual_hot_C_in=actual_hot_C_in, rated_return_C_in=rated_return_C_in, rated_cp_in=rated_cp_in, rated_hot_C_in=rated_hot_C_in, actual_cp_in=actual_cp_in, mode_in=mode_in, enabled_in=enabled_in, actual_return_C_in=actual_return_C_in)

    def run(
        self, actual_hot_C_in: float, rated_return_C_in: float, rated_cp_in: float, rated_hot_C_in: float, actual_cp_in: float, mode_in: float, enabled_in: bool, actual_return_C_in: float    ) -> ModuleResult[Salt_Offered_ConditionsOutput]:
        """Execute calculation.

        Args:
            actual_hot_C_in: actual_hot_C_in input
            rated_return_C_in: rated_return_C_in input
            rated_cp_in: rated_cp_in input
            rated_hot_C_in: rated_hot_C_in input
            actual_cp_in: actual_cp_in input
            mode_in: mode_in input
            enabled_in: enabled_in input
            actual_return_C_in: actual_return_C_in input

        Returns:
            Module result with Salt_Offered_ConditionsOutput (supported, evaluation_defined, applicable)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(actual_hot_C_in, rated_return_C_in, rated_cp_in, rated_hot_C_in, actual_cp_in, mode_in, enabled_in, actual_return_C_in)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.mfe_viability.salt_offered_conditions_impl import (
            run_salt_offered_conditions,
        )

        # Execute implementation - returns tuple of values
        supported, evaluation_defined, applicable = run_salt_offered_conditions(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Salt_Offered_ConditionsOutput(
                supported=supported,
                evaluation_defined=evaluation_defined,
                applicable=applicable,
            )
        )
