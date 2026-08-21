from pydantic import BaseModel, Field


class MfePlasmaScalingParams(BaseModel):
    """Parameters from mfe_plasma_scaling.

    Generated from SysML calculation definitions.
    """
    stellarator_09__stellaris__geom__pi: float = Field(default=3.14159265358979, description="Entry point: pi")
    stellarator_09__stellaris__rb__pi: float = Field(default=3.14159265358979, description="Entry point: pi")
    stellarator_09__stellaris__wall_load_calc__ash_frac_in: float = Field(default=0.2002, description="Entry point: ash_frac_in")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
