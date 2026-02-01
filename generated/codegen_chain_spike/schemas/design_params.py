from pydantic import BaseModel, Field


class DesignParams(BaseModel):
    """Parameters from design.sysml.

    Generated from SysML calculation definitions.
    """
    ChainSpikeDesign__spike_design__area_calc__length: float = Field(description="Entry point: length")
    ChainSpikeDesign__spike_design__area_calc__width: float = Field(description="Entry point: width")
    ChainSpikeDesign__spike_design__cost_calc__rate: float = Field(description="Entry point: rate")

    model_config = {"frozen": True, "extra": "forbid"}
