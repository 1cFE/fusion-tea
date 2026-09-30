"""Facility_Ventilation_CostModule Module Wrapper

TEAx module for Facility_Ventilation_Cost calculation.

Source: work/active/WI-068_layout-based-facilities/design.md; layout-capacity-design.md; evidence/facility-contract.md. Ref: released geometry, capacity, exact civil takeoff and account boundary. Basis: conditional conceptual scenario; unqualified shielding/loading/transport and explicit provisional equipment envelopes. Historical PROCESS1990 empirical nuclear-ventilation relation; does not qualify airflow.

Inputs:
    - coefficient_in: coefficient_in parameter
    - cpi_ratio_in: cpi_ratio_in parameter
    - served_volume_in: served_volume_in parameter
    - exponent_in: exponent_in parameter

Outputs:
    - cost_2025: cost_2025 result
    - cost_1990: cost_1990 result

SysML Source: root-0/analyses/mfe_facilities.sysml:702

SysML Source: root-0/analyses/mfe_facilities.sysml:702

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_facilities/facility_ventilation_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.primitives import Float
from stellarator_materials_rebco_tea.schemas.facility_ventilation_cost_output import Facility_Ventilation_CostOutput


class Facility_Ventilation_CostInput(BaseModel):
    """Input model for Facility_Ventilation_CostModule.

    Attributes:
        coefficient_in: coefficient_in input
        cpi_ratio_in: cpi_ratio_in input
        served_volume_in: served_volume_in input
        exponent_in: exponent_in input
    """
    coefficient_in: float = Field(..., description="coefficient_in input")
    cpi_ratio_in: float = Field(..., description="cpi_ratio_in input")
    served_volume_in: float = Field(..., description="served_volume_in input")
    exponent_in: float = Field(..., description="exponent_in input")


class Facility_Ventilation_CostModule(ModuleBase[Facility_Ventilation_CostInput, Facility_Ventilation_CostOutput]):
    """TEAx module for Facility_Ventilation_Cost calculation.

Source: work/active/WI-068_layout-based-facilities/design.md; layout-capacity-design.md; evidence/facility-contract.md. Ref: released geometry, capacity, exact civil takeoff and account boundary. Basis: conditional conceptual scenario; unqualified shielding/loading/transport and explicit provisional equipment envelopes. Historical PROCESS1990 empirical nuclear-ventilation relation; does not qualify airflow.

Inputs:
    - coefficient_in: coefficient_in parameter
    - cpi_ratio_in: cpi_ratio_in parameter
    - served_volume_in: served_volume_in parameter
    - exponent_in: exponent_in parameter

Outputs:
    - cost_2025: cost_2025 result
    - cost_1990: cost_1990 result

SysML Source: root-0/analyses/mfe_facilities.sysml:702

    SysML Source: root-0/analyses/mfe_facilities.sysml:702

    Calculation Specification:
        cost_1990 = coefficient_in * served_volume_in ** exponent_in
        cost_2025 = cost_1990 * cpi_ratio_in
        
Documentation:
Source: work/active/WI-068_layout-based-facilities/design.md; layout-capacity-design.md; evidence/facility-contract.md. Ref: released geometry, capacity, exact civil takeoff and account boundary. Basis: conditional conceptual scenario; unqualified shielding/loading/transport and explicit provisional equipment envelopes. Historical PROCESS1990 empirical nuclear-ventilation relation; does not qualify airflow.

    IMPLEMENTATION: See stellarator_materials_rebco_tea.handwritten.mfe_facilities.facility_ventilation_cost_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts cost_2025, cost_1990 fields to separate channels.
    """

    name: str = "Facility_Ventilation_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, coefficient_in: float, cpi_ratio_in: float, served_volume_in: float, exponent_in: float    ) -> Facility_Ventilation_CostInput:
        """Validate inputs and fill defaults.

        Args:
            coefficient_in: coefficient_in input
            cpi_ratio_in: cpi_ratio_in input
            served_volume_in: served_volume_in input
            exponent_in: exponent_in input

        Returns:
            Validated input model
        """
        return Facility_Ventilation_CostInput(coefficient_in=coefficient_in, cpi_ratio_in=cpi_ratio_in, served_volume_in=served_volume_in, exponent_in=exponent_in)

    def run(
        self, coefficient_in: float, cpi_ratio_in: float, served_volume_in: float, exponent_in: float    ) -> ModuleResult[Facility_Ventilation_CostOutput]:
        """Execute calculation.

        Args:
            coefficient_in: coefficient_in input
            cpi_ratio_in: cpi_ratio_in input
            served_volume_in: served_volume_in input
            exponent_in: exponent_in input

        Returns:
            Module result with Facility_Ventilation_CostOutput (cost_2025, cost_1990)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(coefficient_in, cpi_ratio_in, served_volume_in, exponent_in)

        # Import handwritten implementation
        from stellarator_materials_rebco_tea.handwritten.mfe_facilities.facility_ventilation_cost_impl import (
            run_facility_ventilation_cost,
        )

        # Execute implementation - returns tuple of values
        cost_2025, cost_1990 = run_facility_ventilation_cost(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Facility_Ventilation_CostOutput(
                cost_2025=cost_2025,
                cost_1990=cost_1990,
            )
        )
