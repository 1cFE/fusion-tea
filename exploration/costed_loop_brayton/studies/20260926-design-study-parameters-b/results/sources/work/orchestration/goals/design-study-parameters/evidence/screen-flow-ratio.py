"""T-001 scratch screen (goal design-study-parameters): cycle flow x stage pressure ratio on the existing WI-093
combinations package, C-1 assembly, every other input at its C-1 design value with the re-selected ratings
(3200 / 7000 / 3600 / 5000 / 3500 MW) as case inputs. Diagnostic receipts only: no study record, no manifest, no
package write. The five WI-093 C-1 cases are re-run as controls and compared with their sealed receipts.

Run: .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python work/orchestration/goals/design-study-parameters/evidence/screen-flow-ratio.py --work <scratch> --out <json>'
"""
import argparse
import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SPEC = importlib.util.spec_from_file_location('combinations_run', ROOT / 'exploration/combinations/run.py')
RUN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUN)
L = RUN.L
RESELECTED = dict(RUN.RESELECTED)
ARIES_RATINGS = {'compressor_capacity': 1600., 'turbine_capacity': 3500., 'generator_capacity': 1800.,
                 'rejection_capacity': 2500., 'he_capacity': 1500.}
RESELECTED_RATINGS = {k.split('__')[-2]: v for k, v in RESELECTED.items()}
FLOWS = [1500., 2000., 2500., 3000., 3500., 4000.]
RATIOS = [1.20, 1.30, 1.35, 1.40, 1.45, 1.5182944859378311, 1.60, 1.70, 1.80]
CONTROLS = {k: v for k, v in RUN.SCENARIOS.items() if k == 'baseline' or k.startswith('c1-')}
SEALED = ROOT / 'work/completed/20260926_WI-093_combination-assemblies/evidence/native_runs'
CHANNELS = {
    'net': 'electrical__evaluate__net_electric', 'gross': 'electrical__evaluate__gross_electric',
    'net_shaft': 'electrical__evaluate__net_shaft', 'shaft_import': 'electrical__evaluate__shaft_import',
    'compressor_demand': 'electrical__evaluate__compressor_demand', 'auxiliary': 'electrical__evaluate__auxiliary_electric',
    'turbine_work': 'turbine__evaluate__shaft_produced', 'turbine_inlet_K': 'heat_exchangers__evaluate__turbine_temperature',
    'heater_inlet_K': 'heat_exchangers__evaluate__heater_inlet', 'accepted': 'heat_exchangers__evaluate__accepted_heat',
    'unmet': 'heat_exchangers__evaluate__unmet_heat', 'he_capability': 'heat_exchangers__evaluate__he_capability',
    'he_return_K': 'heat_exchangers__evaluate__he_return', 'he_hot_bound_margin_K': 'heat_exchangers__evaluate__he_hot_bound_margin',
    'rejected': 'rejection_capacity__rejected_heat__rejected_heat', 'q_ihx': 'primary_loop__evaluate__q_ihx',
    'pump_electric': 'primary_loop__evaluate__p_elec', 'turbine_outlet_K': 'turbine__evaluate__temperature_out',
    'recuperator_bypass': 'recuperator__evaluate__bypass_active', 'recovered_heat': 'recuperator__evaluate__recovered_heat',
    'compressor_outlet_K': 'compressor_3__evaluate__temperature_out', 'turbine_pressure': 'pressure_loss__evaluate__pressure_out',
}
DEMANDS = {'compressor_capacity': 'compressor_demand', 'turbine_capacity': 'turbine_work', 'generator_capacity': 'gross',
           'rejection_capacity': 'rejected', 'he_capacity': 'q_ihx'}


def read(row):
    if row['status'] != 'evaluated':
        return {'status': 'refused', 'error': row['error'], 'refusing_module': row.get('refusing_module')}
    out = row['outputs']
    values = {name: out[L + key] for name, key in CHANNELS.items()}
    native = {r['constraint_id'][len(L):].rsplit('__', 1)[0]: r['status'] for r in out['constraint_report']['results'] if r['constraint_id'].startswith(L)}
    screens = {}
    for inventory, ratings in (('reselected', RESELECTED_RATINGS), ('aries', ARIES_RATINGS)):
        screens[inventory] = {part: ratings[part] - values[DEMANDS[part]] for part in ratings}
    thermal = {'heat_removal_ok': values['unmet'] <= 1e-6, 'net_positive': values['net'] > 0}
    verdicts = {inv: {**{p + '_ok': m >= 0 for p, m in ms.items()}, **thermal} for inv, ms in screens.items()}
    return {'status': 'evaluated', 'values': values, 'native_verdicts': native, 'margins': screens, 'verdicts': verdicts,
            'all_checks': {inv: all(v.values()) for inv, v in verdicts.items()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    runtime = RUN.load_runtime()
    result = {'package_fingerprint': runtime[2], 'controls': {}, 'grid': [], 'ratings': {'reselected': RESELECTED_RATINGS, 'aries': ARIES_RATINGS},
              'note': 'Native verdicts are for the re-selected ratings run as case inputs; the ARIES-inventory verdicts are computed here from the stored demands against the ARIES ratings and are not native verdicts.'}
    for name, changes in CONTROLS.items():
        row = RUN.execute_case(name, changes, runtime, args.work / 'controls')
        sealed = json.loads((SEALED / name / 'result.json').read_text())
        same = row['status'] == sealed['status'] and all(row['outputs'].get(k) == v for k, v in sealed['outputs'].items() if k.startswith(L) and k != 'constraint_report')
        result['controls'][name] = {'reproduces_sealed_c1_outputs': bool(same), 'reading': read(row)}
    for flow in FLOWS:
        for ratio in RATIOS:
            name = f'flow{int(flow)}-ratio{ratio:.4f}'
            changes = {**RESELECTED, L + 'cycle__selected_flow': flow, **{L + f'compressor_{i}__selected_ratio': ratio for i in (1, 2, 3)}}
            row = RUN.execute_case(name, changes, runtime, args.work / 'grid')
            result['grid'].append({'case': name, 'flow': flow, 'ratio': ratio, **read(row)})
            print(json.dumps({'case': name, 'status': row['status'], **({k: round(v, 3) for k, v in result['grid'][-1]['values'].items() if k in ('net', 'unmet', 'compressor_demand', 'turbine_inlet_K', 'heater_inlet_K')} if row['status'] == 'evaluated' else {'error': row['error']})}), flush=True)
    result['package_tree_clean'] = subprocess.run(['git', 'status', '--porcelain', '--', 'exploration/combinations'], cwd=ROOT, capture_output=True, text=True).stdout == ''
    args.out.write_text(json.dumps(result, indent=1) + '\n')
    print(json.dumps({'controls_reproduced': {k: v['reproduces_sealed_c1_outputs'] for k, v in result['controls'].items()}, 'points': len(result['grid']), 'package_tree_clean': result['package_tree_clean']}))


if __name__ == '__main__':
    main()
