"""Independent winding-pack magnitudes, units and current adapter boundary."""

import json
import math
import sys
from pathlib import Path

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
        oracle.evaluate({names[name]: value for name, value in overrides.items()})
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
        oracle.evaluate({oracle.P + 'magnet__k_link': 0.})


@pytest.mark.parametrize('row', BEFORE['controls'])
def test_valid_full_oracle_outputs_and_stress_units_preserved(row):
    actual = oracle._compute(row['overrides'])
    assert actual == row['outputs']
    p = {**oracle.vs.IN, **row['overrides']}
    side = oracle.vs._winding_pack_side(p['magnet_I_coil'], p['magnet_j_wp'])
    assert side**2 * 1e6 * p['magnet_j_wp'] == pytest.approx(p['magnet_I_coil'], rel=1e-12)
    # Substituting metre-sized side into I*B/side requires the explicit factor 1000.
    expected = 1000. * p['magnet_k_sigma'] * actual['B_peak'] * math.sqrt(p['magnet_I_coil'] * p['magnet_j_wp'])
    assert actual['sigma_wp'] == pytest.approx(expected, rel=1e-12)


def test_adapter_coverage_remains_exact():
    assert oracle.ENTRY_KEY_TO_ORACLE_INPUT == BEFORE['input_mapping']
    assert oracle.ORACLE_OUTPUT_TO_CHANNEL == BEFORE['output_mapping']
    assert oracle.ENTRY_KEY_TO_ORACLE_INPUT[oracle.P + 'magnet__I_coil'] == 'magnet_I_coil'
    assert oracle.ENTRY_KEY_TO_ORACLE_INPUT[oracle.P + 'magnet__j_wp'] == 'magnet_j_wp'
    with pytest.raises(oracle.OracleSeamError, match='no declared oracle mapping'):
        oracle.evaluate({oracle.P + 'winding_extra_input': 1.})


def test_current_native_winding_route_agrees_with_independent_oracle(tmp_path, stock_simkit_path):
    import study_route as route
    names = {value: key for key, value in oracle.ENTRY_KEY_TO_ORACLE_INPUT.items()}
    points = [{names[key]: value for key, value in row['overrides'].items()} for row in BEFORE['controls']]
    cases, _ = route.run_points('winding-consumer-controls', points, tmp_path)
    assert len(cases) == len(points)
    for case in cases:
        assert case.state == 'completed', (dict(case.inputs), case.state)
        expected = oracle.evaluate(case.inputs)
        assert len(case.outputs) == 158 and len(expected) == 141
        for key, value in expected.items():
            assert case.outputs[key] == pytest.approx(value, rel=1e-9, abs=1e-9), key
        if not case.inputs:
            assert {key for key, value in route.short_verdicts(case).items() if value == 'violated'} == {'divertor_heat_ok'}
