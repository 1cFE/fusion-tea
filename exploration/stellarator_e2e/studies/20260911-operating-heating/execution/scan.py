import json
from pathlib import Path
from exploration.stellarator_e2e.studies import oracle_entry as oracle, study_route as route
H=Path(__file__).resolve().parents[1]; R=H/'results'
def write(p,x): p.write_text(json.dumps(x,indent=2)+'\n')
p=H/'preparation/execution-proposal.json'; proposal=json.loads(p.read_text()); proposal['case_count']=15; write(p,proposal)
e=H/'preparation/expectations.md'; t=e.read_text().replace('using all 16 proposals as the requested sample','using all 15 executed proposals as the requested sample'); t=t.replace('The coordinated candidate at density','The center was declined before execution under review F2; its construction below is preliminary evidence only. The coordinated candidate at density'); e.write_text(t)
assert json.loads((R/'preflight.json').read_text())['outcome']=='pass'
b=json.loads((R/'baseline_result.json').read_text()); demand=b['channels'][route.P+'sustain__p_aux_required']; candidate=proposal['arms'][0]['cases'][1]['point'][route.P+'p_wallplug_heat']
# Exact generated baseline demand is the pre-sweep reserve equality reference.
corrected=demand/0.5
proposal['arms'][0]['cases'][1]['point'][route.P+'p_wallplug_heat']=corrected
proposal['arms'][0]['cases'][1]['label']='installed-equality'
rows=[]
for arm in proposal['arms']:
 for case in arm['cases']:
  out=oracle.evaluate(case['point']); rows.append({'arm_id':arm['arm_id'],**case,'channels':out})
write(R/'oracle-window-scan.json',{'stage':'Formal native Step 7, after baseline and six passing preflight gates','rows':rows})
write(R/'window-freeze.json',{'case_count':15,'proposal':proposal,'reserve_equality':{'prior_candidate':candidate,'baseline_demand':demand,'baseline_source_efficiency':0.5,'chosen_installed':corrected,'changed_before_sweep':candidate!=corrected,'oracle_demand':rows[1]['channels'][route.P+'sustain__p_aux_required'],'note':'Equality is generated-baseline referenced; oracle float may differ. Exact predicate verification must still pass unchanged.'},'metadata_corrections':'Parent authorized case_count 16 to 15 and expectations sample count 16 to 15 after baseline/preflight, before formal scan and sweep; original proposal/probes/review preserved. Center explicitly marked declined.','window_provenance':'engineered','decision':'Retain all 15 scheduled cases. Fresh scan covers each proposed point and bracket. No inherited engineering envelope or feasible boundary is asserted.'})
write(p,proposal)
print(json.dumps({'baseline_lcoe':b['channels'][route.P+'lcoe_calc__lcoe'],'reserve':json.loads((R/'window-freeze.json').read_text())['reserve_equality'],'scanned':len(rows)},indent=2))
