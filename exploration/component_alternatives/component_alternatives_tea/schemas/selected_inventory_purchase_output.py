from pydantic import Field
from simkit.config.schema import MultiOutput

class Selected_Inventory_PurchaseOutput(MultiOutput):
    """Multi-output container for Selected_Inventory_Purchase.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

SysML Source: root-0/integrated_equipment_costs.sysml:3
    """
    purchased_quantity: float = Field(description="purchased_quantity output")
    source_budget: float = Field(description="source_budget output")
    quantity_ratio: float = Field(description="quantity_ratio output")
    capital: float = Field(description="capital output")
    extrapolated: float = Field(description="extrapolated output")
