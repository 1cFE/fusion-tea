"""Facility_Civil_CostModule Module Wrapper

TEAx module for Facility_Civil_Cost calculation.

Source: work/active/WI-068_layout-based-facilities/design.md; layout-capacity-design.md; evidence/facility-contract.md. Ref: released geometry, capacity, exact civil takeoff and account boundary. Basis: conditional conceptual scenario; unqualified shielding/loading/transport and explicit provisional equipment envelopes. Six installed-direct commodity products, original2018 and CPI-normalized2025 purchasing power. Disabled returns zero; no repeated installation.

Inputs:
    - sub_formwork_rate_in: sub_formwork_rate_in parameter
    - civil_rate_multiplier_in: civil_rate_multiplier_in parameter
    - super_rebar_rate_in: super_rebar_rate_in parameter
    - sub_formwork_in: sub_formwork_in parameter
    - super_rebar_in: super_rebar_in parameter
    - super_concrete_rate_in: super_concrete_rate_in parameter
    - super_concrete_in: super_concrete_in parameter
    - super_formwork_rate_in: super_formwork_rate_in parameter
    - sub_concrete_rate_in: sub_concrete_rate_in parameter
    - super_formwork_in: super_formwork_in parameter
    - enabled_in: enabled_in parameter
    - sub_rebar_rate_in: sub_rebar_rate_in parameter
    - sub_concrete_in: sub_concrete_in parameter
    - civil_cpi_ratio_in: civil_cpi_ratio_in parameter
    - tonne_interpretation_kg_in: tonne_interpretation_kg_in parameter
    - sub_rebar_in: sub_rebar_in parameter

Outputs:
    - sub_cost_2018: sub_cost_2018 result
    - super_cost_2018: super_cost_2018 result
    - cost_2025: cost_2025 result
    - cost_2018: cost_2018 result

SysML Source: root-0/analyses/mfe_facilities.sysml:667

SysML Source: root-0/analyses/mfe_facilities.sysml:667

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_facilities/facility_civil_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.primitives import Float
from stellarator_materials_rebco_tea.schemas.facility_civil_cost_output import Facility_Civil_CostOutput


class Facility_Civil_CostInput(BaseModel):
    """Input model for Facility_Civil_CostModule.

    Attributes:
        sub_formwork_rate_in: sub_formwork_rate_in input
        civil_rate_multiplier_in: civil_rate_multiplier_in input
        super_rebar_rate_in: super_rebar_rate_in input
        sub_formwork_in: sub_formwork_in input
        super_rebar_in: super_rebar_in input
        super_concrete_rate_in: super_concrete_rate_in input
        super_concrete_in: super_concrete_in input
        super_formwork_rate_in: super_formwork_rate_in input
        sub_concrete_rate_in: sub_concrete_rate_in input
        super_formwork_in: super_formwork_in input
        enabled_in: enabled_in input
        sub_rebar_rate_in: sub_rebar_rate_in input
        sub_concrete_in: sub_concrete_in input
        civil_cpi_ratio_in: civil_cpi_ratio_in input
        tonne_interpretation_kg_in: tonne_interpretation_kg_in input
        sub_rebar_in: sub_rebar_in input
    """
    sub_formwork_rate_in: float = Field(..., description="sub_formwork_rate_in input")
    civil_rate_multiplier_in: float = Field(..., description="civil_rate_multiplier_in input")
    super_rebar_rate_in: float = Field(..., description="super_rebar_rate_in input")
    sub_formwork_in: float = Field(..., description="sub_formwork_in input")
    super_rebar_in: float = Field(..., description="super_rebar_in input")
    super_concrete_rate_in: float = Field(..., description="super_concrete_rate_in input")
    super_concrete_in: float = Field(..., description="super_concrete_in input")
    super_formwork_rate_in: float = Field(..., description="super_formwork_rate_in input")
    sub_concrete_rate_in: float = Field(..., description="sub_concrete_rate_in input")
    super_formwork_in: float = Field(..., description="super_formwork_in input")
    enabled_in: bool = Field(..., description="enabled_in input")
    sub_rebar_rate_in: float = Field(..., description="sub_rebar_rate_in input")
    sub_concrete_in: float = Field(..., description="sub_concrete_in input")
    civil_cpi_ratio_in: float = Field(..., description="civil_cpi_ratio_in input")
    tonne_interpretation_kg_in: float = Field(..., description="tonne_interpretation_kg_in input")
    sub_rebar_in: float = Field(..., description="sub_rebar_in input")


class Facility_Civil_CostModule(ModuleBase[Facility_Civil_CostInput, Facility_Civil_CostOutput]):
    """TEAx module for Facility_Civil_Cost calculation.

Source: work/active/WI-068_layout-based-facilities/design.md; layout-capacity-design.md; evidence/facility-contract.md. Ref: released geometry, capacity, exact civil takeoff and account boundary. Basis: conditional conceptual scenario; unqualified shielding/loading/transport and explicit provisional equipment envelopes. Six installed-direct commodity products, original2018 and CPI-normalized2025 purchasing power. Disabled returns zero; no repeated installation.

Inputs:
    - sub_formwork_rate_in: sub_formwork_rate_in parameter
    - civil_rate_multiplier_in: civil_rate_multiplier_in parameter
    - super_rebar_rate_in: super_rebar_rate_in parameter
    - sub_formwork_in: sub_formwork_in parameter
    - super_rebar_in: super_rebar_in parameter
    - super_concrete_rate_in: super_concrete_rate_in parameter
    - super_concrete_in: super_concrete_in parameter
    - super_formwork_rate_in: super_formwork_rate_in parameter
    - sub_concrete_rate_in: sub_concrete_rate_in parameter
    - super_formwork_in: super_formwork_in parameter
    - enabled_in: enabled_in parameter
    - sub_rebar_rate_in: sub_rebar_rate_in parameter
    - sub_concrete_in: sub_concrete_in parameter
    - civil_cpi_ratio_in: civil_cpi_ratio_in parameter
    - tonne_interpretation_kg_in: tonne_interpretation_kg_in parameter
    - sub_rebar_in: sub_rebar_in parameter

Outputs:
    - sub_cost_2018: sub_cost_2018 result
    - super_cost_2018: super_cost_2018 result
    - cost_2025: cost_2025 result
    - cost_2018: cost_2018 result

SysML Source: root-0/analyses/mfe_facilities.sysml:667

    SysML Source: root-0/analyses/mfe_facilities.sysml:667

    Calculation Specification:
        See documentation:
Source: work/active/WI-068_layout-based-facilities/design.md; layout-capacity-design.md; evidence/facility-contract.md. Ref: released geometry, capacity, exact civil takeoff and account boundary. Basis: conditional conceptual scenario; unqualified shielding/loading/transport and explicit provisional equipment envelopes. Six installed-direct commodity products, original2018 and CPI-normalized2025 purchasing power. Disabled returns zero; no repeated installation.

    IMPLEMENTATION: See stellarator_materials_rebco_tea.handwritten.mfe_facilities.facility_civil_cost_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts sub_cost_2018, super_cost_2018, cost_2025, cost_2018 fields to separate channels.
    """

    name: str = "Facility_Civil_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, sub_formwork_rate_in: float, civil_rate_multiplier_in: float, super_rebar_rate_in: float, sub_formwork_in: float, super_rebar_in: float, super_concrete_rate_in: float, super_concrete_in: float, super_formwork_rate_in: float, sub_concrete_rate_in: float, super_formwork_in: float, enabled_in: bool, sub_rebar_rate_in: float, sub_concrete_in: float, civil_cpi_ratio_in: float, tonne_interpretation_kg_in: float, sub_rebar_in: float    ) -> Facility_Civil_CostInput:
        """Validate inputs and fill defaults.

        Args:
            sub_formwork_rate_in: sub_formwork_rate_in input
            civil_rate_multiplier_in: civil_rate_multiplier_in input
            super_rebar_rate_in: super_rebar_rate_in input
            sub_formwork_in: sub_formwork_in input
            super_rebar_in: super_rebar_in input
            super_concrete_rate_in: super_concrete_rate_in input
            super_concrete_in: super_concrete_in input
            super_formwork_rate_in: super_formwork_rate_in input
            sub_concrete_rate_in: sub_concrete_rate_in input
            super_formwork_in: super_formwork_in input
            enabled_in: enabled_in input
            sub_rebar_rate_in: sub_rebar_rate_in input
            sub_concrete_in: sub_concrete_in input
            civil_cpi_ratio_in: civil_cpi_ratio_in input
            tonne_interpretation_kg_in: tonne_interpretation_kg_in input
            sub_rebar_in: sub_rebar_in input

        Returns:
            Validated input model
        """
        return Facility_Civil_CostInput(sub_formwork_rate_in=sub_formwork_rate_in, civil_rate_multiplier_in=civil_rate_multiplier_in, super_rebar_rate_in=super_rebar_rate_in, sub_formwork_in=sub_formwork_in, super_rebar_in=super_rebar_in, super_concrete_rate_in=super_concrete_rate_in, super_concrete_in=super_concrete_in, super_formwork_rate_in=super_formwork_rate_in, sub_concrete_rate_in=sub_concrete_rate_in, super_formwork_in=super_formwork_in, enabled_in=enabled_in, sub_rebar_rate_in=sub_rebar_rate_in, sub_concrete_in=sub_concrete_in, civil_cpi_ratio_in=civil_cpi_ratio_in, tonne_interpretation_kg_in=tonne_interpretation_kg_in, sub_rebar_in=sub_rebar_in)

    def run(
        self, sub_formwork_rate_in: float, civil_rate_multiplier_in: float, super_rebar_rate_in: float, sub_formwork_in: float, super_rebar_in: float, super_concrete_rate_in: float, super_concrete_in: float, super_formwork_rate_in: float, sub_concrete_rate_in: float, super_formwork_in: float, enabled_in: bool, sub_rebar_rate_in: float, sub_concrete_in: float, civil_cpi_ratio_in: float, tonne_interpretation_kg_in: float, sub_rebar_in: float    ) -> ModuleResult[Facility_Civil_CostOutput]:
        """Execute calculation.

        Args:
            sub_formwork_rate_in: sub_formwork_rate_in input
            civil_rate_multiplier_in: civil_rate_multiplier_in input
            super_rebar_rate_in: super_rebar_rate_in input
            sub_formwork_in: sub_formwork_in input
            super_rebar_in: super_rebar_in input
            super_concrete_rate_in: super_concrete_rate_in input
            super_concrete_in: super_concrete_in input
            super_formwork_rate_in: super_formwork_rate_in input
            sub_concrete_rate_in: sub_concrete_rate_in input
            super_formwork_in: super_formwork_in input
            enabled_in: enabled_in input
            sub_rebar_rate_in: sub_rebar_rate_in input
            sub_concrete_in: sub_concrete_in input
            civil_cpi_ratio_in: civil_cpi_ratio_in input
            tonne_interpretation_kg_in: tonne_interpretation_kg_in input
            sub_rebar_in: sub_rebar_in input

        Returns:
            Module result with Facility_Civil_CostOutput (sub_cost_2018, super_cost_2018, cost_2025, cost_2018)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(sub_formwork_rate_in, civil_rate_multiplier_in, super_rebar_rate_in, sub_formwork_in, super_rebar_in, super_concrete_rate_in, super_concrete_in, super_formwork_rate_in, sub_concrete_rate_in, super_formwork_in, enabled_in, sub_rebar_rate_in, sub_concrete_in, civil_cpi_ratio_in, tonne_interpretation_kg_in, sub_rebar_in)

        # Import handwritten implementation
        from stellarator_materials_rebco_tea.handwritten.mfe_facilities.facility_civil_cost_impl import (
            run_facility_civil_cost,
        )

        # Execute implementation - returns tuple of values
        sub_cost_2018, super_cost_2018, cost_2025, cost_2018 = run_facility_civil_cost(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Facility_Civil_CostOutput(
                sub_cost_2018=sub_cost_2018,
                super_cost_2018=super_cost_2018,
                cost_2025=cost_2025,
                cost_2018=cost_2018,
            )
        )
