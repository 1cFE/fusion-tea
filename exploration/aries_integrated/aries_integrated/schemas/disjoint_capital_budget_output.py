from pydantic import Field
from simkit.config.schema import MultiOutput

class Disjoint_Capital_BudgetOutput(MultiOutput):
    """Multi-output container for Disjoint_Capital_Budget.

Source: work/active/WI-088_aries-source-budget-cost-contribution/spec.md. Ref: accepted financial scope and Lyon Eq7/account mapping. Basis: AGENT generic disjoint-budget accounting and explicit period convention. direct_total=sum(account1..8); inclusive_capital=direct_total*inclusive_multiplier; inclusive_addition=inclusive_capital-direct_total. Dollars, supplied disjoint scope and inclusive multiplier; not a price/financing prediction. Native guard rejects nonfinite/negative budgets, nonpositive multiplier/period/power, mode outside0/1, availability outside(0,1], overflow and zero energy. Last Updated: 2026-09-21.

SysML Source: root-0/source_budget_accounting.sysml:3
    """
    direct_total: float = Field(description="direct_total output")
    inclusive_addition: float = Field(description="inclusive_addition output")
    inclusive_capital: float = Field(description="inclusive_capital output")
