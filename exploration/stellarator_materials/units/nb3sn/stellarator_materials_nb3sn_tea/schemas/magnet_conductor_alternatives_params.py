from pydantic import BaseModel, Field


class MagnetConductorAlternativesParams(BaseModel):
    """Parameters from magnet_conductor_alternatives.

    Generated from SysML calculation definitions.
    """
    stellarator_09_materials__nb3sn_material__magnet__conductor__eps_intrinsic_in: float = Field(default=0.0, description="Entry point: eps_intrinsic_in")
    stellarator_09_materials__nb3sn_material__magnet__inventory__manufacturing_per_m_in: float = Field(default=0.0, description="Entry point: manufacturing_per_m_in")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
