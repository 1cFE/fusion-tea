"""Pre-critique signed-demand representability probe, using public plasma controls."""
import json
from pathlib import Path
from exploration.stellarator_e2e.studies import oracle_entry as o
from exploration.stellarator_e2e.studies import study_route as r
P=r.P
base={**json.loads(r.MANIFEST_PATH.read_text())['baseline']['point'],P+'T_i0':17.0}
a=o.evaluate({**base,P+'f_alpha_fast':.95})
b=o.evaluate({**base,P+'f_alpha_fast':1.0})
D=P+'sustain__p_aux_required'
root=.95+.05*a[D]/(a[D]-b[D])
rows=[]
for f in [.95,root-1e-5,root,root+1e-5,1.0]:
    point={**base,P+'f_alpha_fast':f}
    out=o.evaluate(point)
    rows.append({'f_alpha_fast':f,'point':point,'channels':out})
    print(f,out[D],flush=True)
Path(__file__).with_name('preliminary-signed-probe.json').write_text(json.dumps({'scope':'Pre-critique representability probe only; affine interpolation of retained fraction, not an evaluator solve or formal Step 7. Near zero must not be called exact zero unless native arithmetic is exactly zero.','root_fraction':root,'rows':rows},indent=2)+'\n')
