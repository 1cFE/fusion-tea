"""Read-only independent frozen-record and consequential reading checks."""
import hashlib,json,math,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
R=ROOT/'exploration/aries_integrated/studies/20260922-aries-integrated-equipment-costs'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=read(R/'snapshot.json');rows=read(R/'results/cases.json')['cases'];by={r['case']:r for r in rows}
proposals={p['case']:p for p in read(R/'proposed-points.json')['cases']}
for a in s['arms'][0]['artifacts']:assert sha(R/a['path'])==a['sha256'],a['path']
assert sha(R/'snapshot.json')=='894a81ddc6142bc983c95a783a3ff32783ac6b9f4b58a5d1a727269a3b8f4fcc'
con=sqlite3.connect('file:'+str((R/s['stores'][0]['path']).resolve())+'?mode=ro&immutable=1',uri=True)
stored={cid:(state,json.loads(inp),digest) for cid,state,inp,digest in con.execute('select candidate_id,state,inputs_json,evidence_digest from cases')}
assert len(rows)==len(stored)==64
for row in rows:
 assert stored[row['candidate_id']]==('completed',row['inputs'],row['evidence_digest'])
 assert len(row['inputs'])==411 and row['inputs']==proposals[row['case']]['point']
 assert row['executable_fingerprint']==s['fingerprints']['recorded_provenance.executable_fingerprint']
 a=read(R/'results/native/artifacts'/f"{row['evidence_digest']}.json")
 assert a['outputs']==row['outputs'] and {k:v for k,v in a['responses'].items() if k!='headline'}==row['verdicts']
 assert a['responses']['headline']==row['headline']
con.close()
v=read(R/'results/verification_summary.json');assert v['outcome']=='pass'
assert set(v['stores'][0]['sampling']['sampled_case_ids'])==set(stored)
assert len(v['channels_checked'])==278 and len(v['constraints_rederived'])==14 and not v['verdict_mismatches']
P='aries_integrated_plant__';get=lambda n,o,c,f:by[n]['outputs'][P+o+'__'+c+'__'+f]
b='nominal-calculated';net=lambda n:get(n,'plant_ledger','evaluate','net_electric')
assert math.isclose(net(b),423.10679410931664,rel_tol=0,abs_tol=1e-10)
adverse=[r['case'] for r in rows if any(x=='violated' for x in r['verdicts'].values())];assert len(adverse)==11
costkeys=[k for k in by[b]['outputs'] if '__purchase__' in k and k.endswith(('__cost','__capital','__amount'))]
fixed=[n for n,p in proposals.items() if p['arm'] in ('thermal','demand')];assert len(fixed)==56
for n in fixed:
 for k in costkeys:assert by[n]['outputs'][k]==by[b]['outputs'][k],(n,k)
 assert get(n,'cost_ledger','evaluate','overnight')==get(b,'cost_ledger','evaluate','overnight')
for row in rows:
 for suffix in ('magnet','breeding','deposition','hydraulics','materials','machine_map'):
  assert row['outputs'][P+'plant_ledger__evaluate__supported_'+suffix]==0
for n in ('nominal-source-assumed','literal-Lyon-source-input','literal-Raffray-accounting'):
 assert get(n,'heat_exchangers','evaluate','unmet_heat')>0 and n in adverse
for n in ('cycle_flow-low','cycle_flow-high'):assert n in adverse
assert get('cycle_flow-low','heat_exchangers','evaluate','unmet_heat')>138
for n in ('he_u-low','he_u-high','pbli_hot_limit-low','pbli_hot_limit-high','helium_partition-low','helium_partition-high','pbli_cp-low','pbli_cp-high'):
 assert abs(net(n)-net(b))<1e-6 and get(n,'heat_exchangers','evaluate','unmet_heat')<1e-6
assert get('he_hx_area-low','heat_exchangers','evaluate','unmet_heat')>47
assert get('he_hx_area-low','he_hx','purchase','extrapolated')==1
for n,ratio in [('he_hx_area-low',.1),('he_hx_area-high',1.5)]:
 assert math.isclose(get(n,'he_hx','purchase','capital'),get(b,'he_hx','purchase','capital')*ratio)
for n,m in [('he_pump_capacity-low',-1630.5),('he_pump_capacity-high',1630.5)]:
 assert get(n,'he_pump','screen','margin')==m and net(n)==net(b)
 assert get(n,'he_pump','evaluate','electric')==get(b,'he_pump','evaluate','electric')
assert get('density_amplitude-low','fuel_inventory','annual','annual_burn')<get(b,'fuel_inventory','annual','annual_burn')<get('density_amplitude-high','fuel_inventory','annual','annual_burn')
receipt=dict(passed=True,study_commit='494c329e',snapshot_sha256=sha(R/'snapshot.json'),artifacts_checked=len(s['arms'][0]['artifacts']),
 cases_compared_to_sqlite_and_native_artifacts=len(rows),verified_channels=278,verified_predicates=14,fixed_purchase_cases=len(fixed),purchase_channels=len(costkeys),
 adverse_cases=adverse,baseline_net_mw=net(b),scope='Frozen identities and original stored outputs; material interpretation and dependency checks; no repeated physical evaluator run.')
Path(__file__).with_suffix('.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
