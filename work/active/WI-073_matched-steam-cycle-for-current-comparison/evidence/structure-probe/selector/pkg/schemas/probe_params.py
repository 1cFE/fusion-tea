from pydantic import BaseModel, Field


class ProbeParams(BaseModel):
    """Parameters from probe.

    Generated from SysML calculation definitions.
    """
    Probe__plant__turbine__enabled: float = Field(default=0.0, description="Entry point: enabled")
    Probe__plant__turbine__raw: float = Field(default=3.0, description="Entry point: raw")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
