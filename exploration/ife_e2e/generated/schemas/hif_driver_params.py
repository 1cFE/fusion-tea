from pydantic import BaseModel, Field


class HifDriverParams(BaseModel):
    """Parameters from hif_driver.

    Generated from SysML calculation definitions.
    """
    hif_plant_pkg__hif_plant__driver__efficiency: float = Field(default=0.28, description="Entry point: efficiency")
    hif_plant_pkg__hif_plant__driver__lifetime_shots: float = Field(default=6000000000.0, description="Entry point: lifetime_shots")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
