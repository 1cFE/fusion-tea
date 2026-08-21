from pydantic import BaseModel, Field


class MfeMagnetCostParams(BaseModel):
    """Parameters from mfe_magnet_cost.

    Generated from SysML calculation definitions.
    """
    stellarator_09__stellaris__magnet_cost__mu0: float = Field(default=1.25663706212e-06, description="Entry point: mu0")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
