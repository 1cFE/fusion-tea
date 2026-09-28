"""All-case native/oracle verification, entering attribution and paired sensitivities."""
import json,math
from pathlib import Path
H=Path(__file__).resolve().parents[1];R=H/'results';P='stellarator_09__stellaris__';CP=P+'magnet__conductor_current__'
def read(p):return json.loads(p.read_text())
def write(n,x):(R/n).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def close(a,b):return math.isfinite(a) and math.isfinite(b) and math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-12)
rows=read(R/'native-cases.json');byid={r['proposal_id']:r for r in rows};scan={r['proposal_id']:r for r in read(R/'oracle-scan.json')['rows']};catalog=read(R/'predicate-catalog.json');params=read(H/'preparation/resolved-defaults.json');props={r['id']:r for r in read(H/'preparation/proposals.json')}
current=next(cid for cid,e in catalog.items() if e['source_local_identity']=='reference_conductor_current_ok');oldcatalog={cid:e for cid,e in catalog.items() if cid!=current};assert len(oldcatalog)==19
entering_catalog={e['constraint_id']:e for e in read(H/'preparation/entering-model-contract.json')['constraint_catalog']['concrete_entries']}
assert entering_catalog==oldcatalog
failures=[];scalars=predicates=0;worst=0
for r in rows:
 want=scan[r['proposal_id']];assert r['inputs']==want['point'];assert set(r['verdicts'])==set(want['verdicts'])==set(catalog)
 for k,v in want['channels'].items():
  got=r['outputs'][k];scalars+=1;worst=max(worst,abs(got-v)/max(abs(got),abs(v),1e-100))
  if not close(got,v):failures.append({'proposal_id':r['proposal_id'],'channel':k,'native':got,'oracle':v})
 for cid,v in want['verdicts'].items():
  predicates+=1
  if r['verdicts'][cid]!=v:failures.append({'proposal_id':r['proposal_id'],'constraint_id':cid})
write('oracle-all-points.json',{'outcome':'fail' if failures else 'pass','cases':len(rows),'mapped_channels_per_case':len(next(iter(scan.values()))['channels']),'scalar_comparisons':scalars,'predicate_comparisons':predicates,'max_relative_deviation':worst,'failures':failures,'unmapped_native_channels':sorted(set(rows[0]['outputs'])-set(next(iter(scan.values()))['channels']))});assert not failures
entering=read(H/'preparation/entering-comparison.json');comparisons=[];unchanged=checks=0
for before in entering['rows']:
 prop=props[before['proposal_id']];r=byid[prop['canonical_proposal_id']];assert prop['original_point']==before['point']
 changes={k:{'before':v,'after':r['outputs'][k]} for k,v in before['channels'].items() if not close(v,r['outputs'][k])}
 flips={cid:{'before':before['verdicts'][e['source_local_identity']],'after':r['verdicts'][cid]} for cid,e in oldcatalog.items() if before['verdicts'][e['source_local_identity']]!=r['verdicts'][cid]}
 unchanged+=len(before['channels'])-len(changes);checks+=len(oldcatalog)
 comparisons.append({'proposal_id':before['proposal_id'],'candidate_id':r['candidate_id'],'entering_point':before['point'],'resolved_candidate_point':r['inputs'],'scalar_comparisons':len(before['channels']),'changed_channels':changes,'old_verdict_flips':flips,'current_verdict':r['verdicts'][current]})
write('comparison-entering.json',{'scope':'Captured entering independent oracle versus current native cases; no old native rerun','entering_revision':entering['revision'],'matched_cases':len(comparisons),'unchanged_scalar_comparisons':unchanged,'old_predicate_comparisons':checks,'cases':comparisons,'outcome':'pass' if all(not r['changed_channels'] and not r['old_verdict_flips'] for r in comparisons) else 'fail'});assert all(not r['changed_channels'] and not r['old_verdict_flips'] for r in comparisons)
def summary(r):
 o=r['outputs'];return {'proposal_id':r['proposal_id'],'candidate_id':r['candidate_id'],'inputs':r['inputs'],'lcoe':o[P+'lcoe_calc__lcoe'],'feasible_19':all(r['verdicts'][cid]=='satisfied' for cid in oldcatalog),'current_satisfied':r['verdicts'][current]=='satisfied','feasible_20':all(v=='satisfied' for v in r['verdicts'].values()),'violated':[catalog[cid]['source_local_identity'] for cid,v in r['verdicts'].items() if v!='satisfied'],'current':{k.removeprefix(CP):v for k,v in o.items() if k.startswith(CP)},'fit_margin_m':o[P+'magnet__wp_fit__minimum_margin'],'tape_length_m':o[P+'magnet__winding_procurement__tape_length'],'tape_cost':o[P+'magnet__winding_procurement__tape_cost'],'actual_peak_field_T':o[P+'magnet__peak_field_calc__B_peak']}
summaries={r['proposal_id']:summary(r) for r in rows}
def family(ids):
 selected=[summaries[k] for k in sorted(set(ids))];p19=[r for r in selected if r['feasible_19']];p20=[r for r in selected if r['feasible_20']]
 return {'unique_cases':len(selected),'feasible_19':len(p19),'current_passes':sum(r['current_satisfied'] for r in selected),'feasible_20':len(p20),'feasible_20_cases':p20,'cheapest_19':min(p19,key=lambda r:r['lcoe']) if p19 else None,'cheapest_20':min(p20,key=lambda r:r['lcoe']) if p20 else None,'lcoe_range':[min(r['lcoe'] for r in selected),max(r['lcoe'] for r in selected)],'operating_fraction_range':[min(r['current']['operating_fraction_reference'] for r in selected),max(r['current']['operating_fraction_reference'] for r in selected)]}
paired=[];oldoutputs=set(rows[0]['outputs'])-set(read(H/'preparation/interface.json')['outputs'])
for p in props.values():
 if p['family'] not in ['performance-sensitivity','predicate-independence']:continue
 r=byid[p['canonical_proposal_id']];a=byid[props[p['anchor_id']]['canonical_proposal_id']]
 changes=[k for k in oldoutputs if not close(r['outputs'][k],a['outputs'][k])];flips=[cid for cid in oldcatalog if r['verdicts'][cid]!=a['verdicts'][cid]]
 paired.append({'proposal_id':p['id'],'anchor_id':p['anchor_id'],'scalar_comparisons':len(oldoutputs),'predicate_comparisons':len(oldcatalog),'changed_old_channels':changes,'old_verdict_flips':flips});assert not changes and not flips
write('performance-isolation.json',{'outcome':'pass','scope':'Paired native numerical isolation; unchanged old physics is not independently validated by this check','cases':paired,'scalar_comparisons':len(paired)*len(oldoutputs),'predicate_comparisons':len(paired)*len(oldcatalog)})
responses={}
for g in read(H/'axes.json')['groups']:
 keys=[e['key'] for e in g['keys']];grouped={}
 for r in rows:
  inputs=params|r['inputs'];sig=json.dumps({k:v for k,v in inputs.items() if k not in keys},sort_keys=True);grouped.setdefault(sig,[]).append(r)
 responses[g['axis']]=[{'points':[summaries[r['proposal_id']]|{'axis_value':r['inputs'][keys[0]]} for r in sorted(m,key=lambda r:r['inputs'][keys[0]])]} for m in grouped.values() if len(m)>1]
write('axis-responses.json',responses)
repart=[];base=byid[props['reference']['canonical_proposal_id']]
oldref=read(H/'preparation/entering-native-reference.json')
assert all(close(v,base['outputs'][k]) for k,v in oldref['outputs'].items())
assert all(base['verdicts'][cid]==oldref['responses'][cid] for cid in oldcatalog)
write('native-reference-attribution.json',{'outcome':'pass','scalar_comparisons':len(oldref['outputs']),'predicate_comparisons':len(oldcatalog),'scope':'Captured entering native reference compared with current native reference; old package was not rerun.'})
for p in props.values():
 if p['family']=='turn-repartition':
  r=byid[p['canonical_proposal_id']];fraction=r['outputs'][CP+'operating_fraction_reference'];assert close(fraction,base['outputs'][CP+'operating_fraction_reference']);repart.append(summary(r))
write('analysis.json',{'baseline':summaries[props['reference']['canonical_proposal_id']],'unique_cases':len(rows),'report_rows':len(props),'overall':family(byid),'families':{f:family([p['canonical_proposal_id'] for p in props.values() if p['family']==f]) for f in sorted({p['family'] for p in props.values()})},'scenarios':{s:family([p['canonical_proposal_id'] for p in props.values() if p.get('scenario')==s]) for s in sorted({p['scenario'] for p in props.values() if 'scenario' in p})},'named_anchors':{aid:summaries[props[aid]['canonical_proposal_id']] for aid in read(H/'preparation/selection.json')['anchors']},'turn_repartition':repart,'predicate_independence':{'field_pass_current_fail':summaries[props['reference']['canonical_proposal_id']],'current_pass_field_fail':summaries[props['m000--orientation-3-independence']['canonical_proposal_id']]},'violation_counts':{cid:sum(r['verdicts'][cid]!='satisfied' for r in rows) for cid in catalog},'cases':list(summaries.values())})
print('PASS',scalars,'mapped scalar;',predicates,'predicate;',unchanged,'entering scalar;',checks,'entering predicate comparisons')
