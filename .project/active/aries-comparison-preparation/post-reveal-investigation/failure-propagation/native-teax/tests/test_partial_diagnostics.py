import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pytest
from simkit.config.pipeline_schema import ChannelSource, PipelineChannelBinding as Binding, PipelineModuleSpec as Spec, PipelineSpecification
from simkit.core.base import ModuleResult
from simkit.core.pipeline_executor import SerialPipelineExecutor, PipelineExecutionContext
from simkit.core.pipeline_graph import PipelineDagBuilder
from simkit.core.pipeline_registry import ModuleDescriptor, PipelineModuleRegistry
from simkit.evaluation.diagnostics import project_diagnostic


def setup(nodes):
    registry=PipelineModuleRegistry();specs={'entry':Spec(key='entry',module_type='EntryPoint')};exits={};calls=[]
    for name,parents,fn,outputs in nodes:
        class Module:
            def __init__(self, name=name, fn=fn):self.name=name;self.fn=fn
            def run(self,**kwargs):calls.append(self.name);return ModuleResult(data=self.fn(**kwargs))
        declared={field:Binding(source=ChannelSource.MODULE,type_name='float',channel_name=field) for field in outputs}
        registry.register(name,ModuleDescriptor(module_type=name,factory=Module,required_inputs={},optional_inputs={},outputs={k:float for k in outputs},version='test'))
        specs[name]=Spec(key=name,module_type=name,inputs={p:Binding(source=ChannelSource.MODULE,type_name='float',channel_name=p) for p in parents},outputs=declared)
        exits.update(declared)
    specs['exit']=Spec(key='exit',module_type='ExitPoint',outputs=exits)
    graph=PipelineDagBuilder().build(PipelineSpecification(modules=specs))
    executor=SerialPipelineExecutor(registry);context=PipelineExecutionContext(registry)
    return executor,context,graph,calls


def fault(**kwargs):raise ValueError('synthetic fault')


def diagnostic(nodes):
    executor,context,graph,calls=setup(nodes)
    result,records=executor.run_diagnostic(graph,context)
    return project_diagnostic(graph,result,records,fingerprint='synthetic',input_digest='synthetic'),context,calls


def test_diamond_independent_continuation_and_ordinary_refusal():
    nodes=[('up',[],lambda:2.,['up_value']),('bad',['up_value'],fault,['bad_value']),('good',['up_value'],lambda up_value:up_value*3,['good_value']),('join',['bad_value','good_value'],lambda **kw:99.,['joined'])]
    evidence,context,calls=diagnostic(nodes)
    assert evidence.state=='partial' and evidence.numeric_outputs=={'up_value':2.,'good_value':6.}
    assert calls==['up','bad','good']
    assert evidence.modules['join']['root_causes']==('bad',)
    assert evidence.modules['exit']['status']=='blocked_dependency'
    assert not hasattr(evidence,'responses') and not hasattr(evidence,'outputs')
    with pytest.raises(TypeError):evidence.modules['bad']['status']='completed'
    executor,context,graph,calls=setup(nodes)
    with pytest.raises(ValueError,match='synthetic fault'):executor.run(graph,context,persist_outputs=False)
    assert calls==['up','bad']


@pytest.mark.parametrize('bad',[float('inf'),float('-inf'),float('nan'),1+2j])
def test_invalid_intermediate_cannot_be_masked(bad):
    evidence,context,calls=diagnostic([('bad',[],lambda:bad,['bad_value']),('mask',['bad_value'],lambda **kw:0.,['masked']),('independent',[],lambda:7.,['seven'])])
    assert evidence.numeric_outputs=={'seven':7.}
    assert 'mask' not in calls and 'bad_value' not in context.channels
    assert evidence.modules['bad']['status']=='unavailable_numeric_output'
    assert evidence.publications['masked']['status']=='blocked_dependency'


def test_partial_multioutput_atomic_rollback():
    evidence,context,calls=diagnostic([('bad',[],lambda:{'first':42.},['first','second']),('child',['first'],lambda **kw:0.,['child_value'])])
    assert not evidence.numeric_outputs and not context.channels
    assert calls==['bad']


def test_multiple_roots_preserved():
    evidence,_,calls=diagnostic([('bad1',[],fault,['one']),('bad2',[],fault,['two']),('join',['one','two'],lambda **kw:0.,['three'])])
    assert evidence.modules['join']['root_causes']==('bad1','bad2')


def test_normal_success_equal_and_fresh_context_required():
    nodes=[('first',[],lambda:4.,['value']),('second',['value'],lambda value:value*2,['answer'])]
    executor,context,graph,calls=setup(nodes)
    ordinary=executor.run(graph,context,persist_outputs=False)
    with pytest.raises(ValueError,match='fresh context'):executor.run_diagnostic(graph,context)
    evidence,_,_=diagnostic(nodes)
    assert evidence.state=='complete_diagnostic' and evidence.numeric_outputs==ordinary.outputs


def test_explicit_default_is_not_failure_fallback():
    executor,context,graph,calls=setup([('bad',[],fault,['bad_value']),('child',['bad_value'],lambda bad_value=None:5.,['child_value'])])
    result,records=executor.run_diagnostic(graph,context)
    assert calls==['bad'] and 'child_value' not in result.outputs


def test_missing_structured_publication_is_partial():
    from types import SimpleNamespace
    executor,context,graph,calls=setup([('ok',[],lambda:3.,['value'])])
    result,records=executor.run_diagnostic(graph,context)
    evidence=project_diagnostic(graph,SimpleNamespace(outputs={}),records,fingerprint='x',input_digest='y')
    assert evidence.state=='partial' and evidence.publications['value']['status']=='missing_publication'


def test_structured_numeric_field_cannot_mask_infinity():
    from pydantic import BaseModel
    class Payload(BaseModel):
        amount: float
    executor,context,graph,calls=setup([('source',[],lambda:Payload(amount=float('inf')),['payload']),('mask',['payload'],lambda **kw:0.,['masked']),('independent',[],lambda:7.,['seven'])])
    graph.spec.modules['source'].outputs['payload']=graph.spec.modules['source'].outputs['payload'].model_copy(update={'type_name':'Payload'})
    graph.spec.modules['mask'].inputs['payload']=graph.spec.modules['mask'].inputs['payload'].model_copy(update={'field_path':'amount'})
    result,records=executor.run_diagnostic(graph,context)
    assert 'mask' not in calls and 'masked' not in result.outputs
    assert records['mask']['status']=='unavailable_numeric_input'
    assert result.outputs['seven']==7.


def test_explicit_default_binding_still_runs():
    executor,context,graph,calls=setup([('module',[],lambda value=None:5. if value is None else 9.,['answer'])])
    graph.spec.modules['module'].inputs['value']=Binding(source=ChannelSource.DEFAULT,type_name='float',channel_name='default')
    result,records=executor.run_diagnostic(graph,context)
    assert result.outputs['answer']==5. and records['module']['status']=='completed'
