"""Three_Constituent_Recipe_SummaryModule Module Wrapper

TEAx module for Three_Constituent_Recipe_Summary calculation.

represented_fraction = fraction_1_in + fraction_2_in + fraction_3_in; unquantified_volume = region_volume_in * unquantified_fraction_in; known_mass = mass_1_in + mass_2_in + mass_3_in; source_price_subtotal = price_1_in + price_2_in + price_3_in. Units m3, kg and same-source-year dollars; no currency conversion. Finite nonnegative inputs, each fraction in [0,1]; sum of represented and unquantified fractions must equal one within 1e-12, an arithmetic closure tolerance. Check closure even at zero volume. Reject nonfinite outputs. Three explicitly represented material children plus an unquantified-volume complement; their mass and price coverage remain partial. Guarded typed completion implements these equations through the native route. Source: work/active/WI-084_aries-sector-constituent-inventory/spec.md. Reference: geometry/material identities and three-child aggregation contract. Last Updated: 2026-09-21.

Inputs:
    - mass_1_in: mass_1_in parameter
    - region_volume_in: region_volume_in parameter
    - unquantified_fraction_in: unquantified_fraction_in parameter
    - mass_3_in: mass_3_in parameter
    - fraction_1_in: fraction_1_in parameter
    - fraction_3_in: fraction_3_in parameter
    - mass_2_in: mass_2_in parameter
    - fraction_2_in: fraction_2_in parameter
    - price_3_in: price_3_in parameter
    - price_2_in: price_2_in parameter
    - price_1_in: price_1_in parameter

Outputs:
    - unquantified_volume: unquantified_volume result
    - source_price_subtotal: source_price_subtotal result
    - known_mass: known_mass result
    - represented_fraction: represented_fraction result

SysML Source: root-0/sector_constituent_inventory.sysml:20

SysML Source: root-0/sector_constituent_inventory.sysml:20

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/sector_constituent_inventory/three_constituent_recipe_summary_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from inventory_tea.primitives import Float
from inventory_tea.schemas.three_constituent_recipe_summary_output import Three_Constituent_Recipe_SummaryOutput


class Three_Constituent_Recipe_SummaryInput(BaseModel):
    """Input model for Three_Constituent_Recipe_SummaryModule.

    Attributes:
        mass_1_in: mass_1_in input
        region_volume_in: region_volume_in input
        unquantified_fraction_in: unquantified_fraction_in input
        mass_3_in: mass_3_in input
        fraction_1_in: fraction_1_in input
        fraction_3_in: fraction_3_in input
        mass_2_in: mass_2_in input
        fraction_2_in: fraction_2_in input
        price_3_in: price_3_in input
        price_2_in: price_2_in input
        price_1_in: price_1_in input
    """
    mass_1_in: float = Field(..., description="mass_1_in input")
    region_volume_in: float = Field(..., description="region_volume_in input")
    unquantified_fraction_in: float = Field(..., description="unquantified_fraction_in input")
    mass_3_in: float = Field(..., description="mass_3_in input")
    fraction_1_in: float = Field(..., description="fraction_1_in input")
    fraction_3_in: float = Field(..., description="fraction_3_in input")
    mass_2_in: float = Field(..., description="mass_2_in input")
    fraction_2_in: float = Field(..., description="fraction_2_in input")
    price_3_in: float = Field(..., description="price_3_in input")
    price_2_in: float = Field(..., description="price_2_in input")
    price_1_in: float = Field(..., description="price_1_in input")


class Three_Constituent_Recipe_SummaryModule(ModuleBase[Three_Constituent_Recipe_SummaryInput, Three_Constituent_Recipe_SummaryOutput]):
    """TEAx module for Three_Constituent_Recipe_Summary calculation.

represented_fraction = fraction_1_in + fraction_2_in + fraction_3_in; unquantified_volume = region_volume_in * unquantified_fraction_in; known_mass = mass_1_in + mass_2_in + mass_3_in; source_price_subtotal = price_1_in + price_2_in + price_3_in. Units m3, kg and same-source-year dollars; no currency conversion. Finite nonnegative inputs, each fraction in [0,1]; sum of represented and unquantified fractions must equal one within 1e-12, an arithmetic closure tolerance. Check closure even at zero volume. Reject nonfinite outputs. Three explicitly represented material children plus an unquantified-volume complement; their mass and price coverage remain partial. Guarded typed completion implements these equations through the native route. Source: work/active/WI-084_aries-sector-constituent-inventory/spec.md. Reference: geometry/material identities and three-child aggregation contract. Last Updated: 2026-09-21.

Inputs:
    - mass_1_in: mass_1_in parameter
    - region_volume_in: region_volume_in parameter
    - unquantified_fraction_in: unquantified_fraction_in parameter
    - mass_3_in: mass_3_in parameter
    - fraction_1_in: fraction_1_in parameter
    - fraction_3_in: fraction_3_in parameter
    - mass_2_in: mass_2_in parameter
    - fraction_2_in: fraction_2_in parameter
    - price_3_in: price_3_in parameter
    - price_2_in: price_2_in parameter
    - price_1_in: price_1_in parameter

Outputs:
    - unquantified_volume: unquantified_volume result
    - source_price_subtotal: source_price_subtotal result
    - known_mass: known_mass result
    - represented_fraction: represented_fraction result

SysML Source: root-0/sector_constituent_inventory.sysml:20

    SysML Source: root-0/sector_constituent_inventory.sysml:20

    Calculation Specification:
        See documentation:
represented_fraction = fraction_1_in + fraction_2_in + fraction_3_in; unquantified_volume = region_volume_in * unquantified_fraction_in; known_mass = mass_1_in + mass_2_in + mass_3_in; source_price_subtotal = price_1_in + price_2_in + price_3_in. Units m3, kg and same-source-year dollars; no currency conversion. Finite nonnegative inputs, each fraction in [0,1]; sum of represented and unquantified fractions must equal one within 1e-12, an arithmetic closure tolerance. Check closure even at zero volume. Reject nonfinite outputs. Three explicitly represented material children plus an unquantified-volume complement; their mass and price coverage remain partial. Guarded typed completion implements these equations through the native route. Source: work/active/WI-084_aries-sector-constituent-inventory/spec.md. Reference: geometry/material identities and three-child aggregation contract. Last Updated: 2026-09-21.

    IMPLEMENTATION: See inventory_tea.handwritten.sector_constituent_inventory.three_constituent_recipe_summary_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts unquantified_volume, source_price_subtotal, known_mass, represented_fraction fields to separate channels.
    """

    name: str = "Three_Constituent_Recipe_SummaryModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, mass_1_in: float, region_volume_in: float, unquantified_fraction_in: float, mass_3_in: float, fraction_1_in: float, fraction_3_in: float, mass_2_in: float, fraction_2_in: float, price_3_in: float, price_2_in: float, price_1_in: float    ) -> Three_Constituent_Recipe_SummaryInput:
        """Validate inputs and fill defaults.

        Args:
            mass_1_in: mass_1_in input
            region_volume_in: region_volume_in input
            unquantified_fraction_in: unquantified_fraction_in input
            mass_3_in: mass_3_in input
            fraction_1_in: fraction_1_in input
            fraction_3_in: fraction_3_in input
            mass_2_in: mass_2_in input
            fraction_2_in: fraction_2_in input
            price_3_in: price_3_in input
            price_2_in: price_2_in input
            price_1_in: price_1_in input

        Returns:
            Validated input model
        """
        return Three_Constituent_Recipe_SummaryInput(mass_1_in=mass_1_in, region_volume_in=region_volume_in, unquantified_fraction_in=unquantified_fraction_in, mass_3_in=mass_3_in, fraction_1_in=fraction_1_in, fraction_3_in=fraction_3_in, mass_2_in=mass_2_in, fraction_2_in=fraction_2_in, price_3_in=price_3_in, price_2_in=price_2_in, price_1_in=price_1_in)

    def run(
        self, mass_1_in: float, region_volume_in: float, unquantified_fraction_in: float, mass_3_in: float, fraction_1_in: float, fraction_3_in: float, mass_2_in: float, fraction_2_in: float, price_3_in: float, price_2_in: float, price_1_in: float    ) -> ModuleResult[Three_Constituent_Recipe_SummaryOutput]:
        """Execute calculation.

        Args:
            mass_1_in: mass_1_in input
            region_volume_in: region_volume_in input
            unquantified_fraction_in: unquantified_fraction_in input
            mass_3_in: mass_3_in input
            fraction_1_in: fraction_1_in input
            fraction_3_in: fraction_3_in input
            mass_2_in: mass_2_in input
            fraction_2_in: fraction_2_in input
            price_3_in: price_3_in input
            price_2_in: price_2_in input
            price_1_in: price_1_in input

        Returns:
            Module result with Three_Constituent_Recipe_SummaryOutput (unquantified_volume, source_price_subtotal, known_mass, represented_fraction)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(mass_1_in, region_volume_in, unquantified_fraction_in, mass_3_in, fraction_1_in, fraction_3_in, mass_2_in, fraction_2_in, price_3_in, price_2_in, price_1_in)

        # Import handwritten implementation
        from inventory_tea.handwritten.sector_constituent_inventory.three_constituent_recipe_summary_impl import (
            run_three_constituent_recipe_summary,
        )

        # Execute implementation - returns tuple of values
        unquantified_volume, source_price_subtotal, known_mass, represented_fraction = run_three_constituent_recipe_summary(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Three_Constituent_Recipe_SummaryOutput(
                unquantified_volume=unquantified_volume,
                source_price_subtotal=source_price_subtotal,
                known_mass=known_mass,
                represented_fraction=represented_fraction,
            )
        )
