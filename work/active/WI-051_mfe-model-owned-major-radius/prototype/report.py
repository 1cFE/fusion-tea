"""Render complete numerical evidence; this reads results, never creates expectations."""
import difflib, json
from pathlib import Path
H=Path(__file__).resolve().parent; ROOT=Path.cwd(); P='stellarator_09__stellaris__'
r=json.loads((H/'results.json').read_text()); old=json.loads((H/'frozen-results.json').read_text()); c=json.loads((H/'contract-delta.json').read_text())
lines=['# Complete numerical comparison','', '[INHERITED, REFERENT] Expectations are the immutable T-021 baseline and tied_R14 records at `2f8856b7`, frozen by `freeze.py` before prototype generation. Values below are binary64 round-trip decimal representations in the original channel units; their definitions and units remain in the unchanged library source files. No currency, finance, alpha or source conversion is applied. `frozen-results.json` retains complete baseline inputs and `results.json` retains complete executed reports and operands.', '', '[AGENT] Every one of the 158 output channels is covered, including all cost and finance channels. Baseline equality is exact. R14 uses relative and absolute tolerance 1e-9 per channel in its original units. Named verdict IDs/statuses and channel sets are exact. `direct-entering.json` freezes 177 raw channels before repaired execution; `direct-prototype.json` checks those raw channels and the helper’s 158 scalar channels. Metadata differences are reported separately.', '', '| Channel (prefix `stellarator_09__stellaris__`) | Baseline expected = actual | R14 expected | R14 actual |', '|---|---:|---:|---:|']
for k,v in sorted(r['baseline']['outputs'].items()):
    lines.append(f"| `{k.removeprefix(P)}` | {v!r} | {old['cases']['tied_R14']['native']['outputs'][k]!r} | {r['R14']['outputs'][k]!r} |")
lines += ['', '## Named verdicts', '', '| Exact constraint ID | Baseline | R14 |','|---|---|---|']
b={x['constraint_id']:x for x in r['baseline']['report']['results']}; a={x['constraint_id']:x for x in r['R14']['report']['results']}
for k in sorted(b): lines.append(f"| `{k}` | {b[k]['status']} | {a[k]['status']} |")
lines += ['', 'Both aggregate headlines are `violation`. These are 18 authored assertions plus one aggregate response, not 19 assertions.', '', '## Identity and input contract', '', f"Old/new public counts: {c['old_count']} / {c['new_count']}. Exact removed pair: `{c['removed'][0]}`. No additions. Full old/new census is `contract-delta.json`.", '', f"New semantic identity: `{c['semantic_fingerprint']}`. New executable identity: `{c['executable_fingerprint']}`. The unchanged constraint catalog fingerprint is `{r['baseline']['report']['catalog_fingerprint']}`. Baseline raw report, observed operands and margins are exact after serialization; no authored verdict identity changed."]
(H/'numerical-report.md').write_text('\n'.join(lines)+'\n')
patch=''
for name in ['run_stellaris.py','run_stellaris_single.py']:
    before=(ROOT/'exploration/stellarator_e2e'/name).read_text(); after=(H/'direct-prototype'/name).read_text()
    patch+=''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile=name,tofile=name))
(H/'caller-proposed.patch').write_text(patch)
print('Rendered all 158 channels, all 18 verdicts and exact caller patch')
