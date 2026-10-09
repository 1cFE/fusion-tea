"""Cooling_Account_SelectionModule Module Wrapper

TEAx module for Cooling_Account_Selection calculation.

Select independently sized cooling accounts or the retained legacy
allowance. Cost mode and secondary energy mode are binary scenario inputs
(0 or 1), not continuous blending controls. Each energy selector applies
to both electricity and recovered shaft heat. Primary IHX duty remains
upstream of secondary work, avoiding a feedback edge. New equipment
amounts are plant-total for the supported single-module scenario.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Account boundaries; Intermediate equipment and energy; Corrective review details
Basis: explicit accounting identities, independent of equipment price models.

Inputs:
    - legacy_cost_in: legacy_cost_in parameter
    - replacements_in: replacements_in parameter
    - consumables_in: consumables_in parameter
    - delivered_in: delivered_in parameter
    - cost_mode_in: cost_mode_in parameter
    - equipment_cost_in: equipment_cost_in parameter

Outputs:
    - cost: cost result
    - shipping_exclusion: shipping_exclusion result
    - consumables_annual: consumables_annual result
    - replacement_annual: replacement_annual result

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:19

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:19

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_cooling_accounts/cooling_account_selection_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_reference_tea.primitives import Float
from stellarator_materials_reference_tea.schemas.cooling_account_selection_output import Cooling_Account_SelectionOutput


class Cooling_Account_SelectionInput(BaseModel):
    """Input model for Cooling_Account_SelectionModule.

    Attributes:
        legacy_cost_in: legacy_cost_in input
        replacements_in: replacements_in input
        consumables_in: consumables_in input
        delivered_in: delivered_in input
        cost_mode_in: cost_mode_in input
        equipment_cost_in: equipment_cost_in input
    """
    legacy_cost_in: float = Field(..., description="legacy_cost_in input")
    replacements_in: float = Field(..., description="replacements_in input")
    consumables_in: float = Field(..., description="consumables_in input")
    delivered_in: float = Field(..., description="delivered_in input")
    cost_mode_in: float = Field(..., description="cost_mode_in input")
    equipment_cost_in: float = Field(..., description="equipment_cost_in input")


class Cooling_Account_SelectionModule(ModuleBase[Cooling_Account_SelectionInput, Cooling_Account_SelectionOutput]):
    """TEAx module for Cooling_Account_Selection calculation.

Select independently sized cooling accounts or the retained legacy
allowance. Cost mode and secondary energy mode are binary scenario inputs
(0 or 1), not continuous blending controls. Each energy selector applies
to both electricity and recovered shaft heat. Primary IHX duty remains
upstream of secondary work, avoiding a feedback edge. New equipment
amounts are plant-total for the supported single-module scenario.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Account boundaries; Intermediate equipment and energy; Corrective review details
Basis: explicit accounting identities, independent of equipment price models.

Inputs:
    - legacy_cost_in: legacy_cost_in parameter
    - replacements_in: replacements_in parameter
    - consumables_in: consumables_in parameter
    - delivered_in: delivered_in parameter
    - cost_mode_in: cost_mode_in parameter
    - equipment_cost_in: equipment_cost_in parameter

Outputs:
    - cost: cost result
    - shipping_exclusion: shipping_exclusion result
    - consumables_annual: consumables_annual result
    - replacement_annual: replacement_annual result

SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:19

    SysML Source: root-0/analyses/mfe_cooling_accounts.sysml:19

    Calculation Specification:
        cost = (1.0 - cost_mode_in) * legacy_cost_in + cost_mode_in * equipment_cost_in
        shipping_exclusion = cost_mode_in * delivered_in
        replacement_annual = cost_mode_in * replacements_in
        consumables_annual = cost_mode_in * consumables_in
        
Documentation:
Select independently sized cooling accounts or the retained legacy
allowance. Cost mode and secondary energy mode are binary scenario inputs
(0 or 1), not continuous blending controls. Each energy selector applies
to both electricity and recovered shaft heat. Primary IHX duty remains
upstream of secondary work, avoiding a feedback edge. New equipment
amounts are plant-total for the supported single-module scenario.
Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
Ref: Account boundaries; Intermediate equipment and energy; Corrective review details
Basis: explicit accounting identities, independent of equipment price models.

    IMPLEMENTATION: See stellarator_materials_reference_tea.handwritten.mfe_cooling_accounts.cooling_account_selection_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts cost, shipping_exclusion, consumables_annual, replacement_annual fields to separate channels.
    """

    name: str = "Cooling_Account_SelectionModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, legacy_cost_in: float, replacements_in: float, consumables_in: float, delivered_in: float, cost_mode_in: float, equipment_cost_in: float    ) -> Cooling_Account_SelectionInput:
        """Validate inputs and fill defaults.

        Args:
            legacy_cost_in: legacy_cost_in input
            replacements_in: replacements_in input
            consumables_in: consumables_in input
            delivered_in: delivered_in input
            cost_mode_in: cost_mode_in input
            equipment_cost_in: equipment_cost_in input

        Returns:
            Validated input model
        """
        return Cooling_Account_SelectionInput(legacy_cost_in=legacy_cost_in, replacements_in=replacements_in, consumables_in=consumables_in, delivered_in=delivered_in, cost_mode_in=cost_mode_in, equipment_cost_in=equipment_cost_in)

    def run(
        self, legacy_cost_in: float, replacements_in: float, consumables_in: float, delivered_in: float, cost_mode_in: float, equipment_cost_in: float    ) -> ModuleResult[Cooling_Account_SelectionOutput]:
        """Execute calculation.

        Args:
            legacy_cost_in: legacy_cost_in input
            replacements_in: replacements_in input
            consumables_in: consumables_in input
            delivered_in: delivered_in input
            cost_mode_in: cost_mode_in input
            equipment_cost_in: equipment_cost_in input

        Returns:
            Module result with Cooling_Account_SelectionOutput (cost, shipping_exclusion, consumables_annual, replacement_annual)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(legacy_cost_in, replacements_in, consumables_in, delivered_in, cost_mode_in, equipment_cost_in)

        # Import handwritten implementation
        from stellarator_materials_reference_tea.handwritten.mfe_cooling_accounts.cooling_account_selection_impl import (
            run_cooling_account_selection,
        )

        # Execute implementation - returns tuple of values
        cost, shipping_exclusion, consumables_annual, replacement_annual = run_cooling_account_selection(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Cooling_Account_SelectionOutput(
                cost=cost,
                shipping_exclusion=shipping_exclusion,
                consumables_annual=consumables_annual,
                replacement_annual=replacement_annual,
            )
        )
