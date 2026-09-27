"""Read verified stored Round 3 native results; perform reporting arithmetic only.

No native evaluation, oracle scouting or physical postprocessing occurs here.
Run only after coordinator release, with the all-point verification artifact.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
import math
import os
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR','/tmp/exchanger-r3-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
RECORD=ROOT/'exploration/exchanger_architecture/thermal_requirements/studies/20260927-exchanger-thermal-comparison'
P='aries_integrated_plant__'
BRANCHES=('he','pbli','divertor')
ARCH={0:'series',1:'network'}
COLORS={'series':'#286b8b','network':'#d4762c'}
COMPONENTS=('capital','om','tritium','deuterium','consumables','imports','supply','replacement','other_overhaul','terminal','salvage')
NOMINAL_LOAD=1835.4512830147435
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                     'axes.spines.right':False,'svg.fonttype':'none','figure.dpi':130,
                     'savefig.dpi':220,'svg.hashsalt':'exchanger-r3-reporting',
                     'axes.grid':True,'grid.alpha':.18})


def read(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    if not rows:
        path.write_text('no_rows\n')
        return
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with path.open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields)
        writer.writeheader()
        writer.writerows({k:json.dumps(v,sort_keys=True) if isinstance(v,(dict,list)) else v for k,v in row.items()} for row in rows)


def validate_release(record,verification):
    native=read(record/'results/cases.json')
    proof=read(verification)
    if proof.get('outcome')!='pass' or proof.get('verdicts_rederived') is not True:
        raise ValueError('Reporting requires independently rederived, passing all-point verification.')
    stores=proof['stores']
    if len(stores)!=1 or Path(stores[0]['path']).resolve()!=Path(native['store']).resolve():
        raise ValueError('Verification must describe the same native store.')
    ids={row['candidate_id'] for row in native['cases']}
    if set(stores[0]['sampling']['sampled_case_ids'])!=ids or stores[0]['cases_total']!=len(native['cases']):
        raise ValueError('Verification does not cover every exported native candidate.')
    proposals=read(record/'proposed-points.json')
    lookup={row['case']:row for row in proposals['cases']}
    if set(lookup)!={row['case'] for row in native['cases']}:
        raise ValueError('Proposal/native label coverage differs.')
    catalog=read(record/'results/constraint_catalog.json')
    predicate_ids=set(catalog)
    labels=defaultdict(set)
    for row in proposals['cases']:
        labels[row['case']].add(row['classification'])
    for alias in proposals.get('aliases',[]):
        labels[alias['case']].add(alias['label'])
    for row in native['cases']:
        if row['inputs']!=lookup[row['case']]['point'] or row.get('full_numeric_map_equal') is not True:
            raise ValueError('Stored inputs differ from declared full map: '+row['case'])
        if row['state']!='completed' or set(row['verdicts'])!=predicate_ids:
            raise ValueError('Incomplete native execution/predicate catalog: '+row['case'])
    return native,lookup,labels,predicate_ids


def extract(case,proposal,labels):
    inp,out=case['inputs'],case['outputs']
    meta=proposal['metadata']
    get=lambda owner,field:out[P+owner+'__evaluate__'+field]
    val=lambda owner,field:inp[P+owner+'__'+field]
    failed=[k for k,v in case['verdicts'].items() if v!='satisfied']
    row={'case':case['case'],'candidate_id':case['candidate_id'],'scan_id':proposal['scan_id'],
         'parent_scan_id':meta.get('parent_scan_id'),'labels':sorted(labels),'scenario':meta['scenario'],
         'offer':meta['offer'],'architecture':ARCH[int(val('heat_exchangers','network_mode'))],
         'load_MW':get('source','selected_power'),'flow_kg_s':val('cycle','selected_flow'),
         'split':val('heat_exchangers','pbli_split_fraction'),'state':case['state'],
         'failed_checks':failed,'predicate_count':len(case['verdicts']),
         'native_pass':not failed and get('plant_ledger','net_electric')>0,
         'executable_fingerprint':case['executable_fingerprint'],'evidence_digest':case['evidence_digest'],
         'net_MW':get('plant_ledger','net_electric'),'unmet_MW':get('heat_exchangers','unmet_heat'),
         'turbine_inlet_K':get('heat_exchangers','turbine_temperature'),
         'heater_inlet_K':get('heat_exchangers','heater_inlet'),'availability':val('cost_schedule','availability'),
         'pressure_loss':val('pressure_loss','loss_fraction'),'control_mode':val('heat_exchangers','control_mode'),
         'tritium_price_USD2004_kg':val('fuel_inventory','tritium_price'),
         'annual_energy_MWh':get('lifecycle_accounts','annual_energy'),
         'lcoe_USD2004_MWh':get('lifecycle_accounts','lcoe_sum'),
         'annual_cost_USD2004':get('lifecycle_accounts','annual_capital')+get('lifecycle_accounts','noncapital_annual'),
         'overnight_USD2004':get('cost_ledger','overnight'),
         'direct_USD2004':get('cost_ledger','direct')}
    for component in COMPONENTS:
        row['lcoe_'+component]=get('lifecycle_accounts',component+'_lcoe')
    row['lcoe_recurring_fuel']=sum(row['lcoe_'+c] for c in ('tritium','deuterium','supply'))
    row['lcoe_nonfuel']=row['lcoe_USD2004_MWh']-row['lcoe_recurring_fuel']
    assert math.isclose(sum(row['lcoe_'+c] for c in COMPONENTS),row['lcoe_USD2004_MWh'],abs_tol=1e-7,rel_tol=1e-12)
    assert math.isclose(row['annual_cost_USD2004'],row['lcoe_USD2004_MWh']*row['annual_energy_MWh'],abs_tol=1e-5,rel_tol=1e-12)
    assert math.isclose(row['lcoe_USD2004_MWh'],get('lifecycle_accounts','pv_total_cost')/get('lifecycle_accounts','pv_energy'),rel_tol=1e-12)
    assert math.isclose(row['annual_energy_MWh'],8760*row['availability']*row['net_MW'],rel_tol=1e-12)
    for b in BRANCHES:
        for field in ('required_hot','hot','hot_bound_margin','required_hot_margin','hx_return','mixed_return',
                      'return_residual','return_residual_magnitude','active_flow','bypass_fraction','control_margin',
                      'transferred','unmet','state_defined','secondary_in','secondary_out',
                      'hot_terminal_difference','cold_terminal_difference','hot_approach_margin','cold_approach_margin'):
            row[b+'_'+field]=get('heat_exchangers',b+'_'+field)
        for field in ('required_return','limit','hot_approach','cold_approach','max_bypass','flow','cp'):
            row[b+'_input_'+field]=val('heat_exchangers',b+'_'+field)
        for field in ('selected_area','assumed_u','price_factor'):
            row[b+'_input_'+field]=val(b+'_hx',field)
        for field in ('capital','quantity_ratio','extrapolated','purchased_quantity'):
            row[b+'_purchase_'+field]=out[P+b+'_hx__purchase__'+field]
    row['hx_purchase_USD2004']=sum(row[b+'_purchase_capital'] for b in BRANCHES)
    row['minimum_terminal_K']=min(row[b+'_'+end+'_terminal_difference'] for b in BRANCHES for end in ('hot','cold'))
    row['maximum_return_error_K']=max(row[b+'_return_residual_magnitude'] for b in BRANCHES)
    row['minimum_hot_cap_margin_K']=min(row[b+'_hot_bound_margin'] for b in BRANCHES)
    row['maximum_bypass_fraction']=max(row[b+'_bypass_fraction'] for b in BRANCHES)
    return row


def group_key(row):
    return row['scenario'],row['load_MW'],row['offer'],row['architecture']


def select(rows,oracle_selection):
    groups=defaultdict(list)
    for row in rows:
        groups[group_key(row)].append(row)
    old={(s['scenario'],s['load'],s['offer'],ARCH[s['mode']]):s for s in oracle_selection['selected']}
    selected=[];receipts=[];ties=[]
    # All declared operating searches plus executed financial endpoints. Extra
    # source-cap/original-inventory controls do not invent an optimized group.
    keys=set(old)|{key for key in groups if key[0] in ('zero-tritium','price-half','price-double','linear-area-price')}
    for key in sorted(keys):
        pool=groups.get(key,[]);passing=[r for r in pool if r['native_pass']]
        chosen=min(passing,key=lambda r:(-r['net_MW'],r['case'])) if passing else None
        prior=old.get(key,{})
        prior_case=next((r for r in pool if r['scan_id']==prior.get('best_scan_id')),None)
        receipt={'scenario':key[0],'load_MW':key[1],'offer':key[2],'architecture':key[3],
                 'native_candidates':len(pool),'native_passes':len(passing),
                 'oracle_best_scan_id':prior.get('best_scan_id'),'oracle_best_case':prior_case['case'] if prior_case else None,
                 'selected_case':chosen['case'] if chosen else None,'selected_id':chosen['candidate_id'] if chosen else None,
                 'selected_scan_id':chosen['scan_id'] if chosen else None,
                 'selection_changed':chosen is not None and prior_case is not None and chosen['case']!=prior_case['case'],
                 'native_improvement_MW':chosen['net_MW']-prior_case['net_MW'] if chosen and prior_case else None,
                 'selection_rule':'highest native net among all stored complete passes; deterministic case-label tie-break'}
        receipts.append(receipt)
        if chosen:
            selected.append(chosen)
            ties.extend(dict(r,selected_representative=r['case']==chosen['case']) for r in passing if chosen['net_MW']-r['net_MW']<=.001)
    return selected,receipts,ties


def pair(series,network,kind='matched'):
    assert series['native_pass'] and network['native_pass']
    assert series['load_MW']==network['load_MW'] and series['offer']==network['offer']
    assert series['availability']==network['availability']
    assert series['tritium_price_USD2004_kg']==network['tritium_price_USD2004_kg']
    ps,pn=series['net_MW'],network['net_MW']
    a_s,a_n=series['annual_cost_USD2004'],network['annual_cost_USD2004']
    ratio=pn/ps
    return {'kind':kind,'scenario':network['scenario'],'series_scenario':series['scenario'],
            'load_MW':series['load_MW'],'offer':series['offer'],
            'series_case':series['case'],'network_case':network['case'],
            'series_id':series['candidate_id'],'network_id':network['candidate_id'],
            'series_pass':True,'network_pass':True,'series_flow_kg_s':series['flow_kg_s'],
            'network_flow_kg_s':network['flow_kg_s'],'network_split':network['split'],
            'series_net_MW':ps,'network_net_MW':pn,'delta_net_MW':pn-ps,
            'series_lcoe':series['lcoe_USD2004_MWh'],'network_lcoe':network['lcoe_USD2004_MWh'],
            'delta_lcoe':network['lcoe_USD2004_MWh']-series['lcoe_USD2004_MWh'],
            'series_nonfuel_lcoe':series['lcoe_nonfuel'],'network_nonfuel_lcoe':network['lcoe_nonfuel'],
            'delta_nonfuel_lcoe':network['lcoe_nonfuel']-series['lcoe_nonfuel'],
            'series_annual_cost_USD2004':a_s,'network_annual_cost_USD2004':a_n,
            'annual_budget_Bs0_pS0_pN0_USD2004':ratio*a_s-a_n,
            'power_budget_Bs0_Bn0_pS0_MW':pn-a_n*ps/a_s,
            'common_cost_coefficient_pS0_pN0':ratio-1.,
            'budget_slope_pN_USD2004_y_per_MW':-a_s/ps,
            'availability':series['availability'],'series_loss':series['pressure_loss'],
            'network_loss':network['pressure_loss']}


def comparisons(selected):
    groups=defaultdict(dict)
    for r in selected:
        groups[(r['scenario'],r['load_MW'],r['offer'])][r['architecture']]=r
    pairs=[];unpaired=[]
    for key,g in sorted(groups.items()):
        if set(g)=={'series','network'}:
            pairs.append(pair(g['series'],g['network']))
        else:
            r=next(iter(g.values()))
            unpaired.append({'scenario':key[0],'load_MW':key[1],'offer':key[2],
                             'passing_architecture':r['architecture'],'case':r['case'],
                             'candidate_id':r['candidate_id'],'net_MW':r['net_MW'],
                             'lcoe_USD2004_MWh':r['lcoe_USD2004_MWh'],
                             'paired_allowance':'undefined; no passing native counterpart'})
    for key,g in sorted(groups.items()):
        if key[0].startswith('loss') and 'network' in g:
            baseline=groups.get(('main',key[1],key[2]),{}).get('series')
            if baseline:
                pairs.append(pair(baseline,g['network'],'differential-network-loss'))
    return pairs,unpaired


def financial_parent_receipts(rows,selected):
    by_scan={r['scan_id']:r for r in rows}
    main={group_key(r):r for r in selected if r['scenario']=='main'}
    receipts=[]
    for row in selected:
        if row['scenario'] not in ('zero-tritium','price-half','price-double','linear-area-price'):continue
        current=main.get(('main',row['load_MW'],row['offer'],row['architecture']))
        parent=by_scan.get(row['parent_scan_id'])
        receipts.append({'scenario':row['scenario'],'load_MW':row['load_MW'],'offer':row['offer'],
                         'architecture':row['architecture'],'financial_case':row['case'],
                         'financial_parent_scan_id':row['parent_scan_id'],
                         'financial_parent_case':parent['case'] if parent else None,
                         'native_main_selected_case':current['case'] if current else None,
                         'same_selected_parent':bool(current and parent and current['case']==parent['case']),
                         'main_improvement_since_parent_MW':current['net_MW']-parent['net_MW'] if current and parent else None,
                         'native_main_flow_kg_s':current['flow_kg_s'] if current else None,
                         'endpoint_flow_kg_s':row['flow_kg_s']})
    return receipts


def equal_flow(rows):
    groups=defaultdict(dict)
    for row in rows:
        if 'equal-flow-control' in row['labels']:
            groups[(row['load_MW'],row['offer'],row['flow_kg_s'])][row['architecture']]=row
    result=[]
    for (load,offer,flow),g in sorted(groups.items()):
        s,n=g.get('series'),g.get('network')
        result.append({'load_MW':load,'offer':offer,'common_flow_kg_s':flow,
                       'series_case':s['case'] if s else None,'network_case':n['case'] if n else None,
                       'series_id':s['candidate_id'] if s else None,'network_id':n['candidate_id'] if n else None,
                       'series_pass':s['native_pass'] if s else False,'network_pass':n['native_pass'] if n else False,
                       'delta_net_MW':n['net_MW']-s['net_MW'] if s and n else None,
                       'comparison_usable':bool(s and n and s['native_pass'] and n['native_pass'])})
    return result


def thermal_rows(selected):
    records=[]
    for row in selected:
        if row['scenario']!='main':continue
        for b in BRANCHES:
            r={k:row[k] for k in ('case','candidate_id','offer','architecture','load_MW','flow_kg_s','split','native_pass')}
            r['branch']=b
            r.update({k.removeprefix(b+'_'):v for k,v in row.items() if k.startswith(b+'_')})
            records.append(r)
    return records


def refinement_receipt(rows,selected,document):
    by_scan={r['scan_id']:r for r in rows}
    chosen={group_key(r):r for r in selected}
    result=[]
    for entry in document['selected']:
        key=(entry['scenario'],entry['load'],entry['offer'],ARCH[entry['mode']])
        final=chosen.get(key)
        record={k:entry.get(k) for k in ('load','offer','mode','scenario','best_scan_id','stability_pass','edge_passes',
                                       'flow_halving','split_halving','final_neighborhood_change','refinement')}
        record['native_selected_case']=final['case'] if final else None
        record['native_selected_id']=final['candidate_id'] if final else None
        record['stability_basis']='recorded independent-scout refinement; final cases use native acceptance'
        mapped=[]
        scan_ids={entry.get('best_scan_id')}
        for r in entry.get('refinement',[]):scan_ids.add(r['scan_id'])
        for k in ('before_scan_id','after_scan_id'):scan_ids.add(entry.get('flow_halving',{}).get(k))
        for scan_id in sorted(x for x in scan_ids if x is not None):
            native=by_scan.get(scan_id)
            mapped.append({'scan_id':scan_id,'native_case':native['case'] if native else None,
                           'native_pass':native['native_pass'] if native else None,
                           'native_net_MW':native['net_MW'] if native else None})
        record['scan_to_native']=mapped
        if final:
            peers=[r for r in rows if group_key(r)==key and abs(r['split']-final['split'])<1e-12]
            lower=[r for r in peers if r['flow_kg_s']<final['flow_kg_s'] and not r['native_pass']]
            neighbor=max(lower,key=lambda r:r['flow_kg_s'],default=None)
            record['lower_native_failure_case']=neighbor['case'] if neighbor else None
            record['native_flow_bracket_kg_s']=final['flow_kg_s']-neighbor['flow_kg_s'] if neighbor else None
        result.append(record)
    return result


def break_even_coordinates(pairs):
    records=[]
    for p in pairs:
        if p['kind']!='matched' or p['scenario'] not in ('main','zero-tritium'):continue
        if abs(p['load_MW']-NOMINAL_LOAD)>1e-9:continue
        for common in (0.,10_000_000.):
            ps,pn=p['series_net_MW'],p['network_net_MW']
            a_s,a_n=p['series_annual_cost_USD2004'],p['network_annual_cost_USD2004']
            endpoint=pn-(a_n+common)*ps/(a_s+common)
            high=min(.9*pn,max(1.,1.1*abs(endpoint)))
            for j in range(41):
                power=high*j/40
                ratio=(pn-power)/ps
                budget=ratio*(a_s+common)-(a_n+common)
                assert pn-power>0 and ps>0
                records.append({'offer':p['offer'],'scenario':p['scenario'],'load_MW':p['load_MW'],
                    'series_case':p['series_case'],'network_case':p['network_case'],
                    'series_id':p['series_id'],'network_id':p['network_id'],'series_pass':True,'network_pass':True,
                    'common_annual_cost_USD2004':common,'series_extra_power_MW':0.,'network_extra_power_MW':power,
                    'allowed_differential_annual_cost_USD2004':budget,'common_cost_coefficient':ratio-1,
                    'series_adjusted_net_MW':ps,'network_adjusted_net_MW':pn-power,
                    'source':'derived reporting arithmetic from native parents; not an executed plant candidate'})
    return records


def save(fig,name,out):
    out.mkdir(parents=True,exist_ok=True)
    for extension in ('png','svg'):
        fig.savefig(out/(name+'.'+extension),bbox_inches='tight',facecolor='white',
                    metadata={'Date':None} if extension=='svg' else None)
    plt.close(fig)


def figures(selected,pairs,thermal,coordinates,root):
    main=[r for r in selected if r['scenario']=='main']
    fig,axes=plt.subplots(2,3,figsize=(13.7,7.5))
    for i,offer in enumerate(('A','B')):
        for arch,color in COLORS.items():
            rr=sorted((r for r in main if r['offer']==offer and r['architecture']==arch),key=lambda r:r['load_MW'])
            for ax,key in zip(axes[i],('flow_kg_s','net_MW','lcoe_USD2004_MWh')):
                ax.plot([r['load_MW'] for r in rr],[r[key] for r in rr],'o-',color=color,label=arch.capitalize(),lw=1.6)
        for ax,label in zip(axes[i],('Cycle flow (kg/s)','Net electricity (MW)','LCOE (USD2004/MWh)')):
            ax.set_ylabel(label);ax.set_xlabel('Supplied fusion source (MW)')
        axes[i,0].set_title('Offer '+offer+' · best passing tested operation',loc='left')
        axes[i,0].legend()
    fig.suptitle('Exchanger connections under explicit returns and 30 K terminal requirements',fontsize=15)
    fig.text(.07,.012,'Same offered inventory and assumed prices within each row. Native complete passes only; lines join tested source loads.\nConditional retained HX budgets; additional control/topology scope remains unpriced.',fontsize=9)
    fig.tight_layout(rect=(0,.08,1,.95));save(fig,'r3-main-performance',root)

    nominal=[r for r in thermal if abs(r['load_MW']-NOMINAL_LOAD)<1e-9]
    fig,axes=plt.subplots(1,2,figsize=(13,5))
    groups=sorted({(r['offer'],r['architecture']) for r in nominal})
    for i,(offer,arch) in enumerate(groups):
        rr=[r for r in nominal if r['offer']==offer and r['architecture']==arch]
        by={r['branch']:r for r in rr};xx=[j+(i-1.5)*.17 for j in range(6)]
        gaps=[by[b][end+'_terminal_difference'] for b in BRANCHES for end in ('hot','cold')]
        axes[0].plot(xx,gaps,'o',label=f'{offer} · {arch}',color=COLORS[arch],alpha=.65 if offer=='A' else 1.)
        axes[1].plot([j+(i-1.5)*.13 for j in range(3)],[by[b]['bypass_fraction'] for b in BRANCHES],
                     's',label=f'{offer} · {arch}',color=COLORS[arch],alpha=.65 if offer=='A' else 1.)
    axes[0].axhline(30,color='#a42e35',ls='--',lw=1,label='Required 30 K')
    axes[0].set_xticks(range(6),['He hot','He cold','PbLi hot','PbLi cold','Div hot','Div cold'],rotation=25)
    axes[0].set_ylabel('Actual terminal difference (K)');axes[0].set_title('Six local exchanger gaps')
    axes[1].set_xticks(range(3),['Blanket He','PbLi','Divertor']);axes[1].set_ylim(0,1)
    axes[1].set_ylabel('Primary flow bypass fraction');axes[1].set_title('Explicit controller operation')
    axes[0].legend(fontsize=8);axes[1].legend(fontsize=8)
    fig.suptitle(f'Passing operations at {NOMINAL_LOAD:.2f} MW source',fontsize=15)
    fig.text(.08,.01,'Cold gaps use active exchanger outlets before primary mixing. U is held constant as active flow changes.\nCSV includes actual/mixed returns, required returns, hot states/caps, active flows and parent native IDs.',fontsize=9)
    fig.tight_layout(rect=(0,.10,1,.93));save(fig,'r3-actual-thermal-states',root)

    fig,axes=plt.subplots(1,2,figsize=(12.5,5.2))
    for offer,ax in zip(('A','B'),axes):
        for scenario,color in (('main','#5d427c'),('zero-tritium','#27816d')):
            for common,style in ((0.,'-'),(10_000_000.,'--')):
                rr=[r for r in coordinates if r['offer']==offer and r['scenario']==scenario and r['common_annual_cost_USD2004']==common]
                if not rr:continue
                label=('Nominal fuel' if scenario=='main' else 'Zero tritium price')+f'; common ${common/1e6:g}M/y'
                ax.plot([r['network_extra_power_MW'] for r in rr],[r['allowed_differential_annual_cost_USD2004']/1e6 for r in rr],style,color=color,label=label)
        ax.axhline(0,color='#777',lw=.8);ax.set_title('Offer '+offer)
        ax.set_xlabel('Extra dissipative network electric demand (MW)')
        ax.set_ylabel('Allowed extra network annual cost (MUSD2004/y)');ax.legend(fontsize=8)
    fig.suptitle('Equal-LCOE boundary at the supplied N source',fontsize=15)
    fig.text(.08,.01,'Reporting arithmetic; both native parent cases pass. Common $0/$10M annual additions are illustrative slices.\nPower is external dissipation with no recovered-heat or pressure feedback. Positive adjusted net is required.',fontsize=9)
    fig.tight_layout(rect=(0,.10,1,.93));save(fig,'r3-break-even',root)

    rr=[p for p in pairs if p['offer']=='B' and abs(p['load_MW']-NOMINAL_LOAD)<1e-9 and p['scenario'] not in ('zero-tritium','price-half','price-double','linear-area-price')]
    if rr:
        fig,axes=plt.subplots(1,2,figsize=(12.5,max(5,.35*len(rr))))
        labels=[p['scenario']+(' · network loss only' if p['kind']=='differential-network-loss' else ' · common scenario') for p in rr]
        yy=list(range(len(rr)))
        for ax,key,label in zip(axes,('delta_net_MW','delta_lcoe'),('Network − series net (MW)','Network − series LCOE (USD2004/MWh)')):
            ax.barh(yy,[p[key] for p in rr],color=['#286b8b' if p['kind']=='matched' else '#d4762c' for p in rr])
            ax.axvline(0,c='#444',lw=.8);ax.set_yticks(yy,labels if ax is axes[0] else []);ax.invert_yaxis();ax.set_xlabel(label)
        fig.suptitle('Reoptimized sensitivity comparisons · offer B at supplied N',fontsize=15)
        fig.text(.12,.008,'Passing native pairs only. Common-loss pairs and network-loss versus baseline series are separate comparisons.\nMissing paired bars do not imply robustness; failed/unpaired scenarios remain in the data and reading.',fontsize=9)
        fig.tight_layout(rect=(0,.085,1,.95));save(fig,'r3-sensitivities',root)


def reading(summary,out):
    counts=summary['counts'];pairs=summary['pairs'];selected=summary['selected']
    lines=['# Round 3 results analysis','',
           '[AGENT] Executor-authored reading of verified stored native results. This is a conditional comparison under the recorded N-R return convention, six 30 K terminal requirements and explicit assumed exchanger offers.','',
           f"All {counts['native_cases']} exported cases completed and passed independent numerical verification. {counts['native_passes']} satisfy every native engineering predicate and positive net electricity; {counts['native_cases']-counts['native_passes']} fail at least one acceptance condition.",'',
           '## Main matched comparisons','',
           '| Source MW | Offer | Series / network flow kg/s | Series / network net MW | Network minus series LCOE, USD2004/MWh | Native parents |',
           '|---:|---|---:|---:|---:|---|']
    for p in pairs:
        if p['scenario']=='main' and p['kind']=='matched':
            lines.append(f"| {p['load_MW']:.3f} | {p['offer']} | {p['series_flow_kg_s']:.4f} / {p['network_flow_kg_s']:.4f} | {p['series_net_MW']:.3f} / {p['network_net_MW']:.3f} | {p['delta_lcoe']:.3f} | {p['series_case']} / {p['network_case']} |")
    lines+=['','Selection uses every stored native passing candidate in each declared search group. Oracle `best_scan_id` is retained as provenance, not treated as the final authority. The selection receipt lists replacements and their native improvement. A best tested operation is not a global optimum.','',
            '## Passing range and original inventory','']
    for r in summary['unpaired']:
        if r['scenario']=='main':lines.append(f"- Offer {r['offer']} at {r['load_MW']:.3f} MW has a tested {r['passing_architecture']}-only pass: {r['case']}, {r['net_MW']:.3f} MW net. A paired LCOE or allowance is undefined.")
    originals=[r for r in summary['cases'] if r['offer']=='original']
    lines.append(f"Original-inventory controls: {len(originals)} executed, {sum(r['native_pass'] for r in originals)} complete passes. The case ledger retains every failed predicate and actual thermal state.")
    equal=[r for r in summary['equal_flow'] if r['comparison_usable']]
    if equal:lines.append(f"At {len(equal)} passing equal-flow controls, the largest absolute network/series net difference is {max(abs(r['delta_net_MW']) for r in equal):.6g} MW. These controls separate access to lower passing flow from equal-flow cycle output.")
    lines+=['','## Actual thermal states and refinement','',
            'The thermal CSV records all six local gaps, actual hot/cap margins, active exchanger returns, mixed returns, exact return targets, residuals, active flows and bypass fractions for each selected main case. All selected cases satisfy the native contract. Constant U despite changing active flow remains an assumption.','',
            'The refinement receipt maps recorded scout stages to native cases where available, records final native failure brackets and preserves missing mappings. Refinement evidence that was calculated only by the independent scout is labelled separately from native selected-case evidence. See the receipt before interpreting printed digits as resolution.','',
            '## Economics and missing scope','',
            'Main offers retain 58.3257 million USD2004 per exchanger as an explicit assumed purchase budget. Smaller-area extrapolation flags remain visible. This is not a vendor quote. Existing broad piping/control budgets stay booked; coverage of new bypass/manifold/actuation scope is unresolved.','',
            'Nonfuel LCOE here removes recurring tritium, deuterium and supply-service charges; it retains capital, including initial fuel inventory. The executed zero-tritium-price endpoint reprices both initial tritium stock and annual purchases. It is reported separately.','',
            'For passing parents, adjusted LCOE is (A_i+B_i)/[8760 availability (P_i−p_i)]. The allowed network addition is B_N,max = (E_N/E_S)(A_S+B_S)−A_N. If a common unknown annual addition B_c applies to both, the additional network allowance has coefficient E_N/E_S−1 multiplying B_c; common costs do not cancel when electricity differs.','',
            'The curves show external dissipative power with no thermal recovery or pressure feedback and retain positive adjusted net. Pump and pressure-loss sensitivities use native coupled re-evaluation. Curve coordinates and parent case IDs are stored in the break-even CSV.','',
            '## Sensitivity scope','',
            'Operating sensitivities cover offer B at the supplied N load only. Common loss changes are paired separately from a perturbed network versus baseline-loss series. Financial endpoints use the native executed operations recorded for each endpoint; they do not silently reprice a different unexecuted operating choice. Neither a finite sensitivity bracket nor passing hardware temperatures establish procurement, fuel-supply or hydraulic qualification.','',
            '## Evidence','',
            f"Native record: `{summary['record']}`. Source cases SHA256 `{summary['source_sha256']}`. All-point verification SHA256 `{summary['verification_sha256']}`.",'',
            'Data and traceability: [complete native case ledger](r3-data/cases.csv), [selections](r3-data/selections.csv), [paired economics](r3-data/pairs.csv), [actual thermal states](r3-data/thermal.csv), [refinement](r3-data/refinement.csv), [equal-flow controls](r3-data/equal-flow.csv), [break-even coordinates](r3-data/break-even.csv), and [complete reporting JSON](r3-data/reporting.json).','']
    out.write_text('\n'.join(lines))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record',type=Path,default=RECORD)
    parser.add_argument('--verification',type=Path,required=True)
    parser.add_argument('--out',type=Path,default=HERE)
    args=parser.parse_args()
    native,proposals,labels,catalog=validate_release(args.record,args.verification)
    rows=[extract(c,proposals[c['case']],labels[c['case']]) for c in native['cases']]
    oracle_selection=read(args.record/'oracle-selection.json')
    selected,selections,ties=select(rows,oracle_selection)
    pairs,unpaired=comparisons(selected)
    financial_parents=financial_parent_receipts(rows,selected)
    equal=equal_flow(rows);thermal=thermal_rows(selected)
    refinement=refinement_receipt(rows,selected,oracle_selection)
    coordinates=break_even_coordinates(pairs)
    data=args.out/'r3-data';data.mkdir(parents=True,exist_ok=True)
    tables={'cases':rows,'selections':selections,'best-ties':ties,'pairs':pairs,'unpaired':unpaired,
            'equal-flow':equal,'thermal':thermal,'refinement':refinement,'break-even':coordinates,
            'sensitivities':[r for r in selected if r['scenario']!='main'],
            'sensitivity-coverage':[r for r in selections if r['scenario']!='main'],
            'financial-parents':financial_parents}
    for name,values in tables.items():write_csv(data/(name+'.csv'),values)
    summary={'record':str(args.record.relative_to(ROOT)),
             'source_sha256':sha(args.record/'results/cases.json'),'verification_sha256':sha(args.verification),
             'renderer_sha256':sha(__file__),'counts':{'native_cases':len(rows),'native_passes':sum(r['native_pass'] for r in rows),'predicates_per_case':len(catalog)},
             'cases':rows,'selected':selected,'selection_receipts':selections,'pairs':pairs,'unpaired':unpaired,
             'equal_flow':equal,'thermal':thermal,'refinement':refinement,'break_even':coordinates,
             'financial_parent_receipts':financial_parents,
             'currency':'USD2004','nonfuel_definition':'total minus recurring tritium/deuterium/supply-service; initial fuel capital retained',
             'author_role':'executor reporting; not independent review'}
    (data/'reporting.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
    figures(selected,pairs,thermal,coordinates,args.out/'figures')
    reading(summary,args.out/'r3-results-analysis.md')
    print(json.dumps(summary['counts'],indent=2))


if __name__=='__main__':
    main()
