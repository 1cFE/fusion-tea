from pydantic import Field
from simkit.config.schema import MultiOutput

class Integrated_Heat_SourceOutput(MultiOutput):
    """Multi-output container for Integrated_Heat_Source.

*Source**: work/active/WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: accepted WI-089 design and source/assumption register; generic integrated heat source. Normative equations, units and operating domains are in the named design sections; typed native completion enforces them. MW/K/MPa/kg/s/J per kg K/atoms per s as documented; dimensionless flags use 0/1. **Last Updated**: 2026-09-22.

SysML Source: root-0/integrated_heat_electricity.sysml:11
    """
    divertor_deposition: float = Field(description="divertor_deposition output")
    topology_zero: float = Field(description="topology_zero output")
    pump_electric: float = Field(description="pump_electric output")
    neutron_power: float = Field(description="neutron_power output")
    charged_power: float = Field(description="charged_power output")
    pbli_friction: float = Field(description="pbli_friction output")
    other_heat: float = Field(description="other_heat output")
    nuclear_gain: float = Field(description="nuclear_gain output")
    he_deposition: float = Field(description="he_deposition output")
    source_residual: float = Field(description="source_residual output")
    he_friction: float = Field(description="he_friction output")
    exchange: float = Field(description="exchange output")
    pump_recovered: float = Field(description="pump_recovered output")
    pbli_deposition: float = Field(description="pbli_deposition output")
    divertor_friction: float = Field(description="divertor_friction output")
