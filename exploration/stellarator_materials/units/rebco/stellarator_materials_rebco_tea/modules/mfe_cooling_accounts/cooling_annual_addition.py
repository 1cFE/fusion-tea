"""Cooling_Annual_AdditionModule Module Wrapper

TEAx module for Cooling_Annual_Addition calculation.

Add new cooling annual expenses to their distinct existing owners.
Routine service labor remains in inherited O&M; cooling consumable make-up
enters before the existing annual-cost levelization. Dated cooling major
replacements are already annualized and enter CAS72 after that calculation.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Lifecycle; models/library/analyses/mfe_lifecycle.sysml (annualized replacement convention)
Basis: sum each annual expense once before its existing consumer.

Inputs:
    - existing_om_in: existing_om_in parameter
    - cooling_consumables_in: cooling_consumables_in parameter
    - existing_replacements_in: existing_replacements_in parameter
    - cooling_replacements_in: cooling_replacements_in parameter

Outputs:
    - cas72_total: cas72_total result
    - annual_om: annual_om result

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:57

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:57

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_cooling_accounts/cooling_annual_addition_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.primitives import Float
from stellarator_materials_rebco_tea.schemas.cooling_annual_addition_output import Cooling_Annual_AdditionOutput


class Cooling_Annual_AdditionInput(BaseModel):
    """Input model for Cooling_Annual_AdditionModule.

    Attributes:
        existing_om_in: existing_om_in input
        cooling_consumables_in: cooling_consumables_in input
        existing_replacements_in: existing_replacements_in input
        cooling_replacements_in: cooling_replacements_in input
    """
    existing_om_in: float = Field(..., description="existing_om_in input")
    cooling_consumables_in: float = Field(..., description="cooling_consumables_in input")
    existing_replacements_in: float = Field(..., description="existing_replacements_in input")
    cooling_replacements_in: float = Field(..., description="cooling_replacements_in input")


class Cooling_Annual_AdditionModule(ModuleBase[Cooling_Annual_AdditionInput, Cooling_Annual_AdditionOutput]):
    """TEAx module for Cooling_Annual_Addition calculation.

Add new cooling annual expenses to their distinct existing owners.
Routine service labor remains in inherited O&M; cooling consumable make-up
enters before the existing annual-cost levelization. Dated cooling major
replacements are already annualized and enter CAS72 after that calculation.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Lifecycle; models/library/analyses/mfe_lifecycle.sysml (annualized replacement convention)
Basis: sum each annual expense once before its existing consumer.

Inputs:
    - existing_om_in: existing_om_in parameter
    - cooling_consumables_in: cooling_consumables_in parameter
    - existing_replacements_in: existing_replacements_in parameter
    - cooling_replacements_in: cooling_replacements_in parameter

Outputs:
    - cas72_total: cas72_total result
    - annual_om: annual_om result

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:57

    SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:57

    Calculation Specification:
        annual_om = existing_om_in + cooling_consumables_in
        cas72_total = existing_replacements_in + cooling_replacements_in
        
Documentation:
Add new cooling annual expenses to their distinct existing owners.
Routine service labor remains in inherited O&M; cooling consumable make-up
enters before the existing annual-cost levelization. Dated cooling major
replacements are already annualized and enter CAS72 after that calculation.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Lifecycle; models/library/analyses/mfe_lifecycle.sysml (annualized replacement convention)
Basis: sum each annual expense once before its existing consumer.

    IMPLEMENTATION: See stellarator_materials_rebco_tea.handwritten.mfe_cooling_accounts.cooling_annual_addition_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts cas72_total, annual_om fields to separate channels.
    """

    name: str = "Cooling_Annual_AdditionModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, existing_om_in: float, cooling_consumables_in: float, existing_replacements_in: float, cooling_replacements_in: float    ) -> Cooling_Annual_AdditionInput:
        """Validate inputs and fill defaults.

        Args:
            existing_om_in: existing_om_in input
            cooling_consumables_in: cooling_consumables_in input
            existing_replacements_in: existing_replacements_in input
            cooling_replacements_in: cooling_replacements_in input

        Returns:
            Validated input model
        """
        return Cooling_Annual_AdditionInput(existing_om_in=existing_om_in, cooling_consumables_in=cooling_consumables_in, existing_replacements_in=existing_replacements_in, cooling_replacements_in=cooling_replacements_in)

    def run(
        self, existing_om_in: float, cooling_consumables_in: float, existing_replacements_in: float, cooling_replacements_in: float    ) -> ModuleResult[Cooling_Annual_AdditionOutput]:
        """Execute calculation.

        Args:
            existing_om_in: existing_om_in input
            cooling_consumables_in: cooling_consumables_in input
            existing_replacements_in: existing_replacements_in input
            cooling_replacements_in: cooling_replacements_in input

        Returns:
            Module result with Cooling_Annual_AdditionOutput (cas72_total, annual_om)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(existing_om_in, cooling_consumables_in, existing_replacements_in, cooling_replacements_in)

        # Import handwritten implementation
        from stellarator_materials_rebco_tea.handwritten.mfe_cooling_accounts.cooling_annual_addition_impl import (
            run_cooling_annual_addition,
        )

        # Execute implementation - returns tuple of values
        cas72_total, annual_om = run_cooling_annual_addition(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Cooling_Annual_AdditionOutput(
                cas72_total=cas72_total,
                annual_om=annual_om,
            )
        )
