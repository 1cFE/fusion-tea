"""Independent reviewer probe; no artifact writes or production changes."""
import math
import sys
from decimal import Decimal as D, localcontext
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'prototype'))
from factors import annuity_pv, crf, idc, periodic_pv

worst = {}
count = 0


def check(name, actual, expected):
    global count
    error = abs(D(actual) - expected) / abs(expected) if expected else abs(D(actual))
    assert error < D('1e-9'), (name, actual, expected, error)
    worst[name] = max(worst.get(name, D(0)), error)
    count += 1


with localcontext() as context:
    context.prec = 100
    for duration in [.125, .3, math.nextafter(1., 0.), 1., math.nextafter(1., 2.), 8.5, 30.5, 300.5]:
        boundary = .125 / max(1, duration)
        for rate in [0., -.02, .02, .08, -1e-18, 1e-18, -1e-12, 1e-12, -math.nextafter(boundary, 0), math.nextafter(boundary, 0), boundary, math.nextafter(boundary, math.inf)]:
            interest, years = D(rate), D(duration)
            expected = ((1 + interest)**years - 1) / (years * interest) - 1 if interest and years != 1 else D(0)
            check('idc', idc(rate, duration), expected)
            check('crf', crf(rate, duration), interest / (1 - (1 + interest)**(-years)) if interest else 1 / years)
            for events in [0., 1., 9.]:
                expected = sum((D(1000000) / (1 + interest)**(years * k) for k in range(1, int(events) + 1)), D(0))
                check('periodic', periodic_pv(1e6, rate, duration, events), expected)
            neighbors = [rate, math.nextafter(rate, math.inf), math.nextafter(rate, -math.inf)] if rate else [0., -1e-18, 1e-18]
            for escalation in neighbors:
                growth, horizon = D(escalation), D('30.5')
                first_payment = D(1000000) * (1 + growth)**years
                expected = first_payment * horizon / (1 + interest) if interest == growth else first_payment * (1 - ((1 + growth) / (1 + interest))**horizon) / (interest - growth)
                check('annuity', annuity_pv(1e6, rate, escalation, 30.5, duration), expected)

print('Independent reviewer checks:', count)
print({key: float(value) for key, value in worst.items()})
