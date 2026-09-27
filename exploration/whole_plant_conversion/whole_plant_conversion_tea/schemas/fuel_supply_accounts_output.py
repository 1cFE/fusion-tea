from pydantic import Field
from simkit.config.schema import MultiOutput

class Fuel_Supply_AccountsOutput(MultiOutput):
    """Multi-output container for Fuel_Supply_Accounts.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/fuel_supply_accounts_impl.py; reviewed equations in design/configuration.

SysML Source: root-0/whole_plant_conversion_accounts.sysml:83
    """
    initial_T_cost: float = Field(description="initial_T_cost output")
    processing_kg_s: float = Field(description="processing_kg_s output")
    annual_T_bred: float = Field(description="annual_T_bred output")
    annual_T_surplus: float = Field(description="annual_T_surplus output")
    annual_T_cost: float = Field(description="annual_T_cost output")
    self_sufficiency_margin: float = Field(description="self_sufficiency_margin output")
    stock_margin: float = Field(description="stock_margin output")
    processing_margin: float = Field(description="processing_margin output")
    Li6_atom_residual: float = Field(description="Li6_atom_residual output")
    annual_Li6_cost: float = Field(description="annual_Li6_cost output")
    annual_D_cost: float = Field(description="annual_D_cost output")
    T_atom_residual: float = Field(description="T_atom_residual output")
    domain_supported: float = Field(description="domain_supported output")
    annual_Li6_kg: float = Field(description="annual_Li6_kg output")
    loss_kg_s: float = Field(description="loss_kg_s output")
    D_atom_residual: float = Field(description="D_atom_residual output")
    burn_kg_s: float = Field(description="burn_kg_s output")
    annual_T_need: float = Field(description="annual_T_need output")
    annual_D_kg: float = Field(description="annual_D_kg output")
    annual_T_external: float = Field(description="annual_T_external output")
    reaction_rate: float = Field(description="reaction_rate output")
    annual_fuel: float = Field(description="annual_fuel output")
