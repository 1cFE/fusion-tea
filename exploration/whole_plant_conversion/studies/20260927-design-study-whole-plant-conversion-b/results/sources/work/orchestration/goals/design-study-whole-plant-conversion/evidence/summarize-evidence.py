"""Summarize stored native verdicts and observed declared inputs; no model math."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def summarize(record):
    cases_path = record / 'results/cases.json'
    cases = read(cases_path)['cases']
    catalog = read(record / 'results/constraint_catalog.json')
    partition = read(record / 'preparation/predicate-catalog.json')
    assert set(catalog) == set(partition)
    assert cases and all(row['state'] == 'completed' for row in cases)
    assert all(set(row['verdicts']) == set(catalog) for row in cases)
    constraints = []
    for cid, entry in sorted(catalog.items()):
        constraints.append({'constraint_id': cid,
                            'source_local_identity': entry['source_local_identity'],
                            'definition_qualified_name': entry['definition_qualified_name'],
                            'branch': partition[cid]['branch'],
                            'counts': dict(Counter(row['verdicts'][cid] for row in cases)),
                            'failed_cases': [row['case'] for row in cases if row['verdicts'][cid] != 'satisfied']})
    write(record / 'results/constraint-summary.json',
          {'source_sha256': hashlib.sha256(cases_path.read_bytes()).hexdigest(),
           'cases': len(cases), 'constraints': constraints,
           'interpretation': 'Every native verdict retained, including the inactive alternative. Branch ranking uses its applicable shared and branch predicates.'})
    groups = read(record / 'axes.json')['groups']
    frame = {row['axis']: row for row in read(record / 'framing.json')['groups']}
    axes = []
    for group in groups:
        keys = [row['key'] for row in group['keys']]
        values = {key: sorted({row['inputs'][key] for row in cases}) for key in keys}
        axes.append({'axis': group['axis'], 'framing_proposed': frame[group['axis']]['framing'],
                     'framing_judged': frame[group['axis']]['framing'], 'changed': False,
                     'declared_executed': frame[group['axis']]['executed'], 'observed_values': values,
                     'distinct_input_tuples': len({tuple(row['inputs'][key] for key in keys) for row in cases}),
                     'note': group['note'],
                     'interpretation': 'Coordinated catalog/scenario values; this does not isolate a marginal response of one input. Native per-scenario reranking and case-level statuses are in presentation/.'})
    write(record / 'results/axis-assessment.json', {'groups': axes,
          'search_scope': 'Best admitted points of a finite engineered catalog. Open edges do not support continuous boundary or global optimum claims.',
          'sensitivity_scope': 'Conditional scenario responses. No general feasible-region boundary or empirical uncertainty interval is claimed. Explicit native cryogenic threshold brackets are separate held-equipment diagnostics.'})
    print(json.dumps({'cases': len(cases), 'constraints': len(constraints), 'axes': len(axes)}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', type=Path, required=True)
    summarize(parser.parse_args().record)
