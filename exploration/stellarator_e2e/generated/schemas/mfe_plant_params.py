from pydantic import BaseModel, Field


class MfePlantParams(BaseModel):
    """Parameters from mfe_plant.

    Generated from SysML calculation definitions.
    """
    stellarator_09__stellaris__n_mod: float = Field(default=1.0, description="Entry point: n_mod")
    stellarator_09__stellaris__recirc_ok__threshold: float = Field(default=0.5, description="Entry point: threshold")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
