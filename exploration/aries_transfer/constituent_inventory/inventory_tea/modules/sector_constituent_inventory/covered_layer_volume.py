"""Covered_Layer_VolumeModule Module Wrapper

TEAx module for Covered_Layer_Volume calculation.

volume = area_basis_in * coverage_in * thickness_in. Units m2, dimensionless and m yield m3. Inputs finite nonnegative; coverage in [0,1]. Reject nonfinite outputs. Guarded typed completion implements these equations through the native route. Source: work/active/WI-084_aries-sector-constituent-inventory/spec.md. Reference: geometry/material identities and three-child aggregation contract. Last Updated: 2026-09-21.

Inputs:
    - area_basis_in: area_basis_in parameter
    - thickness_in: thickness_in parameter
    - coverage_in: coverage_in parameter

Outputs:
    - volume: volume result

SysML Source: root-0/sector_constituent_inventory.sysml:3

SysML Source: root-0/sector_constituent_inventory.sysml:3

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/sector_constituent_inventory/covered_layer_volume_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from inventory_tea.primitives import Float


class Covered_Layer_VolumeInput(BaseModel):
    """Input model for Covered_Layer_VolumeModule.

    Attributes:
        area_basis_in: area_basis_in input
        thickness_in: thickness_in input
        coverage_in: coverage_in input
    """
    area_basis_in: float = Field(..., description="area_basis_in input")
    thickness_in: float = Field(..., description="thickness_in input")
    coverage_in: float = Field(..., description="coverage_in input")


class Covered_Layer_VolumeModule(ModuleBase[Covered_Layer_VolumeInput, Float]):
    """TEAx module for Covered_Layer_Volume calculation.

volume = area_basis_in * coverage_in * thickness_in. Units m2, dimensionless and m yield m3. Inputs finite nonnegative; coverage in [0,1]. Reject nonfinite outputs. Guarded typed completion implements these equations through the native route. Source: work/active/WI-084_aries-sector-constituent-inventory/spec.md. Reference: geometry/material identities and three-child aggregation contract. Last Updated: 2026-09-21.

Inputs:
    - area_basis_in: area_basis_in parameter
    - thickness_in: thickness_in parameter
    - coverage_in: coverage_in parameter

Outputs:
    - volume: volume result

SysML Source: root-0/sector_constituent_inventory.sysml:3

    SysML Source: root-0/sector_constituent_inventory.sysml:3

    Calculation Specification:
        See documentation:
volume = area_basis_in * coverage_in * thickness_in. Units m2, dimensionless and m yield m3. Inputs finite nonnegative; coverage in [0,1]. Reject nonfinite outputs. Guarded typed completion implements these equations through the native route. Source: work/active/WI-084_aries-sector-constituent-inventory/spec.md. Reference: geometry/material identities and three-child aggregation contract. Last Updated: 2026-09-21.

    IMPLEMENTATION: See inventory_tea.handwritten.sector_constituent_inventory.covered_layer_volume_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Covered_Layer_VolumeModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, area_basis_in: float, thickness_in: float, coverage_in: float    ) -> Covered_Layer_VolumeInput:
        """Validate inputs and fill defaults.

        Args:
            area_basis_in: area_basis_in input
            thickness_in: thickness_in input
            coverage_in: coverage_in input

        Returns:
            Validated input model
        """
        return Covered_Layer_VolumeInput(area_basis_in=area_basis_in, thickness_in=thickness_in, coverage_in=coverage_in)

    def run(
        self, area_basis_in: float, thickness_in: float, coverage_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            area_basis_in: area_basis_in input
            thickness_in: thickness_in input
            coverage_in: coverage_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(area_basis_in, thickness_in, coverage_in)

        # Import handwritten implementation
        from inventory_tea.handwritten.sector_constituent_inventory.covered_layer_volume_impl import (
            run_covered_layer_volume,
        )

        # Execute implementation - returns single value
        volume = run_covered_layer_volume(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(volume))
