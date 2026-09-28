"""Compare the retained failed attempt with the unchanged-map numerical repair."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from scripts.study.common import relative_deviation

base = ROOT / 'exploration/exchanger_architecture/thermal_requirements/studies'
old = base / '20260927-exchanger-thermal-comparison'
new = base / '20260927-exchanger-thermal-comparison-b'
read = lambda p: json.loads(p.read_text())
a = {r['case']: r for r in read(old / 'results/cases.json')['cases']}
b = {r['case']: r for r in read(new / 'results/cases.json')['cases']}
assert a.keys() == b.keys() and len(a) == 1277
manifest = read(new / 'manifest.json')
absolute = {r['channel']: r['value'] for r in manifest['absolute_tolerances']}
verified = {r['channel'] for r in read(new / 'results/verification_summary.json')['channels_checked']}
changed = {}; violations = []; recovered = []; legacy_exact = []; verdict_changes = []
for label, before in a.items():
    after = b[label]
    assert before['inputs'] == after['inputs'] and after['state'] == 'completed'
    if before['state'] != 'completed':
        recovered.append(label)
        continue
    if before['verdicts'] != after['verdicts']:
        verdict_changes.append(label)
    if before['inputs']['aries_integrated_plant__heat_exchangers__control_mode'] == 0:
        assert before['outputs'] == after['outputs']
        legacy_exact.append(label)
    for channel, v in before['outputs'].items():
        w = after['outputs'][channel]
        if v == w:
            continue
        delta = abs(v-w); rel = relative_deviation(v, w)
        prior = changed.get(channel)
        if prior is None or delta > prior['maximum_absolute_difference']:
            changed[channel] = {'case': label, 'maximum_absolute_difference': delta, 'relative_at_this_case': rel}
        if channel in verified and rel >= 1e-9 and delta >= absolute.get(channel, 0):
            violations.append({'case': label, 'channel': channel, 'absolute_difference': delta, 'relative_difference': rel})
assert not verdict_changes and not violations, (verdict_changes, violations)
assert read(old / 'results/constraint_catalog.json') == read(new / 'results/constraint_catalog.json')
result = {'outcome': 'pass', 'cases': len(a), 'exact_input_maps': True,
          'identical_constraint_catalog_and_predicate_ir': True, 'completed_before': len(a)-len(recovered),
          'recovered_cases': recovered, 'completed_after': len(b), 'verdict_changes_on_completed_cases': verdict_changes,
          'legacy_cases_all_outputs_exact': legacy_exact, 'verified_channel_tolerance_violations': violations,
          'changed_channels_maxima': changed,
          'interpretation': 'Stable numerical evaluation changes some controlled floating-point results. All previously completed predicates are exact; independently verified channels retain the unchanged tolerance. All current maps separately pass complete independent verification. Unchecked algorithm diagnostics are disclosed in changed_channels_maxima.'}
(new / 'results/prior-attempt-correlation.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: v for k, v in result.items() if k != 'changed_channels_maxima'}))
