"""Select from retained screening results; never evaluate new physics here."""
import json
from pathlib import Path
H=Path(__file__).resolve().parents[1];R=H/'results';read=lambda p:json.loads(p.read_text());write=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n')
initial=read(R/'initial-oracle-scan.json')['rows'];refine=read(R/'refine-oracle-scan.json')['rows'];ranked=read(R/'ranked.json');defaults=read(H/'preparation/resolved-defaults.json')
def key(p):return json.dumps(defaults|p,sort_keys=True)
selected=[r for r in initial if r['family']=='control' or r['full_satisfied']]
selected += [r for r in ranked if r['family']=='initial-search' and not r['full_satisfied']][:6]
selected += [r for r in refine if r['outcome']=='evaluated']
unique={};props=[]
for r in selected:
 k=key(r['point']);pid=unique[k]['id'] if k in unique else r['id'];row={k:r[k] for k in ['id','family','point']};row.update(proposal_id=r['id'],canonical_proposal_id=pid,arm='arm-native');props.append(row)
 if k not in unique:unique[k]=row
ur=list(unique.values());assert len(ur)+1<=600
write(H/'preparation/proposals.json',props);write(H/'preparation/unique-proposals.json',ur);write(R/'oracle-scan.json',{'rows':initial+refine,'note':'Original stage rows preserved, including duplicates, failures and refusals.'})
summary={'screening_calls':len(initial)+len(refine),'unique_screening_coordinates':len({key(r['point']) for r in initial+refine}),'screening_evaluated_calls':sum(r['outcome']=='evaluated' for r in initial+refine),'screening_refused_calls':sum(r['outcome']=='refused' for r in initial+refine),'native_candidate_calls_planned':len(ur),'native_unique_including_baseline_planned':len(ur)+1,'retained_plot_refusals':sum(r['outcome']=='refused' and r['family']=='map' for r in refine),'generated_calls_already_completed':1,'mechanical_launch_failures_before_evaluation':2,'verification_oracle_calls':'recorded separately after generic verification'}
assert summary['unique_screening_coordinates']<=3000
write(H/'preparation/campaign-counts-planned.json',summary)
(H/'reviews/window-selection.md').write_text('# Window selection\n\n[AGENT] Initial screening found five valid all-screen oracle points; original prepared bounds remain unchanged. Refinement declares a fixed local R/current map and two-sided individual/combined neighbors around the retained engineering-margin anchor. Every evaluated map and neighbor coordinate is selected for native execution; domain refusals stay separate. Exact r2 controls, all five initial passes and six informative near misses are included. No native result is claimed yet. Selection and full override keys are retained in preparation/refinement-selection.json and unique-proposals.json.\n')
print(summary)
