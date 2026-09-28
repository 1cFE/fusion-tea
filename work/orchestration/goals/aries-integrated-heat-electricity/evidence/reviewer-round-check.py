import csv,hashlib,json,math,sqlite3,subprocess
from pathlib import Path
root=Path.cwd();p=root/'exploration/aries_integrated/studies/20260922-integrated-heat-electricity';e=root/'work/orchestration/goals/aries-integrated-heat-electricity/evidence'
read=lambda f:json.loads((p/f).read_text());sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
s=read('snapshot.json');rows=read('results/cases.json')['cases'];proposals=read('proposed-points.json')['cases'];v=read('results/verification_summary.json')
assert len(rows)==len(proposals)==14
by={r['case']:r for r in rows};base=by['nominal-calculated'];P='aries_integrated_plant__'
for proposal in proposals:
 r=by[proposal['case']];assert r['inputs']==proposal['point'];assert r['state']=='completed';assert len(r['inputs'])==122;assert len(r['outputs'])==211;assert len(r['verdicts'])==10
 changed={k:val for k,val in r['inputs'].items() if val!=base['inputs'][k]}
 assert changed==proposal['changed_from_calculated_baseline'],r['case']
 artifact=p/'results/native/artifacts'/(r['evidence_digest']+'.json');assert sha(artifact)==r['evidence_digest'];a=json.loads(artifact.read_text());assert a['outputs']==r['outputs']
 assert {x['constraint_id']:x['status'] for x in a['report']['results']}==r['verdicts']
 for key in ('magnet','breeding','deposition','hydraulics','materials','machine_map'):assert r['outputs'][P+'plant_ledger__evaluate__supported_'+key]==0
assert sum(all(x=='satisfied' for x in r['verdicts'].values()) for r in rows)==8
combos={tuple(sorted(r['verdicts'].items())) for r in rows};assert len(combos)==5
assert len(v['channels_checked'])==30 and len(v['constraints_rederived'])==10
assert set(v['stores'][0]['sampling']['sampled_case_ids'])=={r['candidate_id'] for r in rows}
assert v['outcome']=='pass' and not v['verdict_mismatches']
assert v['absolute_tolerances'][0]['value']==1e-7 and len(v['absolute_tolerances'])==1
con=sqlite3.connect('file:'+str(p/'results/native/20260922-integrated-heat-electricity.db')+'?mode=ro&immutable=1',uri=True)
stored=list(con.execute('select candidate_id,state,inputs_json,evidence_digest from cases'));assert len(stored)==14
cid={r['candidate_id']:r for r in rows}
for ident,state,inputs,digest in stored:assert state=='completed' and json.loads(inputs)==cid[ident]['inputs'] and digest==cid[ident]['evidence_digest']
con.close()
with (p/'results/cases.csv').open() as f:csvrows=list(csv.DictReader(f))
assert len(csvrows)==14
assert len(set(csvrows[0])&set(base['outputs']))==187
for r in csvrows:
 for k in set(r)&set(base['outputs']):assert float(r[k])==by[r['case']]['outputs'][k]
artifacts=s['arms'][0]['artifacts']
for r in artifacts:assert sha(p/r['path'])==r['sha256'],r['path']
assert sha(p/'snapshot.json')=='e888d008f2e740129bdbb39f359a619df53a2d9d6fd789a1df40a982a2bbc4ca'
for label,mult in [('density-low',.9),('density-high',1.1)]:
 r=by[label];assert sum(r['inputs'][k]!=base['inputs'][k] for k in base['inputs'])==1
 for suffix in ('source__evaluate__selected_power','fuel__evaluate__exhaust_rate'):assert math.isclose(r['outputs'][P+suffix]/base['outputs'][P+suffix],mult**2,rel_tol=1e-12)
for axis in ('fuel-rating','helium-rating'):
 for side in ('low','high'):
  r=by[axis+'-'+side];assert r['outputs'][P+'plant_ledger__evaluate__net_electric']==base['outputs'][P+'plant_ledger__evaluate__net_electric']
  assert sum(r['inputs'][k]!=base['inputs'][k] for k in base['inputs'])==1
for axis in ('compressor-ratio','helium-ua'):
 for side in ('low','high'):assert sum(by[axis+'-'+side]['inputs'][k]!=base['inputs'][k] for k in base['inputs'])==1
frozen_files=subprocess.check_output(['git','ls-tree','-r','8e6fb2f2','--',str(p.relative_to(root))],text=True).splitlines()
for line in frozen_files:
 meta,path=line.split('\t');digest=meta.split()[2];actual=subprocess.check_output(['git','hash-object',path],text=True).strip();assert digest==actual,path
missing_tool_copies=[]
for tool in s['tools']:
 for r in tool['source_digest']['files']:
  copy=p/'results/sources'/r['path']
  if not copy.exists():missing_tool_copies.append(r['path'])
  else:assert sha(copy)==r['sha256']
result={'passed':True,'frozen_files_unchanged':len(frozen_files),'snapshot_artifact_hashes_checked':len(artifacts),'sqlite_json_artifact_parity':True,'points':14,'numeric_outputs_per_case':211,'csv_numeric_columns':187,'comparison_coverage':{'scalars':420,'verdicts':140,'verdict_combinations':5},'all_ten_pass':8,'fixed_hardware_input_comparisons':True,'missing_tool_source_copies':sorted(set(missing_tool_copies))}
(e/'reviewer-round-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
