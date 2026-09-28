"""Resolve the complete study snapshot after all evidence is present; do not rerun after commit."""
import hashlib,json,os,subprocess,shutil
from pathlib import Path
from scripts.study import common
H=Path(__file__).resolve().parents[1];ROOT=H.parents[3];R=H/'results'
read=lambda p:json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def artifacts(d):
 return sorted([{'path':str(p.relative_to(H)),'sha256':sha(p)} for p in d.rglob('*') if p.is_file() and not p.is_symlink() and '__pycache__' not in p.parts and 'pkg_link' not in p.parts and not p.name.endswith(('.db-shm','.db-wal','.pyc'))],key=lambda r:r['path'])
assert not (H/'snapshot.json').exists(),'Snapshot is write-once'
m=read(H/'preparation/manifest.json');ind=read(H/'indicators.json');pre=read(R/'preflight_results.json');ver=read(R/'verification_summary.json');exe=read(R/'execution-summary.json');ident=read(R/'package_identity.json');allv=read(R/'oracle-all-points.json')
assert pre['outcome']=='pass';assert allv['outcome']=='pass';common.assert_tree_clean(ROOT/'exploration/stellarator_e2e/generated')
release=read(H/'preparation/integration-return.json')['candidate']; assert ident['identity']['digest']==release['executable_fingerprint']
assert m['fingerprints']['recorded_provenance']['semantic_fingerprint']==release['semantic_fingerprint']
tools=[ind['tool'],pre['tool'],ver['tool']]
local=[str(p.relative_to(ROOT)) for p in sorted((H/'execution').glob('*.py'))]+[str((H/'study.py').relative_to(ROOT))]
tools.append({'path':str((H/'execution/execute.py').relative_to(ROOT)),'source_digest':common.tool_source_digest(tuple(local))})
for t in tools:
 for f in t['source_digest']['files']:
  src=ROOT/f['path'];dest=H/'preparation/tool-sources'/f['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
content={k:m[k] for k in ('ties','objective_catalog','baseline','oracle')};content['oracle']['source_digest']=common.tool_source_digest(('exploration/stellarator_e2e/verify_stellaris.py','exploration/stellarator_e2e/oracle_finance.py','exploration/stellarator_e2e/studies/oracle_entry.py'))
content['fingerprint_names']=['indicator_inputs','recorded_provenance.executable_fingerprint','recorded_provenance.semantic_fingerprint']
props=read(H/'preparation/unique-proposals.json');axes=read(H/'axes.json')['groups'];entry=read(R/'entry-models.json')
rev=subprocess.check_output(['git','-C',os.environ['STOP_PARSER_TEAX_ROOT'],'rev-parse','HEAD'],text=True).strip();assert rev==read(H/'preparation/integration-return.json')['toolchain']['teax_revision']
arm={'arm_id':'arm-native','store_id':'study','effective_executable_fingerprint':{'value':release['executable_fingerprint'],'inputs':None,'no_adapter':True,'note':'Stock strict loader; sealed executable identity.'},'entry_models':entry,'strategy':{'kind':'PreparedListStrategy','definition_fingerprint':read(R/'store-compatibility.json')['study_definition_fingerprint'],'proposals':len(props)},'window':{'bounds':{g['axis']:sorted({r['point'][g['keys'][0]['key']] for r in props}) for g in axes},'provenance':'engineered','unique_points':len(props),'report_rows':len(read(H/'preparation/proposals.json'))},'verification':{'command':ver['command'],'tool_revision':ver['tool']['source_digest'],'sampling_scheme':'Generic stratification by observed verdict combination plus all unique-case mapped scalars and eighteen oracle-derived verdicts','tolerance':{'relative':1e-9,'absolute_for_all_point_scalar_checks':1e-12,'predicate_operators':'exact authored operators'},'summary_sha256':sha(R/'verification_summary.json'),'all_points_sha256':sha(R/'oracle-all-points.json')},'glue_ledger':[],'glue_ledger_none':True,'artifacts':artifacts(R)}
snap={'snapshot_schema_version':'1','study_id':H.name,'package':{'path':m['package']['path'],'package_name':'stellarator_tea','repo_commit':exe['repo_revision'],'git_clean':True},'fingerprints':{'indicator_inputs':m['fingerprints']['indicator_inputs'],'recorded_provenance.executable_fingerprint':release['executable_fingerprint'],'recorded_provenance.semantic_fingerprint':release['semantic_fingerprint']},'manifest':{'path':'preparation/manifest.json','schema_version':m['schema_version'],'digest':sha(H/'preparation/manifest.json'),'content_used':content},'stores':[{'store_id':'study','path':exe['store'],'compatibility_tuple':read(R/'store-compatibility.json')}],'arms':[arm],'tools':tools,'teax':{'revision':rev,'era_pin':None},'indicators':{'path':'indicators.json','sha256':sha(H/'indicators.json'),'output_schema_version':ind['schema_version'],'axis_declaration':{'path':'axes.json','schema_version':'study-axis-declaration/v1','digest':sha(H/'axes.json'),'groups_declared':[g['axis'] for g in axes],'subset':False}},'integration_candidate_pin':release['pin'],'preparation_artifacts':artifacts(H/'preparation'),'review_artifacts':artifacts(H/'reviews'),'execution_artifacts':artifacts(H/'execution'),'definition_artifacts':[{'path':'study.py','sha256':sha(H/'study.py')},{'path':'protocol.md','sha256':sha(H/'protocol.md')}],'entering_reference':{'kind':'captured independent oracle, not native old-package execution','repository_revision':read(H/'preparation/entering/comparison.json')['revision'],'identity':read(H/'preparation/entering/package-identity.json')}}
(H/'snapshot.json').write_text(json.dumps(snap,indent=2,allow_nan=False)+'\n')
print('SNAPSHOT',sha(H/'snapshot.json'),'artifacts',sum(len(snap[k]) for k in ['preparation_artifacts','review_artifacts','execution_artifacts','definition_artifacts'])+len(arm['artifacts']))
