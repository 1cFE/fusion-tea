"""Independent primary-loop denominator, heat-flow and dormant-mode contract."""

import json
import math
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'exploration/stellarator_e2e/studies'))
import oracle_entry as oracle

BEFORE = json.loads((ROOT / '.project/active/primary-loop-current-consumers/implementation/oracle-before.json').read_text())
INVALID = [({key: value}, message) for key, message in (
    ('loop_cp', 'cp must be finite and positive'),
    ('loop_dT_blanket', 'dT_blanket must be finite and positive'),
) for value in (0., -1., math.nan, math.inf, -math.inf)] + [
    ({'loop_cp': -5193., 'loop_dT_blanket': -200.}, 'cp must be finite and positive')]


@pytest.mark.parametrize('live', [0., 1.])
@pytest.mark.parametrize('overrides,message', INVALID)
def test_invalid_public_denominators_are_deliberate(overrides, message, live):
    names = {value: key for key, value in oracle.ENTRY_KEY_TO_ORACLE_INPUT.items()}
    saved = dict(oracle.vs.IN)
    point = {names[key]: value for key, value in {**overrides, 'loop_live': live}.items()}
    with pytest.raises(ValueError, match=message):
        oracle.evaluate(point)
    assert oracle.vs.IN == saved


@pytest.mark.parametrize('source_heat', [0., 1000.])
@pytest.mark.parametrize('overrides,message', INVALID)
def test_local_invalid_denominators_include_zero_source(source_heat, overrides, message):
    values = {**oracle.vs.IN, **overrides}
    with pytest.raises(ValueError, match=message):
        oracle.vs._primary_loop_mass_flow(source_heat, values['loop_cp'], values['loop_dT_blanket'])


@pytest.mark.parametrize('source_heat,cp,rise,expected', [(0., 5000., 200., 0.), (1000., 5000., 200., 1000.), (2000., 5000., 200., 2000.)])
def test_local_heat_units_and_inverse_scaling(source_heat, cp, rise, expected):
    flow = oracle.vs._primary_loop_mass_flow(source_heat, cp, rise)
    assert flow == expected
    assert flow * cp * rise == pytest.approx(source_heat * 1e6, rel=1e-12)
    assert oracle.vs._primary_loop_mass_flow(source_heat, cp * 2., rise) == flow / 2.
    assert oracle.vs._primary_loop_mass_flow(source_heat, cp, rise * 2.) == flow / 2.


@pytest.mark.parametrize('row', BEFORE['controls'])
def test_valid_full_oracle_outputs_and_heat_accounting(row):
    actual = oracle._compute(row['overrides'])
    assert actual == row['outputs']
    p = {**oracle.vs.IN, **row['overrides']}
    assert actual['loop_mdot'] * p['loop_cp'] * p['loop_dT_blanket'] == pytest.approx(actual['q_source'] * 1e6, rel=1e-12)
    assert actual['loop_mdot_loop'] * p['n_loops'] == pytest.approx(actual['loop_mdot'], rel=1e-12)
    assert actual['loop_q_ihx'] - actual['q_source'] == pytest.approx(actual['loop_w_fluid'], rel=1e-12)
    assert actual['loop_p_elec'] * p['eta_drive'] == pytest.approx(actual['loop_w_fluid'], rel=1e-12)
    if p['loop_live'] == 0.:
        baseline = BEFORE['controls'][0]['outputs']
        for key in ('loop_mdot', 'loop_w_fluid', 'loop_p_elec', 'loop_q_ihx'):
            assert actual[key] == baseline[key]
        assert actual['loop_p_pump_total'] == 10.
        assert actual['loop_q_recovered_total'] == 8.


def test_adapter_coverage_remains_exact():
    assert oracle.ENTRY_KEY_TO_ORACLE_INPUT == BEFORE['input_mapping']
    assert oracle.ORACLE_OUTPUT_TO_CHANNEL == BEFORE['output_mapping']
    assert oracle.ENTRY_KEY_TO_ORACLE_INPUT[oracle.P + 'loop_cp'] == 'loop_cp'
    assert oracle.ENTRY_KEY_TO_ORACLE_INPUT[oracle.P + 'loop_dT_blanket'] == 'loop_dT_blanket'
    with pytest.raises(oracle.OracleSeamError, match='no declared oracle mapping'):
        oracle.evaluate({oracle.P + 'primary_loop_extra_input': 1.})


def test_current_native_primary_route_agrees_with_independent_oracle(tmp_path, stock_simkit_path):
    import study_route as route
    names = {value: key for key, value in oracle.ENTRY_KEY_TO_ORACLE_INPUT.items()}
    points = [{names[key]: value for key, value in row['overrides'].items()} for row in BEFORE['controls']]
    cases, _ = route.run_points('primary-loop-consumer-controls', points, tmp_path)
    assert len(cases) == len(points)
    for case in cases:
        assert case.state == 'completed', (dict(case.inputs), case.state)
        expected = oracle.evaluate(case.inputs)
        assert len(case.outputs) == 158 and len(expected) == 141
        for key, value in expected.items():
            assert case.outputs[key] == pytest.approx(value, rel=1e-9, abs=1e-9), key
        if not case.inputs:
            assert {key for key, value in route.short_verdicts(case).items() if value == 'violated'} == {'divertor_heat_ok'}
