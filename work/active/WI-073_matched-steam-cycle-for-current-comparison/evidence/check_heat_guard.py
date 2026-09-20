"""Author domain tests for the integrated heat join, independently reviewed separately."""
import json,sys,math
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'seeds'))
import matched_steam_cycle_impl as m
x=json.loads((HERE/'production/baseline-working.json').read_text())['input']
x|={'source_heat_MW':x['heat_available_MW']-100.,'selected_recovered_MW':100.}
checks=[]
def refusal(label,patch):
 try:m.calculate(x|patch)
 except ValueError as e:checks.append({'case':label,'refused':str(e)})
 else:raise AssertionError(label)
m.calculate(x);checks.append({'case':'coherent upstream heat','completed':True})
refusal('source mismatch',{'source_heat_MW':x['source_heat_MW']-1})
refusal('recovered mismatch',{'selected_recovered_MW':99.})
for k in ('source_heat_MW','selected_recovered_MW'):
 refusal(k+' nan',{k:math.nan})
 r=m.calculate(x|{k:math.nan,'enabled':0.});assert not r['active'];checks.append({'case':k+' disabled invalid','inactive':True})
(HERE/'heat-guard-author-results.json').write_text(json.dumps(checks,indent=2)+'\n')
print('PASS',len(checks),'heat-join cases')
