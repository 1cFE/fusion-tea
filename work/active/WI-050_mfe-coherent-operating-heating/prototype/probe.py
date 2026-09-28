"""Disposable native generation/execution probe; run .codex-test/run python <this>."""
import sys,os,json,shutil,tempfile,difflib,math
from collections.abc import Mapping
from pathlib import Path
ROOT=Path.cwd(); HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT)); sys.path.insert(0,str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
from tests.model_families import MFE,materialize_canonical_subset
from sysml_codegen.cli import GenerationConfig,run_codegen
from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader
from simkit.study.bridge import CandidateBridge
TMP=Path(tempfile.mkdtemp(prefix='wi050-design-')); (HERE/'scratch.txt').write_text(str(TMP)+'\n')
models=materialize_canonical_subset(MFE,TMP/'models'); original={f:f.read_text() for f in models.rglob('*.sysml')}
f=models/'analyses/mfe_heating_chain.sysml'; s=f.read_text(); f.write_text(s.rsplit('}',1)[0]+(HERE/'operating.sysml').read_text()+'}\n')
f=models/'designs/generic_mfe/mfe_plant.sysml'; s=f.read_text()
marker='        // WI-045: the reactor\'s source heat'
block='''        // Generic legacy/direct behavior defaults to installed coupled capacity.
        // A sustained concept overrides this exposed demand with its producer.
        attribute p_operating_coupled_heat : Real default heat.p_coupled;
        calc operating_heat : 'Operating Heating Power' {
            in p_required_in = p_operating_coupled_heat;
            in eta_source_in = eta_source_heat;
            in eta_couple_in = eta_couple_heat;
        }
        assert constraint heating_efficiency_ok : 'Heating Efficiency Domain' {
            in eta_source_in = eta_source_heat;
            in eta_couple_in = eta_couple_heat;
        }

'''
s=s.replace(marker,block+marker).replace('in p_input_in = heat.p_coupled;','in p_input_in = operating_heat.p_coupled;').replace('in p_wallplug_in = heat.p_wallplug_total;','in p_wallplug_in = operating_heat.p_wallplug;').replace('in p_coupled_in = heat.p_coupled;','in p_coupled_in = operating_heat.p_coupled;')
s=s.replace('in p_aux_required_in = sustain.p_aux_required;\n            in p_rad_core_in','in p_aux_required_in = sustain.p_aux_required;\n            in p_installed_coupled_in = heat.p_coupled;\n            in p_rad_core_in')
f.write_text(s)
f=models/'analyses/mfe_divertor_heat.sysml'; s=f.read_text().replace('in attribute p_aux_required_in : Real;','in attribute p_aux_required_in : Real;\n        in attribute p_installed_coupled_in : Real;').replace('= p_aux_required_in - p_coupled_in;','= p_aux_required_in - p_installed_coupled_in;'); f.write_text(s)
f=models/'designs/stellarator_09/stellarator_plant.sysml'; s=f.read_text().replace('        :>> p_wallplug_heat = 100.0 {','        :>> p_operating_coupled_heat = sustain.p_aux_required;\n\n        :>> p_wallplug_heat = 100.0 {'); f.write_text(s)
(HERE/'proposed.patch').write_text(''.join(''.join(difflib.unified_diff(original[f].splitlines(True),f.read_text().splitlines(True),fromfile=str(f.relative_to(models)),tofile=str(f.relative_to(models)))) for f in original if original[f]!=f.read_text()))
# Preserve existing normative manual implementations in copied package only.
pkg=TMP/'generated'; shutil.copytree(ROOT/'exploration/stellarator_e2e/generated',pkg)
assert run_codegen(GenerationConfig(models_path=models,output_path=pkg,package_name='stellarator_tea',overwrite=True,preserve_handwritten=True))
loader=ProvisionalPackageLoader(pkg,'stellarator_tea',TMP/'link',strict=True)
ev=PreparedEvaluator(loader,pkg/'pipelines/pipeline.yaml',expects_constraint_report=True); bridge=CandidateBridge(ev.entry_models)
P='stellarator_09__stellaris__'
results={}
for name,change in [('baseline',{}),('reserve',{P+'p_wallplug_heat':120.0}),('demand',{P+'f_alpha_fast':0.96}),('efficiency',{P+'eta_couple_heat':0.8}),('availability',{P+'unplanned_fraction':0.10}),('negative_efficiency',{P+'eta_source_heat':-0.5}),('zero_efficiency',{P+'eta_source_heat':0.0}),('overunit_efficiency',{P+'eta_source_heat':1.01})]:
    try:
        r=ev.evaluate(bridge.build(change))
        results[name]={'outputs':dict(r.outputs),'responses':dict(r.responses),'report':r.report}
        print(name, r.outputs.get(P+'operating_heat__p_coupled'),r.outputs.get(P+'pb__p_net'), flush=True)
    except Exception as e:
        results[name]={'error':type(e).__name__,'message':str(e)}; print(name,results[name],flush=True)
(HERE/'results.json').write_text(json.dumps(results,indent=2,default=lambda v:dict(v) if isinstance(v,Mapping) else str(v))+'\n')
print('SCRATCH',TMP)
