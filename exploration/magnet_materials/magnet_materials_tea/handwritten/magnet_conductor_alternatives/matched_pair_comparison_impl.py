"""WI-099 'Matched Pair Comparison' (design section 2.8, D2, D7).

rankable = all_pass_nb3sn*all_pass_rebco; pair_status = status_nb3sn when both statuses are supported
(non-zero), else 0; cost_difference = annualized_rebco - annualized_nb3sn; break-even REBCO price per
metre and per kA*m of tape critical current at the operating point. Break-even prices are reported for
every pair and are meaningful only when rankable = 1. rebco_ic_tape_op may be NaN when the REBCO
evaluation is outside its shape's knot interval (unsupported); the per-kA*m price is then NaN. Every
other input must be finite. Inputs are keyed by the design names without the generated `_in` suffix.
"""
import math

AUTO_IMPLEMENTED = False
INPUTS = dict(annualized_nb3sn=0., annualized_rebco=0., all_pass_nb3sn=0., all_pass_rebco=0., status_nb3sn=0.,
              status_rebco=0., rebco_element_length=1., rebco_price_per_m=0., rebco_ic_tape_op=1., crf=1.)
OUTPUTS = ['rankable', 'pair_status', 'cost_difference', 'breakeven_rebco_price_per_m', 'breakeven_rebco_price_per_kAm']
NAME = 'Matched Pair Comparison'


def calculate(x):
    missing = sorted(set(INPUTS) - set(x))
    if missing:
        raise ValueError(f'{NAME}: missing inputs {missing}')
    for key in INPUTS:
        value = x[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f'{NAME}: non-numeric input {key}={value!r}')
        if key != 'rebco_ic_tape_op' and not math.isfinite(value):
            raise ValueError(f'{NAME}: nonfinite input {key}={value!r}')
    for key in ('all_pass_nb3sn', 'all_pass_rebco'):
        if x[key] not in (0, 1):
            raise ValueError(f'{NAME}: {key} must be 0 or 1')
    for key in ('status_nb3sn', 'status_rebco'):
        if x[key] not in (0, 1, 2, 3):
            raise ValueError(f'{NAME}: {key} must be a status code 0-3')
    if x['crf'] <= 0 or x['rebco_element_length'] <= 0:
        raise ValueError(f'{NAME}: crf and rebco_element_length must be positive')
    both_supported = x['status_nb3sn'] != 0 and x['status_rebco'] != 0
    difference = x['annualized_rebco'] - x['annualized_nb3sn']
    per_m = x['rebco_price_per_m'] - difference / (x['crf'] * x['rebco_element_length'])
    ic = x['rebco_ic_tape_op']
    per_kAm = per_m / (ic / 1000) if math.isfinite(ic) and ic > 0 else math.nan
    return dict(rankable=x['all_pass_nb3sn'] * x['all_pass_rebco'], pair_status=x['status_nb3sn'] if both_supported else 0.0,
                cost_difference=difference, breakeven_rebco_price_per_m=per_m, breakeven_rebco_price_per_kAm=per_kAm)


from magnet_materials_tea.modules.magnet_conductor_alternatives.matched_pair_comparison import Matched_Pair_ComparisonInput


def _native_result(inputs):
    """Typed native adapter: strip the generated `_in` suffix, delegate to calculate, return schema order."""
    result = calculate({k.removesuffix('_in'): v for k, v in inputs.model_dump().items()})
    return tuple(result[k] for k in ['breakeven_rebco_price_per_m', 'breakeven_rebco_price_per_kAm', 'pair_status', 'cost_difference', 'rankable'])


def run_matched_pair_comparison(inputs: Matched_Pair_ComparisonInput) -> tuple[float, float, float, float, float]:
    return _native_result(inputs)
