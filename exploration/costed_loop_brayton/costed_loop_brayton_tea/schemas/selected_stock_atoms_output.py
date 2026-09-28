from pydantic import Field
from simkit.config.schema import MultiOutput

class Selected_Stock_AtomsOutput(MultiOutput):
    """Multi-output container for Selected_Stock_Atoms.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

SysML Source: root-0/integrated_equipment_costs.sysml:37
    """
    stock_kg: float = Field(description="stock_kg output")
    atoms: float = Field(description="atoms output")
