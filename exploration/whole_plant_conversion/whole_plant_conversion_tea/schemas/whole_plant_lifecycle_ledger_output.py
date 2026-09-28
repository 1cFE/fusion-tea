from pydantic import Field
from simkit.config.schema import MultiOutput

class Whole_Plant_Lifecycle_LedgerOutput(MultiOutput):
    """Multi-output container for Whole_Plant_Lifecycle_Ledger.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/whole_plant_lifecycle_ledger_impl.py; reviewed equations in design/configuration.

SysML Source: root-0/whole_plant_conversion_accounts.sysml:255
    """
    cost_residual: float = Field(description="cost_residual output")
    source_replacement_pv: float = Field(description="source_replacement_pv output")
    annual_service: float = Field(description="annual_service output")
    initial_financed_capital: float = Field(description="initial_financed_capital output")
    primary_replacement_pv: float = Field(description="primary_replacement_pv output")
    total_cost_pv: float = Field(description="total_cost_pv output")
    energy_pv: float = Field(description="energy_pv output")
    economic_defined: float = Field(description="economic_defined output")
    conversion_replacement_pv: float = Field(description="conversion_replacement_pv output")
    magnet_events: float = Field(description="magnet_events output")
    annual_expense: float = Field(description="annual_expense output")
    lcoe_USD2025_MWh: float = Field(description="lcoe_USD2025_MWh output")
    annual_expense_pv: float = Field(description="annual_expense_pv output")
    primary_events: float = Field(description="primary_events output")
    outage_years: float = Field(description="outage_years output")
    domain_supported: float = Field(description="domain_supported output")
    terminal_pv: float = Field(description="terminal_pv output")
    annual_makeup: float = Field(description="annual_makeup output")
    magnet_life_years: float = Field(description="magnet_life_years output")
    magnet_replacement_pv: float = Field(description="magnet_replacement_pv output")
    overhaul_pv: float = Field(description="overhaul_pv output")
    annual_source_service: float = Field(description="annual_source_service output")
    blanket_events: float = Field(description="blanket_events output")
    outage_margin: float = Field(description="outage_margin output")
    blanket_life_years: float = Field(description="blanket_life_years output")
    blanket_replacement_pv: float = Field(description="blanket_replacement_pv output")
