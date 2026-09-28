from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parent
base=ROOT/'selector'; pkg=base/'pkg'; link=base/'probe_selector'
if not link.exists(): link.symlink_to('pkg',target_is_directory=True)
(pkg/'handwritten/probe/match_impl.py').write_text('''from probe_selector.modules.probe.match import MatchInput
PROPERTY_CALLS = 0
def run_match(inputs: MatchInput) -> tuple[float,float,float]:
    global PROPERTY_CALLS
    if inputs.enabled_in == 0.0:
        return inputs.legacy_in, 0.0, 0.0
    if inputs.enabled_in != 1.0:
        raise ValueError("mode must be zero or one")
    PROPERTY_CALLS += 1
    if inputs.property_in <= 0.0:
        raise ValueError("toy property domain")
    return inputs.property_in * 10.0, inputs.property_in * 100.0, 2.0
''')
sys.path.insert(0,str(base))
import probe_selector as p
from probe_selector.modules.probe.match import MatchModule
from probe_selector.handwritten.probe import match_impl as impl
from simkit.core.pipeline import execute_pipeline
execute_pipeline(pkg/'pipelines/pipeline.yaml', ROOT/'disabled-execution', registry=p.create_probe_selector_registry(),custom_schema_types=p.CUSTOM_SCHEMA_TYPES)
assert impl.PROPERTY_CALLS == 0
m=MatchModule()
disabled=m.run(property_in=-1.,enabled_in=0.,legacy_in=6.).data.model_dump()
active=m.run(property_in=4.,enabled_in=1.,legacy_in=6.).data.model_dump()
assert disabled=={'gross_out':6.,'state_h':0.,'pump_out':0.}
assert active=={'gross_out':40.,'state_h':400.,'pump_out':2.}
errors={}
for mode in [1.,.5]:
 try:m.run(property_in=-1.,enabled_in=mode,legacy_in=6.)
 except ValueError as e: errors[str(mode)]=str(e)
assert errors=={'1.0':'toy property domain','0.5':'mode must be zero or one'}
inputs=json.loads((pkg/'inputs/probe_params.json').read_text())
assert not any('state_h' in k or 'enthalpy' in k or 'pump_out' in k for k in inputs)
result={'disabled_full_pipeline':'passed; zero property calls','disabled_wrapper':disabled,'active_wrapper':active,'expected_rejections':errors,'entry_points':inputs,'state_outputs_are_entries':False}
(ROOT/'execution-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
