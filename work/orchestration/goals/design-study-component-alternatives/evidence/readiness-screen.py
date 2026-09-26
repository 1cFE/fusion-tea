"""Named native-package readiness diagnostics; no matched economic comparison."""
import argparse
import importlib
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit'))
from simkit.study.bridge import CandidateBridge


def evaluate(prepared, cases):
    bridge = CandidateBridge(prepared.entry_models)
    rows = []
    for name, point, expected, provenance in cases:
        row = dict(case=name, inputs=point, expected=expected, provenance=provenance)
        try:
            result = prepared.evaluate(bridge.build(point))
            outputs = {k: v for k, v in dict(result.outputs).items()}
            responses = {k: (v if isinstance(v, (str, int, float, bool)) else str(v)) for k, v in dict(result.responses).items()}
            row.update(state='completed', outputs=outputs, responses=responses,
                       violated=[k for k, v in responses.items() if 'violated' in str(v).lower()])
        except Exception as error:
            row.update(state='refused', error_type=type(error).__name__, message=str(error))
        rows.append(row)
        print(json.dumps({'case': name, 'state': row['state'], 'failed_checks': len(row.get('violated', []))}), flush=True)
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=False)
    s = 'stellarator_09__stellaris__'
    steam = importlib.import_module('exploration.stellarator_e2e.studies.study_route')
    steam_pkg = args.work / 'stellarator_tea'
    shutil.copytree(steam.PACKAGE_DIR, steam_pkg, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    prepared = steam.prepare(steam_pkg, args.work / 'steam-evaluation')
    steam_cases = [
        ('S0-default', {}, 'Native baseline; retain unrelated plant failures', 'Unchanged package defaults'),
        ('S1-salt436', {s+'heat_transport__salt_hot_C': 436.0}, 'Refused at salt heat join', 'Prior H2/O2 diagnostic'),
        ('S2-steam416', {s+'turbine__main_steam_generator__outlet_temperature_C':416.0,s+'turbine__reheater__outlet_temperature_C':416.0}, 'Executes; unchanged offered temperature conditions fail', 'Prior L-006 diagnostic'),
        ('S3-source456', {s+'heat_transport__loop_dT_blanket':156.0}, 'Refused: nonpositive IHX terminal approach', 'Prior H2/O4 diagnostic'),
        ('S4-source480', {s+'heat_transport__loop_dT_blanket':180.0}, 'Retain actual capacity and condition failures', 'Agent diagnostic: fixed equipment, source temperature 480 C'),
        ('S5-source520', {s+'heat_transport__loop_dT_blanket':220.0}, 'Retain actual capacity and condition failures', 'Agent diagnostic: fixed equipment, source temperature 520 C'),
    ]
    receipt = {'purpose':'Readiness diagnostics only; cases are not matched technology alternatives', 'steam':{'fingerprint':str(prepared.fingerprint),'cases':evaluate(prepared,steam_cases)}}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt,indent=2)+'\n')
    brayton = importlib.import_module('exploration.costed_loop_brayton.studies.study_route')
    gas_pkg = args.work / 'costed_loop_brayton_tea'
    shutil.copytree(brayton.PACKAGE_DIR, gas_pkg, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    prepared_b = brayton.prepare(gas_pkg, args.work / 'brayton-evaluation')
    source = 'exploration/costed_loop_brayton/studies/20260926-design-study-parameters-b/results/cases.json'
    sealed = json.loads((ROOT / source).read_text())['cases']
    names = [('B0-original','ir-f2500-r1.5183'),('B1-matched','ir-boundary-f2500'),('B2-unremoved','ir-f2500-r1.4250')]
    gas_cases = []
    expected_rows = {}
    for name, previous in names:
        old = next(r for r in sealed if r['case']==previous)
        gas_cases.append((name,old['inputs'],'Exact native replay of prior stored case',source+'#'+previous))
        expected_rows[name]=old
    gas_rows=evaluate(prepared_b,gas_cases)
    for row in gas_rows:
        old=expected_rows[row['case']]
        common=set(old['outputs']) & set(row.get('outputs',{}))
        mismatch=[k for k in common if old['outputs'][k] != row['outputs'][k]]
        row['replay_check']={'previous_output_count':len(old['outputs']),'common_output_count':len(common),'mismatches':mismatch}
    receipt['brayton']={'fingerprint':str(prepared_b.fingerprint),'cases':gas_rows}
    args.out.write_text(json.dumps(receipt,indent=2)+'\n')

if __name__=='__main__':
    main()
