from pydantic import BaseModel, Field


class DesignParams(BaseModel):
    """Parameters from design.sysml.

    Generated from SysML calculation definitions.
    """
    SolarBatteryDesign__solar_battery_plant__p_net_mw: float = Field(default=0.008, description="Entry point: p_net_mw")
    SolarBatteryDesign__solar_battery_plant__energy_production__p_net_mw: float = Field(default=0.008, description="Entry point: p_net_mw")
    SolarBatteryDesign__solar_battery_plant__energy_production__n_mod: float = Field(default=1.0, description="Entry point: n_mod")
    SolarBatteryDesign__solar_battery_plant__energy_production__plant_availability: float = Field(default=0.159, description="Entry point: plant_availability")
    SolarBatteryDesign__solar_battery_plant__annualized_om__om_rate_per_kw_year: float = Field(default=20.0, description="Entry point: om_rate_per_kw_year")
    SolarBatteryDesign__solar_battery_plant__annualized_fuel__fuel_unit_cost: float = Field(default=0.0, description="Entry point: fuel_unit_cost")
    SolarBatteryDesign__solar_battery_plant__annualized_fuel__fuel_consumption: float = Field(default=0.0, description="Entry point: fuel_consumption")
    SolarBatteryDesign__solar_battery_plant__annualized_financial__total_capex: float = Field(description="Entry point: total_capex")
    SolarBatteryDesign__solar_battery_plant__annualized_financial__discount_rate: float = Field(default=0.05, description="Entry point: discount_rate")
    SolarBatteryDesign__solar_battery_plant__annualized_financial__plant_lifetime: float = Field(default=25.0, description="Entry point: plant_lifetime")
    SolarBatteryDesign__solar_battery_plant__lcoe__yearly_inflation: float = Field(default=0.0245, description="Entry point: yearly_inflation")
    SolarBatteryDesign__solar_battery_plant__lcoe__plant_lifetime: float = Field(default=25.0, description="Entry point: plant_lifetime")

    model_config = {"frozen": True, "extra": "forbid"}
