"""SV-090: independent factors and actual generated public finance routes."""
import importlib
import importlib.util
import json
import math
import os
from decimal import Decimal, localcontext
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / 'work/active/WI-052_mfe-financial-rate-limits/implementation/reference_finance.py'
spec = importlib.util.spec_from_file_location('wi052_reference_finance', REFERENCE)
reference = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)

RATES = (0., .02, .08) + tuple(sign * 10. ** -power for power in (4, 8, 12, 16, 18) for sign in (-1, 1))
DURATIONS = (.25, .5, math.nextafter(1., 0.), 1., math.nextafter(1., 2.), 8., 8.5, 30., 30.5, 100.5, 200.5)


def assert_finance(actual, expected, quantity, operands):
    """Relative error has no absolute floor, even for a tiny nonzero IDC."""
    assert math.isfinite(actual), (quantity, operands, actual)
    with localcontext() as context:
        context.prec = 100
        error = abs(Decimal(actual) - expected)
        if expected:
            error /= abs(expected)
        assert error <= Decimal('1e-9'), (quantity, operands, actual, str(expected), str(error))


@pytest.fixture(scope='module')
def production():
    # Import the native package, never a copied prototype. The location assertion
    # rejects contamination by earlier tests' temporary package aliases.
    package_parent = ROOT / 'exploration/stellarator_e2e/pkg'
    added_paths = [str(package_parent)]
    if os.environ.get('STOP_PARSER_TEAX_ROOT'):
        added_paths.append(str(Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit'))
    for path in added_paths:
        sys.path.insert(0, path)
    try:
        factors = importlib.import_module('stellarator_tea.handwritten.mfe_account_costs.financial_factors')
        expected = ROOT / 'exploration/stellarator_e2e/generated/handwritten/mfe_account_costs/financial_factors.py'
        assert Path(factors.__file__).resolve() == expected.resolve()
        annual = importlib.import_module('stellarator_tea.modules.mfe_account_costs.levelized_annual_cost')
        idc = importlib.import_module('stellarator_tea.modules.mfe_account_costs.idc_closed_form_cost')
        dcf = importlib.import_module('stellarator_tea.modules.mfe_lcoe_dcf.lcoe_dcf')
        yield factors, annual.Levelized_Annual_CostModule(), idc.IDC_Closed_Form_CostModule(), dcf.LCOE_DCFModule()
    finally:
        for path in added_paths:
            sys.path.remove(path)


def switch_rates(duration):
    boundary = .125 / max(1., abs(duration))
    return tuple(sign * value for sign in (-1, 1) for value in
                 (math.nextafter(boundary, 0.), boundary, math.nextafter(boundary, math.inf)))


@pytest.mark.parametrize('duration', DURATIONS)
def test_crf_idc_and_dated_periodic_factors(production, duration, record_property):
    factors, _, public_idc, _ = production
    switches = switch_rates(duration)
    record_property('switch_operands', repr([(i, duration, abs(i) * max(1., abs(duration)) <= .125) for i in switches]))
    for rate in RATES + switches:
        operands = (rate, duration)
        assert_finance(factors.crf(*operands), reference.crf(*operands), 'crf', operands)
        expected_idc = reference.idc(*operands)
        actual_idc = factors.idc(*operands)
        assert_finance(actual_idc, expected_idc, 'idc_factor', operands)
        cost = public_idc.run(overnight_cost=1e9, interest_rate=rate, construction_years_in=duration).data.root
        with localcontext() as context:
            context.prec = 100
            assert_finance(cost, Decimal('1e9') * expected_idc, 'idc_currency', operands)
        if not rate or duration == 1.:
            assert actual_idc == cost == 0.
        elif rate > 0 and duration < 1:
            assert actual_idc < 0 and cost < 0
        for count in (0., 1., 7.):
            for event_cost in (0., 1e6):
                args = (event_cost, rate, duration, count)
                assert_finance(factors.periodic_pv(*args), reference.periodic_pv(*args), 'periodic_pv', args)


def annuity_pairs():
    # Preserve requested deltas as well as actual represented operands; do not
    # silently deduplicate the .02 +/- 1e-18 requests that round to equality.
    pairs = [(i, g, None) for i in RATES + (-.02,) for g in RATES + (-.02,)]
    pairs += [(base, base + sign * 10. ** -power, sign * 10. ** -power)
              for base in (0., .02) for power in (4, 8, 12, 16, 18) for sign in (-1, 1)]
    return pairs


@pytest.mark.parametrize('n,t', [(n, t) for n in DURATIONS for t in (8., 8.5)]
                         + [(30., t) for t in DURATIONS if t not in (8., 8.5)])
def test_annuity_stream_pv_and_public_charges(production, n, t, record_property):
    factors, public_annual, _, _ = production
    represented = []
    for i, g, requested in annuity_pairs():
        if requested is not None:
            represented.append(dict(i=i, g=g, requested=requested, equal=i == g,
                                    actual_delta=str(Decimal(g) - Decimal(i))))
        args = (1e6, i, g, n, t)
        assert_finance(factors.annuity_pv(*args), reference.annuity_pv(*args), 'stream_pv', args)
        result = public_annual.run(annual_cost=1e6, interest_rate=i, inflation_rate_in=g,
                                  operational_years_in=n, project_time=t).data
        assert tuple(type(result).model_fields) == ('levelized', 'crf')
        assert_finance(result.crf, reference.crf(i, n), 'public_crf', args)
        assert_finance(result.levelized, reference.levelized(*args), 'public_levelized', args)
        if i == g == 0:
            assert_finance(result.levelized, Decimal('1e6'), 'zero_rate_charge', args)
    record_property('represented_rate_differences', repr(represented))


@pytest.mark.parametrize('n', (30., 30.5))
@pytest.mark.parametrize('t', DURATIONS)
def test_dcf_components_and_public_price(production, n, t):
    _, _, _, public_dcf = production
    for rate in RATES:
        expected = reference.dcf_components(1e9, 1e7, rate, n, t, 1000., .85)
        # Capture actual implementation locals at return to check components
        # before addition/division can conceal a defective intermediate factor.
        captured = {}
        def capture(frame, event, arg):
            if event == 'return' and frame.f_code.co_name == 'run_lcoe_dcf':
                captured.update(frame.f_locals)
        previous = sys.getprofile()
        try:
            sys.setprofile(capture)
            result = public_dcf.run(discount_rate_in=rate, availability_in=.85,
                construction_years_in=t, net_electric_mw=1000., annual_om_in=1e7,
                operational_years_in=n, total_capital_in=1e9).data.root
        finally:
            sys.setprofile(previous)
        operands = (rate, n, t)
        assert captured, 'Public wrapper did not execute its production handwritten implementation'
        for name, aliases in [('crf', ('crf', 'recovery', 'c')), ('midpoint', ('midpoint', 'idc_factor')),
                              ('annual_capital', ('annual_capital',)),
                              ('annual_energy', ('annual_energy', 'annual_energy_mwh'))]:
            actual = next((captured[key] for key in aliases if key in captured), None)
            assert actual is not None, (name, tuple(captured))
            assert_finance(actual, expected[name], name, operands)
        numerator = captured.get('numerator', captured['annual_capital'] + 1e7)
        assert_finance(numerator, expected['numerator'], 'dcf_numerator', operands)
        assert_finance(result, expected['lcoe'], 'public_dcf_price', operands)


def test_original_counterexamples_and_zero_cost(production):
    factors, annual, idc, dcf = production
    args = (1e6, .02, .02, 30., 8.)
    result = annual.run(annual_cost=1e6, interest_rate=.02, inflation_rate_in=.02,
                        operational_years_in=30., project_time=8.).data
    assert_finance(result.levelized, reference.levelized(*args), '$1M equal-rate regression', args)
    expected = reference.dcf_components(1e9, 1e7, 0., 30., 8., 1000., .85)
    result = dcf.run(discount_rate_in=0., availability_in=.85, construction_years_in=8.,
                     net_electric_mw=1000., annual_om_in=1e7, operational_years_in=30., total_capital_in=1e9).data.root
    assert_finance(result, expected['lcoe'], '$1B/$10M zero-rate regression', (0., 30., 8.))
    for rate in RATES:
        assert factors.annuity_pv(0., rate, rate, 30.5, 8.5) == 0.
        assert annual.run(annual_cost=0., interest_rate=rate, inflation_rate_in=rate,
                          operational_years_in=30.5, project_time=8.5).data.levelized == 0.
        assert idc.run(overnight_cost=0., interest_rate=rate, construction_years_in=8.5).data.root == 0.


def current_generation():
    """Load today's completion helper without shadowing historical regenerate imports."""
    from tests.models.current_mfe_regressions import current_generation as current
    return current()


@pytest.mark.parametrize('kind',['visible','hidden','file','symlink','dangling'])
def test_current_regeneration_refuses_nonfresh_without_mutation(tmp_path,kind):
    module=current_generation();target=tmp_path/'destination'
    if kind in ('symlink','dangling'):
        referent=tmp_path/'referent'
        if kind=='symlink':referent.mkdir()
        target.symlink_to(referent)
    elif kind=='file':target.write_text('retain')
    else:
        target.mkdir();(target/('.hidden' if kind=='hidden' else 'entry')).write_text('retain')
    before=target.readlink() if target.is_symlink() else target.read_bytes() if target.is_file() else module.hashes(target)
    with pytest.raises(FileExistsError):module.seed_and_generate(target,generator=lambda _:pytest.fail('generator called'))
    after=target.readlink() if target.is_symlink() else target.read_bytes() if target.is_file() else module.hashes(target)
    assert before==after


@pytest.mark.parametrize('kind',['missing','mismatch','extra','symlink'])
def test_current_regeneration_refuses_bad_seed(tmp_path,kind):
    import shutil
    module=current_generation();source=tmp_path/'source'
    for name in json.loads(module.SEEDS.read_text()):
        p=source/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(module.PRODUCTION/name,p)
    target=source/sorted(json.loads(module.SEEDS.read_text()))[0]
    if kind=='missing':target.unlink()
    elif kind=='mismatch':target.write_text('changed')
    elif kind=='extra':(source/'handwritten/extra.py').write_text('AUTO_IMPLEMENTED = False\n')
    else:
        target.unlink();target.symlink_to(module.PRODUCTION/sorted(json.loads(module.SEEDS.read_text()))[0])
    with pytest.raises(ValueError):module.seed_and_generate(tmp_path/'destination',source,generator=lambda _:pytest.fail('generator called'))
    assert not (tmp_path/'destination').exists() or not list((tmp_path/'destination').iterdir())
