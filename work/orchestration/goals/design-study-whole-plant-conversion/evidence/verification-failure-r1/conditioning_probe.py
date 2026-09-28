"""Local binary64 conditioning analysis; no native study or acceptance changes."""
import json,math,hashlib,sys
from decimal import Decimal,localcontext
from pathlib import Path
ROOT=Path(__file__).resolve().parents[6];HERE=Path(__file__).resolve().parent
RECORD=ROOT/'exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion'
P='whole_plant_conversion__plant__'
sys.path.insert(0,str(ROOT))
from exploration.whole_plant_conversion import verify
center=json.loads((RECORD/'preparation/extension-plan.json').read_text())['cryogenic_brackets'][0]['threshold_W_m3']
cases=json.loads((RECORD/'results/cases.json').read_text())['cases']
rows=[]
for case in cases:
 if not case['case'].startswith('cryo-capacity-'):continue
 inputs=case['inputs'];outputs=case['outputs'];core=lambda key:outputs[P+'supplied_core__evaluate__'+key]
 rating=inputs[P+'cryogenic_offer__cold_rating_W'];volume=core('cold_volume_m3');fixed=core('fixed_cold_MW');inventory=core('inventory_cold_W');extra=inputs[P+'cryogenic_demand__extra_cold_W'];original_q=inputs[P+'cryogenic_demand__q_nuc_W_m3']
 threshold=center
 oracle=verify.evaluate(inputs);ocore=lambda key:oracle[P+'supplied_core__evaluate__'+key]
 ovolume=ocore('cold_volume_m3');ofixed=ocore('fixed_cold_MW');oinventory=ocore('inventory_cold_W')
 for spacing in (1e-5,1e-4,1e-3,1e-2):
  q=threshold+(-spacing if '-below-' in case['case'] else spacing)
  # Diagnose the two published operation orders, without importing either body.
  mw=(q*volume+extra)*1e-6+fixed+inventory*1e-6
  native_order_cold=mw*1e6;watt_order_cold=math.fsum([q*ovolume,extra,ofixed*1e6,oinventory])
  native_order_margin=rating-native_order_cold;watt_order_margin=rating-watt_order_cold
  with localcontext() as ctx:
   ctx.prec=60;d=Decimal.from_float
   exact=d(rating)-(d(q)*d(volume)+d(extra)+d(fixed)*Decimal(1000000)+d(inventory))
  absolute=abs(native_order_margin-watt_order_margin);relative=absolute/max(abs(watt_order_margin),1e-30)
  native_extra=rating-inventory-fixed*1e6-q*volume;oracle_extra=rating-q*ovolume-ofixed*1e6-oinventory
  extra_relative=abs(native_extra-oracle_extra)/max(abs(oracle_extra),1e-30)
  rows.append(dict(original_case=case['case'],candidate_id=case['candidate_id'],spacing_W_m3=spacing,q_nuc_W_m3=q,threshold_W_m3=threshold,original_point=q==original_q,native_inputs=dict(volume_m3=volume,inventory_W=inventory,fixed_MW=fixed),oracle_inputs=dict(volume_m3=ovolume,inventory_W=oinventory,fixed_MW=ofixed),native_order_cold_W=native_order_cold,oracle_order_cold_W=watt_order_cold,native_order_margin_W=native_order_margin,oracle_order_margin_W=watt_order_margin,exact_arithmetic_margin_of_binary64_inputs_W=str(exact),absolute_order_difference_W=absolute,relative_order_difference=relative,native_order_extra_cold_capacity_W=native_extra,oracle_order_extra_cold_capacity_W=oracle_extra,extra_cold_capacity_relative_difference=extra_relative,unchanged_relative_rule_pass=relative<1e-9,native_margin_reproduced_from_published_order=(native_order_margin==outputs[P+'cryogenic_demand__evaluate__cold_margin_W']) if q==original_q else None,margin_sign_consistent=native_order_margin*watt_order_margin>0,cold_sum_ulp_W=math.ulp(native_order_cold)))
result=dict(kind='diagnosis of published arithmetic and native/independent captured intermediates; proposed spacings have no native execution authority',production_formula='exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/conditional_cryogenic_demand_impl.py:11',independent_formula='exploration/whole_plant_conversion/oracle_whole_plant.py:174',recommended_spacing_W_m3=1e-2,recommendation='Replace only the four near-zero cryogenic boundary points in a reviewed new record; preserve failed study and unchanged equations/oracle/manifest/tolerances. Full native execution and stock verification remain required.',cases=rows)
(HERE/'conditioning-probe.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({str(s):dict(max_relative=max(max(x['relative_order_difference'],x['extra_cold_capacity_relative_difference']) for x in rows if x['spacing_W_m3']==s),all_signs_consistent=all(x['margin_sign_consistent'] for x in rows if x['spacing_W_m3']==s)) for s in (1e-5,1e-4,1e-3,1e-2)},indent=2))
