"""Seal final stored native results, independent checks and their exact sources."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import sys
import tarfile
import tempfile

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from scripts.study import common
from exploration.exchanger_architecture.thermal_requirements.studies import study_route as route
p=argparse.ArgumentParser();p.add_argument('--record',type=Path,required=True);args=p.parse_args()
record=args.record.resolve();results=record/'results';route.MANIFEST_PATH=record/'manifest.json'
assert not (record/'snapshot.json').exists(),'preserve sealed snapshot'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
cases=read(results/'cases.json')['cases'];verification=read(results/'verification_summary.json')
assert verification['outcome']=='pass' and all(r['state']=='completed' for r in cases)
context=read(results/'execution-context.json');integration=read(results/'integration_return_used.json')
manifest=read(results/'manifest_used.json');indicators=read(record/'indicators.json')
assert integration['class']=='CANDIDATE' and read(route.MANIFEST_PATH)==manifest
assert sha(route.MANIFEST_PATH)==indicators['manifest']['digest']
expected=integration['candidate']['executable_fingerprint']
assert {r['executable_fingerprint'] for r in cases}=={expected} and route.interface()['executable_fingerprint']==expected
common.assert_tree_clean(route.PACKAGE_DIR)
with tempfile.TemporaryDirectory(prefix='thermal-freeze-') as tmp:
    prepared=route.prepare(route.PACKAGE_DIR,Path(tmp))
    entry_models={k:f'{v.__module__}.{v.__name__}' for k,v in prepared.entry_models.items()}
preflight=read(record/'preparation/preflight.json')
tools=[indicators['tool'],verification['tool'],preflight['tool']]
paths=set()
for tool in tools+[integration['tool']]:paths.update(r['path'] for r in tool['source_digest']['files'])
paths.update(p.relative_to(ROOT).as_posix() for p in route.HERE.glob('*.py'))
paths.update(p.relative_to(ROOT).as_posix() for p in route.E2E.glob('*.py'))
for folder in ('models','bodies','input_models','tests'):
    paths.update(p.relative_to(ROOT).as_posix() for p in (route.E2E/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/'exploration/aries_integrated/studies').glob('*.py'))
work=ROOT/'work/active/WI-097_exchanger-thermal-requirements'
paths.update(p.relative_to(ROOT).as_posix() for p in work.glob('*.md'))
paths.update(p.relative_to(ROOT).as_posix() for p in (work/'evidence').glob('*') if p.is_file() and p.suffix in ('.md','.py','.json','.log'))
goal=ROOT/'work/orchestration/goals/design-study-exchanger-architecture'
paths.update(p.relative_to(ROOT).as_posix() for p in (goal/'evidence').glob('r[23]-*') if p.is_file())
paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/'work/active/WI-086_aries-dual-blanket-heat-accounting/evidence').glob('raffray-p*.png'))
paths.update(['modeling_project/REQUIREMENTS.md',route.MANIFEST_PATH.relative_to(ROOT).as_posix(),(route.HERE/'ANNEX.md').relative_to(ROOT).as_posix()])
for relative in sorted(paths):
    source=ROOT/relative
    if not source.is_file():raise ValueError('missing declared source '+relative)
    target=results/'sources'/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
archive=record/'sealed-package.tar.gz'
assert not archive.exists()
with tarfile.open(archive,'w:gz') as tar:
    for path in sorted(route.PACKAGE_DIR.rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts and path.suffix!='.pyc':tar.add(path,arcname=route.PACKAGE_NAME+'/'+path.relative_to(route.PACKAGE_DIR).as_posix())
store=results/'native'/(record.name+'.db')
con=sqlite3.connect('file:'+str(store)+'?mode=ro&immutable=1',uri=True);con.row_factory=sqlite3.Row
compatibility=dict(con.execute('select * from compatibility').fetchone());compatibility.pop('singleton')
assert con.execute("select count(*) from cases where state='completed'").fetchone()[0]==len(cases);con.close()
content=copy.deepcopy(manifest);content['fingerprint_names']=['indicator_inputs','recorded_provenance.executable_fingerprint','recorded_provenance.semantic_fingerprint']
content['oracle']['source_digest']=common.tool_source_digest(tuple(sorted(p.relative_to(ROOT).as_posix() for p in route.HERE.glob('*.py'))))
artifacts=[{'path':p.relative_to(record).as_posix(),'sha256':sha(p)} for p in sorted(record.rglob('*')) if p.is_file() and p.name not in ('record.md','snapshot.json','synthesis.md') and '__pycache__' not in p.parts and 'pkg_link' not in p.parts and p.suffix!='.pyc' and not p.name.endswith(('-wal','-shm'))]
snapshot={
 'snapshot_schema_version':'1','study_id':record.name,
 'package':{'path':route.PACKAGE_DIR.relative_to(ROOT).as_posix(),'package_name':route.PACKAGE_NAME,'repo_commit':context['repo_commit_at_execution'],'git_clean':True},
 'fingerprints':{'indicator_inputs':indicators['package']['indicator_input_fingerprint'],'recorded_provenance.executable_fingerprint':expected,'recorded_provenance.semantic_fingerprint':integration['candidate']['semantic_fingerprint']},
 'manifest':{'path':route.MANIFEST_PATH.relative_to(ROOT).as_posix(),'schema_version':manifest['schema_version'],'digest':indicators['manifest']['digest'],'content_used':content},
 'stores':[{'store_id':record.name,'path':store.relative_to(record).as_posix(),'compatibility_tuple':compatibility}],
 'arms':[{'arm_id':'arm-architecture','store_id':record.name,'effective_executable_fingerprint':{'value':expected,'inputs':None,'no_adapter':True},'entry_models':entry_models,'strategy':compatibility['strategy_identity'],'window':{'bounds':read(record/'axis-plan.json')['axes'],'provenance':'engineered'},'verification':{'command':context['verification_command'],'tool_revision':verification['tool']['source_digest'],'sampling_scheme':verification['stores'][0]['sampling'],'tolerance':{'relative':1e-9,'absolute_tolerances':manifest['absolute_tolerances'],'exact_verdicts':True},'summary_sha256':sha(results/'verification_summary.json')},'glue_ledger':[],'glue_ledger_none':True,'artifacts':artifacts}],
 'tools':tools,'teax':{'revision':integration['toolchain']['teax_revision'],'era_pin':None,'identity_evidence':'results/integration_return_used.json'},
 'indicators':{'path':'indicators.json','sha256':sha(record/'indicators.json'),'output_schema_version':indicators['schema_version'],'axis_declaration':indicators['axis_declaration']},
 'execution_context':'results/execution-context.json','case_count':len(cases),'numeric_outputs_per_case':sorted({len(r['outputs']) for r in cases}),'verified_numeric_channels_per_case':len(verification['channels_checked']),'exact_verdicts_per_case':len(verification['constraints_rederived']),'all_scoped_checks_satisfied_count':sum(all(v=='satisfied' for v in r['verdicts'].values()) for r in cases),
 'science_qualification':'Conditional N-R primary returns, full delivered duty and all six actual primary-exchanger terminal minima enforced. Explicit fixed area/price offers and physical primary bypass. Constant U, ideal mixing and supplied source remain assumptions. No plant, source, actuator, procurement or hydraulic qualification. Unknown incremental costs/power remain break-even allowances. Best tested operations are not global optima.'}
(record/'snapshot.json').write_text(json.dumps(snapshot,indent=2)+'\n')
print(json.dumps({'cases':len(cases),'artifacts':len(artifacts),'snapshot_sha256':sha(record/'snapshot.json')}))
