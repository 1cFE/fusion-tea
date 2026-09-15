"""Retain the immediately entering package and oracle comparisons before the fit screen."""
import itertools,json,shutil,subprocess
from pathlib import Path
from exploration.stellarator_e2e.studies import oracle_entry as oe,study_route as route
from scripts.study.verify import derive_verdict,package_input_values
H=Path(__file__).resolve().parent
D=H/'entering';D.mkdir(exist_ok=True)
for rel in ('studies/oracle_entry.py','verify_stellaris.py','oracle_finance.py','studies/manifest.json','generated/contracts/model_contract.json','generated/contracts/package_contract.json','generated/inputs/stellarator_plant_params.json'):
    src=Path('exploration/stellarator_e2e')/rel
    if src.exists():
        target=D/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,target)
P=oe.P
j0=oe.vs.IN['magnet_j_wp']
proposals=[]
for j,b,a,i in itertools.product((.8,1.,1.2),(20.,24.9,30.),(1.3,1.7,2.1),(15.4e6,17e6)):
    proposals.append({'id':f'm{len(proposals):03d}','arm':'density-envelope-length-current','point':{P+'magnet__winding_pack__j_wp':j*j0,P+'magnet__winding_pack__B_max':b,P+'plasma__a':a,P+'magnet__coil__I_coil':i}})
for r,j in itertools.product((11.43,13.97),(.8,1.,1.2)):
    proposals.append({'id':f'm{len(proposals):03d}','arm':'major-radius','point':{P+'plasma__R':r,P+'magnet__winding_pack__j_wp':j*j0,P+'plasma__a':1.7}})
catalog=route._catalog_by_constraint_id(route.PACKAGE_DIR)
params=package_input_values(route.PACKAGE_DIR);bindings=oe.operand_bindings()
rows=[]
for proposal in proposals:
    channels=oe.evaluate(proposal['point'])
    verdicts={e['source_local_identity']:('satisfied' if derive_verdict(cid,e,bindings,proposal['point'],params,channels)[0] else 'violated') for cid,e in catalog.items()}
    rows.append(proposal|{'channels':channels,'verdicts':verdicts})
(D/'comparison.json').write_text(json.dumps({'revision':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'scope':'Entering oracle comparison, not native study execution; engineered sensitivity candidates','baseline':oe.evaluate({}),'rows':rows},indent=2)+'\n')
(H/'candidate-proposals.json').write_text(json.dumps(proposals,indent=2)+'\n')
route.write_identity_document(route.PACKAGE_DIR,D/'package-identity.json')
print('Retained',len(rows),'entering oracle points plus baseline and package identity')
