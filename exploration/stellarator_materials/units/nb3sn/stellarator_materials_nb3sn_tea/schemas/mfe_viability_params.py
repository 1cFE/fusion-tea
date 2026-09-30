from pydantic import BaseModel, Field


class MfeViabilityParams(BaseModel):
    """Parameters from mfe_viability.

    Generated from SysML calculation definitions.
    """
    stellarator_09_materials__nb3sn_material__cryoplant__cold_stage_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__cryoplant__cryogenic_offered_conditions__enabled_in: bool = Field(default=1.0, description="Entry point: enabled_in")
    stellarator_09_materials__nb3sn_material__cryoplant__direct_electric_capability__applicable_in: bool = Field(default=1.0, description="Entry point: applicable_in")
    stellarator_09_materials__nb3sn_material__cryoplant__direct_electric_capability__conditions_supported_in: bool = Field(default=1.0, description="Entry point: conditions_supported_in")
    stellarator_09_materials__nb3sn_material__cryoplant__direct_electric_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__electric_plant__electric_gross_capability__applicable_in: bool = Field(default=1.0, description="Entry point: applicable_in")
    stellarator_09_materials__nb3sn_material__electric_plant__electric_gross_capability__conditions_supported_in: bool = Field(default=1.0, description="Entry point: conditions_supported_in")
    stellarator_09_materials__nb3sn_material__electric_plant__electric_gross_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__heat_rejection__water_electric_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__heat_rejection__water_flow_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__heat_rejection__water_head_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__heat_rejection__water_rejection_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__heat_transport__helium_electric_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__heat_transport__helium_flow_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__heat_transport__helium_pressure_rise_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__heat_transport__helium_pumping_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__heat_transport__salt_electric_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__heat_transport__salt_flow_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__heat_transport__salt_head_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__heat_transport__salt_shaft_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__power_supplies__magnet_pf_electric_capability__applicable_in: bool = Field(default=1.0, description="Entry point: applicable_in")
    stellarator_09_materials__nb3sn_material__power_supplies__magnet_pf_electric_capability__conditions_supported_in: bool = Field(default=1.0, description="Entry point: conditions_supported_in")
    stellarator_09_materials__nb3sn_material__power_supplies__magnet_pf_electric_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__power_supplies__magnet_tf_electric_capability__applicable_in: bool = Field(default=1.0, description="Entry point: applicable_in")
    stellarator_09_materials__nb3sn_material__power_supplies__magnet_tf_electric_capability__conditions_supported_in: bool = Field(default=1.0, description="Entry point: conditions_supported_in")
    stellarator_09_materials__nb3sn_material__power_supplies__magnet_tf_electric_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__turbine__condensate_electric_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__turbine__condensate_flow_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__turbine__condensate_pressure_rise_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__turbine__condenser_rejection_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__turbine__feedwater_electric_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__turbine__feedwater_flow_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__turbine__feedwater_pressure_rise_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__turbine__hp_flow_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__turbine__hp_shaft_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__turbine__lp_flow_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__turbine__lp_shaft_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")
    stellarator_09_materials__nb3sn_material__turbine__turbine_gross_capability__applicable_in: bool = Field(default=1.0, description="Entry point: applicable_in")
    stellarator_09_materials__nb3sn_material__turbine__turbine_gross_capability__conditions_supported_in: bool = Field(default=1.0, description="Entry point: conditions_supported_in")
    stellarator_09_materials__nb3sn_material__turbine__turbine_gross_capability__demand_available_in: bool = Field(default=1.0, description="Entry point: demand_available_in")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
