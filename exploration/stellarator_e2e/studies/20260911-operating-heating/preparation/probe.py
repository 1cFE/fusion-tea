"""Pre-critique oracle-only exploration; not formal runbook Step 7 or TEAx evidence."""
import json
from pathlib import Path
from exploration.stellarator_e2e.studies import oracle_entry as o
from exploration.stellarator_e2e.studies import study_route as r
P=r.P
baseline=json.loads(r.MANIFEST_PATH.read_text())['baseline']['point']
rows=[]
for axis, values in [('p_wallplug_heat',[80, 98.15920157585356,100,110,120]), ('f_alpha_fast',[.94,.95,.96,1.0]), ('T_i0',[12,13,14,14.63,15,16,17,18,20,22,24])]:
    for value in values:
        point={**baseline,P+axis:value}
        try:
            out=o.evaluate(point)
            rows.append({'axis':axis,'value':value,'point':point,'channels':out})
        except Exception as exc:
            rows.append({'axis':axis,'value':value,'point':point,'error':type(exc).__name__+': '+str(exc)})
path=Path(__file__).parent/'preliminary-oracle-probe.json'
path.write_text(json.dumps({'scope':'Pre-critique candidate exploration only. Formal Step 7 scan remains after baseline and preflight. No TEAx execution.','rows':rows},indent=2)+'\n')
for x in rows:
    c=x.get('channels',{})
    print(x['axis'],x['value'],{k:c.get(P+k) for k in ['sustain__p_aux_required','pb__p_net','divheat__q_target_peak','lcoe_calc__lcoe']},x.get('error',''))
