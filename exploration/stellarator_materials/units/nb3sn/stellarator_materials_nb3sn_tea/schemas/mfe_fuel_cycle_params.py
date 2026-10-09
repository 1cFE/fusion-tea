from pydantic import BaseModel, Field


class MfeFuelCycleParams(BaseModel):
    """Parameters from mfe_fuel_cycle.

    Generated from SysML calculation definitions.
    """
    stellarator_09_materials__nb3sn_material__fuel_cycle__fuel__s_per_fpy_in: float = Field(default=31536000.0, description="Entry point: s_per_fpy_in")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
