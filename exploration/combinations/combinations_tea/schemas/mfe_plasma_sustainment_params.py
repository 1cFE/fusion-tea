from pydantic import BaseModel, Field


class MfePlasmaSustainmentParams(BaseModel):
    """Parameters from mfe_plasma_sustainment.

    Generated from SysML calculation definitions.
    """
    combinations_plasma_chain__plasma_chain__plasma__sustain__R_w_sync_in: float = Field(default=0.6, description="Entry point: R_w_sync_in")
    combinations_plasma_chain__plasma_chain__plasma__sustain__ash_frac_in: float = Field(default=0.2002, description="Entry point: ash_frac_in")
    combinations_plasma_chain__plasma_chain__plasma__sustain__kappa_sync_in: float = Field(default=1.0, description="Entry point: kappa_sync_in")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
