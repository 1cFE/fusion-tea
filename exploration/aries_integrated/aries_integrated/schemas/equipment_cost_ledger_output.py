from pydantic import Field
from simkit.config.schema import MultiOutput

class Equipment_Cost_LedgerOutput(MultiOutput):
    """Multi-output container for Equipment_Cost_Ledger.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

SysML Source: root-0/integrated_equipment_costs.sysml:98
    """
    annual_operating: float = Field(description="annual_operating output")
    source_inclusive: float = Field(description="source_inclusive output")
    direct: float = Field(description="direct output")
    source_reactor_gap: float = Field(description="source_reactor_gap output")
    direct_difference: float = Field(description="direct_difference output")
    annual_export_mwh: float = Field(description="annual_export_mwh output")
    source_direct: float = Field(description="source_direct output")
    source_coil_excess: float = Field(description="source_coil_excess output")
    annual_import_cost: float = Field(description="annual_import_cost output")
    annual_replacement_reserve: float = Field(description="annual_replacement_reserve output")
    source_core_excess: float = Field(description="source_core_excess output")
    overnight: float = Field(description="overnight output")
    annual_import_mwh: float = Field(description="annual_import_mwh output")
    lifetime_replacement: float = Field(description="lifetime_replacement output")
    currency_year: float = Field(description="currency_year output")
