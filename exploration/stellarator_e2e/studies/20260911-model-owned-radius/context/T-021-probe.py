"""Read-only F06/F07-radius probes. Run from repo root through .codex-test/run.

Launcher invocation: .codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python work/analysis/20260911-230953_radius-ownership-evidence/probe.py'
"""
import hashlib, importlib, json, math, subprocess, sys, tempfile
from pathlib import Path
from types import SimpleNamespace
from collections.abc import Mapping
import yaml
ROOT=Path.cwd(); HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'exploration/stellarator_e2e/studies'))
import study_route as route
import oracle_entry as oracle
from simkit.study.bridge import CandidateBridge
from tests.model_families import MFE,canonical_path
P=route.P; pkg=route.PACKAGE_DIR
scratch=Path(tempfile.mkdtemp(prefix='radius-ownership-'))
evaluator=route.prepare(pkg,scratch); bridge=CandidateBridge(evaluator.entry_models)
contract=json.loads((pkg/'contracts/model_contract.json').read_text())
inputs={}
for f in (pkg/'inputs').glob('*.json'): inputs.update(json.loads(f.read_text()))
results={'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'semantic_fingerprint':contract['semantic_fingerprint'],'input_count':len(contract['parameters']),'inputs':inputs,'cases':{},'component':{},'family_byte_equality':{p:canonical_path(p).read_bytes()==(MFE.twin/p).read_bytes() for p in MFE.owned}}
results['contract_parameters']=[p for p in contract['parameters'] if 'R0' in str(p) or P+'R' in str(p)]
pipeline=yaml.safe_load((pkg/'pipelines/pipeline.yaml').read_text())
results['radius_direct_bindings']={n:m['inputs'] for n,m in pipeline['modules'].items() if any(P+'R' in str(v) or P+'magnet__R0' in str(v) for v in m.get('inputs',{}).values())}
# The exact bore equality uses the model's sequential binary64 layer sum.
a=inputs[P+'a']; vessel=a
for k in ['vacuum_t','firstwall_t','blanket_t','reflector_t','ht_shield_t','structure_t','gap1_t','vessel_t']: vessel+=inputs[P+k]
bore=vessel+inputs[P+'coil_t']/2
cases={'baseline':{},'plant_only_R14':{P+'R':14.0},'magnet_only_R14':{P+'magnet__R0':14.0},'tied_R14':{P+'R':14.0,P+'magnet__R0':14.0},'tied_R4':{P+'R':4.0,P+'magnet__R0':4.0},'tied_bore_equal':{P+'R':bore,P+'magnet__R0':bore},'tied_bore_below':{P+'R':3.0,P+'magnet__R0':3.0},'plant_zero':{P+'R':0.0},'magnet_zero':{P+'magnet__R0':0.0},'tied_negative':{P+'R':-1.0,P+'magnet__R0':-1.0}}
for name,change in cases.items():
 row={'changes':change}
 for kind,fn in [('native',lambda:evaluator.evaluate(bridge.build(change))),('oracle',lambda:oracle.evaluate(change))]:
  try:
   r=fn(); row[kind]={'outputs':dict(r.outputs),'responses':dict(r.responses),'report':r.report} if kind=='native' else {'outputs':r}
  except Exception as exc: row[kind]={'error':type(exc).__name__,'message':str(exc)}
 if 'outputs' in row['native'] and 'outputs' in row['oracle']:
  g=row['native']['outputs']; o=row['oracle']['outputs']; row['differences']={k:{'native':g[k],'oracle':v,'delta':g[k]-v} for k,v in o.items() if k in g and not math.isclose(g[k],v,rel_tol=1e-9,abs_tol=1e-9)}
 results['cases'][name]=row
 print(name,'native',row['native'].get('error','ok'),'oracle',row['oracle'].get('error','ok'),'mismatches',len(row.get('differences',{})),flush=True)
module=importlib.import_module('stellarator_tea.handwritten.mfe_plasma_scaling.conductor_peak_field_impl')
for name,rr,aa,ref,refa in [('original_negative',12.7,13.,12.7,3.1500000000000004),('equality',12.7,12.7,12.7,3.1500000000000004),('valid',12.7,3.1500000000000004,12.7,3.1500000000000004),('reference_equal',12.7,3.15,12.7,12.7),('reference_inverted',12.7,3.15,12.7,13.)]:
 values=dict(B_axis_in=9.,peak_ratio_in=24.9/9.,R_in=rr,a_coil_in=aa,R_ref_in=ref,a_coil_ref_in=refa)
 try:
  value=module.run_conductor_peak_field(SimpleNamespace(**values)); row={'inputs':values,'B_peak':value,'upper_bound_24_9_satisfied':value<=24.9,'independent_expected':9*(24.9/9)*(rr/(rr-aa))/(ref/(ref-refa))}
 except Exception as exc: row={'inputs':values,'error':type(exc).__name__,'message':str(exc)}
 results['component'][name]=row
results['derived_baseline_geometry']={'vessel_outer':vessel,'coil_centre':bore,'outer_build':vessel+inputs[P+'coil_t']+inputs[P+'gap2_t']+inputs[P+'lt_shield_t']}
(HERE/'results.json').write_text(json.dumps(results,indent=2,default=lambda v:dict(v) if isinstance(v,Mapping) else str(v))+'\n')
print('retained',HERE/'results.json')
