"""Re-execute the frozen native package in an external output directory.

Run with the recorded Python/teax environment. This never edits the study record.
The copied package, route and inputs are authoritative; no live model is loaded.
"""
import argparse,importlib.util,json,math,os,shutil,subprocess,sys
from pathlib import Path
H=Path('/home/reid/1cfe/fusion-tea/exploration/stellarator_e2e/studies/20260919-throughput-based-fuel-processing-costs')
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
out=args.out.resolve()
if out.is_relative_to(H) or out.exists():raise SystemExit('Use a new output directory outside the immutable record')
snap=json.loads((H/'snapshot.json').read_text())
teax=Path(os.environ['STOP_PARSER_TEAX_ROOT'])
revision=subprocess.check_output(['git','-C',str(teax),'rev-parse','HEAD'],text=True).strip()
if revision!=snap['teax']['revision']:raise SystemExit('Recorded teax revision is required')
out.mkdir(parents=True)
shutil.copytree(H/'preparation/producer-package',out/'package')
shutil.copytree(H/'preparation/tool-sources',out/'tools')
sys.path.insert(0,str(teax/'packages/teax-simkit'));sys.path.insert(0,str(out/'tools'))
source=out/'tools/exploration/stellarator_e2e/studies/study_route.py'
spec=importlib.util.spec_from_file_location('frozen_study_route',source);route=importlib.util.module_from_spec(spec);spec.loader.exec_module(route)
proposals=json.loads((H/'preparation/proposals.json').read_text())
proposals=[r for r in proposals if r['id'] in ('reference','burn-0.025','margin-1.5','legacy-reference')]
required=json.loads((H/'preparation/required-channels.json').read_text())
cases,db=route.run_points(H.name,[r['point'] for r in proposals],out/'native',package_dir=out/'package',required_channels={k:k for k in required})
canonical=lambda p:json.dumps({k:float(v) for k,v in p.items()},sort_keys=True)
prior={canonical(c['inputs']):c for c in json.loads((H/'results/native-cases.json').read_text())}
checks=0
for case in cases:
 old=prior[canonical(case.inputs)]
 assert case.state=='completed' and case.verdicts==old['verdicts']
 assert set(case.outputs)==set(old['outputs'])
 for key,actual in case.outputs.items():
  assert math.isclose(actual,old['outputs'][key],rel_tol=1e-9,abs_tol=1e-18 if '__fuel_cycle__inventory__' in key else 1e-9),(case.candidate_id,key)
  checks+=1
(out/'reproduction.json').write_text(json.dumps({'cases':len(cases),'native_scalar_comparisons':checks,'predicates_equal':True,'store':str(db),'fingerprint':snap['fingerprints']['recorded_provenance.executable_fingerprint'],'scope':'Frozen native-to-native reproduction, not independent physical validation.'},indent=2)+'\n')
print('Reproduced',len(cases),'cases and',checks,'native scalar entries; record unchanged')
