from pydantic import BaseModel, Field


class MfeCryoPlantParams(BaseModel):
    """Parameters from mfe_cryo_plant.

    Generated from SysML calculation definitions.
    """
    stellarator_09_materials__nb3sn_material__cryoplant__cryo_elec__f_uplift: float = Field(default=1.0, description="Entry point: f_uplift")
    stellarator_09_materials__nb3sn_material__cryoplant__cryo_elec__q_nuc: float = Field(default=0.0, description="Entry point: q_nuc")
    stellarator_09_materials__nb3sn_material__cryoplant__cryo_elec__vol_cold: float = Field(default=0.0, description="Entry point: vol_cold")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
