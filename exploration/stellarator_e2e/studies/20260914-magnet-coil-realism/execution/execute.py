"""Runbook step 9: run every point of every arm through the stock teax lifecycle; export complete evidence."""
import csv, json, sys, time, subprocess
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from exploration.stellarator_e2e.studies import study_route as route
from scripts.study import preflight, verify
from simkit.study.store import StudyStore
H = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(H)); import study
R = H / 'results'
def write(p, data): p.write_text(json.dumps(data, indent=2, allow_nan=False) + '\n')
def key(p): return json.dumps({k: float(v) for k, v in dict(p).items()}, sort_keys=True, separators=(',', ':'))
assert json.loads((R / 'preflight_results.json').read_text())['outcome'] == 'pass'
clean = preflight.run_clean(route.PACKAGE_DIR); write(R / 'execution-clean-before.json', clean); assert clean['outcome'] == 'pass'
route.write_identity_document(route.PACKAGE_DIR, R / 'execution-package-identity.json')
assert json.loads((R / 'execution-package-identity.json').read_text()) == json.loads((R / 'package_identity.json').read_text())
props = json.loads((H / 'preparation/proposals.json').read_text())
channels = study.channels(); catalog = route._catalog_by_constraint_id(route.PACKAGE_DIR)
INPUTS = ['plasma__R', 'plasma__a', 'magnet__coil__I_coil', 'magnet__winding_pack__B_max', 'plasma__n_e0', 'heating__p_wallplug_heat', 'availability_direct']
fieldnames = ['arm_id', 'column', 'source_case', 'candidate_id', *INPUTS, *channels, *[catalog[c]['source_local_identity'] for c in catalog], 'full_satisfied', 'headline']
all_rows, summary, stores, case_inputs = [], {}, {}, []
unique = study.proposals(); print('unique proposals', len(unique), flush=True)
started = datetime.now(timezone.utc).isoformat(); t0 = time.time()
ta = time.time(); cases, db = study.run()
failures = [{'candidate_id': c.candidate_id, 'state': c.state, 'inputs': dict(c.inputs)} for c in cases if c.state != 'completed']
summary['study'] = {'cases': len(cases), 'unique_proposals': len(unique), 'states': dict(Counter(c.state for c in cases)), 'elapsed_seconds': time.time() - ta, 'failures': failures, 'store': str(db.relative_to(H))}
print('study', summary['study']['states'], f"{summary['study']['elapsed_seconds']:.0f}s", flush=True)
assert len(cases) == len(unique)
if failures: write(R / 'execution-summary.json', {'started_at_utc': started, 'arms': summary, 'publication': 'stopped'}); raise RuntimeError('native cases failed; store retained, publication stopped')
by_key = {key(c.inputs): c for c in cases}
for arm in study.ARMS:
    for r in props[arm]:
        c = by_key[key(r['point'])]
        values = route.required_outputs(c, channels)
        if set(c.verdicts) != set(catalog): raise route.RouteError('verdicts do not match the catalog')
        short = route._short_verdicts(c, catalog)
        full = all(v == 'satisfied' for v in short.values())
        if c.headline != ('satisfied' if full else 'violated'): raise route.RouteError('headline disagrees with verdicts')
        column, source_case = r['column'], r.get('source_case') or ''
        case_inputs.append({'arm_id': arm, 'candidate_id': c.candidate_id, 'column': column, 'source_case': source_case, 'inputs': dict(c.inputs), 'state': c.state})
        inputs = {k: c.inputs.get(route.P + k, '') for k in INPUTS}
        all_rows.append({'arm_id': arm, 'column': column, 'source_case': source_case, 'candidate_id': c.candidate_id, **inputs, **values, **short, 'full_satisfied': full, 'headline': c.headline})
store = StudyStore(db)
try: stores['study'] = verify.compatibility_digest(store)[1]
finally: store.close()
with (R / 'points.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='\n'); w.writeheader(); w.writerows(all_rows)
write(R / 'store-compatibility.json', stores)
write(R / 'case-inputs.json', case_inputs)
clean = preflight.run_clean(route.PACKAGE_DIR); write(R / 'post-run-clean.json', clean); assert clean['outcome'] == 'pass'
write(R / 'execution-summary.json', {'started_at_utc': started, 'finished_at_utc': datetime.now(timezone.utc).isoformat(), 'elapsed_seconds': time.time() - t0, 'repo_revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(), 'arms': summary, 'rows_exported': len(all_rows), 'publication': 'complete'})
print('EXECUTE_DONE', len(all_rows), 'rows', flush=True)
