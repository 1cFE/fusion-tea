"""Meier_COEModule Module Wrapper

TEAx module for Meier_COE calculation.

Cost of Electricity from Meier's engineering-economic model.
Combines fixed charge rate (8.3%) and O&M rate (3%) into a
single capital charge rate (11.3%). Exposes the numerator and
energy denominator for Generating Electricity Price.

Constants: 0.113 = R + M (8.3% fixed charge + 3% O&M),
0.0876 = 8760 hr/yr * 1e6 kW/GW / (1e9 dollars/billion * 100 cents/dollar),
the scaled energy denominator when cost is in billions and price in cents/kWh.

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Reference**: Eq. 1 (lines 76-102)
*Last Updated**: 2026-09-10
*Basis**: Meier 1986 COE formula. Year-dollars: 1988$.

Inputs:
    - net_electric_power_gw_in: net_electric_power_gw_in parameter
    - total_capital_billions: total_capital_billions parameter
    - availability_in: availability_in parameter

Outputs:
    - energy_denominator: energy_denominator result
    - annualized_cost: annualized_cost result

SysML Source: root-0/analyses/hif_economics.sysml:88

SysML Source: root-0/analyses/hif_economics.sysml:88

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/hif_economics/meier_coe_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from ife_tea.primitives import Float
from ife_tea.schemas.meier_coe_output import Meier_COEOutput


class Meier_COEInput(BaseModel):
    """Input model for Meier_COEModule.

    Attributes:
        net_electric_power_gw_in: net_electric_power_gw_in input
        total_capital_billions: total_capital_billions input
        availability_in: availability_in input
    """
    net_electric_power_gw_in: float = Field(..., description="net_electric_power_gw_in input")
    total_capital_billions: float = Field(..., description="total_capital_billions input")
    availability_in: float = Field(..., description="availability_in input")


class Meier_COEModule(ModuleBase[Meier_COEInput, Meier_COEOutput]):
    """TEAx module for Meier_COE calculation.

Cost of Electricity from Meier's engineering-economic model.
Combines fixed charge rate (8.3%) and O&M rate (3%) into a
single capital charge rate (11.3%). Exposes the numerator and
energy denominator for Generating Electricity Price.

Constants: 0.113 = R + M (8.3% fixed charge + 3% O&M),
0.0876 = 8760 hr/yr * 1e6 kW/GW / (1e9 dollars/billion * 100 cents/dollar),
the scaled energy denominator when cost is in billions and price in cents/kWh.

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Reference**: Eq. 1 (lines 76-102)
*Last Updated**: 2026-09-10
*Basis**: Meier 1986 COE formula. Year-dollars: 1988$.

Inputs:
    - net_electric_power_gw_in: net_electric_power_gw_in parameter
    - total_capital_billions: total_capital_billions parameter
    - availability_in: availability_in parameter

Outputs:
    - energy_denominator: energy_denominator result
    - annualized_cost: annualized_cost result

SysML Source: root-0/analyses/hif_economics.sysml:88

    SysML Source: root-0/analyses/hif_economics.sysml:88

    Calculation Specification:
        annualized_cost = 0.113 * total_capital_billions
        energy_denominator = 0.0876 * availability_in * net_electric_power_gw_in
        
Documentation:
Cost of Electricity from Meier's engineering-economic model.
Combines fixed charge rate (8.3%) and O&M rate (3%) into a
single capital charge rate (11.3%). Exposes the numerator and
energy denominator for Generating Electricity Price.

Constants: 0.113 = R + M (8.3% fixed charge + 3% O&M),
0.0876 = 8760 hr/yr * 1e6 kW/GW / (1e9 dollars/billion * 100 cents/dollar),
the scaled energy denominator when cost is in billions and price in cents/kWh.

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Reference**: Eq. 1 (lines 76-102)
*Last Updated**: 2026-09-10
*Basis**: Meier 1986 COE formula. Year-dollars: 1988$.

    IMPLEMENTATION: See ife_tea.handwritten.hif_economics.meier_coe_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts energy_denominator, annualized_cost fields to separate channels.
    """

    name: str = "Meier_COEModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, net_electric_power_gw_in: float, total_capital_billions: float, availability_in: float    ) -> Meier_COEInput:
        """Validate inputs and fill defaults.

        Args:
            net_electric_power_gw_in: net_electric_power_gw_in input
            total_capital_billions: total_capital_billions input
            availability_in: availability_in input

        Returns:
            Validated input model
        """
        return Meier_COEInput(net_electric_power_gw_in=net_electric_power_gw_in, total_capital_billions=total_capital_billions, availability_in=availability_in)

    def run(
        self, net_electric_power_gw_in: float, total_capital_billions: float, availability_in: float    ) -> ModuleResult[Meier_COEOutput]:
        """Execute calculation.

        Args:
            net_electric_power_gw_in: net_electric_power_gw_in input
            total_capital_billions: total_capital_billions input
            availability_in: availability_in input

        Returns:
            Module result with Meier_COEOutput (energy_denominator, annualized_cost)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(net_electric_power_gw_in, total_capital_billions, availability_in)

        # Import handwritten implementation
        from ife_tea.handwritten.hif_economics.meier_coe_impl import (
            run_meier_coe,
        )

        # Execute implementation - returns tuple of values
        energy_denominator, annualized_cost = run_meier_coe(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Meier_COEOutput(
                energy_denominator=energy_denominator,
                annualized_cost=annualized_cost,
            )
        )
