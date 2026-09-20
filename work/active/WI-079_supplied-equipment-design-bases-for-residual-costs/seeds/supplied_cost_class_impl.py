"""WI-079 preserves chosen procurement class with a native domain guard."""
from __future__ import annotations

import math

AUTO_IMPLEMENTED = False


def calculate(class_in: float) -> float:
    if isinstance(class_in, bool) or not isinstance(class_in, (int, float)) or not math.isfinite(class_in) or class_in < 0:
        raise ValueError('Selected procurement class must be a finite nonnegative number')
    return class_in


def run_supplied_cost_class(inputs: Supplied_Cost_ClassInput) -> float:
    return calculate(inputs.class_in)
