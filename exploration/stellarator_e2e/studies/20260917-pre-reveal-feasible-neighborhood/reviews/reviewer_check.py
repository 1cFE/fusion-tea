import csv, json, math, operator, sqlite3, hashlib, subprocess
from pathlib import Path
from scripts.study.verify import evaluate_operand
from exploration.stellarator_e2e.studies import oracle_entry as oe
H=Path('exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood'); E=Path(__file__).parent; P='stellarator_09__stellaris__'
read=lambda p:json.loads(p.read_text()); sha=lambda b:hashlib.sha256(b).hexdigest(); key=lambda p:json.dumps(p,sort_keys=True)
N=read(H/'results/native-cases.json'); byid={r['proposal_id']:r for r in N}; bycid={r['candidate_id']:r for r in N}; S=read(H/'results/oracle-scan.json')['rows']; scan={key(r['point']):r for r in S if r['outcome']=='evaluated'}; C=read(H/'results/predicate-catalog.json'); D=read(H/'preparation/resolved-defaults.json'); bindings=oe.operand_bindings(); props=read(H/'preparation/proposals.json'); pm={r['id']:r for r in props}; A=read(H/'results/analysis.json'); am={r['proposal_id']:r for r in A['cases']}; anchor=read(H/'preparation/refinement-selection.json')['anchor']; axis=read(H/'axes.json')['groups']; axiskeys={g['keys'][0]['key'] for g in axis}
counts={'scalar_comparisons':0,'predicate_comparisons':0,'native_operand_checks':0,'store_joins':0}; exceptions=[]; strict=[]
for n in N:
 s=scan[key(n['inputs'])]; assert len(n['outputs'])==242 and len(s['channels'])==226
 for k,v in s['channels'].items():
  counts['scalar_comparisons']+=1; assert math.isclose(n['outputs'][k],v,rel_tol=1e-9,abs_tol=1e-9)
  if not math.isclose(n['outputs'][k],v,rel_tol=1e-9):strict.append([n['proposal_id'],k,n['outputs'][k],v])
 for cid,c in C.items():
  counts['predicate_comparisons']+=1
  if n['verdicts'][cid]!=s['verdicts'][cid]: exceptions.append([n['proposal_id'],c['source_local_identity']])
  ir=json.loads(c['predicate_ir']); l,r=[evaluate_operand(cid,x,bindings,n['inputs'],D,n['outputs'])[0] for x in ir['operands']]; pred={'<':operator.lt,'<=':operator.le,'>':operator.gt,'>=':operator.ge}[ir['operator']](l,r); assert n['verdicts'][cid]==('satisfied' if pred else 'violated'); counts['native_operand_checks']+=1
  margin=(l-r) if ir['operator'].startswith('>') else r-l; assert margin==am[n['proposal_id']]['signed_margins'][c['source_local_identity']]
 assert am[n['proposal_id']]['all20_satisfied']==all(v=='satisfied' for v in n['verdicts'].values())
assert len(exceptions)==3 and len(strict)==6
bounds=dict(zip([P+x for x in ['plasma__R','plasma__a','magnet__coil__I_coil','plasma__n_e0','plasma__T_i0','magnet__coil__coil_t','magnet__casing__interior_y','heat_transport__n_loops','magnet__winding_pack__inventory_multiplier']],[(10.5,15),(1.1,1.7),(12e6,18e6),(4e20,6e20),(12,18),(.55,.75),(.55,.75),(12,22),(1,1.01)]))
exempt=[]
for p in props:
 pt=p['point']; assert axiskeys<=pt.keys()
 if p['family']=='control':exempt.append(p['id']);continue
 for k,(lo,hi) in bounds.items():assert lo<=pt[k]<=hi,(p['id'],k,pt[k])
 assert pt[P+'heat_transport__n_loops'].is_integer()
 assert {k:v for k,v in pt.items() if k not in axiskeys}=={k:v for k,v in anchor['point'].items() if k not in axiskeys}
for name,folder in [('r2-forward','selected-mode'),('r2-table5','table5-conditioned')]:
 old=read(H/f'preparation/r2-{folder}-native-result.json'); assert old['outputs']==byid[name]['outputs'] and old['verdicts']==byid[name]['verdicts']
for db in (H/'results').rglob('*.db'):
 con=sqlite3.connect(f'file:{db}?mode=ro&immutable=1',uri=True)
 for cid,state,inputs,digest in con.execute('select candidate_id,state,inputs_json,evidence_digest from cases'):
  b=(db.parent/'artifacts'/f'{digest}.json').read_bytes(); assert sha(b)==digest; e=json.loads(b);assert state=='completed'
  if cid in bycid:
   n=bycid[cid]; assert json.loads(inputs)==n['inputs'] and e['outputs']==n['outputs']; assert {k:v for k,v in e['responses'].items() if k in C}==n['verdicts']; counts['store_joins']+=1
 for raw,valid,cid in con.execute('select raw_json,valid,candidate_id from proposals'):
  if cid in bycid: assert valid==1 and json.loads(raw)==bycid[cid]['inputs']
 con.close()
assert counts['store_joins']==334
M=list(csv.DictReader((H/'results/map-data.csv').open())); meta=read(H/'results/plot-metadata.json'); classes={}
for m in M:
 n=bycid[m['native_candidate_id']]; p=pm[m['proposal_id']]; assert p['point']==n['inputs'];assert float(m['R_m'])==n['inputs'][P+'plasma__R']; assert float(m['current_MAturn'])==n['inputs'][P+'magnet__coil__I_coil']/1e6
 assert {k:v for k,v in n['inputs'].items() if k not in [P+'plasma__R',P+'magnet__coil__I_coil']}==meta['fixed_inputs']
 a=am[n['proposal_id']]; valid=bool(n['outputs'][P+'divertor__divheat__power_account_valid']); label='pass' if a['all20_satisfied'] and valid else ('invalid-account' if not valid else 'fail'); assert label==m['classification'];classes[label]=classes.get(label,0)+1
 for column,local in [('field_margin_T','peak_field_ok'),('divertor_margin_MW_m2','divertor_heat_ok')]:assert float(m[column])==a['signed_margins'][local]
 assert float(m['auxiliary_window_margin_MW'])==min(a['signed_margins']['burn_hold_ok'],a['signed_margins']['sustainment_ok'])
assert classes=={'fail':210,'invalid-account':2,'pass':44}
nb=read(H/'results/neighborhood-summary.json')
for axis,v in nb['axis_two_sided'].items():
 for sign,ids in [('passing_below',v['passing_below']),('passing_above',v['passing_above'])]:
  assert ids
  for i in ids:
   n=byid[pm[i]['canonical_proposal_id']]; changes=[k for k in n['inputs'] if n['inputs'][k]!=anchor['point'][k]];assert changes==[P+axis]; assert all(x=='satisfied' for x in n['verdicts'].values()); assert (n['inputs'][P+axis]<anchor['point'][P+axis])==(sign=='passing_below')
for p in props:
 if p['family']=='combined-neighbor':
  assert all(byid[p['canonical_proposal_id']]['verdicts'][c]=='satisfied' for c in C)
  for k in axiskeys-{P+'magnet__winding_pack__inventory_multiplier',P+'heat_transport__n_loops'}:assert math.isclose(abs(p['point'][k]/anchor['point'][k]-1),.005)
  assert abs(p['point'][P+'heat_transport__n_loops']-18)==1
freshids=['r2-forward','r2-table5',anchor['id'],'neighbor-plasma__R--0.01','neighbor-plasma__a-+0.01','combined-00']+[m['proposal_id'] for m in sorted(M,key=lambda m:abs(float(m['field_margin_T'])))[:2]]
fresh=[]
for pid in freshids:
 pt=pm[pid]['point']; ch=oe.evaluate(pt); assert ch==scan[key(pt)]['channels'];fresh.append({'proposal_id':pid,'point':pt,'purpose':'verification-only; already screened coordinate','oracle_calls':1})
archive=Path('.project/active/aries-comparison-preparation/package/freeze/r2/comparison-freeze.tar.gz'); assert sha(archive.read_bytes())=='fa42cb32c1a51989871ba15a3bf2c51ca0a88c9a506b27c8e314c88b42960a21'
for rel,info in read(H/'preparation/r2-control-provenance.json').items():
 b=subprocess.check_output(['git','show',info['revision']+':'+info['source']]);assert sha(b)==info['sha256']==sha((H/rel).read_bytes())
assert not subprocess.check_output(['git','diff','9c8874c97fd75039b9fe516fe06a0427ac559120','--','.project/active/aries-comparison-preparation/package/input-rules.json','.project/active/aries-comparison-preparation/package/comparison_adapter.py'])
report={'outcome':'PASS','checks':counts,'native_cases':len(N),'native_combined_passes':sum(a['all20_satisfied'] and a['quantities']['power_account_valid'] for a in A['cases']),'map_counts':classes,'raw_boundary_exceptions':exceptions,'strict_relative_differences':strict,'bounds_control_exemptions':exempt,'fresh_oracle_checks':fresh,'fresh_oracle_calls':len(fresh),'new_screening_coordinates':0,'native_evaluations':0,'archive_sha256':sha(archive.read_bytes()),'png_visually_inspected':True,'generic_verifier':'Original log is a first-case strict-relative refusal, not a pass. Local full comparison retains all raw signs.'}
(E/'reviewer-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['fresh_oracle_checks','strict_relative_differences']},indent=2))
