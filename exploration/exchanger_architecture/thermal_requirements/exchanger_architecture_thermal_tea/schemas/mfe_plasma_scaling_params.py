from pydantic import BaseModel, Field


class MfePlasmaScalingParams(BaseModel):
    """Parameters from mfe_plasma_scaling.

    Generated from SysML calculation definitions.
    """
    aries_cs_plasma_integration__plasma__beta_calculation__mu0: float = Field(default=1.25663706212e-06, description="Entry point: mu0")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
