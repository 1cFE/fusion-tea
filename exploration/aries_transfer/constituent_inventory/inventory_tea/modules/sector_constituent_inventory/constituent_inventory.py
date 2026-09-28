"""Constituent_InventoryModule Module Wrapper

TEAx module for Constituent_Inventory calculation.

constituent_volume = region_volume_in * fraction_in; known_mass = constituent_volume * density_in; source_price_subtotal = known_mass * unit_price_in. Units m3, kg/m3 and source-year dollars/kg yield kg and source-year dollars. Finite nonnegative inputs, fraction in [0,1], density strictly positive. Reject nonfinite outputs. A missing density or price is not zero; an unquantified constituent is represented outside this calculation. Guarded typed completion implements these equations through the native route. Source: work/active/WI-084_aries-sector-constituent-inventory/spec.md. Reference: geometry/material identities and three-child aggregation contract. Last Updated: 2026-09-21.

Inputs:
    - region_volume_in: region_volume_in parameter
    - density_in: density_in parameter
    - unit_price_in: unit_price_in parameter
    - fraction_in: fraction_in parameter

Outputs:
    - constituent_volume: constituent_volume result
    - known_mass: known_mass result
    - source_price_subtotal: source_price_subtotal result

SysML Source: root-0/sector_constituent_inventory.sysml:10

SysML Source: root-0/sector_constituent_inventory.sysml:10

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/sector_constituent_inventory/constituent_inventory_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from inventory_tea.primitives import Float
from inventory_tea.schemas.constituent_inventory_output import Constituent_InventoryOutput


class Constituent_InventoryInput(BaseModel):
    """Input model for Constituent_InventoryModule.

    Attributes:
        region_volume_in: region_volume_in input
        density_in: density_in input
        unit_price_in: unit_price_in input
        fraction_in: fraction_in input
    """
    region_volume_in: float = Field(..., description="region_volume_in input")
    density_in: float = Field(..., description="density_in input")
    unit_price_in: float = Field(..., description="unit_price_in input")
    fraction_in: float = Field(..., description="fraction_in input")


class Constituent_InventoryModule(ModuleBase[Constituent_InventoryInput, Constituent_InventoryOutput]):
    """TEAx module for Constituent_Inventory calculation.

constituent_volume = region_volume_in * fraction_in; known_mass = constituent_volume * density_in; source_price_subtotal = known_mass * unit_price_in. Units m3, kg/m3 and source-year dollars/kg yield kg and source-year dollars. Finite nonnegative inputs, fraction in [0,1], density strictly positive. Reject nonfinite outputs. A missing density or price is not zero; an unquantified constituent is represented outside this calculation. Guarded typed completion implements these equations through the native route. Source: work/active/WI-084_aries-sector-constituent-inventory/spec.md. Reference: geometry/material identities and three-child aggregation contract. Last Updated: 2026-09-21.

Inputs:
    - region_volume_in: region_volume_in parameter
    - density_in: density_in parameter
    - unit_price_in: unit_price_in parameter
    - fraction_in: fraction_in parameter

Outputs:
    - constituent_volume: constituent_volume result
    - known_mass: known_mass result
    - source_price_subtotal: source_price_subtotal result

SysML Source: root-0/sector_constituent_inventory.sysml:10

    SysML Source: root-0/sector_constituent_inventory.sysml:10

    Calculation Specification:
        See documentation:
constituent_volume = region_volume_in * fraction_in; known_mass = constituent_volume * density_in; source_price_subtotal = known_mass * unit_price_in. Units m3, kg/m3 and source-year dollars/kg yield kg and source-year dollars. Finite nonnegative inputs, fraction in [0,1], density strictly positive. Reject nonfinite outputs. A missing density or price is not zero; an unquantified constituent is represented outside this calculation. Guarded typed completion implements these equations through the native route. Source: work/active/WI-084_aries-sector-constituent-inventory/spec.md. Reference: geometry/material identities and three-child aggregation contract. Last Updated: 2026-09-21.

    IMPLEMENTATION: See inventory_tea.handwritten.sector_constituent_inventory.constituent_inventory_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts constituent_volume, known_mass, source_price_subtotal fields to separate channels.
    """

    name: str = "Constituent_InventoryModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, region_volume_in: float, density_in: float, unit_price_in: float, fraction_in: float    ) -> Constituent_InventoryInput:
        """Validate inputs and fill defaults.

        Args:
            region_volume_in: region_volume_in input
            density_in: density_in input
            unit_price_in: unit_price_in input
            fraction_in: fraction_in input

        Returns:
            Validated input model
        """
        return Constituent_InventoryInput(region_volume_in=region_volume_in, density_in=density_in, unit_price_in=unit_price_in, fraction_in=fraction_in)

    def run(
        self, region_volume_in: float, density_in: float, unit_price_in: float, fraction_in: float    ) -> ModuleResult[Constituent_InventoryOutput]:
        """Execute calculation.

        Args:
            region_volume_in: region_volume_in input
            density_in: density_in input
            unit_price_in: unit_price_in input
            fraction_in: fraction_in input

        Returns:
            Module result with Constituent_InventoryOutput (constituent_volume, known_mass, source_price_subtotal)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(region_volume_in, density_in, unit_price_in, fraction_in)

        # Import handwritten implementation
        from inventory_tea.handwritten.sector_constituent_inventory.constituent_inventory_impl import (
            run_constituent_inventory,
        )

        # Execute implementation - returns tuple of values
        constituent_volume, known_mass, source_price_subtotal = run_constituent_inventory(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Constituent_InventoryOutput(
                constituent_volume=constituent_volume,
                known_mass=known_mass,
                source_price_subtotal=source_price_subtotal,
            )
        )
