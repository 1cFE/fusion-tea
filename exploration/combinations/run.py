"""Execute the WI-093 combination cases through the generated combinations_tea graph.

All four assemblies evaluate together in the package's one pipeline; a case overrides entry inputs by key and touches
one assembly. Each case stores its effective inputs, every output, the constraint report or the refusal with the
body's message and the module that raised it. Writes only under the evidence directory (or --root).

Run: .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python exploration/combinations/run.py'
"""
import argparse
import json
import re
import shutil
import traceback
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PACKAGE = HERE / 'combinations_tea'
EVIDENCE = ROOT / 'work/active/WI-093_combination-assemblies/evidence'
L = 'combinations_loop_brayton__loop_brayton__'
C = 'combinations_plasma_chain__plasma_chain__'
F = 'combinations_lumped_fit__lumped_fit__'
E = 'combinations_circulator_purchase__circulator_purchase__'
ASSEMBLY = {L: 'C-1', C: 'C-2', F: 'C-4', E: 'C-5'}
RESELECTED = {L + 'compressor_capacity__selected_rating': 3200., L + 'turbine_capacity__selected_rating': 7000.,
              L + 'generator_capacity__selected_rating': 3600., L + 'rejection_capacity__selected_rating': 5000.,
              L + 'he_capacity__selected_rating': 3500.}
ALT_HW = {C + 'cycle__selected_flow': 1700., C + 'cycle__recuperator_effectiveness': .95, C + 'heat_exchangers__network_mode': 1.,
          C + 'compressor_capacity__selected_rating': 1700., C + 'he_pump__selected_flow_capacity': 3359.,
          C + 'pbli_pump__selected_flow_capacity': 27666., C + 'heat_exchangers__he_flow': 3359.,
          C + 'heat_exchangers__pbli_flow': 27666.}
# 'baseline' is every assembly at its design values: it is c1-aries-ratios-aries-ratings, c2-stellaris-plasma-aries-nominal,
# c4-aries-branches and c5-rating-8 at once (design § 2-5).
SCENARIOS = {
    'baseline': {},
    'c1-aries-ratios-reselected-ratings': dict(RESELECTED),
    'c1-ratio1.35-reselected-ratings': {**RESELECTED, **{L + f'compressor_{i}__selected_ratio': 1.35 for i in (1, 2, 3)}},
    'c1-flow1400-aries-ratings': {L + 'cycle__selected_flow': 1400.},
    'c1-flow4000-reselected-ratings': {**RESELECTED, L + 'cycle__selected_flow': 4000.},
    'c2-stellaris-plasma-alternative-hardware': dict(ALT_HW),
    'c2-ne0-4.2e20': {C + 'plasma__n_e0': 4.2e20},
    'c2-peaked-profile': {C + 'plasma__alpha_n': 1.0},
    'c2-flat-temperature': {C + 'plasma__alpha_T': 0.5},
    'c5-rating-5': {E + 'circulator_equipment__selected_rating': 5.},
    'c5-rating-12': {E + 'circulator_equipment__selected_rating': 12.},
}


def load_runtime():
    from simkit.evaluation.package_load import ProvisionalPackageLoader
    module, fingerprint = ProvisionalPackageLoader(package_dir=PACKAGE, package_name='combinations_tea', link_root=HERE / 'links').load()
    return module, module.create_combinations_tea_registry(), str(fingerprint)


def entry_module(pipeline):
    return next(m for m in pipeline['modules'].values() if m.get('module_type') == 'EntryPoint')


def refusing_module(text):
    found = re.findall(r'(combinations_[a-z_]+__[A-Za-z0-9_]+)', text)
    return found[0] if found else None


def execute_case(name, changes, runtime, root=None):
    from simkit.core.pipeline import execute_pipeline
    module, registry, fingerprint = runtime
    folder = (root or EVIDENCE / 'native_runs') / name
    folder.mkdir(parents=True, exist_ok=True)
    pipeline = yaml.safe_load((PACKAGE / 'pipelines/pipeline.yaml').read_text())
    entry = entry_module(pipeline)
    effective = {}
    for key, spec in entry['inputs'].items():
        schema, relative = spec.split(' ', 1)
        values = json.loads((PACKAGE / 'pipelines' / relative).read_text())
        for parameter in values:
            if parameter in changes:
                values[parameter] = changes[parameter]
        path = folder / (key + '.json')
        path.write_text(json.dumps(values, indent=2) + '\n')
        entry['inputs'][key] = schema + ' ' + str(path.resolve())
        effective.update(values)
    unknown = set(changes) - set(effective)
    if unknown:
        raise ValueError('unknown scenario keys: ' + repr(sorted(unknown)))
    path = folder / 'pipeline.yaml'
    path.write_text(yaml.safe_dump(pipeline, sort_keys=False))
    touched = sorted({ASSEMBLY[p] for p in ASSEMBLY for k in changes if k.startswith(p)})
    row = dict(case=name, assemblies_changed=touched, changes=changes, effective_inputs=effective, fingerprint=fingerprint)
    try:
        result = execute_pipeline(path, folder / 'outputs', registry=registry, custom_schema_types=module.CUSTOM_SCHEMA_TYPES)
        row.update(status='evaluated', outputs={k: v.model_dump(mode='json') if hasattr(v, 'model_dump') else v for k, v in result.outputs.items()})
    except Exception as error:
        text = traceback.format_exc()
        row.update(status='refused', error=str(error), exception_type=type(error).__name__, refusing_module=refusing_module(text), traceback=text)
    (folder / 'result.json').write_text(json.dumps(row, indent=2) + '\n')
    # result.json carries every output; the pipeline's per-channel output tree is regenerable and not retained.
    shutil.rmtree(folder / 'outputs', ignore_errors=True)
    return row


def constraint_summary(row):
    report = row.get('outputs', {}).get('constraint_report')
    if not report:
        return None
    results = report['results']
    by = {}
    for r in results:
        cid = r['constraint_id']
        prefix = next((p for p in ASSEMBLY if cid.startswith(p)), 'other')
        by.setdefault(ASSEMBLY.get(prefix, prefix), {'satisfied': [], 'violated': [], 'other': []})
        bucket = 'satisfied' if r['status'] == 'satisfied' else ('violated' if r['status'] == 'violated' else 'other')
        by[ASSEMBLY.get(prefix, prefix)][bucket].append(cid[len(prefix):] if prefix != 'other' else cid)
    return by


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path)
    parser.add_argument('--cases', nargs='*')
    args = parser.parse_args()
    runtime = load_runtime()
    rows = []
    for name, changes in SCENARIOS.items():
        if args.cases and name not in args.cases:
            continue
        row = execute_case(name, changes, runtime, args.root)
        summary = {'case': name, 'assemblies_changed': row['assemblies_changed'], 'status': row['status']}
        if row['status'] == 'evaluated':
            summary['constraints'] = {a: {'violated': v['violated'], 'n_satisfied': len(v['satisfied']), 'other': v['other']} for a, v in constraint_summary(row).items()}
        else:
            summary.update(error=row['error'], refusing_module=row['refusing_module'])
        rows.append(summary)
        print(json.dumps(summary))
    out = args.root or EVIDENCE / 'native_runs'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'summary.json').write_text(json.dumps({'fingerprint': runtime[2], 'cases': rows}, indent=2) + '\n')
