"""Independent integration identity and bounded selected-offer guard probes."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT))
from exploration.whole_plant_conversion.run import execute

HERE = Path(__file__).resolve().parent
E = ROOT / 'work/active/WI-098_whole-plant-conversion-comparison/evidence'
P = 'whole_plant_conversion__plant__'
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
build = json.loads((E / 'build/build-hashes.json').read_text())
checks = []
for path, expected in build['sources'].items():
    assert digest(ROOT / path) == expected, path
    checks.append(path)
package = ROOT / build['package']
for path, expected in build['package_tree'].items():
    assert digest(package / path) == expected, path
for record in build['completions']:
    assert digest(ROOT / record['target']) == record['target_sha256'], record['target']
development = json.loads((E / 'development-final/native/cases.json').read_text())['cases']
baseline = next(r for r in development if r['case'] == 'whole-baseline2500')
fingerprint = '6915694e74919ebb764445dfc7f0782eda85a9de29fa44c4b55ffa415c1eb30f'
assert {r['executable_fingerprint'] for r in development} == {fingerprint}
for name in ['native-check-final.json', 'native-behaviors-final.json']:
    receipt = json.loads((E / 'independent-verification' / name).read_text())
    assert receipt['receipts_sha256'] == digest(E / 'development-final/native/cases.json')
contract = json.loads((package / 'contracts/package_contract.json').read_text())
assert contract['executable_fingerprint'] == fingerprint
points = []
for name, changes in [
    ('negative-selected-cryo-quote', {'cryogenic_offer__quote_USD2025': -1.}),
    ('negative-quote-zero-factor', {'cryogenic_offer__quote_USD2025': -1., 'cryoplant_account__price_factor': 0.}),
    ('zero-selected-cold-rating', {'cryogenic_offer__cold_rating_W': 0.}),
]:
    inputs = baseline['effective_inputs'] | {P + key: value for key, value in changes.items()}
    points.append(dict(case=name, inputs=inputs))
rows = execute(points, HERE / 'integration-domain-probes')
assert all(r['state'] == 'failed' and 'nonnegative' in r['error'] for r in rows[:2])
zero = rows[2]
assert zero['state'] == 'completed'
assert any('cryogenic_demand__cold_margin' in k and v == 'violated' for k, v in zero['responses'].items())
result = dict(status='pass', executable=fingerprint, source_files_checked=len(checks),
              package_files_checked=len(build['package_tree']), installed_bodies_checked=len(build['completions']),
              development_receipt_sha256=digest(E / 'development-final/native/cases.json'),
              model_sha256=digest(ROOT / 'models/designs/whole_plant_conversion/plant.sysml'),
              library_sha256=digest(ROOT / 'models/library/analyses/whole_plant_conversion_accounts.sysml'),
              native_guards={r['case']:r['state'] for r in rows})
(HERE / 'integration-checks.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
