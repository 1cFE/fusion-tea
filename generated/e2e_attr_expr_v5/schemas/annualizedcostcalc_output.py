from pydantic import Field
from simkit.config.schema import MultiOutput

class AnnualizedCostCalcOutput(MultiOutput):
    """Multi-output container for AnnualizedCostCalc.

SysML Source: models/tests/e2e_attr_expr/library.sysml:19
    """
    crf: float = Field(description="crf output")
    annualized_cost: float = Field(description="annualized_cost output")
