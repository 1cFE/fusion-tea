"""Fuel_Supply_AccountsModule Module Wrapper

TEAx module for Fuel_Supply_Accounts calculation.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/fuel_supply_accounts_impl.py; reviewed equations in design/configuration.

Inputs:
    - MeV_J_in: MeV_J_in parameter
    - availability_in: availability_in parameter
    - deuterium_price_in: deuterium_price_in parameter
    - m_Li6_in: m_Li6_in parameter
    - m_D_in: m_D_in parameter
    - seconds_year_in: seconds_year_in parameter
    - tbr_in: tbr_in parameter
    - startup_required_kg_in: startup_required_kg_in parameter
    - processing_capacity_kg_s_in: processing_capacity_kg_s_in parameter
    - tritium_price_in: tritium_price_in parameter
    - stock_kg_in: stock_kg_in parameter
    - fusion_MW_in: fusion_MW_in parameter
    - decay_in: decay_in parameter
    - extraction_in: extraction_in parameter
    - recycle_in: recycle_in parameter
    - q_eff_in: q_eff_in parameter
    - burn_fraction_in: burn_fraction_in parameter
    - li6_price_in: li6_price_in parameter
    - m_T_in: m_T_in parameter

Outputs:
    - initial_T_cost: initial_T_cost result
    - processing_kg_s: processing_kg_s result
    - annual_T_bred: annual_T_bred result
    - annual_T_surplus: annual_T_surplus result
    - annual_T_cost: annual_T_cost result
    - self_sufficiency_margin: self_sufficiency_margin result
    - stock_margin: stock_margin result
    - processing_margin: processing_margin result
    - Li6_atom_residual: Li6_atom_residual result
    - annual_Li6_cost: annual_Li6_cost result
    - annual_D_cost: annual_D_cost result
    - T_atom_residual: T_atom_residual result
    - domain_supported: domain_supported result
    - annual_Li6_kg: annual_Li6_kg result
    - loss_kg_s: loss_kg_s result
    - D_atom_residual: D_atom_residual result
    - burn_kg_s: burn_kg_s result
    - annual_T_need: annual_T_need result
    - annual_D_kg: annual_D_kg result
    - annual_T_external: annual_T_external result
    - reaction_rate: reaction_rate result
    - annual_fuel: annual_fuel result

SysML Source: root-0/whole_plant_conversion_accounts.sysml:83

SysML Source: root-0/whole_plant_conversion_accounts.sysml:83

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/whole_plant_conversion_accounts/fuel_supply_accounts_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.primitives import Float
from whole_plant_conversion_tea.schemas.fuel_supply_accounts_output import Fuel_Supply_AccountsOutput


class Fuel_Supply_AccountsInput(BaseModel):
    """Input model for Fuel_Supply_AccountsModule.

    Attributes:
        MeV_J_in: MeV_J_in input
        availability_in: availability_in input
        deuterium_price_in: deuterium_price_in input
        m_Li6_in: m_Li6_in input
        m_D_in: m_D_in input
        seconds_year_in: seconds_year_in input
        tbr_in: tbr_in input
        startup_required_kg_in: startup_required_kg_in input
        processing_capacity_kg_s_in: processing_capacity_kg_s_in input
        tritium_price_in: tritium_price_in input
        stock_kg_in: stock_kg_in input
        fusion_MW_in: fusion_MW_in input
        decay_in: decay_in input
        extraction_in: extraction_in input
        recycle_in: recycle_in input
        q_eff_in: q_eff_in input
        burn_fraction_in: burn_fraction_in input
        li6_price_in: li6_price_in input
        m_T_in: m_T_in input
    """
    MeV_J_in: float = Field(..., description="MeV_J_in input")
    availability_in: float = Field(..., description="availability_in input")
    deuterium_price_in: float = Field(..., description="deuterium_price_in input")
    m_Li6_in: float = Field(..., description="m_Li6_in input")
    m_D_in: float = Field(..., description="m_D_in input")
    seconds_year_in: float = Field(..., description="seconds_year_in input")
    tbr_in: float = Field(..., description="tbr_in input")
    startup_required_kg_in: float = Field(..., description="startup_required_kg_in input")
    processing_capacity_kg_s_in: float = Field(..., description="processing_capacity_kg_s_in input")
    tritium_price_in: float = Field(..., description="tritium_price_in input")
    stock_kg_in: float = Field(..., description="stock_kg_in input")
    fusion_MW_in: float = Field(..., description="fusion_MW_in input")
    decay_in: float = Field(..., description="decay_in input")
    extraction_in: float = Field(..., description="extraction_in input")
    recycle_in: float = Field(..., description="recycle_in input")
    q_eff_in: float = Field(..., description="q_eff_in input")
    burn_fraction_in: float = Field(..., description="burn_fraction_in input")
    li6_price_in: float = Field(..., description="li6_price_in input")
    m_T_in: float = Field(..., description="m_T_in input")


class Fuel_Supply_AccountsModule(ModuleBase[Fuel_Supply_AccountsInput, Fuel_Supply_AccountsOutput]):
    """TEAx module for Fuel_Supply_Accounts calculation.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/fuel_supply_accounts_impl.py; reviewed equations in design/configuration.

Inputs:
    - MeV_J_in: MeV_J_in parameter
    - availability_in: availability_in parameter
    - deuterium_price_in: deuterium_price_in parameter
    - m_Li6_in: m_Li6_in parameter
    - m_D_in: m_D_in parameter
    - seconds_year_in: seconds_year_in parameter
    - tbr_in: tbr_in parameter
    - startup_required_kg_in: startup_required_kg_in parameter
    - processing_capacity_kg_s_in: processing_capacity_kg_s_in parameter
    - tritium_price_in: tritium_price_in parameter
    - stock_kg_in: stock_kg_in parameter
    - fusion_MW_in: fusion_MW_in parameter
    - decay_in: decay_in parameter
    - extraction_in: extraction_in parameter
    - recycle_in: recycle_in parameter
    - q_eff_in: q_eff_in parameter
    - burn_fraction_in: burn_fraction_in parameter
    - li6_price_in: li6_price_in parameter
    - m_T_in: m_T_in parameter

Outputs:
    - initial_T_cost: initial_T_cost result
    - processing_kg_s: processing_kg_s result
    - annual_T_bred: annual_T_bred result
    - annual_T_surplus: annual_T_surplus result
    - annual_T_cost: annual_T_cost result
    - self_sufficiency_margin: self_sufficiency_margin result
    - stock_margin: stock_margin result
    - processing_margin: processing_margin result
    - Li6_atom_residual: Li6_atom_residual result
    - annual_Li6_cost: annual_Li6_cost result
    - annual_D_cost: annual_D_cost result
    - T_atom_residual: T_atom_residual result
    - domain_supported: domain_supported result
    - annual_Li6_kg: annual_Li6_kg result
    - loss_kg_s: loss_kg_s result
    - D_atom_residual: D_atom_residual result
    - burn_kg_s: burn_kg_s result
    - annual_T_need: annual_T_need result
    - annual_D_kg: annual_D_kg result
    - annual_T_external: annual_T_external result
    - reaction_rate: reaction_rate result
    - annual_fuel: annual_fuel result

SysML Source: root-0/whole_plant_conversion_accounts.sysml:83

    SysML Source: root-0/whole_plant_conversion_accounts.sysml:83

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/fuel_supply_accounts_impl.py; reviewed equations in design/configuration.

    IMPLEMENTATION: See whole_plant_conversion_tea.handwritten.whole_plant_conversion_accounts.fuel_supply_accounts_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts initial_T_cost, processing_kg_s, annual_T_bred, annual_T_surplus, annual_T_cost, self_sufficiency_margin, stock_margin, processing_margin, Li6_atom_residual, annual_Li6_cost, annual_D_cost, T_atom_residual, domain_supported, annual_Li6_kg, loss_kg_s, D_atom_residual, burn_kg_s, annual_T_need, annual_D_kg, annual_T_external, reaction_rate, annual_fuel fields to separate channels.
    """

    name: str = "Fuel_Supply_AccountsModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, MeV_J_in: float, availability_in: float, deuterium_price_in: float, m_Li6_in: float, m_D_in: float, seconds_year_in: float, tbr_in: float, startup_required_kg_in: float, processing_capacity_kg_s_in: float, tritium_price_in: float, stock_kg_in: float, fusion_MW_in: float, decay_in: float, extraction_in: float, recycle_in: float, q_eff_in: float, burn_fraction_in: float, li6_price_in: float, m_T_in: float    ) -> Fuel_Supply_AccountsInput:
        """Validate inputs and fill defaults.

        Args:
            MeV_J_in: MeV_J_in input
            availability_in: availability_in input
            deuterium_price_in: deuterium_price_in input
            m_Li6_in: m_Li6_in input
            m_D_in: m_D_in input
            seconds_year_in: seconds_year_in input
            tbr_in: tbr_in input
            startup_required_kg_in: startup_required_kg_in input
            processing_capacity_kg_s_in: processing_capacity_kg_s_in input
            tritium_price_in: tritium_price_in input
            stock_kg_in: stock_kg_in input
            fusion_MW_in: fusion_MW_in input
            decay_in: decay_in input
            extraction_in: extraction_in input
            recycle_in: recycle_in input
            q_eff_in: q_eff_in input
            burn_fraction_in: burn_fraction_in input
            li6_price_in: li6_price_in input
            m_T_in: m_T_in input

        Returns:
            Validated input model
        """
        return Fuel_Supply_AccountsInput(MeV_J_in=MeV_J_in, availability_in=availability_in, deuterium_price_in=deuterium_price_in, m_Li6_in=m_Li6_in, m_D_in=m_D_in, seconds_year_in=seconds_year_in, tbr_in=tbr_in, startup_required_kg_in=startup_required_kg_in, processing_capacity_kg_s_in=processing_capacity_kg_s_in, tritium_price_in=tritium_price_in, stock_kg_in=stock_kg_in, fusion_MW_in=fusion_MW_in, decay_in=decay_in, extraction_in=extraction_in, recycle_in=recycle_in, q_eff_in=q_eff_in, burn_fraction_in=burn_fraction_in, li6_price_in=li6_price_in, m_T_in=m_T_in)

    def run(
        self, MeV_J_in: float, availability_in: float, deuterium_price_in: float, m_Li6_in: float, m_D_in: float, seconds_year_in: float, tbr_in: float, startup_required_kg_in: float, processing_capacity_kg_s_in: float, tritium_price_in: float, stock_kg_in: float, fusion_MW_in: float, decay_in: float, extraction_in: float, recycle_in: float, q_eff_in: float, burn_fraction_in: float, li6_price_in: float, m_T_in: float    ) -> ModuleResult[Fuel_Supply_AccountsOutput]:
        """Execute calculation.

        Args:
            MeV_J_in: MeV_J_in input
            availability_in: availability_in input
            deuterium_price_in: deuterium_price_in input
            m_Li6_in: m_Li6_in input
            m_D_in: m_D_in input
            seconds_year_in: seconds_year_in input
            tbr_in: tbr_in input
            startup_required_kg_in: startup_required_kg_in input
            processing_capacity_kg_s_in: processing_capacity_kg_s_in input
            tritium_price_in: tritium_price_in input
            stock_kg_in: stock_kg_in input
            fusion_MW_in: fusion_MW_in input
            decay_in: decay_in input
            extraction_in: extraction_in input
            recycle_in: recycle_in input
            q_eff_in: q_eff_in input
            burn_fraction_in: burn_fraction_in input
            li6_price_in: li6_price_in input
            m_T_in: m_T_in input

        Returns:
            Module result with Fuel_Supply_AccountsOutput (initial_T_cost, processing_kg_s, annual_T_bred, annual_T_surplus, annual_T_cost, self_sufficiency_margin, stock_margin, processing_margin, Li6_atom_residual, annual_Li6_cost, annual_D_cost, T_atom_residual, domain_supported, annual_Li6_kg, loss_kg_s, D_atom_residual, burn_kg_s, annual_T_need, annual_D_kg, annual_T_external, reaction_rate, annual_fuel)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(MeV_J_in, availability_in, deuterium_price_in, m_Li6_in, m_D_in, seconds_year_in, tbr_in, startup_required_kg_in, processing_capacity_kg_s_in, tritium_price_in, stock_kg_in, fusion_MW_in, decay_in, extraction_in, recycle_in, q_eff_in, burn_fraction_in, li6_price_in, m_T_in)

        # Import handwritten implementation
        from whole_plant_conversion_tea.handwritten.whole_plant_conversion_accounts.fuel_supply_accounts_impl import (
            run_fuel_supply_accounts,
        )

        # Execute implementation - returns tuple of values
        initial_T_cost, processing_kg_s, annual_T_bred, annual_T_surplus, annual_T_cost, self_sufficiency_margin, stock_margin, processing_margin, Li6_atom_residual, annual_Li6_cost, annual_D_cost, T_atom_residual, domain_supported, annual_Li6_kg, loss_kg_s, D_atom_residual, burn_kg_s, annual_T_need, annual_D_kg, annual_T_external, reaction_rate, annual_fuel = run_fuel_supply_accounts(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Fuel_Supply_AccountsOutput(
                initial_T_cost=initial_T_cost,
                processing_kg_s=processing_kg_s,
                annual_T_bred=annual_T_bred,
                annual_T_surplus=annual_T_surplus,
                annual_T_cost=annual_T_cost,
                self_sufficiency_margin=self_sufficiency_margin,
                stock_margin=stock_margin,
                processing_margin=processing_margin,
                Li6_atom_residual=Li6_atom_residual,
                annual_Li6_cost=annual_Li6_cost,
                annual_D_cost=annual_D_cost,
                T_atom_residual=T_atom_residual,
                domain_supported=domain_supported,
                annual_Li6_kg=annual_Li6_kg,
                loss_kg_s=loss_kg_s,
                D_atom_residual=D_atom_residual,
                burn_kg_s=burn_kg_s,
                annual_T_need=annual_T_need,
                annual_D_kg=annual_D_kg,
                annual_T_external=annual_T_external,
                reaction_rate=reaction_rate,
                annual_fuel=annual_fuel,
            )
        )
