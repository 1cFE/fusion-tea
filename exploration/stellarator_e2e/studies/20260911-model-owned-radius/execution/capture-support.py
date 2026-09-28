"""Copy an explicit permitted support list; never enumerate the repository for preservation."""
import json,hashlib,subprocess
from pathlib import Path
H=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
rows=read(H/'context/provenance.json')
sources={
'T-021-assessment.md':'work/analysis/20260911-230953_radius-ownership.md',
'stellaris-table2.png':'work/analysis/20260911-230953_radius-ownership-evidence/stellaris-table2.png',
'T-021-probe.py':'work/analysis/20260911-230953_radius-ownership-evidence/probe.py',
'baseline_result.v1.schema.json':'scripts/study/schemas/baseline_result.v1.schema.json',
'preflight.py':'scripts/study/preflight.py','verify.py':'scripts/study/verify.py','indicators.py':'scripts/study/indicators.py',
'common.py':'scripts/study/common.py','manifest.py':'scripts/study/manifest.py','identity.py':'scripts/study/identity.py',
'codex-test-setup.md':'.project/codex-test-setup.md',
}
for name,source in sources.items():
 p=Path(source);assert 'knowledge/holdout' not in str(p.resolve());data=p.read_bytes();(H/'context'/name).write_bytes(data)
 rows.append({'path':'context/'+name,'source_path':source,'source_commit':subprocess.check_output(['git','log','-1','--format=%H','--',source],text=True).strip(),'sha256':hashlib.sha256(data).hexdigest(),'status':'copied retained evidence/source, not new execution'})
for row in rows:
 p=Path(row['source_path']);commit=row['source_commit']
 if commit:
  proc=subprocess.run(['git','show',commit+':'+row['source_path']],capture_output=True)
  row['source_commit_bytes_match']=proc.returncode==0 and hashlib.sha256(proc.stdout).hexdigest()==row['sha256']
 else:row['source_commit_bytes_match']=None;row['provenance_gap']='No repository commit for this installed/untracked path; copied bytes identified by digest.'
write(H/'context/provenance.json',rows)
# Copy inherited adverse records into an unmistakably separate diagnostic index.
frozen=read(H/'context/frozen-results.json');newer=read(H/'context/WI-051-results.json');checks=read(H/'context/WI-051-checks.json')
write(H/'diagnostics/retained-evidence.json',{'evidence_class':'Retained T-021 at 2f8856b7 and WI-051 implementation at 641c1051; NOT new T-026 execution','T-021_cases':{k:v for k,v in frozen['cases'].items() if k not in ['baseline','tied_R14']},'T-021_component':frozen['component'],'WI-051_invalid_and_retired':{k:v for k,v in newer.items() if k not in ['baseline','R14']},'WI-051_component':checks['component'],'complete_source_files':['context/frozen-results.json','context/WI-051-results.json','context/WI-051-checks.json','context/expectations.json'],'provenance':'context/provenance.json; context/consumer-handoff.md supplies chronology corrections','new_diagnostic_execution':False})
# Verify every effective native input stays fixed apart from the one R key.
effective=read(H/'results/effective-inputs.json');base=read(H/'results/baseline-effective-inputs.json');P='stellarator_09__stellaris__';changes=[]
for c in effective:
 diffs=[{'group':g,'key':k,'baseline':base[g][k],'actual':v} for g,values in c['groups'].items() for k,v in values.items() if v!=base[g][k]]
 assert set(c['groups'])==set(base)
 assert all(set(values)==set(base[g]) for g,values in c['groups'].items())
 assert all(d['key']==P+'R' for d in diffs)
 assert set(c['proposal'])=={P+'R'}
 changes.append({'candidate_id':c['candidate_id'],'changed_fields':diffs,'all_other_fields_identical':True})
write(H/'results/fixed-input-verification.json',{'outcome':'pass','public_inputs':sum(len(x) for x in base.values()),'cases':changes,'reference_anchors':{k:v for g in base.values() for k,v in g.items() if k in [P+'magnet__R_ref',P+'magnet__a_coil_ref',P+'wall_peak_R_ref',P+'R_ref_divertor']}})
print('Captured',len(rows),'provenance entries, retained diagnostics, and complete fixed-input checks')
