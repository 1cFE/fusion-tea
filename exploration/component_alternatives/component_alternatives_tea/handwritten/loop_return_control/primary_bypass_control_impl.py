"""WI-095 reviewed native calculation: primary-side bypass control holding the loop's return requirement at a counterflow exchanger.

Equations and physical assumptions: models/library/analyses/loop_return_control.sysml ('Primary Bypass Control' doc). The
effectiveness-NTU form is the 'Network Heat Driven Closure' body's, so capability(0) equals the closure's stage capability.
"""
from __future__ import annotations
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from component_alternatives_tea.modules.loop_return_control.primary_bypass_control import Primary_Bypass_ControlInput

AUTO_IMPLEMENTED = False

FIELDS = ('ua', 'primary_flow', 'primary_cp', 'secondary_flow', 'secondary_cp', 'primary_limit', 'secondary_inlet', 'duty', 'required_return', 'max_bypass', 'tolerance')


def _values(inputs):
    v = {}
    for f in FIELDS:
        x = float(getattr(inputs, f + '_in'))
        if not math.isfinite(x):
            raise ValueError('nonfinite input ' + f)
        v[f] = x
    return v


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _capability(ua, c_h, c_s, dt):
    """Counterflow effectiveness-NTU capability [MW] with effectiveness and NTU; zero for a stage that cannot transfer."""
    if c_h <= 0.0 or c_s <= 0.0 or ua <= 0.0 or dt <= 0.0:
        return 0.0, 0.0, 0.0
    cmin, cmax = min(c_h, c_s), max(c_h, c_s)
    cr, ntu = cmin / cmax, ua / cmin
    if abs(1.0 - cr) < 1e-10:
        eps = ntu / (1.0 + ntu)
    else:
        decay = math.exp(-ntu * (1.0 - cr))
        eps = -math.expm1(-ntu * (1.0 - cr)) / (1.0 - cr * decay)
    return eps * cmin * dt, eps, ntu


def calculate(inputs) -> dict[str, float]:
    v = _values(inputs)
    _require(v['primary_flow'] > 0 and v['primary_cp'] > 0 and v['secondary_flow'] > 0 and v['secondary_cp'] > 0, 'flows and specific heats must be positive')
    _require(v['ua'] >= 0 and v['duty'] >= 0, 'UA and duty must be nonnegative')
    _require(0.0 <= v['max_bypass'] <= 1.0, 'max bypass must lie in [0, 1]')
    _require(v['tolerance'] > 0, 'tolerance must be positive')
    c_h = v['primary_flow'] * v['primary_cp'] / 1e6
    c_s = v['secondary_flow'] * v['secondary_cp'] / 1e6
    dt = v['primary_limit'] - v['secondary_inlet']
    q = v['duty']
    t_out = v['primary_limit']
    cap0, eps0, ntu0 = _capability(v['ua'], c_h, c_s, dt)
    if cap0 < q:
        f, feasible, cap_f, eps, ntu = 0.0, 0.0, cap0, eps0, ntu0
    else:
        feasible = 1.0

        def g(frac):
            return _capability(v['ua'], (1.0 - frac) * c_h, c_s, dt)[0] - q

        lo, hi = 0.0, 1.0 - 1e-9
        g_lo, g_hi = g(lo), g(hi)
        _require(g_lo >= 0.0 and g_hi <= g_lo, 'capability must decrease with the bypass fraction')
        if g_lo == 0.0:
            f = 0.0
        elif g_hi > 0.0:
            raise ValueError('bypass cannot match the duty inside [0, 1)')
        else:
            f = None
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                g_mid = g(mid)
                if abs(g_mid) <= 1e-9 or (hi - lo) < 1e-15:
                    f = mid
                    break
                if g_mid > 0.0:
                    lo = mid
                else:
                    hi = mid
            _require(f is not None, 'bypass bisection did not converge in 200 iterations')
        cap_f, eps, ntu = _capability(v['ua'], (1.0 - f) * c_h, c_s, dt)
    exchanger_return = t_out - cap_f / ((1.0 - f) * c_h)
    mixed = f * t_out + (1.0 - f) * exchanger_return
    residual = mixed - v['required_return']
    return {'bypass_fraction': f, 'feasible': feasible, 'capability_open': cap0, 'capability_at_solution': cap_f, 'exchanger_primary_flow': (1.0 - f) * v['primary_flow'],
            'exchanger_return': exchanger_return, 'mixed_return': mixed, 'return_residual': residual,
            'return_residual_magnitude': abs(residual), 'effectiveness_at_solution': eps, 'ntu_at_solution': ntu}


def run_primary_bypass_control(inputs: Primary_Bypass_ControlInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float]:
    from component_alternatives_tea.schemas.primary_bypass_control_output import Primary_Bypass_ControlOutput
    result = calculate(inputs)
    return tuple(result[name] for name in Primary_Bypass_ControlOutput.model_fields)
