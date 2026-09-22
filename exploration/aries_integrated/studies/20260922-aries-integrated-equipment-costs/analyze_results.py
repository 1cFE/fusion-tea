"""Summarize stored native results; performs no plant or cost-model calculations."""
from __future__ import annotations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
P='aries_integrated_plant__'


def channel(owner,name,calc='evaluate'):
    return P+owner+'__'+calc+'__'+name


CHANNELS={
 'net_MW':channel('plant_ledger','net_electric'),
 'gross_MW':channel('plant_ledger','gross_electric'),
 'accepted_MW':channel('heat_exchangers','accepted_heat'),
 'unmet_MW':channel('heat_exchangers','unmet_heat'),
 'fuel_exhaust_atoms_s':channel('fuel','exhaust_rate'),
 'pump_MW':channel('deposition','pump_electric'),
 'direct_USD2004':channel('cost_ledger','direct'),
 'overnight_USD2004':channel('cost_ledger','overnight'),
 'annual_operating_USD2004':channel('cost_ledger','annual_operating'),
 'annual_replacement_reserve_USD2004':channel('cost_ledger','annual_replacement_reserve'),
 'lifetime_replacement_USD2004':channel('cost_ledger','lifetime_replacement'),
 'annual_external_T_kg':channel('fuel_inventory','annual_external','annual'),
 'annual_T_USD2004':channel('fuel_inventory','annual_cost','annual'),
 'replacement_events':channel('replacement','event_count'),
}


def analyze():
    read=lambda name:json.loads((HERE/name).read_text())
    stored=read('results/cases.json')['cases']
    proposals={x['case']:x for x in read('proposed-points.json')['cases']}
    if {x['case'] for x in stored}!=set(proposals):raise ValueError('stored/proposed case sets differ')
    native={x['case']:x for x in stored}
    baseline=native['nominal-calculated']
    def metrics(row):return {name:row['outputs'][key] for name,key in CHANNELS.items()}
    base=metrics(baseline)
    purchase_keys=[k for k in baseline['outputs'] if '__purchase__' in k and k.endswith(('__capital','__cost','__amount'))]
    rows=[]
    for name,row in native.items():
        proposal=proposals[name]
        if row['inputs']!=proposal['point']:raise ValueError('stored input map differs: '+name)
        numbers=metrics(row)
        differences={k:{'baseline':baseline['outputs'][k],'case':row['outputs'][k]} for k in purchase_keys if row['outputs'][k]!=baseline['outputs'][k]}
        selected_changes={k:{'baseline':baseline['inputs'][k],'case':v} for k,v in row['inputs'].items() if v!=baseline['inputs'][k]}
        if proposal['arm'] in ('thermal','demand') and differences:
            raise ValueError('fixed-purchase evidence violated: '+name)
        if proposal['arm'] in ('thermal','demand') and numbers['overnight_USD2004']!=base['overnight_USD2004']:
            raise ValueError('upfront total changed with fixed purchases: '+name)
        rows.append({'case':name,'family':proposal['arm'],'metrics':numbers,
                     'delta_net_MW':numbers['net_MW']-base['net_MW'],
                     'changed_inputs':selected_changes,'changed_purchase_accounts':differences,
                     'violated_constraints':[cid for cid,status in row['verdicts'].items() if status=='violated'],
                     'other_statuses':{cid:status for cid,status in row['verdicts'].items() if status not in ('satisfied','violated')},
                     'verdicts':row['verdicts']})
    by_name={x['case']:x for x in rows}
    thermal=[]
    for axis in read('axis-plan.json')['axes']:
        if axis['role'] in ('purchased','demand'):continue
        endpoints=[by_name[axis['axis']+'-'+side] for side in ('low','high')]
        thermal.append({'axis':axis['axis'],'units':axis['units'],'values':axis['values'],
                        'low':endpoints[0]['metrics'],'high':endpoints[1]['metrics'],
                        'max_abs_delta_net_MW':max(abs(x['delta_net_MW']) for x in endpoints),
                        'violations':{x['case']:x['violated_constraints'] for x in endpoints},
                        'missing_response':axis['missing_response']})
    # Compare finite declared perturbations, never infer intrinsic sensitivity or an optimum.
    thermal.sort(key=lambda x:x['max_abs_delta_net_MW'],reverse=True)
    constraints={}
    for cid in baseline['verdicts']:
        constraints[cid]={status:[r['case'] for r in rows if r['verdicts'][cid]==status]
                          for status in sorted({r['verdicts'][cid] for r in rows})}
    summary={'authorship':'executor analysis of stored native results only',
             'case_count':len(rows),'baseline':base,'purchase_channels_compared':purchase_keys,
             'fixed_purchase_case_count':sum(x['family'] in ('thermal','demand') for x in rows),
             'cases_with_violations':sum(bool(x['violated_constraints']) for x in rows),
             'all_scoped_checks_satisfied':sum(not x['violated_constraints'] and not x['other_statuses'] for x in rows),
             'thermal_finite_perturbation_order':thermal,'constraint_outcomes':constraints,'cases':rows,
             'limits':['Ordering compares declared engineered endpoint changes, not normalized uncertainty or global parameter importance.',
                       'No LCOE calculation, optimum, qualified machine/material/hydraulic/neutronic result or price uncertainty envelope.']}
    target=HERE/'results'/'analysis.json'
    if target.exists():raise ValueError('analysis exists; preserve or explicitly replace uncommitted analysis')
    target.write_text(json.dumps(summary,indent=2)+'\n')
    return summary


if __name__=='__main__':
    result=analyze()
    print(json.dumps({k:result[k] for k in ('case_count','fixed_purchase_case_count','cases_with_violations','all_scoped_checks_satisfied')}))
