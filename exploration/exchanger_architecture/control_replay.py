"""Exact calculated/supplied N control replay, separate from main study execution."""
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from exploration.aries_integrated.studies import study_route as route

R=ROOT/'exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture'
P='aries_integrated_plant__'
original=json.loads((R/'baseline-control.json').read_text())
base=original['inputs']
fusion=1835.4512830147435
assert base[P+'source__producer_mode']==1
assert base[P+'pressure_loss__loss_fraction']==.045
assert original['outputs'][P+'source__evaluate__selected_power']==fusion
supplied=base|{P+'source__producer_mode':0.,P+'source__reference_fusion_mw':fusion}
target=R/'preparation/control-replay.json'
if target.exists():
    raise ValueError('control receipt exists; preserve it')
cases,db=route.run_points('exchanger-architecture-N-controls',[base,supplied],R/'preparation/control-native')
by_mode={c.inputs[P+'source__producer_mode']:c for c in cases}
calculated,source=by_mode[1],by_mode[0]
assert all(c.state=='completed' for c in cases)
assert dict(calculated.outputs)==original['outputs']
assert dict(calculated.verdicts)==original['verdicts']
differences={k:{'calculated':v,'supplied':source.outputs[k]} for k,v in calculated.outputs.items() if v!=source.outputs[k]}
expected={P+'source__evaluate__selected_mode',P+'plant_ledger__evaluate__net_result_producer_mode'}
assert set(differences)==expected,differences
assert calculated.verdicts==source.verdicts
assert source.outputs[P+'source__evaluate__selected_power']==fusion
rows=[{'source_mode':c.inputs[P+'source__producer_mode'],'candidate_id':c.candidate_id,'inputs':dict(c.inputs),'outputs':dict(c.outputs),'verdicts':dict(c.verdicts),'executable_fingerprint':c.executable_fingerprint} for c in cases]
receipt={'outcome':'pass','store':str(db.relative_to(ROOT)),'exact_original_channels':len(calculated.outputs),'exact_original_verdicts':len(calculated.verdicts),'downstream_equal_channels':len(calculated.outputs)-len(differences),'only_changed_outputs':differences,'baseline_pressure_loss':.045,'exact_source_power_MW':fusion,'cases':rows}
with target.open('x') as stream:
    json.dump(receipt,stream,indent=2)
    stream.write('\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='cases'}))
