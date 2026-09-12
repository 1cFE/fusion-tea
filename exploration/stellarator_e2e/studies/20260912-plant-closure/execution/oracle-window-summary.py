"""Summarize the complete oracle scan, explicitly separate from native execution."""
import json,csv
from pathlib import Path
from collections import Counter
H=Path(__file__).resolve().parents[1];R=H/'results';P='stellarator_09__stellaris__'
read=lambda p:json.loads(p.read_text())
def main():
 corr=read(H/'preparation/correlation.json');oracle={x['proposal_key']:x for x in read(H/'preparation/oracle-scan.json')};defaults=read(R/'package-inputs.json');pc=read(H/'preparation/predicate-correlation.json');cat=read(R/'constraint-catalog.json')
 sets={era:[x['current_id'] for x in pc if x['era']==era] for era in ['old-ten','round1-fourteen']};sets['current-eighteen']=list(cat)
 old={r['case_id']:r for r in csv.DictReader((H/'context/historical-points.csv').open())};groups={};comparisons=[]
 for row in corr:
  if not row['arm_id'].startswith('arm-window'):continue
  prior=old.get(row['historical_id']);r={'arm_id':row['arm_id'],'historical_id':row['historical_id'],'historical_arm':row['historical_arm'],'installed_power_MW':row['inputs'].get(P+'p_wallplug_heat',defaults[P+'p_wallplug_heat']),'oracle_status':row['scan_status'],'proposal_key':row['proposal_key']}
  if row['scan_status']=='eligible':
   e=oracle[row['proposal_key']];r.update(lcoe=e['channels'][P+'lcoe_calc__lcoe'],lcoe_1cfe=e['channels'][P+'lcoe_1cfe_calc__lcoe'],satisfied_sets={name:all(e['verdicts'][cid]=='satisfied' for cid in ids) for name,ids in sets.items()},old_ten_flips=[{'source_local_identity':x['source_local_identity'],'historical':prior[x['source_local_identity']],'current_oracle':e['verdicts'][x['current_id']]} for x in pc if x['era']=='old-ten' and prior and prior[x['source_local_identity']]!=e['verdicts'][x['current_id']]])
  else:r['reason']=row['exclusion_reason']
  comparisons.append(r);groups.setdefault((r['arm_id'],r['historical_arm'],r['installed_power_MW']),[]).append(r)
 summaries=[]
 for (arm,oldarm,power),rows in sorted(groups.items()):
  eligible=[r for r in rows if r['oracle_status']=='eligible'];mins={}
  for name in sets:
   passing=[r for r in eligible if r['satisfied_sets'][name]]
   if passing:
    m=min(passing,key=lambda r:r['lcoe']);e=oracle[m['proposal_key']];mins[name]={'historical_id':m['historical_id'],'inputs':e['inputs'],'lcoe':m['lcoe'],'lcoe_1cfe':m['lcoe_1cfe'],'aspect_ratio':e['channels'][P+'radial_build__A'] if P+'radial_build__A' in e['channels'] else (e['inputs'].get(P+'R',defaults[P+'R'])/e['inputs'].get(P+'a',defaults[P+'a']))}
   else:mins[name]=None
  summaries.append({'arm_id':arm,'historical_arm':oldarm,'installed_power_MW':power,'oracle_status_counts':dict(Counter(r['oracle_status'] for r in rows)),'oracle_satisfaction_counts':{name:sum(r['satisfied_sets'][name] for r in eligible) for name in sets},'oracle_minima':mins})
 for name,data in [('oracle-historical-comparison.json',{'basis':'Full independent oracle scan; not exhaustive native execution. Original source IDs retained.','rows':comparisons}),('oracle-window-summary.json',{'basis':'Full independent oracle scan; selected candidate minima and verdict patterns are separately native-verified.','groups':summaries})]:(R/name).write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
 print('Separated full-oracle historical summaries written',len(comparisons),'rows')
if __name__=='__main__':main()
