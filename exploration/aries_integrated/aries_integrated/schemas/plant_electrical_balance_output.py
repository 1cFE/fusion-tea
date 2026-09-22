from pydantic import Field
from simkit.config.schema import MultiOutput

class Plant_Electrical_BalanceOutput(MultiOutput):
    """Multi-output container for Plant_Electrical_Balance.

*Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: generator/auxiliary owner and electrical energy ledger equations; efficiencies dimensionless, rates atoms/s, all powers MW. **Last Updated**: 2026-09-22.

SysML Source: root-0/integrated_heat_electricity.sysml:124
    """
    fuel_base_electric: float = Field(description="fuel_base_electric output")
    other_electric_demand: float = Field(description="other_electric_demand output")
    dissipated_auxiliary: float = Field(description="dissipated_auxiliary output")
    net_electric: float = Field(description="net_electric output")
    generator_loss: float = Field(description="generator_loss output")
    net_shaft: float = Field(description="net_shaft output")
    heating_electric: float = Field(description="heating_electric output")
    cryo_electric: float = Field(description="cryo_electric output")
    fuel_variable_electric: float = Field(description="fuel_variable_electric output")
    compressor_demand: float = Field(description="compressor_demand output")
    auxiliary_electric: float = Field(description="auxiliary_electric output")
    gross_electric: float = Field(description="gross_electric output")
    fuel_electric: float = Field(description="fuel_electric output")
    primary_pump_electric: float = Field(description="primary_pump_electric output")
    motor_loss: float = Field(description="motor_loss output")
    shaft_import: float = Field(description="shaft_import output")
    heating_loss: float = Field(description="heating_loss output")
    pump_loss: float = Field(description="pump_loss output")
    control_electric: float = Field(description="control_electric output")
