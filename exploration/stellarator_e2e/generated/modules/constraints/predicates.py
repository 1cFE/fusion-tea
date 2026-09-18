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

# definition:mfe_viability::'Winding Pack Stress Limit'
def constraint_pred_definition_mfe_viability__winding_pack_stress_limit(sigma_in, sigma_allow_in):
    value = _cmp('<=', sigma_in, sigma_allow_in)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((sigma_allow_in - sigma_in)) if (_fin(sigma_in) and _fin(sigma_allow_in)) else None))

# definition:mfe_viability::'Conductor Strain Limit'
def constraint_pred_definition_mfe_viability__conductor_strain_limit(eps_cond, eps_cond_allow_in):
    value = _cmp('<=', eps_cond, eps_cond_allow_in)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((eps_cond_allow_in - eps_cond)) if (_fin(eps_cond) and _fin(eps_cond_allow_in)) else None))

# definition:mfe_viability::'Economic Recirculating Threshold'
def constraint_pred_definition_mfe_viability__economic_recirculating_threshold(rec_frac, threshold):
    value = _cmp('<=', rec_frac, threshold)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((threshold - rec_frac)) if (_fin(rec_frac) and _fin(threshold)) else None))

# definition:mfe_viability::'Cycle Fit Domain'
def constraint_pred_definition_mfe_viability__cycle_fit_domain(domain_product_in):
    value = _cmp('>=', domain_product_in, 0.0)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((domain_product_in - 0.0)) if (_fin(domain_product_in) and _fin(0.0)) else None))

# definition:mfe_viability::'Beta Limit'
def constraint_pred_definition_mfe_viability__beta_limit(beta_in, beta_limit_in):
    value = _cmp('<=', beta_in, beta_limit_in)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((beta_limit_in - beta_in)) if (_fin(beta_in) and _fin(beta_limit_in)) else None))

# definition:mfe_heating_chain::'Heating Efficiency Positive'
def constraint_pred_definition_mfe_heating_chain__heating_efficiency_positive(efficiency):
    value = _cmp('>', efficiency, 0.0)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((efficiency - 0.0)) if (_fin(efficiency) and _fin(0.0)) else None))

# definition:mfe_viability::'Divertor Target Heat Limit'
def constraint_pred_definition_mfe_viability__divertor_target_heat_limit(q_target_peak_in, q_target_limit_in):
    value = _cmp('<=', q_target_peak_in, q_target_limit_in)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((q_target_limit_in - q_target_peak_in)) if (_fin(q_target_peak_in) and _fin(q_target_limit_in)) else None))

# definition:mfe_heating_chain::'Heating Efficiency Upper'
def constraint_pred_definition_mfe_heating_chain__heating_efficiency_upper(efficiency):
    value = _cmp('<=', efficiency, 1.0)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((1.0 - efficiency)) if (_fin(efficiency) and _fin(1.0)) else None))

# definition:mfe_viability::'Net Power Positive'
def constraint_pred_definition_mfe_viability__net_power_positive(net_electric):
    value = _cmp('>', net_electric, 0.0)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((net_electric - 0.0)) if (_fin(net_electric) and _fin(0.0)) else None))

# definition:mfe_viability::'Burn Hold'
def constraint_pred_definition_mfe_viability__burn_hold(p_aux_required_in):
    value = _cmp('>=', p_aux_required_in, 0.0)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((p_aux_required_in - 0.0)) if (_fin(p_aux_required_in) and _fin(0.0)) else None))

# definition:mfe_viability::'Neutron Wall Load Limit'
def constraint_pred_definition_mfe_viability__neutron_wall_load_limit(wall_load, wall_load_limit_in):
    value = _cmp('<=', wall_load, wall_load_limit_in)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((wall_load_limit_in - wall_load)) if (_fin(wall_load) and _fin(wall_load_limit_in)) else None))

# definition:mfe_tritium_breeding::'Computed TBR Adequacy'
def constraint_pred_definition_mfe_tritium_breeding__computed_tbr_adequacy(defined_in, numerical_margin_in):
    value = _and(_cmp('>=', defined_in, 1.0), _cmp('>=', numerical_margin_in, 0.0))
    return _PredicateBodyResult(actual_value=value, source_margin=None)

# definition:mfe_viability::'Conductor Peak Field Limit'
def constraint_pred_definition_mfe_viability__conductor_peak_field_limit(B_peak, B_max_in):
    value = _cmp('<=', B_peak, B_max_in)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((B_max_in - B_peak)) if (_fin(B_peak) and _fin(B_max_in)) else None))

# definition:mfe_conductor_current::'Reference Conductor Current Margin'
def constraint_pred_definition_mfe_conductor_current__reference_conductor_current_margin(margin_fraction_in):
    value = _cmp('>=', margin_fraction_in, 0.0)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((margin_fraction_in - 0.0)) if (_fin(margin_fraction_in) and _fin(0.0)) else None))

# definition:mfe_viability::'Sustainment Limit'
def constraint_pred_definition_mfe_viability__sustainment_limit(p_aux_required_in, p_aux_installed_in):
    value = _cmp('<=', p_aux_required_in, p_aux_installed_in)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((p_aux_installed_in - p_aux_required_in)) if (_fin(p_aux_required_in) and _fin(p_aux_installed_in)) else None))

# definition:mfe_viability::'Loop Capacity'
def constraint_pred_definition_mfe_viability__loop_capacity(mdot_loop_in, mdot_loop_rated_in):
    value = _cmp('<=', mdot_loop_in, mdot_loop_rated_in)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((mdot_loop_rated_in - mdot_loop_in)) if (_fin(mdot_loop_in) and _fin(mdot_loop_rated_in)) else None))

# definition:mfe_winding_pack_fit::'Winding Pack Fits Casing'
def constraint_pred_definition_mfe_winding_pack_fit__winding_pack_fits_casing(minimum_margin_in):
    value = _cmp('>=', minimum_margin_in, 0.0)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((minimum_margin_in - 0.0)) if (_fin(minimum_margin_in) and _fin(0.0)) else None))

# definition:mfe_viability::'Loop Pressure Margin'
def constraint_pred_definition_mfe_viability__loop_pressure_margin(p_loop_margin_in):
    value = _cmp('>', p_loop_margin_in, 0.0)
    return _PredicateBodyResult(actual_value=value, source_margin=(_norm0((p_loop_margin_in - 0.0)) if (_fin(p_loop_margin_in) and _fin(0.0)) else None))
