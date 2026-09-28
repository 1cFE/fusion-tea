"""Read recorded results only; never imports or executes the physical model."""
import hashlib, json
from pathlib import Path
H=Path(__file__).resolve().parent
S=Path('exploration/stellarator_e2e/studies/20260916-stellaris-reference-reconciliation')
P='stellarator_09__stellaris__'
raw=json.loads((S/'results/native-cases.json').read_text())
rows=[]
for r in raw:
 o={k.removeprefix(P):v for k,v in r['outputs'].items()}
 terms={k.removeprefix('plasma__sustain__'):v for k,v in o.items() if k.startswith('plasma__sustain__')}
 terms['p_fus']=o['plasma__fusion__p_fus']; terms['p_transport']=terms['W_th']/terms['tau_E']
 terms['residual_check']=terms['p_rad']+terms['p_transport']-terms['p_alpha_heat']-terms['p_aux_required']
 rows.append(dict(case=r['proposal_id'],candidate_id=r['candidate_id'],inputs=r['inputs'],terms=terms,downstream={k:v for k,v in o.items() if k.startswith(('divertor__divheat__','pb__','operating_heat__','heating__heat__','lcoe_calc__','heat_transport__primary_loop__','blanket__source_heat__'))},verdicts=r['verdicts']))
files=['models/library/analyses/mfe_plasma_sustainment.sysml','exploration/stellarator_e2e/models/analyses/mfe_plasma_sustainment.sysml','exploration/stellarator_e2e/generated/handwritten/mfe_plasma_sustainment/plasma_sustainment_impl.py','exploration/stellarator_e2e/verify_stellaris.py',str(S/'preparation/verify_stellaris.py'),str(S/'results/native-cases.json'),str(S/'results/oracle-all-points.json')]
identity={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in files}
comparison=[]
for a,b in [('legacy-control','exact-profiles-legacy'),('exact-profiles-legacy','table5-conditioned-legacy')]:
 x=next(r for r in rows if r['case']==a)['terms'];y=next(r for r in rows if r['case']==b)['terms']
 comparison.append(dict(start=a,end=b,delta_rad=y['p_rad']-x['p_rad'],delta_transport=y['p_transport']-x['p_transport'],delta_minus_alpha=x['p_alpha_heat']-y['p_alpha_heat'],delta_aux=y['p_aux_required']-x['p_aux_required']))
(H/'inventory.json').write_text(json.dumps(dict(scope='Stored native results plus arithmetic; no new model evaluation',identity=identity,cases=rows,ordered_attribution=comparison),indent=2)+'\n')
lines=['| Case | Fusion MW | W MJ | tau s | Brems MW | W-line MW | Sync MW | W/tau MW | Retained alpha MW | Auxiliary MW |','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
for r in rows:
 t=r['terms'];lines.append('| '+r['case']+' | '+' | '.join(f'{t[k]:.9f}' for k in ['p_fus','W_th','tau_E','p_brems','p_line','p_sync','p_transport','p_alpha_heat','p_aux_required'])+' |')
(H/'controls.md').write_text('# Recorded native controls\n\n'+ '\n'.join(lines)+'\n')
print(json.dumps({'identity':identity,'ordered_attribution':comparison,'table5_downstream':rows[4]['downstream'],'table5_verdicts':rows[4]['verdicts']},indent=2))
