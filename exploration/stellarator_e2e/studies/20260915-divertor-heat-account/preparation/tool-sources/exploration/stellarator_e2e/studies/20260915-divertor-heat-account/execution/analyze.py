"""Compare every mapped scalar/predicate and report conditional heat-account consequences."""
import csv
import json
import math
from collections import Counter
from pathlib import Path

H=Path(__file__).resolve().parents[1]
R=H/'results'
P='stellarator_09__stellaris__'
read=lambda p:json.loads(p.read_text())
def write(name,value): (R/name).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
def close(a,b): return math.isfinite(a) and math.isfinite(b) and math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-9)

native=read(R/'native-cases.json')
byid={r['proposal_id']:r for r in native}
scan={r['proposal_id']:r for r in read(R/'oracle-scan.json')['rows']}
old={r['proposal_id']:r for r in read(R/'entering-all-points.json')['rows']}
props={r['proposal_id']:r for r in read(H/'preparation/proposals.json')}
catalog=read(R/'predicate-catalog.json')
defaults=read(H/'preparation/resolved-defaults.json')
assert len(byid)==27 and set(byid)==set(scan)==set(old)==set(props)
assert len(catalog)==20
divid=next(cid for cid,e in catalog.items() if e['source_local_identity']=='divertor_heat_ok')
failures=[]
scalar_count=predicate_count=0
max_abs=max_rel=0.
for pid,row in byid.items():
    expected=scan[pid]
    assert row['inputs']==expected['point']
    assert len(expected['channels'])==226
    for channel,value in expected['channels'].items():
        got=row['outputs'][channel]
        scalar_count+=1
        max_abs=max(max_abs,abs(got-value))
        max_rel=max(max_rel,abs(got-value)/max(abs(value),abs(got),1e-300))
        if not close(got,value): failures.append({'proposal_id':pid,'channel':channel,'native':got,'oracle':value})
    assert set(row['verdicts'])==set(expected['verdicts'])==set(catalog)
    for cid,value in expected['verdicts'].items():
        predicate_count+=1
        if row['verdicts'][cid]!=value: failures.append({'proposal_id':pid,'constraint_id':cid,'native':row['verdicts'][cid],'oracle':value})
write('oracle-all-points.json',{'outcome':'fail' if failures else 'pass','cases':len(native),'scalar_comparisons':scalar_count,'predicate_comparisons':predicate_count,'relative_tolerance':1e-9,'absolute_tolerance':1e-9,'exact_predicates':True,'max_absolute_deviation':max_abs,'max_relative_deviation':max_rel,'failures':failures,'unmapped_native_channels':sorted(set(native[0]['outputs'])-set(scan[native[0]['proposal_id']]['channels']))})
comparison=[]
for pid,row in byid.items():
    previous=old[pid]
    entry={'proposal_id':pid,'entering_outcome':previous['outcome'],'scope':'Frozen entering oracle, same coordinates and source peak/radiation, only capture input removed.'}
    if previous['outcome']=='evaluated':
        changes={k:{'before':v,'after':row['outputs'][k],'delta':row['outputs'][k]-v} for k,v in previous['channels'].items() if not close(v,row['outputs'][k])}
        flips={k:{'before':v,'after':row['verdicts'][k]} for k,v in previous['verdicts'].items() if row['verdicts'][k]!=v}
        entry|={'scalar_comparisons':len(previous['channels']),'changed_channels':changes,'predicate_flips':flips}
    else: entry['error']=previous['error']
    comparison.append(entry)
preserved=all(e['entering_outcome']=='evaluated' and not e['changed_channels'] and not e['predicate_flips'] for e in comparison)
write('comparison-entering.json',{'scope':read(R/'entering-all-points.json')['scope'],'existing_outputs_and_predicates_preserved':preserved,'cases':comparison})
summaries=[]
for pid,row in byid.items():
    inputs=defaults|row['inputs']
    val=lambda suffix:row['outputs'][P+suffix]
    dh=lambda suffix:val('divertor__divheat__'+suffix)
    Habs=dh('p_heat_abs'); q=dh('q_target_peak'); limit=inputs[P+'divertor__q_target_limit']
    valid=dh('power_account_valid')==1
    active=dh('peak_equivalent_area_defined')==1
    rawpass=row['verdicts'][divid]=='satisfied'
    account={suffix:dh(suffix) for suffix in ['p_heat_abs','p_sep','p_target_nonrad','p_target_deposited','p_nonrad_uncaptured','p_rad_total','p_rad_edge','f_rad_edge','f_rad_edge_defined','f_rad_edge_in_range','peak_equivalent_area','peak_equivalent_area_defined','power_account_valid','q_target_peak','q_target_peak_area_scaled','q_target_margin']}
    account['p_rad_core']=val('plasma__sustain__p_rad')
    account['conservation_residual']=Habs-account['p_rad_core']-account['p_rad_edge']-account['p_target_deposited']-account['p_nonrad_uncaptured']
    account['peak_reconstruction_residual']=account['p_target_deposited']/account['peak_equivalent_area']-q if active else None
    needed={'applicable':q>limit and valid and active,'target_power_reduction_fraction':1-limit/q if q>limit else 0.,'equivalent_area_increase_fraction':q/limit-1 if q>limit else 0.,'required_total_radiation_fraction_at_held_H':1-limit*inputs[P+'divertor__p_nonrad_ref']/(inputs[P+'divertor__q_target_ref']*Habs),'interpretation':'Necessary arithmetic at held source transport and H; no achieved radiation control or physical wetted-area design. For invalid account, values are diagnostic only.'}
    quantities={label:val(key) for label,key in {'plant_heat_MW':'pb__p_th','target_cost':'divertor__divertor_cost__cost','loop_demand_kg_s':'heat_transport__primary_loop__mdot_loop','loop_capacity_margin_kg_s':'heat_transport__primary_loop__capacity_margin','peak_field_T':'magnet__peak_field_calc__B_peak','current_operating_fraction':'magnet__conductor_current__operating_fraction_reference','current_margin_fraction':'magnet__conductor_current__margin_fraction','fit_margin_x_m':'magnet__wp_fit__margin_x','fit_margin_y_m':'magnet__wp_fit__margin_y','burn_auxiliary_MW':'plasma__sustain__p_aux_required','LCOE_dollars_MWh':'lcoe_calc__lcoe'}.items()}
    quantities['loop_capacity_kg_s']=inputs[P+'heat_transport__mdot_loop_ref']
    summaries.append({'proposal_id':pid,'family':props[pid]['family'],'base_id':props[pid]['base_id'],'candidate_id':row['candidate_id'],'inputs':row['inputs'],'account':account,'quantities':quantities,'conditional_requirements':needed,'divertor_predicate_satisfied':rawpass,'divertor_account_supported_pass':rawpass and valid and active,'all20_satisfied':all(v=='satisfied' for v in row['verdicts'].values()),'violated':[catalog[cid]['source_local_identity'] for cid,v in row['verdicts'].items() if v!='satisfied']})
summaryby={r['proposal_id']:r for r in summaries}
pairs=[]
for row in summaries:
    bid=row['base_id']
    if not bid or bid==row['proposal_id']: continue
    base=summaryby[bid]
    pairs.append({'proposal_id':row['proposal_id'],'base_id':bid,'family':row['family'],'account_deltas':{k:v-base['account'][k] for k,v in row['account'].items() if isinstance(v,(int,float))},'quantity_deltas':{k:v-base['quantities'][k] for k,v in row['quantities'].items()},'before_violated':base['violated'],'after_violated':row['violated']})
transport=[r for r in pairs if r['family']=='source-profile']
radiation=[r for r in pairs if r['family']=='radiation-sensitivity']
unchanged=['plant_heat_MW','target_cost','loop_demand_kg_s','loop_capacity_margin_kg_s','peak_field_T','current_operating_fraction','fit_margin_x_m','fit_margin_y_m','LCOE_dollars_MWh']
pair_checks={'profile_and_radiation_held_outputs_unchanged':all(close(r['quantity_deltas'][k],0.) for r in transport+radiation for k in unchanged),'paired_low_profile_increases_uncaptured_load':all(r['account_deltas']['p_nonrad_uncaptured']>0 for r in transport),'profile_keeps_incoming_nonradiated_power':all(close(r['account_deltas']['p_target_nonrad'],0.) for r in transport)}
def aggregate(rows):
    return {'cases':len(rows),'divertor_predicate_passes':sum(r['divertor_predicate_satisfied'] for r in rows),'divertor_account_supported_passes':sum(r['divertor_account_supported_pass'] for r in rows),'invalid_accounts':sum(r['account']['power_account_valid']!=1 for r in rows),'all20_passes':sum(r['all20_satisfied'] for r in rows),'violations':dict(Counter(v for r in rows for v in r['violated']))}
analysis={'scope':'27 selected diagnostic points; no optimized design, global infeasibility, geometry law or engineering qualification.','unique_cases':len(summaries),'overall':aggregate(summaries),'families':{f:aggregate([r for r in summaries if r['family']==f]) for f in sorted({r['family'] for r in summaries})},'predicate_outcomes':{cid:{'source_local_identity':e['source_local_identity'],'counts':dict(Counter(r['verdicts'][cid] for r in native))} for cid,e in catalog.items()},'cases':summaries,'paired_consequences':pairs,'pair_checks':pair_checks,'entering_preservation':preserved,'conservation_max_abs_MW':max(abs(r['account']['conservation_residual']) for r in summaries),'limitations':['Source profile at held target arrangement is transport sensitivity, not demonstrated design improvement.','Radius shadow is a conditional peak, never average; no identified physical wetted area or separate peaking.','Total radiative target deposition and first-wall destination map absent.','Wall interception accommodation, breeding, target cooling/support/manufacturing and target/control costs unqualified.','Inherited joint-sizing bounded negative remains its original finding; selected sensitivity cases do not regrade it.']}
write('analysis.json',analysis)
flat=[]
for row in summaries:
    flat.append({'proposal_id':row['proposal_id'],'family':row['family'],**row['account'],**row['quantities'],'divertor_predicate_satisfied':row['divertor_predicate_satisfied'],'divertor_account_supported_pass':row['divertor_account_supported_pass'],'all20_satisfied':row['all20_satisfied'],'violated':';'.join(row['violated']),**{k:v for k,v in row['conditional_requirements'].items() if k!='interpretation'}})
with (R/'case-summary.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(flat[0]),lineterminator='\n');writer.writeheader();writer.writerows(flat)
print('All-point scalar/predicate checks',scalar_count,predicate_count,'failures',len(failures))
print('Aggregate',analysis['overall'],'entering preserved',preserved,'paired checks',pair_checks)
assert not failures and preserved and all(pair_checks.values()), 'Review retained discrepancies'
