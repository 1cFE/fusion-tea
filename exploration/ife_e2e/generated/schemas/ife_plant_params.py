from pydantic import BaseModel, Field


class IfePlantParams(BaseModel):
    """Parameters from ife_plant.

    Generated from SysML calculation definitions.
    """
    hif_plant_pkg__hif_plant__viability__threshold: float = Field(default=10.0, description="Entry point: threshold")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
