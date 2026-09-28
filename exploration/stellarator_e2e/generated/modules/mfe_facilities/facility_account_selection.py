"""Facility_Account_SelectionModule Module Wrapper

TEAx module for Facility_Account_Selection calculation.

*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Select the complete priced facility account or the preserved grouped legacy account; layout validates the binary mode.

Inputs:
    - civil_in: civil_in parameter
    - mode_in: mode_in parameter
    - legacy_in: legacy_in parameter
    - ventilation_in: ventilation_in parameter
    - site_in: site_in parameter

Outputs:
    - layout_buildings_capital: layout_buildings_capital result
    - cost: cost result
    - installed_facility_capital: installed_facility_capital result

SysML Source: root-0/analyses/mfe_facilities.sysml:746

SysML Source: root-0/analyses/mfe_facilities.sysml:746

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_facilities/facility_account_selection_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float
from stellarator_tea.schemas.facility_account_selection_output import Facility_Account_SelectionOutput


class Facility_Account_SelectionInput(BaseModel):
    """Input model for Facility_Account_SelectionModule.

    Attributes:
        civil_in: civil_in input
        mode_in: mode_in input
        legacy_in: legacy_in input
        ventilation_in: ventilation_in input
        site_in: site_in input
    """
    civil_in: float = Field(..., description="civil_in input")
    mode_in: float = Field(..., description="mode_in input")
    legacy_in: float = Field(..., description="legacy_in input")
    ventilation_in: float = Field(..., description="ventilation_in input")
    site_in: float = Field(..., description="site_in input")


class Facility_Account_SelectionModule(ModuleBase[Facility_Account_SelectionInput, Facility_Account_SelectionOutput]):
    """TEAx module for Facility_Account_Selection calculation.

*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Select the complete priced facility account or the preserved grouped legacy account; layout validates the binary mode.

Inputs:
    - civil_in: civil_in parameter
    - mode_in: mode_in parameter
    - legacy_in: legacy_in parameter
    - ventilation_in: ventilation_in parameter
    - site_in: site_in parameter

Outputs:
    - layout_buildings_capital: layout_buildings_capital result
    - cost: cost result
    - installed_facility_capital: installed_facility_capital result

SysML Source: root-0/analyses/mfe_facilities.sysml:746

    SysML Source: root-0/analyses/mfe_facilities.sysml:746

    Calculation Specification:
        installed_facility_capital = civil_in + ventilation_in
        layout_buildings_capital = installed_facility_capital + site_in
        cost = (1.0 - mode_in) * legacy_in + mode_in * layout_buildings_capital
        
Documentation:
*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Select the complete priced facility account or the preserved grouped legacy account; layout validates the binary mode.

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_facilities.facility_account_selection_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts layout_buildings_capital, cost, installed_facility_capital fields to separate channels.
    """

    name: str = "Facility_Account_SelectionModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, civil_in: float, mode_in: float, legacy_in: float, ventilation_in: float, site_in: float    ) -> Facility_Account_SelectionInput:
        """Validate inputs and fill defaults.

        Args:
            civil_in: civil_in input
            mode_in: mode_in input
            legacy_in: legacy_in input
            ventilation_in: ventilation_in input
            site_in: site_in input

        Returns:
            Validated input model
        """
        return Facility_Account_SelectionInput(civil_in=civil_in, mode_in=mode_in, legacy_in=legacy_in, ventilation_in=ventilation_in, site_in=site_in)

    def run(
        self, civil_in: float, mode_in: float, legacy_in: float, ventilation_in: float, site_in: float    ) -> ModuleResult[Facility_Account_SelectionOutput]:
        """Execute calculation.

        Args:
            civil_in: civil_in input
            mode_in: mode_in input
            legacy_in: legacy_in input
            ventilation_in: ventilation_in input
            site_in: site_in input

        Returns:
            Module result with Facility_Account_SelectionOutput (layout_buildings_capital, cost, installed_facility_capital)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(civil_in, mode_in, legacy_in, ventilation_in, site_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_facilities.facility_account_selection_impl import (
            run_facility_account_selection,
        )

        # Execute implementation - returns tuple of values
        layout_buildings_capital, cost, installed_facility_capital = run_facility_account_selection(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Facility_Account_SelectionOutput(
                layout_buildings_capital=layout_buildings_capital,
                cost=cost,
                installed_facility_capital=installed_facility_capital,
            )
        )
