"""Coordinator's full comparison of every stored case of study 20260926-design-study-parameters against the package-owned oracle under the manifest's rule (relative 1e-9 or a declared absolute class) plus a re-derivation of the heat-removal and net-positive verdicts; deposited because the verifier stops at its first refusal. Evidence for owner gate G-001, not a verdict of the tool."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
import sys; sys.path.insert(0, str(ROOT))
from exploration.costed_loop_brayton.studies import oracle_entry as o
R = ROOT / 'exploration/costed_loop_brayton/studies/20260926-design-study-parameters'
P = 'costed_loop_brayton__plant__'
cases = json.load(open(R / 'results/cases.json'))['cases']
classes = {t['channel']: t['value'] for t in json.load(open(R / 'manifest.json'))['absolute_tolerances']}
cat = o.comparison_catalog()
outside, worst_within, verdict_mismatch = [], (0.0, None, None), []
for c in cases:
    v = o.evaluate({k: float(x) for k, x in c['inputs'].items()})
    for ch in cat:
        s = c['outputs'].get(ch)
        if s is None or isinstance(s, bool) or not isinstance(s, (int, float)):
            continue
        ab = abs(v[ch] - s); rel = ab / max(abs(s), 1e-300)
        if rel <= 1e-9 or (ch in classes and ab <= classes[ch]):
            if ch not in classes and rel > worst_within[0]:
                worst_within = (rel, ch, c['case'])
        else:
            outside.append({'case': c['case'], 'candidate': c['candidate_id'], 'channel': ch, 'store': s, 'oracle': v[ch], 'absolute': ab, 'relative': rel})
    tol = float(c['inputs'][P + 'checks__energy_tolerance'])
    derived = {'heat_removal_ok': v[P + 'heat_exchangers__evaluate__unmet_heat'] <= tol, 'net_positive': v[P + 'electrical__evaluate__net_electric'] > 0}
    for cid, status in c['verdicts'].items():
        for name, val in derived.items():
            if name in cid and (status == 'satisfied') != val:
                verdict_mismatch.append({'case': c['case'], 'constraint_id': cid})
summary = {'cases': len(cases), 'channels_per_case': len(cat), 'rule': 'relative <= 1e-9 or declared absolute class', 'classes': classes,
           'outside_rule': outside, 'worst_within_rule_undeclared': {'relative': worst_within[0], 'channel': worst_within[1], 'case': worst_within[2]},
           'verdict_rederivation_mismatches': verdict_mismatch}
(Path(__file__).with_suffix('.json')).write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({'cases': len(cases), 'outside_rule': len(outside), 'worst_within': worst_within, 'verdict_mismatches': len(verdict_mismatch)}))
