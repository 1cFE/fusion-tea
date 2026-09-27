#!/usr/bin/env python
"""Render stored native exchanger-study evidence; no plant simulation or oracle substitution.

Run from the repository root through .codex-test/run. A full render requires an
executed cases.json and an explicit successful verification artifact. Tables retain
failed cases; only complete native passes enter economic selections. The 30 K
approach screen is supplementary and does not change native predicates.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
from collections import Counter

os.environ.setdefault('MPLCONFIGDIR', '/tmp/exchanger-architecture-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
P = 'aries_integrated_plant__'
COLORS = {'series': '#236b8e', 'network': '#d57930'}
STATUS = {'pass': ('#27816d', 'o'), 'heat removal': ('#c75146', 'x'),
          'equipment': ('#7957a1', 's'), 'heat + equipment': ('#b02f6b', 'X'),
          'other / undefined': ('#777777', '+')}
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.titlesize': 12, 'axes.labelsize': 10,
                     'svg.fonttype': 'none', 'figure.dpi': 130,
                     'svg.hashsalt': 'exchanger-architecture-report-v1',
                     'savefig.dpi': 220, 'axes.grid': True, 'grid.alpha': .18})


def read(path):
    return json.loads(path.read_text())


def save(fig, name, out):
    out.mkdir(parents=True, exist_ok=True)
    for ext in ('svg', 'png'):
        fig.savefig(out / f'{name}.{ext}', bbox_inches='tight', facecolor='white',
                    metadata={'Date':None} if ext=='svg' else None)
    plt.close(fig)


def diagram(out):
    fig, axes = plt.subplots(2, 1, figsize=(12, 6.1))
    def box(ax, x, y, label, width=1.7):
        ax.add_patch(FancyBboxPatch((x-width/2, y-.3), width, .6,
                    boxstyle='round,pad=.03', ec='#45616c', fc='#eef4f5', lw=1.1))
        ax.text(x, y, label, ha='center', va='center', fontsize=10)
    def arrow(ax, a, b):
        ax.annotate('', xy=b, xytext=a, arrowprops={'arrowstyle': '->', 'color': '#45616c', 'lw': 1.5})
    for ax in axes:
        ax.set_xlim(-.5, 11); ax.set_ylim(-1.2, 1.2); ax.axis('off')
    ax=axes[0]; ax.set_title('Series: the full cycle-helium stream visits all three exchangers', loc='left')
    for x, label in [(0.7,'Recuperator\noutlet'),(3,'Blanket He HX'),(5.3,'Divertor HX'),(7.6,'PbLi HX'),(9.9,'Turbine')]:box(ax,x,0,label)
    for x in (.7,3,5.3,7.6):arrow(ax,(x+.87,0),(x+1.43,0))
    ax=axes[1];ax.set_title('Network: heat in blanket He first, then divide and mix the cycle stream',loc='left')
    for x,y,label in [(.7,0,'Recuperator\noutlet'),(3,0,'Blanket He HX'),(6,.65,'PbLi HX'),(6,-.65,'Divertor HX'),(9.9,0,'Turbine')]:box(ax,x,y,label)
    arrow(ax,(1.57,0),(2.13,0));arrow(ax,(3.87,0),(4.4,0))
    for y,label in [(.65,'s × flow'),(-.65,'(1−s) × flow')]:
        ax.plot([4.4,4.4,5.1],[0,y,y],color='#45616c');arrow(ax,(4.6,y),(5.13,y))
        ax.text(5,y+(.38 if y>0 else -.48),label,fontsize=9,ha='center')
        ax.plot([6.87,8.2,8.2],[y,y,0],color='#45616c')
    arrow(ax,(8.2,0),(9.03,0));ax.text(8.2,-.28,'ideal mixing',ha='center',fontsize=9)
    fig.text(.08,.012,'Separate primary He, PbLi and divertor streams supply each exchanger. Supplied split; no branch hydraulic balance.\nBoth layouts use the same selected exchangers. Primary return requirements and layout-specific hardware remain unqualified.',fontsize=10)
    fig.subplots_adjust(hspace=.48,bottom=.18,top=.91)
    save(fig,'connections',out)


CHANNELS = {'fusion_MW': 'source__evaluate__selected_power',
 'turbine_MW':'turbine__evaluate__shaft_produced',
 'net_MW':'plant_ledger__evaluate__net_electric','gross_MW':'plant_ledger__evaluate__gross_electric',
 'compressor_MW':'plant_ledger__evaluate__compressor_demand', 'auxiliary_MW':'plant_ledger__evaluate__auxiliary_electric',
 'pump_MW':'plant_ledger__evaluate__primary_pump_electric','heating_MW':'plant_ledger__evaluate__heating_electric',
 'rejection_MW':'plant_ledger__evaluate__cycle_rejection','accepted_MW':'heat_exchangers__evaluate__accepted_heat',
 'unmet_MW':'heat_exchangers__evaluate__unmet_heat','plant_residual_MW':'plant_ledger__evaluate__plant_residual',
 'cycle_residual_MW':'plant_ledger__evaluate__cycle_residual','branch_residual_MW':'plant_ledger__evaluate__branch_residual',
 'electrical_residual_MW':'plant_ledger__evaluate__electrical_residual',
 'direct_USD':'cost_ledger__evaluate__direct','overnight_USD':'cost_ledger__evaluate__overnight',
 'financed_USD':'lifecycle_accounts__evaluate__financed_capital','annual_energy_MWh':'lifecycle_accounts__evaluate__annual_energy',
 'lcoe_USD_MWh':'lifecycle_accounts__evaluate__lcoe_sum','annualized_capital_USD':'lifecycle_accounts__evaluate__annual_capital',
 'annualized_noncapital_USD':'lifecycle_accounts__evaluate__noncapital_annual',
 'external_tritium_kg_y':'fuel_inventory__annual__annual_external',
 'turbine_inlet_K':'heat_exchangers__evaluate__turbine_temperature','heater_inlet_K':'heat_exchangers__evaluate__heater_inlet'}
for branch in ('he','pbli','divertor'):
    for field in ('transferred','unmet','hot','return','hot_terminal_difference','cold_terminal_difference','secondary_in','secondary_out','state_defined'):
        CHANNELS[f'{branch}_{field}'] = f'heat_exchangers__evaluate__{branch}_{field}'
for field in ('capital','om','tritium','deuterium','consumables','imports','supply','replacement','other_overhaul','terminal','salvage'):
    CHANNELS[f'lcoe_{field}'] = f'lifecycle_accounts__evaluate__{field}_lcoe'
for field in ('magnet','breeding','deposition','hydraulics','materials','machine_map'):
    CHANNELS[f'supported_{field}'] = f'plant_ledger__evaluate__supported_{field}'
for field in ('generator_loss','motor_loss','heating_loss','pump_loss','dissipated_auxiliary','fuel_electric','cryo_electric','control_electric','other_electric_demand'):
    CHANNELS[field+'_MW'] = f'plant_ledger__evaluate__{field}'


def extract(c, meta):
    inp,out=c['inputs'],c.get('outputs',{})
    val=lambda key:inp.get(P+key)
    failed=[k for k,v in c.get('verdicts',{}).items() if v!='satisfied']
    passed=c['state']=='completed' and len(c.get('verdicts',{}))==14 and not failed
    heat=any('heat_removal' in x for x in failed);equip=any('capacity_ok' in x for x in failed)
    status='pass' if passed else ('heat + equipment' if heat and equip else 'heat removal' if heat else 'equipment' if equip else 'other / undefined')
    r={'case':c['case'],'candidate_id':c['candidate_id'],'group':meta.get('classification','unknown'),
       'scenario':meta.get('metadata',{}).get('scenario','baseline'), 'state':c['state'],'native_pass':passed,
       'sensitivity_level':meta.get('metadata',{}).get('level'),
       'failure_class':status,'failed_checks':';'.join(failed),'predicate_count':len(c.get('verdicts',{})),
       'architecture':'series' if val('heat_exchangers__network_mode')==0 else 'network',
       'flow_kg_s':val('cycle__selected_flow'),'split':val('heat_exchangers__pbli_split_fraction'),
       'availability':val('cost_schedule__availability'),'source_mode':val('source__producer_mode'),
       'supplied_fusion_MW':val('source__reference_fusion_mw'),
       'tritium_price_USD_kg':val('fuel_inventory__tritium_price'),
       'pressure_loss':val('pressure_loss__loss_fraction'),
       'evidence_digest':c.get('evidence_digest'),'executable_fingerprint':c.get('executable_fingerprint'),
       'primary_return_qualified':False,'scientifically_qualified':False}
    r['temperature_diagnostics_independently_verified']=False
    for key,value in inp.items():
        if key.startswith(P) and any(s in key for s in ('selected_rating','selected_area','selected_flow_capacity','assumed_u','pump_mode','fixed_power','price_factor','selected_tritium_kg','annual_recovery_kg','discount_rate','plant_years','selected_ratio')):
            r['input_'+key.removeprefix(P)]=value
    r.update({k:out.get(P+v) for k,v in CHANNELS.items()})
    approach=[r[b+'_'+side+'_terminal_difference'] for b in ('he','pbli','divertor') for side in ('hot','cold')]
    r['min_terminal_approach_K']=min(approach) if all(x is not None for x in approach) else None
    r['approach30_pass']=r['min_terminal_approach_K'] is not None and r['min_terminal_approach_K']>=30 and all(r[b+'_state_defined']==1 for b in ('he','pbli','divertor'))
    if r['lcoe_USD_MWh'] is not None:
        r['lcoe_fuel']=r['lcoe_tritium']+r['lcoe_deuterium']+r['lcoe_supply']
        r['lcoe_nonfuel']=r['lcoe_USD_MWh']-r['lcoe_fuel']
        r['annualized_cost_USD']=r['annualized_capital_USD']+r['annualized_noncapital_USD']
        r['annualized_fuel_USD']=r['lcoe_fuel']*r['annual_energy_MWh']
        r['annualized_nonfuel_USD']=r['annualized_cost_USD']-r['annualized_fuel_USD']
        assert abs(sum(r['lcoe_'+f] for f in ('capital','om','tritium','deuterium','consumables','imports','supply','replacement','other_overhaul','terminal','salvage'))-r['lcoe_USD_MWh'])<1e-6
    for key,value in out.items():
        if key.startswith(P) and key.endswith(('__capital','__cost','__amount','__purchased_quantity')) and '__purchase__' in key:
            r['purchase_'+key.removeprefix(P)]=value
        if key.startswith(P) and key.endswith('__margin'):
            r['margin_'+key.removeprefix(P)]=value
    return r


def write_csv(path, rows):
    if not rows: return
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)


def paired_row(s,n):
    assert s['native_pass'] and n['native_pass'] and s['fusion_MW']==n['fusion_MW']
    assert s['availability']==n['availability'] and s['tritium_price_USD_kg']==n['tritium_price_USD_kg']
    h=8760*s['availability']
    return {'fusion_MW':s['fusion_MW'],'series_case':s['case'],'network_case':n['case'],
        'series_id':s['candidate_id'],'network_id':n['candidate_id'],
        'series_flow':s['flow_kg_s'],'network_flow':n['flow_kg_s'],'network_split':n['split'],
        'series_loss':s['pressure_loss'],'network_loss':n['pressure_loss'],
        'series_net':s['net_MW'],'network_net':n['net_MW'],'delta_net':n['net_MW']-s['net_MW'],
        'series_lcoe':s['lcoe_USD_MWh'],'network_lcoe':n['lcoe_USD_MWh'],
        'delta_lcoe':n['lcoe_USD_MWh']-s['lcoe_USD_MWh'],
        'delta_nonfuel_lcoe':n['lcoe_nonfuel']-s['lcoe_nonfuel'],
        'annual_budget_USD':s['lcoe_USD_MWh']*h*n['net_MW']-n['annualized_cost_USD'],
        'power_budget_MW':n['net_MW']-n['annualized_cost_USD']/(h*s['lcoe_USD_MWh']),
        'budget_slope_USD_y_per_MW':-s['lcoe_USD_MWh']*h}


def select(rows):
    main=[r for r in rows if r['group']=='main']
    best=[];pairs=[]
    for load in sorted({r['fusion_MW'] for r in main if r['fusion_MW'] is not None}):
        chosen={}
        for arch in COLORS:
            pool=[r for r in main if r['fusion_MW']==load and r['architecture']==arch and r['native_pass']]
            if not pool:continue
            power=max(r['net_MW'] for r in pool)
            ties=sorted([r for r in pool if power-r['net_MW']<=.01],key=lambda r:(r['flow_kg_s'],r['split']))
            # Representative is the exact maximum, with deterministic IDs for exact ties.
            representative=min(ties,key=lambda r:(-r['net_MW'],r['case']))
            chosen[arch]=representative
            best.extend(dict(r,tied_case_ids=';'.join(t['candidate_id'] for t in ties),selected_representative=r is representative) for r in ties)
        if len(chosen)==2:
            pairs.append(paired_row(chosen['series'],chosen['network']))
    return main,best,pairs


def sensitivity_summary(rows):
    summary=[]
    groups=sorted({(r['scenario'],r['sensitivity_level'] or 0,r['fusion_MW']) for r in rows if r['group']=='sensitivity'})
    for scenario,level,load in groups:
        pool=[r for r in rows if r['group']=='sensitivity' and r['scenario']==scenario and (r['sensitivity_level'] or 0)==level and r['fusion_MW']==load]
        result={'scenario':scenario,'level':level,'fusion_MW':load}
        for arch in COLORS:
            candidates=[r for r in pool if r['architecture']==arch]
            passing=[r for r in candidates if r['native_pass']]
            result[arch+'_cases']=len(candidates);result[arch+'_passes']=len(passing)
            if passing:
                chosen=min(passing,key=lambda r:(-r['net_MW'],r['case']))
                for key in ('case','candidate_id','flow_kg_s','split','net_MW','lcoe_USD_MWh','lcoe_nonfuel','min_terminal_approach_K'):
                    result[arch+'_'+key]=chosen[key]
        if result.get('series_passes') and result.get('network_passes'):
            result['delta_net_MW']=result['network_net_MW']-result['series_net_MW']
            result['delta_lcoe_USD_MWh']=result['network_lcoe_USD_MWh']-result['series_lcoe_USD_MWh']
        summary.append(result)
    return summary


def complete_ledger(record, rows):
    source=read(record/'candidate-ledger.json')
    native={r['case']:r for r in rows};result=[]
    for candidate in source['candidates']:
        canonical=candidate['canonical_case'];row=native.get(canonical)
        entry={'requested_case':candidate['case'],'canonical_case':canonical,
               'preparation_status':candidate['status'],
               'requested_classification':candidate['classification'],
               'requested_metadata':json.dumps(candidate.get('metadata',{}),sort_keys=True),
               'oracle_status':candidate.get('oracle_status'),
               'oracle_violations':json.dumps(candidate.get('oracle_violations',[]))}
        if row:entry.update(row)
        else:entry.update(candidate_id='',state='not executed',native_pass=False)
        result.append(entry)
    return result


def zero_price_pairs(rows):
    # Reuse the primary selector solely on the already executed zero-price subset.
    selected=[dict(r,group='main') for r in rows if r['group']=='sensitivity' and r['scenario']=='zero-tritium-price']
    return select(selected)[2] if selected else []


def asymmetric_loss_pairs(rows,best):
    result=[]
    for load in (2200.,2300.):
        series=next(r for r in best if r['fusion_MW']==load and r['architecture']=='series' and r['selected_representative'])
        pool=[r for r in rows if r['group']=='sensitivity' and r['fusion_MW']==load and r['architecture']=='network' and r['pressure_loss']==.08 and r['native_pass']]
        if pool:
            power=max(r['net_MW'] for r in pool);ties=[r for r in pool if power-r['net_MW']<=.01]
            network=min(ties,key=lambda r:(-r['net_MW'],r['case']))
            result.append(dict(paired_row(series,network),network_ties=';'.join(r['candidate_id'] for r in ties),
                               basis='existing native network 0.08 loss cases, best tested operations; series baseline 0.045'))
    return result


def explanation_cases(main, pairs):
    by_name={r['case']:r for r in main}
    result={}
    equal=[]
    for s in main:
        if s['architecture']!='series' or not s['native_pass']:continue
        for n in main:
            if n['architecture']=='network' and n['native_pass'] and n['fusion_MW']==s['fusion_MW'] and n['flow_kg_s']==s['flow_kg_s']:
                equal.append((abs(s['fusion_MW']-1835.4512830147435)+abs(s['flow_kg_s']-1400),abs(n['split']-.85),s,n))
    if equal:
        _,_,s,n=min(equal,key=lambda x:x[:2]);result['equal_flow_pair']={'series':s,'network':n}
    different=[p for p in pairs if p['series_flow']!=p['network_flow']]
    if different:
        maximum=max(p['delta_net'] for p in different)
        tied=[p for p in different if maximum-p['delta_net']<=.01]
        p=min(tied,key=lambda p:abs(p['fusion_MW']-2300))
        result['different_flow_pair']={'selection':'illustrative pair nearest 2300 MW among gains tied within 0.01 MW',
                                      'series':by_name[p['series_case']], 'network':by_name[p['network_case']]}
        result['series_at_network_flow']=[r for r in main if r['architecture']=='series' and r['fusion_MW']==p['fusion_MW'] and r['flow_kg_s']==p['network_flow']]
    return result


def break_even_coordinates(pairs,zero):
    informative=[p for p in pairs if abs(p['delta_net'])>=.01]
    picks=informative if informative else pairs[:1]
    xmax=min(max([p['power_budget_MW'] for p in picks]+[1])*1.35,
             .95*min(p['network_net'] for p in picks))
    curves=[(p,'nominal tritium price') for p in picks]
    if informative and zero:
        maximum=max(p['delta_net'] for p in informative)
        peak=min([p for p in informative if maximum-p['delta_net']<=.01],key=lambda p:abs(p['fusion_MW']-2300))
        z=next((p for p in zero if p['fusion_MW']==peak['fusion_MW']),None)
        if z:curves.append((z,'zero tritium price'))
    return [{'record_kind':'derived curve coordinate','fuel_scenario':scenario,
             'fusion_MW':p['fusion_MW'],'series_case':p['series_case'],'network_case':p['network_case'],
             'series_candidate_id':p['series_id'],'network_candidate_id':p['network_id'],
             'series_native_pass':True,'network_native_pass':True,
             'extra_power_MW':x,'remaining_network_net_MW':p['network_net']-x,
             'allowed_extra_annual_cost_USD':p['annual_budget_USD']+p['budget_slope_USD_y_per_MW']*x,
             'series_flow_kg_s':p['series_flow'],'network_flow_kg_s':p['network_flow']}
            for p,scenario in curves for x in (0,xmax)]


def plots(main,best,pairs,rows,out):
    loads=sorted({r['fusion_MW'] for r in main});li={p:i for i,p in enumerate(loads)}
    flows=sorted({r['flow_kg_s'] for r in main})
    fig,axes=plt.subplots(1,2,figsize=(12.8,7),gridspec_kw={'width_ratios':[1,1.3]})
    for arch,ax in zip(COLORS,axes):
        subset=[r for r in main if r['architecture']==arch]
        for status,(color,marker) in STATUS.items():
            rr=[r for r in subset if r['failure_class']==status]
            ax.scatter([li[r['fusion_MW']] for r in rr],
                [flows.index(r['flow_kg_s'])*10+(0 if arch=='series' else round(r['split']*100)-50)/5 for r in rr],
                c=color,marker=marker,s=28,lw=.85,zorder=3)
        ax.set_title('Series' if arch=='series' else 'Network: one mark per supplied split',pad=30)
        ax.set_xticks(range(len(loads)),[f'{p:.0f}' for p in loads],rotation=55,ha='right');ax.set_xlabel('Supplied fusion source (MW)')
        if arch=='series':ax.set_yticks([i*10 for i in range(len(flows))],[str(int(f)) for f in flows]);ax.set_ylabel('Cycle helium flow (kg/s)')
        else:
            ax.set_yticks([i*10+4 for i in range(len(flows))],[str(int(f)) for f in flows]);ax.set_ylabel('Flow groups (kg/s); split rises within group')
            ax.text(.02,1.01,'Split 0.50 → 0.90 bottom → top in each group',transform=ax.transAxes,fontsize=9)
    fig.legend(handles=[Line2D([],[],color=c,marker=m,ls='',label=s) for s,(c,m) in STATUS.items() if any(r['failure_class']==s for r in main)],loc='lower center',ncol=4,bbox_to_anchor=(.5,.045))
    fig.suptitle('Connection choice changes the passing operating range',fontsize=16,y=.98)
    fig.text(.07,.013,'Conditional downstream source; fixed selected hardware. Primary returns and hydraulics remain unqualified.\nNo primary native-pass point meets the separate 30 K source-specific approach screen (unverified temperature diagnostics).',fontsize=9)
    fig.tight_layout(rect=(0,.12,1,.93));save(fig,'operating-range',out)
    fig,axes=plt.subplots(1,3,figsize=(14.5,4.8))
    for arch,color in COLORS.items():
        rr=sorted([r for r in best if r['architecture']==arch and r['selected_representative']],key=lambda r:r['fusion_MW'])
        for ax,key in zip(axes[:2],('net_MW','lcoe_USD_MWh')):
            ax.plot([r['fusion_MW'] for r in rr],[r[key] for r in rr],marker='o',label=arch.capitalize(),c=color)
    axes[0].set_ylabel('Net electricity (MW)');axes[0].set_title('Highest passing tested net output');axes[0].legend()
    unmatched=[r for r in best if r['architecture']=='network' and r['selected_representative'] and r['fusion_MW'] not in {p['fusion_MW'] for p in pairs}]
    if unmatched:
        r=unmatched[-1]
        axes[0].annotate(f"Network alone passes\nat {r['fusion_MW']:.0f} MW source",xy=(r['fusion_MW'],r['net_MW']),xytext=(.38,.9),textcoords='axes fraction',fontsize=8.5,arrowprops={'arrowstyle':'->','color':'#666'},ha='center')
    axes[1].set_ylabel('Conditional LCOE (USD2004/MWh)');axes[1].set_title('Nominal tritium purchase assumption')
    axes[2].plot([p['fusion_MW'] for p in pairs],[p['delta_lcoe'] for p in pairs],'o-',label='Total',c='#543b73')
    axes[2].plot([p['fusion_MW'] for p in pairs],[p['delta_nonfuel_lcoe'] for p in pairs],'s--',label='Nonfuel',c='#27816d')
    zero=zero_price_pairs(rows)
    if zero:
        axes[2].plot([p['fusion_MW'] for p in zero],[p['delta_lcoe'] for p in zero],'^:',label='Zero tritium price',c='#b78319')
    axes[2].axhline(0,c='#777',lw=.8);axes[2].set_ylabel('Network minus series (USD2004/MWh)');axes[2].set_title('Common-load paired difference');axes[2].legend()
    for ax in axes:ax.set_xlabel('Supplied fusion source (MW)')
    fig.text(.06,.01,'Passing native cases only; lines join tested points. Zero price also reprices initial stock. Primary returns, practical approaches and hydraulics unqualified.',fontsize=9)
    fig.tight_layout(rect=(0,.06,1,1));save(fig,'paired-performance-cost',out)
    fig,ax=plt.subplots(figsize=(9,5.7))
    coordinates=break_even_coordinates(pairs,zero)
    for a,b in zip(coordinates[::2],coordinates[1::2]):
        is_zero=a['fuel_scenario']=='zero tritium price'
        label=(f"{a['fusion_MW']:.0f} MW source; zero tritium price" if is_zero else
               f"{a['fusion_MW']:.0f} MW source; {a['series_flow_kg_s']:.0f} → {a['network_flow_kg_s']:.0f} kg/s")
        kwargs={'ls':'--','c':'#222','lw':2} if is_zero else {}
        ax.plot([a['extra_power_MW'],b['extra_power_MW']],
                [a['allowed_extra_annual_cost_USD']/1e6,b['allowed_extra_annual_cost_USD']/1e6],label=label,**kwargs)
    ax.axhline(0,c='#777',lw=.8);ax.set_xlabel('Extra unrecovered network electric demand (MW)');ax.set_ylabel('Allowed extra equivalent annual cost (MUSD2004/year)')
    ax.set_title('Missing network cost and power: equal-LCOE boundary');ax.legend(fontsize=9)
    fig.text(.12,.01,'Below a line: network has lower conditional LCOE. Negative allowance: network already loses.\nAdded demand dissipates outside recovered source heat; no piping cost or hydraulic law is inferred.',fontsize=9)
    fig.tight_layout(rect=(0,.085,1,1));save(fig,'break-even',out)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record',type=Path,default=ROOT/'exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture')
    parser.add_argument('--verification',type=Path)
    parser.add_argument('--out',type=Path,default=HERE)
    parser.add_argument('--diagram-only',action='store_true')
    args=parser.parse_args();figures=args.out/'figures';diagram(figures)
    if args.diagram_only:return
    if args.verification is None or not args.verification.is_file():
        parser.error('Full reporting requires the completed verification artifact via --verification.')
    source=args.record/'results/cases.json';doc=read(source)
    verification=read(args.verification)
    if verification.get('outcome')!='pass' or verification.get('verdicts_rederived') is not True:
        raise ValueError('Native verification must pass with independently rederived predicates.')
    stores=verification['stores']
    if len(stores)!=1 or Path(stores[0]['path']).resolve()!=Path(doc['store']).resolve():
        raise ValueError('Verification and reporting must refer to the same native store.')
    expected_ids={c['candidate_id'] for c in doc['cases']}
    checked_ids=set(stores[0]['sampling']['sampled_case_ids'])
    if checked_ids!=expected_ids or stores[0]['cases_total']!=len(doc['cases']):
        raise ValueError('Verification must cover every exported case identity.')
    proposals=read(args.record/'proposed-points.json');meta={r['case']:r for r in proposals['cases']}
    rows=[extract(c,meta.get(c['case'],{})) for c in doc['cases']]
    mainrows,best,pairs=select(rows)
    if not mainrows:raise ValueError('No explicitly classified main cases; inspect preparation metadata.')
    write_csv(args.out/'results-cases.csv',rows);write_csv(args.out/'results-best-ties.csv',best);write_csv(args.out/'results-pairs.csv',pairs)
    ledger=complete_ledger(args.record,rows)
    named=[]
    for r in ledger:
        if r['candidate_id']:
            m=json.loads(r['requested_metadata'])
            named.append(dict(r,group=r['requested_classification'],scenario=m.get('scenario','baseline'),sensitivity_level=m.get('level')))
    sensitivities=sensitivity_summary(named);zero=zero_price_pairs(rows)
    write_csv(args.out/'results-candidate-ledger.csv',ledger)
    write_csv(args.out/'results-sensitivities.csv',sensitivities)
    write_csv(args.out/'results-zero-tritium-pairs.csv',zero)
    asymmetric=asymmetric_loss_pairs(rows,best)
    write_csv(args.out/'results-asymmetric-loss-pairs.csv',asymmetric)
    coordinates=break_even_coordinates(pairs,zero)
    write_csv(args.out/'results-break-even.csv',coordinates)
    summary={'native_cases_source':str(source),'native_cases_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
      'verification_source':str(args.verification),'verification_sha256':hashlib.sha256(args.verification.read_bytes()).hexdigest(),
      'native_counts':dict(Counter(r['failure_class'] for r in rows)),
      'main_counts':dict(Counter(r['failure_class'] for r in mainrows)),
      'main_approach30_pass_count':sum(r['native_pass'] and r['approach30_pass'] for r in mainrows),
      'pairs':pairs,'zero_tritium_pairs':zero,'sensitivities':sensitivities,'best_ties':best,'cases':rows,
      'asymmetric_loss_pairs':asymmetric,
      'break_even_coordinates':coordinates,
      'explanation_cases':explanation_cases(mainrows,pairs),
      'named_candidate_count':len(ledger),
      'primary_return_qualified':False,'temperature_diagnostics_independently_verified':False}
    (args.out/'results-reporting.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
    plots(mainrows,best,pairs,rows,figures)
    print(json.dumps({k:v for k,v in summary.items() if k.endswith('counts') or k.endswith('count')},indent=2))

if __name__=='__main__':main()
