"""Oracle-only neighborhood scan; no native sweep or physical bounds."""
import json,math
from pathlib import Path
from exploration.stellarator_e2e.studies import oracle_entry as oracle,study_route as route
from scripts.study import verify
H=Path(__file__).resolve().parents[1];R=H/'results'
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
assert read(R/'preflight.json')['outcome']=='pass'
cat=read(R/'constraint-catalog.json');baseline=read(R/'package-inputs.json');rows=[]
for radius in [12.0,12.35,12.7,13.0,13.35,13.7,14.0]:
 point={route.P+'R':radius};channels=oracle.evaluate(point)
 assert len(channels)==141 and all(math.isfinite(v) for v in channels.values())
 verdicts={cid:('satisfied' if verify.derive_verdict(cid,e,oracle.operand_bindings(),point,baseline,channels)[0] else 'violated') for cid,e in cat.items()}
 rows.append({'R':radius,'point':point,'channels':channels,'verdicts':verdicts})
write(R/'oracle-window-scan.json',{'kind':'new independent-oracle execution only; not native study cases','rows':rows})
write(H/'preparation/window-freeze.json',{'provenance':'engineered','R_m':[r['R'] for r in rows],'decision':'All seven scan points have finite declared channels and individually derived verdicts. Retain this modest neighborhood including required controls to expose local coherent radius response. No feasible anchor is assumed or envelope sought; violations are expected and retained. Edges are not physical fences and are not claimed caught.','held_fixed':'Every public input except plant R, including reference radii and installed heating.','validity_mask':'R > a + 2.25 = 3.55 m at fixed a=1.3; all selected points pass. This geometric exclusion alone does not guarantee execution or physical validity.'})
print(json.dumps([{'R':r['R'],'lcoe':r['channels'][route.P+'lcoe_calc__lcoe'],'violations':[cat[c]['source_local_identity'] for c,s in r['verdicts'].items() if s=='violated']} for r in rows],indent=2))
