"""Independent preservation, native scaling, and public-contract checks."""
import ast,collections,json,math,re,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
PACKAGE=ROOT/'exploration/stellarator_e2e/generated'
checks={}
for kind in ('positive','financial'):
 old=json.loads((HERE/f'baseline-{kind}.json').read_text())
 new=json.loads((HERE/f'candidate-{kind}.json').read_text())
 assert old==new,kind+' outputs/report/error changed'
 checks[kind]={'cases':len(new['cases']),'successful':sum('outputs' in v for v in new['cases'].values()),'equal':True,'errors':{k:v['message'] for k,v in new['cases'].items() if 'error'in v}}
rows=json.loads((HERE/'candidate-positive.json').read_text())['cases']
base=rows['baseline']['outputs'];double=rows['double_current']['outputs']
ratios={}
for name in base:
 if name.endswith(('wp_side','sigma_wp','B_axis','vol_cold_total','eps_cond')):
  ratios[name]=double[name]/base[name]
  expected=math.sqrt(2) if name.endswith('wp_side') else 2**1.5 if name.endswith(('sigma_wp','eps_cond')) else 2
  assert ratios[name]==__import__('pytest').approx(expected,rel=1e-12),(name,ratios[name],expected)
checks['double_current_ratios']=ratios
# Compare contracts structurally, disregarding generated schema prose only.
def strip_docs(obj):
 if isinstance(obj,dict):return {k:strip_docs(v) for k,v in obj.items() if k not in ('description','title')}
 if isinstance(obj,list):return [strip_docs(v) for v in obj]
 return obj
for name in ('model_contract.json','package_contract.json'):
 path=PACKAGE/'contracts'/name
 old=json.loads(subprocess.check_output(['git','show','HEAD:'+str(path.relative_to(ROOT))],cwd=ROOT,text=True))
 new=json.loads(path.read_text())
 if name == 'package_contract.json':
  assert old['executable_fingerprint'] != new['executable_fingerprint']
  checks['executable_identity']={'before':old.pop('executable_fingerprint'),'after':new.pop('executable_fingerprint')}
  old.pop('artifact_hashes');new.pop('artifact_hashes')
 assert strip_docs(old)==strip_docs(new),name
 checks[name]='semantic equality; package artifact hashes and executable identity change as recorded'
# All generated Python wrappers/schemas/tests retain their executable AST.
def no_docs(tree):
 for node in ast.walk(tree):
  if hasattr(node,'body') and isinstance(node.body,list):
   node.body=[v for v in node.body if not (isinstance(v,ast.Expr) and isinstance(v.value,ast.Constant) and isinstance(v.value.value,str))]
 return ast.dump(tree,include_attributes=False)
changes=json.loads((HERE/'package-changes.json').read_text())
checked=[]
for name in changes:
 if name.endswith('.py') and not name.startswith('handwritten/'):
  path=PACKAGE/name
  old=subprocess.check_output(['git','show','HEAD:'+str(path.relative_to(ROOT))],cwd=ROOT,text=True)
  assert no_docs(ast.parse(old))==no_docs(ast.parse(path.read_text())),name
  checked.append(name)
checks['unchanged_generated_AST']=checked
(HERE/'acceptance-summary.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
