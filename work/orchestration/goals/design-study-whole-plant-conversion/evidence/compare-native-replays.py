"""Compare repeated native evidence by exact complete input maps; no model solve.

The replacement cases must match 2,492 unchanged cases from the sealed failed
study and four already stock-verified cryogenic replacements. Iteration outputs
are compared exactly and reported separately; they receive no implicit waiver.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[5]
STUDIES = ROOT / 'exploration/whole_plant_conversion/studies'
FIRST = STUDIES / '20260927-design-study-whole-plant-conversion'
SECOND = STUDIES / '20260927-design-study-whole-plant-conversion-b'
EVIDENCE = Path(__file__).resolve().parent
CRYO = EVIDENCE / 'numerical-repair-r2-validation/cryo-native/results/cases.json'


def read(path):
    return json.loads(path.read_text())


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def input_key(point):
    return json.dumps(point, sort_keys=True, separators=(',', ':'), allow_nan=False)


def point_id(key):
    return hashlib.sha256(key.encode()).hexdigest()


def relative(path):
    return str(path.resolve().relative_to(ROOT))


def checked_path(record, name):
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts:
        raise ValueError('unsafe sealed artifact path: ' + name)
    result = (record / name).resolve()
    if not result.is_relative_to(record.resolve()):
        raise ValueError('sealed artifact escapes record: ' + name)
    return result


def seal_check(record):
    snapshot_path = record / 'snapshot.json'
    snapshot = read(snapshot_path)
    artifacts = {}
    for arm in snapshot['arms']:
        for item in arm['artifacts']:
            if item['path'] in artifacts and artifacts[item['path']] != item['sha256']:
                raise ValueError('conflicting sealed artifact identities')
            artifacts[item['path']] = item['sha256']
    failures = []
    for name, expected in artifacts.items():
        path = checked_path(record, name)
        actual = sha(path) if path.is_file() else None
        if actual != expected:
            failures.append(dict(path=name, expected_sha256=expected, actual_sha256=actual))
    return dict(snapshot_sha256=sha(snapshot_path), artifacts_checked=len(artifacts), failures=failures)


def compare(first, replacement, cryo, out):
    if out.exists():
        raise ValueError('comparison output already exists; preserve the previous diagnostic')
    if out.resolve().is_relative_to(first.resolve()) or out.resolve().is_relative_to(replacement.resolve()):
        raise ValueError('comparison output must be outside both study records')
    paths = {'sealed_first': first / 'results/cases.json', 'replacement_cryo': cryo, 'new_study': replacement / 'results/cases.json'}
    hashes_before = {name: sha(path) for name, path in paths.items()}
    sealed = seal_check(first)
    sources = []
    index = {}
    for kind in ('sealed_first', 'replacement_cryo'):
        rows = read(paths[kind])['cases']
        sources.append(dict(kind=kind, path=relative(paths[kind]), sha256=hashes_before[kind], cases=len(rows)))
        for row in rows:
            key = input_key(row['inputs'])
            index.setdefault(key, []).append((kind, row))
    rows = read(paths['new_study'])['cases']
    seen = set()
    matches = []
    missing = []
    duplicate_new = []
    ambiguous = []
    differences = []
    iteration_differences = []
    counts = Counter()
    for new in rows:
        key = input_key(new['inputs']);pid = point_id(key)
        context = dict(case=new['case'], candidate_id=new['candidate_id'], point_id=pid)
        if key in seen:
            duplicate_new.append(context)
        seen.add(key)
        origins = index.get(key, [])
        if not origins:
            missing.append(context)
            continue
        if len(origins) != 1:
            ambiguous.append(dict(context, origins=[dict(kind=k, case=r['case']) for k, r in origins]))
            continue
        kind, original = origins[0]
        counts[kind] += 1
        match = dict(context, source=kind, original_case=original['case'], original_candidate_id=original.get('candidate_id'))
        matches.append(match)
        for field in ('state', 'executable_fingerprint'):
            if new[field] != original[field]:
                differences.append(dict(match, field=field, original=original[field], repeated=new[field]))
        if new['state'] != 'completed':
            differences.append(dict(match, field='state', reason='repeated native point is not completed'))
        for field in ('outputs', 'verdicts'):
            a, b = original[field], new[field]
            for name in sorted(set(a) | set(b)):
                if name in a and name in b and a[name] == b[name]:
                    continue
                difference = dict(match, field=field, channel=name, original=a.get(name), repeated=b.get(name), missing_original=name not in a, missing_repeated=name not in b)
                if field == 'outputs' and name.endswith('__iterations'):
                    iteration_differences.append(difference)
                else:
                    differences.append(difference)
    unused_first = [r['case'] for key, origins in index.items() if key not in seen for kind, r in origins if kind == 'sealed_first']
    expected_counts = {'sealed_first': 2492, 'replacement_cryo': 4}
    checks = dict(new_case_count=len(rows) == 2496, unique_complete_inputs=len(seen) == 2496,
                  exact_source_counts=dict(counts) == expected_counts, every_point_has_one_source=not missing and not ambiguous,
                  all_states_outputs_verdicts_identities_exact=not differences and not iteration_differences,
                  unused_originals_are_four_replaced_cryo_points=len(unused_first) == 4 and all(name.startswith('cryo-capacity-') for name in unused_first),
                  sealed_first_artifacts_unchanged=not sealed['failures'])
    hashes_after = {name: sha(path) for name, path in paths.items()}
    checks['receipt_files_unchanged_during_comparison'] = hashes_before == hashes_after
    checks['first_snapshot_unchanged_during_comparison'] = sha(first / 'snapshot.json') == sealed['snapshot_sha256']
    result = dict(status='pass' if all(checks.values()) and not duplicate_new else 'fail', kind='read-only comparison of genuinely repeated native executions; no new study execution',
                  sources=sources, new_cases=dict(path=relative(paths['new_study']), sha256=hashes_before['new_study'], cases=len(rows)),
                  checks=checks, matched_sources=dict(counts), matches=matches, differences=differences,
                  iteration_differences=iteration_differences, iteration_policy='All iteration outputs are checked exactly; differences fail this comparison and are listed separately.',
                  missing_source_points=missing, ambiguous_source_points=ambiguous, duplicate_new_points=duplicate_new,
                  unused_first_cases=unused_first, sealed_first_record=sealed, receipt_sha256_after=hashes_after)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('matches', 'differences', 'iteration_differences')}, indent=2))
    if result['status'] != 'pass':
        raise ValueError('native evidence comparison failed; inspect the retained diagnostic')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--first-record', type=Path, default=FIRST)
    parser.add_argument('--replacement-record', type=Path, default=SECOND)
    parser.add_argument('--cryo-receipts', type=Path, default=CRYO)
    parser.add_argument('--out', type=Path, default=EVIDENCE / 'native-replay-comparison.json')
    args = parser.parse_args()
    compare(args.first_record, args.replacement_record, args.cryo_receipts, args.out)
