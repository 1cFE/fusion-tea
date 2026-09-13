"""Exercise unchanged reusable generated input schemas and functions independently."""
import importlib, json, math, sys
from pathlib import Path
import yaml
from simkit.evaluation.package_load import ProvisionalPackageLoader
H=Path(__file__).resolve().parent; P='stellarator_09__stellaris__'; pkg=H/'generated'
ProvisionalPackageLoader(pkg,'stellarator_tea',H/'standalone-link',strict=True).load()
pipeline=yaml.safe_load((pkg/'pipelines/pipeline.yaml').read_text())
outputs=json.loads((H/'frozen-results.json').read_text())['cases']['baseline']['native']['outputs']
inputs={f.stem:json.loads(f.read_text()) for f in (pkg/'inputs').glob('*.json')}
result={}
for suffix,area,module,klass,ratio in [('coil_length','mfe_magnet_field','coil_winding_length','Coil_Winding_Length',14/12.7),('field_calc','mfe_magnet_field','coil_set_axis_field','Coil_Set_Axis_Field',12.7/14),('stored_energy','mfe_magnet_field','coil_set_stored_energy','Coil_Set_Stored_Energy',12.7/14),('magnet_cost','mfe_magnet_cost','magnet_coil_cost','Magnet_Coil_Cost',14/12.7)]:
    schema=getattr(importlib.import_module(f'stellarator_tea.modules.{area}.{module}'),klass+'Input')
    fn=getattr(importlib.import_module(f'stellarator_tea.handwritten.{area}.{module}_impl'),'run_'+module)
    values={}
    for formal,binding in pipeline['modules'][P+suffix]['inputs'].items():
        ref=binding.split(' ',1)[1]
        if '.' in ref:
            group,key=ref.split('.',1); values[formal]=inputs[group][key]
        else: values[formal]=outputs[ref]
    assert 'R0' in schema.model_fields
    a=fn(schema(**values)); b=fn(schema(**(values|{'R0':14.0})))
    assert math.isclose(b/a,ratio,rel_tol=1e-9,abs_tol=1e-9)
    result[suffix]={'schema':schema.__name__,'inputs':values,'baseline':a,'R0_only14':b,'expected_ratio_at_other_formals_fixed':ratio,'actual_ratio':b/a}
(H/'standalone.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS four standalone R0 schemas and independent radius responses')
