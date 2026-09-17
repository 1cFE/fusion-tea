"""Synthetic policy checks; no physical or reference cases are executed."""
import importlib.util
import json
import math
from pathlib import Path

import pytest

HOME = Path(__file__).resolve().parents[1] / '.project/active/aries-comparison-preparation/package'
SPEC = importlib.util.spec_from_file_location('execute_frozen', HOME / 'execute_frozen.py')
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)
RULES = json.loads((HOME / 'input-rules.json').read_text())
KEY = RULES['independent_reference_inputs'][0]['key']
PREFIX = RULES['prefix']


def record(value=2.0):
    return {'value': value, 'unit': 'm', 'source': 'synthetic fixture',
            'definition': 'synthetic major radius', 'resolution': 'matched'}


def test_only_declared_mode_changes_at_verification():
    point, info = MOD.select_inputs(RULES, {'run_kind': 'verification'})
    assert point == RULES['forward_overrides']
    assert info['run_kind'] == 'verification'
    assert not info['held_fallback']


def test_forward_exact_profiles_preserve_geometry_current_and_reserve():
    point, info = MOD.select_inputs(RULES, {'run_kind': 'verification'})
    effective = {**RULES['default_values'], **point}
    expected = {'plasma__alpha_n': 0.35, 'plasma__alpha_T': 1.2,
                'plasma__R': 12.7, 'plasma__a': 1.3, 'plasma__f_shape': 1.0031567,
                'magnet__coil__I_coil': 15.4e6,
                'magnet__winding_pack__sizing_mode': 1,
                'magnet__winding_pack__inventory_multiplier': 1}
    assert {k: effective[PREFIX + k] for k in expected} == expected
    assert len(RULES['independent_reference_inputs']) == 7
    assert not info['conditioned_input_keys']


@pytest.mark.parametrize('suffix', ['plasma__alpha_n', 'plasma__alpha_T', 'plasma__f_shape'])
def test_blind_profile_and_shape_overrides_refuse(suffix):
    with pytest.raises(ValueError, match='not a permitted independent input'):
        MOD.select_inputs(RULES, {'run_kind': 'blind', 'values': {PREFIX + suffix: record()}})


def table5_request():
    return {'run_kind': 'conditioned', 'conditioned_seam': 'table5_geometry_field'}


def test_table5_control_fixed_values_roles_and_no_silent_overlap():
    point, info = MOD.select_inputs(RULES, table5_request())
    assert point[PREFIX + 'plasma__R'] == 12.74
    assert point[PREFIX + 'plasma__a'] == 1.3
    assert point[PREFIX + 'plasma__f_shape'] == 425 / (2 * math.pi**2 * 12.74 * 1.3**2)
    assert point[PREFIX + 'magnet__coil__I_coil'] == 15.4e6 * (12.74 / 12.7)
    assert point[PREFIX + 'plasma__alpha_n'] == 0.35
    assert point[PREFIX + 'plasma__alpha_T'] == 1.2
    assert len(info['conditioned_input_keys']) == 6
    assert info['conditioned_input_roles'][PREFIX + 'plasma__f_shape'] == 'derived_from_supplied_volume'
    assert info['conditioned_input_roles'][PREFIX + 'magnet__coil__I_coil'] == 'derived_from_supplied_field'
    quantities = info['conditioned_supplied_quantities']
    assert quantities['axis_field']['value'] == 9
    assert quantities['plasma_volume']['value'] == 425
    assert all(q['role'] == 'supplied' and not q['independent_prediction_credit'] for q in quantities.values())
    with pytest.raises(ValueError, match='overlap'):
        MOD.select_inputs(RULES, {**table5_request(), 'values': {KEY: record()}})
    with pytest.raises(ValueError, match='exactly'):
        MOD.select_inputs(RULES, {**table5_request(), 'conditioned_values': {KEY: 13}})


def test_supplied_inputs_and_missing_fallback_are_visible():
    point, info = MOD.select_inputs(RULES, {'run_kind': 'blind', 'values': {KEY: record()}})
    assert point[KEY] == 2.0
    assert info['supplied_input_keys'] == [KEY]
    assert len(info['missing_independent_inputs']) == 6
    assert info['held_fallback']
    assert not info['independent_prediction_credit_for_supplied']


@pytest.mark.parametrize('value', [True, None, float('nan'), float('inf'), '2'])
def test_invalid_numeric_inputs_refuse(value):
    with pytest.raises(ValueError):
        MOD.select_inputs(RULES, {'run_kind': 'blind', 'values': {KEY: record(value)}})


@pytest.mark.parametrize('change', [{'unit': 'cm'}, {'source': ''}, {'definition': ''},
                                  {'resolution': 'unresolved'}, {'role': 'independent'}])
def test_evidence_conversion_and_role_bypasses_refuse(change):
    with pytest.raises(ValueError):
        MOD.select_inputs(RULES, {'run_kind': 'blind', 'values': {KEY: {**record(), **change}}})


def test_unlisted_parameter_and_blind_conditioning_refuse():
    with pytest.raises(ValueError):
        MOD.select_inputs(RULES, {'run_kind': 'blind', 'values': {'B_max': record()}})
    with pytest.raises(ValueError):
        MOD.select_inputs(RULES, {'run_kind': 'blind', 'conditioned_seam': 'legacy_inventory'})
    with pytest.raises(ValueError):
        MOD.select_inputs(RULES, {'run_kind': 'verification', 'values': {KEY: record()}})


def test_conditioned_mode_is_separate_and_seam_limited():
    point, info = MOD.select_inputs(RULES, {'run_kind': 'conditioned', 'conditioned_seam': 'legacy_inventory'})
    assert point[PREFIX + 'magnet__winding_pack__sizing_mode'] == 0
    assert info['run_kind'] == 'conditioned'
    with pytest.raises(ValueError):
        MOD.select_inputs(RULES, {'run_kind': 'conditioned', 'conditioned_seam': 'held_pump'})
    with pytest.raises(ValueError):
        MOD.select_inputs(RULES, {'run_kind': 'conditioned', 'conditioned_seam': 'legacy_inventory',
                                 'conditioned_values': {'B_max': 99}})


def exporter():
    spec = importlib.util.spec_from_file_location('export_model_values', HOME / 'export_model_values.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def model_fixture():
    manifest = json.loads((HOME / 'manifest.json').read_text())
    root = HOME.parents[3]
    contract = json.loads((root / manifest['package_path'] / 'contracts/model_contract.json').read_text())
    native = json.loads((HOME / 'selected-mode/native-result.json').read_text())
    return manifest, contract, native


def test_actual_mapping_preserves_missing_mass_and_raw_power_balance():
    manifest, contract, native = model_fixture()
    mapped = exporter().extract(manifest, contract, native)
    rows = {r['id']: r for r in mapped['quantities']}
    assert len(rows) == len(manifest['quantities'])
    assert rows['coil_mass_complete']['model_value'] is None
    assert rows['coil_mass_complete']['status'] == 'not_produced'
    assert all(r['reference_value'] is None for r in rows.values())
    producers = next(q['producers'] for q in manifest['quantities'] if q['id'] == 'recirculating_power')
    assert rows['recirculating_power']['model_value'] == native['outputs'][producers[0]] - native['outputs'][producers[1]]
    assert rows['major_radius']['role_at_this_point'] == 'held'
    assert not any(row['status'] == 'missing_producer' for row in rows.values())
    assert rows['constraint_reference_conductor_current_ok']['model_value'] == 0


def test_refused_native_execution_cannot_map_defaults_as_predictions():
    manifest, contract, native = model_fixture()
    native['state'] = 'failed'
    result = exporter().extract(manifest, contract, native)
    assert all(q['model_value'] is None and q['status'] == 'execution_not_completed' for q in result['quantities'])


def test_missing_native_output_stays_missing():
    manifest, contract, native = model_fixture()
    row = next(q for q in manifest['quantities'] if q['id'] == 'recirculating_power')
    native['outputs'].pop(row['producers'][0])
    result = exporter().extract(manifest, contract, native)
    mapped = next(q for q in result['quantities'] if q['id'] == row['id'])
    assert mapped['model_value'] is None and mapped['status'] == 'missing_producer'


def test_supplied_geometry_output_alias_is_not_a_prediction():
    manifest, contract, native = model_fixture()
    cavity = next(q for q in manifest['quantities'] if q['id'] == 'fit_cavity_y')
    native['supplied_input_keys'] = [cavity['role_input']]
    result = exporter().extract(manifest, contract, native)
    rows = {q['id']: q for q in result['quantities']}
    assert rows['fit_cavity_y']['role_at_this_point'] == 'supplied'
    assert rows['fit_exterior_x']['role_at_this_point'] == 'held'
    assert rows['installed_wallplug']['role_at_this_point'] == 'held'


def test_conditioned_native_export_preserves_fixed_controls_and_field_alias_no_credit():
    manifest, contract, native = model_fixture()
    point, info = MOD.select_inputs(RULES, table5_request())
    # Classification check only: retained numeric outputs are a synthetic fixture,
    # not a claim to have executed the Table5 control here.
    native.update(info, requested_overrides=point)
    result = exporter().extract(manifest, contract, native)
    rows = {q['id']: q for q in result['quantities']}
    assert len(rows) == 174
    assert len(result['constraints']) == 20
    assert rows['major_radius']['model_value'] == 12.74
    assert rows['major_radius']['role_at_this_point'] == 'supplied'
    assert rows['minor_radius']['role_at_this_point'] == 'supplied'
    assert rows['peak_field']['conditioning'] == 'derived_from_supplied_field'
    assert not any(q['independent_prediction_credit'] for q in rows.values())
    assert result['conditioned_output_roles'][PREFIX + 'magnet__field_calc__B_axis'] == 'supplied'
    assert result['conditioned_supplied_quantities']['plasma_volume']['role'] == 'supplied'
    assert not result['conditioned_supplied_quantities']['plasma_volume']['independent_prediction_credit']
    assert all(q['reference_value'] is None for q in rows.values())
