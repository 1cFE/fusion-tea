"""Thin single-arm study support for the design-choice interactions study (goal design-space-combinations).

Reuses the reconciliation proposal composer unchanged. Canonical bases are the stored input maps of
two sealed cases (`nominal-calculated` from 20260925-aries-revised-reference-network and
`resized-compressor-1700-network-scaledflows-0.85` from 20260925-aries-flow-scaling-check), read
verbatim from the sealed records' `results/cases.json` and checked against this package's executable
fingerprint (the WI-092 identity, unchanged). No native evaluation happens during preparation or the
oracle scan. Route, executor, manifest schema, indicators, preflight and verifier are stock; the live
manifest is reused without a re-pin because the package identity is unchanged.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import runpy

from exploration.aries_integrated.studies import reconciliation_support as base_support
from exploration.aries_integrated.studies import study_route as route
from scripts.study import common, manifest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREDECESSOR = base_support.PREDECESSOR
SEALED = {
    '20260925-aries-revised-reference-network': ('nominal-calculated',),
    '20260925-aries-flow-scaling-check': ('resized-compressor-1700-network-scaledflows-0.85',),
}


def canonical_inputs():
    """Verbatim stored input maps of the sealed cases, with the sealed files' digests."""
    expected = route.interface()['executable_fingerprint']
    canonical, provenance = {}, {}
    for record, names in SEALED.items():
        path = HERE / record / 'results' / 'cases.json'
        rows = {r['case']: r for r in common.read_json(path, 'sealed cases')['cases']}
        for name in names:
            row = rows[name]
            if row['executable_fingerprint'] != expected or row['state'] != 'completed':
                raise ValueError('sealed case is not a completed case of this package identity: ' + name)
            canonical[name] = {k: float(v) for k, v in row['inputs'].items()}
        provenance[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return canonical, provenance


def prepare(record, config_path):
    config = common.read_json(config_path, 'audited study configuration')
    if record.name != config['study_id']:
        raise ValueError('record name and study_id differ')
    common.assert_tree_clean(route.PACKAGE_DIR)
    loaded = manifest.load(route.MANIFEST_PATH)
    manifest.assert_pin_matches(loaded, manifest.indicator_input_fingerprint(route.PACKAGE_DIR))
    canonical, provenance = canonical_inputs()
    proposal = base_support.proposals(config, loaded.data['baseline']['point'], route.interface()['entry_keys'], canonical)
    groups = {'schema_version': 'study-axis-declaration/v1', 'groups': [
        {'axis': a['axis'], 'keys': a['keys'], 'note': a['basis']} for a in config['axes']]}
    record.mkdir(parents=True, exist_ok=True)
    paths = ['proposed-points.json', 'axes.json', 'axis-plan.json', 'preparation-provenance.json', 'manifest.json']
    if any((record / p).exists() for p in paths):
        raise ValueError('preparation exists; preserve it')
    for name, value in zip(paths, [proposal, groups, config, {
        'manifest_sha256': hashlib.sha256(route.MANIFEST_PATH.read_bytes()).hexdigest(),
        'canonical_sources': provenance, 'canonical_cases': sorted(canonical),
        'fingerprints': loaded.data['fingerprints'], 'native_evaluations': 0,
        'source_comparisons': 'Canonical bases are the verbatim stored input maps of two sealed cases on this package identity; every other case composes declared changes on a named base.'}, loaded.data]):
        base_support.write_new(record / name, value)
    return {'cases': len(proposal['cases']), 'record': str(record)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'scan', 'baseline', 'execute'])
    parser.add_argument('--record', type=Path, required=True)
    parser.add_argument('--config', type=Path)
    parser.add_argument('--integration-return', type=Path)
    args = parser.parse_args()
    if args.command == 'prepare':
        if args.config is None:
            parser.error('prepare requires --config')
        result = prepare(args.record, args.config)
    elif args.command == 'scan':
        result = base_support.scan(args.record)
    elif args.command == 'baseline':
        out = args.record / 'preparation'
        out.mkdir(exist_ok=True)
        paths = route.execute_baseline(out, manifest_path=(args.record / 'manifest.json').resolve())
        result = {k: str(v) for k, v in paths.items()}
    else:
        if args.integration_return is None:
            parser.error('execute requires --integration-return')
        route.MANIFEST_PATH = (args.record / 'manifest.json').resolve()
        execute = runpy.run_path(str(PREDECESSOR / 'execute_study.py'))['execute']
        result = execute(args.record, args.integration_return)
    if result is not None:
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
