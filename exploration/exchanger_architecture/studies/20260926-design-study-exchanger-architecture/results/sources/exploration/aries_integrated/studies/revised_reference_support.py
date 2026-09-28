"""Thin single-arm study support for the revised ARIES reference cases on the network package.

Reuses the reconciliation proposal composer unchanged. Canonical bases come from the mode-0
replay receipt named in the configuration (`canonical_receipt`), executed on this package
identity, because the predecessor's canonical receipt carries the earlier package identity and
lacks the two WI-092 entry keys. No native evaluation happens during preparation or the
oracle scan. Route, executor, manifest schema, indicators, preflight and verifier are stock.
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


def prepare(record, config_path):
    config = common.read_json(config_path, 'audited study configuration')
    if record.name != config['study_id']:
        raise ValueError('record name and study_id differ')
    common.assert_tree_clean(route.PACKAGE_DIR)
    loaded = manifest.load(route.MANIFEST_PATH)
    manifest.assert_pin_matches(loaded, manifest.indicator_input_fingerprint(route.PACKAGE_DIR))
    receipt_path = ROOT / config['canonical_receipt']
    receipt = common.read_json(receipt_path, 'canonical replay receipt')['cases']
    if any(r['fingerprint'] != route.interface()['executable_fingerprint'] for r in receipt):
        raise ValueError('canonical replay receipt executable differs from this package')
    proposal = base_support.proposals(config, loaded.data['baseline']['point'], route.interface()['entry_keys'],
                                      {r['case']: r['effective_inputs'] for r in receipt})
    groups = {'schema_version': 'study-axis-declaration/v1', 'groups': [
        {'axis': a['axis'], 'keys': a['keys'], 'note': a['basis']} for a in config['axes']]}
    record.mkdir(parents=True, exist_ok=True)
    paths = ['proposed-points.json', 'axes.json', 'axis-plan.json', 'preparation-provenance.json', 'manifest.json']
    if any((record / p).exists() for p in paths):
        raise ValueError('preparation exists; preserve it')
    for name, value in zip(paths, [proposal, groups, config, {
        'manifest_sha256': hashlib.sha256(route.MANIFEST_PATH.read_bytes()).hexdigest(),
        'canonical_receipt': config['canonical_receipt'],
        'canonical_receipt_sha256': hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
        'fingerprints': loaded.data['fingerprints'], 'native_evaluations': 0,
        'source_comparisons': 'Canonical controls are copied verbatim from the mode-0 replay receipt on this package; every other case composes declared changes on a named base.'}, loaded.data]):
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
