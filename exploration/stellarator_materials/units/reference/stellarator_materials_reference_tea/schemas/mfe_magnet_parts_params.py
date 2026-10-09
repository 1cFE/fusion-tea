from pydantic import BaseModel, Field


class MfeMagnetPartsParams(BaseModel):
    """Parameters from mfe_magnet_parts.

    Generated from SysML calculation definitions.
    """
    stellarator_09__stellaris__magnet__coil__arm_slope: float = Field(default=0.0, description="Entry point: arm_slope")
    stellarator_09__stellaris__magnet__coil__arm_x_ref: float = Field(default=0.0, description="Entry point: arm_x_ref")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
