"""Independent 100-digit financial references from represented input operands.

Integer horizons explicitly sum dated cash flows. Fractional horizons retain
existing analytic continuations, evaluated with Decimal powers. No production
finance helper, prototype, or study oracle supplies these expectations.
"""
from decimal import Decimal, localcontext
from functools import wraps

PRECISION = 100


def precise(function):
    """Keep every reference operation inside its own high precision context."""
    @wraps(function)
    def wrapped(*args, **kwargs):
        with localcontext() as context:
            context.prec = PRECISION
            return function(*args, **kwargs)
    return wrapped


@precise
def crf(i, n):
    i, n = Decimal(i), Decimal(n)
    if n == n.to_integral_value():
        return 1 / sum(((1 + i) ** -k for k in range(1, int(n) + 1)), Decimal(0))
    return 1 / n if not i else i / (1 - (1 + i) ** -n)


@precise
def annuity_pv(annual, i, g, n, t):
    annual, i, g, n, t = map(Decimal, (annual, i, g, n, t))
    first = annual * (1 + g) ** t
    if n == n.to_integral_value():
        return sum((first * (1 + g) ** (k - 1) / (1 + i) ** k
                    for k in range(1, int(n) + 1)), Decimal(0))
    if i == g:
        return first * n / (1 + i)
    return first * (1 - ((1 + g) / (1 + i)) ** n) / (i - g)


@precise
def levelized(annual, i, g, n, t):
    return crf(i, n) * annuity_pv(annual, i, g, n, t)


@precise
def idc(i, t):
    i, t = Decimal(i), Decimal(t)
    return Decimal(0) if not i or t == 1 else ((1 + i) ** t - 1) / (i * t) - 1


@precise
def dated_pv(cost, i, dates):
    cost, i = Decimal(cost), Decimal(i)
    return sum((cost / (1 + i) ** Decimal(date) for date in dates), Decimal(0))


@precise
def periodic_pv(cost, i, interval, count):
    interval, count = Decimal(interval), Decimal(count)
    if count != count.to_integral_value():
        raise ValueError('The dated reference requires an integer event count')
    return dated_pv(cost, i, (k * interval for k in range(1, int(count) + 1)))


@precise
def midpoint(i, t):
    return (1 + Decimal(i)) ** (Decimal(t) / 2)


@precise
def dcf_components(capital, annual, i, n, t, power, availability):
    recovery = crf(i, n)
    construction = midpoint(i, t)
    annual_capital = Decimal(capital) * construction * recovery
    numerator = annual_capital + Decimal(annual)
    energy = Decimal(8760) * Decimal(power) * Decimal(availability)
    return dict(crf=recovery, midpoint=construction, annual_capital=annual_capital,
                numerator=numerator, annual_energy=energy, lcoe=numerator / energy)
