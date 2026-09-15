"""Independent finance arithmetic and the unchanged current study interface."""
from tests.models.current_mfe_regressions import WI059_PARAMETERS, WI059_EXISTING_MAPPED_PARAMETERS, WI059_CHANNELS, WI059_NATIVE_ONLY_PARAMETERS, WI059_NATIVE_ONLY_VALUES

import json
import math
import sys
from decimal import Decimal, localcontext
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'exploration/stellarator_e2e/studies'), str(ROOT / 'exploration/stellarator_e2e')]
import oracle_entry as oracle
import oracle_finance as finance
import study_route as route
from tests.study.financial_channels import FINANCIAL_CHANNELS

RATES = [0.0, 0.02, 0.08] + [sign * magnitude for magnitude in (1e-4, 1e-8, 1e-12, 1e-16, 1e-18) for sign in (-1, 1)]


def relative(actual, expected):
    assert math.isfinite(actual)
    if expected == 0:
        assert abs(actual) <= 1e-9
    else:
        assert abs((actual - expected) / expected) <= 1e-9, (actual, expected)


@pytest.mark.parametrize('rate', RATES)
def test_integer_finance_against_dated_sums(rate):
    with localcontext() as ctx:
        ctx.prec = 100
        base = 1 + Decimal(rate)
        recovery = 1 / sum(base ** -k for k in range(1, 31))
        relative(finance.crf(rate, 30), float(recovery))
        # Construction cash flows give the reported IDC identity for integer T.
        expected_idc = sum(base ** k - 1 for k in range(8)) / 8
        relative(finance.idc_factor(rate, 8), float(expected_idc))
        for escalation in (0.0, rate, 0.02, rate + 1e-12, rate - 1e-12):
            growth = 1 + Decimal(escalation)
            pv = sum(Decimal(1e6) * growth ** (8 + k - 1) / base ** k for k in range(1, 31))
            relative(finance.annuity(1e6, rate, escalation, 30, 8), float(pv * recovery))
        relative(finance.dated_pv(2e6, rate, [4.25, 8.5, 12.75]),
                 float(sum(Decimal(2e6) / base ** Decimal(t) for t in (4.25, 8.5, 12.75))))
        assert finance.dated_pv(2e6, rate, []) == 0


@pytest.mark.parametrize('years', [0.5, 1.0, math.nextafter(1.0, 0.0), math.nextafter(1.0, 2.0), 8.5, 30.5])
@pytest.mark.parametrize('rate', RATES)
def test_real_duration_identity_and_idc_binomial_series(years, rate):
    relative(finance.crf(0, years), 1 / years)
    # At equal rates, PV is A1*N/(1+i), including fractional N and T.
    with localcontext() as ctx:
        ctx.prec = 100
        i, n = Decimal(rate), Decimal(years)
        expected = Decimal(1e6) * (1+i) ** Decimal('8.5') * n / (1+i)
        recovery = 1/n if not i else i/(1-(-n*(1+i).ln()).exp())
        relative(finance.annuity(1e6, rate, rate, years, 8.5), float(expected * recovery))
        # Generalized binomial expansion of IDC: sum binom(T,k)*i^(k-1)/T,
        # k>=2. This avoids the oracle's power-minus-one calculation entirely.
        term = (n-1)*i/2
        total = term
        for k in range(3, 400):
            term *= (n-k+1)*i/k
            total += term
        relative(finance.idc_factor(rate, years), float(total))


@pytest.mark.parametrize('held', [0.0, 0.85])
@pytest.mark.parametrize('rate', RATES)
def test_calendar_dates_and_finance(rate, held):
    kwargs = dict(cost_per_event=2e6, q_n=2., fluence_limit=8., interest_rate=rate,
                  operational_years=30.5, outage_years=.4, unplanned_fraction=.05,
                  coil_life_fpy=40., availability_direct=held)
    actual = oracle.vs._oracle_lifecycle_calendar(**kwargs)
    control = oracle.vs._oracle_lifecycle_calendar(**{**kwargs, 'interest_rate': .07})
    for key in actual.keys() - {'replacement_pv', 'cas72_annual', 'dated_energy_ratio'}:
        assert actual[key] == control[key], key
    with localcontext() as ctx:
        ctx.prec = 100
        base = 1+Decimal(rate)
        pv = sum((Decimal(2e6) / base ** Decimal(t) for t in actual['events']), Decimal(0))
        relative(actual['replacement_pv'], float(pv))
        relative(actual['cas72_annual'], float(pv) * finance.crf(rate, 30.5))
    empty = oracle.vs._oracle_lifecycle_calendar(**{**kwargs, 'q_n': 0.0})
    assert empty['n_replacements'] == empty['replacement_pv'] == empty['cas72_annual'] == 0


def test_current_rate_route_and_coverage(tmp_path, stock_simkit_path):
    rates = [.07, .02, .02-1e-12, .02+1e-12, 0.] + [sign*magnitude for magnitude in (1e-4, 1e-8, 1e-12, 1e-16, 1e-18) for sign in (-1, 1)]
    proposals = [{route.P+'availability_direct': held, route.P+'discount_rate': rate}
                 for held in (0., .85) for rate in rates]
    cases, _ = route.run_points('finance-current-contract', proposals, tmp_path / 'route')
    assert len(cases) == len(proposals)
    inputs = {}
    for path in (route.PACKAGE_DIR/'inputs').glob('*.json'):
        inputs.update(json.loads(path.read_text()))
    assert len(inputs) == 265 + len(WI059_PARAMETERS | WI059_NATIVE_ONLY_PARAMETERS)  # WI-038 adds two explicitly mapped grade inputs.
    assert len(oracle.ENTRY_KEY_TO_ORACLE_INPUT) == 118 + len(WI059_PARAMETERS | WI059_EXISTING_MAPPED_PARAMETERS)
    assert len(set(inputs)-oracle.ENTRY_KEY_TO_ORACLE_INPUT.keys()) == 147 + len(WI059_NATIVE_ONLY_PARAMETERS) - len(WI059_EXISTING_MAPPED_PARAMETERS)
    controls = {}
    rows = []
    for case in cases:
        assert case.state == 'completed', (dict(case.inputs), case.state)
        if case.inputs[route.P+'discount_rate'] == .07:
            controls[case.inputs[route.P+'availability_direct']] = case
    for case in cases:
        control = controls[case.inputs[route.P+'availability_direct']]
        assert len(case.outputs) == 177 + len(WI059_CHANNELS)  # WI-038 adds three grade outputs.
        assert case.verdicts == control.verdicts
        assert len(case.verdicts) == 18
        for channel in case.outputs.keys() - FINANCIAL_CHANNELS:
            assert case.outputs[channel] == control.outputs[channel], channel
        expected = oracle.evaluate(case.inputs)
        covered_finance = set(expected) & FINANCIAL_CHANNELS
        for channel in covered_finance:
            relative(case.outputs[channel], expected[channel])
        rows.append({'inputs': dict(case.inputs), 'finance': {
            channel: {'native': case.outputs[channel], 'oracle': expected[channel]}
            for channel in sorted(covered_finance)}, 'nonfinancial_exact': len(case.outputs.keys() - FINANCIAL_CHANNELS),
            'verdicts': route.short_verdicts(case)})
    evidence = {'native_inputs': sorted(inputs), 'mapping': oracle.ENTRY_KEY_TO_ORACLE_INPUT,
                'unmapped': sorted(set(inputs)-oracle.ENTRY_KEY_TO_ORACLE_INPUT.keys()),
                'native_outputs': sorted(cases[0].outputs), 'oracle_mapping': oracle.ORACLE_OUTPUT_TO_CHANNEL,
                'uncovered_outputs': sorted(set(cases[0].outputs)-set(expected)),
                'covered_finance': sorted(covered_finance), 'cases': rows}
    (tmp_path/'finance-route-evidence.json').write_text(json.dumps(evidence, indent=2)+'\n')


@pytest.mark.parametrize('rate', RATES)
def test_dated_energy_against_yearly_downtime_subtraction(rate):
    # Compute yearly production as full year minus outage overlaps, independently
    # of the oracle's productive-segment intersection loop.
    kwargs = dict(cost_per_event=2e6, q_n=2., fluence_limit=8., interest_rate=rate,
                  operational_years=30.5, outage_years=.4, unplanned_fraction=.05,
                  coil_life_fpy=40., availability_direct=0.)
    actual = oracle.vs._oracle_lifecycle_calendar(**kwargs)
    horizon, outage, online_fraction = 30.5, .4, .95
    next_limit = (len(actual['events'])+1)*4/online_fraction + len(actual['events'])*outage
    off_intervals = [(t, t+outage) for t in actual['events']]
    if next_limit < horizon:
        off_intervals.append((next_limit, horizon))
    with localcontext() as ctx:
        ctx.prec = 100
        numerator = denominator = Decimal(0)
        for year in range(1, 32):
            start, end = year-1., min(float(year), horizon)
            off = sum(max(0., min(end,b)-max(start,a)) for a,b in off_intervals)
            discount = (1+Decimal(rate))**-year
            numerator += Decimal(online_fraction)*Decimal(end-start-off)*discount
            denominator += Decimal(actual['productive_fpy']/horizon)*Decimal(end-start)*discount
        relative(actual['dated_energy_ratio'], float(numerator/denominator))
    if rate == 0:
        relative(actual['dated_energy_ratio'], 1.)


@pytest.mark.parametrize('horizon', [math.nextafter(4.5, 0.), 4.5, math.nextafter(4.5, 5.)])
@pytest.mark.parametrize('rate', [0., 1e-18, -1e-18])
def test_strict_restart_boundary_and_held_clip_order(horizon, rate):
    actual = oracle.vs._oracle_lifecycle_calendar(2e6, 2., 8., rate, horizon, .5, 0., 40., 0.)
    assert actual['n_replacements'] == (1. if horizon > 4.5 else 0.)
    relative(actual['replacement_pv'], finance.dated_pv(2e6, rate, [4.] if horizon > 4.5 else []))
    # The cap follows the 0.5-FPY floor, even when the horizon's cap is smaller.
    held = oracle.vs._oracle_lifecycle_calendar(2e6, 100., .01, rate, .4, .5, 0., 40., .5)
    assert held['physical_life_fpy'] == .2
    assert held['n_replacements'] == held['replacement_pv'] == held['cas72_annual'] == 0.


@pytest.mark.parametrize('rate', [0., .02, -.02])
@pytest.mark.parametrize('delta', [sign*m for m in (1e-4, 1e-8, 1e-12, 1e-16, 1e-18) for sign in (-1, 1)])
def test_fractional_annuity_near_equal_actual_operands(rate, delta):
    escalation = rate + delta  # A rounded equality is tested as equality.
    with localcontext() as ctx:
        ctx.prec = 100
        i, g, n, t = Decimal(rate), Decimal(escalation), Decimal('30.5'), Decimal('8.5')
        log_ratio = (1+g).ln()-(1+i).ln()
        pv = n/(1+i) if i == g else (1-(n*log_ratio).exp())/(i-g)
        recovery = 1/n if not i else i/(1-(-n*(1+i).ln()).exp())
        expected = Decimal(1e6)*(t*(1+g).ln()).exp()*pv*recovery
        relative(finance.annuity(1e6, rate, escalation, 30.5, 8.5), float(expected))
