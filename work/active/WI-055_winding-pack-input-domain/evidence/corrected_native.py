"""Bounded corrected-package check without rewriting original candidate evidence."""
import importlib.util,json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
s=importlib.util.spec_from_file_location('native_probe',ROOT/'work/active/WI-053_magnet-and-cryogenic-input-domains/evidence/native_probe.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
P=p.P+'magnet__'
p.CASES={'baseline':{},'zero_current':{P+'I_coil':0.,P+'j_wp':119.},'negative_pair':{P+'I_coil':-15400000.,P+'j_wp':-119.},'nan_density':{P+'I_coil':15400000.,P+'j_wp':math.nan}}
p.run(ROOT/'exploration/stellarator_e2e/generated',HERE/'corrected-native.json')
old=json.loads((HERE/'candidate-domain-native.json').read_text())['cases'];new=json.loads((HERE/'corrected-native.json').read_text())['cases']
for name,row in new.items():
 # NaN override values are intentionally not compared for equality.
 assert {k:v for k,v in row.items() if k!='overrides'}=={k:v for k,v in old[name].items() if k!='overrides'},name
print('PASS corrected baseline full outputs/report and three invalid routes unchanged')
