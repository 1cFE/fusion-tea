"""Readable interpretation of retained predicates; no evaluation or verdict edits."""
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'attempts/diagnostic-1/report.json'
report = json.loads(SOURCE.read_text())
records = {}
for key, entry in report['predicates'].items():
    observed = entry['native_evaluation'].get('observed', {})
    native = entry['native_status']
    scoped = entry['model_definedness']['model_definedness']
    explicit = observed.get('defined_in')
    guarded = scoped in ('undefined', 'unknown') or ('defined_in' in observed and explicit != 1)
    field = entry['qualification']['field_applicability']
    if native == 'unavailable':
        category = 'unavailable'
    elif guarded:
        category = 'not_evaluable_under_model_conditions'
    elif 'facility_occupancy_ok__' in key and native == 'violated':
        category = 'strict_boundary_violation_requires_numerical_review'
    elif native == 'violated':
        category = 'violated_field_unqualified' if field == 'unknown_unqualified' else 'violated_unaffected_by_field_finding'
    else:
        category = 'native_' + native + '_without_engineering_acceptance'
    records[key] = {'native_status': native, 'observed_defined_in': explicit,
                    'propagated_guard_status': scoped, 'field_applicability': field,
                    'interpretation': category, 'observed': observed,
                    'engineering_acceptance': False}
result = {'schema_version': 'predicate-interpretation/v1',
          'source_report_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
          'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'scope': 'Supplement to unchanged diagnostic-1. Native observed defined_in is considered in addition to the six propagated guard families. Strict occupancy-boundary violation is retained; no numerical tolerance is introduced.',
          'counts': dict(Counter(r['interpretation'] for r in records.values())),
          'predicates': records}
with (HERE / 'predicate-interpretation.json').open('x') as stream:
    json.dump(result, stream, indent=2, sort_keys=True, allow_nan=False)
    stream.write('\n')
print(json.dumps(result['counts'], indent=2))
