from pydantic import BaseModel, Field


class StellaratorPlantParams(BaseModel):
    """Parameters from stellarator_plant.sysml.

    Generated from SysML calculation definitions.
    """
    stellarator_09__stellaris__beta: float = Field(default=0.0276, description="Entry point: beta")
    stellarator_09__stellaris__beta_limit: float = Field(default=0.05, description="Entry point: beta_limit")
    stellarator_09__stellaris__tbr: float = Field(default=1.074, description="Entry point: tbr")
    stellarator_09__stellaris__tbr_floor: float = Field(default=1.05, description="Entry point: tbr_floor")
    stellarator_09__stellaris__wall_load_calc__ash_frac: float = Field(default=0.2002, description="Entry point: ash_frac")
    stellarator_09__stellaris__wall_load_limit: float = Field(default=4.05, description="Entry point: wall_load_limit")

    model_config = {"frozen": True, "extra": "forbid"}
