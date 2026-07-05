from pydantic import BaseModel, Field


class HifDriverParams(BaseModel):
    """Parameters from hif_driver.sysml.

    Generated from SysML calculation definitions.
    """
    hif_driver__hif_driver_instance__meier_cost__beam_energy_mj: float = Field(description="Entry point: beam_energy_mj")
    hif_driver__hif_driver_instance__meier_cost__driver_efficiency: float = Field(description="Entry point: driver_efficiency")
    hif_driver__hif_driver_instance__meier_cost__num_chambers: float = Field(description="Entry point: num_chambers")
    hif_driver__hif_driver_instance__meier_cost__rep_rate: float = Field(description="Entry point: rep_rate")

    model_config = {"frozen": True, "extra": "forbid"}
