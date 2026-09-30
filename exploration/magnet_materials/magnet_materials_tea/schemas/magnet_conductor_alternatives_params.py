from pydantic import BaseModel, Field


class MagnetConductorAlternativesParams(BaseModel):
    """Parameters from magnet_conductor_alternatives.

    Generated from SysML calculation definitions.
    """
    magnet_subsystem__subsystem__nb3sn__conductor__eps_intrinsic_in: float = Field(default=0.0, description="Entry point: eps_intrinsic_in")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
