from pydantic import BaseModel, Field


class NominalBraytonParams(BaseModel):
    """Parameters from nominal_brayton.

    Generated from SysML calculation definitions.
    """
    aries_nominal_brayton__compressor_1__efficiency: float = Field(default=0.89, description="Entry point: efficiency")
    aries_nominal_brayton__compressor_1__selected_ratio: float = Field(default=1.5182944859378311, description="Entry point: selected_ratio")
    aries_nominal_brayton__compressor_2__efficiency: float = Field(default=0.89, description="Entry point: efficiency")
    aries_nominal_brayton__compressor_2__selected_ratio: float = Field(default=1.5182944859378311, description="Entry point: selected_ratio")
    aries_nominal_brayton__compressor_3__efficiency: float = Field(default=0.89, description="Entry point: efficiency")
    aries_nominal_brayton__compressor_3__selected_ratio: float = Field(default=1.5182944859378311, description="Entry point: selected_ratio")
    aries_nominal_brayton__compressor_capacity__assumed_supported: bool = Field(default=1.0, description="Entry point: assumed_supported")
    aries_nominal_brayton__compressor_capacity__demand_available: bool = Field(default=1.0, description="Entry point: demand_available")
    aries_nominal_brayton__compressor_capacity__offered_rating: float = Field(default=1100.0, description="Entry point: offered_rating")
    aries_nominal_brayton__compressor_capacity__scenario_applicable: bool = Field(default=1.0, description="Entry point: scenario_applicable")
    aries_nominal_brayton__equivalent_turbine__efficiency: float = Field(default=0.93, description="Entry point: efficiency")
    aries_nominal_brayton__heater__heating_role: float = Field(default=1.0, description="Entry point: heating_role")
    aries_nominal_brayton__heater_capacity__assumed_supported: bool = Field(default=1.0, description="Entry point: assumed_supported")
    aries_nominal_brayton__heater_capacity__demand_available: bool = Field(default=1.0, description="Entry point: demand_available")
    aries_nominal_brayton__heater_capacity__offered_rating: float = Field(default=2000.0, description="Entry point: offered_rating")
    aries_nominal_brayton__heater_capacity__scenario_applicable: bool = Field(default=1.0, description="Entry point: scenario_applicable")
    aries_nominal_brayton__hot_side_loss__loss_fraction: float = Field(default=0.045, description="Entry point: loss_fraction")
    aries_nominal_brayton__intercooler_1__heating_role: float = Field(default=0.0, description="Entry point: heating_role")
    aries_nominal_brayton__intercooler_1__target_temperature: float = Field(default=308.15, description="Entry point: target_temperature")
    aries_nominal_brayton__intercooler_2__heating_role: float = Field(default=0.0, description="Entry point: heating_role")
    aries_nominal_brayton__intercooler_2__target_temperature: float = Field(default=308.15, description="Entry point: target_temperature")
    aries_nominal_brayton__operating_point__cp: float = Field(default=5193.0, description="Entry point: cp")
    aries_nominal_brayton__operating_point__gamma: float = Field(default=1.6666666666666667, description="Entry point: gamma")
    aries_nominal_brayton__operating_point__low_temperature: float = Field(default=308.15, description="Entry point: low_temperature")
    aries_nominal_brayton__operating_point__return_pressure: float = Field(default=4.285714285714286, description="Entry point: return_pressure")
    aries_nominal_brayton__operating_point__selected_flow: float = Field(default=1000.0, description="Entry point: selected_flow")
    aries_nominal_brayton__operating_point__turbine_temperature: float = Field(default=980.15, description="Entry point: turbine_temperature")
    aries_nominal_brayton__precooler__heating_role: float = Field(default=0.0, description="Entry point: heating_role")
    aries_nominal_brayton__recuperator__effectiveness: float = Field(default=0.95, description="Entry point: effectiveness")
    aries_nominal_brayton__rejection_capacity__assumed_supported: bool = Field(default=1.0, description="Entry point: assumed_supported")
    aries_nominal_brayton__rejection_capacity__demand_available: bool = Field(default=1.0, description="Entry point: demand_available")
    aries_nominal_brayton__rejection_capacity__offered_rating: float = Field(default=1200.0, description="Entry point: offered_rating")
    aries_nominal_brayton__rejection_capacity__scenario_applicable: bool = Field(default=1.0, description="Entry point: scenario_applicable")

    model_config = {"frozen": True, "extra": "forbid", "populate_by_name": True}
