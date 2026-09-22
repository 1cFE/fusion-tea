import sys,json,hashlib,tempfile,shutil,sqlite3,math
from pathlib import Path
ROOT=Path.cwd();sys.path.insert(0,str(ROOT))
from exploration.aries_integrated.studies import study_route as route
from simkit.study.bridge import CandidateBridge
E=ROOT/'work/orchestration/goals/aries-integrated-design-studies/evidence'
S=ROOT/'exploration/aries_integrated/studies/20260922-aries-integrated-coupled-design'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
cases=read(S/'results/cases.json')['cases'];proposals=read(S/'proposed-points.json')['cases']
by={c['case']:c for c in cases};prop={c['case']:c for c in proposals}
assert len(by)==len(prop)==68
prefix='aries_integrated_plant__';L=prefix+'lifecycle_accounts__evaluate__'
close=lambda a,b: math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-7)
dbpath=S/'results/native/20260922-aries-integrated-coupled-design.db';dbsha=sha(dbpath)
db=sqlite3.connect(f'file:{dbpath}?mode=ro&immutable=1',uri=True)
rows=db.execute('select candidate_id,inputs_json,evidence_digest,state from cases').fetchall();assert len(rows)==68
stored={r[0]:r for r in rows};summary=[]
for c in cases:
 n=c['case'];x=c['inputs'];y=c['outputs'];r=stored[c['candidate_id']]
 assert x==prop[n]['point']==json.loads(r[1]);assert r[3]==c['state']=='completed';assert r[2]==c['evidence_digest']
 artifact=S/'results/native/artifacts'/f'{r[2]}.json';assert sha(artifact)==r[2]
 a=read(artifact);assert a['outputs']==y and a['responses']==dict(c['verdicts'],headline=c['headline'])
 assert a['provenance']['executable_fingerprint']==c['executable_fingerprint']==route.interface()['executable_fingerprint']
 feed=100. if n.endswith('--feed100-service30m') else 0.;service=30e6 if feed else 0.
 assert x[prefix+'fuel_inventory__annual_recovery_kg']==y[L+'new_feed']==feed
 assert x[prefix+'finance__supply_service_annual']==service
 gross=sum(y[prefix+'fuel_inventory__annual__annual_'+k] for k in ('burn','loss','decay'))
 assert close(gross,y[L+'gross_makeup']);assert close(max(gross-feed,0),y[L+'external_shortfall']);assert close(max(feed-gross,0),y[L+'curtailed_feed'])
 energy=y[L+'annual_energy'];assert close(energy,y[prefix+'plant_ledger__evaluate__net_electric']*8760*x[prefix+'cost_schedule__availability'])
 assert close(y[L+'supply_lcoe'],service/energy)
 terms=['capital','om','tritium','deuterium','consumables','imports','supply','replacement','other_overhaul','terminal','salvage']
 assert close(sum(y[L+k+'_lcoe'] for k in terms),y[prefix+'lifecycle_price__evaluate__lcoe'])
 for k,v in y.items():
  if '__plant_ledger__evaluate__supported_' in k and not k.endswith('supported_deposition'):assert v==0,(n,k,v)
  if k.endswith(('breeding_supported','supply_supported','hydraulic_supported')):assert v==0
 for hx in ['he_hx','pbli_hx']:
  area=x[prefix+hx+'__selected_area'];assert y[prefix+hx+'__purchase__purchased_quantity']==area
  assert close(y[prefix+hx+'__evaluate__ua'],area*x[prefix+hx+'__assumed_u']/1e6)
  assert close(y[prefix+hx+'__purchase__capital'],area/x[prefix+hx+'__reference_quantity']*x[prefix+hx+'__reference_cost']*x[prefix+hx+'__price_factor'])
 if n.startswith('density'):
  base=by['baseline--'+n.split('--')[1]]['outputs']
  for k,v in y.items():
   if '__purchase__' in k:assert v==base[k],(n,k)
 if '-5000.0' in n:
  hx='he_hx' if n.startswith('he_') else 'pbli_hx'
  assert y[prefix+hx+'__purchase__extrapolated']==1
  assert any(v=='violated' for v in c['verdicts'].values())
 summary.append({'case':n,'net_mw':y[prefix+'plant_ledger__evaluate__net_electric'],'gross':gross,'purchases':y[L+'external_shortfall'],'lcoe':y[prefix+'lifecycle_price__evaluate__lcoe'],'violations':[k for k,v in c['verdicts'].items() if v=='violated']})
assert sha(dbpath)==dbsha
scratch=Path(tempfile.mkdtemp(prefix='aries-coupled-review-'));package=scratch/'aries_integrated'
def hashes(p):return {str(f.relative_to(p)):sha(f) for f in p.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.suffix!='.pyc'}
before=hashes(route.PACKAGE_DIR);shutil.copytree(route.PACKAGE_DIR,package,ignore=shutil.ignore_patterns('__pycache__','*.pyc'));assert hashes(package)==before
evaluator=route.prepare(package,scratch/'evaluation');bridge=CandidateBridge(evaluator.entry_models)
replays=[]
for name in ['baseline','grid-he45000-pbli45000-n5e+20','probe-he45000-pbli45000-n4.875e20','grid-he45000-pbli45000-n5.25e+20']:
 for arm in ['no-credit','feed100-service30m']:
  c=by[name+'--'+arm];row=evaluator.evaluate(bridge.build(c['inputs']))
  assert dict(row.outputs)==c['outputs'],c['case'];assert dict(row.responses)==dict(c['verdicts'],headline=c['headline']),c['case']
  replays.append({'case':c['case'],'inputs':c['inputs'],'outputs':dict(row.outputs),'verdicts':dict(row.responses),'original_evidence_digest':c['evidence_digest'],'exact_match':True})
assert hashes(route.PACKAGE_DIR)==before
out={'status':'PASS','fingerprints':{k:route.interface()[k] for k in ['executable_fingerprint','semantic_fingerprint']},'store_sha256':dbsha,'store_unchanged':sha(dbpath)==dbsha,'original_package_unchanged':True,'scratch':str(scratch),'all_case_checks':summary,'replays':replays}
(E/'coupled-review-probe.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','case_count':len(summary),'replay_count':len(replays),'outputs_each':546,'verdicts_each':14}))
