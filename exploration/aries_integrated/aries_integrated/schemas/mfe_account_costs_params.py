from pydantic import BaseModel, Field


class MfeAccountCostsParams(BaseModel):
    """Parameters from mfe_account_costs.

    Generated from SysML calculation definitions.
    """
    aries_integrated_plant__annual_om__evaluate__alpha: float = Field(default=0.5, description="Entry point: alpha")
    aries_integrated_plant__annual_om__evaluate__n_mod_in: float = Field(default=1.0, description="Entry point: n_mod_in")
    aries_integrated_plant__annual_om__evaluate__om_ref: float = Field(default=0.0, description="Entry point: om_ref")
    aries_integrated_plant__annual_om__evaluate__p_net: float = Field(default=1000.0, description="Entry point: p_net")
    aries_integrated_plant__annual_om__evaluate__ref_net_power: float = Field(default=1000.0, description="Entry point: ref_net_power")
    aries_integrated_plant__indirect_cost__evaluate__construction_time: float = Field(default=6.0, description="Entry point: construction_time")
    aries_integrated_plant__indirect_cost__evaluate__reference_construction_time: float = Field(default=6.0, description="Entry point: reference_construction_time")
    aries_integrated_plant__operating_levelization__evaluate__inflation_rate_in: float = Field(default=0.0, description="Entry point: inflation_rate_in")
    aries_integrated_plant__operating_levelization__evaluate__project_time: float = Field(default=0.0, description="Entry point: project_time")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
