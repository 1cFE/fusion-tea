"""Check namespace-only oracle port without executing a native study."""
from pathlib import Path
import hashlib,importlib,json,sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
E=Path(__file__).resolve().parent
manifest=json.loads((E/'conversion-port-manifest.json').read_text());checks=[]
for row in manifest:
 s=ROOT/row['source'];t=ROOT/row['target'];data=t.read_bytes()
 if t.suffix=='.py':compile(data,str(t),'exec')
 if t.name=='oracle_gas.py':data=data.replace(b"P='whole_plant_conversion__plant__'",b"P='component_alternatives__plant__'")
 if t.name=='verify.py':
  text=data.decode().replace("P='whole_plant_conversion__plant__'","P='component_alternatives__plant__'")
  text=text.replace("PACKAGE=HERE/'whole_plant_conversion_tea'","PACKAGE=HERE/'component_alternatives_tea'")
  text=text.replace('models/designs/whole_plant_conversion/plant.sysml','models/designs/component_alternatives/plant.sysml')
  text=text.replace('work/active/WI-098_whole-plant-conversion-comparison/evidence/native_runs','work/active/WI-096_matched-conversion-subsystems/evidence/native_runs')
  text=text.replace('try:\n    from . import oracle_gas,oracle_matched_cycle\nexcept ImportError:\n    import oracle_gas,oracle_matched_cycle','import oracle_gas,oracle_matched_cycle')
  text=text.replace('    try:\n        from . import oracle_thermal,oracle_cooling\n    except ImportError:\n        import oracle_thermal,oracle_cooling','    import oracle_thermal,oracle_cooling')
  data=text.encode()
 checks.append({'file':row['target'],'inverse_namespace_equals_source':data==s.read_bytes(),'source_unchanged':hashlib.sha256(s.read_bytes()).hexdigest()==row['source_sha256']})
 assert checks[-1]['inverse_namespace_equals_source'] and checks[-1]['source_unchanged']
old=importlib.import_module('exploration.component_alternatives.oracle_gas')
new=importlib.import_module('exploration.whole_plant_conversion.oracle_gas')
v=importlib.import_module('exploration.whole_plant_conversion.verify')
api={name:callable(getattr(v,name,None)) for name in ['evaluate','operand_bindings','comparison_catalog','absolute_tolerances']}
assert all(api.values())
point={}
for p in (ROOT/'exploration/component_alternatives/component_alternatives_tea/inputs').glob('*_params.json'):point.update(json.loads(p.read_text()))
expected=old.evaluate(point);actual=new.evaluate({k.replace(old.P,new.P):x for k,x in point.items()})
remapped={k.replace(old.P,new.P):x for k,x in expected.items()}
assert remapped==actual
receipt={'scope':'port mechanics and isolated inherited gas-oracle baseline arithmetic only; no native evaluation/new whole-plant equation','files':checks,'api':api,'gas_compared_channels':len(actual),'gas_bit_exact':True,'full_plant_verification':'pending accepted design and generated package'}
(E/'conversion-port-check.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'files':len(checks),'gas_compared_channels':len(actual),'gas_bit_exact':True,'api':api}))
