"""Independent energy/LMTD solution for WI-097; imports no production helpers.

The passive transfer law follows ln(a/b)=UA*(1/Ch-1/Cs), where
a=H-S-q/Cs and b=H-S-q/Ch. Controlled transfer instead fixes q,
solves for log(b/a), then recovers active capacity from primary energy.
This differs from native effectiveness-NTU and its bypass root.
"""
from math import exp, expm1, isfinite, log

from scipy.optimize import brentq


def passive_transfer(drive, ua, primary_capacity, secondary_capacity):
    """Finite-duty LMTD solution without subtracting nearly equal temperatures."""
    if min(primary_capacity, secondary_capacity) <= 0 or ua < 0:
        raise ValueError("positive stream capacities and nonnegative UA required")
    if drive <= 0 or ua == 0:
        return 0.0
    inverse_difference = 1 / primary_capacity - 1 / secondary_capacity
    z = ua * inverse_difference
    if abs(z) < 1e-7:
        # Analytic equal-capacity limit, retaining unequal-capacity correction.
        exprel = 1 - z / 2 + z*z / 6 - z*z*z / 24 + z**4 / 120
        return drive * ua * exprel / (1 + ua * exprel / secondary_capacity)
    if z > 0:
        return drive * (-expm1(-z)) / (1 / primary_capacity - exp(-z) / secondary_capacity)
    return drive * (-expm1(z)) / (1 / secondary_capacity - exp(z) / primary_capacity)


def log_mean_ratio(x):
    """log((exp(x)-1)/x), with stable limits and no exp overflow."""
    if abs(x) < 1e-5:
        return x/2 + x*x/24 - x**4/2880
    if x > 50:
        return x + log(-expm1(-x)) - log(x)
    if x < 0:
        return log(-expm1(x)) - log(-x)
    return log(expm1(x)) - log(x)


def passive_log_terminal_gaps(drive, ua, ch, cs):
    """Logs of both positive passive gaps, even below temperature precision."""
    if min(drive, ch, cs) <= 0 or ua < 0:
        raise ValueError("positive driving temperature and stream capacities required")
    difference = 1/ch-1/cs
    z = ua*difference
    if abs(z) < 1e-7:
        q = passive_transfer(drive, ua, ch, cs)
        return log(drive-q/cs), log(drive-q/ch)
    if z > 0:
        log_a = log(drive)+log(difference)-log(1/ch-exp(-z)/cs)
        return log_a, log_a-z
    log_b = log(drive)+log(-difference)-log(1/cs-exp(z)/ch)
    return log_b+z, log_b


def cold_gap_from_lmtd(hot_gap, mean_gap):
    """Return cold gap and its logarithm, retaining sub-float terminal states."""
    if hot_gap <= 0 or mean_gap <= 0:
        raise ValueError("positive actual hot gap and logarithmic mean required")
    target = log(mean_gap / hot_gap)
    low, high = -1.0, 1.0
    while log_mean_ratio(low) > target:
        low *= 2
    while log_mean_ratio(high) < target:
        high *= 2
    ratio_log = brentq(lambda x: log_mean_ratio(x)-target, low, high,
                       xtol=1e-12, rtol=1e-14)
    log_gap = log(hot_gap) + ratio_log
    return exp(log_gap), log_gap


def stage(*, duty, ua, ch, cs, source_hot, secondary, controlled):
    """Independent branch state; source_hot is required hot or legacy hot cap."""
    if duty < 0:
        raise ValueError("nonnegative delivered duty required")
    drive = source_hot-secondary
    capability = passive_transfer(drive, ua, ch, cs)
    q = min(duty, capability)
    defined = q > 0 and ua > 0 and drive > 0
    bypass, active_ch, gap_log = 0.0, ch, None
    if controlled:
        hot = source_hot
        if defined and capability >= duty:
            # The bypass is recovered from a prescribed-duty LMTD inversion.
            a = drive-duty/cs
            if a <= 0:
                # At the secondary asymptote binary64 can round capability to
                # duty although a positive finite-UA deficit still exists.
                # Reconstruct that no-bypass limiting state at higher precision.
                q = precise_passive_transfer(drive, ua, ch, cs)
                q = min(duty, q)
                hx_return = hot-q/ch
                secondary_out = secondary+q/cs
                return dict(transferred=q, unmet=duty-q, capability=capability,
                    hot=hot, hx_return=hx_return, mixed_return=hx_return,
                    secondary_in=secondary, secondary_out=secondary_out,
                    hot_terminal_difference=hot-secondary_out,
                    cold_terminal_difference=hx_return-secondary,
                    state_defined=1.0, bypass_fraction=0.0, active_capacity=ch,
                    solved_capability=q, cold_gap_log=None)
            b, gap_log = cold_gap_from_lmtd(a, duty/ua)
            active_ch = duty/(drive-b)
            bypass = max(0.0, 1-active_ch/ch)
            active_ch = ch*(1-bypass)
        hx_return = hot-q/active_ch
        mixed_return = hot-q/ch
    else:
        coefficient = passive_transfer(1.0, ua, ch, cs)
        hot = secondary+q/coefficient if defined else 0.0
        hx_return = hot-q/ch if defined else 0.0
        mixed_return = hx_return
    secondary_out = secondary+q/cs
    actual_capability = passive_transfer(hot-secondary, ua, active_ch, cs) if defined else 0.0
    return dict(transferred=q, unmet=duty-q, capability=capability,
                hot=hot, hx_return=hx_return, mixed_return=mixed_return,
                secondary_in=secondary, secondary_out=secondary_out,
                hot_terminal_difference=hot-secondary_out if defined else 0.0,
                cold_terminal_difference=hx_return-secondary if defined else 0.0,
                state_defined=float(defined), bypass_fraction=bypass,
                active_capacity=active_ch, solved_capability=actual_capability,
                cold_gap_log=gap_log)


def solve_cycle(cold, expansion, recuperator, capacity, network, split, branches):
    """Brent closure on actual accepted heat; reconstruct branch topology."""
    if network not in (0, 1) or not 0 < split < 1:
        raise ValueError("network must be 0/1 and split strictly between 0 and 1")
    def evaluate(temperature):
        inlet = cold+recuperator*max(expansion*temperature-cold, 0.0)
        states = {}
        secondary = inlet
        for name in ("he", "divertor", "pbli"):
            cs = capacity if network == 0 or name == "he" else capacity*(split if name == "pbli" else 1-split)
            states[name] = stage(**branches[name], cs=cs, secondary=secondary)
            if network == 0 or name == "he":
                secondary = states[name]["secondary_out"]
        accepted = sum(s["transferred"] for s in states.values())
        return capacity*(temperature-inlet)-accepted, inlet, states
    high = max([cold]+[s["source_hot"] for s in branches.values()])
    if evaluate(cold)[0] > 1e-10 or evaluate(high)[0] < -1e-10:
        raise ValueError("independent thermal bracket invalid")
    root = brentq(lambda t: evaluate(t)[0], cold, high, xtol=1e-11, rtol=1e-14)
    residual, inlet, states = evaluate(root)
    if not isfinite(residual) or abs(residual) > 1e-7:
        raise ValueError("independent cycle solve failed its numerical contract")
    return root, inlet, states, residual


def precise_passive_transfer(drive, ua, ch, cs, digits=100):
    """High-precision LMTD relation for a rounded secondary asymptote.

    Used only when binary64 cannot resolve the hot terminal; the float output
    is the correctly rounded finite-transfer state, never a zero-duty sentinel.
    """
    import mpmath as mp
    with mp.workdps(digits):
        g, u, h, s = map(mp.mpf, (drive, ua, ch, cs))
        z = u*(1/h-1/s)
        if z == 0:
            q = g*u/(1+u/h)
        elif z > 0:
            q = g*(-mp.expm1(-z))/(1/h-mp.exp(-z)/s)
        else:
            q = g*(-mp.expm1(z))/(1/s-mp.exp(z)/h)
        return float(q)
