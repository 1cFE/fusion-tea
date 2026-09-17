"""Declare eight complete native points without evaluating scientific results."""
import json, math, shutil
from pathlib import Path
from scripts.study.verify import package_input_values
from exploration.stellarator_e2e.studies import study_route as route
H=Path(__file__).resolve().parents[1]; ROOT=H.parents[3]; PREP=H/'preparation'; GOAL=ROOT/'work/orchestration/goals/stellaris-reference-reconciliation'; P=route.P
read=lambda p:json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,indent=2,allow_nan=False)+'\n')
for name in ['manifest.json','oracle_entry.py','ANNEX.md','study_route.py']:shutil.copy2(H.parent/name,PREP/name)
for name in ['verify_stellaris.py','oracle_finance.py']:shutil.copy2(H.parent.parent/name,PREP/name)
for name in ['contracts','inputs','pipelines','schemas']:shutil.copytree(route.PACKAGE_DIR/name,PREP/('package-'+name),dirs_exist_ok=True)
params=package_input_values(route.PACKAGE_DIR);write(PREP/'resolved-defaults.json',params)
contract=read(PREP/'package-contracts/model_contract.json');write(PREP/'required-channels.json',sorted(o['channel_name'] for o in contract['outputs'] if o['python_type'] in ['float','int']))
keys=['plasma__R','plasma__a','plasma__f_shape','plasma__alpha_n','plasma__alpha_T','magnet__coil__I_coil','magnet__winding_pack__sizing_mode','magnet__winding_pack__inventory_multiplier']
base={P+k:params[P+k] for k in keys}
rows=[]
def add(pid,point):rows.append({'id':pid,'proposal_id':pid,'canonical_proposal_id':pid,'family':pid,'arm':'arm-native','point':point})
selected={P+'magnet__winding_pack__sizing_mode':1.,P+'magnet__winding_pack__inventory_multiplier':1.01}
exact=base|{P+'plasma__alpha_n':.35,P+'plasma__alpha_T':1.2}
conditioned=exact|{P+'plasma__R':12.74,P+'plasma__a':1.3,P+'plasma__f_shape':425/(2*math.pi**2*12.74*1.3**2),P+'magnet__coil__I_coil':base[P+'magnet__coil__I_coil']*12.74/base[P+'plasma__R']}
for pid,pt in [('legacy-control',base),('selected-reserve-control',base|selected),('exact-profiles-legacy',exact),('exact-profiles-selected-reserve',exact|selected),('table5-conditioned-legacy',conditioned),('table5-conditioned-selected-reserve',conditioned|selected),('offref-R-plus2pct',exact|{P+'plasma__R':base[P+'plasma__R']*1.02}),('offref-a-plus2pct',exact|{P+'plasma__a':base[P+'plasma__a']*1.02})]:add(pid,pt)
assert len(rows)==8 and all(set(r['point'])<=set(params) for r in rows)
groups=[{'axis':k,'note':'Complete native public attribute; coordinated source conditioning is declared in protocol.md, never an independent prediction.', 'keys':[{'key':P+k,'provenance':'fan_out'}]} for k in keys]
write(H/'axes.json',{'schema_version':'study-axis-declaration/v1','groups':groups})
for name in ['proposals.json','unique-proposals.json','scan-proposals.json']:write(PREP/name,rows)
shutil.copy2(GOAL/'goal.md',PREP/'goal-at-authority.md');shutil.copy2(GOAL/'evidence/execution-design.md',PREP/'execution-design.md');shutil.copy2(ROOT/'modeling_project/STUDY_POLICY.md',PREP/'STUDY_POLICY.md')
print('Prepared eight cases and eight complete entry groups. No scientific evaluation.')
