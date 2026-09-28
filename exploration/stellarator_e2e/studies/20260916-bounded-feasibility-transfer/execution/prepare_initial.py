import json,shutil,random
from pathlib import Path
from exploration.stellarator_e2e.studies import study_route as route
from scripts.study.verify import package_input_values
H=Path('exploration/stellarator_e2e/studies/20260916-bounded-feasibility-transfer');P=route.P
write=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n')
old=H.parent/'20260916-primary-loop-sizing'
for n in ['manifest.json','oracle_entry.py','ANNEX.md','study_route.py']:shutil.copy2(H.parent/n,H/'preparation'/n)
for n in ['verify_stellaris.py','oracle_finance.py']:shutil.copy2(H.parent.parent/n,H/'preparation'/n)
for n in ['contracts','inputs','pipelines','schemas']:shutil.copytree(route.PACKAGE_DIR/n,H/'preparation'/('package-'+n),dirs_exist_ok=True)
write(H/'preparation/resolved-defaults.json',package_input_values(route.PACKAGE_DIR))
rows=json.loads((old/'preparation/unique-proposals.json').read_text())
controls=[r for r in rows if r['point'][P+'heat_transport__n_loops']==16]
base=controls[-1]['point']|{P+'plasma__R':12.7,P+'plasma__a':1.3,P+'magnet__coil__I_coil':15.4e6,P+'magnet__coil__coil_t':.60,P+'magnet__casing__interior_y':.60,P+'magnet__winding_pack__sizing_mode':1.,P+'magnet__winding_pack__inventory_multiplier':1.01}
write(H/'preparation/search-base.json',base)
scan=[{'id':'control-'+r['base_id'],'family':'control','point':r['point']} for r in controls]
scan.append({'id':'allocated-reference','family':'transfer-reference','point':base})
rng=random.Random(20260916); strata=[]
for lo,hi in [(10.5,13.5),(1.1,1.55),(12e6,16.2e6)]:
 vals=[lo+(hi-lo)*(i+.5)/64 for i in range(64)];rng.shuffle(vals);strata.append(vals)
for i,values in enumerate(zip(*strata)):
 scan.append({'id':f'lhs-{i:02}','family':'initial-search','point':base|dict(zip([P+'plasma__R',P+'plasma__a',P+'magnet__coil__I_coil'],values))})
write(H/'preparation/scan-proposals.json',scan)
axes=['plasma__R','plasma__a','magnet__coil__I_coil','magnet__coil__coil_t','magnet__casing__interior_y','heat_transport__n_loops','magnet__winding_pack__sizing_mode','magnet__winding_pack__inventory_multiplier']
write(H/'axes.json',{'schema_version':'study-axis-declaration/v1','groups':[{'axis':a,'keys':[{'key':P+a,'provenance':'fan_out'}],'note':'Complete public attribute; sizing mode/reserve vary only in legacy controls. Main search fixed current sizing/reserve.'} for a in axes]})
c=json.loads((H/'preparation/integration-return.json').read_text())
write(H/'preparation/execution-release.json',{'authorized_by':'coordinator','candidate_pin':c['candidate']['pin'],'basis':'Unchanged source equations; inherited independent reviews plus scoped protocol; indicators must pass before baseline.'})
print(len(scan),'initial scan candidates; no evaluations')
