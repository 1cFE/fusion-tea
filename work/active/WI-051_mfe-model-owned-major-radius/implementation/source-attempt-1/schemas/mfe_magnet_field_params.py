from pydantic import BaseModel, Field


class MfeMagnetFieldParams(BaseModel):
    """Parameters from mfe_magnet_field.

    Generated from SysML calculation definitions.
    """
    stellarator_09__stellaris__field_calc__mu0: float = Field(default=1.25663706212e-06, description="Entry point: mu0")
    stellarator_09__stellaris__field_calc__two_pi: float = Field(default=6.283185307179586, description="Entry point: two_pi")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
