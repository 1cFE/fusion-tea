"""Versioned preparation selection and first-attempt custody; no reference data."""
import importlib.util
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import pytest

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / '.project/active/model-evaluation-comparison-adapter/v1'
spec = importlib.util.spec_from_file_location('evaluation_adapter', DIRECTORY / 'adapter.py')
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


def request(values=None):
    return {'schema_version': 'adapter-request/v1', 'purpose': 'synthetic_preparation', 'values': values or {}}


def record(key, value):
    row = next(r for r in json.loads((DIRECTORY / 'mapping.json').read_text())['inputs'] if r['key'] == key)
    return {'value': value, 'unit': row['unit'], 'definition': row['definition'],
            'resolution': 'matched', 'source': 'synthetic test fixture; no reference source'}


@pytest.fixture
def base():
    return adapter.defaults(json.loads((adapter.PACKAGE / 'contracts/model_contract.json').read_text()))


def test_mapping_and_hardware_preservation(base):
    key = adapter.P + 'magnet__coil__turn_current'
    point, selected = adapter.select(request({key: record(key, 49000)}), base)
    assert point == {key: 49000.0}
    assert len(selected['effective_inputs']) == 704
    assert {k for k in base if base[k] != selected['effective_inputs'][k]} == {key}
    assert len(selected['missing_proposed_inputs']) == 7
    assert selected['held_fallback'] and not selected['fully_reference_specified']
    assert selected['input_roles'][key] == 'supplied'
    assert all(role == 'held' for k, role in selected['input_roles'].items() if k != key)


@pytest.mark.parametrize('bad', [True, False, float('nan'), float('inf'), '1'])
def test_non_numeric_refused(base, bad):
    key = adapter.P + 'plasma__R'
    with pytest.raises(ValueError, match='finite non-Boolean'):
        adapter.select(request({key: record(key, bad)}), base)


@pytest.mark.parametrize('field,value', [('definition', 'volume_average_density'), ('unit', 'cm^-3'), ('resolution', 'ambiguous')])
def test_definition_refused(base, field, value):
    key = adapter.P + 'plasma__n_e0'
    row = record(key, 5e20)
    row[field] = value
    with pytest.raises(ValueError, match='incompatible or ambiguous'):
        adapter.select(request({key: row}), base)


def test_retired_ampere_turns_and_sizing_refused(base):
    with pytest.raises(ValueError, match='ampere-turns'):
        adapter.select(request({adapter.P + 'magnet__coil__I_coil': {}}), base)
    with pytest.raises(ValueError, match='retired'):
        adapter.select(request({adapter.P + 'magnet__winding_pack__sizing_mode': 1}), base)


def test_strict_decode():
    for raw in ['{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}']:
        with pytest.raises(ValueError):
            adapter.strict(raw)


def test_atomic_first_reservation_and_duplicate(tmp_path):
    with ThreadPoolExecutor(max_workers=4) as pool:
        reservations = list(pool.map(lambda n: adapter.reserve(tmp_path, str(n)), range(4)))
    first = reservations[0][1]
    assert all(r[1] == first for r in reservations)
    initial = (tmp_path / 'first-attempt.json').read_bytes()
    with pytest.raises(FileExistsError):
        adapter.reserve(tmp_path, '0')
    assert (tmp_path / 'first-attempt.json').read_bytes() == initial


def test_corrupt_first_is_never_replaced(tmp_path):
    (tmp_path / 'first-attempt.json').write_text('{')
    with pytest.raises(ValueError):
        adapter.reserve(tmp_path, 'later')
    assert (tmp_path / 'first-attempt.json').read_text() == '{'


def test_interrupted_first_stays_first(tmp_path):
    first, identity = adapter.reserve(tmp_path, 'interrupted')
    assert not (first / 'result.json').exists()
    second, later = adapter.reserve(tmp_path, 'later')
    assert later == identity and later['attempt'] == 'interrupted'
    assert second.name == 'later'


def test_export_partial_is_unavailable_and_current_roles(base):
    key = adapter.P + 'magnet__coil__turn_current'
    calculated = adapter.P + 'magnet__winding_state__I_coil'
    manifest = {'quantities': [dict(id='calculated', producers=[calculated], unit='A-turn'),
                               dict(id='chosen', producers=[key], unit='A')]}
    native = dict(state='failed', effective_inputs=base, outputs={calculated: 15.4e6}, input_roles={k: 'held' for k in base})
    rows = adapter.export(native, manifest)['rows']
    assert all(r['value'] is None for r in rows)
    native['state'] = 'completed'
    rows = adapter.export(native, manifest)['rows']
    assert rows[0]['role'] == 'calculated' and rows[1]['role'] == 'held'
    assert all(not r['independent_prediction_credit'] for r in rows)


def test_refusal_custody_precedes_decode(tmp_path):
    raw = tmp_path / 'bad.json'
    raw.write_bytes(b'{')
    result = adapter.execute(raw, tmp_path / 'store', 'first')
    assert result['refusal_stage'] == 'request_decode'
    assert (tmp_path / 'store/first/request.raw.json').read_bytes() == b'{'
    receipt = json.loads((tmp_path / 'store/first/receipt.json').read_text())
    assert receipt['first_attempt']['attempt'] == 'first'
    with pytest.raises(FileExistsError):
        adapter.execute(raw, tmp_path / 'store', 'first')


def test_identity_drift_refuses_before_native(tmp_path, monkeypatch):
    monkeypatch.setattr(adapter, 'identity_files', lambda: {'changed.py': '0' * 64})
    raw = tmp_path / 'request.json'
    raw.write_text(json.dumps(request()))
    result = adapter.execute(raw, tmp_path / 'store', 'changed')
    assert result['refusal_stage'] == 'identity'
    assert 'identity drift' in result['error']
    assert not result['native_execution_started']
    assert all(r['value'] is None for r in json.loads((tmp_path / 'store/changed/model-export.json').read_text())['rows'])


def test_mass_migration_and_predicate_overlay(base):
    contract = json.loads((adapter.PACKAGE / 'contracts/model_contract.json').read_text())
    predicate = contract['constraint_catalog']['concrete_entries'][0]
    manifest = {'quantities': [dict(id='casing_mass', producers=['retired_casing_mass'], unit='kg'),
                               dict(id='constraint', producers=[predicate['evaluation_channel']], unit='1')]}
    native = dict(state='completed', effective_inputs=base, outputs={},
                  input_roles={k: 'held' for k in base}, verdicts={predicate['constraint_id']: 'violated'})
    rows = adapter.export(native, manifest, contract)['rows']
    assert rows[0]['value'] == base[adapter.P + 'magnet__casing__m_casing']
    assert rows[0]['role'] == 'held'
    assert rows[1]['value'] is False and rows[1]['role'] == 'calculated'


def test_unavailable_raw_values_remain_explicit(tmp_path):
    path = tmp_path / 'raw.json'
    adapter.document(path, {'partial': complex(1, 2), 'nan': float('nan')})
    raw = json.loads(path.read_text())
    assert raw['partial'] == {'unavailable_complex': '(1+2j)'}
    assert raw['nan'] == {'unavailable_nonfinite': 'nan'}


@pytest.mark.parametrize('flag,expected', [(0, 'undefined_prediction'), (None, 'unknown_prediction'), (2, 'unknown_prediction'), (1, 'mapped')])
def test_definedness_never_promotes_zero_carriers(base, flag, expected):
    value_key = adapter.P + 'blanket__breeding__tbr_mean'
    flag_key = adapter.P + 'blanket__breeding__defined_flag'
    outputs = {value_key: 0.0}
    if flag is not None:
        outputs[flag_key] = flag
    manifest = {'quantities': [dict(id='achieved_tbr', producers=[value_key], unit='1')]}
    native = dict(state='completed', effective_inputs=base, outputs=outputs, input_roles={k: 'held' for k in base})
    row = adapter.export(native, manifest)['rows'][0]
    assert row['status'] == expected and row['raw_value'] == 0.0
    assert row['value'] == (0.0 if flag == 1 else None)


def test_complete_synthetic_controls_are_not_reference_claim(base):
    keys = [r['key'] for r in json.loads((DIRECTORY / 'mapping.json').read_text())['inputs']]
    point, selection = adapter.select(request({k: record(k, base[k]) for k in keys}), base)
    assert set(point) == set(keys)
    assert selection['fully_specified_preparation_controls']
    assert not selection['fully_reference_specified'] and not selection['held_fallback']
