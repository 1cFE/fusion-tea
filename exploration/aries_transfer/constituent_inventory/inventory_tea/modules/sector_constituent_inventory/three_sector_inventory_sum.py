"""Three_Sector_Inventory_SumModule Module Wrapper

TEAx module for Three_Sector_Inventory_Sum calculation.

The three supplied lateral coverages must each lie in [0,1] and sum to one within 1e-12, including zero-volume cases. Refuse inconsistent supplied partitions; never normalize them. This establishes arithmetic partition closure, not geometric nonoverlap qualification.

volume = volume_1_in + volume_2_in + volume_3_in; known_mass = mass_1_in + mass_2_in + mass_3_in; source_price_subtotal = price_1_in + price_2_in + price_3_in; unquantified_volume = unquantified_volume_1_in + unquantified_volume_2_in + unquantified_volume_3_in. Inputs and outputs finite nonnegative. Units m3, kg and same-source-year dollars; no currency conversion. Sums three nonoverlapping lateral layer occurrences, not arbitrary stacked area fractions. Partial source-price sum is not installed capital. Guarded typed completion implements these equations through the native route. Source: work/active/WI-084_aries-sector-constituent-inventory/spec.md. Reference: geometry/material identities and three-child aggregation contract. Last Updated: 2026-09-21.

Inputs:
    - coverage_1_in: coverage_1_in parameter
    - mass_2_in: mass_2_in parameter
    - price_3_in: price_3_in parameter
    - volume_1_in: volume_1_in parameter
    - price_1_in: price_1_in parameter
    - mass_1_in: mass_1_in parameter
    - unquantified_volume_3_in: unquantified_volume_3_in parameter
    - coverage_2_in: coverage_2_in parameter
    - volume_3_in: volume_3_in parameter
    - price_2_in: price_2_in parameter
    - coverage_3_in: coverage_3_in parameter
    - mass_3_in: mass_3_in parameter
    - unquantified_volume_1_in: unquantified_volume_1_in parameter
    - unquantified_volume_2_in: unquantified_volume_2_in parameter
    - volume_2_in: volume_2_in parameter

Outputs:
    - known_mass: known_mass result
    - unquantified_volume: unquantified_volume result
    - source_price_subtotal: source_price_subtotal result
    - volume: volume result

SysML Source: root-0/sector_constituent_inventory.sysml:38

SysML Source: root-0/sector_constituent_inventory.sysml:38

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/sector_constituent_inventory/three_sector_inventory_sum_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from inventory_tea.primitives import Float
from inventory_tea.schemas.three_sector_inventory_sum_output import Three_Sector_Inventory_SumOutput


class Three_Sector_Inventory_SumInput(BaseModel):
    """Input model for Three_Sector_Inventory_SumModule.

    Attributes:
        coverage_1_in: coverage_1_in input
        mass_2_in: mass_2_in input
        price_3_in: price_3_in input
        volume_1_in: volume_1_in input
        price_1_in: price_1_in input
        mass_1_in: mass_1_in input
        unquantified_volume_3_in: unquantified_volume_3_in input
        coverage_2_in: coverage_2_in input
        volume_3_in: volume_3_in input
        price_2_in: price_2_in input
        coverage_3_in: coverage_3_in input
        mass_3_in: mass_3_in input
        unquantified_volume_1_in: unquantified_volume_1_in input
        unquantified_volume_2_in: unquantified_volume_2_in input
        volume_2_in: volume_2_in input
    """
    coverage_1_in: float = Field(..., description="coverage_1_in input")
    mass_2_in: float = Field(..., description="mass_2_in input")
    price_3_in: float = Field(..., description="price_3_in input")
    volume_1_in: float = Field(..., description="volume_1_in input")
    price_1_in: float = Field(..., description="price_1_in input")
    mass_1_in: float = Field(..., description="mass_1_in input")
    unquantified_volume_3_in: float = Field(..., description="unquantified_volume_3_in input")
    coverage_2_in: float = Field(..., description="coverage_2_in input")
    volume_3_in: float = Field(..., description="volume_3_in input")
    price_2_in: float = Field(..., description="price_2_in input")
    coverage_3_in: float = Field(..., description="coverage_3_in input")
    mass_3_in: float = Field(..., description="mass_3_in input")
    unquantified_volume_1_in: float = Field(..., description="unquantified_volume_1_in input")
    unquantified_volume_2_in: float = Field(..., description="unquantified_volume_2_in input")
    volume_2_in: float = Field(..., description="volume_2_in input")


class Three_Sector_Inventory_SumModule(ModuleBase[Three_Sector_Inventory_SumInput, Three_Sector_Inventory_SumOutput]):
    """TEAx module for Three_Sector_Inventory_Sum calculation.

The three supplied lateral coverages must each lie in [0,1] and sum to one within 1e-12, including zero-volume cases. Refuse inconsistent supplied partitions; never normalize them. This establishes arithmetic partition closure, not geometric nonoverlap qualification.

volume = volume_1_in + volume_2_in + volume_3_in; known_mass = mass_1_in + mass_2_in + mass_3_in; source_price_subtotal = price_1_in + price_2_in + price_3_in; unquantified_volume = unquantified_volume_1_in + unquantified_volume_2_in + unquantified_volume_3_in. Inputs and outputs finite nonnegative. Units m3, kg and same-source-year dollars; no currency conversion. Sums three nonoverlapping lateral layer occurrences, not arbitrary stacked area fractions. Partial source-price sum is not installed capital. Guarded typed completion implements these equations through the native route. Source: work/active/WI-084_aries-sector-constituent-inventory/spec.md. Reference: geometry/material identities and three-child aggregation contract. Last Updated: 2026-09-21.

Inputs:
    - coverage_1_in: coverage_1_in parameter
    - mass_2_in: mass_2_in parameter
    - price_3_in: price_3_in parameter
    - volume_1_in: volume_1_in parameter
    - price_1_in: price_1_in parameter
    - mass_1_in: mass_1_in parameter
    - unquantified_volume_3_in: unquantified_volume_3_in parameter
    - coverage_2_in: coverage_2_in parameter
    - volume_3_in: volume_3_in parameter
    - price_2_in: price_2_in parameter
    - coverage_3_in: coverage_3_in parameter
    - mass_3_in: mass_3_in parameter
    - unquantified_volume_1_in: unquantified_volume_1_in parameter
    - unquantified_volume_2_in: unquantified_volume_2_in parameter
    - volume_2_in: volume_2_in parameter

Outputs:
    - known_mass: known_mass result
    - unquantified_volume: unquantified_volume result
    - source_price_subtotal: source_price_subtotal result
    - volume: volume result

SysML Source: root-0/sector_constituent_inventory.sysml:38

    SysML Source: root-0/sector_constituent_inventory.sysml:38

    Calculation Specification:
        See documentation:
The three supplied lateral coverages must each lie in [0,1] and sum to one within 1e-12, including zero-volume cases. Refuse inconsistent supplied partitions; never normalize them. This establishes arithmetic partition closure, not geometric nonoverlap qualification.

volume = volume_1_in + volume_2_in + volume_3_in; known_mass = mass_1_in + mass_2_in + mass_3_in; source_price_subtotal = price_1_in + price_2_in + price_3_in; unquantified_volume = unquantified_volume_1_in + unquantified_volume_2_in + unquantified_volume_3_in. Inputs and outputs finite nonnegative. Units m3, kg and same-source-year dollars; no currency conversion. Sums three nonoverlapping lateral layer occurrences, not arbitrary stacked area fractions. Partial source-price sum is not installed capital. Guarded typed completion implements these equations through the native route. Source: work/active/WI-084_aries-sector-constituent-inventory/spec.md. Reference: geometry/material identities and three-child aggregation contract. Last Updated: 2026-09-21.

    IMPLEMENTATION: See inventory_tea.handwritten.sector_constituent_inventory.three_sector_inventory_sum_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts known_mass, unquantified_volume, source_price_subtotal, volume fields to separate channels.
    """

    name: str = "Three_Sector_Inventory_SumModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, coverage_1_in: float, mass_2_in: float, price_3_in: float, volume_1_in: float, price_1_in: float, mass_1_in: float, unquantified_volume_3_in: float, coverage_2_in: float, volume_3_in: float, price_2_in: float, coverage_3_in: float, mass_3_in: float, unquantified_volume_1_in: float, unquantified_volume_2_in: float, volume_2_in: float    ) -> Three_Sector_Inventory_SumInput:
        """Validate inputs and fill defaults.

        Args:
            coverage_1_in: coverage_1_in input
            mass_2_in: mass_2_in input
            price_3_in: price_3_in input
            volume_1_in: volume_1_in input
            price_1_in: price_1_in input
            mass_1_in: mass_1_in input
            unquantified_volume_3_in: unquantified_volume_3_in input
            coverage_2_in: coverage_2_in input
            volume_3_in: volume_3_in input
            price_2_in: price_2_in input
            coverage_3_in: coverage_3_in input
            mass_3_in: mass_3_in input
            unquantified_volume_1_in: unquantified_volume_1_in input
            unquantified_volume_2_in: unquantified_volume_2_in input
            volume_2_in: volume_2_in input

        Returns:
            Validated input model
        """
        return Three_Sector_Inventory_SumInput(coverage_1_in=coverage_1_in, mass_2_in=mass_2_in, price_3_in=price_3_in, volume_1_in=volume_1_in, price_1_in=price_1_in, mass_1_in=mass_1_in, unquantified_volume_3_in=unquantified_volume_3_in, coverage_2_in=coverage_2_in, volume_3_in=volume_3_in, price_2_in=price_2_in, coverage_3_in=coverage_3_in, mass_3_in=mass_3_in, unquantified_volume_1_in=unquantified_volume_1_in, unquantified_volume_2_in=unquantified_volume_2_in, volume_2_in=volume_2_in)

    def run(
        self, coverage_1_in: float, mass_2_in: float, price_3_in: float, volume_1_in: float, price_1_in: float, mass_1_in: float, unquantified_volume_3_in: float, coverage_2_in: float, volume_3_in: float, price_2_in: float, coverage_3_in: float, mass_3_in: float, unquantified_volume_1_in: float, unquantified_volume_2_in: float, volume_2_in: float    ) -> ModuleResult[Three_Sector_Inventory_SumOutput]:
        """Execute calculation.

        Args:
            coverage_1_in: coverage_1_in input
            mass_2_in: mass_2_in input
            price_3_in: price_3_in input
            volume_1_in: volume_1_in input
            price_1_in: price_1_in input
            mass_1_in: mass_1_in input
            unquantified_volume_3_in: unquantified_volume_3_in input
            coverage_2_in: coverage_2_in input
            volume_3_in: volume_3_in input
            price_2_in: price_2_in input
            coverage_3_in: coverage_3_in input
            mass_3_in: mass_3_in input
            unquantified_volume_1_in: unquantified_volume_1_in input
            unquantified_volume_2_in: unquantified_volume_2_in input
            volume_2_in: volume_2_in input

        Returns:
            Module result with Three_Sector_Inventory_SumOutput (known_mass, unquantified_volume, source_price_subtotal, volume)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(coverage_1_in, mass_2_in, price_3_in, volume_1_in, price_1_in, mass_1_in, unquantified_volume_3_in, coverage_2_in, volume_3_in, price_2_in, coverage_3_in, mass_3_in, unquantified_volume_1_in, unquantified_volume_2_in, volume_2_in)

        # Import handwritten implementation
        from inventory_tea.handwritten.sector_constituent_inventory.three_sector_inventory_sum_impl import (
            run_three_sector_inventory_sum,
        )

        # Execute implementation - returns tuple of values
        known_mass, unquantified_volume, source_price_subtotal, volume = run_three_sector_inventory_sum(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Three_Sector_Inventory_SumOutput(
                known_mass=known_mass,
                unquantified_volume=unquantified_volume,
                source_price_subtotal=source_price_subtotal,
                volume=volume,
            )
        )
