from pydantic import Field
from simkit.config.schema import MultiOutput

class Controlled_Conversion_BoundaryOutput(MultiOutput):
    """Multi-output container for Controlled_Conversion_Boundary.

*Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. Numerical semantics are the complete calculate function in exploration/component_alternatives/bodies/component_alternatives_thermal/controlled_conversion_boundary_impl.py; units MW, K/degC, kg/s, Pa, MW/K, USD2025 and years as named.

SysML Source: root-0/component_alternatives_thermal.sysml:123
    """
    salt_hot: float = Field(description="salt_hot output")
    salt_return: float = Field(description="salt_return output")
    bypass_fraction_margin: float = Field(description="bypass_fraction_margin output")
    steam_heat: float = Field(description="steam_heat output")
    source_adequate: float = Field(description="source_adequate output")
    temperature_margin: float = Field(description="temperature_margin output")
    added_dp: float = Field(description="added_dp output")
    added_dp_margin: float = Field(description="added_dp_margin output")
    bypass_flow: float = Field(description="bypass_flow output")
    salt_motor_loss: float = Field(description="salt_motor_loss output")
    converged: float = Field(description="converged output")
    duty_correction: float = Field(description="duty_correction output")
    pressure_margin: float = Field(description="pressure_margin output")
    actual_heat: float = Field(description="actual_heat output")
    raw_return_residual: float = Field(description="raw_return_residual output")
    controller_capacity_ok: float = Field(description="controller_capacity_ok output")
    motor_import_loss: float = Field(description="motor_import_loss output")
    exchanger_flow_margin: float = Field(description="exchanger_flow_margin output")
    bypass_flow_margin: float = Field(description="bypass_flow_margin output")
    total_flow_margin: float = Field(description="total_flow_margin output")
    rejection_load: float = Field(description="rejection_load output")
    raw_heat_residual: float = Field(description="raw_heat_residual output")
    unremoved_heat: float = Field(description="unremoved_heat output")
    generator_loss: float = Field(description="generator_loss output")
