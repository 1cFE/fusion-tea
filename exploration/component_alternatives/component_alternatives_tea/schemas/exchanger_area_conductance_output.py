from pydantic import Field
from simkit.config.schema import MultiOutput

class Exchanger_Area_ConductanceOutput(MultiOutput):
    """Multi-output container for Exchanger_Area_Conductance.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

SysML Source: root-0/integrated_equipment_costs.sysml:16
    """
    area: float = Field(description="area output")
    ua: float = Field(description="ua output")
