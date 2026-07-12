from pydantic import BaseModel, Field


class LibraryParams(BaseModel):
    """Parameters from library.sysml.

    Generated from SysML calculation definitions.
    """
    SolarBatteryDesign__solar_battery_plant__solar_array__allocation_model__child_count: float = Field(default=25.0, description="Entry point: child_count")
    SolarBatteryDesign__solar_battery_plant__solar_array__allocation_model__total_child_mass: float = Field(default=50.0, description="Entry point: total_child_mass")
    SolarBatteryDesign__solar_battery_plant__solar_array__pv_module__cost_model__cost_per_watt: float = Field(default=1.07, description="Entry point: cost_per_watt")
    SolarBatteryDesign__solar_battery_plant__solar_array__pv_module__cost_model__fab_factor: float = Field(default=0.45, description="Entry point: fab_factor")
    SolarBatteryDesign__solar_battery_plant__solar_array__pv_module__cost_model__install_factor: float = Field(default=0.3, description="Entry point: install_factor")
    SolarBatteryDesign__solar_battery_plant__solar_array__inverter__cost_model__cost_per_watt: float = Field(default=0.286, description="Entry point: cost_per_watt")
    SolarBatteryDesign__solar_battery_plant__solar_array__inverter__cost_model__fab_factor: float = Field(default=0.45, description="Entry point: fab_factor")
    SolarBatteryDesign__solar_battery_plant__solar_array__inverter__cost_model__install_factor: float = Field(default=0.3, description="Entry point: install_factor")
    SolarBatteryDesign__solar_battery_plant__solar_array__array_bos__cost_model__cost_per_panel_bos: float = Field(default=30.0, description="Entry point: cost_per_panel_bos")
    SolarBatteryDesign__solar_battery_plant__solar_array__array_bos__cost_model__cost_per_string: float = Field(default=150.0, description="Entry point: cost_per_string")
    SolarBatteryDesign__solar_battery_plant__solar_array__array_bos__cost_model__fab_factor: float = Field(default=0.45, description="Entry point: fab_factor")
    SolarBatteryDesign__solar_battery_plant__solar_array__array_bos__cost_model__install_factor: float = Field(default=0.3, description="Entry point: install_factor")
    SolarBatteryDesign__solar_battery_plant__battery_system__battery_pack__cost_model__cost_per_kwh: float = Field(default=171.5, description="Entry point: cost_per_kwh")
    SolarBatteryDesign__solar_battery_plant__battery_system__battery_pack__cost_model__fab_factor: float = Field(default=0.45, description="Entry point: fab_factor")
    SolarBatteryDesign__solar_battery_plant__battery_system__battery_pack__cost_model__install_factor: float = Field(default=0.3, description="Entry point: install_factor")
    SolarBatteryDesign__solar_battery_plant__battery_system__hybrid_inverter__cost_model__cost_per_watt: float = Field(default=0.1714, description="Entry point: cost_per_watt")
    SolarBatteryDesign__solar_battery_plant__battery_system__hybrid_inverter__cost_model__fab_factor: float = Field(default=0.45, description="Entry point: fab_factor")
    SolarBatteryDesign__solar_battery_plant__battery_system__hybrid_inverter__cost_model__install_factor: float = Field(default=0.3, description="Entry point: install_factor")
    SolarBatteryDesign__solar_battery_plant__battery_system__battery_bos__cost_model__cost_per_pack_bos: float = Field(default=71.5, description="Entry point: cost_per_pack_bos")
    SolarBatteryDesign__solar_battery_plant__battery_system__battery_bos__cost_model__fab_factor: float = Field(default=0.45, description="Entry point: fab_factor")
    SolarBatteryDesign__solar_battery_plant__battery_system__battery_bos__cost_model__install_factor: float = Field(default=0.3, description="Entry point: install_factor")
    SolarBatteryDesign__solar_battery_plant__site_infra__racking__cost_model__cost_per_panel_rack: float = Field(default=57.0, description="Entry point: cost_per_panel_rack")
    SolarBatteryDesign__solar_battery_plant__site_infra__racking__cost_model__fab_factor: float = Field(default=0.45, description="Entry point: fab_factor")
    SolarBatteryDesign__solar_battery_plant__site_infra__racking__cost_model__install_factor: float = Field(default=0.3, description="Entry point: install_factor")
    SolarBatteryDesign__solar_battery_plant__site_infra__electrical_panel__cost_model__base_cost: float = Field(default=150.0, description="Entry point: base_cost")
    SolarBatteryDesign__solar_battery_plant__site_infra__electrical_panel__cost_model__cost_per_circuit: float = Field(default=34.0, description="Entry point: cost_per_circuit")
    SolarBatteryDesign__solar_battery_plant__site_infra__electrical_panel__cost_model__fab_factor: float = Field(default=0.45, description="Entry point: fab_factor")
    SolarBatteryDesign__solar_battery_plant__site_infra__electrical_panel__cost_model__install_factor: float = Field(default=0.3, description="Entry point: install_factor")
    SolarBatteryDesign__solar_battery_plant__site_infra__permitting__cost_model__cost_per_kw: float = Field(default=187.5, description="Entry point: cost_per_kw")
    SolarBatteryDesign__solar_battery_plant__solar_array__allocation_model__fastener_cost_per_child: float = Field(default=0.5, description="Entry point: fastener_cost_per_child")
    SolarBatteryDesign__solar_battery_plant__solar_array__allocation_model__seal_cost_per_child: float = Field(default=0.3, description="Entry point: seal_cost_per_child")
    SolarBatteryDesign__solar_battery_plant__solar_array__allocation_model__wiring_cost_per_kg: float = Field(default=2.0, description="Entry point: wiring_cost_per_kg")

    model_config = {"frozen": True, "extra": "forbid"}
