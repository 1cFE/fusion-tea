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

# definition:component_alternatives_thermal::'Nonnegative Margin'
def constraint_pred_definition_component_alternatives_thermal__nonnegative_margin(margin_in):
    value = _cmp('>=', margin_in, 0.0)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((margin_in - 0.0)) if (_fin(margin_in) and _fin(0.0)) else None))

# definition:component_alternatives_thermal::'Required Flag'
def constraint_pred_definition_component_alternatives_thermal__required_flag(flag_in):
    value = _cmp('>=', flag_in, 1.0)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((flag_in - 1.0)) if (_fin(flag_in) and _fin(1.0)) else None))

# definition:whole_plant_conversion_accounts::'Whole Plant Supported'
def constraint_pred_definition_whole_plant_conversion_accounts__whole_plant_supported(metric_in):
    value = _cmp('>=', metric_in, 1.0)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((metric_in - 1.0)) if (_fin(metric_in) and _fin(1.0)) else None))

# definition:mfe_viability::'Loop Pressure Margin'
def constraint_pred_definition_mfe_viability__loop_pressure_margin(p_loop_margin_in):
    value = _cmp('>', p_loop_margin_in, 0.0)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((p_loop_margin_in - 0.0)) if (_fin(p_loop_margin_in) and _fin(0.0)) else None))

# definition:mfe_viability::'Loop Capacity'
def constraint_pred_definition_mfe_viability__loop_capacity(mdot_loop_in, mdot_loop_rated_in):
    value = _cmp('<=', mdot_loop_in, mdot_loop_rated_in)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((mdot_loop_rated_in - mdot_loop_in)) if (_fin(mdot_loop_in) and _fin(mdot_loop_rated_in)) else None))

# definition:whole_plant_conversion_accounts::'Whole Plant Positive'
def constraint_pred_definition_whole_plant_conversion_accounts__whole_plant_positive(metric_in):
    value = _cmp('>', metric_in, 0.0)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((metric_in - 0.0)) if (_fin(metric_in) and _fin(0.0)) else None))

# definition:whole_plant_conversion_accounts::'Whole Plant Nonnegative'
def constraint_pred_definition_whole_plant_conversion_accounts__whole_plant_nonnegative(metric_in):
    value = _cmp('>=', metric_in, 0.0)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((metric_in - 0.0)) if (_fin(metric_in) and _fin(0.0)) else None))

# definition:component_alternatives_thermal::'Numerical Residual'
def constraint_pred_definition_component_alternatives_thermal__numerical_residual(residual_in, tolerance_in):
    value = _cmp('<=', residual_in, tolerance_in)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((tolerance_in - residual_in)) if (_fin(residual_in) and _fin(tolerance_in)) else None))

# definition:mfe_viability::'Net Power Positive'
def constraint_pred_definition_mfe_viability__net_power_positive(net_electric):
    value = _cmp('>', net_electric, 0.0)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((net_electric - 0.0)) if (_fin(net_electric) and _fin(0.0)) else None))
