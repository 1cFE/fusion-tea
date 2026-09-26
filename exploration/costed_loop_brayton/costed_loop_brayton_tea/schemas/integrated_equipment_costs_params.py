from pydantic import BaseModel, Field


class IntegratedEquipmentCostsParams(BaseModel):
    """Parameters from integrated_equipment_costs.

    Generated from SysML calculation definitions.
    """
    costed_loop_brayton__plant__contingency_basis__evaluate__amount3_in: float = Field(default=0.0, description="Entry point: amount3_in")
    costed_loop_brayton__plant__contingency_basis__evaluate__amount4_in: float = Field(default=0.0, description="Entry point: amount4_in")
    costed_loop_brayton__plant__contingency_basis__evaluate__amount5_in: float = Field(default=0.0, description="Entry point: amount5_in")
    costed_loop_brayton__plant__contingency_basis__evaluate__amount6_in: float = Field(default=0.0, description="Entry point: amount6_in")
    costed_loop_brayton__plant__contingency_basis__evaluate__amount7_in: float = Field(default=0.0, description="Entry point: amount7_in")
    costed_loop_brayton__plant__contingency_basis__evaluate__amount8_in: float = Field(default=0.0, description="Entry point: amount8_in")
    costed_loop_brayton__plant__cost_ledger__evaluate__currency_year_in: float = Field(default=2004.0, description="Entry point: currency_year_in")
    costed_loop_brayton__plant__direct_cost__evaluate__amount4_in: float = Field(default=0.0, description="Entry point: amount4_in")
    costed_loop_brayton__plant__direct_cost__evaluate__amount5_in: float = Field(default=0.0, description="Entry point: amount5_in")
    costed_loop_brayton__plant__direct_cost__evaluate__amount6_in: float = Field(default=0.0, description="Entry point: amount6_in")
    costed_loop_brayton__plant__direct_cost__evaluate__amount7_in: float = Field(default=0.0, description="Entry point: amount7_in")
    costed_loop_brayton__plant__direct_cost__evaluate__amount8_in: float = Field(default=0.0, description="Entry point: amount8_in")
    costed_loop_brayton__plant__priced_equipment__evaluate__amount8_in: float = Field(default=0.0, description="Entry point: amount8_in")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
