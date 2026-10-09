"""Cycle_Mode_SelectionModule Module Wrapper

TEAx module for Cycle_Mode_Selection calculation.

*Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Numerical semantic: the normative handwritten implementation executes the exact state/work equations in the cited design. Disabled modes branch before property access; no extrapolation. Units are given by the scalar names and interface inventory.

Inputs:
    - legacy_domain_product_in: legacy_domain_product_in parameter
    - legacy_eta_in: legacy_eta_in parameter
    - matched_eta_in: matched_eta_in parameter
    - matched_enabled_in: matched_enabled_in parameter

Outputs:
    - matched_domain_applicable: matched_domain_applicable result
    - legacy_domain_applicable: legacy_domain_applicable result
    - eta_selected: eta_selected result

SysML Source: root-0/analyses/mfe_matched_steam_cycle.sysml:130

SysML Source: root-0/analyses/mfe_matched_steam_cycle.sysml:130

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_matched_steam_cycle/cycle_mode_selection_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.primitives import Float
from stellarator_materials_rebco_tea.schemas.cycle_mode_selection_output import Cycle_Mode_SelectionOutput


class Cycle_Mode_SelectionInput(BaseModel):
    """Input model for Cycle_Mode_SelectionModule.

    Attributes:
        legacy_domain_product_in: legacy_domain_product_in input
        legacy_eta_in: legacy_eta_in input
        matched_eta_in: matched_eta_in input
        matched_enabled_in: matched_enabled_in input
    """
    legacy_domain_product_in: float = Field(..., description="legacy_domain_product_in input")
    legacy_eta_in: float = Field(..., description="legacy_eta_in input")
    matched_eta_in: float = Field(..., description="matched_eta_in input")
    matched_enabled_in: float = Field(..., description="matched_enabled_in input")


class Cycle_Mode_SelectionModule(ModuleBase[Cycle_Mode_SelectionInput, Cycle_Mode_SelectionOutput]):
    """TEAx module for Cycle_Mode_Selection calculation.

*Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Numerical semantic: the normative handwritten implementation executes the exact state/work equations in the cited design. Disabled modes branch before property access; no extrapolation. Units are given by the scalar names and interface inventory.

Inputs:
    - legacy_domain_product_in: legacy_domain_product_in parameter
    - legacy_eta_in: legacy_eta_in parameter
    - matched_eta_in: matched_eta_in parameter
    - matched_enabled_in: matched_enabled_in parameter

Outputs:
    - matched_domain_applicable: matched_domain_applicable result
    - legacy_domain_applicable: legacy_domain_applicable result
    - eta_selected: eta_selected result

SysML Source: root-0/analyses/mfe_matched_steam_cycle.sysml:130

    SysML Source: root-0/analyses/mfe_matched_steam_cycle.sysml:130

    Calculation Specification:
        See documentation:
*Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Numerical semantic: the normative handwritten implementation executes the exact state/work equations in the cited design. Disabled modes branch before property access; no extrapolation. Units are given by the scalar names and interface inventory.

    IMPLEMENTATION: See stellarator_materials_rebco_tea.handwritten.mfe_matched_steam_cycle.cycle_mode_selection_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts matched_domain_applicable, legacy_domain_applicable, eta_selected fields to separate channels.
    """

    name: str = "Cycle_Mode_SelectionModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, legacy_domain_product_in: float, legacy_eta_in: float, matched_eta_in: float, matched_enabled_in: float    ) -> Cycle_Mode_SelectionInput:
        """Validate inputs and fill defaults.

        Args:
            legacy_domain_product_in: legacy_domain_product_in input
            legacy_eta_in: legacy_eta_in input
            matched_eta_in: matched_eta_in input
            matched_enabled_in: matched_enabled_in input

        Returns:
            Validated input model
        """
        return Cycle_Mode_SelectionInput(legacy_domain_product_in=legacy_domain_product_in, legacy_eta_in=legacy_eta_in, matched_eta_in=matched_eta_in, matched_enabled_in=matched_enabled_in)

    def run(
        self, legacy_domain_product_in: float, legacy_eta_in: float, matched_eta_in: float, matched_enabled_in: float    ) -> ModuleResult[Cycle_Mode_SelectionOutput]:
        """Execute calculation.

        Args:
            legacy_domain_product_in: legacy_domain_product_in input
            legacy_eta_in: legacy_eta_in input
            matched_eta_in: matched_eta_in input
            matched_enabled_in: matched_enabled_in input

        Returns:
            Module result with Cycle_Mode_SelectionOutput (matched_domain_applicable, legacy_domain_applicable, eta_selected)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(legacy_domain_product_in, legacy_eta_in, matched_eta_in, matched_enabled_in)

        # Import handwritten implementation
        from stellarator_materials_rebco_tea.handwritten.mfe_matched_steam_cycle.cycle_mode_selection_impl import (
            run_cycle_mode_selection,
        )

        # Execute implementation - returns tuple of values
        matched_domain_applicable, legacy_domain_applicable, eta_selected = run_cycle_mode_selection(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Cycle_Mode_SelectionOutput(
                matched_domain_applicable=matched_domain_applicable,
                legacy_domain_applicable=legacy_domain_applicable,
                eta_selected=eta_selected,
            )
        )
