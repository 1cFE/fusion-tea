"""Independent winding-pack magnitudes, units and current adapter boundary."""

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

BEFORE = json.loads((ROOT / '.project/active/winding-pack-current-consumers/implementation/oracle-before.json').read_text())
INVALID = [
    ({'magnet_I_coil': -1.0}, 'I_coil must be finite and nonnegative'),
    ({'magnet_I_coil': -1.0, 'magnet_j_wp': -2.0}, 'I_coil must be finite and nonnegative'),
    ({'magnet_I_coil': math.nan}, 'I_coil must be finite and nonnegative'),
    ({'magnet_I_coil': math.inf}, 'I_coil must be finite and nonnegative'),
    ({'magnet_I_coil': -math.inf}, 'I_coil must be finite and nonnegative'),
    ({'magnet_j_wp': -1.0}, 'j_wp must be finite and positive'),
    ({'magnet_j_wp': 0.0}, 'j_wp must be finite and positive'),
    ({'magnet_j_wp': math.nan}, 'j_wp must be finite and positive'),
    ({'magnet_j_wp': math.inf}, 'j_wp must be finite and positive'),
    ({'magnet_j_wp': -math.inf}, 'j_wp must be finite and positive'),
    ({'magnet_I_coil': 0.0}, 'wp_side must be nonzero'),
]


@pytest.mark.parametrize('overrides,message', INVALID)
def test_invalid_public_oracle_inputs_are_deliberate(overrides, message):
    names = {value: key for key, value in oracle.ENTRY_KEY_TO_ORACLE_INPUT.items()}
    saved = dict(oracle.vs.IN)
    with pytest.raises(ValueError, match=message):
        oracle.evaluate(WI059_REPLAY | {names[name]: value for name, value in overrides.items()})
    assert oracle.vs.IN == saved


@pytest.mark.parametrize('current,density,side', [(0., 1., 0.), (1e6, 100., .1), (4e6, 100., .2), (4e6, 400., .1)])
def test_local_sizing_area_units_and_scale(current, density, side):
    actual = oracle.vs._winding_pack_side(current, density)
    assert actual == side
    assert (actual * 1000.) ** 2 * density == pytest.approx(current, rel=1e-12)
    assert oracle.vs._winding_pack_side(current * 4., density) == actual * 2.
    assert oracle.vs._winding_pack_side(current, density * 4.) == actual / 2.


@pytest.mark.parametrize('overrides,message', INVALID[:-1])
def test_local_sizing_invalid_magnitudes(overrides, message):
    values = {**oracle.vs.IN, **overrides}
    with pytest.raises(ValueError, match=message):
        oracle.vs._winding_pack_side(values['magnet_I_coil'], values['magnet_j_wp'])


def test_zero_field_is_rejected_by_sustainment_consumer():
    # Test the existing consumer directly; zero sizing is separately accepted above.
    with pytest.raises(RuntimeError, match='B_axis must be nonzero'):
        oracle.vs._sustainment(oracle.vs.IN, 1000., 0.)
    # A zero axis-field producer from a mapped linkage input reaches that guard too.
    with pytest.raises(RuntimeError, match='B_axis must be nonzero'):
        oracle.evaluate({oracle.P + 'magnet__coil__k_link': 0.})  # WI-057 (2026-09-13): the key carries its part's path


@pytest.mark.parametrize('row', BEFORE['controls'])
def test_valid_full_oracle_outputs_and_stress_units_preserved(row):
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
    side = oracle.vs._winding_pack_side(p['magnet_I_coil'], p['magnet_j_wp'])
    assert side**2 * 1e6 * p['magnet_j_wp'] == pytest.approx(p['magnet_I_coil'], rel=1e-12)
    # Substituting metre-sized side into I*B/side requires the explicit factor 1000.
    expected = 1000. * p['magnet_k_sigma'] * actual['B_peak'] * math.sqrt(p['magnet_I_coil'] * p['magnet_j_wp'])
    assert actual['sigma_wp'] == pytest.approx(expected, rel=1e-12)


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
    assert oracle.ENTRY_KEY_TO_ORACLE_INPUT[oracle.P + 'magnet__coil__I_coil'] == 'magnet_I_coil'
    assert oracle.ENTRY_KEY_TO_ORACLE_INPUT[oracle.P + 'magnet__winding_pack__j_wp'] == 'magnet_j_wp'
    with pytest.raises(oracle.OracleSeamError, match='no declared oracle mapping'):
        oracle.evaluate({oracle.P + 'winding_extra_input': 1.})


def test_current_native_winding_route_agrees_with_independent_oracle(tmp_path, stock_simkit_path):
    import study_route as route
    names = {value: key for key, value in oracle.ENTRY_KEY_TO_ORACLE_INPUT.items()}
    points = [WI059_REPLAY | {names[key]: value for key, value in row['overrides'].items()} for row in BEFORE['controls']]
    cases, _ = route.run_points('winding-consumer-controls', points, tmp_path)
    assert len(cases) == len(points)
    for case in cases:
        assert case.state == 'completed', (dict(case.inputs), case.state)
        expected = oracle.evaluate(case.inputs)
        assert len(case.outputs) == 177 + len(WI059_CHANNELS) and len(expected) == 161 + len(WI059_CHANNELS)  # WI-038 adds three grade outputs
        for key, value in expected.items():
            assert case.outputs[key] == pytest.approx(value, rel=1e-9, abs=1e-9), key
        if dict(case.inputs) == WI059_REPLAY:
            assert {key for key, value in route.short_verdicts(case).items() if value == 'violated'} == {'divertor_heat_ok'}
