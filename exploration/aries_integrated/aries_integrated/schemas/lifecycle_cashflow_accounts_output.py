from pydantic import Field
from simkit.config.schema import MultiOutput

class Lifecycle_Cashflow_AccountsOutput(MultiOutput):
    """Multi-output container for Lifecycle_Cashflow_Accounts.

*Source**: work/active/WI-091_aries-integrated-lifecycle-cost/design.md. **Ref**: reviewed financial convention, roles and F1-F9 assumptions; work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md. **Basis**: conditional real USD2004 dated lifecycle accounts; assumptions are not scientific qualification. **Last Updated**: 2026-09-22.

SysML Source: root-0/integrated_lifecycle_costs.sysml:3
    """
    real_convention: float = Field(description="real_convention output")
    other_overhaul_cost: float = Field(description="other_overhaul_cost output")
    gross_makeup: float = Field(description="gross_makeup output")
    supply_lcoe: float = Field(description="supply_lcoe output")
    other_overhaul_lcoe: float = Field(description="other_overhaul_lcoe output")
    lcoe_sum: float = Field(description="lcoe_sum output")
    noncapital_annual: float = Field(description="noncapital_annual output")
    pv_total_cost: float = Field(description="pv_total_cost output")
    breeding_supported: float = Field(description="breeding_supported output")
    pv_supply: float = Field(description="pv_supply output")
    other_overhaul_occurs: float = Field(description="other_overhaul_occurs output")
    curtailed_feed: float = Field(description="curtailed_feed output")
    replacement_lcoe: float = Field(description="replacement_lcoe output")
    gross_terminal: float = Field(description="gross_terminal output")
    salvage_lcoe: float = Field(description="salvage_lcoe output")
    financial_defined: float = Field(description="financial_defined output")
    idc: float = Field(description="idc output")
    annual_capital: float = Field(description="annual_capital output")
    pv_replacement: float = Field(description="pv_replacement output")
    supply_supported: float = Field(description="supply_supported output")
    om_lcoe: float = Field(description="om_lcoe output")
    pv_terminal_gross: float = Field(description="pv_terminal_gross output")
    tritium_lcoe: float = Field(description="tritium_lcoe output")
    capital_lcoe: float = Field(description="capital_lcoe output")
    annual_energy: float = Field(description="annual_energy output")
    external_shortfall: float = Field(description="external_shortfall output")
    pv_salvage: float = Field(description="pv_salvage output")
    pv_operating: float = Field(description="pv_operating output")
    new_feed: float = Field(description="new_feed output")
    lifetime_energy: float = Field(description="lifetime_energy output")
    financed_capital: float = Field(description="financed_capital output")
    pv_other_overhaul: float = Field(description="pv_other_overhaul output")
    terminal_lcoe: float = Field(description="terminal_lcoe output")
    currency_year: float = Field(description="currency_year output")
    pv_energy: float = Field(description="pv_energy output")
    salvage: float = Field(description="salvage output")
    deuterium_lcoe: float = Field(description="deuterium_lcoe output")
    pv_terminal_net: float = Field(description="pv_terminal_net output")
    imports_lcoe: float = Field(description="imports_lcoe output")
    consumables_lcoe: float = Field(description="consumables_lcoe output")
