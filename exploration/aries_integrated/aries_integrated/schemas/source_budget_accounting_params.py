from pydantic import BaseModel, Field


class SourceBudgetAccountingParams(BaseModel):
    """Parameters from source_budget_accounting.

    Generated from SysML calculation definitions.
    """
    aries_integrated_plant__source_budget__evaluate__account_1_in: float = Field(default=12929000.0, description="Entry point: account_1_in")
    aries_integrated_plant__source_budget__evaluate__account_2_in: float = Field(default=336133000.0, description="Entry point: account_2_in")
    aries_integrated_plant__source_budget__evaluate__account_3_in: float = Field(default=1538817000.0, description="Entry point: account_3_in")
    aries_integrated_plant__source_budget__evaluate__account_4_in: float = Field(default=314558000.0, description="Entry point: account_4_in")
    aries_integrated_plant__source_budget__evaluate__account_5_in: float = Field(default=138764000.0, description="Entry point: account_5_in")
    aries_integrated_plant__source_budget__evaluate__account_6_in: float = Field(default=70958000.0, description="Entry point: account_6_in")
    aries_integrated_plant__source_budget__evaluate__account_7_in: float = Field(default=151327000.0, description="Entry point: account_7_in")
    aries_integrated_plant__source_budget__evaluate__account_8_in: float = Field(default=56086000.0, description="Entry point: account_8_in")
    aries_integrated_plant__source_budget__evaluate__inclusive_multiplier_in: float = Field(default=1.93, description="Entry point: inclusive_multiplier_in")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
