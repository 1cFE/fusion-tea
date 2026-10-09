"""One baseline and the reviewed 48 kA supplied magnet offer; no model/package edits."""
from pathlib import Path
import dataclasses, hashlib, json, os, sys, traceback
ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
sys.path.insert(0,str(ROOT/'exploration/stellarator_e2e/studies'))
import study_route as route
from scripts.study.verify import package_input_values
P=route.P
OFFER={P+'magnet__winding_pack__wp_side':.54,P+'magnet__winding_pack__fit_aspect_ratio':.19,P+'magnet__casing__interior_y':1.30,
 P+'magnet__coil__turn_current':48000.,
 P+'magnet__winding_pack__allow_field_extrapolation':0.,
 P+'magnet__winding_pack__cost_escalation':321.9/130.7,
 P+'magnet__winding_pack__price_helium':88.16040477645615*321.9/334.4,
 P+'magnet__winding_pack__q_nuc_cryo':35.5,
 P+'cryoplant__rated_cold_W':40000.,P+'cryoplant__rated_intercept_W':60000.,
 P+'cryoplant__purchase_cost_per_module':62957384.24217385}

def save(name,value):
 (OUT/name).write_text(json.dumps(value,indent=2,sort_keys=True,default=str)+'\n')

def hashes():
 return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for base in [ROOT/'exploration/stellarator_e2e/generated',ROOT/'models'] for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts}

before=hashes();save('protected-before.json',before)
params=package_input_values(route.PACKAGE_DIR)
save('declared-cases.json',{'baseline':{},'offer':OFFER})
save('baseline-inputs.json',params)
save('offer-inputs.json',params|OFFER)
route.write_identity_document(route.PACKAGE_DIR,OUT/'package-identity.json')
try:
 cases,db=route.run_points('wi098-reviewed-magnet-capture',[{},OFFER],OUT/'native')
 save('case-fields.json',list(dataclasses.asdict(cases[0])) if dataclasses.is_dataclass(cases[0]) else list(vars(cases[0])))
 rows=[]
 for case in cases:
  row=dataclasses.asdict(case) if dataclasses.is_dataclass(case) else vars(case)
  rows.append(row)
 save('native-cases.json',rows)
 print('case states:',[(r.get('candidate_id'),r.get('state')) for r in rows])
except Exception as exc:
 save('refusal.json',{'type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()})
 raise
finally:
 after=hashes();save('preservation.json',{'before_count':len(before),'after_count':len(after),'changed':[k for k in before if before[k]!=after.get(k)],'added':sorted(set(after)-set(before)),'removed':sorted(set(before)-set(after))})
