"""Independent current-domain audit; writes only this audit's evidence."""
import hashlib, importlib.util, json, math, os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit')]
from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader
from simkit.study.bridge import CandidateBridge
pkg=ROOT/'exploration/stellarator_e2e/generated'
ev=PreparedEvaluator(ProvisionalPackageLoader(pkg,'stellarator_tea',HERE/'link',strict=True),pkg/'pipelines/pipeline.yaml',expects_constraint_report=True)
bridge=CandidateBridge(ev.entry_models); P='stellarator_09__stellaris__magnet__'; rows={}
cases={'base':{},'negative_pair':{'I_coil':-1e6,'j_wp':-100.},'zero':{'I_coil':0.},'minus_zero':{'I_coil':-0.},'zero_density':{'j_wp':0.},'minus_zero_density':{'j_wp':-0.},'zero_linkage':{'k_link':0.},'double':{'I_coil':30.8e6}}
for key in ('I_coil','j_wp'):
 for label,value in [('negative',-1.),('nan',math.nan),('inf',math.inf),('minus_inf',-math.inf)]:cases[key+'_'+label]={key:value}
for name,overrides in cases.items():
 try:
  r=ev.evaluate(bridge.build({P+k:v for k,v in overrides.items()})); rows[name]={'outputs':dict(r.outputs),'report':r.report}
 except Exception as e:rows[name]={'error':type(e).__name__,'message':str(e)}
 if name not in ('base','double'):
  assert rows[name].get('error')=='EvaluationFailed',(name,rows[name])
  expected=('must be nonzero' if name in ('zero','minus_zero','zero_linkage') else 'Winding Pack Sizing:')
  assert expected in rows[name]['message'],(name,rows[name])
a,b=rows['base']['outputs'],rows['double']['outputs']; ratios={}
for key in a:
 if key.endswith(('wp_side','B_axis','sigma_wp','eps_cond','vol_cold_total')):
  expected=math.sqrt(2) if key.endswith('wp_side') else 2**1.5 if key.endswith(('sigma_wp','eps_cond')) else 2
  ratio=b[key]/a[key];assert math.isclose(ratio,expected,rel_tol=1e-12);ratios[key]=ratio
# Exact bounded history: only explicit audit-authorized implementation paths inspected.
changed=subprocess.check_output(['git','diff','--name-only','747a8a35^','HEAD'],text=True,cwd=ROOT).splitlines()
assert not any(p.startswith(('exploration/ife','models/designs/ife')) for p in changed)
assert not any(p.startswith(('work/active/WI-051_mfe-model-owned-major-radius/implementation/','work/active/WI-053_magnet-and-cryogenic-input-domains/evidence/')) for p in changed)
evidence=ROOT/'work/active/WI-055_winding-pack-input-domain/evidence'
receipt=json.loads((evidence/'candidate-package-hashes.json').read_text())
for name,digest in receipt.items():assert hashlib.sha256((pkg/name).read_bytes()).hexdigest()==digest,name
seeds=json.loads((evidence/'candidate-seeds.json').read_text());assert len(seeds)==12
entering=json.loads((evidence/'manual-seeds.json').read_text())
for name,digest in entering.items():
 if 'plasma_sustainment_impl' not in name:assert seeds['handwritten/'+name]==digest
(HERE/'native.json').write_text(json.dumps({'cases':rows,'ratios':ratios,'receipt_files':len(receipt),'seeds':len(seeds),'changed_paths':changed},indent=2,default=str)+'\n')
print('PASS independent public native domain cases, linked scaling, exact receipt, nine inherited seed bodies and bounded unchanged history')
