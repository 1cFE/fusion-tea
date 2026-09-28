from pydantic import Field
from simkit.config.schema import MultiOutput

class Fusion_Source_SelectorOutput(MultiOutput):
    """Multi-output container for Fusion_Source_Selector.

*Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: accepted WI-089 design and source/assumption register; generic fusion source selector. Normative equations, units and operating domains are in the named design sections; typed native completion enforces them. MW/K/MPa/kg/s/J per kg K/atoms per s as documented; dimensionless flags use 0/1. **Last Updated**: 2026-09-22.

SysML Source: root-0/integrated_heat_electricity.sysml:3
    """
    selected_power: float = Field(description="selected_power output")
    selected_mode: float = Field(description="selected_mode output")
