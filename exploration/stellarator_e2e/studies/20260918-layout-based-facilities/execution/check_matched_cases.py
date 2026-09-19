"""Check matched study controls against retained entering evidence and each other."""
from pathlib import Path
import json,math
H=Path(__file__).resolve().parents[1];R=H/'results';P='stellarator_09__stellaris__'
read=lambda p:json.loads(p.read_text())
rows={r['proposal_id']:r for r in read(R/'interpreted-cases.json')}
cases=read(R/'native-cases.json');by_id={r['candidate_id']:r for r in cases}
entering=read(H/'preparation/entering-replay.json')['cases'];report=[];failures=[]
physical=tuple(P+n for n in ('plasma__','radial_build__','rb__','pb__','calendar__','heat_transport__','blanket__','divertor__','magnet__','cryoplant__','sustain__','heat__','operating_heat__'))
for index,name in enumerate(('default14','selected18')):
 old=by_id[rows[name+'-legacy']['case_id']];new=by_id[rows[name+'-layout']['case_id']]
 shared=set(entering[index]['outputs']) & set(old['outputs']);misses=[]
 for key in sorted(shared):
  a,b=old['outputs'][key],entering[index]['outputs'][key]
  if not math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-8):misses.append({'channel':key,'legacy':a,'entering':b})
 unchanged=[k for k in old['outputs'] if k.startswith(physical) or (k.startswith(P+'buildings__layout__') and not k.endswith('__cost_mode'))]
 for key in unchanged:
  if old['outputs'][key]!=new['outputs'][key]:failures.append({'pair':name,'physical_channel_changed':key})
 if old['verdicts']!=new['verdicts']:failures.append({'pair':name,'predicate_status_changed':True})
 failures.extend({'pair':name,**m} for m in misses)
 changed={k:{'legacy':v,'layout':new['outputs'][k]} for k,v in old['outputs'].items() if v!=new['outputs'][k]}
 report.append({'pair':name,'legacy_case':old['candidate_id'],'layout_case':new['candidate_id'],'entering_comparisons':len(shared),'entering_mismatches':misses,'identical_physical_channels':len(unchanged),'all_predicates_identical':old['verdicts']==new['verdicts'],'changed_channels':changed})
result={'outcome':'fail' if failures else 'pass','pairs':report,'failures':failures,'scope':'Matched cost selection and entering replay parity. Does not qualify unchanged physical assumptions.'}
(R/'matched-control-checks.json').write_text(json.dumps(result,indent=2)+'\n')
assert not failures,failures
print('Matched controls and entering replay pass:',[(r['pair'],r['entering_comparisons'],r['identical_physical_channels']) for r in report])
