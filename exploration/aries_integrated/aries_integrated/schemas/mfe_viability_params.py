from pydantic import BaseModel, Field


class MfeViabilityParams(BaseModel):
    """Parameters from mfe_viability.

    Generated from SysML calculation definitions.
    """
    aries_integrated_plant__divertor_pump__screen__applicable_in: bool = Field(default=1.0, description="Entry point: applicable_in")
    aries_integrated_plant__divertor_pump__screen__conditions_supported_in: bool = Field(default=1.0, description="Entry point: conditions_supported_in")
    aries_integrated_plant__divertor_pump__screen__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    aries_integrated_plant__fuel_inventory__screen__applicable_in: bool = Field(default=1.0, description="Entry point: applicable_in")
    aries_integrated_plant__fuel_inventory__screen__conditions_supported_in: bool = Field(default=1.0, description="Entry point: conditions_supported_in")
    aries_integrated_plant__fuel_inventory__screen__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    aries_integrated_plant__he_pump__screen__applicable_in: bool = Field(default=1.0, description="Entry point: applicable_in")
    aries_integrated_plant__he_pump__screen__conditions_supported_in: bool = Field(default=1.0, description="Entry point: conditions_supported_in")
    aries_integrated_plant__he_pump__screen__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    aries_integrated_plant__pbli_pump__screen__applicable_in: bool = Field(default=1.0, description="Entry point: applicable_in")
    aries_integrated_plant__pbli_pump__screen__conditions_supported_in: bool = Field(default=1.0, description="Entry point: conditions_supported_in")
    aries_integrated_plant__pbli_pump__screen__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
