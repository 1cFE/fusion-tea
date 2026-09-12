"""Every declared channel, predicate, frozen control and independent radius ratio."""
import json,math
from pathlib import Path
from exploration.stellarator_e2e.studies import oracle_entry as oracle,study_route as route
from scripts.study import verify,common
H=Path(__file__).resolve().parents[1];R=H/'results'
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
cases=read(R/'cases.json');inputs=read(R/'package-inputs.json');catalog=read(R/'constraint-catalog.json');frozen=read(H/'context/frozen-results.json');exp=read(H/'context/expectations.json')
baseline=next(c for c in cases if c['inputs'][route.P+'R']==12.7)
checks=[];failures=[];controls=[];ratio_rows=[]
for c in cases:
 radius=c['inputs'][route.P+'R'];channels=oracle.evaluate(c['inputs']);channel_checks={}
 if set(channels)!=set(oracle.ORACLE_OUTPUT_TO_CHANNEL.values()):failures.append('oracle channel set')
 for k,v in channels.items():
  actual=c['outputs'].get(k);deviation=common.relative_deviation(actual,v)
  ok=math.isfinite(actual) and deviation<1e-9
  channel_checks[k]={'native':actual,'oracle':v,'relative_deviation':deviation,'pass':ok}
  if not ok:failures.append([radius,k])
 verdict_checks={}
 for cid,entry in catalog.items():
  derived,resolved=verify.derive_verdict(cid,entry,oracle.operand_bindings(),c['inputs'],inputs,channels)
  want='satisfied' if derived else 'violated';actual=c['verdicts'].get(cid)
  verdict_checks[cid]={'source_local_identity':entry['source_local_identity'],'native':actual,'oracle_rederived':want,'operands_resolved':resolved,'pass':actual==want}
  if actual!=want:failures.append([radius,cid])
 checks.append({'candidate_id':c['candidate_id'],'R':radius,'channels':channel_checks,'verdicts':verdict_checks})
 if radius in (12.7,14.0):
  name='baseline' if radius==12.7 else 'tied_R14';expected=frozen['cases'][name]['native']
  same_set=set(c['outputs'])==set(expected['outputs'])==set(exp['channels']); rows={}
  for k,v in expected['outputs'].items():
   actual=c['outputs'][k];ok=actual==v if radius==12.7 else math.isclose(actual,v,rel_tol=1e-9,abs_tol=1e-9)
   rows[k]={'frozen':v,'actual':actual,'pass':ok}
   if not ok:failures.append(['frozen',radius,k])
  responses={**c['verdicts'],'headline':c['headline']};response_match=responses==expected['responses']
  controls.append({'R':radius,'historical_case':name,'channel_set_exact':same_set,'scalars':rows,'responses':responses,'expected_responses':expected['responses'],'responses_exact':response_match})
  if not same_set or not response_match:failures.append(['frozen set/response',radius])
 # Independent algebra: fixed a/profiles/current/n_coils/coil-centre/reference radii.
 expected_ratios={'geom__V':radius/12.7,'coil_length__c_coil':radius/12.7,'field_calc__B_axis':12.7/radius,'stored_energy__W_mag':12.7/radius,'peak_field_calc__B_peak':(12.7-3.1500000000000004)/(radius-3.1500000000000004),'magnet_cost__capital_cost':1.0}
 ratios={}
 for suffix,expected_ratio in expected_ratios.items():
  key=route.P+suffix;actual_ratio=c['outputs'][key]/baseline['outputs'][key];ok=math.isclose(actual_ratio,expected_ratio,rel_tol=1e-9,abs_tol=1e-9)
  ratios[key]={'expected_ratio':expected_ratio,'actual_ratio':actual_ratio,'pass':ok}
  if not ok:failures.append(['ratio',radius,key])
 ratio_rows.append({'R':radius,'ratios':ratios})
unsupported=sorted(set(inputs)-set(oracle.ENTRY_KEY_TO_ORACLE_INPUT));omitted=sorted(set(baseline['outputs'])-set(oracle.ORACLE_OUTPUT_TO_CHANNEL.values()))
write(R/'all-channel-verification.json',{'outcome':'fail' if failures else 'pass','failures':failures,'cases':checks})
write(R/'frozen-control-verification.json',{'controls':controls,'provenance':'context/frozen-results.json and context/expectations.json; baseline exact, R14 relative/absolute 1e-9; historical chronology caveat in context/consumer-handoff.md'})
write(R/'analytic-ratios.json',{'assumptions':'Held minor radius, plasma shape/profile, coil current, winding count, fixed coil-centre c=3.1500000000000004 m, material/procurement coefficients and reference anchors. V and winding length scale with R; axis field and stored energy inversely with R; peak field inversely with R-c; computed B*R cancellation holds conductor procurement fixed. This does not assert invariant total/decomposed magnet cost or valid physical domain.','cases':ratio_rows})
write(R/'coverage.json',{'supported_input_count':len(oracle.ENTRY_KEY_TO_ORACLE_INPUT),'unsupported_inputs':unsupported,'independent_oracle_channels':sorted(oracle.ORACLE_OUTPUT_TO_CHANNEL.values()),'omitted_independent_channels':omitted,'coverage':'All 141 declared oracle channels and all 18 predicates at every study case; all 158 frozen native scalars and 19 responses at baseline/R14. Other 17-channel values are published for every case but lack independent oracle computation. Unsupported inputs stay fixed; this study does not verify arbitrary overrides.'})
assert not failures,failures
assert len(unsupported)==147 and len(omitted)==17
print('All-case oracle, 158-scalar frozen controls, 19 responses and independent ratios PASS')
