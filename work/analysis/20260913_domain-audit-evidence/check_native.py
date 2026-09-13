"""Use the supported native evaluator without mutating author evidence."""
import importlib.util
import json
from pathlib import Path
ROOT=Path.cwd()
spec=importlib.util.spec_from_file_location('native_probe',ROOT/'work/active/WI-053_magnet-and-cryogenic-input-domains/evidence/native_probe.py')
probe=importlib.util.module_from_spec(spec);spec.loader.exec_module(probe)
P=probe.P
probe.CASES={'ordinary':{},'live_original':{P+'coil_t':20.},'live_equal':{P+'coil_t':19.4},'reference_original':{P+'magnet__a_coil_ref':13.},'reference_equal':{P+'magnet__a_coil_ref':12.7},'zero_cold':{P+'T_cold_cryo':0.},'equal_temperatures':{P+'T_cold_cryo':300.},'reversed_temperatures':{P+'T_cold_cryo':301.},'negative_ambient':{P+'T_amb_cryo':-1.}}
destination=ROOT/'work/analysis/20260913_domain-audit-evidence/native.json'
probe.run(ROOT/'exploration/stellarator_e2e/generated',destination)
rows=json.loads(destination.read_text())['cases']
for name,row in rows.items():
    if name=='ordinary': continue
    assert row['error']=='EvaluationFailed',(name,row)
    target='clearance' if name.startswith(('live','reference')) else 'require 0 < T_cold < T_amb'
    assert target in row['message'],(name,row)
base=json.loads((ROOT/'work/active/WI-053_magnet-and-cryogenic-input-domains/evidence/baseline-native.json').read_text())['cases']['live_ordinary']
for key in ['outputs','responses','report']: assert rows['ordinary'][key]==base[key],key
print('Eight native deliberate refusals; ordinary 158 outputs, response map and engineering report exactly preserved')
