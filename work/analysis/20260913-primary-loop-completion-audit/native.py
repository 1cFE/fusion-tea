"""Independent ordinary public-override denominator probes."""
import importlib.util,json,math
from pathlib import Path
R=Path.cwd();O=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('runner',R/'work/active/WI-053_magnet-and-cryogenic-input-domains/evidence/native_probe.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.CASES={'baseline':{},'dormant':{m.P+'loop_live':0.},**{f'{key}/{live}/{i}':{m.P+key:v,m.P+'loop_live':live} for key in ('loop_cp','loop_dT_blanket') for live in (0.,1.) for i,v in enumerate((0.,-1.,math.nan,math.inf,-math.inf))},'negative_pair':{m.P+'loop_cp':-5000.,m.P+'loop_dT_blanket':-100.}}
m.run(R/'exploration/stellarator_e2e/generated',O/'native.json')
r=json.loads((O/'native.json').read_text())['cases']
for k,v in r.items():
 if k in ('baseline','dormant'):assert 'error' not in v
 else:assert v['error']=='EvaluationFailed' and 'Primary Coolant Loop:' in v['message'] and 'finite and positive' in v['message'],(k,v)
print('PASS 21 deliberate ordinary native refusals, baseline and dormant controls')
