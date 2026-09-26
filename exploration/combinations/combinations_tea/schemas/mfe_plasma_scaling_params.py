from pydantic import BaseModel, Field


class MfePlasmaScalingParams(BaseModel):
    """Parameters from mfe_plasma_scaling.

    Generated from SysML calculation definitions.
    """
    combinations_plasma_chain__plasma_chain__plasma__beta_calc__mu0: float = Field(default=1.25663706212e-06, description="Entry point: mu0")
    combinations_plasma_chain__plasma_chain__plasma__geom__pi: float = Field(default=3.14159265358979, description="Entry point: pi")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
