"""WI-059 native candidate witnesses, every mapped channel compared independently."""
from pathlib import Path
import sys,json,math
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'exploration/stellarator_e2e/studies'))
import oracle_entry as oe
from exploration.stellarator_e2e.studies import study_route as route
P=route.P; H=Path(__file__).resolve().parent
points=[{}, {P+'plasma__a':1.7,P+'magnet__coil__I_coil':13e6,P+'plasma__n_e0':4.048e20},
        {P+'cryoplant__inventory_enabled':False,P+'magnet__c_support':0,P+'magnet__legacy_casing_fraction':1},
        {P+'cryoplant__q_nuc_structure':35.5,P+'structure__residual_fraction':0},
        {P+'cryoplant__f_carnot_cryo':.15,P+'cryoplant__f_carnot_shield':.15,P+'cryoplant__g_per_coil':.16}]
channels=oe.ORACLE_OUTPUT_TO_CHANNEL
cases,db=route.run_points('wi059-native-witnesses-r2',points,H/'offdesign-work-r2',required_channels=channels)
assert len(cases)==len(points), (len(cases),len(points))
rows=[]
for c in cases:
 assert c.state=='completed',c.state
 expected=oe.evaluate(c.inputs);missing=set(expected)-set(c.outputs);diff=[k for k,v in expected.items() if k in c.outputs and not math.isclose(v,c.outputs[k],rel_tol=1e-9,abs_tol=1e-12)]
 assert not missing and not diff,(missing,diff)
 rows.append({'id':c.candidate_id,'inputs':dict(c.inputs),'channels_checked':len(expected),'outputs':dict(c.outputs),'verdicts':dict(c.verdicts),'outcome':'pass'})
(H/'offdesign-results.json').write_text(json.dumps({'store':str(db),'cases':rows},indent=2)+'\n')
print(len(rows),'native points PASS',len(expected),'mapped channels each')
