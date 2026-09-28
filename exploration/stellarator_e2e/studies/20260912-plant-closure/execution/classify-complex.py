import json,sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from exploration.stellarator_e2e.studies import oracle_entry as oracle
H=Path('exploration/stellarator_e2e/studies/20260912-plant-closure')
def inspect(point):
 r=oracle._compute(oracle._oracle_overrides(point))
 bad={k:{'real':v.real,'imag':v.imag} for k,v in r.items() if isinstance(v,complex)}
 return {'inputs':point,'p_net_MW':r['p_net'],'complex_outputs':bad,'negative_net_power_confirmed':r['p_net']<0}
if __name__=='__main__':
 rows=json.loads((H/'preparation/correlation.json').read_text())
 points={x['proposal_key']:x['inputs'] for x in rows if x.get('exclusion_reason','').startswith('TypeError:')}
 with ProcessPoolExecutor(max_workers=8,mp_context=multiprocessing.get_context('spawn')) as pool:results=list(pool.map(inspect,points.values()))
 assert all(x['negative_net_power_confirmed'] and x['complex_outputs'] for x in results)
 data={'outcome':'pass','unique_cases':len(results),'basis':'Unmodified full oracle computation returns negative net electrical power; fractional cost powers and square-root land scaling produce complex outputs. This is an arithmetic domain exclusion, not a physical feasibility proof.','source':'exploration/stellarator_e2e/verify_stellaris.py:707,711,732,733,748','cases':results}
 (H/'preparation/complex-domain-diagnostics.json').write_text(json.dumps(data,indent=2)+'\n')
 print(data['outcome'],data['unique_cases'])
