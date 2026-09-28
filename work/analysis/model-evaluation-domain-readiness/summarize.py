from pathlib import Path
import json,collections,hashlib
P='stellarator_09__stellaris__';out=Path(__file__).resolve().parent;rows=[]
base=json.loads((out/'case-00.json').read_text());bo=base['result']['outputs'];desc=json.loads((out/'descendants.json').read_text())
for f in sorted(out.glob('case-*.json')):
 r=json.loads(f.read_text());s={k:r[k] for k in ('index','label','proposal','status')}; result=r.get('result',{});o=result.get('outputs',{})
 if o:
  report=result['report'];s.update(output_count=len(o),headline=report['headline'],constraint_statuses=dict(collections.Counter(x['status'] for x in report['results'])),violated=[x['constraint_id'] for x in report['results'] if x['status']!='satisfied'],undefined_channels={k:v for k,v in o.items() if ('evaluation_defined' in k or 'defined_flag' in k) and not v},selected={k:v for k,v in o.items() if any(k.endswith(z) for z in ['__lcoe_calc__lcoe','__total_capital__total_capital','__peak_field_calc__B_peak','__primary_loop__dp_loop','__primary_loop__mdot','__primary_loop__T_comp_in','__breeding__defined_flag','__breeding__tbr_mean'])})
 else:
  fail=r.get('exception_attributes',{}).get('failure',{});s.update(failure=fail,exception=r.get('exception'),unavailable_descendants=desc.get(fail.get('module_or_channel'),[]),partial_result_policy='Route returned no result; partial_artifacts as retained, never invent upstream values.')
 rows.append(s)
# Fixed-equipment proof for demand pair. Every effective input except demanded density matches.
checks=[]
for i in [4,5]:
 r=json.loads((out/f'case-{i:02}.json').read_text());inputs=r['typed_inputs'];bi=base['typed_inputs'];differences={k:[bi[g][k],v] for g,vs in inputs.items() for k,v in vs.items() if bi[g][k]!=v};o=r['result']['outputs'];cost_keys=[k for k in bo if any(w in k for w in ['__turbine_cost__cost','__heat_rejection_cost__cost','__cryoplant_cost__cost','__equipment__installed_total','__equipment__purchased_total','__equipment__hx_purchase','__equipment__replacement_annual'])];checks.append({'case':i,'all_input_differences':differences,'selected_cost_comparison':{k:[bo[k],o[k]] for k in cost_keys},'all_compared_costs_equal':all(bo[k]==o[k] for k in cost_keys)})
(out/'summary.json').write_text(json.dumps({'attempt_accounting':{'attempt1_native_calls':18,'attempt1_native_refusals_retained':4,'attempt1_returned_but_result_capture_failed':14,'attempt1_interrupted_call_maximum':1,'attempt2_calls':21,'maximum_total':40,'attempt2_returned':sum(s['status']=='returned' for s in rows),'attempt2_raised':sum(s['status']=='raised' for s in rows)},'fixed_hardware_checks':checks,'cases':rows},indent=2))
print(json.dumps(checks,indent=2));print('BASE VIOLATED',rows[0]['violated']); print('BASE FP',json.loads((out/'identity.json').read_text())['fingerprint'])
