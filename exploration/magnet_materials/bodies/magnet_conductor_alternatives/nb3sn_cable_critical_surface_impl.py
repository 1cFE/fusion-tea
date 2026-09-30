"""WI-099 'Nb3Sn Cable Critical Surface' (design section 2.1).

ITER-form strand critical surface (Tsui & Hampshire 2012 eq. 6-7; Breschi et al. 2017 Table III form,
C1 in A*T per whole strand), evaluated for a supplied strand count at a supplied duty. Inputs are keyed
by the design names without the generated `_in` suffix. Invalid inputs raise ValueError; an evaluation
outside the law's domain is reported through status outputs (status_code 0, acceptance_pass 0), never as
an exception and never as a pass.

Resolved design reading: the design writes the law for 0 < t < 1 but its T_cs bracket evaluates
n*Ic(B, 0); the law is therefore applied on 0 <= t < 1 (implementation-notes.md). If the strain function
s(eps) is not positive the law is undefined and its outputs are NaN (only far outside the strain domain).
"""
import math

AUTO_IMPLEMENTED = False
INPUTS = dict(n_strands=0., strand_diameter=0., strand_copper_fraction=0., turn_current=0., B_peak=0., T_supply=0.,
              nuclear_rise=0., margin_rise=0., p=0., q=0., C1=0., Ca1=0., Ca2=0., eps0a=0., Bc20=0., Tc0=0.,
              fraction_rule=0., acceptance_rule=0., B_law_min=0., B_law_max=0., B_design_max=0., B_edge_max=0.,
              T_law_min=0., T_law_max=0., eps_min=0., eps_max=0., eps_intrinsic=0.)
OUTPUTS = ['T_conductor', 'ic_strand_op', 'ic_cable_op', 'operating_fraction', 'T_cs', 'tcs_defined', 'temperature_margin',
           'temp_rule_margin', 'fraction_rule_margin', 'acceptance_margin', 'status_code', 'supported', 'acceptance_pass',
           'element_area_total', 'element_copper_area']
TCS_TOLERANCE = 1e-10  # K, bisection interval width (design section 2.1)
NAME = 'Nb3Sn Cable Critical Surface'


def _check(x):
    missing = sorted(set(INPUTS) - set(x))
    if missing:
        raise ValueError(f'{NAME}: missing inputs {missing}')
    for key in INPUTS:
        value = x[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f'{NAME}: nonfinite or non-numeric input {key}={value!r}')
    positive = ('n_strands', 'strand_diameter', 'turn_current', 'B_peak', 'T_supply', 'p', 'q', 'C1', 'Ca1', 'eps0a',
                'Bc20', 'Tc0', 'fraction_rule')
    for key in positive:
        if x[key] <= 0:
            raise ValueError(f'{NAME}: {key} must be positive, got {x[key]}')
    for key in ('nuclear_rise', 'margin_rise', 'Ca2'):
        if x[key] < 0:
            raise ValueError(f'{NAME}: {key} must be nonnegative, got {x[key]}')
    if not 0 <= x['strand_copper_fraction'] <= 1:
        raise ValueError(f'{NAME}: strand_copper_fraction must lie in [0, 1]')
    if x['Ca2'] >= x['Ca1']:
        raise ValueError(f'{NAME}: Ca2 must be below Ca1 (strain shift undefined)')
    if 1 - x['Ca1'] * x['eps0a'] <= 0:
        raise ValueError(f'{NAME}: 1 - Ca1*eps0a must be positive (strain entered in percent?)')
    if x['acceptance_rule'] not in (0, 1):
        raise ValueError(f'{NAME}: acceptance_rule must be 0 (temperature) or 1 (fraction)')
    if not (x['B_law_min'] <= x['B_design_max'] <= x['B_edge_max'] <= x['B_law_max']):
        raise ValueError(f'{NAME}: field bounds must satisfy B_law_min <= B_design_max <= B_edge_max <= B_law_max')
    if not (x['T_law_min'] <= x['T_law_max'] and x['eps_min'] <= x['eps_max']):
        raise ValueError(f'{NAME}: temperature and strain bounds must be ordered')


def strain_function(eps, Ca1, Ca2, eps0a):
    """Tsui & Hampshire 2012 eq. (7); eps_sh = 0 when Ca2 = 0."""
    eps_sh = Ca2 * eps0a / math.sqrt(Ca1 ** 2 - Ca2 ** 2)
    return 1 + (Ca1 * (math.sqrt(eps_sh ** 2 + eps0a ** 2) - math.sqrt((eps - eps_sh) ** 2 + eps0a ** 2)) - Ca2 * eps) / (1 - Ca1 * eps0a)


def strand_ic(B, T, s, x):
    """Strand critical current (A) at field B (T), temperature T (K) and strain function value s > 0."""
    tc = x['Tc0'] * s ** (1 / 3)
    t = T / tc
    if not 0 <= t < 1:
        return 0.0
    temperature_term = 1 - t ** 1.52
    b = B / (x['Bc20'] * s * temperature_term)
    if not 0 < b < 1:
        return 0.0
    return (x['C1'] / B) * s * temperature_term * (1 - t ** 2) * b ** x['p'] * (1 - b) ** x['q']


def status(B, T, eps, x):
    """Contract section 2 statuses: 0 unsupported, 1 supported, 2 edge, 3 law-only."""
    if not (x['B_law_min'] <= B <= x['B_law_max'] and x['T_law_min'] <= T <= x['T_law_max']
            and x['eps_min'] <= eps <= x['eps_max']):
        return 0.0
    if B <= x['B_design_max']:
        return 1.0
    if B <= x['B_edge_max']:
        return 2.0
    return 3.0


def current_sharing_temperature(n, B, I, s, x):
    """Bisection on [0, T_zero] to TCS_TOLERANCE; (T_cs, tcs_defined)."""
    if n * strand_ic(B, 0.0, s, x) < I:
        return 0.0, 0.0
    tc = x['Tc0'] * s ** (1 / 3)
    t_zero = (1 - B / (x['Bc20'] * s)) ** (1 / 1.52)  # b = 1 here; n*Ic(B, 0) >= I > 0 implies B < Bc20*s
    lo, hi = 0.0, t_zero * tc
    for _ in range(400):
        if hi - lo <= TCS_TOLERANCE:
            break
        mid = 0.5 * (lo + hi)
        if n * strand_ic(B, mid, s, x) >= I:
            lo = mid
        else:
            hi = mid
    else:
        raise ValueError(f'{NAME}: T_cs bisection did not converge')
    return 0.5 * (lo + hi), 1.0


def calculate(x):
    _check(x)
    n, I, B = x['n_strands'], x['turn_current'], x['B_peak']
    eps = x['eps_intrinsic']
    T_conductor = x['T_supply'] + x['nuclear_rise']
    T_rule = x['T_supply'] + x['nuclear_rise'] + x['margin_rise']
    code = status(B, T_conductor, eps, x)
    element_area_total = n * math.pi / 4 * x['strand_diameter'] ** 2 * 1e6
    s = strain_function(eps, x['Ca1'], x['Ca2'], x['eps0a'])
    if s > 0:
        ic_strand = strand_ic(B, T_conductor, s, x)
        ic_cable = n * ic_strand
        fraction = I / ic_cable if ic_cable > 0 else math.inf
        T_cs, tcs_defined = current_sharing_temperature(n, B, I, s, x)
    else:
        ic_strand = ic_cable = fraction = T_cs = math.nan
        tcs_defined = 0.0
    temp_margin = T_cs - T_rule
    fraction_margin = x['fraction_rule'] - fraction
    acceptance_margin = temp_margin if x['acceptance_rule'] == 0 else fraction_margin
    supported = 1.0 if code != 0 else 0.0
    accepted = 1.0 if supported == 1.0 and acceptance_margin >= 0 else 0.0
    return dict(T_conductor=T_conductor, ic_strand_op=ic_strand, ic_cable_op=ic_cable, operating_fraction=fraction,
                T_cs=T_cs, tcs_defined=tcs_defined, temperature_margin=T_cs - T_conductor, temp_rule_margin=temp_margin,
                fraction_rule_margin=fraction_margin, acceptance_margin=acceptance_margin, status_code=code,
                supported=supported, acceptance_pass=accepted, element_area_total=element_area_total,
                element_copper_area=x['strand_copper_fraction'] * element_area_total)
