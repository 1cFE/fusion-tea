"""Independent finance arithmetic and the unchanged current study interface."""
from tests.models.current_mfe_regressions import WI060_PARAMETERS, WI059_PARAMETERS, WI059_EXISTING_MAPPED_PARAMETERS, WI059_CHANNELS, WI059_NATIVE_ONLY_PARAMETERS, WI059_NATIVE_ONLY_VALUES

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
from tests.models.current_mfe_regressions import CURRENT_PARAMETERS, CURRENT_NUMERIC, CURRENT_PREDICATES, ADDITIONAL_MAPPING, FINANCE_DEPENDENCIES, LEGACY_COOLING_FACILITIES, assert_current_predicates, oracle_local_overrides

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
    import sqlite3
    from types import SimpleNamespace
    rates = [.07, .02, .02-1e-12, .02+1e-12, 0.] + [sign*magnitude for magnitude in (1e-4, 1e-8, 1e-12, 1e-16, 1e-18) for sign in (-1, 1)]
    proposals = [{route.P+'availability_direct': held, route.P+'discount_rate': rate}
                 for held in (0., .85) for rate in rates]
    current,db = route.run_points('finance-current-contract', proposals, tmp_path / 'current')
    legacy,_ = route.run_points('finance-qualified-legacy-contract', [LEGACY_COOLING_FACILITIES | p for p in proposals], tmp_path / 'legacy')
    assert len(current)==len(legacy)==len(proposals)==30
    with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as connection:
        failures={candidate:json.loads(payload) if payload else None for candidate,payload in connection.execute('select candidate_id,failure_json from cases')}
    for case in current:
        rate=case.inputs[route.P+'discount_rate']; held=case.inputs[route.P+'availability_direct']
        if rate < 0:
            assert case.state=='execution_failed'
            assert failures[case.candidate_id]['cause']=='ValueError: negative allowance or invalid makeup fraction'
            assert failures[case.candidate_id]['module_or_channel']==route.P+'heat_transport__equipment'
        elif held:
            assert case.state=='execution_failed'
            assert failures[case.candidate_id]['cause']=='ValueError: facilities requires one module, four sectors, live calendar'
            assert failures[case.candidate_id]['module_or_channel']==route.P+'buildings__layout'
        else:
            assert case.state=='completed'
    assert sum(c.state=='completed' for c in current)==10
    assert all(c.state=='completed' for c in legacy)
    inputs={}
    for path in (route.PACKAGE_DIR/'inputs').glob('*.json'):
        inputs.update(json.loads(path.read_text()))
    assert set(inputs)==CURRENT_PARAMETERS
    assert set(oracle.ENTRY_KEY_TO_ORACLE_INPUT)==set(ADDITIONAL_MAPPING['mapped_input_keys'])
    assert set(inputs)-set(oracle.ENTRY_KEY_TO_ORACLE_INPUT)==CURRENT_PARAMETERS-set(ADDITIONAL_MAPPING['mapped_input_keys'])
    financial=set(FINANCE_DEPENDENCIES['complete_channels']); unchanged=set(FINANCE_DEPENDENCIES['unchanged_channels'])
    assert financial | unchanged == CURRENT_NUMERIC and not financial & unchanged
    assert FINANCIAL_CHANNELS <= financial
    rows=[]
    for label,cases in [('current',[c for c in current if c.state=='completed']),('qualified-legacy',legacy)]:
        controls={c.inputs[route.P+'availability_direct']:c for c in cases if c.inputs[route.P+'discount_rate']==.07}
        for case in cases:
            control=controls[case.inputs[route.P+'availability_direct']]
            assert set(case.outputs)==CURRENT_NUMERIC
            assert set(case.verdicts)==CURRENT_PREDICATES
            assert case.verdicts==control.verdicts
            for channel in unchanged:
                assert case.outputs[channel]==control.outputs[channel],(label,channel)
            expected=oracle.evaluate(case.inputs)
            assert set(expected)==CURRENT_NUMERIC
            closure_residuals = {route.P+suffix for suffix in (
                'turbine__matched_cycle__salt_heat_residual_MW',
                'turbine__matched_cycle__heater_mass_residual_kg_s',
                'turbine__matched_cycle__heater_energy_residual_MW',
                'turbine__matched_cycle__cycle_shaft_residual_MW',
                'turbine__matched_cycle__cycle_electric_residual_MW',
                'heat_rejection__cooling_water__water_energy_residual_MW')}
            assert closure_residuals <= expected.keys()
            for channel,value in expected.items():
                if channel in closure_residuals:
                    assert case.outputs[channel] == pytest.approx(value, rel=1e-9, abs=1e-9), channel
                else:
                    relative(case.outputs[channel],value)
            assert_current_predicates(SimpleNamespace(outputs=case.outputs,responses=dict(case.verdicts,headline=case.headline)),case.inputs)
            p=oracle.vs.IN | oracle_local_overrides(case.inputs)
            equipment=route.P+'heat_transport__equipment__'
            annual=0.
            if p['cooling_enabled']:
                with localcontext() as context:
                    context.prec=100
                    rate=Decimal(p['discount_rate']); years=Decimal(p['operational_years']); base=1+rate
                    recovery=1/years if not rate else rate/(1-(-years*base.ln()).exp())
                    pv=Decimal(0)
                    for kind in ('machine','bundle'):
                        life=Decimal(p['cooling_'+kind+'_life']); k=1
                        cost=sum(Decimal(expected[equipment+kind+'_event_'+item]) for item in ('purchase','installation','removal'))
                        while k*life < years:
                            pv+=cost/(base**(k*life));k+=1
                    annual=float(pv*recovery)
            relative(case.outputs[equipment+'replacement_annual'],annual)
            selected=p['cooling_cost_mode']*annual
            relative(case.outputs[route.P+'heat_transport__cooling_selection__replacement_annual'],selected)
            relative(case.outputs[route.P+'cooling_annual__cas72_total'],expected[route.P+'calendar__cas72_annual']+selected)
            rows.append({'family':label,'inputs':dict(case.inputs),'financial':{k:{'native':case.outputs[k],'oracle':expected[k]} for k in sorted(financial)},'nonfinancial_exact':len(unchanged),'verdicts':route.short_verdicts(case)})
    (tmp_path/'finance-route-evidence.json').write_text(json.dumps({'cases':rows,'current_failure_evidence':failures,'mapped_inputs':sorted(oracle.ENTRY_KEY_TO_ORACLE_INPUT),'unmapped_inputs':sorted(set(inputs)-set(oracle.ENTRY_KEY_TO_ORACLE_INPUT)),'financial_channels':sorted(financial),'unchanged_channels':sorted(unchanged)},indent=2)+'\n')


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
