from pydantic import Field
from simkit.config.schema import MultiOutput

class Finite_Water_CoolerOutput(MultiOutput):
    """Multi-output container for Finite_Water_Cooler.

*Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. Numerical semantics are the complete calculate function in exploration/component_alternatives/bodies/component_alternatives_thermal/finite_water_cooler_impl.py; units MW, K/degC, kg/s, Pa, MW/K, USD2025 and years as named.

SysML Source: root-0/component_alternatives_thermal.sysml:84
    """
    min_gap: float = Field(description="min_gap output")
    power_margin: float = Field(description="power_margin output")
    duty_margin: float = Field(description="duty_margin output")
    water_inlet_after_C: float = Field(description="water_inlet_after_C output")
    water_flow: float = Field(description="water_flow output")
    required_ua: float = Field(description="required_ua output")
    flow_margin: float = Field(description="flow_margin output")
    ua_residual: float = Field(description="ua_residual output")
    bracket_high_ua: float = Field(description="bracket_high_ua output")
    pump_electric: float = Field(description="pump_electric output")
    total_rejection: float = Field(description="total_rejection output")
    bracket_low_ua: float = Field(description="bracket_low_ua output")
    energy_residual: float = Field(description="energy_residual output")
    evaluation_defined: float = Field(description="evaluation_defined output")
    water_outlet_C: float = Field(description="water_outlet_C output")
    iterations: float = Field(description="iterations output")
    failure_code: float = Field(description="failure_code output")
    duty: float = Field(description="duty output")
