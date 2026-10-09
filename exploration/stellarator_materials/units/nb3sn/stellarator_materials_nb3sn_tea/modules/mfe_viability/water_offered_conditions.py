"""Water_Offered_ConditionsModule Module Wrapper

TEAx module for Water_Offered_Conditions calculation.

Point-rating applicability: finite actual/supplied values match when equal or separated by at most 8*max(ulp(actual),ulp(supplied)); fixed numerical identity only, no public tolerance or physical envelope. Disabled returns unsupported/undefined; no inferred envelope. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: round2/architecture-review.md; entering-model checkpoint 53a0366a. **Basis**: [AGENT] assumed offered capability at declared conditions; captured design, not vendor qualification. **Last Updated**: 2026-09-20

Inputs:
    - rated_inlet_C_in: rated_inlet_C_in parameter
    - actual_outlet_C_in: actual_outlet_C_in parameter
    - actual_condenser_C_in: actual_condenser_C_in parameter
    - actual_inlet_C_in: actual_inlet_C_in parameter
    - rated_outlet_C_in: rated_outlet_C_in parameter
    - rated_condenser_C_in: rated_condenser_C_in parameter
    - enabled_in: enabled_in parameter

Outputs:
    - supported: supported result
    - applicable: applicable result
    - evaluation_defined: evaluation_defined result

SysML Source: root-0/analyses/mfe_viability.sysml:61

SysML Source: root-0/analyses/mfe_viability.sysml:61

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_viability/water_offered_conditions_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float
from stellarator_materials_nb3sn_tea.schemas.water_offered_conditions_output import Water_Offered_ConditionsOutput


class Water_Offered_ConditionsInput(BaseModel):
    """Input model for Water_Offered_ConditionsModule.

    Attributes:
        rated_inlet_C_in: rated_inlet_C_in input
        actual_outlet_C_in: actual_outlet_C_in input
        actual_condenser_C_in: actual_condenser_C_in input
        actual_inlet_C_in: actual_inlet_C_in input
        rated_outlet_C_in: rated_outlet_C_in input
        rated_condenser_C_in: rated_condenser_C_in input
        enabled_in: enabled_in input
    """
    rated_inlet_C_in: float = Field(..., description="rated_inlet_C_in input")
    actual_outlet_C_in: float = Field(..., description="actual_outlet_C_in input")
    actual_condenser_C_in: float = Field(..., description="actual_condenser_C_in input")
    actual_inlet_C_in: float = Field(..., description="actual_inlet_C_in input")
    rated_outlet_C_in: float = Field(..., description="rated_outlet_C_in input")
    rated_condenser_C_in: float = Field(..., description="rated_condenser_C_in input")
    enabled_in: bool = Field(..., description="enabled_in input")


class Water_Offered_ConditionsModule(ModuleBase[Water_Offered_ConditionsInput, Water_Offered_ConditionsOutput]):
    """TEAx module for Water_Offered_Conditions calculation.

Point-rating applicability: finite actual/supplied values match when equal or separated by at most 8*max(ulp(actual),ulp(supplied)); fixed numerical identity only, no public tolerance or physical envelope. Disabled returns unsupported/undefined; no inferred envelope. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: round2/architecture-review.md; entering-model checkpoint 53a0366a. **Basis**: [AGENT] assumed offered capability at declared conditions; captured design, not vendor qualification. **Last Updated**: 2026-09-20

Inputs:
    - rated_inlet_C_in: rated_inlet_C_in parameter
    - actual_outlet_C_in: actual_outlet_C_in parameter
    - actual_condenser_C_in: actual_condenser_C_in parameter
    - actual_inlet_C_in: actual_inlet_C_in parameter
    - rated_outlet_C_in: rated_outlet_C_in parameter
    - rated_condenser_C_in: rated_condenser_C_in parameter
    - enabled_in: enabled_in parameter

Outputs:
    - supported: supported result
    - applicable: applicable result
    - evaluation_defined: evaluation_defined result

SysML Source: root-0/analyses/mfe_viability.sysml:61

    SysML Source: root-0/analyses/mfe_viability.sysml:61

    Calculation Specification:
        See documentation:
Point-rating applicability: finite actual/supplied values match when equal or separated by at most 8*max(ulp(actual),ulp(supplied)); fixed numerical identity only, no public tolerance or physical envelope. Disabled returns unsupported/undefined; no inferred envelope. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: round2/architecture-review.md; entering-model checkpoint 53a0366a. **Basis**: [AGENT] assumed offered capability at declared conditions; captured design, not vendor qualification. **Last Updated**: 2026-09-20

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.mfe_viability.water_offered_conditions_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts supported, applicable, evaluation_defined fields to separate channels.
    """

    name: str = "Water_Offered_ConditionsModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, rated_inlet_C_in: float, actual_outlet_C_in: float, actual_condenser_C_in: float, actual_inlet_C_in: float, rated_outlet_C_in: float, rated_condenser_C_in: float, enabled_in: bool    ) -> Water_Offered_ConditionsInput:
        """Validate inputs and fill defaults.

        Args:
            rated_inlet_C_in: rated_inlet_C_in input
            actual_outlet_C_in: actual_outlet_C_in input
            actual_condenser_C_in: actual_condenser_C_in input
            actual_inlet_C_in: actual_inlet_C_in input
            rated_outlet_C_in: rated_outlet_C_in input
            rated_condenser_C_in: rated_condenser_C_in input
            enabled_in: enabled_in input

        Returns:
            Validated input model
        """
        return Water_Offered_ConditionsInput(rated_inlet_C_in=rated_inlet_C_in, actual_outlet_C_in=actual_outlet_C_in, actual_condenser_C_in=actual_condenser_C_in, actual_inlet_C_in=actual_inlet_C_in, rated_outlet_C_in=rated_outlet_C_in, rated_condenser_C_in=rated_condenser_C_in, enabled_in=enabled_in)

    def run(
        self, rated_inlet_C_in: float, actual_outlet_C_in: float, actual_condenser_C_in: float, actual_inlet_C_in: float, rated_outlet_C_in: float, rated_condenser_C_in: float, enabled_in: bool    ) -> ModuleResult[Water_Offered_ConditionsOutput]:
        """Execute calculation.

        Args:
            rated_inlet_C_in: rated_inlet_C_in input
            actual_outlet_C_in: actual_outlet_C_in input
            actual_condenser_C_in: actual_condenser_C_in input
            actual_inlet_C_in: actual_inlet_C_in input
            rated_outlet_C_in: rated_outlet_C_in input
            rated_condenser_C_in: rated_condenser_C_in input
            enabled_in: enabled_in input

        Returns:
            Module result with Water_Offered_ConditionsOutput (supported, applicable, evaluation_defined)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(rated_inlet_C_in, actual_outlet_C_in, actual_condenser_C_in, actual_inlet_C_in, rated_outlet_C_in, rated_condenser_C_in, enabled_in)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.mfe_viability.water_offered_conditions_impl import (
            run_water_offered_conditions,
        )

        # Execute implementation - returns tuple of values
        supported, applicable, evaluation_defined = run_water_offered_conditions(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Water_Offered_ConditionsOutput(
                supported=supported,
                applicable=applicable,
                evaluation_defined=evaluation_defined,
            )
        )
