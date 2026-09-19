"""Independent read-only WI-070 candidate audit; writes only reviewer evidence."""
import hashlib,json,math,os,sys,tempfile
from pathlib import Path
ROOT=Path.cwd(); HERE=ROOT/'work/orchestration/goals/throughput-based-fuel-processing-costs/evidence/implementation-review'; E=ROOT/'work/active/WI-070_throughput-based-fuel-processing-costs/evidence'; PKG=ROOT/'exploration/stellarator_e2e/generated'
for p in (ROOT,ROOT/'exploration/stellarator_e2e/pkg',ROOT/'exploration/stellarator_e2e/studies',Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'):sys.path.insert(0,str(p))
from scripts.study import manifest as m
from tests.model_families import MFE,canonical_path
from simkit.study.bridge import CandidateBridge
import study_route,oracle_entry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks={}
for label,base,file in [('package',PKG,'package-hashes.json'),('models',ROOT,'model-hashes.json')]:
 data=json.loads((E/file).read_text())
 for name,value in data.items():
  p=base/name
  if not p.exists() and label=='models':p=canonical_path(name)
  assert sha(p)==value,(label,name)
 checks[label+'_hashes']=len(data)
for name in MFE.owned:assert canonical_path(name).read_bytes()==(MFE.twin/name).read_bytes(),name
checks['canonical_twin_count']=len(MFE.owned)
seeds=json.loads((E/'candidate-seeds.json').read_text());prior=json.loads((ROOT/'work/active/WI-069_fuel-inventory-and-startup/evidence/candidate-seeds.json').read_text())
for name,value in seeds.items():assert sha(PKG/name)==value,name
assert set(seeds)-set(prior)=={'handwritten/mfe_fuel_cycle/fuel_processing_cost_impl.py'}
assert {k for k in prior if prior[k]!=seeds[k]}=={'handwritten/mfe_facilities/facility_shipping_scope_impl.py'}
checks['seeds']=len(seeds)
fp=m.indicator_input_fingerprint(PKG);man=json.loads((ROOT/'exploration/stellarator_e2e/studies/manifest.json').read_text())
assert fp['digest']==man['fingerprints']['indicator_inputs']['digest']
checks['fingerprints']={'semantic':m.read_semantic_fingerprint(PKG),'executable':m.read_executable_fingerprint(PKG),'indicator':fp['digest']}
assert checks['fingerprints']['semantic']==man['fingerprints']['recorded_provenance']['semantic_fingerprint']
assert checks['fingerprints']['executable']==man['fingerprints']['recorded_provenance']['executable_fingerprint']
P='stellarator_09__stellaris__'; rows={}; cases={'base':{},'legacy':{'fuel_cycle__processing_enabled':False},'burn':{'fuel_cycle__burn_fraction':.037},'price':{'fuel_cycle__processing_price_multiplier':1.37},'source_false':{'fuel_cycle__processing_source_conditions':False},'breeding_undefined':{'plasma__R':12.71},'calendar':{'unplanned_fraction':.23}}
with tempfile.TemporaryDirectory(prefix='wi070-review-native-') as tmp:
 ev=study_route.prepare(PKG,Path(tmp));bridge=CandidateBridge(ev.entry_models)
 for label,changes in cases.items():
  public={P+k:v for k,v in changes.items()};row=ev.evaluate(bridge.build(public));assert row.outputs,label
  expected=oracle_entry.evaluate(public)
  for k,v in expected.items():assert math.isclose(row.outputs[k],v,rel_tol=1e-9,abs_tol=1e-18 if '__inventory__' in k else 1e-6),(label,k,row.outputs[k],v)
  rows[label]={'outputs':dict(row.outputs),'responses':dict(row.responses),'mapped':len(expected)}
  print(label,len(row.outputs),len(expected),flush=True)
g=lambda label,k:rows[label]['outputs'][P+k]
cost='fuel_cycle__processing_cost__cost';flow='fuel_cycle__processing_cost__flow_kg_s';labor='fuel_cycle__processing_cost__installation_total'
assert math.isclose(g('base',cost),22786229.4037934,abs_tol=1e-6)
assert math.isclose(g('burn',cost)/g('base',cost),(g('burn',flow)/g('base',flow))**.3,rel_tol=1e-13)
assert math.isclose(g('price',cost)/g('base',cost),1.37,rel_tol=1e-13)
assert g('calendar',cost)==g('base',cost)
assert g('source_false','fuel_cycle__processing_cost__defined_flag')==0 and g('source_false',cost)==g('base',cost)
assert g('breeding_undefined','blanket__breeding__defined_flag')==0 and g('breeding_undefined','fuel_cycle__processing_cost__defined_flag')==1
assert g('legacy',cost)==g('legacy','fuel_cycle__fuel_handling__cost')
allowed={'cas22_capital__cas22_capital','cas2x_pre_contingency__cas2x_pre_contingency','cas20_capital__cas20_capital','contingency__cost','indirect__cost','supplementary__cost','overnight_capital__overnight_capital','total_capital__total_capital','idc__cost','cas90_1cfe_calc__cas90','lcoe_calc__lcoe','lcoe_1cfe_calc__lcoe','shipping_scope__remaining_shipping_base','shipping_scope__fuel_installation_exclusion'}
changes={k for k,v in rows['base']['outputs'].items() if rows['price']['outputs'][k]!=v};assert all(k.removeprefix(P) in allowed or k.startswith(P+'fuel_cycle__processing_cost__') for k in changes),changes
assert rows['base']['responses']==rows['price']['responses']
# Reconcile from observed existing account ratios, independent of production/oracle source defaults.
D=g('base','cas2x_pre_contingency__cas2x_pre_contingency');c=g('base','contingency__cost')/D;k=g('base','indirect__cost')/g('base','cas20_capital__cas20_capital');d=g('base',cost)-g('legacy',cost);L=g('base',labor)
ds=.015*(1+c)*(d-L)+.01*(1+c)*d+.015*(1+k)*(1+c)*d
assert math.isclose(g('base','supplementary__cost')-g('legacy','supplementary__cost'),ds,abs_tol=2e-6)
assert math.isclose(g('base','total_capital__total_capital')-g('legacy','total_capital__total_capital'),(1+k)*(1+c)*d+ds,abs_tol=2e-5)
checks.update(cases=len(rows),mapped_comparisons=sum(r['mapped'] for r in rows.values()),unchanged_price_outputs=len(rows['base']['outputs'])-len(changes),price_changed_channels=sorted(changes),account_delta={'c':c,'k':k,'fuel':d,'supplementary':ds,'overnight':(1+k)*(1+c)*d+ds})
(HERE/'native-results.json').write_text(json.dumps(rows,indent=2,default=str)+'\n');(HERE/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2))
