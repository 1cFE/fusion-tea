"""Fresh repaired native receipts; original study/development evidence stays unchanged."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
BASE = ROOT / 'exploration/exchanger_architecture/thermal_requirements'
STORE = BASE / 'studies/20260927-exchanger-thermal-comparison/results/native/20260927-exchanger-thermal-comparison.db'
spec = importlib.util.spec_from_file_location('repair_native_runner', BASE / 'run.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
preserved = [STORE, HERE / 'native-controls.json', HERE / 'oracle-native-verification.json']
before = {str(p.relative_to(ROOT)): sha(p) for p in preserved}
original = json.loads((HERE / 'native-controls.json').read_text())
# Replay exact complete saved maps, including all previously defaulted inputs.
cases = {r['case']: r['effective_inputs'] for r in original}
connection = sqlite3.connect('file:' + str(STORE.resolve()) + '?mode=ro', uri=True)
failed = list(connection.execute("select candidate_id, inputs_json from cases where state='execution_failed' order by candidate_id"))
connection.close()
assert len(failed) == 2
for cid, raw in failed:
    cases['repair-' + cid.rsplit(':', 1)[-1]] = json.loads(raw)
runtime = runner.load_runtime()
rows = []
for name, inputs in cases.items():
    row = runner.execute_case(name, inputs, runtime, HERE / 'repair-native-runs')
    assert row['effective_inputs'] == inputs
    rows.append(row)
    print(json.dumps({'case': name, 'status': row['status']}), flush=True)
(HERE / 'repair-native-controls.json').write_text(json.dumps(rows, indent=2) + '\n')
after = {str(p.relative_to(ROOT)): sha(p) for p in preserved}
assert before == after
assert all(r['status'] == 'evaluated' for r in rows)
(HERE / 'repair-preservation.json').write_text(json.dumps({'original_evidence_hashes': before, 'unchanged': True, 'new_cases': len(rows), 'fingerprint': runtime[2]}, indent=2) + '\n')
