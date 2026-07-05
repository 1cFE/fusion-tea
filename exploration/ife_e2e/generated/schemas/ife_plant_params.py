from pydantic import BaseModel, Field


class IfePlantParams(BaseModel):
    """Parameters from ife_plant.sysml.

    Generated from SysML calculation definitions.
    """
    hif_plant_pkg__hif_plant__lcoe_calc__availability: float = Field(description="Entry point: availability")
    hif_plant_pkg__hif_plant__lcoe_calc__blanket_energy_multiple: float = Field(description="Entry point: blanket_energy_multiple")
    hif_plant_pkg__hif_plant__lcoe_calc__discount_rate: float = Field(description="Entry point: discount_rate")
    hif_plant_pkg__hif_plant__lcoe_calc__driver_cost_constant: float = Field(description="Entry point: driver_cost_constant")
    hif_plant_pkg__hif_plant__lcoe_calc__driver_efficiency: float = Field(description="Entry point: driver_efficiency")
    hif_plant_pkg__hif_plant__lcoe_calc__driver_energy: float = Field(description="Entry point: driver_energy")
    hif_plant_pkg__hif_plant__lcoe_calc__driver_lifetime_shots: float = Field(description="Entry point: driver_lifetime_shots")
    hif_plant_pkg__hif_plant__lcoe_calc__frequency: float = Field(description="Entry point: frequency")
    hif_plant_pkg__hif_plant__lcoe_calc__gain: float = Field(description="Entry point: gain")
    hif_plant_pkg__hif_plant__lcoe_calc__om_cost_constant: float = Field(description="Entry point: om_cost_constant")
    hif_plant_pkg__hif_plant__lcoe_calc__plant_cost_constant: float = Field(description="Entry point: plant_cost_constant")
    hif_plant_pkg__hif_plant__lcoe_calc__target_cost_constant: float = Field(description="Entry point: target_cost_constant")
    hif_plant_pkg__hif_plant__lcoe_calc__thermal_efficiency: float = Field(description="Entry point: thermal_efficiency")
    hif_plant_pkg__hif_plant__lcoe_calc__yield_cost_constant: float = Field(description="Entry point: yield_cost_constant")
    hif_plant_pkg__hif_plant__recirc_calc__eta: float = Field(description="Entry point: eta")
    hif_plant_pkg__hif_plant__recirc_calc__gain: float = Field(description="Entry point: gain")
    hif_plant_pkg__hif_plant__recirc_calc__blanket_multiplier: float = Field(description="Entry point: blanket_multiplier")
    hif_plant_pkg__hif_plant__recirc_calc__thermal_efficiency: float = Field(description="Entry point: thermal_efficiency")
    hif_plant_pkg__hif_plant__lcoe_calc__construction_years: float = Field(default=5.0, description="Entry point: construction_years")
    hif_plant_pkg__hif_plant__lcoe_calc__operational_years: float = Field(default=40.0, description="Entry point: operational_years")

    model_config = {"frozen": True, "extra": "forbid"}
