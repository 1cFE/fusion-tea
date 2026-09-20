from pathlib import Path
from tempfile import mkdtemp
from sysml_codegen.cli import GenerationConfig,run_codegen
import json
base=Path(mkdtemp(prefix='wi076-origin-probe-'))
for label,binding in [('zero', '= 0.0'),('positive', '= 186.0'),('equal', '= -186.9046987566545'),('default', 'default -186.9046987566545'),('default_assign', 'default := -186.9046987566545'),('assign', ':= -186.9046987566545')]:
 src=base/label;src.mkdir()
 (src/'model.sysml').write_text("package Probe { private import ScalarValues::*; calc def 'Echo' { in attribute x : Real; out attribute y : Real = x + 1.0; } part def Box { attribute x : Real default 0.0; calc echo : 'Echo' { in x = Box::x; } } part box : Box { :>> x "+binding+"; } }")
 try:
  ok=run_codegen(GenerationConfig(models_path=src,output_path=base/(label+'_out')))
  contract=json.loads((base/(label+'_out')/'contracts/model_contract.json').read_text()) if ok else {}
  print('RESULT',label,ok,contract.get('parameters'))
 except Exception as exc:print('RESULT',label,type(exc).__name__,str(exc)[:250])
print('SCRATCH',base)
