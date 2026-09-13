"""Independent high-precision evaluation of the retained financial equations.

Decimal.from_float preserves actual binary64 operands. Eighty digits leave over
50 guard digits after the smallest tested (1e-18) rate cancellation. Integer
cash flows are dated sums; fractional horizons retain analytic continuation.
No generated package or production helper is imported.
"""
from decimal import Decimal, localcontext


def _d(value):
    return Decimal(value)


def crf(rate, years):
    with localcontext() as ctx:
        ctx.prec = 80
        i, n = _d(rate), _d(years)
        return float(1 / n if not i else i / (1 - (1 + i) ** -n))


def annuity(annual, rate, escalation, years, construction):
    with localcontext() as ctx:
        ctx.prec = 80
        a, i, g, n, t = map(_d, (annual, rate, escalation, years, construction))
        a1 = a * (1 + g) ** t
        pv = a1 * n / (1 + i) if i == g else a1 * (1 - ((1 + g) / (1 + i)) ** n) / (i - g)
        recovery = 1 / n if not i else i / (1 - (1 + i) ** -n)
        return float(pv * recovery)


def idc_factor(rate, construction):
    with localcontext() as ctx:
        ctx.prec = 80
        i, t = _d(rate), _d(construction)
        return float(((1 + i) ** t - 1) / (i * t) - 1) if i else 0.0


def growth(rate, years):
    with localcontext() as ctx:
        ctx.prec = 80
        return float((1 + _d(rate)) ** _d(years))


def dated_pv(amount, rate, dates):
    with localcontext() as ctx:
        ctx.prec = 80
        base = 1 + _d(rate)
        return float(sum((_d(amount) / base ** _d(t) for t in dates), Decimal(0)))
