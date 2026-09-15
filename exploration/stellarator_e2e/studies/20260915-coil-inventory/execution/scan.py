"""Pre-execution oracle scan with independent predicate derivation, no native point execution."""
import json, sys
from pathlib import Path
H=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(H.parent))
import oracle_entry as oe
from exploration.stellarator_e2e.studies import study_route as route
from scripts.study.verify import derive_verdict, package_input_values
catalog=route._catalog_by_constraint_id(route.PACKAGE_DIR)
params=package_input_values(route.PACKAGE_DIR); bindings=oe.operand_bindings()
props=json.loads((H/'preparation/proposals.json').read_text())
result={'scope':'oracle only; current candidate, before native study execution','arms':{},'errors':[]}
for arm,rows in props.items():
    out=[]
    for row in rows:
        ch=oe.evaluate(row['point'])
        verdicts={entry['source_local_identity']:('satisfied' if derive_verdict(cid,entry,bindings,row['point'],params,ch)[0] else 'violated') for cid,entry in catalog.items()}
        out.append(row|{'channels':ch,'verdicts':verdicts,'full_satisfied':all(v=='satisfied' for v in verdicts.values())})
    result['arms'][arm]=out
    print(arm,len(out),'oracle18-feasible',sum(r['full_satisfied'] for r in out),flush=True)
(H/'results/oracle-scan.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
