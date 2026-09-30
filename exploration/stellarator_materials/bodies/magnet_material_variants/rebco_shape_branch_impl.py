"""WI-100 'REBCO Shape Branch' (design section 2.4, D15; probe P4 fallback body).

Selects Round 1's REBCO field shape from the calculated peak field: 1.0 (power-law continuation) above the last
knot, 0.0 (measured knots) at or below it. The codegen exact route refuses an `if` expression, so the calc def
declares only its output and this body completes it. Inputs are keyed by the design names without the generated
`_in` suffix; nonfinite inputs raise ValueError.
"""
import math

AUTO_IMPLEMENTED = False
INPUTS = dict(B_peak=0., B_knot_max=0.)
OUTPUTS = ['shape_mode']
NAME = 'REBCO Shape Branch'


def calculate(x):
    for key in INPUTS:
        value = x[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f'{NAME}: nonfinite or non-numeric input {key}={value!r}')
    return dict(shape_mode=1.0 if x['B_peak'] > x['B_knot_max'] else 0.0)
