"""Facility_Preconstruction_SelectionModule Module Wrapper

TEAx module for Facility_Preconstruction_Selection calculation.

*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Replace only land; keep the fixed preconstruction adders and legacy mode.

Inputs:
    - fixed_in: fixed_in parameter
    - legacy_in: legacy_in parameter
    - mode_in: mode_in parameter
    - land_in: land_in parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_facilities.sysml:769

SysML Source: root-0/analyses/mfe_facilities.sysml:769

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_facilities/facility_preconstruction_selection_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float


class Facility_Preconstruction_SelectionInput(BaseModel):
    """Input model for Facility_Preconstruction_SelectionModule.

    Attributes:
        fixed_in: fixed_in input
        legacy_in: legacy_in input
        mode_in: mode_in input
        land_in: land_in input
    """
    fixed_in: float = Field(..., description="fixed_in input")
    legacy_in: float = Field(..., description="legacy_in input")
    mode_in: float = Field(..., description="mode_in input")
    land_in: float = Field(..., description="land_in input")


class Facility_Preconstruction_SelectionModule(ModuleBase[Facility_Preconstruction_SelectionInput, Float]):
    """TEAx module for Facility_Preconstruction_Selection calculation.

*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Replace only land; keep the fixed preconstruction adders and legacy mode.

Inputs:
    - fixed_in: fixed_in parameter
    - legacy_in: legacy_in parameter
    - mode_in: mode_in parameter
    - land_in: land_in parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_facilities.sysml:769

    SysML Source: root-0/analyses/mfe_facilities.sysml:769

    Calculation Specification:
        cost = (1.0 - mode_in) * legacy_in + mode_in * (fixed_in + land_in)
        
Documentation:
*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Replace only land; keep the fixed preconstruction adders and legacy mode.

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.mfe_facilities.facility_preconstruction_selection_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Facility_Preconstruction_SelectionModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, fixed_in: float, legacy_in: float, mode_in: float, land_in: float    ) -> Facility_Preconstruction_SelectionInput:
        """Validate inputs and fill defaults.

        Args:
            fixed_in: fixed_in input
            legacy_in: legacy_in input
            mode_in: mode_in input
            land_in: land_in input

        Returns:
            Validated input model
        """
        return Facility_Preconstruction_SelectionInput(fixed_in=fixed_in, legacy_in=legacy_in, mode_in=mode_in, land_in=land_in)

    def run(
        self, fixed_in: float, legacy_in: float, mode_in: float, land_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            fixed_in: fixed_in input
            legacy_in: legacy_in input
            mode_in: mode_in input
            land_in: land_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(fixed_in, legacy_in, mode_in, land_in)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.mfe_facilities.facility_preconstruction_selection_impl import (
            run_facility_preconstruction_selection,
        )

        # Execute implementation - returns single value
        cost = run_facility_preconstruction_selection(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
