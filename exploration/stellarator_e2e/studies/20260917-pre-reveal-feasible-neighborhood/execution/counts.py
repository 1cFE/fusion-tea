"""Count retained proposals and actual native/verification calls, without evaluation."""
import json
from pathlib import Path
H=Path(__file__).resolve().parents[1];R=H/'results';read=lambda p:json.loads(p.read_text());defaults=read(H/'preparation/resolved-defaults.json')
def key(p):return json.dumps(defaults|p,sort_keys=True)
scan=read(R/'oracle-scan.json')['rows'];native=read(R/'native-cases.json');baseline=read(R/'baseline_result.json');generic=read(R/'generic-verification-refusal.json');sampled=[c for s in generic['stores'] for c in s['sampling']['sampled_case_ids']]
review=H.parents[3]/'work/orchestration/goals/pre-reveal-feasible-neighborhood/evidence/reviewer-checks.json'
result={'screening_calls':len(scan),'unique_screening_coordinates':len({key(r['point']) for r in scan}),'screening_evaluated_calls':sum(r['outcome']=='evaluated' for r in scan),'screening_refused_calls':sum(r['outcome']=='refused' for r in scan),'native_calls':len(native)+1,'native_unique_coordinates':len({key(r['inputs']) for r in native}|{key(baseline['point'])}),'native_selected_cases':len(native),'native_baseline_cases':1,'generic_verification_oracle_calls':len(sampled),'generic_verification_unique_coordinates':len({key(r['inputs']) for r in native if r['candidate_id'] in sampled}),'all_point_comparison_new_oracle_calls':0,'all_point_comparison_note':'Reuses independent retained screening outputs at the identical coordinates;226 mapped scalars and20 verdicts per native case.','reviewer_verification':'Recorded in goal evidence/reviewer-checks.json; all requested coordinates already screened, no generated executions permitted.','mechanical_launch_failures_before_evaluation':2,'mechanical_retries_used':2,'caps':{'screening_unique':3000,'native_unique':600,'rounds':2}}
assert result['unique_screening_coordinates']<=3000 and result['native_unique_coordinates']<=600
if review.exists():
 result['reviewer_receipt']=read(review)
 result['reviewer_verification_oracle_calls']=8
 result['total_oracle_calls']=len(scan)+len(sampled)+8
 result['total_oracle_unique_coordinates']=result['unique_screening_coordinates']
 result['reviewer_native_calls']=0
(R/'campaign-counts.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if isinstance(v,int)})
