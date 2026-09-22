from pydantic import Field
from simkit.config.schema import MultiOutput

class Annual_Selected_FuelOutput(MultiOutput):
    """Multi-output container for Annual_Selected_Fuel.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

SysML Source: root-0/integrated_equipment_costs.sysml:44
    """
    annual_loss: float = Field(description="annual_loss output")
    annual_cost: float = Field(description="annual_cost output")
    annual_burn: float = Field(description="annual_burn output")
    annual_recovery: float = Field(description="annual_recovery output")
    annual_decay: float = Field(description="annual_decay output")
    annual_external: float = Field(description="annual_external output")
    required_stock: float = Field(description="required_stock output")
    breeding_supported: float = Field(description="breeding_supported output")
