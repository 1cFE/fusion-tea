import json,os,subprocess,sys
from pathlib import Path
root=Path.cwd();pkg=root/'exploration/stellarator_e2e/generated'
a=json.loads((pkg/'contracts/model_contract.json').read_text()); b=json.loads((pkg/'contracts/package_contract.json').read_text())
rev=subprocess.check_output(['git','-C',os.environ['STOP_PARSER_TEAX_ROOT'],'rev-parse','HEAD'],text=True).strip()
cmd=[sys.executable,'scripts/integrate.py','--audited-work','work/active/WI-064_current-driven-magnet-inventory-sizing@a8589d6b','--models-root','exploration/stellarator_e2e/models','--package',str(pkg),'--manifest','exploration/stellarator_e2e/studies/manifest.json','--groups','tests/study/data/axes.known_answers.json','--census-file','tests/models/data/mfe_census.json','--expected-semantic-fingerprint',a['semantic_fingerprint'],'--expected-executable-fingerprint',b['executable_fingerprint'],'--expected-teax-revision',rev,'--route-sys-path','exploration/stellarator_e2e/studies','--route-module','study_route','--route-callable','execute_baseline','--out-dir','work/orchestration/goals/joint-magnet-sizing-feasibility/evidence/T-003_integration']
raise SystemExit(subprocess.call(cmd))
