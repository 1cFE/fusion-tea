"""Supplied_Primary_CapacityModule Module Wrapper

TEAx module for Supplied_Primary_Capacity calculation.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/supplied_primary_capacity_impl.py; reviewed equations in design/configuration.

Inputs:
    - pressure_demand_Pa_in: pressure_demand_Pa_in parameter
    - electric_demand_MW_in: electric_demand_MW_in parameter
    - path_count_in: path_count_in parameter
    - path_flow_demand_in: path_flow_demand_in parameter
    - path_flow_rating_in: path_flow_rating_in parameter
    - electric_rating_MW_in: electric_rating_MW_in parameter
    - pressure_rating_Pa_in: pressure_rating_Pa_in parameter

Outputs:
    - electric_margin_MW: electric_margin_MW result
    - pressure_margin_Pa: pressure_margin_Pa result
    - flow_margin_kg_s: flow_margin_kg_s result
    - inventory_supported: inventory_supported result

SysML Source: root-0/whole_plant_conversion_accounts.sysml:127

SysML Source: root-0/whole_plant_conversion_accounts.sysml:127

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/whole_plant_conversion_accounts/supplied_primary_capacity_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.primitives import Float
from whole_plant_conversion_tea.schemas.supplied_primary_capacity_output import Supplied_Primary_CapacityOutput


class Supplied_Primary_CapacityInput(BaseModel):
    """Input model for Supplied_Primary_CapacityModule.

    Attributes:
        pressure_demand_Pa_in: pressure_demand_Pa_in input
        electric_demand_MW_in: electric_demand_MW_in input
        path_count_in: path_count_in input
        path_flow_demand_in: path_flow_demand_in input
        path_flow_rating_in: path_flow_rating_in input
        electric_rating_MW_in: electric_rating_MW_in input
        pressure_rating_Pa_in: pressure_rating_Pa_in input
    """
    pressure_demand_Pa_in: float = Field(..., description="pressure_demand_Pa_in input")
    electric_demand_MW_in: float = Field(..., description="electric_demand_MW_in input")
    path_count_in: float = Field(..., description="path_count_in input")
    path_flow_demand_in: float = Field(..., description="path_flow_demand_in input")
    path_flow_rating_in: float = Field(..., description="path_flow_rating_in input")
    electric_rating_MW_in: float = Field(..., description="electric_rating_MW_in input")
    pressure_rating_Pa_in: float = Field(..., description="pressure_rating_Pa_in input")


class Supplied_Primary_CapacityModule(ModuleBase[Supplied_Primary_CapacityInput, Supplied_Primary_CapacityOutput]):
    """TEAx module for Supplied_Primary_Capacity calculation.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/supplied_primary_capacity_impl.py; reviewed equations in design/configuration.

Inputs:
    - pressure_demand_Pa_in: pressure_demand_Pa_in parameter
    - electric_demand_MW_in: electric_demand_MW_in parameter
    - path_count_in: path_count_in parameter
    - path_flow_demand_in: path_flow_demand_in parameter
    - path_flow_rating_in: path_flow_rating_in parameter
    - electric_rating_MW_in: electric_rating_MW_in parameter
    - pressure_rating_Pa_in: pressure_rating_Pa_in parameter

Outputs:
    - electric_margin_MW: electric_margin_MW result
    - pressure_margin_Pa: pressure_margin_Pa result
    - flow_margin_kg_s: flow_margin_kg_s result
    - inventory_supported: inventory_supported result

SysML Source: root-0/whole_plant_conversion_accounts.sysml:127

    SysML Source: root-0/whole_plant_conversion_accounts.sysml:127

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/supplied_primary_capacity_impl.py; reviewed equations in design/configuration.

    IMPLEMENTATION: See whole_plant_conversion_tea.handwritten.whole_plant_conversion_accounts.supplied_primary_capacity_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts electric_margin_MW, pressure_margin_Pa, flow_margin_kg_s, inventory_supported fields to separate channels.
    """

    name: str = "Supplied_Primary_CapacityModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, pressure_demand_Pa_in: float, electric_demand_MW_in: float, path_count_in: float, path_flow_demand_in: float, path_flow_rating_in: float, electric_rating_MW_in: float, pressure_rating_Pa_in: float    ) -> Supplied_Primary_CapacityInput:
        """Validate inputs and fill defaults.

        Args:
            pressure_demand_Pa_in: pressure_demand_Pa_in input
            electric_demand_MW_in: electric_demand_MW_in input
            path_count_in: path_count_in input
            path_flow_demand_in: path_flow_demand_in input
            path_flow_rating_in: path_flow_rating_in input
            electric_rating_MW_in: electric_rating_MW_in input
            pressure_rating_Pa_in: pressure_rating_Pa_in input

        Returns:
            Validated input model
        """
        return Supplied_Primary_CapacityInput(pressure_demand_Pa_in=pressure_demand_Pa_in, electric_demand_MW_in=electric_demand_MW_in, path_count_in=path_count_in, path_flow_demand_in=path_flow_demand_in, path_flow_rating_in=path_flow_rating_in, electric_rating_MW_in=electric_rating_MW_in, pressure_rating_Pa_in=pressure_rating_Pa_in)

    def run(
        self, pressure_demand_Pa_in: float, electric_demand_MW_in: float, path_count_in: float, path_flow_demand_in: float, path_flow_rating_in: float, electric_rating_MW_in: float, pressure_rating_Pa_in: float    ) -> ModuleResult[Supplied_Primary_CapacityOutput]:
        """Execute calculation.

        Args:
            pressure_demand_Pa_in: pressure_demand_Pa_in input
            electric_demand_MW_in: electric_demand_MW_in input
            path_count_in: path_count_in input
            path_flow_demand_in: path_flow_demand_in input
            path_flow_rating_in: path_flow_rating_in input
            electric_rating_MW_in: electric_rating_MW_in input
            pressure_rating_Pa_in: pressure_rating_Pa_in input

        Returns:
            Module result with Supplied_Primary_CapacityOutput (electric_margin_MW, pressure_margin_Pa, flow_margin_kg_s, inventory_supported)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(pressure_demand_Pa_in, electric_demand_MW_in, path_count_in, path_flow_demand_in, path_flow_rating_in, electric_rating_MW_in, pressure_rating_Pa_in)

        # Import handwritten implementation
        from whole_plant_conversion_tea.handwritten.whole_plant_conversion_accounts.supplied_primary_capacity_impl import (
            run_supplied_primary_capacity,
        )

        # Execute implementation - returns tuple of values
        electric_margin_MW, pressure_margin_Pa, flow_margin_kg_s, inventory_supported = run_supplied_primary_capacity(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Supplied_Primary_CapacityOutput(
                electric_margin_MW=electric_margin_MW,
                pressure_margin_Pa=pressure_margin_Pa,
                flow_margin_kg_s=flow_margin_kg_s,
                inventory_supported=inventory_supported,
            )
        )
