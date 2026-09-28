"""Invoke the native seam against the reviewed, committed WI-068 package."""
from pathlib import Path
import json,os,subprocess,sys
ROOT=Path.cwd(); package=ROOT/'exploration/stellarator_e2e/pkg/stellarator_tea'
contract=json.loads((package/'contracts/package_contract.json').read_text())
model=json.loads((package/'contracts/model_contract.json').read_text())
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
teax=subprocess.check_output(['git','-C',os.environ['STOP_PARSER_TEAX_ROOT'],'rev-parse','HEAD'],text=True).strip()
manifest=json.loads((ROOT/'exploration/stellarator_e2e/studies/manifest.json').read_text())
fp=manifest['fingerprints']['recorded_provenance']
assert fp['executable_fingerprint']==contract['executable_fingerprint']
command=[sys.executable,'scripts/integrate.py','--audited-work','work/active/WI-068_layout-based-facilities@'+head,'--models-root','exploration/stellarator_e2e/models','--package',str(package),'--manifest','exploration/stellarator_e2e/studies/manifest.json','--groups','tests/study/data/axes.known_answers.json','--census-file','tests/models/data/mfe_census.json','--expected-semantic-fingerprint',fp['semantic_fingerprint'],'--expected-executable-fingerprint',fp['executable_fingerprint'],'--expected-teax-revision',teax,'--route-sys-path','exploration/stellarator_e2e/studies','--route-module','study_route','--route-callable','execute_baseline','--out-dir','work/orchestration/goals/layout-based-facilities/evidence/integration']
raise SystemExit(subprocess.run(command,cwd=ROOT).returncode)
