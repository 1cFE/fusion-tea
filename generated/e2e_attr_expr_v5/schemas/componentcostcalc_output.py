from pydantic import Field
from simkit.config.schema import MultiOutput

class ComponentCostCalcOutput(MultiOutput):
    """Multi-output container for ComponentCostCalc.

SysML Source: models/tests/e2e_attr_expr/library.sysml:5
    """
    material_cost: float = Field(description="material_cost output")
    fab_cost: float = Field(description="fab_cost output")
    install_cost: float = Field(description="install_cost output")
    total_cost: float = Field(description="total_cost output")
    idiot_index: float = Field(description="idiot_index output")
