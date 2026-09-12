"""WI-052 candidate numerical methods; source expressions are in spec.md.

Prototype only. No input-domain guards are introduced.
"""
import math


def crf(i, n):
    return 1.0 / n if i == 0.0 else i / -math.expm1(-n * math.log1p(i))


def annuity_pv(a, i, g, n, t):
    a1 = a * math.exp(t * math.log1p(g))
    if i == g:
        return a1 * n / (1.0 + i)
    z = math.log1p((g - i) / (1.0 + i))
    return a1 * -math.expm1(n * z) / (i - g)


def idc(i, t):
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
        raise ArithmeticError('IDC prototype series failed to converge')
    # Factor out the exact T=1 zero before subtracting; this also improves
    # ordinary-rate behavior for durations close to one.
    delta = t - 1.0
    return ((1.0 + i) * math.expm1(delta * math.log1p(i)) - delta * i) / (t * i)


def periodic_pv(cost, i, interval, count):
    if count == 0.0:
        return 0.0
    if i == 0.0:
        return cost * count
    x = -interval * math.log1p(i)
    return cost * math.exp(x) * math.expm1(count * x) / math.expm1(x)
