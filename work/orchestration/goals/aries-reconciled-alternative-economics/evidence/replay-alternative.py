"""T-001: replay the stored 891 MW alternative cases on the live package through the stock route.

Reads the exact input maps from the sealed cases.json files, executes them with
`study_route.run_points` into a scratch store, and compares every stored numeric output and
verdict under the tolerances declared in replay-tolerance-declaration.md. Writes only the
scratch store (--work) and the summary (--out). Never writes into a frozen record.
"""
import argparse, json, math, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from exploration.aries_integrated.studies import study_route as route  # noqa: E402

STUDIES = ROOT / 'exploration/aries_integrated/studies'
NET = STUDIES / '20260925-aries-revised-reference-network/results/cases.json'
FS = STUDIES / '20260925-aries-flow-scaling-check/results/cases.json'
CASES = {'resized-compressor-1700-network-scaledflows-0.85': FS, 'resized-compressor-1700-network-0.85': FS,
         'nominal-calculated': NET, 'nominal-source-assumed': NET}
P = 'aries_integrated_plant__heat_exchangers__evaluate__'
UNMET = {P + n for n in ('unmet_heat', 'he_unmet', 'pbli_unmet', 'divertor_unmet')}
REL, ABS_ZERO, UNMET_ABS = 1e-12, 1e-12, 1e-7

parser = argparse.ArgumentParser()
parser.add_argument('--work', type=Path, required=True)
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()

sealed = {}
for name, path in CASES.items():
    rows = json.loads(path.read_text())['cases']
    row = next(r for r in rows if r['case'] == name)
    sealed[name] = {'source': str(path.relative_to(ROOT)), 'candidate_id': row['candidate_id'],
                    'executable_fingerprint': row['executable_fingerprint'], 'inputs': row['inputs'],
                    'outputs': row['outputs'], 'verdicts': row['verdicts']}

def key(point):
    return tuple(sorted((k, float(v)) for k, v in point.items()))

proposals = [dict(sealed[n]['inputs']) for n in CASES]
labels = {key(p): n for p, n in zip(proposals, CASES)}
cases, db = route.run_points('aries-alternative-replay-entry', proposals, args.work)
summary = {'package': str(route.PACKAGE_DIR.relative_to(ROOT)), 'store': str(db), 'tolerances': {
    'relative_nonzero': REL, 'absolute_exact_zero': ABS_ZERO, 'absolute_unmet_heat_mw': UNMET_ABS}, 'cases': {}}
for case in cases:
    name = labels[key(dict(case.inputs))]
    s = sealed[name]
    failures, worst_rel, worst_abs = [], 0.0, 0.0
    for channel, v0 in s['outputs'].items():
        v1 = case.outputs.get(channel)
        if v1 is None or not isinstance(v1, (int, float)) or not math.isfinite(float(v1)):
            failures.append({'channel': channel, 'sealed': v0, 'replay': v1, 'rule': 'present-finite'}); continue
        v1 = float(v1); v0 = float(v0); d = abs(v1 - v0)
        if channel in UNMET:
            ok = d <= UNMET_ABS; rule = 'unmet-abs'
        elif v0 == 0.0:
            ok = d <= ABS_ZERO; rule = 'exact-zero-abs'
        else:
            rel = d / abs(v0); worst_rel = max(worst_rel, rel); ok = rel <= REL; rule = 'relative'
        worst_abs = max(worst_abs, d)
        if not ok:
            failures.append({'channel': channel, 'sealed': v0, 'replay': v1, 'abs': d, 'rule': rule})
    extra = sorted(set(case.outputs) - set(s['outputs']))
    verdict_diffs = {c: (s['verdicts'].get(c), case.verdicts.get(c)) for c in set(s['verdicts']) | set(case.verdicts)
                     if s['verdicts'].get(c) != case.verdicts.get(c)}
    summary['cases'][name] = {
        'sealed_source': s['source'], 'sealed_candidate_id': s['candidate_id'], 'replay_candidate_id': case.candidate_id,
        'sealed_executable_fingerprint': s['executable_fingerprint'], 'replay_executable_fingerprint': case.executable_fingerprint,
        'state': case.state, 'channels_compared': len(s['outputs']), 'extra_replay_channels': extra,
        'worst_relative_nonzero': worst_rel, 'worst_absolute': worst_abs, 'failures': failures,
        'verdicts_compared': len(s['verdicts']), 'verdict_differences': verdict_diffs,
        'passed': not failures and not verdict_diffs and case.state == 'completed'
                  and case.executable_fingerprint == s['executable_fingerprint']}
summary['passed'] = all(c['passed'] for c in summary['cases'].values()) and len(summary['cases']) == len(CASES)
args.out.write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({n: {k: c[k] for k in ('passed', 'channels_compared', 'worst_relative_nonzero', 'worst_absolute', 'state')}
                  for n, c in summary['cases'].items()} | {'all_passed': summary['passed']}, indent=1))
