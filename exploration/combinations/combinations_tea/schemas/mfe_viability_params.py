from pydantic import BaseModel, Field


class MfeViabilityParams(BaseModel):
    """Parameters from mfe_viability.

    Generated from SysML calculation definitions.
    """
    combinations_plasma_chain__plasma_chain__divertor_pump__screen__applicable_in: bool = Field(default=1.0, description="Entry point: applicable_in")
    combinations_plasma_chain__plasma_chain__divertor_pump__screen__conditions_supported_in: bool = Field(default=1.0, description="Entry point: conditions_supported_in")
    combinations_plasma_chain__plasma_chain__divertor_pump__screen__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    combinations_plasma_chain__plasma_chain__he_pump__screen__applicable_in: bool = Field(default=1.0, description="Entry point: applicable_in")
    combinations_plasma_chain__plasma_chain__he_pump__screen__conditions_supported_in: bool = Field(default=1.0, description="Entry point: conditions_supported_in")
    combinations_plasma_chain__plasma_chain__he_pump__screen__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    combinations_plasma_chain__plasma_chain__pbli_pump__screen__applicable_in: bool = Field(default=1.0, description="Entry point: applicable_in")
    combinations_plasma_chain__plasma_chain__pbli_pump__screen__conditions_supported_in: bool = Field(default=1.0, description="Entry point: conditions_supported_in")
    combinations_plasma_chain__plasma_chain__pbli_pump__screen__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
