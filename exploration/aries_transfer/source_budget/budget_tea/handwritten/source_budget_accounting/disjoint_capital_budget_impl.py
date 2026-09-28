"""Guarded eight-account budget; accounts are assumed disjoint by the design."""
import math
AUTO_IMPLEMENTED = False

def run_disjoint_capital_budget(inputs):
    from budget_tea.schemas.disjoint_capital_budget_output import Disjoint_Capital_BudgetOutput
    for name,value in inputs.model_dump().items():
        if not math.isfinite(value):raise ValueError(name+' must be finite')
        if name!='inclusive_multiplier_in' and value<0:raise ValueError(name+' cost must be nonnegative')
    if inputs.inclusive_multiplier_in<=0:raise ValueError('inclusive multiplier must be positive')
    direct=sum(getattr(inputs,f'account_{i}_in') for i in range(1,9))
    capital=direct*inputs.inclusive_multiplier_in
    result=dict(direct_total=direct,inclusive_capital=capital,inclusive_addition=capital-direct)
    if not all(math.isfinite(v) for v in result.values()):raise ValueError('nonfinite budget output')
    return tuple(result[name] for name in Disjoint_Capital_BudgetOutput.model_fields)
