from pydantic import Field
from simkit.config.schema import MultiOutput

class Selected_Flow_PumpOutput(MultiOutput):
    """Multi-output container for Selected_Flow_Pump.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

SysML Source: root-0/integrated_equipment_costs.sysml:23
    """
    electric: float = Field(description="electric output")
    operating_flow: float = Field(description="operating_flow output")
    mode: float = Field(description="mode output")
    hydraulic_supported: float = Field(description="hydraulic_supported output")
