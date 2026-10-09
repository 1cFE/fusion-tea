"""WI-099 'Magnet Cold Stage Load' (design section 2.5).

Cold-stage load at the supply temperature and the 77 K intercept load, in W. The 316 stainless
conductivity integral K(T) = int_T^T_shield k(T') dT' uses the NIST fit log10 k = sum_i c_i (log10 T)^i
(coefficients k_a..k_i) and composite Simpson over SIMPSON_INTERVALS equal intervals in u = ln T
(dT = T du). Inputs are keyed by the design names without the generated `_in` suffix; invalid inputs
raise ValueError.
"""
import math

AUTO_IMPLEMENTED = False
COEFFICIENTS = ('k_a', 'k_b', 'k_c', 'k_d', 'k_e', 'k_f', 'k_g', 'k_h', 'k_i')
INPUTS = dict(T_supply=0., T_shield=0., T_amb=0., turn_current=0., nuclear_density=0., cold_volume=0., radiation_ref=0.,
              conduction_ref=0., T_conduction_ref=0., **{key: 0. for key in COEFFICIENTS}, n_leads=0., f_lead=1., L0=0.,
              p_joint_ref=0., I_joint_ref=1., shield_static=0., load_multiplier=1.)
OUTPUTS = ['q_nuclear', 'q_radiation', 'q_conduction', 'q_leads', 'q_joints', 'q_cold', 'q_shield', 'k_integral']
SIMPSON_INTERVALS = 2000  # even; design section 2.5 ("composite Simpson, 2000 panels in log T")
NAME = 'Magnet Cold Stage Load'


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
    if not 0 < x['T_conduction_ref'] < x['T_shield']:
        raise ValueError(f'{NAME}: T_conduction_ref must lie in (0, T_shield)')
    if x['I_joint_ref'] <= 0:
        raise ValueError(f'{NAME}: I_joint_ref must be positive')
    for key in ('nuclear_density', 'cold_volume', 'radiation_ref', 'conduction_ref', 'n_leads', 'f_lead', 'L0', 'p_joint_ref',
                'shield_static', 'load_multiplier'):
        if x[key] < 0:
            raise ValueError(f'{NAME}: {key} must be nonnegative, got {x[key]}')


def conductivity(T, c):
    """NIST 316 stainless thermal conductivity, W/(m K)."""
    y = math.log10(T)
    return 10 ** sum(ci * y ** i for i, ci in enumerate(c))


def conductivity_integral(T_low, T_high, c):
    """int_{T_low}^{T_high} k dT by composite Simpson in ln T, W/m."""
    a, b = math.log(T_low), math.log(T_high)
    h = (b - a) / SIMPSON_INTERVALS
    f = lambda u: conductivity(math.exp(u), c) * math.exp(u)
    total = f(a) + f(b)
    total += 4 * math.fsum(f(a + i * h) for i in range(1, SIMPSON_INTERVALS, 2))
    total += 2 * math.fsum(f(a + i * h) for i in range(2, SIMPSON_INTERVALS, 2))
    return h / 3 * total


def calculate(x):
    _check(x)
    c = [x[key] for key in COEFFICIENTS]
    I = abs(x['turn_current'])
    k_supply = conductivity_integral(x['T_supply'], x['T_shield'], c)
    k_reference = conductivity_integral(x['T_conduction_ref'], x['T_shield'], c)
    q_nuclear = x['nuclear_density'] * x['cold_volume']
    q_radiation = x['radiation_ref']
    q_conduction = x['conduction_ref'] * k_supply / k_reference
    q_leads = x['f_lead'] * x['n_leads'] * I * math.sqrt(x['L0'] * (x['T_shield'] ** 2 - x['T_supply'] ** 2))
    q_joints = x['p_joint_ref'] * (x['turn_current'] / x['I_joint_ref']) ** 2
    q_cold = x['load_multiplier'] * (q_nuclear + q_radiation + q_conduction + q_leads + q_joints)
    q_shield = x['shield_static'] + x['f_lead'] * x['n_leads'] * I * math.sqrt(x['L0'] * (x['T_amb'] ** 2 - x['T_shield'] ** 2))
    return dict(q_nuclear=q_nuclear, q_radiation=q_radiation, q_conduction=q_conduction, q_leads=q_leads, q_joints=q_joints,
                q_cold=q_cold, q_shield=q_shield, k_integral=k_supply)


from stellarator_materials_nb3sn_tea.modules.magnet_conductor_alternatives.magnet_cold_stage_load import Magnet_Cold_Stage_LoadInput


def _native_result(inputs):
    """Typed native adapter: strip the generated `_in` suffix, delegate to calculate, return schema order."""
    result = calculate({k.removesuffix('_in'): v for k, v in inputs.model_dump().items()})
    return tuple(result[k] for k in ['q_cold', 'q_conduction', 'q_shield', 'q_nuclear', 'q_radiation', 'q_leads', 'k_integral', 'q_joints'])


def run_magnet_cold_stage_load(inputs: Magnet_Cold_Stage_LoadInput) -> tuple[float, float, float, float, float, float, float, float]:
    return _native_result(inputs)
