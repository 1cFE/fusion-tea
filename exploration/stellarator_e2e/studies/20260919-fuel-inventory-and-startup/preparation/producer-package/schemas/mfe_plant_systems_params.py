from pydantic import BaseModel, Field


class MfePlantSystemsParams(BaseModel):
    """Parameters from mfe_plant_systems.

    Generated from SysML calculation definitions.
    """
    stellarator_09__stellaris__fuel_cycle__held_inventory: float = Field(default=0.0, description="Entry point: held_inventory")
    stellarator_09__stellaris__fuel_cycle__s_per_year: float = Field(default=31536000.0, description="Entry point: s_per_year")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
