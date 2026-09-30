"""WI-099 'REBCO Cable Critical Surface' (design section 2.2).

Tape Ic(B, T) = anchor_ic*g(B)*exp(-(T - 20)/T_star), with g the measured 20 K, B||c field shape
(shape_mode 0: log-log interpolation between knots at 8, 10, 12, 15, 20 T) or the power law
(shape_mode 1: (B/20)^-alpha). Cable Ic = n*degradation*tape Ic; T_cs in closed form.
Inputs are keyed by the design names without the generated `_in` suffix. Invalid inputs raise
ValueError. Outside the supported field or temperature range the evaluation is reported with
status_code 0 and acceptance_pass 0. With shape_mode 0 and B outside the knot interval [8, 20] T
the shape has no defined value, so g and every quantity depending on it are NaN.
"""
import math

AUTO_IMPLEMENTED = False
INPUTS = dict(n_tapes=0., tape_width=0., tape_thickness=0., tape_copper_fraction=0., turn_current=0., B_peak=0.,
              T_supply=0., nuclear_rise=0., margin_rise=0., anchor_ic=0., shape_mode=0., g8=1., g10=1., g12=1., g15=1.,
              g20=1., alpha=0., T_star=1., degradation=1., fraction_rule=0., acceptance_rule=0., B_knot_min=0.,
              B_knot_max=0., B_law_min=0., B_law_max=0., T_law_min=0., T_law_max=0.)
OUTPUTS = ['T_conductor', 'ic_tape_op', 'ic_cable_op', 'operating_fraction', 'T_cs', 'tcs_defined', 'temperature_margin',
           'temp_rule_margin', 'fraction_rule_margin', 'acceptance_margin', 'status_code', 'supported', 'acceptance_pass',
           'element_area_total', 'element_copper_area']
KNOT_FIELDS = (8.0, 10.0, 12.0, 15.0, 20.0)  # T; the positions of g8..g20
ANCHOR_T = 20.0  # K; temperature of anchor_ic and of the measured shape
ANCHOR_B = 20.0  # T; field at which the shape is normalized
NAME = 'REBCO Cable Critical Surface'


def _check(x):
    missing = sorted(set(INPUTS) - set(x))
    if missing:
        raise ValueError(f'{NAME}: missing inputs {missing}')
    for key in INPUTS:
        value = x[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f'{NAME}: nonfinite or non-numeric input {key}={value!r}')
    for key in ('n_tapes', 'tape_width', 'tape_thickness', 'turn_current', 'B_peak', 'T_supply', 'anchor_ic', 'g8', 'g10',
                'g12', 'g15', 'g20', 'T_star', 'degradation', 'fraction_rule'):
        if x[key] <= 0:
            raise ValueError(f'{NAME}: {key} must be positive, got {x[key]}')
    for key in ('nuclear_rise', 'margin_rise', 'alpha'):
        if x[key] < 0:
            raise ValueError(f'{NAME}: {key} must be nonnegative, got {x[key]}')
    if not 0 <= x['tape_copper_fraction'] <= 1:
        raise ValueError(f'{NAME}: tape_copper_fraction must lie in [0, 1]')
    if x['shape_mode'] not in (0, 1):
        raise ValueError(f'{NAME}: shape_mode must be 0 (measured knots) or 1 (power law)')
    if x['acceptance_rule'] not in (0, 1):
        raise ValueError(f'{NAME}: acceptance_rule must be 0 (temperature) or 1 (fraction)')
    if not (x['B_knot_min'] <= x['B_knot_max'] and x['B_law_min'] <= x['B_law_max'] and x['T_law_min'] <= x['T_law_max']):
        raise ValueError(f'{NAME}: domain bounds must be ordered')


def shape(B, x):
    """g(B) = Ic(B, 20 K)/Ic(20 T, 20 K)."""
    if x['shape_mode'] == 1:
        return (B / ANCHOR_B) ** (-x['alpha'])
    values = (x['g8'], x['g10'], x['g12'], x['g15'], x['g20'])
    if not KNOT_FIELDS[0] <= B <= KNOT_FIELDS[-1]:
        return math.nan
    for (b0, g0), (b1, g1) in zip(zip(KNOT_FIELDS, values), zip(KNOT_FIELDS[1:], values[1:])):
        if b0 <= B <= b1:
            w = (math.log(B) - math.log(b0)) / (math.log(b1) - math.log(b0))
            return math.exp((1 - w) * math.log(g0) + w * math.log(g1))
    raise AssertionError('unreachable: B inside the knot interval')


def status(B, T, x):
    low, high = (x['B_knot_min'], x['B_knot_max']) if x['shape_mode'] == 0 else (x['B_law_min'], x['B_law_max'])
    return 1.0 if low <= B <= high and x['T_law_min'] <= T <= x['T_law_max'] else 0.0


def calculate(x):
    _check(x)
    n, I, B = x['n_tapes'], x['turn_current'], x['B_peak']
    T_conductor = x['T_supply'] + x['nuclear_rise']
    T_rule = x['T_supply'] + x['nuclear_rise'] + x['margin_rise']
    code = status(B, T_conductor, x)
    g = shape(B, x)
    ic_tape = x['anchor_ic'] * g * math.exp(-(T_conductor - ANCHOR_T) / x['T_star'])
    ic_cable = n * x['degradation'] * ic_tape
    fraction = I / ic_cable if ic_cable > 0 else (math.nan if math.isnan(ic_cable) else math.inf)
    T_cs = ANCHOR_T + x['T_star'] * math.log(n * x['degradation'] * x['anchor_ic'] * g / I) if math.isfinite(g) else math.nan
    temp_margin = T_cs - T_rule
    fraction_margin = x['fraction_rule'] - fraction
    acceptance_margin = temp_margin if x['acceptance_rule'] == 0 else fraction_margin
    supported = 1.0 if code != 0 else 0.0
    accepted = 1.0 if supported == 1.0 and acceptance_margin >= 0 else 0.0
    element_area_total = n * x['tape_width'] * x['tape_thickness'] * 1e6
    return dict(T_conductor=T_conductor, ic_tape_op=ic_tape, ic_cable_op=ic_cable, operating_fraction=fraction, T_cs=T_cs,
                tcs_defined=1.0 if math.isfinite(T_cs) else 0.0, temperature_margin=T_cs - T_conductor,
                temp_rule_margin=temp_margin, fraction_rule_margin=fraction_margin, acceptance_margin=acceptance_margin,
                status_code=code, supported=supported, acceptance_pass=accepted, element_area_total=element_area_total,
                element_copper_area=x['tape_copper_fraction'] * element_area_total)


from magnet_materials_tea.modules.magnet_conductor_alternatives.rebco_cable_critical_surface import REBCO_Cable_Critical_SurfaceInput


def _native_result(inputs):
    """Typed native adapter: strip the generated `_in` suffix, delegate to calculate, return schema order."""
    result = calculate({k.removesuffix('_in'): v for k, v in inputs.model_dump().items()})
    return tuple(result[k] for k in ['acceptance_margin', 'acceptance_pass', 'tcs_defined', 'status_code', 'ic_tape_op', 'temperature_margin', 'operating_fraction', 'element_area_total', 'T_conductor', 'ic_cable_op', 'element_copper_area', 'fraction_rule_margin', 'supported', 'T_cs', 'temp_rule_margin'])


def run_rebco_cable_critical_surface(inputs: REBCO_Cable_Critical_SurfaceInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float, float, float, float, float]:
    return _native_result(inputs)
