from pydantic import BaseModel, Field


class SourceBudgetParams(BaseModel):
    """Parameters from source_budget.

    Generated from SysML calculation definitions.
    """
    aries_source_budget__budget_period__selected_availability: float = Field(default=0.85, description="Entry point: selected_availability")
    aries_source_budget__budget_period__selected_mode: float = Field(default=0.0, description="Entry point: selected_mode")
    aries_source_budget__budget_period__selected_net_power: float = Field(default=1000.0, description="Entry point: selected_net_power")
    aries_source_budget__budget_period__selected_period: float = Field(default=40.0, description="Entry point: selected_period")
    aries_source_budget__capital_budget__inclusive_multiplier: float = Field(default=1.93, description="Entry point: inclusive_multiplier")
    aries_source_budget__electrical_equipment__selected_cost_usd2004: float = Field(default=138764000.0, description="Entry point: selected_cost_usd2004")
    aries_source_budget__heat_rejection__selected_cost_usd2004: float = Field(default=56086000.0, description="Entry point: selected_cost_usd2004")
    aries_source_budget__land__selected_cost_usd2004: float = Field(default=12929000.0, description="Entry point: selected_cost_usd2004")
    aries_source_budget__miscellaneous_equipment__selected_cost_usd2004: float = Field(default=70958000.0, description="Entry point: selected_cost_usd2004")
    aries_source_budget__reactor_equipment__selected_cost_usd2004: float = Field(default=1538817000.0, description="Entry point: selected_cost_usd2004")
    aries_source_budget__replacement_budget__selected_lifetime_cost_usd2004: float = Field(default=966000000.0, description="Entry point: selected_lifetime_cost_usd2004")
    aries_source_budget__special_materials__selected_cost_usd2004: float = Field(default=151327000.0, description="Entry point: selected_cost_usd2004")
    aries_source_budget__structures__selected_cost_usd2004: float = Field(default=336133000.0, description="Entry point: selected_cost_usd2004")
    aries_source_budget__turbine_equipment__selected_cost_usd2004: float = Field(default=314558000.0, description="Entry point: selected_cost_usd2004")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
