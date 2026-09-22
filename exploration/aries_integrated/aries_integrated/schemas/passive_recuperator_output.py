from pydantic import Field
from simkit.config.schema import MultiOutput

class Passive_RecuperatorOutput(MultiOutput):
    """Multi-output container for Passive_Recuperator.

*Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: accepted WI-089 design and source/assumption register; generic passive recuperator. Normative equations, units and operating domains are in the named design sections; typed native completion enforces them. MW/K/MPa/kg/s/J per kg K/atoms per s as documented; dimensionless flags use 0/1. **Last Updated**: 2026-09-22.

SysML Source: root-0/integrated_heat_electricity.sysml:112
    """
    bypass_active: float = Field(description="bypass_active output")
    cold_out: float = Field(description="cold_out output")
    hot_out: float = Field(description="hot_out output")
    recovered_heat: float = Field(description="recovered_heat output")
