"""Native boundary/legacy-default fixtures, deliberately not complete plants."""
import os,sys,json,tempfile,shutil,math
from collections.abc import Mapping
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=Path.cwd(); TMP=Path(tempfile.mkdtemp(prefix='wi050-boundaries-'))
sys.path.insert(0,str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
from sysml_codegen.cli import GenerationConfig,run_codegen
from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader
from simkit.study.bridge import CandidateBridge
src=TMP/'models'; src.mkdir(); full=Path((HERE/'scratch.txt').read_text().strip())/'models'
shutil.copy(full/'analyses/mfe_heating_chain.sysml',src/'mfe_heating_chain.sysml')
fixture='''package boundary_fixture {
 private import ScalarValues::*;
 private import mfe_heating_chain::*;
 constraint def Upper { doc /* Fixture sustainment ceiling. */ in attribute demand : Real; in attribute capacity : Real; demand <= capacity }
 constraint def Lower { doc /* Fixture burn hold. */ in attribute demand : Real; demand >= 0.0 }
 part test {
  attribute demand : Real = 12.0;
  attribute installed : Real = 100.0;
  attribute source_eta : Real = 0.5;
  attribute couple_eta : Real = 0.75;
  calc heat : 'Heating Power Chain' { in p_wallplug = installed; in eta_source = source_eta; in eta_couple = couple_eta; }
  calc operating_heat : 'Operating Heating Power' { in p_required_in = demand; in eta_source_in = source_eta; in eta_couple_in = couple_eta; }
  assert constraint upper : Upper { in demand = operating_heat.p_coupled; in capacity = heat.p_coupled; }
  assert constraint lower : Lower { in demand = operating_heat.p_coupled; }
  assert constraint source_positive : 'Heating Efficiency Positive' { in efficiency = source_eta; }
  assert constraint source_upper : 'Heating Efficiency Upper' { in efficiency = source_eta; }
  assert constraint couple_positive : 'Heating Efficiency Positive' { in efficiency = couple_eta; }
  assert constraint couple_upper : 'Heating Efficiency Upper' { in efficiency = couple_eta; }
 }
 part def Legacy {
  attribute installed : Real default 0.0;
  attribute delivered_direct : Real default 50.0;
  attribute coupled_direct : Real default 30.0;
  attribute source_eta : Real default 0.5;
  attribute couple_eta : Real default 0.75;
  calc heat : 'Heating Power Chain' { in p_wallplug = installed; in p_delivered_direct = delivered_direct; in p_coupled_direct = coupled_direct; in eta_source = source_eta; in eta_couple = couple_eta; }
  attribute demand : Real default heat.p_coupled;
  calc operating_heat : 'Operating Heating Power' { in p_required_in = demand; in eta_source_in = source_eta; in eta_couple_in = couple_eta; }
 }
 part legacy : Legacy;
 part mixed : Legacy { :>> installed = 100.0; }
 part allzero : Legacy { :>> installed = 0.0; :>> delivered_direct = 0.0; :>> coupled_direct = 0.0; :>> source_eta = 1.0; :>> couple_eta = 1.0; }
}
'''
(HERE/'boundary_fixture.sysml').write_text(fixture); (src/'fixture.sysml').write_text(fixture)
pkg=TMP/'generated'; assert run_codegen(GenerationConfig(models_path=src,output_path=pkg,package_name='boundary_heat',overwrite=True))
ev=PreparedEvaluator(ProvisionalPackageLoader(pkg,'boundary_heat',TMP/'link',strict=True),pkg/'pipelines/pipeline.yaml',expects_constraint_report=True); bridge=CandidateBridge(ev.entry_models)
p='boundary_fixture__test__'; out={}
for name,d in [('positive',12.0),('equality',37.5),('zero',0.0),('insufficient',38.0),('negative',-1.0)]:
 r=ev.evaluate(bridge.build({p+'demand':d})); expected_upper='violated' if name=='insufficient' else 'satisfied'; expected_lower='violated' if name=='negative' else 'satisfied'
 assert any('__upper__' in k and v==expected_upper for k,v in r.responses.items())
 assert any('__lower__' in k and v==expected_lower for k,v in r.responses.items())
 out[name]={'outputs':dict(r.outputs),'responses':dict(r.responses),'report':r.report}
 for field,expected in [('p_coupled',d),('p_delivered',d/.75),('p_wallplug',d/.75/.5)]: assert math.isclose(r.outputs[p+'operating_heat__'+field],expected,abs_tol=1e-9,rel_tol=1e-9)
 assert r.outputs['boundary_fixture__legacy__heat__p_wallplug_total']==r.outputs['boundary_fixture__legacy__operating_heat__p_wallplug']==80.0
 assert r.outputs['boundary_fixture__legacy__heat__p_delivered']==50.0
 assert r.outputs['boundary_fixture__legacy__operating_heat__p_delivered']==40.0
# Prove mixed and all-zero default paths using native emitted channels.
for name,wall,delivered,coupled,se,ce in [('legacy',0.,50.,30.,.5,.75),('mixed',100.,50.,30.,.5,.75),('allzero',0.,0.,0.,1.,1.)]:
 q='boundary_fixture__'+name+'__';outputs=out['positive']['outputs'];d=wall*se*ce+coupled
 for field,expected in [('p_coupled',d),('p_delivered',d/ce),('p_wallplug',wall+coupled/(se*ce))]: assert math.isclose(outputs[q+'operating_heat__'+field],expected,abs_tol=1e-9)
 assert outputs[q+'heat__p_delivered']==wall*se+delivered
for stage in ['source','couple']:
 for label,value in [('valid_one',1.),('negative',-.5),('zero',0.),('over_one',1.01)]:
  name=stage+'_'+label
  try:
   r=ev.evaluate(bridge.build({p+stage+'_eta':value}))
   assert value!=0
   out[name]={'outputs':dict(r.outputs),'responses':dict(r.responses),'report':r.report}
   for bound in ['positive','upper']:
    expected='satisfied' if (value>0 if bound=='positive' else value<=1) else 'violated'
    assert any('__'+stage+'_'+bound+'__' in k and v==expected for k,v in r.responses.items())
  except Exception as e:
   if value!=0: raise
   assert type(e).__name__=='EvaluationFailed'
   out[name]={'error':type(e).__name__,'message':str(e)}
print(json.dumps(out,indent=2,default=lambda v:dict(v) if isinstance(v,Mapping) else str(v))); (HERE/'boundary-results.json').write_text(json.dumps(out,indent=2,default=lambda v:dict(v) if isinstance(v,Mapping) else str(v))+'\n')
