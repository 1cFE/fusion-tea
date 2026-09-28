"""Postprocess retained native evidence; no execution or new physical model."""
import json,math
from pathlib import Path
G=Path(__file__).resolve().parents[1];H=G.parents[3]/'exploration/stellarator_e2e/studies/20260916-bounded-feasibility-transfer';P='stellarator_09__stellaris__'
rows=json.loads((H/'results/native-cases.json').read_text()); by={r['proposal_id']:r for r in rows}
base=by['control-allocated-current-sized-reference']; anchors=['transfer-smaller',base['proposal_id'],'transfer-larger'];report={'anchors':[],'one_input_contrasts':[],'transverse_contrasts':[],'loop_contrasts':[],'scope':'Retained native evidence, all-point independent-oracle receipt separate. Held-output checks do not validate held physical assumptions.'}
keys=['plasma__fusion__p_fus','magnet__peak_field_calc__B_peak','magnet__winding_procurement__tape_length','magnet__wp_fit__margin_x','magnet__wp_fit__margin_y','plasma__sustain__p_aux_required','divertor__divheat__q_target_peak','divertor__divheat__power_account_valid','heat_transport__primary_loop__mdot_loop','heat_transport__primary_loop__p_elec','blanket__source_heat__q_source','pb__p_net','calendar__availability','fuel_cycle__fuel__tbr_required','fuel_cycle__fuel__tbr_margin','magnet__magnet_capital_rollup__capital_cost','lcoe_calc__lcoe']
for id in anchors:
 r=by[id];report['anchors'].append({'id':id,'inputs':r['inputs'],'outputs':{k:r['outputs'][P+k] for k in keys},'verdicts':r['verdicts']})
for r in rows:
 if r['proposal_id'].startswith('transfer-') and r['proposal_id'] not in anchors:
  changed={k:[base['inputs'].get(k),v] for k,v in r['inputs'].items() if v!=base['inputs'].get(k)}
  assert len(changed)==1
  report['one_input_contrasts'].append({'id':r['proposal_id'],'changed_inputs':changed,'changed_outputs':[k for k,v in r['outputs'].items() if v!=base['outputs'][k]],'selected_outputs':{k:r['outputs'][P+k] for k in keys}})
near=by['lhs-03-i-0.02-a+0.00']
for r in rows:
 if r['proposal_id'].startswith('near-y-'):
  changed=[k for k,v in r['outputs'].items() if v!=near['outputs'][k]]
  assert all('wp_fit' in k for k in changed)
  report['transverse_contrasts'].append({'id':r['proposal_id'],'changed_outputs':changed,'model_cost_response':0,'meaning':'Only fit responds; added transverse geometry has incomplete physical/accounting response.'})
 if r['proposal_id'].startswith('near-loops-'):
  held=[k for k in near['outputs'] if k.startswith(P+'magnet__') or k.startswith(P+'divertor__divheat__')]
  assert all(r['outputs'][k]==near['outputs'][k] for k in held)
  report['loop_contrasts'].append({'id':r['proposal_id'],'held_magnet_divertor_outputs':len(held),'pump_MW':r['outputs'][P+'heat_transport__primary_loop__p_elec'],'net_MW':r['outputs'][P+'pb__p_net']})
assert len(report['one_input_contrasts'])==6 and len(report['transverse_contrasts'])==3 and len(report['loop_contrasts'])==4
(G/'evidence/transfer-checks.json').write_text(json.dumps(report,indent=2)+'\n');print('transfer checks pass: 3 anchors, 6 single-input contrasts, 3 transverse and 4 loop contrasts')
