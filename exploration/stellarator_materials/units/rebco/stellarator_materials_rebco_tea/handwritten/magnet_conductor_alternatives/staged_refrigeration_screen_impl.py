"""WI-099 'Staged Refrigeration Screen' (design section 2.6).

Electrical demand and capital of the installed two-stage refrigerator, and the installed cold-stage
rating compared with the calculated cold load. Efficiency is a property of the installed plant,
evaluated at its rating and applied to the operating load (part-load penalty not modeled). Powers W,
p_in_total_MW in MW, ratings W (Green laws take kW), capital USD2021. Inputs are keyed by the design
names without the generated `_in` suffix; invalid inputs (including an efficiency outside (0, 1])
raise ValueError.
"""
import math

AUTO_IMPLEMENTED = False
INPUTS = dict(q_cold=0., T_supply=0., q_shield=0., T_shield=0., T_amb=0., rating_cold=0., eta_mode=0., eta_const=0.,
              green_a=0., green_b=0., f_carnot_shield=1., capital_mode=0., green_c=0., green_d=0., T_green=0.,
              usd2015_to_2021=1.)
OUTPUTS = ['carnot_specific_power', 'eta_cold', 'p_in_cold', 'p_in_shield', 'p_in_total_MW', 'R_equiv_kW',
           'refrigerator_capital', 'capacity_margin', 'capacity_pass', 'green_extrapolated']
GREEN_DATA_KW = (0.01, 35.0)  # Green 2015 fitted data range (design D6)
NAME = 'Staged Refrigeration Screen'


def _check(x):
    missing = sorted(set(INPUTS) - set(x))
    if missing:
        raise ValueError(f'{NAME}: missing inputs {missing}')
    for key in INPUTS:
        value = x[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f'{NAME}: nonfinite or non-numeric input {key}={value!r}')
    if not 0 < x['T_supply'] < x['T_shield'] < x['T_amb']:
        raise ValueError(f'{NAME}: temperatures must satisfy 0 < T_supply < T_shield < T_amb')
    if not 0 < x['T_green'] < x['T_amb']:
        raise ValueError(f'{NAME}: T_green must lie in (0, T_amb)')
    for key in ('rating_cold', 'f_carnot_shield', 'usd2015_to_2021'):
        if x[key] <= 0:
            raise ValueError(f'{NAME}: {key} must be positive, got {x[key]}')
    for key in ('q_cold', 'q_shield', 'green_c'):
        if x[key] < 0:
            raise ValueError(f'{NAME}: {key} must be nonnegative, got {x[key]}')
    if x['eta_mode'] not in (0, 1, 2):
        raise ValueError(f'{NAME}: eta_mode must be 0 (Green at rating), 1 (constant) or 2 (Green at input-power equivalent)')
    if x['capital_mode'] not in (0, 1):
        raise ValueError(f'{NAME}: capital_mode must be 0 (input-power equivalence) or 1 (capacity basis)')


def calculate(x):
    _check(x)
    carnot = (x['T_amb'] - x['T_supply']) / x['T_supply']
    carnot_ref = (x['T_amb'] - x['T_green']) / x['T_green']
    equiv = carnot / carnot_ref
    rating_kW = x['rating_cold'] / 1000
    R_equiv = rating_kW * equiv if x['capital_mode'] == 0 else rating_kW
    if x['eta_mode'] == 1:
        eta, R_eta = x['eta_const'], None
    else:
        R_eta = rating_kW if x['eta_mode'] == 0 else rating_kW * equiv
        eta = x['green_a'] * R_eta ** x['green_b']
    if not 0 < eta <= 1:
        raise ValueError(f'{NAME}: refrigerator efficiency {eta} outside (0, 1]')
    p_cold = x['q_cold'] * carnot / eta
    p_shield = x['q_shield'] * (x['T_amb'] - x['T_shield']) / x['T_shield'] / x['f_carnot_shield']
    low, high = GREEN_DATA_KW
    arguments = [R_equiv] + ([] if R_eta is None else [R_eta])
    extrapolated = 1.0 if any(not low <= r <= high for r in arguments) else 0.0
    margin = x['rating_cold'] - x['q_cold']
    return dict(carnot_specific_power=carnot, eta_cold=eta, p_in_cold=p_cold, p_in_shield=p_shield,
                p_in_total_MW=(p_cold + p_shield) / 1e6, R_equiv_kW=R_equiv,
                refrigerator_capital=x['green_c'] * R_equiv ** x['green_d'] * x['usd2015_to_2021'],
                capacity_margin=margin, capacity_pass=1.0 if margin >= 0 else 0.0, green_extrapolated=extrapolated)


from stellarator_materials_rebco_tea.modules.magnet_conductor_alternatives.staged_refrigeration_screen import Staged_Refrigeration_ScreenInput


def _native_result(inputs):
    """Typed native adapter: strip the generated `_in` suffix, delegate to calculate, return schema order."""
    result = calculate({k.removesuffix('_in'): v for k, v in inputs.model_dump().items()})
    return tuple(result[k] for k in ['p_in_total_MW', 'eta_cold', 'green_extrapolated', 'R_equiv_kW', 'refrigerator_capital', 'carnot_specific_power', 'p_in_cold', 'capacity_pass', 'capacity_margin', 'p_in_shield'])


def run_staged_refrigeration_screen(inputs: Staged_Refrigeration_ScreenInput) -> tuple[float, float, float, float, float, float, float, float, float, float]:
    return _native_result(inputs)
