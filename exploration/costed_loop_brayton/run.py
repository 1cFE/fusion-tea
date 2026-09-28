"""Execute the WI-094 development cases through the generated costed_loop_brayton_tea graph.

A case overrides entry inputs by key. Each case stores its effective inputs, every output, the constraint report or the
refusal with the body's message and the module that raised it. Writes only under the evidence directory (or --root).

Run: .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python exploration/costed_loop_brayton/run.py'
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
PACKAGE = HERE / 'costed_loop_brayton_tea'
EVIDENCE = ROOT / 'work/completed/20260926_WI-095_loop-return-control/evidence'  # WI-094's receipts stay under its own evidence directory
P = 'costed_loop_brayton__plant__'
RESELECTED = {P + 'compressor_capacity__selected_rating': 3200., P + 'turbine_capacity__selected_rating': 7000.,
              P + 'generator_capacity__selected_rating': 3600., P + 'rejection_capacity__selected_rating': 5000.,
              P + 'he_capacity__selected_rating': 3500.}
ARIES_RATINGS = {P + 'compressor_capacity__selected_rating': 1600., P + 'turbine_capacity__selected_rating': 3500.,
                 P + 'generator_capacity__selected_rating': 1800., P + 'rejection_capacity__selected_rating': 2500.,
                 P + 'he_capacity__selected_rating': 1500.}
RATIO = lambda r: {P + f'compressor_{i}__selected_ratio': r for i in (1, 2, 3)}
# The design's defaults are the C-1 design values with the ARIES ratings, as in WI-093 (its 'baseline' case).
# The five WI-093 C-1 cases (the bit-exact control set, design section 6) come first.
SCENARIOS = {
    'c1-aries-ratios-aries-ratings': {},
    'c1-aries-ratios-reselected-ratings': dict(RESELECTED),
    'c1-ratio1.35-reselected-ratings': {**RESELECTED, **RATIO(1.35)},
    'c1-flow1400-aries-ratings': {P + 'cycle__selected_flow': 1400.},
    'c1-flow4000-reselected-ratings': {**RESELECTED, P + 'cycle__selected_flow': 4000.},
    'best-screen-point-reselected': {**RESELECTED, **RATIO(1.45)},
    'best-screen-point-aries-ratings': {**ARIES_RATINGS, **RATIO(1.45)},
    'starting-point-fuel-term-wired': {**RESELECTED, P + 'electrical__fuel_exhaust': None},  # filled from the stored exhaust rate at run time
}
CONTROL_SEALED = ROOT / 'work/completed/20260926_WI-093_combination-assemblies/evidence/native_runs'
C1 = 'combinations_loop_brayton__loop_brayton__'
CONTROL_CASES = ['baseline', 'c1-aries-ratios-reselected-ratings', 'c1-ratio1.35-reselected-ratings', 'c1-flow1400-aries-ratings', 'c1-flow4000-reselected-ratings']


def load_runtime():
    from simkit.evaluation.package_load import ProvisionalPackageLoader
    module, fingerprint = ProvisionalPackageLoader(package_dir=PACKAGE, package_name='costed_loop_brayton_tea', link_root=HERE / 'links').load()
    return module, module.create_costed_loop_brayton_tea_registry(), str(fingerprint)


def entry_module(pipeline):
    return next(m for m in pipeline['modules'].values() if m.get('module_type') == 'EntryPoint')


def refusing_module(text):
    found = re.findall(r'(costed_loop_brayton__[A-Za-z0-9_]+)', text)
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
    row = dict(case=name, changes=changes, effective_inputs=effective, fingerprint=fingerprint)
    try:
        result = execute_pipeline(path, folder / 'outputs', registry=registry, custom_schema_types=module.CUSTOM_SCHEMA_TYPES)
        row.update(status='evaluated', outputs={k: v.model_dump(mode='json') if hasattr(v, 'model_dump') else v for k, v in result.outputs.items()})
    except Exception as error:
        text = traceback.format_exc()
        row.update(status='refused', error=str(error), exception_type=type(error).__name__, refusing_module=refusing_module(text), traceback=text)
    (folder / 'result.json').write_text(json.dumps(row, indent=2) + '\n')
    shutil.rmtree(folder / 'outputs', ignore_errors=True)
    return row


def control_comparison(name, row):
    """Every numeric C-1 channel of a control case against its sealed WI-093 value (exact equality expected), and every C-1
    verdict by local identity (the constraint ids carry a hash of the qualified name, which differs between packages, so
    the per-constraint evaluation records are compared by status, not by key). A refused case compares nothing and is
    reported as such."""
    sealed = json.loads((CONTROL_SEALED / name / 'result.json').read_text())
    if row['status'] != 'evaluated':
        return {'sealed_case': name, 'channels_compared': 0, 'differences': [], 'exact': False, 'refused': row['error']}
    differences, compared = [], 0
    for key, value in sealed['outputs'].items():
        if not key.startswith(C1) or key == 'constraint_report' or key.endswith('__evaluation'):
            continue
        mine = row['outputs'].get(P + key[len(C1):])
        compared += 1
        if mine != value:
            differences.append({'channel': key[len(C1):], 'sealed': value, 'costed': mine})
    local = lambda cid, prefix: cid[len(prefix):].rsplit('__', 1)[0]
    sealed_verdicts = {local(r['constraint_id'], C1): r['status'] for r in sealed['outputs']['constraint_report']['results'] if r['constraint_id'].startswith(C1)}
    mine_verdicts = {local(r['constraint_id'], P): r['status'] for r in row['outputs']['constraint_report']['results'] if r['constraint_id'].startswith(P)}
    verdict_differences = [{'check': k, 'sealed': v, 'costed': mine_verdicts.get(k)} for k, v in sealed_verdicts.items() if mine_verdicts.get(k) != v]
    return {'sealed_case': name, 'channels_compared': compared, 'verdicts_compared': len(sealed_verdicts), 'differences': differences,
            'verdict_differences': verdict_differences, 'exact': not differences and not verdict_differences}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path)
    parser.add_argument('--cases', nargs='*')
    args = parser.parse_args()
    runtime = load_runtime()
    rows, controls = [], {}
    exhaust = None
    for name, changes in SCENARIOS.items():
        if args.cases and name not in args.cases:
            continue
        changes = dict(changes)
        if P + 'electrical__fuel_exhaust' in changes and changes[P + 'electrical__fuel_exhaust'] is None:
            if exhaust is None:
                raise RuntimeError('the fuel-term case needs a prior evaluated case to read the stored exhaust rate from')
            changes[P + 'electrical__fuel_exhaust'] = exhaust
        row = execute_case(name, changes, runtime, args.root)
        if row['status'] == 'evaluated' and exhaust is None:
            exhaust = row['outputs'][P + 'fuel__evaluate__exhaust_rate']
        summary = {'case': name, 'status': row['status']}
        if row['status'] == 'evaluated':
            results = row['outputs']['constraint_report']['results']
            summary['violated'] = [r['constraint_id'][len(P):].rsplit('__', 1)[0] for r in results if r['status'] == 'violated']
            summary['n_satisfied'] = sum(r['status'] == 'satisfied' for r in results)
            summary.update({k: row['outputs'][P + c] for k, c in (('net', 'electrical__evaluate__net_electric'), ('unmet', 'heat_exchangers__evaluate__unmet_heat'),
                                                                 ('overnight', 'cost_ledger__evaluate__overnight'), ('lcoe', 'lifecycle_price__evaluate__lcoe'))})
        else:
            summary.update(error=row['error'], refusing_module=row['refusing_module'])
        if name in CONTROL_CASES or name == 'c1-aries-ratios-aries-ratings':
            sealed_name = 'baseline' if name == 'c1-aries-ratios-aries-ratings' else name
            controls[name] = control_comparison(sealed_name, row)
            summary['control_exact'] = controls[name]['exact']
        rows.append(summary)
        print(json.dumps(summary))
    out = args.root or EVIDENCE / 'native_runs'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'summary.json').write_text(json.dumps({'fingerprint': runtime[2], 'cases': rows, 'controls': controls}, indent=2) + '\n')
