from pydantic import BaseModel, Field


class SystemDesign(BaseModel):
    """Parameters from hierarchy.

    Generated from SysML calculation definitions.
    """
    hif_plant_pkg__hif_plant__driver__meier_cost__beam_energy_mj: float = Field(default=5.0, description="Entry point: beam_energy_mj")
    hif_plant_pkg__hif_plant__driver__meier_cost__num_chambers: float = Field(default=1.0, description="Entry point: num_chambers")
    hif_plant_pkg__hif_plant__driver__meier_cost__rep_rate: float = Field(default=3.5, description="Entry point: rep_rate")
    hif_plant_pkg__hif_plant__lcoe_calc__availability: float = Field(default=0.9, description="Entry point: availability")
    hif_plant_pkg__hif_plant__lcoe_calc__discount_rate: float = Field(default=0.08, description="Entry point: discount_rate")
    hif_plant_pkg__hif_plant__lcoe_calc__frequency: float = Field(default=3.5, description="Entry point: frequency")
    hif_plant_pkg__hif_plant__lcoe_calc__gain: float = Field(default=80.0, description="Entry point: gain")
    hif_plant_pkg__hif_plant__lcoe_calc__om_cost_constant: float = Field(default=65.0, description="Entry point: om_cost_constant")
    hif_plant_pkg__hif_plant__lcoe_calc__plant_cost_constant: float = Field(default=2000.0, description="Entry point: plant_cost_constant")
    hif_plant_pkg__hif_plant__lcoe_calc__thermal_efficiency: float = Field(default=0.43, description="Entry point: thermal_efficiency")
    hif_plant_pkg__hif_plant__meier_coe_calc__availability: float = Field(default=0.9, description="Entry point: availability")
    hif_plant_pkg__hif_plant__recirc_calc__gain: float = Field(default=80.0, description="Entry point: gain")
    hif_plant_pkg__hif_plant__recirc_calc__thermal_efficiency: float = Field(default=0.43, description="Entry point: thermal_efficiency")

    model_config = {"frozen": True, "extra": "forbid"}
