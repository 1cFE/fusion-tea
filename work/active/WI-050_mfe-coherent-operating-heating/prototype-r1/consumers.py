"""Actual indicator parsing and verifier rederivation; no tooling patches."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from scripts.study import indicators, verify
h=Path(__file__).resolve().parent
scratch=Path((h/'scratch.txt').read_text().strip())
contract=json.loads((scratch/'generated/contracts/model_contract.json').read_text())
entries=contract['constraint_catalog']['concrete_entries']
assert len(entries)==18
assert len(contract['parameters'])==247
assert not any('p_operating_coupled_heat' in str(x) for x in contract['parameters'])
parsed={e['constraint_id']: indicators.predicate_operands(e) for e in entries}
assert sum(len(verify.feature_refs(json.loads(e['predicate_ir']))) for e in entries)==28
new={e['source_local_identity']:e for e in entries if e['source_local_identity'].startswith('heating_')}
assert len(new)==4
P='stellarator_09__stellaris__'
bindings={e['constraint_id']:{'efficiency':{'kind':'input','key':P+('eta_source_heat' if 'source' in name else 'eta_couple_heat')}} for name,e in new.items()}
result={'constraint_count':len(entries),'parameter_count':len(contract['parameters']),'feature_occurrences':28,'all_indicator_operands':parsed,'new_bindings':bindings,'cases':{}}
native=json.loads((h/'results.json').read_text())
for stage in ['source','couple']:
 for label,value in [('valid_one',1.0),('negative',-0.5),('zero',0.0),('over_one',1.01)]:
  inputs={P+'eta_source_heat':0.5,P+'eta_couple_heat':0.75};inputs[P+f'eta_{stage}_heat']=value
  verdicts={}
  for name,e in new.items():
   actual,count=verify.derive_verdict(e['constraint_id'],e,bindings,{},inputs,{})
   assert count==1
   expected=(value>0 if 'positive' in name else value<=1) if stage in name else True
   assert actual==expected,(name,value,actual)
   verdicts[name]={'satisfied':actual,'operands_resolved':count}
  result['cases'][stage+'_'+label]=verdicts
# Compare native verdicts with independent input-only verifier for all four entries.
for case,inputs in [('baseline',{P+'eta_source_heat':.5,P+'eta_couple_heat':1.}),('negative_efficiency',{P+'eta_source_heat':-.5,P+'eta_couple_heat':1.}),('overunit_efficiency',{P+'eta_source_heat':1.01,P+'eta_couple_heat':1.})]:
 for name,e in new.items():
  actual,count=verify.derive_verdict(e['constraint_id'],e,bindings,{},inputs,{})
  assert native[case]['responses'][e['constraint_id']]==('satisfied' if actual else 'violated')
(h/'consumer-results.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: actual indicator parser accepts all 18 entries; verifier resolves all four new entries across both efficiency boundaries; 28 feature occurrences, 247 parameters, no demand entry')
