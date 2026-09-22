from pydantic import Field
from simkit.config.schema import MultiOutput

class Heat_Driven_ClosureOutput(MultiOutput):
    """Multi-output container for Heat_Driven_Closure.

*Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: accepted WI-089 design and source/assumption register; generic heat driven closure. Normative equations, units and operating domains are in the named design sections; typed native completion enforces them. MW/K/MPa/kg/s/J per kg K/atoms per s as documented; dimensionless flags use 0/1. **Last Updated**: 2026-09-22.

SysML Source: root-0/integrated_heat_electricity.sysml:46
    """
    he_return: float = Field(description="he_return output")
    he_unmet: float = Field(description="he_unmet output")
    turbine_temperature: float = Field(description="turbine_temperature output")
    he_hot: float = Field(description="he_hot output")
    accepted_heat: float = Field(description="accepted_heat output")
    divertor_return: float = Field(description="divertor_return output")
    divertor_transferred: float = Field(description="divertor_transferred output")
    he_secondary_in: float = Field(description="he_secondary_in output")
    divertor_unmet: float = Field(description="divertor_unmet output")
    he_state_defined: float = Field(description="he_state_defined output")
    divertor_hot_terminal_difference: float = Field(description="divertor_hot_terminal_difference output")
    pbli_hot: float = Field(description="pbli_hot output")
    he_capability: float = Field(description="he_capability output")
    divertor_cold_terminal_difference: float = Field(description="divertor_cold_terminal_difference output")
    unmet_heat: float = Field(description="unmet_heat output")
    iterations: float = Field(description="iterations output")
    he_secondary_out: float = Field(description="he_secondary_out output")
    pbli_return: float = Field(description="pbli_return output")
    pbli_capability: float = Field(description="pbli_capability output")
    pbli_unmet: float = Field(description="pbli_unmet output")
    divertor_secondary_in: float = Field(description="divertor_secondary_in output")
    divertor_hot_bound_margin: float = Field(description="divertor_hot_bound_margin output")
    pbli_secondary_out: float = Field(description="pbli_secondary_out output")
    divertor_state_defined: float = Field(description="divertor_state_defined output")
    pbli_transferred: float = Field(description="pbli_transferred output")
    he_hot_bound_margin: float = Field(description="he_hot_bound_margin output")
    divertor_capability: float = Field(description="divertor_capability output")
    pbli_secondary_in: float = Field(description="pbli_secondary_in output")
    heater_inlet: float = Field(description="heater_inlet output")
    closure_residual: float = Field(description="closure_residual output")
    he_hot_terminal_difference: float = Field(description="he_hot_terminal_difference output")
    pbli_hot_bound_margin: float = Field(description="pbli_hot_bound_margin output")
    pbli_hot_terminal_difference: float = Field(description="pbli_hot_terminal_difference output")
    divertor_hot: float = Field(description="divertor_hot output")
    pbli_state_defined: float = Field(description="pbli_state_defined output")
    divertor_secondary_out: float = Field(description="divertor_secondary_out output")
    he_transferred: float = Field(description="he_transferred output")
    pbli_cold_terminal_difference: float = Field(description="pbli_cold_terminal_difference output")
    he_cold_terminal_difference: float = Field(description="he_cold_terminal_difference output")
    expansion_factor: float = Field(description="expansion_factor output")
