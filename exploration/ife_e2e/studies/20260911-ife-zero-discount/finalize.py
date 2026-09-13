"""Resolve the record's data snapshot from retained evidence, without execution."""
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess

HERE = Path(__file__).resolve().parent
R = HERE / 'results'
def read(path):
    return json.loads(path.read_text())
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def artifact(path):
    return {'path': str(path.relative_to(HERE)), 'sha256': digest(path)}

manifest = read(R/'context/manifest.json')
indicators = read(HERE/'indicators.json')
verification = read(R/'verification_summary.json')
preflight = read(R/'preflight.json')
fp = {'indicator_inputs': indicators['package']['indicator_input_fingerprint']}
fp.update({'recorded_provenance.'+key:value for key,value in manifest['fingerprints']['recorded_provenance'].items()})
db = R/'_work'/f'{HERE.name}.db'
connection = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
connection.row_factory = sqlite3.Row
compat = dict(connection.execute('select * from compatibility').fetchone())
compat.pop('singleton')
connection.close()
arm = {'arm_id':'arm-ife','store_id':'ife-main',
 'effective_executable_fingerprint':{'value':manifest['fingerprints']['recorded_provenance']['executable_fingerprint'],'inputs':None,'no_adapter':True,'note':'The sealed fingerprint is the execution identity; no adapter.'},
 'entry_models':read(R/'entry-models.json'),'strategy':'prepared-list/v1','window':read(R/'window.json'),
 'verification':{'command':f'.codex-test/run bash -c \'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python {HERE.relative_to(Path.cwd())}/execute.py execute\'', 'tool_revision':verification['tool']['source_digest'],'sampling_scheme':verification['stores'][0]['sampling'],'tolerance':verification['tolerance'],'summary_sha256':digest(R/'verification_summary.json')},
 'glue_ledger':[],'glue_ledger_none':True,
 'artifacts':[artifact(p) for p in sorted(R.rglob('*')) if p.is_file() and not p.is_symlink() and '__pycache__' not in p.parts and 'pkg_link' not in p.parts]}
snapshot={'snapshot_schema_version':'1','study_id':HERE.name,'package':{'path':manifest['package']['path'],'package_name':'ife_tea','repo_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'git_clean':True},'fingerprints':fp,
 'manifest':{'path':'results/context/manifest.json','schema_version':manifest['schema_version'],'digest':digest(R/'context/manifest.json'),'content_used':{**{key:manifest[key] for key in ['ties','objective_catalog','baseline','oracle']},'fingerprint_names':list(fp)}},
 'stores':[{'store_id':'ife-main','path':str(db.relative_to(HERE)),'compatibility_tuple':compat}], 'arms':[arm], 'tools':[indicators['tool'],preflight['tool'],verification['tool']],
 'indicators':{'path':'indicators.json','sha256':digest(HERE/'indicators.json'),'output_schema_version':indicators['schema_version'],'axis_declaration':indicators['axis_declaration']},
 'protocol':{**artifact(HERE/'protocol.md'),'pre_execution_review':artifact(HERE/'pre-execution-review.md')},
 'execution':artifact(HERE/'execute.py'),'reference_check':artifact(HERE/'reference_check.py'),
 'teax':{'revision':'8d877460ac4f6f264561d916e40c1708adb13397','era_pin':None},
 'post_execution_review':artifact(HERE/'post-execution-review.md') if (HERE/'post-execution-review.md').exists() else None}
(HERE/'snapshot.json').write_text(json.dumps(snapshot,indent=2)+'\n')
record = (HERE/'record.md').read_text()
import re
record = re.sub(r'(?m)^- \*\*sha256:\*\* .*$', '- **sha256:** '+digest(HERE/'snapshot.json'), record)
(HERE/'record.md').write_text(record)
