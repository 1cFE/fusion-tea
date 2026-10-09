"""Steam_Offered_ConditionsModule Module Wrapper

TEAx module for Steam_Offered_Conditions calculation.

Point-rating applicability: finite actual/supplied values match when equal or separated by at most 8*max(ulp(actual),ulp(supplied)); fixed numerical identity only, no public tolerance or physical envelope. Disabled returns unsupported/undefined; no inferred envelope. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: round2/architecture-review.md; entering-model checkpoint 53a0366a. **Basis**: [AGENT] assumed offered capability at declared conditions; captured design, not vendor qualification. **Last Updated**: 2026-09-20

Inputs:
    - actual_condenser_C_in: actual_condenser_C_in parameter
    - actual_reheat_C_in: actual_reheat_C_in parameter
    - actual_salt_hot_C_in: actual_salt_hot_C_in parameter
    - actual_steam_C_in: actual_steam_C_in parameter
    - actual_extraction_pressure_MPa_in: actual_extraction_pressure_MPa_in parameter
    - rated_reheat_C_in: rated_reheat_C_in parameter
    - actual_salt_return_C_in: actual_salt_return_C_in parameter
    - actual_main_pressure_MPa_in: actual_main_pressure_MPa_in parameter
    - enabled_in: enabled_in parameter
    - rated_salt_return_C_in: rated_salt_return_C_in parameter
    - rated_salt_cp_in: rated_salt_cp_in parameter
    - rated_condenser_C_in: rated_condenser_C_in parameter
    - rated_salt_hot_C_in: rated_salt_hot_C_in parameter
    - rated_steam_C_in: rated_steam_C_in parameter
    - rated_main_pressure_MPa_in: rated_main_pressure_MPa_in parameter
    - rated_extraction_pressure_MPa_in: rated_extraction_pressure_MPa_in parameter
    - actual_salt_cp_in: actual_salt_cp_in parameter

Outputs:
    - supported: supported result
    - applicable: applicable result
    - evaluation_defined: evaluation_defined result

SysML Source: root-0/analyses/mfe_viability.sysml:38

SysML Source: root-0/analyses/mfe_viability.sysml:38

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_viability/steam_offered_conditions_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float
from stellarator_materials_nb3sn_tea.schemas.steam_offered_conditions_output import Steam_Offered_ConditionsOutput


class Steam_Offered_ConditionsInput(BaseModel):
    """Input model for Steam_Offered_ConditionsModule.

    Attributes:
        actual_condenser_C_in: actual_condenser_C_in input
        actual_reheat_C_in: actual_reheat_C_in input
        actual_salt_hot_C_in: actual_salt_hot_C_in input
        actual_steam_C_in: actual_steam_C_in input
        actual_extraction_pressure_MPa_in: actual_extraction_pressure_MPa_in input
        rated_reheat_C_in: rated_reheat_C_in input
        actual_salt_return_C_in: actual_salt_return_C_in input
        actual_main_pressure_MPa_in: actual_main_pressure_MPa_in input
        enabled_in: enabled_in input
        rated_salt_return_C_in: rated_salt_return_C_in input
        rated_salt_cp_in: rated_salt_cp_in input
        rated_condenser_C_in: rated_condenser_C_in input
        rated_salt_hot_C_in: rated_salt_hot_C_in input
        rated_steam_C_in: rated_steam_C_in input
        rated_main_pressure_MPa_in: rated_main_pressure_MPa_in input
        rated_extraction_pressure_MPa_in: rated_extraction_pressure_MPa_in input
        actual_salt_cp_in: actual_salt_cp_in input
    """
    actual_condenser_C_in: float = Field(..., description="actual_condenser_C_in input")
    actual_reheat_C_in: float = Field(..., description="actual_reheat_C_in input")
    actual_salt_hot_C_in: float = Field(..., description="actual_salt_hot_C_in input")
    actual_steam_C_in: float = Field(..., description="actual_steam_C_in input")
    actual_extraction_pressure_MPa_in: float = Field(..., description="actual_extraction_pressure_MPa_in input")
    rated_reheat_C_in: float = Field(..., description="rated_reheat_C_in input")
    actual_salt_return_C_in: float = Field(..., description="actual_salt_return_C_in input")
    actual_main_pressure_MPa_in: float = Field(..., description="actual_main_pressure_MPa_in input")
    enabled_in: bool = Field(..., description="enabled_in input")
    rated_salt_return_C_in: float = Field(..., description="rated_salt_return_C_in input")
    rated_salt_cp_in: float = Field(..., description="rated_salt_cp_in input")
    rated_condenser_C_in: float = Field(..., description="rated_condenser_C_in input")
    rated_salt_hot_C_in: float = Field(..., description="rated_salt_hot_C_in input")
    rated_steam_C_in: float = Field(..., description="rated_steam_C_in input")
    rated_main_pressure_MPa_in: float = Field(..., description="rated_main_pressure_MPa_in input")
    rated_extraction_pressure_MPa_in: float = Field(..., description="rated_extraction_pressure_MPa_in input")
    actual_salt_cp_in: float = Field(..., description="actual_salt_cp_in input")


class Steam_Offered_ConditionsModule(ModuleBase[Steam_Offered_ConditionsInput, Steam_Offered_ConditionsOutput]):
    """TEAx module for Steam_Offered_Conditions calculation.

Point-rating applicability: finite actual/supplied values match when equal or separated by at most 8*max(ulp(actual),ulp(supplied)); fixed numerical identity only, no public tolerance or physical envelope. Disabled returns unsupported/undefined; no inferred envelope. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: round2/architecture-review.md; entering-model checkpoint 53a0366a. **Basis**: [AGENT] assumed offered capability at declared conditions; captured design, not vendor qualification. **Last Updated**: 2026-09-20

Inputs:
    - actual_condenser_C_in: actual_condenser_C_in parameter
    - actual_reheat_C_in: actual_reheat_C_in parameter
    - actual_salt_hot_C_in: actual_salt_hot_C_in parameter
    - actual_steam_C_in: actual_steam_C_in parameter
    - actual_extraction_pressure_MPa_in: actual_extraction_pressure_MPa_in parameter
    - rated_reheat_C_in: rated_reheat_C_in parameter
    - actual_salt_return_C_in: actual_salt_return_C_in parameter
    - actual_main_pressure_MPa_in: actual_main_pressure_MPa_in parameter
    - enabled_in: enabled_in parameter
    - rated_salt_return_C_in: rated_salt_return_C_in parameter
    - rated_salt_cp_in: rated_salt_cp_in parameter
    - rated_condenser_C_in: rated_condenser_C_in parameter
    - rated_salt_hot_C_in: rated_salt_hot_C_in parameter
    - rated_steam_C_in: rated_steam_C_in parameter
    - rated_main_pressure_MPa_in: rated_main_pressure_MPa_in parameter
    - rated_extraction_pressure_MPa_in: rated_extraction_pressure_MPa_in parameter
    - actual_salt_cp_in: actual_salt_cp_in parameter

Outputs:
    - supported: supported result
    - applicable: applicable result
    - evaluation_defined: evaluation_defined result

SysML Source: root-0/analyses/mfe_viability.sysml:38

    SysML Source: root-0/analyses/mfe_viability.sysml:38

    Calculation Specification:
        See documentation:
Point-rating applicability: finite actual/supplied values match when equal or separated by at most 8*max(ulp(actual),ulp(supplied)); fixed numerical identity only, no public tolerance or physical envelope. Disabled returns unsupported/undefined; no inferred envelope. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: round2/architecture-review.md; entering-model checkpoint 53a0366a. **Basis**: [AGENT] assumed offered capability at declared conditions; captured design, not vendor qualification. **Last Updated**: 2026-09-20

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.mfe_viability.steam_offered_conditions_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts supported, applicable, evaluation_defined fields to separate channels.
    """

    name: str = "Steam_Offered_ConditionsModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, actual_condenser_C_in: float, actual_reheat_C_in: float, actual_salt_hot_C_in: float, actual_steam_C_in: float, actual_extraction_pressure_MPa_in: float, rated_reheat_C_in: float, actual_salt_return_C_in: float, actual_main_pressure_MPa_in: float, enabled_in: bool, rated_salt_return_C_in: float, rated_salt_cp_in: float, rated_condenser_C_in: float, rated_salt_hot_C_in: float, rated_steam_C_in: float, rated_main_pressure_MPa_in: float, rated_extraction_pressure_MPa_in: float, actual_salt_cp_in: float    ) -> Steam_Offered_ConditionsInput:
        """Validate inputs and fill defaults.

        Args:
            actual_condenser_C_in: actual_condenser_C_in input
            actual_reheat_C_in: actual_reheat_C_in input
            actual_salt_hot_C_in: actual_salt_hot_C_in input
            actual_steam_C_in: actual_steam_C_in input
            actual_extraction_pressure_MPa_in: actual_extraction_pressure_MPa_in input
            rated_reheat_C_in: rated_reheat_C_in input
            actual_salt_return_C_in: actual_salt_return_C_in input
            actual_main_pressure_MPa_in: actual_main_pressure_MPa_in input
            enabled_in: enabled_in input
            rated_salt_return_C_in: rated_salt_return_C_in input
            rated_salt_cp_in: rated_salt_cp_in input
            rated_condenser_C_in: rated_condenser_C_in input
            rated_salt_hot_C_in: rated_salt_hot_C_in input
            rated_steam_C_in: rated_steam_C_in input
            rated_main_pressure_MPa_in: rated_main_pressure_MPa_in input
            rated_extraction_pressure_MPa_in: rated_extraction_pressure_MPa_in input
            actual_salt_cp_in: actual_salt_cp_in input

        Returns:
            Validated input model
        """
        return Steam_Offered_ConditionsInput(actual_condenser_C_in=actual_condenser_C_in, actual_reheat_C_in=actual_reheat_C_in, actual_salt_hot_C_in=actual_salt_hot_C_in, actual_steam_C_in=actual_steam_C_in, actual_extraction_pressure_MPa_in=actual_extraction_pressure_MPa_in, rated_reheat_C_in=rated_reheat_C_in, actual_salt_return_C_in=actual_salt_return_C_in, actual_main_pressure_MPa_in=actual_main_pressure_MPa_in, enabled_in=enabled_in, rated_salt_return_C_in=rated_salt_return_C_in, rated_salt_cp_in=rated_salt_cp_in, rated_condenser_C_in=rated_condenser_C_in, rated_salt_hot_C_in=rated_salt_hot_C_in, rated_steam_C_in=rated_steam_C_in, rated_main_pressure_MPa_in=rated_main_pressure_MPa_in, rated_extraction_pressure_MPa_in=rated_extraction_pressure_MPa_in, actual_salt_cp_in=actual_salt_cp_in)

    def run(
        self, actual_condenser_C_in: float, actual_reheat_C_in: float, actual_salt_hot_C_in: float, actual_steam_C_in: float, actual_extraction_pressure_MPa_in: float, rated_reheat_C_in: float, actual_salt_return_C_in: float, actual_main_pressure_MPa_in: float, enabled_in: bool, rated_salt_return_C_in: float, rated_salt_cp_in: float, rated_condenser_C_in: float, rated_salt_hot_C_in: float, rated_steam_C_in: float, rated_main_pressure_MPa_in: float, rated_extraction_pressure_MPa_in: float, actual_salt_cp_in: float    ) -> ModuleResult[Steam_Offered_ConditionsOutput]:
        """Execute calculation.

        Args:
            actual_condenser_C_in: actual_condenser_C_in input
            actual_reheat_C_in: actual_reheat_C_in input
            actual_salt_hot_C_in: actual_salt_hot_C_in input
            actual_steam_C_in: actual_steam_C_in input
            actual_extraction_pressure_MPa_in: actual_extraction_pressure_MPa_in input
            rated_reheat_C_in: rated_reheat_C_in input
            actual_salt_return_C_in: actual_salt_return_C_in input
            actual_main_pressure_MPa_in: actual_main_pressure_MPa_in input
            enabled_in: enabled_in input
            rated_salt_return_C_in: rated_salt_return_C_in input
            rated_salt_cp_in: rated_salt_cp_in input
            rated_condenser_C_in: rated_condenser_C_in input
            rated_salt_hot_C_in: rated_salt_hot_C_in input
            rated_steam_C_in: rated_steam_C_in input
            rated_main_pressure_MPa_in: rated_main_pressure_MPa_in input
            rated_extraction_pressure_MPa_in: rated_extraction_pressure_MPa_in input
            actual_salt_cp_in: actual_salt_cp_in input

        Returns:
            Module result with Steam_Offered_ConditionsOutput (supported, applicable, evaluation_defined)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(actual_condenser_C_in, actual_reheat_C_in, actual_salt_hot_C_in, actual_steam_C_in, actual_extraction_pressure_MPa_in, rated_reheat_C_in, actual_salt_return_C_in, actual_main_pressure_MPa_in, enabled_in, rated_salt_return_C_in, rated_salt_cp_in, rated_condenser_C_in, rated_salt_hot_C_in, rated_steam_C_in, rated_main_pressure_MPa_in, rated_extraction_pressure_MPa_in, actual_salt_cp_in)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.mfe_viability.steam_offered_conditions_impl import (
            run_steam_offered_conditions,
        )

        # Execute implementation - returns tuple of values
        supported, applicable, evaluation_defined = run_steam_offered_conditions(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Steam_Offered_ConditionsOutput(
                supported=supported,
                applicable=applicable,
                evaluation_defined=evaluation_defined,
            )
        )
