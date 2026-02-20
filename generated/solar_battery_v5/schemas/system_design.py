from pydantic import BaseModel, Field


class SystemDesign(BaseModel):
    """Parameters from hierarchy.

    Generated from SysML calculation definitions.
    """
    SolarBatteryDesign__solar_battery_plant__battery_system__battery_pack__cost_model__capacity_kwh: float = Field(default=5.0, description="Entry point: capacity_kwh")
    SolarBatteryDesign__solar_battery_plant__site_infra__racking__cost_model__panel_count: float = Field(default=20.0, description="Entry point: panel_count")
    SolarBatteryDesign__solar_battery_plant__site_infra__permitting__cost_model__system_capacity_kw: float = Field(default=8.0, description="Entry point: system_capacity_kw")
    SolarBatteryDesign__solar_battery_plant__battery_system__battery_bos__cost_model__pack_count: float = Field(default=8.0, description="Entry point: pack_count")
    SolarBatteryDesign__solar_battery_plant__site_infra__electrical_panel__cost_model__circuit_count: float = Field(default=4.0, description="Entry point: circuit_count")
    SolarBatteryDesign__solar_battery_plant__site_infra__racking__cost_model__tilt_angle: float = Field(default=30.0, description="Entry point: tilt_angle")
    SolarBatteryDesign__solar_battery_plant__solar_array__array_bos__cost_model__panel_count: float = Field(default=20.0, description="Entry point: panel_count")
    SolarBatteryDesign__solar_battery_plant__battery_system__hybrid_inverter__cost_model__power_rating: float = Field(default=10000.0, description="Entry point: power_rating")
    SolarBatteryDesign__solar_battery_plant__solar_array__array_bos__cost_model__string_count: float = Field(default=4.0, description="Entry point: string_count")
    SolarBatteryDesign__solar_battery_plant__solar_array__pv_module__cost_model__efficiency: float = Field(default=0.21, description="Entry point: efficiency")
    SolarBatteryDesign__solar_battery_plant__solar_array__inverter__cost_model__power_rating: float = Field(default=2000.0, description="Entry point: power_rating")
    SolarBatteryDesign__solar_battery_plant__solar_array__pv_module__cost_model__wattage: float = Field(default=400.0, description="Entry point: wattage")
    SolarBatteryDesign__solar_battery_plant__battery_system__battery_pack__cost_model__chemistry_factor: float = Field(default=1.0, description="Entry point: chemistry_factor")
    SolarBatteryDesign__solar_battery_plant__solar_array__module_count: float = Field(default=20.0, description="Entry point: module_count")
    SolarBatteryDesign__solar_battery_plant__solar_array__inverter_count: float = Field(default=4.0, description="Entry point: inverter_count")
    SolarBatteryDesign__solar_battery_plant__battery_system__pack_count: float = Field(default=8.0, description="Entry point: pack_count")
    SolarBatteryDesign__solar_battery_plant__site_infra__raw_material_cost__permitting_raw_material_cost: float = Field(default=0.0, description="Entry point: permitting_raw_material_cost")
    SolarBatteryDesign__solar_battery_plant__site_infra__fabrication_cost__permitting_fabrication_cost: float = Field(default=0.0, description="Entry point: permitting_fabrication_cost")
    SolarBatteryDesign__solar_battery_plant__site_infra__installation_cost__permitting_installation_cost: float = Field(default=0.0, description="Entry point: permitting_installation_cost")

    model_config = {"frozen": True, "extra": "forbid"}
