from pydantic import Field
from simkit.config.schema import MultiOutput

class Whole_Plant_Capital_AccountsOutput(MultiOutput):
    """Multi-output container for Whole_Plant_Capital_Accounts.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/whole_plant_capital_accounts_impl.py; reviewed equations in design/configuration.

SysML Source: root-0/whole_plant_conversion_accounts.sysml:178
    """
    common_purchases: float = Field(description="common_purchases output")
    nonfuel_commissioning: float = Field(description="nonfuel_commissioning output")
    salvage_base: float = Field(description="salvage_base output")
    equipment_base: float = Field(description="equipment_base output")
    general_spares: float = Field(description="general_spares output")
    indirect: float = Field(description="indirect output")
    freight_base: float = Field(description="freight_base output")
    cas50: float = Field(description="cas50 output")
    freight: float = Field(description="freight output")
    initial_capital: float = Field(description="initial_capital output")
    direct_base: float = Field(description="direct_base output")
    contingency: float = Field(description="contingency output")
    branch_purchases: float = Field(description="branch_purchases output")
    insurance: float = Field(description="insurance output")
    tax: float = Field(description="tax output")
    domain_supported: float = Field(description="domain_supported output")
    reconciliation_residual: float = Field(description="reconciliation_residual output")
    cas20: float = Field(description="cas20 output")
    overhaul_base: float = Field(description="overhaul_base output")
    general_spares_base: float = Field(description="general_spares_base output")
    insurance_base: float = Field(description="insurance_base output")
    cas30: float = Field(description="cas30 output")
    tax_base: float = Field(description="tax_base output")
