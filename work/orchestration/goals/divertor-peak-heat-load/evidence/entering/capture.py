"""Capture entering native cases for exact regression, before WI-065 mutation."""
import json
import os
import sys
from pathlib import Path
ROOT=Path.cwd()
H=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'exploration/stellarator_e2e/pkg'),str(ROOT/'exploration/stellarator_e2e/studies'),str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit')]
from simkit.study.bridge import CandidateBridge
import study_route
import oracle_entry
rows=json.loads((ROOT/'exploration/stellarator_e2e/studies/20260915-joint-magnet-sizing/preparation/unique-proposals.json').read_text())
names=['reference','r-12.7-1.35-1.62e+07','r-13.1-1.45-1.54e+07']
selected=[row for name in names for row in rows if row['proposal_id']==name]
assert len(selected)==3
P=study_route.P
selected += [{'proposal_id':'current-sized-reference','point':selected[0]['point']|{P+'magnet__winding_pack__sizing_mode':1.,P+'magnet__winding_pack__inventory_multiplier':1.01}}, {'proposal_id':'allocated-current-sized-reference','point':selected[0]['point']|{P+'magnet__winding_pack__sizing_mode':1.,P+'magnet__winding_pack__inventory_multiplier':1.01,P+'magnet__coil__coil_t':.6,P+'magnet__casing__interior_y':.6}}]
evaluator=study_route.prepare(ROOT/'exploration/stellarator_e2e/generated',H/'_native_work')
bridge=CandidateBridge(evaluator.entry_models)
results=[]
for row in selected:
    result=evaluator.evaluate(bridge.build(row['point']))
    assert result.outputs
    expected=oracle_entry.evaluate(row['point'])
    results.append(row|{'outputs':dict(result.outputs),'responses':dict(result.responses),'oracle_outputs':expected})
(H/'native-cases.json').write_text(json.dumps({'entering_commit':'f76ec031951d7918fbfec2de23d298830941c121','cases':results},indent=2)+'\n')
print([(r['proposal_id'],r['outputs'][P+'divertor__divheat__q_target_peak']) for r in results])
