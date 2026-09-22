"""Independent read-only native-store, export-recovery and cost-reading review."""
import hashlib,json,math,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
R=ROOT/'exploration/aries_integrated/studies/20260922-aries-integrated-cost-uncertainty'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=read(R/'snapshot.json');rows=read(R/'results/cases.json')['cases'];by={r['case']:r for r in rows}
proposals={p['case']:p for p in read(R/'proposed-points.json')['cases']}
assert sha(R/'snapshot.json')=='3d44612d68a513246f18b8184c9022d5ed3dcd93e9002b13497a8460a7dc4041'
for a in s['arms'][0]['artifacts']:assert sha(R/a['path'])==a['sha256'],a['path']
recovery=read(R/'results/export-recovery-proof.json')
assert recovery['source_hashes_unchanged']==read(R/'results/export-recovery-before.json')['persistent_sha256']
post_export_metadata_changes=[path for path,digest in recovery['source_hashes_unchanged'].items() if sha(R/path)!=digest]
assert post_export_metadata_changes==['results/execution-context.json'],post_export_metadata_changes
con=sqlite3.connect('file:'+str((R/s['stores'][0]['path']).resolve())+'?mode=ro&immutable=1',uri=True)
assert con.execute('pragma integrity_check').fetchone()[0]=='ok'
stored={cid:(state,json.loads(inp),digest) for cid,state,inp,digest in con.execute('select candidate_id,state,inputs_json,evidence_digest from cases')}
attempts=con.execute('select count(distinct attempt_id),max(attempt_number) from attempt_transitions').fetchone()
assert attempts==(113,1),attempts
assert len(rows)==len(stored)==113
type_changes=[]
for row in rows:
 assert stored[row['candidate_id']]==('completed',row['inputs'],row['evidence_digest'])
 assert len(row['inputs'])==411 and row['inputs']==proposals[row['case']]['point']
 changes={k:(type(v).__name__,type(row['inputs'][k]).__name__) for k,v in proposals[row['case']]['point'].items() if type(v)!=type(row['inputs'][k])}
 if changes:type_changes.append((row['case'],changes))
 assert row['executable_fingerprint']==s['fingerprints']['recorded_provenance.executable_fingerprint']
 path=R/'results/native/artifacts'/f"{row['evidence_digest']}.json"
 assert sha(path)==row['evidence_digest']
 a=read(path)
 assert a['outputs']==row['outputs'] and {k:v for k,v in a['responses'].items() if k!='headline'}==row['verdicts']
 assert a['responses']['headline']==row['headline']
con.close()
assert len(type_changes)==3 and all(list(ch.values())==[('int','float')] for _,ch in type_changes)
v=read(R/'results/verification_summary.json');assert v['outcome']=='pass'
assert set(v['stores'][0]['sampling']['sampled_case_ids'])==set(stored)
assert len(v['channels_checked'])==278 and len(v['constraints_rederived'])==14 and not v['verdict_mismatches']
P='aries_integrated_plant__';get=lambda n,o,c,f:by[n]['outputs'][P+o+'__'+c+'__'+f]
b='nominal-calculated';net=lambda n:get(n,'plant_ledger','evaluate','net_electric')
controls={'nominal-source-assumed','literal-Lyon-source-input','literal-Raffray-accounting'}
adverse={r['case'] for r in rows if any(x=='violated' for x in r['verdicts'].values())};assert adverse==controls
for row in rows:
 for suffix in ('magnet','breeding','deposition','hydraulics','materials','machine_map'):assert row['outputs'][P+'plant_ledger__evaluate__supported_'+suffix]==0
 if row['case'] not in controls:assert net(row['case'])==net(b)
 cost=get(row['case'],'cost_ledger','evaluate','annual_operating')
 expected=sum(get(row['case'],o,c,f) for o,c,f in [('annual_om','evaluate','annual_om'),('fuel_inventory','annual','annual_cost'),('fuel_inventory','deuterium','annual_fuel'),('cost_ledger','evaluate','annual_import_cost')])+row['inputs'][P+'cost_ledger__consumables']
 assert math.isclose(cost,expected,abs_tol=.01)
 selected=sum(val for key,val in row['outputs'].items() if '__purchase__' in key and key.endswith(('__cost','__capital','__amount')))
 assert math.isclose(selected,get(row['case'],'cost_ledger','evaluate','direct'),abs_tol=.01)
assert math.isclose(get('recovery-100','fuel_inventory','annual','annual_external'),4.66770702324638,abs_tol=1e-10)
assert get('recovery-200','fuel_inventory','annual','annual_external')==0
assert math.isclose(get('recovery-100','cost_ledger','evaluate','annual_operating'),215100712.857122,abs_tol=.01)
for n in ('adequate-area-mode-0','adequate-area-mode-1'):assert get(n,'he_hx','evaluate','ua')==75 and get(n,'heat_exchangers','evaluate','unmet_heat')==0
assert math.isclose(get('adequate-area-mode-0','cost_ledger','evaluate','overnight')-get(b,'cost_ledger','evaluate','overnight'),43452646.5,abs_tol=.01)
assert get('adequate-area-mode-1','cost_ledger','evaluate','overnight')==get(b,'cost_ledger','evaluate','overnight')
corners={n:{'overnight':get(n,'cost_ledger','evaluate','overnight'),'annual_operating':get(n,'cost_ledger','evaluate','annual_operating'),'lifetime_replacement':get(n,'replacement','evaluate','lifetime_total'),'event_count':get(n,'replacement','evaluate','event_count')} for n in by if n.startswith('combined-')}
assert corners['combined-low-recovery-0']['overnight']==1623355845
assert corners['combined-high-recovery-0']['overnight']==13331716800
assert corners['combined-low-recovery-0']['lifetime_replacement']==48498750
assert corners['combined-high-recovery-0']['lifetime_replacement']==5126241600
economic=[n for n,p in proposals.items() if p['arm']=='economic'];assert len(economic)==100
ranking=sorted([(n,get(n,'cost_ledger','evaluate','overnight')-get(b,'cost_ledger','evaluate','overnight')) for n in economic],key=lambda p:abs(p[1]),reverse=True)
assert [n for n,_ in ranking[:3]]==['fuel_inventory_tritium_price-high','fuel_inventory_selected_tritium_kg-high','contingency_fraction-high']
receipt=dict(passed=True,study_commit='8d322312',snapshot_sha256=sha(R/'snapshot.json'),snapshot_artifacts=len(s['arms'][0]['artifacts']),
 recovery_time_protected_files=len(recovery['source_hashes_unchanged']),current_matching_protected_hashes=len(recovery['source_hashes_unchanged'])-len(post_export_metadata_changes),post_export_metadata_changes=post_export_metadata_changes,durable_store_artifact_hashes_still_matching=114,cases_compared_to_sqlite_and_original_native_artifacts=len(rows),attempt_count=attempts[0],maximum_attempt_number=attempts[1],type_changes=type_changes,
 verified_channels=278,verified_predicates=14,conditional_points=110,adverse_cases=sorted(adverse),corners=corners,overnight_effects_top_three=ranking[:3],
 historical_first_recovery_database_byte_parity='Not claimed; no before hash exists.',scope='Original stored maps, outputs, verdicts, identities, final export hash proof and material cost reading; no evaluator run.')
Path(__file__).with_suffix('.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
