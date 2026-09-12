"""Run the unmodified native verifier with an explicit stratified sample request."""
import json
from pathlib import Path
from scripts.study import verify
H=Path(__file__).resolve().parents[1];R=H/'results'
args=['--package','exploration/stellarator_e2e/generated','--manifest','exploration/stellarator_e2e/studies/manifest.json','--identity',str(R/'package_identity.json'),'--store',str(R/'store'/f'{H.name}.db'),'--sample-size','128','--out',str(R/'verification_summary.json')]
(H/'execution/verification-command.json').write_text(json.dumps(['scripts/study/verify.py',*args],indent=2)+'\n')
if __name__=='__main__':raise SystemExit(verify.main(args))
