from pydantic import BaseModel, Field


class DualBlanketHeatParams(BaseModel):
    """Parameters from dual_blanket_heat.

    Generated from SysML calculation definitions.
    """
    aries_dual_blanket_heat__helium__assumed_conditions_supported: bool = Field(default=1.0, description="Entry point: assumed_conditions_supported")
    aries_dual_blanket_heat__helium__deposited_heat_mw: float = Field(default=940.0, description="Entry point: deposited_heat_mw")
    aries_dual_blanket_heat__helium__duty_available: bool = Field(default=1.0, description="Entry point: duty_available")
    aries_dual_blanket_heat__helium__offered_duty_mw: float = Field(default=1250.0, description="Entry point: offered_duty_mw")
    aries_dual_blanket_heat__helium__recovered_friction_mw: float = Field(default=141.0, description="Entry point: recovered_friction_mw")
    aries_dual_blanket_heat__helium__scenario_applicable: bool = Field(default=1.0, description="Entry point: scenario_applicable")
    aries_dual_blanket_heat__inter_coolant_exchange__transferred_heat_mw: float = Field(default=111.0, description="Entry point: transferred_heat_mw")
    aries_dual_blanket_heat__pbli__assumed_conditions_supported: bool = Field(default=1.0, description="Entry point: assumed_conditions_supported")
    aries_dual_blanket_heat__pbli__deposited_heat_mw: float = Field(default=1555.0, description="Entry point: deposited_heat_mw")
    aries_dual_blanket_heat__pbli__duty_available: bool = Field(default=1.0, description="Entry point: duty_available")
    aries_dual_blanket_heat__pbli__offered_duty_mw: float = Field(default=1500.0, description="Entry point: offered_duty_mw")
    aries_dual_blanket_heat__pbli__recovered_friction_mw: float = Field(default=0.0, description="Entry point: recovered_friction_mw")
    aries_dual_blanket_heat__pbli__scenario_applicable: bool = Field(default=1.0, description="Entry point: scenario_applicable")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
