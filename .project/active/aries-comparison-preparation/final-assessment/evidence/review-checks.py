"""Independent reporting integrity checks; never evaluate a plant."""
import hashlib
import importlib.util
import json
import math
import contextlib
import io
import tarfile
import tempfile
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
BASE = HERE.parent.parent

def read(path):
    return json.loads(path.read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_build(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build()

original = read(BASE / 'partial-assessment/attempts/diagnostic-1/report.json')
quantities = read(HERE / 'quantity-rows.json')
costs = read(HERE / 'cost-rows.json')
combined = read(HERE / 'comparison-rows.json')
assert combined['row_count'] == 276
assert [r['original_row'] for r in combined['rows']] == original['rows']
assert len({r['id'] for r in combined['rows']}) == 276
assert load_build(HERE / 'quantity-review.py') == quantities
assert load_build(HERE / 'assemble.py') == combined
with tempfile.TemporaryDirectory(prefix='aries-review-cost-') as directory:
    code = (HERE / 'cost-assessment.py').read_text()
    statement = "OUT = BASE / 'final-assessment/evidence'"
    assert code.count(statement) == 1
    code = code.replace(statement, 'OUT = Path(' + repr(directory) + ')')
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(code, str(HERE / 'cost-assessment.py'), 'exec'), {'__name__': '__review__'})
    for name in ['cost-rows.json', 'cost-rows.csv', 'cost-frozen-excerpts.json']:
        assert (Path(directory) / name).read_bytes() == (HERE / name).read_bytes(), name
assert all(not r['independent_prediction_credit'] for r in combined['rows'])
original_by_id = {r['id']: r for r in original['rows']}
for row in quantities['rows']:
    prior = original_by_id[row['id']]
    assert row['model_value'] == prior['diagnostic_value']
    assert row['producers'] == prior['producers']
    if row['nominal_ratio'] is not None:
        assert row['nominal_ratio'] == row['model_value'] / row['reference_value']
for row in costs['rows']:
    prior = original_by_id[row['id']]
    assert row['model_raw_USD'] == prior['raw_arithmetic']
    assert row['producers'] == prior['producers']
    assert not row['scientific_comparison_eligible']
    if row['reference_raw_USD'] is not None:
        assert math.isclose(row['reference_raw_USD'], row['reference_raw_printed_MUSD'] * 1e6, rel_tol=1e-14)
        assert row['nominal_model_reference_ratio'] == row['model_raw_USD'] / row['reference_raw_USD']
        assert digest(ROOT / row['reference_image']) == row['reference_image_sha256']
assert next(r for r in costs['rows'] if r['id'] == 'C220107')['scientific_verdict'] == 'excluded'
identity = read(HERE / 'structure-identities.json')
archive = ROOT / identity['archive']
assert digest(archive) == identity['archive_sha256']
with tarfile.open(archive) as frozen:
    for item in identity['model_checks']:
        content = frozen.extractfile(item['path']).read()
        assert content == (ROOT / item['path']).read_bytes()
        assert hashlib.sha256(content).hexdigest() == item['frozen_sha256']
protected = read(HERE / 'preservation-before.json')['files']
changed = [name for name, sha in protected.items() if not (ROOT / name).exists() or digest(ROOT / name) != sha]
assert not changed, changed
result = {
    'scope': 'Independent retained-report arithmetic, full-row preservation, frozen model identity, and reporting replay; no plant evaluation',
    'original_rows_preserved': len(combined['rows']),
    'quantity_rows_checked': len(quantities['rows']),
    'cost_rows_checked': len(costs['rows']),
    'cost_nominal_band_counts': dict(Counter(r['descriptive_band_position'] for r in costs['rows'])),
    'frozen_model_files_checked': len(identity['model_checks']),
    'protected_files_checked': len(protected),
    'protected_files_changed': changed,
    'quantity_and_combined_reporting_replay': 'exact',
    'cost_reporting_replay_to_temporary_directory': 'byte_exact',
    'source_report_sha256': digest(BASE / 'partial-assessment/attempts/diagnostic-1/report.json'),
    'examined_artifacts': {p.name: digest(p) for p in [HERE.parent/'structure.md', HERE.parent/'quantities.md', HERE.parent/'costs.md', HERE.parent/'report.md', HERE.parent/'replay.md', HERE/'quantity-rows.json', HERE/'cost-rows.json', HERE/'comparison-rows.json', HERE/'preservation-after.json']},
}
(HERE / 'review-checks.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
