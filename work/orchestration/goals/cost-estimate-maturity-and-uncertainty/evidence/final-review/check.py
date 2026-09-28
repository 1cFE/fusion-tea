import csv,hashlib,json,math,subprocess
from pathlib import Path
S=Path('exploration/stellarator_e2e/studies/20260919-cost-estimate-maturity-and-uncertainty');G=Path('work/orchestration/goals/cost-estimate-maturity-and-uncertainty');O=G/'evidence/final-review';commit='82bf78f8'
def blob(path,rev=commit):return subprocess.check_output(['git','show',f'{rev}:{path}'])
def digest(x):return hashlib.sha256(x).hexdigest()
snap=json.loads(blob(S/'snapshot.json'));assert digest(blob(S/'snapshot.json'))=='75fcaad1c0b01659235973d323d0e01871ce1c8949bbf10515f07419453bb0dd'
artifacts=sum([snap[k] for k in ['preparation_artifacts','review_artifacts','execution_artifacts','definition_artifacts']],[])+snap['arms'][0]['artifacts']+[{'path':'indicators.json','sha256':snap['indicators']['sha256']},{'path':'axes.json','sha256':snap['indicators']['axis_declaration']['digest']}];assert len(artifacts)==565
for a in artifacts:
 p=S/a['path'];assert digest(blob(p))==a['sha256'],str(p);assert digest(p.read_bytes())==a['sha256'],str(p)
assert blob('.project/active/demo-depth-rubric/rubric.md','dc0f0b6dc6512b29e1307da647f3a508a1f5356d')==Path('.project/active/demo-depth-rubric/rubric.md').read_bytes()
rows=list(csv.DictReader((S/'results/points.csv').open()));native={c['candidate_id']:c for c in json.loads((S/'results/native-cases.json').read_text())};allrows=list(csv.DictReader((S/'results/all-native-channels.csv').open()));P='stellarator_09__stellaris__';E='heat_transport__equipment__';checks=0

def eq(a,b):
 global checks
 assert math.isclose(float(a),float(b),rel_tol=1e-11,abs_tol=1e-6),(a,b)
 checks+=1
for r in allrows:
 for k,v in r.items():
  if k.startswith(P):eq(v,native[r['candidate_id']]['outputs'][k])
export_comparisons=checks
base=next(r for r in rows if r['id']=='reference');b=native[base['candidate_id']]['outputs'];accounts=list(csv.DictReader((G/'evidence/accounts/functional-accounts.csv').open()))
for r in rows:
 c=native[r['candidate_id']];out=c['outputs'];v=lambda k:out[P+k];f=lambda k:float(r[k]);rate=f('heat_transport__equipment_stainless_fabrication_usd2017_per_kg')
 for key in ['LCOE','overnight','annual_expense']:
  suffix={'LCOE':'lcoe_calc__lcoe','overnight':'total_capital__total_capital','annual_expense':'cas70_calc__annual_total'}[key];eq(f(key),v(suffix))
 direct=sum(5000000 if a['channel']=='@cas28_capital' else v(a['channel']) for a in accounts);eq(direct,f('direct'));eq(f('contingency'),direct*f('contingency_rate'));eq(f('indirect'),(direct+f('contingency'))*.2*8/6)
 eq(f('energy_MWh'),8760*f('net_MW')*f('availability'));eq(f('LCOE'),(f('overnight')*1.07**4*(.07/(1-1.07**-30))+f('annual_expense'))/f('energy_MWh'))
 for bill,mass,count in [('hx_purchase','hx_mass','ihx_count'),('primary_pipe_purchase','primary_pipe_mass',None),('secondary_pipe_purchase','secondary_pipe_mass',None),('bundle_event_purchase','bundle_mass','ihx_count')]:
  eq(v(E+bill),v(E+mass)*(v(E+count) if count else 1)*rate*321.9/245.1)
 for bill in ['hx_purchase','primary_pipe_purchase','secondary_pipe_purchase','bundle_event_purchase','bundle_event_installation','bundle_event_removal']:eq(v(E+bill),b[P+E+bill]*rate/310)
 for part in ['containment_capital','containment_installation']:eq(v('fuel_cycle__processing_cost__'+part),b[P+'fuel_cycle__processing_cost__'+part]*82.4/f('fuel_cycle__processing_containment_cpi'))
 eq(v('magnet__insulation_inventory__stock_cost'),v('magnet__insulation_inventory__sheet_area')*f('magnet__winding_pack__insulation_sheet_price'))
 assert len(c['verdicts'])==25 and sum(x=='violated' for x in c['verdicts'].values())==4
sources=[r for r in rows if r['family']=='source-envelope'];diags=[r for r in rows if r['family']=='contingency-diagnostic'];assert len(sources)==len(diags)==36 and len(rows)==74
axes=['heat_transport__equipment_stainless_fabrication_usd2017_per_kg','buildings__tonne_interpretation_kg','fuel_cycle__processing_containment_cpi','magnet__winding_pack__insulation_sheet_price'];key=lambda r:tuple(float(r[k]) for k in axes);dmap={key(r):r for r in diags};assert len(dmap)==36
for r in sources:
 d=dmap[key(r)]
 for k in ['direct','annual_expense','energy_MWh','replacement_total']:eq(r[k],d[k])
 assert float(r['overnight'])-float(d['overnight'])>float(r['contingency'])
 eq(r['energy_MWh'],base['energy_MWh'])
original=list(csv.DictReader((G/'evidence/precommit-record-repair/original/results/points.csv').open()))
assert len(original)==74
for a,brow in zip(original,rows):assert all(brow[k]==value for k,value in a.items()) and brow['arm_id']=='arm-native'
result={'verdict':'PASS','commit':commit,'snapshot_sha256':digest(blob(S/'snapshot.json')),'committed_artifacts_verified':len(artifacts),'current_artifacts_identical':len(artifacts),'numeric_equalities':checks,'export_native_comparisons':export_comparisons,'cases':74,'contingency_pairs':36,'source_LCOE_bounds':[min(float(r['LCOE']) for r in sources),max(float(r['LCOE']) for r in sources)],'source_overnight_bounds':[min(float(r['overnight']) for r in sources),max(float(r['overnight']) for r in sources)],'repair_existing_cells_unchanged':True,'rubric_unchanged':True,'scope':'Committed custody and independently authored arithmetic/export checks; reuse prior audited execution and frozen reproduction, no new physical/source validation.'}
(O/'checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
