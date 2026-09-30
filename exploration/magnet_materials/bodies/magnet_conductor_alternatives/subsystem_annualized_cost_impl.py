"""WI-099 'Subsystem Annualized Cost' (design section 2.7).

capital_total = winding_capital + refrigerator_capital (USD2021); annual_electricity = p_in_total_MW *
hours * availability * electricity_price (USD/MWh); annualized_cost = crf*capital_total +
annual_electricity. Inputs are keyed by the design names without the generated `_in` suffix; invalid
inputs raise ValueError.
"""
import math

AUTO_IMPLEMENTED = False
INPUTS = dict(winding_capital=0., refrigerator_capital=0., p_in_total_MW=0., crf=0., hours=0., availability=0.,
              electricity_price=0.)
OUTPUTS = ['capital_total', 'annual_electricity', 'annualized_cost']
NAME = 'Subsystem Annualized Cost'


def calculate(x):
    missing = sorted(set(INPUTS) - set(x))
    if missing:
        raise ValueError(f'{NAME}: missing inputs {missing}')
    for key in INPUTS:
        value = x[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f'{NAME}: nonfinite or non-numeric input {key}={value!r}')
        if value < 0:
            raise ValueError(f'{NAME}: {key} must be nonnegative, got {value}')
    if x['availability'] > 1:
        raise ValueError(f'{NAME}: availability must not exceed 1')
    capital = x['winding_capital'] + x['refrigerator_capital']
    electricity = x['p_in_total_MW'] * x['hours'] * x['availability'] * x['electricity_price']
    return dict(capital_total=capital, annual_electricity=electricity, annualized_cost=x['crf'] * capital + electricity)
