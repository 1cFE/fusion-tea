"""Near-zero residuals need explicit accuracy without weakening other comparisons."""
import copy
import json
from pathlib import Path
from types import SimpleNamespace

import jsonschema
import pytest

from scripts.study import manifest, verify

ROOT = Path(__file__).resolve().parents[2]
DECLARATION = {'channel': 'residual', 'value': 1e-7, 'units': 'MW',
               'basis': '1e-8 MW closure termination plus rounding; below 1e-6 MW engineering tolerance'}


def document():
    return json.loads((ROOT / 'exploration/ife_e2e/studies/manifest.json').read_text())


def run_check(got=7.539028956671245e-9, expected=9.094947017729282e-13, tolerances=None,
              other_got=100.0, verdict='satisfied'):
    case = SimpleNamespace(candidate_id='residual-case', executable_fingerprint='pin', inputs={},
                           outputs={'residual': got, 'other': other_got}, verdicts={'balance': verdict})
    catalog = {'balance': {'source_local_identity': 'balance', 'predicate_ir': json.dumps({
        'kind': 'operator', 'operator': '<=', 'operands': [
            {'kind': 'feature_ref', 'reference': {'source_name': 'residual'}},
            {'kind': 'literal', 'literal': {'value': 1e-6}}]})}}
    bindings = {'balance': {'residual': {'kind': 'channel', 'key': 'residual'}}}
    return verify.check_case(case, lambda _: {'residual': expected, 'other': 100.0},
                             bindings, catalog, {'other': 'power'}, {}, 'pin', tolerances)


def test_actual_native_roundoff_requires_named_declaration():
    with pytest.raises(verify.VerifyError, match='channel off tolerance'):
        run_check()
    worst, compared, rederived, _ = run_check(tolerances={'residual': 1e-7})
    assert worst[0] > 8000  # Actual relative discrepancy remains visible.
    assert set(compared) == {'residual', 'other'}
    assert rederived[0]['constraint_id'] == 'balance'


@pytest.mark.parametrize('got', [1e-7, 2e-7])
def test_absolute_boundary_is_strict_and_excess_refuses(got):
    with pytest.raises(verify.VerifyError, match='channel off tolerance'):
        run_check(got=got, expected=0.0, tolerances={'residual': 1e-7})


def test_absolute_declaration_does_not_relax_other_channels_or_verdicts():
    with pytest.raises(verify.VerifyError, match='channel off tolerance'):
        run_check(tolerances={'residual': 1e-7}, other_got=101.0)
    with pytest.raises(verify.VerifyError, match='verdict mismatch'):
        run_check(tolerances={'residual': 1e-7}, verdict='violated')


def test_unknown_or_unused_tolerance_refuses():
    with pytest.raises(verify.VerifyError, match='unchecked channels'):
        run_check(tolerances={'misspelled': 1e-7})


@pytest.mark.parametrize('value', [float('nan'), float('inf'), -float('inf')])
@pytest.mark.parametrize('side', ['got', 'expected'])
def test_nonfinite_values_never_pass_absolute_rule(value, side):
    with pytest.raises(verify.VerifyError, match='nonfinite'):
        run_check(**{side: value}, tolerances={'residual': 1e-7})


def test_native_manifest_and_schema_accept_explicit_declaration():
    doc = document()
    doc['absolute_tolerances'] = [copy.deepcopy(DECLARATION)]
    manifest.validate(doc)
    schema = json.loads((ROOT / 'scripts/study/schemas/study_package_manifest.v1.schema.json').read_text())
    jsonschema.validate(doc, schema)
    manifest.validate(document())  # Old manifests remain valid.


@pytest.mark.parametrize('value', [0, -1, True, float('nan'), float('inf'), '1e-7'])
def test_invalid_tolerance_values_refuse(value):
    doc = document()
    doc['absolute_tolerances'] = [{**DECLARATION, 'value': value}]
    with pytest.raises(manifest.ManifestError):
        manifest.validate(doc)


@pytest.mark.parametrize('change', ['duplicate', 'units', 'basis', 'extra'])
def test_declarations_require_unique_channels_and_complete_basis(change):
    doc = document()
    doc['absolute_tolerances'] = [copy.deepcopy(DECLARATION)]
    if change == 'duplicate':
        doc['absolute_tolerances'].append(copy.deepcopy(DECLARATION))
    elif change == 'extra':
        doc['absolute_tolerances'][0]['implicit'] = True
    else:
        doc['absolute_tolerances'][0][change] = ' '
    with pytest.raises(manifest.ManifestError):
        manifest.validate(doc)
