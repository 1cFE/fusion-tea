from pydantic import BaseModel, Field


class MfePlantSystemsParams(BaseModel):
    """Parameters from mfe_plant_systems.

    Generated from SysML calculation definitions.
    """
    stellarator_09_materials__nb3sn_material__fuel_cycle__held_inventory: float = Field(default=0.0, description="Entry point: held_inventory")
    stellarator_09_materials__nb3sn_material__fuel_cycle__s_per_year: float = Field(default=31536000.0, description="Entry point: s_per_year")
    stellarator_09_materials__nb3sn_material__heat_transport__salt_cp_kJ_kgK: float = Field(default=1.56, description="Entry point: salt_cp_kJ_kgK")
    stellarator_09_materials__nb3sn_material__heat_transport__salt_hot_C: float = Field(default=465.0, description="Entry point: salt_hot_C")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
