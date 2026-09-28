from pydantic import BaseModel, Field


class MfeVacuumParams(BaseModel):
    """Parameters from mfe_vacuum.

    Generated from SysML calculation definitions.
    """
    stellarator_09__stellaris__vacuum__k_B_in: float = Field(default=1.380649e-23, description="Entry point: k_B_in")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
