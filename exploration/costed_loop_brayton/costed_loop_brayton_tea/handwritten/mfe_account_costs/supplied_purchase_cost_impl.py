"""WI-079 supplied amount; source contract is design.md, not a price prediction."""
from __future__ import annotations

import math

AUTO_IMPLEMENTED = False


def calculate(purchase_cost_in: float, n_mod_in: float) -> float:
    for name, value in [('purchase_cost_in', purchase_cost_in), ('n_mod_in', n_mod_in)]:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
            raise ValueError(f'{name} must be a finite nonnegative number')
    if n_mod_in != 1.0:
        raise ValueError('Supplied package accounts support one module only')
    return purchase_cost_in * n_mod_in


def run_supplied_purchase_cost(inputs: Supplied_Purchase_CostInput) -> float:
    return calculate(inputs.purchase_cost_in, inputs.n_mod_in)
