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
    assert actual.keys() == expected.keys()
    for name, value in expected.items():
        if name in changed:
            assert actual[name] == pytest.approx(value, rel=1e-12, abs=1e-9), name
        else:
            assert actual[name] == value, name
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
    old_inputs = renamed_keys(BEFORE['input_mapping'])
    # WI-058 (2026-09-14): the seam maps c_coil_ref in place of the retired k_coil.
    assert WI058_RETIRED <= old_inputs.keys()
    old_inputs = {k: v for k, v in old_inputs.items() if k not in WI058_RETIRED}
    assert {k: v for k, v in oracle.ENTRY_KEY_TO_ORACLE_INPUT.items() if k not in WI040_PARAMETERS | WI038_PARAMETERS | WI058_PARAMETERS | WI059_PARAMETERS | WI059_EXISTING_MAPPED_PARAMETERS | WI060_PARAMETERS} == old_inputs
    assert oracle.ENTRY_KEY_TO_ORACLE_INPUT.keys() - old_inputs.keys() == WI040_PARAMETERS | WI038_PARAMETERS | WI058_PARAMETERS | WI059_PARAMETERS | WI059_EXISTING_MAPPED_PARAMETERS | WI060_PARAMETERS
    old_outputs = renamed_values(BEFORE['output_mapping'])
    old_outputs['winding_pack_legacy'] = old_outputs.pop('winding_pack')
    old_outputs['p_cryo'] = oracle.P + 'cryoplant__refrigeration_sum__total'
    extras = WI040_CHANNELS | LIVE_CONDUCTOR_CHANNELS | WI059_ORACLE_ADDED_CHANNELS | {oracle.P + 'reactor_equipment_subtotal__reactor_equipment_subtotal'}
    assert {k: v for k, v in oracle.ORACLE_OUTPUT_TO_CHANNEL.items() if v not in extras} == old_outputs
    assert set(oracle.ORACLE_OUTPUT_TO_CHANNEL.values()) - set(old_outputs.values()) == extras
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
    for case in cases:
        assert case.state == 'completed', (dict(case.inputs), case.state)
        expected = oracle.evaluate(case.inputs)
        assert len(case.outputs) == 177 + len(WI059_CHANNELS) and len(expected) == 161 + len(WI059_CHANNELS)  # WI-038 adds three grade outputs
        for key, value in expected.items():
            assert case.outputs[key] == pytest.approx(value, rel=1e-9, abs=1e-9), key
        if dict(case.inputs) == WI059_REPLAY:
            assert {key for key, value in route.short_verdicts(case).items() if value == 'violated'} == {'divertor_heat_ok'}
