"""Check the predeclared ABI/scalar/predicate delta against the entering package."""
import json
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
P='stellarator_09__stellaris__'
enter=json.loads((HERE/'entering.json').read_text())
current=json.loads((HERE/'baseline.json').read_text())
old_contract=json.loads((HERE/'entering-model_contract.json').read_text())
new_contract=json.loads((ROOT/'exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())
keys=lambda c:{x['qualified_name'] for x in c['parameters']}
assert keys(old_contract)-keys(new_contract)=={P+'blanket__tbr'}
assert not keys(new_contract)-keys(old_contract)
assert (len(keys(old_contract)),len(keys(new_contract)))==(313,312)
old,new=enter['outputs'],current['outputs']
assert len(old)==242 and len(new)==261
assert not old.keys()-new.keys()
changed={k for k in old if not math.isclose(old[k],new[k],rel_tol=1e-12,abs_tol=1e-12)}
assert changed=={P+'fuel_cycle__fuel__tbr_margin'},changed
before,after=enter['responses'],current['responses']
assert before.keys()==after.keys()
changed_responses={k for k in before if before[k]!=after[k]}
assert changed_responses=={P+'tbr_ok__2cd198f674d413e4'},changed_responses
assert before[P+'tbr_ok__2cd198f674d413e4']=='satisfied'
assert after[P+'tbr_ok__2cd198f674d413e4']=='violated'
assert current['oracle_mapped_count']==245
old_ids={e['constraint_id'] for e in old_contract['constraint_catalog']['concrete_entries']}
new_ids={e['constraint_id'] for e in new_contract['constraint_catalog']['concrete_entries']}
assert old_ids==new_ids and len(new_ids)==20
report=dict(status='PASS',parameters_before=313,parameters_after=312,numeric_before=242,numeric_after=261,oracle_mapped=245,unchanged_predicate_ids=20,changed_old_scalars=sorted(changed),changed_responses=sorted(changed_responses),new_channels=sorted(new.keys()-old.keys()))
(HERE/'baseline-delta.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
