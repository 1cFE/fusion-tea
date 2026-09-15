"""Verify all mapped scalars/verdicts and attribute the change to the entering oracle capture."""
import json,math
from pathlib import Path
from collections import Counter
H=Path(__file__).resolve().parents[1];R=H/'results';P='stellarator_09__stellaris__'
read=lambda p:json.loads(p.read_text())
def write(n,x):(R/n).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
rows=read(R/'native-cases.json'); byid={r['proposal_id']:r for r in rows}; scan={r['proposal_id']:r for r in read(R/'oracle-scan.json')['rows']};catalog=read(R/'predicate-catalog.json');params=read(H/'preparation/resolved-defaults.json')
fail=[];n=0;nv=0;worst=0
for r in rows:
 s=scan[r['proposal_id']]; assert r['inputs']==s['point']
 for k,want in s['channels'].items():
  assert k in r['outputs'];got=r['outputs'][k];n+=1;dev=abs(got-want)/max(abs(got),abs(want),1e-100);worst=max(worst,dev)
  if not math.isclose(got,want,rel_tol=1e-9,abs_tol=1e-12):fail.append({'proposal_id':r['proposal_id'],'channel':k,'native':got,'oracle':want})
 assert set(r['verdicts'])==set(s['verdicts'])
 for k,want in s['verdicts'].items():
  nv+=1
  if r['verdicts'][k]!=want:fail.append({'proposal_id':r['proposal_id'],'constraint_id':k})
write('oracle-all-points.json',{'outcome':'pass' if not fail else 'fail','cases':len(rows),'mapped_channels_per_case':len(next(iter(scan.values()))['channels']),'scalar_comparisons':n,'predicate_comparisons':nv,'max_relative_deviation':worst,'failures':fail,'unmapped_native_channels':sorted(set(rows[0]['outputs'])-set(next(iter(scan.values()))['channels']))});assert not fail
old=read(H/'preparation/entering/comparison.json'); oldcatalog=read(H/'preparation/entering/generated/contracts/model_contract.json')['constraint_catalog']['concrete_entries'];assert {c['constraint_id']:c for c in oldcatalog}==catalog
props={r['id']:r for r in read(H/'preparation/proposals.json')}; comparisons=[];changes=Counter();physical_fail=[];same=0;pv=0
# Changes are admitted only in the revised tape purchase and downstream economic totals.
economic=('magnet__winding_procurement__tape_cost','magnet__winding_procurement__cost','magnet__magnet_capital_rollup__capital_cost','cas20_capital__cas20_capital','cas22_capital__cas22_capital','cas2x_pre_contingency__cas2x_pre_contingency','cas90_1cfe_calc__cas90','contingency__cost','idc__cost','indirect__cost','installation__cost','lcoe_1cfe_calc__lcoe','lcoe_calc__lcoe','overnight_capital__overnight_capital','powercore_capital__powercore_capital','reactor_equipment_subtotal__reactor_equipment_subtotal','supplementary__cost','total_capital__total_capital')
for b in old['rows']:
 r=byid[props[b['id']]['canonical_proposal_id']];assert props[b['id']]['original_point']==b['point'];ds={};flips={}
 for k,w in b['channels'].items():
  if k not in r['outputs']:continue
  v=r['outputs'][k]
  if not math.isclose(v,w,rel_tol=1e-9,abs_tol=1e-12):
   ds[k]={'before':w,'after':v,'delta':v-w};changes[k]+=1
   if not k in {P+e for e in economic}:physical_fail.append({'proposal_id':b['id'],'channel':k,'before':w,'after':v})
  else:same+=1
 for c,e in catalog.items():
  pv+=1;name=e['source_local_identity'];w=b['verdicts'][name];v=r['verdicts'][c]
  if w!=v:flips[name]={'before':w,'after':v}
 comparisons.append({'proposal_id':b['id'],'candidate_id':r['candidate_id'],'entering_point':b['point'],'resolved_candidate_point':r['inputs'],'changed_channels':ds,'verdict_flips':flips})
write('comparison-entering.json',{'scope':'Increment against captured entering independent-oracle values, not entering native study execution','entering_revision':old['revision'],'matched_cases':len(comparisons),'unchanged_scalar_comparisons':same,'predicate_comparisons':pv,'predicate_catalog_exact_equal':True,'changed_channel_counts':dict(changes),'unexpected_physical_changes':physical_fail,'cases':comparisons})
assert not physical_fail,physical_fail[:3];assert not any(r['verdict_flips'] for r in comparisons)
def val(r,k):return r['outputs'][P+k]
def feasible(r):return all(v=='satisfied' for v in r['verdicts'].values())
def summarize(r):
 return {'proposal_id':r['proposal_id'],'candidate_id':r['candidate_id'],'inputs':r['inputs'],'lcoe':val(r,'lcoe_calc__lcoe'),'tape_length_m':val(r,'magnet__winding_procurement__tape_length'),'tape_cost':val(r,'magnet__winding_procurement__tape_cost'),'procurement_cost':val(r,'magnet__winding_procurement__cost'),'feasible_18':feasible(r),'violated':[catalog[c]['source_local_identity'] for c,v in r['verdicts'].items() if v!='satisfied']}
base=byid[props['baseline']['canonical_proposal_id']]; bch=old['baseline']
baseinfo=summarize(base)|{'entering_lcoe':bch[P+'lcoe_calc__lcoe'],'entering_tape_cost':bch[P+'magnet__winding_procurement__tape_cost'],'lcoe_delta':val(base,'lcoe_calc__lcoe')-bch[P+'lcoe_calc__lcoe'],'tape_cost_delta':val(base,'magnet__winding_procurement__tape_cost')-bch[P+'magnet__winding_procurement__tape_cost']}
# Independently check the disclosed inventory ratios and distinction from winding work.
identities=[]; jref=params[P+'magnet__winding_pack__j_wp']; BRef=params[P+'magnet__winding_pack__B_grade_ref']; exponent=params[P+'magnet__winding_pack__field_exponent'];ftape=1-sum(params[P+'magnet__winding_pack__'+k] for k in ['f_copper','f_solder','f_steel','f_helium'])
for r in rows:
 ip=params|r['inputs'];j=ip[P+'magnet__winding_pack__j_wp'];B=ip[P+'magnet__winding_pack__B_max'];q=(B/BRef)**exponent;area=ip[P+'magnet__winding_pack__tape_width']*ip[P+'magnet__winding_pack__tape_thickness'];L=val(r,'magnet__winding_procurement__tape_length');C=val(r,'magnet__winding_procurement__tape_cost');V=val(r,'magnet__wp_volume__vol_winding_pack')
 assert math.isclose(L,V*ftape/area,rel_tol=1e-12);assert math.isclose(C,L*ip[P+'magnet__winding_pack__tape_price_per_m'],rel_tol=1e-12)
 identities.append({'proposal_id':r['proposal_id'],'j_ratio':j/jref,'envelope_quantity_factor':q,'tape_metres':L,'tape_cost':C,'pack_volume_m3':V,'reference_coil_tape_loading_A':j/q*1e6*area/ftape,'set_effective_tape_loading_A':j/q*1e6*area/ftape*ip[P+'magnet__coil__f_set']/ip[P+'magnet__winding_pack__f_wp_vol']})
write('inventory-identities.json',{'outcome':'pass','cases':identities,'scope':'Arithmetic inventory identities; no absolute critical-current margin or integer tape-count qualification'})
# Group by every input except the chosen axis to expose matched pair effects.
responses={}
for axis in ['j_wp','B_max','a','R','I_coil','tape_price_per_m']:
 group=next(g for g in read(H/'axes.json')['groups'] if g['axis']==axis); k=group['keys'][0]['key'];groups={}
 for r in rows:
  point=dict(params|r['inputs']); point.pop(k); sig=json.dumps(point,sort_keys=True);groups.setdefault(sig,[]).append(r)
 result=[]
 for rs in groups.values():
  if len(rs)<2:continue
  rs.sort(key=lambda r:r['inputs'][k]);ref=rs[0]
  result.append({'points':[summarize(r)|{'axis_value':r['inputs'][k],'tape_ratio_to_first':val(r,'magnet__winding_procurement__tape_length')/val(ref,'magnet__winding_procurement__tape_length'),'volume_ratio_to_first':val(r,'magnet__wp_volume__vol_winding_pack')/val(ref,'magnet__wp_volume__vol_winding_pack'),'winding_cost':val(r,'magnet__winding_procurement__winding_fabrication_cost')} for r in rs]})
 responses[axis]=result
write('axis-responses.json',responses)
write('analysis.json',{'baseline':baseinfo,'unique_cases':len(rows),'report_rows':len(props),'feasible_18':sum(feasible(r) for r in rows),'feasible_cases':[summarize(r) for r in rows if feasible(r)],'price_cases':[summarize(r) for r in rows if r['proposal_id'].startswith('price-')],'violation_counts':{c:sum(r['verdicts'][c]!='satisfied' for r in rows) for c in catalog},'all_case_lcoe_range':[min(val(r,'lcoe_calc__lcoe') for r in rows),max(val(r,'lcoe_calc__lcoe') for r in rows)]})
print('ALL-POINT PASS',n,'scalar',nv,'predicate comparisons;',worst,'max relative deviation');print(json.dumps(baseinfo,indent=2))
# All-point combined identity: envelope, density, current and bore length multiply once.
checks=[]
for r in rows:
 ip=params|r['inputs'];bp=params|base['inputs'];cc=val(r,'magnet__coil_length__c_coil');cb=val(base,'magnet__coil_length__c_coil')
 ratio=(ip[P+'magnet__winding_pack__B_max']/bp[P+'magnet__winding_pack__B_max'])**exponent*(bp[P+'magnet__winding_pack__j_wp']/ip[P+'magnet__winding_pack__j_wp'])*(ip[P+'magnet__coil__I_coil']/bp[P+'magnet__coil__I_coil'])*(cc/cb)
 for channel in ['magnet__winding_procurement__tape_length','magnet__wp_volume__vol_winding_pack','magnet__material_inventory__mass_copper','magnet__material_inventory__mass_solder','magnet__material_inventory__mass_steel','magnet__material_inventory__mass_helium','magnet__material_inventory__material_cost']:
  assert math.isclose(val(r,channel)/val(base,channel),ratio,rel_tol=1e-12)
 wind=(ip[P+'magnet__coil__I_coil']/bp[P+'magnet__coil__I_coil'])*(cc/cb)
 for channel in ['magnet__winding_procurement__conductor_length','magnet__winding_procurement__winding_fabrication_cost']:
  assert math.isclose(val(r,channel)/val(base,channel),wind,rel_tol=1e-12)
 checks.append({'proposal_id':r['proposal_id'],'inventory_ratio_to_baseline':ratio,'winding_operations_ratio_to_baseline':wind,'circumference_ratio_to_baseline':cc/cb})
# Price changes leave every mapped physical quantity and all predicates unchanged.
price_checks=[]
for r in rows:
 if not r['proposal_id'].startswith('price-'):continue
 ip=params|r['inputs'];ip[P+'magnet__winding_pack__tape_price_per_m']=20.0
 nominal=next(c for c in rows if params|c['inputs']==ip)
 changed=[k for k in r['outputs'] if not math.isclose(r['outputs'][k],nominal['outputs'][k],rel_tol=1e-12,abs_tol=1e-12)]
 assert set(changed)<={P+e for e in economic}|{P+'cas70_calc__annual_total',P+'cas70_calc__cas70',P+'cas71_calc__levelized',P+'cas80_calc__levelized'}
 assert r['verdicts']==nominal['verdicts']
 price_checks.append({'price_proposal_id':r['proposal_id'],'nominal_proposal_id':nominal['proposal_id'],'changed_economic_channels':changed,'verdicts_unchanged':True})
write('combined-response-checks.json',{'outcome':'pass','combined_identity_checks':len(rows)*9,'rows':checks,'price_checks':price_checks,'qualification':'Identities are arithmetic checks against the native baseline and retained factors, supplementing the independent oracle rather than replacing it.'})
