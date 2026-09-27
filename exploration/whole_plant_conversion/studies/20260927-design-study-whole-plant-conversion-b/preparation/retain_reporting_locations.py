"""Retain the original engineered reporting samples after coordinator selection.

Preserve the recomputed proposal and diagnostic comparison. Restore only the
reporting-family quote maps and t values, then re-evaluate with the current oracle.
No native execution or model/oracle/acceptance edits occur here.
"""
from pathlib import Path
import copy,hashlib,json,shutil,sys
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from exploration.whole_plant_conversion.studies import scan_catalog as scanner,proposals
OLD=HERE.parent.parent/'20260927-design-study-whole-plant-conversion/preparation'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,x:p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
source_context=read(OLD.parent/'results/execution-context.json')
assert sha(OLD/'proposed-points.json')==sha(OLD.parent/'proposed-points.json')==source_context['proposal_sha256']
diagnostic=HERE/'recomputed-reporting-locations';diagnostic.mkdir(exist_ok=False)
for name in ('proposed-points.json','reporting-band-plan.json','original-point-comparison.json','case-membership.json','scenario-scan.json','summary.json','window.json'):
 shutil.copyfile(HERE/name,diagnostic/name)
old=read(OLD/'proposed-points.json');new=read(HERE/'proposed-points.json');by_case={r['case']:r for r in old['cases']}
old_members={r['case']:r for r in read(OLD/'case-membership.json')['cases']}
scan=scanner.Scanner(read(HERE/'baseline.json')['point']);scan.cache={r['point_id']:r for r in read(HERE/'oracle-scan.json')['cases']}
allowed={proposals.P+k for k in proposals.GAS_QUOTE_KEYS+proposals.STEAM_QUOTE_KEYS};changes=[]
for row in new['cases']:
 if not any(a['family']=='reporting_boundary' for a in row['aliases']):continue
 assert all(a['family']=='reporting_boundary' for a in row['aliases'])
 original=by_case[row['case']];delta={k:dict(recomputed=row['point'][k],retained=original['point'][k]) for k in row['point'] if row['point'][k]!=original['point'][k]}
 assert set(delta)<=allowed
 assert {a['case'] for a in row['aliases']}=={a['case'] for a in original['aliases']}
 changes.append(dict(case=row['case'],recomputed_point_id=row['point_id'],retained_point_id=original['point_id'],changed_quote_inputs=delta))
 row['point']=copy.deepcopy(original['point']);row['point_id']=original['point_id'];row['aliases']=copy.deepcopy(original['aliases'])
 result=scan.evaluate(row['point']);assert result['status']=='evaluated'
assert len(changes)==56 and all(r['changed_quote_inputs'] for r in changes)
members=[copy.deepcopy(old_members[r['case']]) if r['family']=='reporting_boundary' else r for r in read(HERE/'case-membership.json')['cases']]
assert len({r['point_id'] for r in new['cases']})==2496 and len(members)==2651
summary=read(HERE/'summary.json');summary.update(oracle_evaluations=len(scan.cache),oracle_refusals=sum(r['status']=='oracle_refusal' for r in scan.cache.values()),reporting_sample_location_authority='original engineered points retained by explicit coordinator disposition; corrected oracle recheck passes')
assert summary['oracle_refusals']==0
new['summary']=summary
# Summarize every scenario from the exact point identities now selected.
results={}
for role in members:
 branch=role['branch'];key=(role['scenario'],role['source_MW'],branch);row=scan.cache[role['point_id']]
 entry=results.setdefault(key,dict(scenario=key[0],source_MW=key[1],branch=branch,attempted_aliases=0,eligible_aliases=0,best=None));entry['attempted_aliases']+=1
 if row['eligible'][branch]:
  entry['eligible_aliases']+=1;value=scan.value(row,branch)
  if entry['best'] is None or value<entry['best']['oracle_lcoe_USD2025_MWh']:entry['best']=dict(case=role['case'],point_id=role['point_id'],oracle_lcoe_USD2025_MWh=value,interpretation='planning selection; native ranking required')
scenario=read(HERE/'scenario-scan.json');scenario['results']=list(results.values())
band=copy.deepcopy(read(OLD/'reporting-band-plan.json'))
for bracket in band['brackets']:
 target=bracket['target_gap_USD2025_MWh']
 for endpoint in bracket['bracket']:
  name=endpoint['scenario'];best={b:results[(name,2800.,b)]['best']['oracle_lcoe_USD2025_MWh'] for b in ('gas','steam')}
  endpoint.update(best=best,gap_USD2025_MWh=best['gas']-best['steam'])
 assert bracket['bracket'][0]['gap_USD2025_MWh']>target>bracket['bracket'][1]['gap_USD2025_MWh']
selection=dict(decision_authority='coordinator instruction after exact point comparison: retain originally declared engineered reporting sample locations; no need to move them by floating-point noise',original_record=str(OLD.parent.relative_to(ROOT)),original_snapshot_sha256=sha(OLD.parent/'snapshot.json'),original_proposals_sha256=sha(OLD/'proposed-points.json'),original_reporting_plan_sha256=sha(OLD/'reporting-band-plan.json'),recomputed_diagnostics={p.name:sha(p) for p in sorted(diagnostic.iterdir())},restored_complete_points=len(changes),restored_aliases=sum(r['family']=='reporting_boundary' for r in members),quote_only_differences=True,bracket_signs_rechecked=True,changes=changes)
band['sample_location_selection']={k:v for k,v in selection.items() if k not in ('changes','recomputed_diagnostics')}
window=read(HERE/'window.json');window['reporting_sample_location_selection']=band['sample_location_selection']
write(HERE/'proposed-points.json',new);write(HERE/'case-membership.json',dict(cases=members));write(HERE/'oracle-scan.json',dict(baseline='baseline.json',point_reconstruction='baseline.point updated by input_delta; SHA256 of canonical complete point is point_id',cases=list(scan.cache.values())));write(HERE/'scenario-scan.json',scenario);write(HERE/'reporting-band-plan.json',band);write(HERE/'summary.json',summary);write(HERE/'window.json',window);write(HERE/'reporting-location-selection.json',selection)
print(json.dumps({k:v for k,v in selection.items() if k not in ('changes','recomputed_diagnostics')},indent=2))
