"""Stable financial factors; rates dimensionless, durations Real years, PV in money.

Source: models/library/analyses/mfe_account_costs.sysml (IDC and annual cost),
models/library/analyses/mfe_lcoe_dcf.sysml and mfe_lifecycle.sysml.
Ref: work/active/WI-052_mfe-financial-rate-limits/design.md, Numerical method
and justification. Basis: equivalent native equations, first payment at operating
year one after construction escalation; reported uniform-spend IDC remains
separate from headline midpoint finance. Last Updated: 2026-09-12.

For abs(i)*max(1,abs(T)) <= 0.125 the generalized-binomial IDC series has
successive absolute term ratios <= 0.125 for positive T. Its 1e-17 relative
last-term stop bounds the remaining tail below about 1.43e-18 of the sum.
Outside that switch, factor T-1 before subtracting. Tested durations span
0.25 through 200.5 including both neighbors of one; this is numerical evidence,
not a supported-domain boundary. Construction-duration zero remains parked.
"""
import math


def crf(i: float, n: float) -> float:
    return 1.0 / n if i == 0.0 else i / -math.expm1(-n * math.log1p(i))


def annuity_pv(a: float, i: float, g: float, n: float, t: float) -> float:
    a1 = a * math.exp(t * math.log1p(g))
    if i == g:
        return a1 * n / (1.0 + i)
    z = math.log1p((g - i) / (1.0 + i))
    return a1 * -math.expm1(n * z) / (i - g)


def idc(i: float, t: float) -> float:
    if i == 0.0 or t == 1.0:
        return 0.0
    if abs(i) * max(1.0, abs(t)) <= 0.125:
        term = (t - 1.0) * i / 2.0
        terms = [term]
        for k in range(2, 100):
            term *= (t - k) * i / (k + 1.0)
            terms.append(term)
            if abs(term) <= abs(math.fsum(terms)) * 1e-17:
                return math.fsum(terms)
        raise ArithmeticError('IDC series failed to converge')
    # Factor out the exact T=1 zero before subtracting; this also improves
    # ordinary-rate behavior for durations close to one.
    delta = t - 1.0
    return ((1.0 + i) * math.expm1(delta * math.log1p(i)) - delta * i) / (t * i)


def periodic_pv(cost: float, i: float, interval: float, count: float) -> float:
    if count == 0.0:
        return 0.0
    if i == 0.0:
        return cost * count
    x = -interval * math.log1p(i)
    return cost * math.exp(x) * math.expm1(count * x) / math.expm1(x)
