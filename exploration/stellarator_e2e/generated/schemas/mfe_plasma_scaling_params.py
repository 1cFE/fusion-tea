from pydantic import BaseModel, Field


class MfePlasmaScalingParams(BaseModel):
    """Parameters from mfe_plasma_scaling.

    Generated from SysML calculation definitions.
    """
    stellarator_09__stellaris__beta_calc__e_keV: float = Field(default=1.602176634e-16, description="Entry point: e_keV")
    stellarator_09__stellaris__beta_calc__mu0: float = Field(default=1.25663706212e-06, description="Entry point: mu0")
    stellarator_09__stellaris__geom__pi: float = Field(default=3.14159265358979, description="Entry point: pi")
    stellarator_09__stellaris__rb__pi: float = Field(default=3.14159265358979, description="Entry point: pi")
    stellarator_09__stellaris__wall_load_calc__ash_frac_in: float = Field(default=0.2002, description="Entry point: ash_frac_in")
    stellarator_09__stellaris__wall_peak_cal__ash_frac_in: float = Field(default=0.2002, description="Entry point: ash_frac_in")
    stellarator_09__stellaris__wall_peak_cal__pi: float = Field(default=3.14159265358979, description="Entry point: pi")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
