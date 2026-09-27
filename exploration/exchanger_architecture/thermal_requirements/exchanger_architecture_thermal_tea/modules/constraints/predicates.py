"""Compiled Kleene predicates (Item 7 / D2/D3) — one function per constraint definition.

Compile-once, class-per-assertion (INV-1): every constraint module instantiated from the same
source assertion imports its function from here rather than duplicating the compiled predicate.
"""

import math
from typing import NamedTuple


class _PredicateResult(NamedTuple):
    actual_value: object  # True/False/None (None = indeterminate)
    status: str           # satisfied | violated | indeterminate
    margin: object         # signed float or None (simple-inequality roots only)


class _PredicateBodyResult(NamedTuple):
    actual_value: object
    source_margin: object


def _finalize_assertion(body, *, is_negated, expected_value):
    if type(is_negated) is not bool or type(expected_value) is not bool:
        raise ValueError("assertion finalization requires Boolean polarity fields")
    if expected_value is not (not is_negated):
        raise ValueError("assertion polarity fields must be complementary")
    if body.actual_value is None:
        return _PredicateResult(None, "indeterminate", None)
    status = "satisfied" if body.actual_value == expected_value else "violated"
    margin = body.source_margin
    if margin is not None:
        margin = -margin if is_negated else margin
        if margin == 0:
            margin = 0.0
    return _PredicateResult(body.actual_value, status, margin)


def _fin(x):
    return isinstance(x, (int, float)) and math.isfinite(x)


def _cmp(op, a, b):
    """Leaf comparison: unknown (None) if either operand is non-finite."""
    if not _fin(a) or not _fin(b):
        return None
    if op == "<=": return a <= b
    if op == ">=": return a >= b
    if op == "<":  return a < b
    if op == ">":  return a > b
    raise ValueError(f"not a comparison: {op}")


def _and(*vals):
    if any(v is False for v in vals): return False
    if any(v is None for v in vals): return None
    return True


def _or(*vals):
    if any(v is True for v in vals): return True
    if any(v is None for v in vals): return None
    return False


def _not(v):
    return None if v is None else (not v)


def _norm0(x):
    """Normalize an exact-boundary signed zero (-0.0) to 0.0 (`[HARD]`)."""
    return 0.0 if x == 0.0 else x

# definition:mfe_viability::'Offered Equipment Capacity'
def constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in, margin_in):
    value = _and(_cmp('>=', defined_in, 1.0), _cmp('>=', margin_in, 0.0))
    return _PredicateBodyResult(actual_value=value, source_margin=None)

# definition:controlled_exchanger_closure::'Thermal Return Held'
def constraint_pred_definition_controlled_exchanger_closure__thermal_return_held(residual_magnitude_in, tolerance_in):
    value = _cmp('<=', residual_magnitude_in, tolerance_in)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((tolerance_in - residual_magnitude_in)) if (_fin(residual_magnitude_in) and _fin(tolerance_in)) else None))

# definition:controlled_exchanger_closure::'Thermal Nonnegative Margin'
def constraint_pred_definition_controlled_exchanger_closure__thermal_nonnegative_margin(margin_in):
    value = _cmp('>=', margin_in, 0.0)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((margin_in - 0.0)) if (_fin(margin_in) and _fin(0.0)) else None))

# definition:controlled_exchanger_closure::'Thermal State Defined'
def constraint_pred_definition_controlled_exchanger_closure__thermal_state_defined(defined_in):
    value = _cmp('>=', defined_in, 1.0)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((defined_in - 1.0)) if (_fin(defined_in) and _fin(1.0)) else None))

# definition:integrated_heat_electricity::'Heat Removal Adequate'
def constraint_pred_definition_integrated_heat_electricity__heat_removal_adequate(unmet_in, tolerance_in):
    value = _cmp('<=', unmet_in, tolerance_in)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((tolerance_in - unmet_in)) if (_fin(unmet_in) and _fin(tolerance_in)) else None))

# definition:integrated_heat_electricity::'Integrated Ledger Balanced'
def constraint_pred_definition_integrated_heat_electricity__integrated_ledger_balanced(magnitude_in, tolerance_in):
    value = _cmp('<=', magnitude_in, tolerance_in)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((tolerance_in - magnitude_in)) if (_fin(magnitude_in) and _fin(tolerance_in)) else None))
