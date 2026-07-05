from pydantic import BaseModel, Field


class HifPlantParams(BaseModel):
    """Parameters from hif_plant.sysml.

    Generated from SysML calculation definitions.
    """
    hif_plant_pkg__hif_plant__meier_reactor_cost_calc__thermal_power_gw: float = Field(default=2.054, description="Entry point: thermal_power_gw")
    hif_plant_pkg__hif_plant__meier_capital_calc__driver_cost: float = Field(description="Entry point: driver_cost")
    hif_plant_pkg__hif_plant__meier_coe_calc__availability: float = Field(description="Entry point: availability")
    hif_plant_pkg__hif_plant__meier_coe_calc__net_electric_power_gw: float = Field(default=1.0, description="Entry point: net_electric_power_gw")
    hif_plant_pkg__hif_plant__meier_reactor_cost_calc__num_units: float = Field(default=1.0, description="Entry point: num_units")
    hif_plant_pkg__hif_plant__meier_capital_calc__target_factory_cost: float = Field(default=0.1, description="Entry point: target_factory_cost")

    model_config = {"frozen": True, "extra": "forbid"}
