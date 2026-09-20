"""Independent primary-loop denominator, heat-flow and dormant-mode contract."""

import json
import math
import sys
from pathlib import Path
from tests.study.structure_ledger import renamed_keys, renamed_values
from tests.study.test_domain_consumers import wi040_expected
from tests.models.current_mfe_regressions import (WI040_PARAMETERS, WI040_CHANNELS, WI038_PARAMETERS,
                                                  WI058_PARAMETERS, WI058_RETIRED)


from tests.models.current_mfe_regressions import WI059_PARAMETERS, WI059_EXISTING_MAPPED_PARAMETERS, WI059_CHANNELS, WI059_ORACLE_ADDED_CHANNELS, WI059_REPLAY, wi059_replay

from tests.models.current_mfe_regressions import WI060_PARAMETERS, LIVE_CONDUCTOR_CHANNELS

import pytest
from tests.models.current_mfe_regressions import PARTITION_PATH, extend_cycle_fixture, ADDITIONAL_MAPPING, CURRENT_NUMERIC, assert_current_predicates
PRIMARY_PARTITIONS={k:extend_cycle_fixture(v) for k,v in json.loads((PARTITION_PATH.parent/"primary-loop-partitions.json").read_text())["fixture_partitions"].items()}

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
    actual = oracle._compute(wi059_replay(row['overrides']))
    # WI-040: independently derive only the additive-account cost increments;
    # all frozen physics and unrelated output values retain exact comparison.
    expected, changed = wi040_expected(row)
    part=PRIMARY_PARTITIONS[str(BEFORE['controls'].index(row))]
    unchanged=set(part['unaffected_exact_locals']); changed_names=set(part['changed_current_equation_locals'])
    assert set(row['outputs'])==unchanged | changed_names
    assert set(actual)==set(row['outputs']) | set(part['added_local_names'])
    for name in unchanged:
        assert actual[name]==row['outputs'][name],name
    for name in changed | changed_names:
        value=actual['breeding_tbr_mean']-actual['fuel_tbr_required'] if name=='fuel_tbr_margin' else expected[name]
        assert actual[name]==pytest.approx(value,rel=1e-12,abs=1e-9),name
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
    assert set(oracle.ENTRY_KEY_TO_ORACLE_INPUT)==set(ADDITIONAL_MAPPING['mapped_input_keys'])
    for key,value in ADDITIONAL_MAPPING['unchanged_input_bindings'].items():
        assert oracle.ENTRY_KEY_TO_ORACLE_INPUT[key]==value,key
    expected=ADDITIONAL_MAPPING['historical_output_bindings_after_explicit_alias_translation'] | ADDITIONAL_MAPPING['added_output_bindings']
    assert oracle.ORACLE_OUTPUT_TO_CHANNEL==expected
    assert set(expected.values())==CURRENT_NUMERIC
    assert len(expected)==len(set(expected.values()))
    assert oracle.ENTRY_KEY_TO_ORACLE_INPUT[oracle.P + 'heat_transport__loop_cp'] == 'loop_cp'
    assert oracle.ENTRY_KEY_TO_ORACLE_INPUT[oracle.P + 'heat_transport__loop_dT_blanket'] == 'loop_dT_blanket'
    with pytest.raises(oracle.OracleSeamError, match='no declared oracle mapping'):
        oracle.evaluate({oracle.P + 'primary_loop_extra_input': 1.})


def test_current_native_primary_route_agrees_with_independent_oracle(tmp_path, stock_simkit_path):
    import study_route as route
    names = {value: key for key, value in oracle.ENTRY_KEY_TO_ORACLE_INPUT.items()}
    points = [WI059_REPLAY | {names[key]: value for key, value in row['overrides'].items()} for row in BEFORE['controls']]
    cases, _ = route.run_points('primary-loop-consumer-controls', points, tmp_path)
    assert len(cases) == len(points)
    from types import SimpleNamespace
    for case,point in zip(cases,points):
        assert case.state == 'completed', (dict(case.inputs), case.state)
        expected = oracle.evaluate(case.inputs)
        assert set(case.outputs)==set(expected)==CURRENT_NUMERIC  # WI-038 adds three grade outputs
        for key, value in expected.items():
            assert case.outputs[key] == pytest.approx(value, rel=1e-9, abs=1e-9), key
        assert_current_predicates(SimpleNamespace(outputs=case.outputs,responses=dict(case.verdicts,headline=case.headline)),point)
        if point == WI059_REPLAY:
            assert {key for key, value in route.short_verdicts(case).items() if value == 'violated'} == {'divertor_heat_ok','wp_fit_ok','reference_conductor_current_ok','tbr_ok'}
