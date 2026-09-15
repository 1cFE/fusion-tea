"""Invoke native fixed-point integration for a separately audited, committed candidate."""
import argparse,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--audited-revision',required=True);p.add_argument('--out-dir',required=True);a=p.parse_args()
root=Path('exploration/stellarator_e2e')
semantic=json.loads((root/'generated/contracts/model_contract.json').read_text())['semantic_fingerprint']
executable=json.loads((root/'generated/contracts/package_contract.json').read_text())['executable_fingerprint']
# Expected sealed checkout revision inherited from entering integration evidence.
teax='8d877460ac4f6f264561d916e40c1708adb13397'
args=[sys.executable,'scripts/integrate.py','--audited-work',f'work/active/WI-061_winding-pack-casing-fit@{a.audited_revision}','--models-root',str(root/'models'),'--package',str(root/'pkg/stellarator_tea'),'--manifest',str(root/'studies/manifest.json'),'--groups','tests/study/data/axes.known_answers.json','--census-file','tests/models/data/mfe_census.json','--expected-semantic-fingerprint',semantic,'--expected-executable-fingerprint',executable,'--expected-teax-revision',teax,'--route-sys-path',str(root/'studies'),'--route-module','study_route','--route-callable','execute_baseline','--out-dir',a.out_dir]
raise SystemExit(subprocess.call(args))
