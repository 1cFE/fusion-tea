"""Freeze the first final snapshot and append execution facts to preparatory record."""
import json,hashlib,os,re
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from scripts.study import common
H=Path(__file__).resolve().parents[1];R=H/'results'
read=lambda p:json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def artifacts(directory):
 out=[]
 for root,dirs,files in os.walk(directory,followlinks=False):
  dirs[:]=[d for d in dirs if d not in ['runtime-links','pkg_link','__pycache__'] and not (Path(root)/d).is_symlink()]
  for name in sorted(files):
   p=Path(root)/name
   if p.is_symlink() or name.endswith(('.db-wal','.db-shm','.pyc')):continue
   out.append({'path':str(p.relative_to(H)),'sha256':sha(p)})
 return sorted(out,key=lambda x:x['path'])
def main():
 today=datetime.now(ZoneInfo('America/Los_Angeles')).date().isoformat()
 assert read(H/'reviews/final-approval.json')['approved']
 assert read(R/'all-channel-verification.json')['outcome']=='pass'
 assert not (H/'snapshot.json').exists(),'Final snapshot is write-once'
 summary=read(R/'report-summary.json');manifest=read(H/'context/manifest.json');ind=read(H/'indicators.json');gates=read(R/'preflight.json');ver=read(R/'verification_summary.json');rt=read(R/'runtime.json');compat=read(R/'store-compatibility.json');freeze=read(H/'preparation/reduced-window-freeze.json');execution=read(R/'execution-runtime.json')
 names=['indicator_inputs','recorded_provenance.executable_fingerprint','recorded_provenance.semantic_fingerprint'];content={k:manifest[k] for k in ['ties','objective_catalog','baseline','oracle']};content['fingerprint_names']=names
 content['oracle']['source_digest']=common.tool_source_digest(('exploration/stellarator_e2e/studies/oracle_entry.py','exploration/stellarator_e2e/verify_stellaris.py'));content['oracle']['copied_sources']=['context/oracle_entry.py','context/verify_stellaris.py']
 outputs=artifacts(R);accounts={a['axis']:a for a in read(R/'axis-accounts.json')};correlation=read(R/'correlation.json');axes=read(H/'axes.json')['groups'];defaults=read(R/'package-inputs.json')
 arms=[]
 for arm in summary['arms']:
  if not arm['unique_cases']:continue
  rows=[r for r in correlation if r['arm_id']==arm['arm_id'] and r['scan_status']=='eligible'];bounds={g['axis']:sorted({r['inputs'].get(g['keys'][0]['key'],defaults[g['keys'][0]['key']]) for r in rows}) for g in axes}
  arms.append({'arm_id':arm['arm_id'],'store_id':'plant-native','effective_executable_fingerprint':{'value':compat['executable_fingerprint'],'inputs':None,'no_adapter':True,'note':'Strict native loader; sealed executable identity'},'entry_models':read(R/'entry-models.json'),'strategy':'prepared-list/v1','window':{'bounds':bounds,'provenance':'engineered','correlation':'results/correlation.json','freeze_sha256':sha(H/'preparation/reduced-window-freeze.json')},'verification':{'command':read(H/'execution/verification-command.json'),'tool_revision':ver['tool'],'sampling_scheme':'Native generic stratified sample across every observed verdict combination; additional all-case 141-channel, 18-predicate and 17-scalar verification','tolerance':{'oracle_channels_relative':1e-9,'residual_relative_and_absolute':1e-9},'summary_sha256':sha(R/'verification_summary.json')},'glue_ledger':[],'glue_ledger_none':True,'artifacts':[x for x in outputs if x['path'] in ['results/points.csv','results/correlation.json','results/native-points.csv','results/all-channel-verification.json']]})
 findings=[
 ('1','model','Computed versus held availability has no modeled reliability resistance.','Sensitivity-only owner ruling; reliability model remains missing.','unrouted'),
 ('2','model','Outage duration has no modeled maintenance-resource or access resistance.','Retain 5/7/10-month conditional comparison.','unrouted'),
 ('3','model','Residual unplanned downtime has no modeled reliability response.','Retain 0/0.05/0.10 conditional comparison.','unrouted'),
 ('4','model','Burn fraction changes fuel flows and costs without a resisting modeled processing limit.','Retain 0.025/0.05/0.10 sensitivity and fuel-capacity gap.','unrouted'),
 ('5','model',f"The current study has {summary['fully_satisfied']} fully satisfied cases among {summary['unique_cases']} distinct executed cases.",'Sampled model satisfaction only; no buildability or global-optimum certification.','documented seam: current plant comparison'),
 ('6','model','Representative loop and cycle fits lack separately sized equipment costs and materials qualification.','Bounded source/calibration transfer; fresh grader assesses full anchors.','unrouted'),
 ('7','model','Fuel throughput and pressure-conditional pumping speed leave inventory, startup and installed vacuum-train evidence missing.','Retain complete rubric conjuncts and missing source inputs.','unrouted'),
 ('8','model','Physical required TBR and its margin are published but the authored TBR predicate still checks the held floor.','Retain the computed conditional deficit separately from predicate satisfaction; no recovery tuning.','documented seam: breeding adequacy'),
 ('9','process','Pre-execution critique found three changing direct-control inputs missing from the declaration.','Corrected before baseline and scan; original review and objective disposition retained.','reviews/pre-execution-disposition.md'),
 ('10','process','The initial serial scan was stopped for performance and replaced by isolated parallel oracle evaluations.','Original script/log retained; exact control equality passed; proposal and native lifecycle unchanged.','execution/scan-operational-note.md'),
 ('12','process','The owner stopped the exhaustive replay after 2525 completed cases and requested risk-focused reduction.','Use the 371-case primary store for native counts; retain full-window oracle evidence and stopped-store prefix checks separately.','preparation/reduction-amendment.md'),
 ('11','process','Inherited certificates retain the historical quarantined-file hashing violation and claim-specific audit limits.','No historical compliance or independent item-audit claim added; owner acceptance remains separate.','context/consumer-audit.md')]
 write(H/'preparation/findings.json',findings)
 snap={'snapshot_schema_version':'1','study_id':H.name,'status':'Final executor record; fresh review dispositioned; administration and owner acceptance remain separate','package':{'path':manifest['package']['path'],'package_name':'stellarator_tea','repo_commit':execution['repo_revision'],'git_clean':True},'fingerprints':{'indicator_inputs':ind['package']['indicator_input_fingerprint'],'recorded_provenance.executable_fingerprint':compat['executable_fingerprint'],'recorded_provenance.semantic_fingerprint':compat['model_contract_fingerprint']},'manifest':{'path':'context/manifest.json','schema_version':manifest['schema_version'],'digest':sha(H/'context/manifest.json'),'content_used':content},'stores':[{'store_id':'plant-native','path':'results/targeted-store/'+H.name+'.db','sha256':sha(R/'targeted-store'/f'{H.name}.db'),'compatibility_tuple':compat}],'arms':arms,'declined_arms':[a for a in summary['arms'] if not a['unique_cases']],'tools':[ind['tool'],gates['tool'],ver['tool']],'teax':{'revision':rt['teax_revision'],'era_pin':None,'runtime':'results/runtime.json'},'indicators':{'path':'indicators.json','sha256':sha(H/'indicators.json'),'output_schema_version':ind['schema_version'],'axis_declaration':{'path':'axes.json','schema_version':'study-axis-declaration/v1','digest':sha(H/'axes.json'),'groups_declared':[g['axis'] for g in axes],'subset':False}},'result_artifacts':outputs,'support_artifacts':[{'path':p,'sha256':sha(H/p)} for p in ['study.py','axes.json','.gitignore','execution-reading.md']],'gaps':['The sealed generated package and runtime installation are not copied; re-execution requires their named identities.','Both the primary reduced native store and stopped exhaustive store are retained locally and gitignored. Complete reduced numeric exports, verdicts, inputs and compatibility are committed. The stopped store is supporting evidence only; 2525 cases completed before the owner-directed stop.','No fresh administrator synthesis, consolidated grading or owner acceptance is claimed by this executor.']}
 for k,d in [('context_artifacts','context'),('preparation_artifacts','preparation'),('execution_artifacts','execution'),('review_artifacts','reviews')]:snap[k]=artifacts(H/d)
 snap['interrupted_executions']=[read(R/'interrupted-execution-summary.json')]
 snap['date_completed']=today
 write(H/'snapshot.json',snap)
 text='\n## Addendum 2026-09-12 — completed execution\n\nThis addendum supersedes the preparatory status statements above with completed execution evidence. Earlier preparatory text is retained. The complete numerical reading is `execution-reading.md`; resolved values and digests are in the first final `snapshot.json`.\n\n'
 text+=(H/'execution-reading.md').read_text().replace('# Plant-closure execution reading','### Completed study reading',1)
 text+='\n### Per-axis framing account\n\nEvery axis remains sensitivity-framed. Coordinated control terms are interpreted only within their declared blocks. No boundary claim is made.\n\n'
 for g in axes:
  a=accounts[g['axis']];text+=f"#### {g['axis']} — feasible structure (search framing)\n\n**Applies:** not applicable — sensitivity-framed.\n\n#### {g['axis']} — observed response (sensitivity framing)\n\n**Applies:** yes. The exact {len(a['values'])} observed values, objective ranges and locations of every violated predicate are retained in `results/axis-accounts.json` under axis `{g['axis']}`. Interpretation is conditional on the coordinated arms in `results/correlation.json`; aggregate bins do not establish a causal slope.\n\n"
 text+='### Execution findings\n\n| Id | Kind | Finding | Disposition | Home |\n|---|---|---|---|---|\n'+'\n'.join(f'| `{H.name}#{n}` | {k} | {f} | {d} | `{home}` |' for n,k,f,d,home in findings)+'\n\n'
 text+='### Final snapshot and review\n\n- **File:** snapshot.json\n- **sha256:** '+sha(H/'snapshot.json')+'\n- **Schema version:** 1\n\nFresh correctness/honesty/readability review and its disposition are in `reviews/final-review.md` and `reviews/final-disposition.md`. No executor self-certification replaces that review. The four sensitivity rulings remain as quoted in the retained intake and trail.\n'
 text=text.replace('## Addendum 2026-09-12','## Addendum '+today)
 assert '<' not in text
 with (H/'record.md').open('a') as f:f.write(text)
 log=H.parent/'DISCOVERY_LOG.md';existing=log.read_text();rows=[]
 for n,k,f,d,home in findings:
  identifier=H.name+'#'+n
  if '| `'+identifier+'` |' not in existing:
   resolved=H.name+'/'+home if home.startswith(('context/','reviews/','execution/','preparation/')) else home
   rows.append(f'| {today} | `{k}` | `{identifier}` | {f} | {d} | `{resolved}` |')
 with log.open('a') as f:f.write('\n'.join(rows)+'\n')
 print('First final snapshot frozen; completed execution appended; native first sightings registered')
if __name__=='__main__':main()
