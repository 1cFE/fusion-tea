"""Supplementary pre-critique oracle-only density candidate probe."""
import json
from pathlib import Path
from exploration.stellarator_e2e.studies import oracle_entry as o
from exploration.stellarator_e2e.studies import study_route as r
P=r.P
baseline=json.loads(r.MANIFEST_PATH.read_text())['baseline']['point']
rows=[]
for factor in [.5,.7,.8,.9,1,1.1,1.2,1.3,1.4,1.5]:
    point={**baseline,P+'n_e0':5.06e20*factor}
    try:
        out=o.evaluate(point)
        rows.append({'factor':factor,'point':point,'channels':out})
        print(factor, out[P+'sustain__p_aux_required'],flush=True)
    except Exception as exc:
        rows.append({'factor':factor,'point':point,'error':type(exc).__name__+': '+str(exc)})
Path(__file__).with_name('preliminary-density-probe.json').write_text(json.dumps({'scope':'Pre-critique probe, not formal Step 7. No TEAx execution.','rows':rows},indent=2)+'\n')
