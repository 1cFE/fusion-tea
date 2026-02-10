from pydantic import BaseModel, Field


class PipelineConfig(BaseModel):
    model_path: str = Field(..., description="Path to SysML model directory")
    model_config = {"frozen": True, "extra": "forbid"}
