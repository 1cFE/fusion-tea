"""Cooling_Scenario_GuardModule Module Wrapper

TEAx module for Cooling_Scenario_Guard calculation.

Validate supported scenario choices before using zero dormant outputs.
Both modes must be finite and exactly zero or one. If either mode is one,
equipment_enabled_in must be true; otherwise raise ValueError. Return the
validated cost_mode_in and energy_mode_in unchanged. False/zero/zero is the
generic dormant scenario. Manual completion supplies the explicit guards.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Implementation review control-domain correction; Basis: scenario validity.

Inputs:
    - equipment_enabled_in: equipment_enabled_in parameter
    - energy_mode_in: energy_mode_in parameter
    - cost_mode_in: cost_mode_in parameter

Outputs:
    - energy_mode: energy_mode result
    - cost_mode: cost_mode result

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:4

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_cooling_accounts/cooling_scenario_guard_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_reference_tea.primitives import Float
from stellarator_materials_reference_tea.schemas.cooling_scenario_guard_output import Cooling_Scenario_GuardOutput


class Cooling_Scenario_GuardInput(BaseModel):
    """Input model for Cooling_Scenario_GuardModule.

    Attributes:
        equipment_enabled_in: equipment_enabled_in input
        energy_mode_in: energy_mode_in input
        cost_mode_in: cost_mode_in input
    """
    equipment_enabled_in: bool = Field(..., description="equipment_enabled_in input")
    energy_mode_in: float = Field(..., description="energy_mode_in input")
    cost_mode_in: float = Field(..., description="cost_mode_in input")


class Cooling_Scenario_GuardModule(ModuleBase[Cooling_Scenario_GuardInput, Cooling_Scenario_GuardOutput]):
    """TEAx module for Cooling_Scenario_Guard calculation.

Validate supported scenario choices before using zero dormant outputs.
Both modes must be finite and exactly zero or one. If either mode is one,
equipment_enabled_in must be true; otherwise raise ValueError. Return the
validated cost_mode_in and energy_mode_in unchanged. False/zero/zero is the
generic dormant scenario. Manual completion supplies the explicit guards.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Implementation review control-domain correction; Basis: scenario validity.

Inputs:
    - equipment_enabled_in: equipment_enabled_in parameter
    - energy_mode_in: energy_mode_in parameter
    - cost_mode_in: cost_mode_in parameter

Outputs:
    - energy_mode: energy_mode result
    - cost_mode: cost_mode result

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:4

    SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:4

    Calculation Specification:
        See documentation:
Validate supported scenario choices before using zero dormant outputs.
Both modes must be finite and exactly zero or one. If either mode is one,
equipment_enabled_in must be true; otherwise raise ValueError. Return the
validated cost_mode_in and energy_mode_in unchanged. False/zero/zero is the
generic dormant scenario. Manual completion supplies the explicit guards.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Implementation review control-domain correction; Basis: scenario validity.

    IMPLEMENTATION: See stellarator_materials_reference_tea.handwritten.mfe_cooling_accounts.cooling_scenario_guard_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts energy_mode, cost_mode fields to separate channels.
    """

    name: str = "Cooling_Scenario_GuardModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, equipment_enabled_in: bool, energy_mode_in: float, cost_mode_in: float    ) -> Cooling_Scenario_GuardInput:
        """Validate inputs and fill defaults.

        Args:
            equipment_enabled_in: equipment_enabled_in input
            energy_mode_in: energy_mode_in input
            cost_mode_in: cost_mode_in input

        Returns:
            Validated input model
        """
        return Cooling_Scenario_GuardInput(equipment_enabled_in=equipment_enabled_in, energy_mode_in=energy_mode_in, cost_mode_in=cost_mode_in)

    def run(
        self, equipment_enabled_in: bool, energy_mode_in: float, cost_mode_in: float    ) -> ModuleResult[Cooling_Scenario_GuardOutput]:
        """Execute calculation.

        Args:
            equipment_enabled_in: equipment_enabled_in input
            energy_mode_in: energy_mode_in input
            cost_mode_in: cost_mode_in input

        Returns:
            Module result with Cooling_Scenario_GuardOutput (energy_mode, cost_mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(equipment_enabled_in, energy_mode_in, cost_mode_in)

        # Import handwritten implementation
        from stellarator_materials_reference_tea.handwritten.mfe_cooling_accounts.cooling_scenario_guard_impl import (
            run_cooling_scenario_guard,
        )

        # Execute implementation - returns tuple of values
        energy_mode, cost_mode = run_cooling_scenario_guard(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Cooling_Scenario_GuardOutput(
                energy_mode=energy_mode,
                cost_mode=cost_mode,
            )
        )
