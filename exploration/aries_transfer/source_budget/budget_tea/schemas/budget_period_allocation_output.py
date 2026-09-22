from pydantic import Field
from simkit.config.schema import MultiOutput

class Budget_Period_AllocationOutput(MultiOutput):
    """Multi-output container for Budget_Period_Allocation.

Source: work/active/WI-088_aries-source-budget-cost-contribution/spec.md. Ref: accepted financial scope and Lyon Eq7/account mapping. Basis: AGENT generic disjoint-budget accounting and explicit period convention. period=selected_period for mode0; period=selected_period/availability for mode1. annual_capital=capital/period; annual_replacement=replacement/period; partial_annual_cost=annual_capital+annual_replacement; annual_energy=8760*net_power*availability; lifetime_energy=annual_energy*period. Guarded pass-through net_power/availability; constant module_count1 and excluded_annual_channel0 are nonpublic outputs. Dollars, MW, years, MWh; mode selects explicit comparison convention, not inferred reliability. Native guard rejects nonfinite/negative budgets, nonpositive multiplier/period/power, mode outside0/1, availability outside(0,1], overflow and zero energy. Last Updated: 2026-09-21.

SysML Source: root-0/source_budget_accounting.sysml:18
    """
    annual_replacement: float = Field(description="annual_replacement output")
    module_count: float = Field(description="module_count output")
    validated_availability: float = Field(description="validated_availability output")
    annual_energy: float = Field(description="annual_energy output")
    lifetime_energy: float = Field(description="lifetime_energy output")
    excluded_annual_channel: float = Field(description="excluded_annual_channel output")
    comparison_period: float = Field(description="comparison_period output")
    partial_annual_cost: float = Field(description="partial_annual_cost output")
    annual_capital: float = Field(description="annual_capital output")
    validated_net_power: float = Field(description="validated_net_power output")
