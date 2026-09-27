"""Numerical regressions for the approved continuous counterflow evaluator."""
import importlib.util
import json
from pathlib import Path

import mpmath as mp
import pytest

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[2]
EVIDENCE = ROOT / 'work/active/WI-097_exchanger-thermal-requirements/evidence'
spec = importlib.util.spec_from_file_location('repair_regression_body', BASE / 'bodies/controlled_exchanger_closure/controlled_network_heat_driven_closure_impl.py')
body = importlib.util.module_from_spec(spec)
spec.loader.exec_module(body)


def precise(ua, ch, cs):
    # Independent high-precision transfer relation; no binary64 equality cutoff.
    with mp.workdps(120):
        ua, ch, cs = map(mp.mpf, (ua, ch, cs))
        if ch == cs:
            return ua * ch / (ua + ch)
        factor = mp.exp(ua * (1 / cs - 1 / ch))
        return (factor - 1) / (factor / cs - 1 / ch)


OFFSETS = [-1e-4, -1e-6, -1e-8, -2e-10, -1.0001e-10, -.9999e-10, -5e-11, 0., 5e-11, .9999e-10, 1.0001e-10, 2e-10, 1e-8, 1e-6, 1e-4]


@pytest.mark.parametrize('delta', OFFSETS)
def test_continuous_conductance_against_precise_transfer(delta):
    ch = 6. * (1 + delta)
    assert body.conductance(18., ch, 6.) == pytest.approx(float(precise(18., ch, 6.)), abs=2e-15, rel=0)


@pytest.mark.parametrize('delta', OFFSETS[3:12])
def test_bypass_root_near_capacity_equality(delta):
    duty = float(precise(18., 6. * (1 + delta), 6.) * 300.)
    result = body.bypass_stage(duty, 18., 12., 6., 800., 500.)
    active = (1 - result['bypass_fraction']) * 12.
    with mp.workdps(120):
        residual = precise(18., active, 6.) * 300 - duty
    assert abs(residual) <= 1e-10
    assert result['transferred'] == duty


@pytest.mark.parametrize('index', [0, 1])
def test_captured_native_trial_root(index):
    probe = json.loads((EVIDENCE / 'numerical-repair-probe.json').read_text())
    stage = probe['failed_cases'][index]['captured_exceptions'][-1]['state']
    q, ua, ch, cs, hot, tin = [stage[k] for k in ('q_available', 'ua', 'ch', 'cs', 'hot', 'secondary')]
    result = body.bypass_stage(q, ua, ch, cs, hot, tin)
    with mp.workdps(120):
        residual = precise(ua, (1 - result['bypass_fraction']) * ch, cs) * mp.mpf(hot - tin) - q
    assert abs(residual) <= 1e-10
    assert result['transferred'] == q


def test_repaired_full_native_maps_and_legacy_preservation():
    old = {r['case']: r for r in json.loads((EVIDENCE / 'native-controls.json').read_text())}
    rows = {r['case']: r for r in json.loads((EVIDENCE / 'repair-native-controls.json').read_text())}
    assert len(rows) == 20
    legacy_count = 0
    for name, row in rows.items():
        assert row['status'] == 'evaluated'
        verdicts = {v['constraint_id']: v['status'] for v in row['outputs']['constraint_report']['results']}
        assert len(verdicts) == 35
        if name.startswith('repair-'):
            assert set(verdicts.values()) == {'satisfied'}
            continue
        original = old[name]
        assert row['effective_inputs'] == original['effective_inputs']
        old_verdicts = {v['constraint_id']: v['status'] for v in original['outputs']['constraint_report']['results']}
        assert verdicts == old_verdicts
        if name.startswith('replay-'):
            legacy_count += 1
            assert row['outputs'] == original['outputs']
        for key, value in original['outputs'].items():
            if '__purchase__' in key:
                assert row['outputs'][key] == value
    assert legacy_count == 7
