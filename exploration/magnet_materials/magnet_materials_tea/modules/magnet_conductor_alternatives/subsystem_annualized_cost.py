"""Subsystem_Annualized_CostModule Module Wrapper

TEAx module for Subsystem_Annualized_Cost calculation.

capital_total = winding_capital + refrigerator_capital; annual_electricity = p_in_total_MW*hours*availability*electricity_price (USD/MWh); annualized_cost = crf*capital_total + annual_electricity. **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: section 2.7; contract section 7. **Basis**: [AGENT] capital recovery factor and electricity price are case inputs; partial accounting within the evaluated categories. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/subsystem_annualized_cost_impl.py. **Last Updated**: 2026-09-29

Inputs:
    - p_in_total_MW_in: p_in_total_MW_in parameter
    - availability_in: availability_in parameter
    - crf_in: crf_in parameter
    - electricity_price_in: electricity_price_in parameter
    - hours_in: hours_in parameter
    - winding_capital_in: winding_capital_in parameter
    - refrigerator_capital_in: refrigerator_capital_in parameter

Outputs:
    - capital_total: capital_total result
    - annualized_cost: annualized_cost result
    - annual_electricity: annual_electricity result

SysML Source: root-0/magnet_conductor_alternatives.sysml:233

SysML Source: root-0/magnet_conductor_alternatives.sysml:233

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/magnet_conductor_alternatives/subsystem_annualized_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from magnet_materials_tea.primitives import Float
from magnet_materials_tea.schemas.subsystem_annualized_cost_output import Subsystem_Annualized_CostOutput


class Subsystem_Annualized_CostInput(BaseModel):
    """Input model for Subsystem_Annualized_CostModule.

    Attributes:
        p_in_total_MW_in: p_in_total_MW_in input
        availability_in: availability_in input
        crf_in: crf_in input
        electricity_price_in: electricity_price_in input
        hours_in: hours_in input
        winding_capital_in: winding_capital_in input
        refrigerator_capital_in: refrigerator_capital_in input
    """
    p_in_total_MW_in: float = Field(..., description="p_in_total_MW_in input")
    availability_in: float = Field(..., description="availability_in input")
    crf_in: float = Field(..., description="crf_in input")
    electricity_price_in: float = Field(..., description="electricity_price_in input")
    hours_in: float = Field(..., description="hours_in input")
    winding_capital_in: float = Field(..., description="winding_capital_in input")
    refrigerator_capital_in: float = Field(..., description="refrigerator_capital_in input")


class Subsystem_Annualized_CostModule(ModuleBase[Subsystem_Annualized_CostInput, Subsystem_Annualized_CostOutput]):
    """TEAx module for Subsystem_Annualized_Cost calculation.

capital_total = winding_capital + refrigerator_capital; annual_electricity = p_in_total_MW*hours*availability*electricity_price (USD/MWh); annualized_cost = crf*capital_total + annual_electricity. **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: section 2.7; contract section 7. **Basis**: [AGENT] capital recovery factor and electricity price are case inputs; partial accounting within the evaluated categories. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/subsystem_annualized_cost_impl.py. **Last Updated**: 2026-09-29

Inputs:
    - p_in_total_MW_in: p_in_total_MW_in parameter
    - availability_in: availability_in parameter
    - crf_in: crf_in parameter
    - electricity_price_in: electricity_price_in parameter
    - hours_in: hours_in parameter
    - winding_capital_in: winding_capital_in parameter
    - refrigerator_capital_in: refrigerator_capital_in parameter

Outputs:
    - capital_total: capital_total result
    - annualized_cost: annualized_cost result
    - annual_electricity: annual_electricity result

SysML Source: root-0/magnet_conductor_alternatives.sysml:233

    SysML Source: root-0/magnet_conductor_alternatives.sysml:233

    Calculation Specification:
        winding_capital_in = 0.0
        refrigerator_capital_in = 0.0
        p_in_total_MW_in = 0.0
        crf_in = 0.0
        hours_in = 0.0
        availability_in = 0.0
        electricity_price_in = 0.0
        
Documentation:
capital_total = winding_capital + refrigerator_capital; annual_electricity = p_in_total_MW*hours*availability*electricity_price (USD/MWh); annualized_cost = crf*capital_total + annual_electricity. **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: section 2.7; contract section 7. **Basis**: [AGENT] capital recovery factor and electricity price are case inputs; partial accounting within the evaluated categories. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/subsystem_annualized_cost_impl.py. **Last Updated**: 2026-09-29

    IMPLEMENTATION: See magnet_materials_tea.handwritten.magnet_conductor_alternatives.subsystem_annualized_cost_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts capital_total, annualized_cost, annual_electricity fields to separate channels.
    """

    name: str = "Subsystem_Annualized_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, p_in_total_MW_in: float, availability_in: float, crf_in: float, electricity_price_in: float, hours_in: float, winding_capital_in: float, refrigerator_capital_in: float    ) -> Subsystem_Annualized_CostInput:
        """Validate inputs and fill defaults.

        Args:
            p_in_total_MW_in: p_in_total_MW_in input
            availability_in: availability_in input
            crf_in: crf_in input
            electricity_price_in: electricity_price_in input
            hours_in: hours_in input
            winding_capital_in: winding_capital_in input
            refrigerator_capital_in: refrigerator_capital_in input

        Returns:
            Validated input model
        """
        return Subsystem_Annualized_CostInput(p_in_total_MW_in=p_in_total_MW_in, availability_in=availability_in, crf_in=crf_in, electricity_price_in=electricity_price_in, hours_in=hours_in, winding_capital_in=winding_capital_in, refrigerator_capital_in=refrigerator_capital_in)

    def run(
        self, p_in_total_MW_in: float, availability_in: float, crf_in: float, electricity_price_in: float, hours_in: float, winding_capital_in: float, refrigerator_capital_in: float    ) -> ModuleResult[Subsystem_Annualized_CostOutput]:
        """Execute calculation.

        Args:
            p_in_total_MW_in: p_in_total_MW_in input
            availability_in: availability_in input
            crf_in: crf_in input
            electricity_price_in: electricity_price_in input
            hours_in: hours_in input
            winding_capital_in: winding_capital_in input
            refrigerator_capital_in: refrigerator_capital_in input

        Returns:
            Module result with Subsystem_Annualized_CostOutput (capital_total, annualized_cost, annual_electricity)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(p_in_total_MW_in, availability_in, crf_in, electricity_price_in, hours_in, winding_capital_in, refrigerator_capital_in)

        # Import handwritten implementation
        from magnet_materials_tea.handwritten.magnet_conductor_alternatives.subsystem_annualized_cost_impl import (
            run_subsystem_annualized_cost,
        )

        # Execute implementation - returns tuple of values
        capital_total, annualized_cost, annual_electricity = run_subsystem_annualized_cost(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Subsystem_Annualized_CostOutput(
                capital_total=capital_total,
                annualized_cost=annualized_cost,
                annual_electricity=annual_electricity,
            )
        )
