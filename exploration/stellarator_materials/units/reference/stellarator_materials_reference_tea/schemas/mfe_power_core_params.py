from pydantic import BaseModel, Field


class MfePowerCoreParams(BaseModel):
    """Parameters from mfe_power_core.

    Generated from SysML calculation definitions.
    """
    stellarator_09__stellaris__magnet__rebco_law_enabled: float = Field(default=1.0, description="Entry point: rebco_law_enabled")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
