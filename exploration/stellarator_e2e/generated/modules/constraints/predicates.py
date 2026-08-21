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

# definition:mfe_viability::'Economic Recirculating Threshold'
def constraint_pred_definition_mfe_viability__economic_recirculating_threshold(rec_frac, threshold):
    value = _cmp('<=', rec_frac, threshold)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((threshold - rec_frac)) if (_fin(rec_frac) and _fin(threshold)) else None))

# definition:mfe_viability::'Beta Limit'
def constraint_pred_definition_mfe_viability__beta_limit(beta_in, beta_limit_in):
    value = _cmp('<=', beta_in, beta_limit_in)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((beta_limit_in - beta_in)) if (_fin(beta_in) and _fin(beta_limit_in)) else None))

# definition:mfe_viability::'Net Power Positive'
def constraint_pred_definition_mfe_viability__net_power_positive(net_electric):
    value = _cmp('>', net_electric, 0.0)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((net_electric - 0.0)) if (_fin(net_electric) and _fin(0.0)) else None))

# definition:mfe_viability::'Neutron Wall Load Limit'
def constraint_pred_definition_mfe_viability__neutron_wall_load_limit(wall_load, wall_load_limit_in):
    value = _cmp('<=', wall_load, wall_load_limit_in)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((wall_load_limit_in - wall_load)) if (_fin(wall_load) and _fin(wall_load_limit_in)) else None))

# definition:mfe_viability::'TBR Floor'
def constraint_pred_definition_mfe_viability__tbr_floor(tbr_in, tbr_floor_in):
    value = _cmp('>=', tbr_in, tbr_floor_in)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((tbr_in - tbr_floor_in)) if (_fin(tbr_in) and _fin(tbr_floor_in)) else None))
