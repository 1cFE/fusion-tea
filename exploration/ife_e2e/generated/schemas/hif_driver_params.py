from pydantic import BaseModel, Field


class HifDriverParams(BaseModel):
    """Parameters from hif_driver.sysml.

    Generated from SysML calculation definitions.
    """
    hif_driver__HIF_Driver__efficiency: float = Field(default=0.35, description="Entry point: efficiency")

    model_config = {"frozen": True, "extra": "forbid"}
