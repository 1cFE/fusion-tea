"""Retain the pre-fix omission and prove all authored guards now execute."""
import argparse,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args()
def read(name):return json.loads((HERE/'native_runs'/name/'result.json').read_text())
current=read('baseline');before=read('baseline.attempt2')
def ids(row):return {r['constraint_id'] for r in row['outputs']['constraint_report']['results']}
expected=len(re.findall(r'assert constraint ',(ROOT/'models/designs/component_alternatives/plant.sysml').read_text()))
adverse=read('salt-three-pumps');prior=read('salt-three-pumps.attempt1')
key='component_alternatives__plant__steam_transport__evaluate__design_pump_type_ok'
violations=[r['constraint_id'] for r in adverse['outputs']['constraint_report']['results'] if r['status']=='violated']
assert expected==len(ids(current))==84
assert len(ids(before))==66 and len(ids(current)-ids(before))==18
assert adverse['outputs'][key] is False and prior['outputs'][key] is False
assert any('__design_pump_type_ok_required__' in k for k in violations)
assert not any(r['status']=='violated' for r in prior['outputs']['constraint_report']['results'])
result=dict(expected_authored_guards=expected,emitted_before=len(ids(before)),emitted_after=len(ids(current)),added=sorted(ids(current)-ids(before)),pre_fix_receipt='native_runs/baseline.attempt2/result.json',three_pump_before='native_runs/salt-three-pumps.attempt1/result.json',three_pump_after='native_runs/salt-three-pumps/result.json',raw_design_pump_type_ok=False,executing_violations=violations,status='pass')
if args.out.exists():raise FileExistsError(args.out)
args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
