"""Independent native structured field-reference masking regression probe."""
import json, sys
from pathlib import Path
from pydantic import BaseModel
base=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(base/'native-teax'),str(base/'native-teax/tests')]
from test_partial_diagnostics import setup
from simkit.evaluation.diagnostics import project_diagnostic, source_digest
class Box(BaseModel):
    value:float
executor,context,graph,calls=setup([('producer',[],lambda:Box(value=float('inf')),['box']),('mask',['box'],lambda box:0.,['masked'])])
graph.spec.modules['producer'].outputs['box']=graph.spec.modules['producer'].outputs['box'].model_copy(update={'type_name':'Box'})
graph.spec.modules['mask'].inputs['box']=graph.spec.modules['mask'].inputs['box'].model_copy(update={'field_path':'value'})
result,records=executor.run_diagnostic(graph,context)
evidence=project_diagnostic(graph,result,records,fingerprint='review-probe',input_digest='synthetic')
print(json.dumps({'source_digest':source_digest(),'calls':calls,'numeric_outputs':dict(evidence.numeric_outputs),'state':evidence.state,'module_statuses':{k:v['status'] for k,v in evidence.modules.items()}},indent=2))
