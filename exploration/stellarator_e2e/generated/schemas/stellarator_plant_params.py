from pydantic import BaseModel, Field


class StellaratorPlantParams(BaseModel):
    """Parameters from stellarator_plant.sysml.

    Generated from SysML calculation definitions.
    """
    stellarator_09__stellaris__wall_load_calc__ash_frac: float = Field(default=0.2002, description="Entry point: ash_frac")
    stellarator_09__stellaris__wall_load_calc__wall_area: float = Field(default=802.201, description="Entry point: wall_area")

    model_config = {"frozen": True, "extra": "forbid"}
