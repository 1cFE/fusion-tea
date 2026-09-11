from pydantic import BaseModel, Field


class IfeLcoeParams(BaseModel):
    """Parameters from ife_lcoe.

    Generated from SysML calculation definitions.
    """
    hif_plant_pkg__hif_plant__lcoe_calc__construction_years: float = Field(default=5.0, description="Entry point: construction_years")
    hif_plant_pkg__hif_plant__lcoe_calc__operational_years: float = Field(default=40.0, description="Entry point: operational_years")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
