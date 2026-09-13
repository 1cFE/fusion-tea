import json,hashlib,subprocess,shutil
from pathlib import Path
H=Path(__file__).resolve().parents[1]
def write(p,x): p.write_text(json.dumps(x,indent=2)+'\n')
sources={
'goal.md':'work/orchestration/goals/fusion-audit-remediation/goal.md',
'learnings.md':'work/orchestration/goals/fusion-audit-remediation/learnings.md',
'goal-trail.md':'work/orchestration/goals/fusion-audit-remediation/trail.md',
'integration_return.json':'work/orchestration/goals/fusion-audit-remediation/evidence/T-025_pin/integration_return.json',
'WI-051-audit.md':'work/active/WI-051_mfe-model-owned-major-radius/audit.md',
'WI-051-audit-report.md':'work/analysis/20260912-003541_audit_WI-051.md',
'consumer-audit.md':'.project/active/mfe-major-radius-study-package/audit.md',
'consumer-handoff.md':'work/active/WI-051_mfe-model-owned-major-radius/implementation/consumer-handoff.md',
'ANNEX.md':'exploration/stellarator_e2e/studies/ANNEX.md',
'STUDY_POLICY.md':'modeling_project/STUDY_POLICY.md',
'runbook.md':'.claude/skills/run-study/runbook.md',
'record-template.md':'.claude/skills/run-study/record-template.md',
'manifest.json':'exploration/stellarator_e2e/studies/manifest.json',
'oracle_entry.py':'exploration/stellarator_e2e/studies/oracle_entry.py',
'verify_stellaris.py':'exploration/stellarator_e2e/verify_stellaris.py',
'study_route.py':'exploration/stellarator_e2e/studies/study_route.py',
'model_contract.json':'exploration/stellarator_e2e/generated/contracts/model_contract.json',
'package_contract.json':'exploration/stellarator_e2e/generated/contracts/package_contract.json',
'pipeline.yaml':'exploration/stellarator_e2e/generated/pipelines/pipeline.yaml',
}
for name in ['frozen-results.json','frozen-inventory.json','frozen-checks.json','frozen-source-meaning.md','expectations.json']:
 sources[name]='work/active/WI-051_mfe-model-owned-major-radius/prototype/'+name
for name in ['results.json','checks.json','standalone.json','schema-refusals.json','numerical-report.md']:
 sources['WI-051-'+name]='work/active/WI-051_mfe-model-owned-major-radius/implementation/acceptance-attempt-2/'+name
rows=[]
for name,source in sources.items():
 p=Path(source); assert 'knowledge/holdout' not in str(p.resolve())
 data=p.read_bytes();(H/'context'/name).write_bytes(data)
 rows.append({'path':'context/'+name,'source_path':source,'source_commit':subprocess.check_output(['git','log','-1','--format=%H','--',source],text=True).strip(),'sha256':hashlib.sha256(data).hexdigest(),'status':'copied retained evidence, not new execution'})
write(H/'context/provenance.json',rows)
write(H/'axes.json',{'schema_version':'study-axis-declaration/v1','groups':[{'axis':'R','note':'AGENT: engineered sensitivity of model-owned plant radius; all other inputs fixed; no external tie.','keys':[{'key':'stellarator_09__stellaris__R','provenance':'fan_out'}]}]})
text=(H/'context/record-template.md').read_text().split('\n---\n',1)[1].split('**END OF RECORD**')[0]
(H/'record.md').write_text(text)
(H/'preparation/intake.md').write_text('''# Intake and bounded plan

[OWNER-VERBATIM] "I'd like you to $run-goal to address these." The referent is `.project/reports/20260907-fusion-model-audit.md`.

[OWNER-VERBATIM] "yes ground and proceed".

[AGENT: parent/executor] T-026 tests whether ordinary plant-R variation propagates through plasma, sustainment, magnets and costs with no external radius coordination. One engineered sensitivity axis; no search, optimum or envelope claim. Scan a small neighborhood after baseline/preflight, then select approximately 5–9 points including 12.7 and 14 m. Hold every other input and fixed reference radius unchanged. Baseline is known to violate fixed-target divertor heat; the area-scaled shadow is unconstrained. Pending STEP reading supplies no new physical rule; P_sep/R is not a generic MW/m² conversion.

[AGENT: executor] Proposed preliminary oracle scan: 12.0, 12.35, 12.7, 13.0, 13.35, 13.7, 14.0 m. Final window and point list follow that scan. Inspect all 141 declared oracle channels and independently rederive all 18 verdicts for every case. Compare all 158 native scalar controls and 19 responses at baseline/R14; analytic ratios retain fixed-input assumptions. Do not rerun invalid diagnostics: copy original T-021 and WI-051 evidence, including split-radius counterexamples and all five invalid probes, and label it retained.

[AGENT: executor] Use the study-local documented direct API: strict PreparedEvaluator + CandidateBridge for the preparatory baseline, without a baseline store; then StudyRunner + PreparedListStrategy through study_route.run_points for the complete final list, including baseline, in exactly one store. Export every scalar and verdict, keep the store and evidence bodies. This makes the baseline preparation distinct from the seven ordinary lifecycle cases and avoids creating a second store. No hand-rolled execution sweep. The fresh pre-execution reviewer must assess this route against the runbook before any execution.

[INHERITED] Certificates cover bounded arithmetic/interface preservation only. The consumer certificate discloses a prior seven-file quarantine hashing violation; no full clean-room compliance is claimed. No holdout content is read or hashed here. 147 oracle input overrides remain unsupported, and 17 native scalar outputs lack independent oracle computation. Full native frozen controls cover those outputs only at baseline/R14. No finance, constraint, installed-power, source, model, package or current-consumer change is authorized. Executor owns this directory and its discovery rows only; no commit or synthesis.
''')
print('Copied',len(rows),'explicitly selected artifacts')
