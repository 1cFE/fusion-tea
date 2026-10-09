from pydantic import BaseModel, Field


class MfeMagnetPartsParams(BaseModel):
    """Parameters from mfe_magnet_parts.

    Generated from SysML calculation definitions.
    """
    stellarator_09_materials__rebco_material__magnet__coil__arm_slope: float = Field(default=0.0, description="Entry point: arm_slope")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
