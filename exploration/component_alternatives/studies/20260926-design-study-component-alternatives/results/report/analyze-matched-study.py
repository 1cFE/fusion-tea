"""Read retained native cases, summarize accounting and render publication figures.

No model/oracle imports or evaluations. Values come from results/cases.json;
selection metadata and duplicate aliases come from the same study record.
Run with .codex-test/run python <this-file> [--record PATH] [--out-dir PATH].
"""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,math,os
os.environ.setdefault("MPLCONFIGDIR","/tmp/wi096-matplotlib")
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
P='component_alternatives__plant__'
ROOT=Path(__file__).resolve().parents[5]
DEFAULT=ROOT/'exploration/component_alternatives/studies/20260926-design-study-component-alternatives'
LEDGER=('gross_electric electrical_load net_electric total_rejected unremoved_heat energy_residual conversion_energy_residual capital_total recurring_base annual_service annual_makeup machine_replacement_pv bundle_replacement_pv conversion_replacement_pv replacement_pv annuity_factor annual_energy discounted_energy accounted_pv corrected_pv cost_per_net_MWh economic_defined').split()
C={'steam':'#b65a26','fixed':'#967351','gas':'#176f91','failed':'#be4048','no_root':'#9ca3af'}
def read(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def channel(row,owner,field,calc='evaluate'):return float(row['outputs'][P+owner+'__'+calc+'__'+field])
def inp(row,key):return float(row['inputs'][P+key])
def close(a,b,absolute=1e-5):assert math.isclose(a,b,rel_tol=1e-9,abs_tol=absolute),(a,b)
def ledger(row,branch):
 d={k:channel(row,branch+'_ledger',k) for k in LEDGER}
 d['capital_accounts']={str(i):channel(row,branch+'_ledger','capital_'+str(i)) for i in range(1,11)}
 d['controller_capital']=inp(row,branch+'_ledger__controller_capital')
 d['service_pv']=d['annual_service']*d['annuity_factor'];d['makeup_pv']=d['annual_makeup']*d['annuity_factor']
 d['cost_components_per_MWh']={k:d[v]/d['discounted_energy'] for k,v in [('Capital','capital_total'),('Service','service_pv'),('Makeup','makeup_pv'),('Replacement','replacement_pv')]}
 close(sum(d['capital_accounts'].values())+d['controller_capital'],d['capital_total'])
 close(d['capital_total']+d['replacement_pv']+d['service_pv']+d['makeup_pv'],d['accounted_pv'])
 if d['economic_defined']:
  close(d['corrected_pv']/d['discounted_energy'],d['cost_per_net_MWh'])
 else:assert d['cost_per_net_MWh']==0
 return d

def summarize(record):
 raw=read(record/'results/cases.json')['cases'];proposals=read(record/'proposed-points.json')['cases'];window=read(record/'window.json')
 assert len(raw)==len(proposals)==window['native_case_count']==498
 native={r['case']:r for r in raw};assert len(native)==498 and set(native)=={r['case'] for r in proposals}
 diagnostics=read(record/'results/verification-diagnostics.json');diagnostic_cases={r['case']:r for r in diagnostics['cases']}
 assert set(diagnostic_cases)==set(native)
 roles={r['case']:{r['role']} for r in proposals};aliases=collections.defaultdict(list)
 for a in window['duplicate_aliases']:
  aliases[a['native_case']].append(a['alias']);roles[a['native_case']].add(a['role'])
 index={**native,**{a['alias']:native[a['native_case']] for a in window['duplicate_aliases']}}
 rows=[]
 for ordinal,row in enumerate(raw):
  diag=diagnostic_cases[row['case']];assert diag['candidate_id']==row['candidate_id']
  assert row['state']=='completed'
  failed=sorted(k for k,v in row['verdicts'].items() if v!='satisfied')
  assert len(row['verdicts'])==84
  cooler={c:channel(row,c,'failure_code') for c in ('water_ic1','water_ic2','water_pre')}
  no_root=[k for k,v in cooler.items() if v==2];pinch=[k for k,v in cooler.items() if v==1]
  status='pass' if not failed else 'cooler_no_root' if no_root else 'cooler_invalid' if pinch else 'equipment_or_coupling_insufficient'
  r={'case':row['case'],'candidate_id':row['candidate_id'],'state':row['state'],'roles':sorted(roles[row['case']]),'aliases':aliases[row['case']],'plot_index':ordinal,'status':status,'all_checks_pass':not failed,'verification_status':'numerical_mismatch' if diag['numeric_mismatches'] else 'diagnostic_agreement_not_released','numerical_verification_mismatch':bool(diag['numeric_mismatches']),'numeric_mismatches':diag['numeric_mismatches'],'predicate_mismatches':diag['predicate_mismatches'],'failed_constraints':failed,'cooler_no_root':no_root,'cooler_invalid':pinch,'source_MW':inp(row,'blanket_source__q_source'),'delivered_heat_MW':channel(row,'primary_loop','q_ihx'),'source_hot_K':channel(row,'primary_loop','T_out'),'source_return_K':channel(row,'primary_loop','T_comp_in'),'gas_flow_kg_s':inp(row,'cycle__selected_flow'),'stage_ratio':inp(row,'compressor_1__selected_ratio'),'cooler_UA':[inp(row,c+'__ua') for c in ('water_ic1','water_ic2','water_pre')],'recuperator_UA':inp(row,'recuperator_hardware__ua'),'steam_circuits':inp(row,'steam_transport__n_loops'),'salt_pumps_per_circuit':inp(row,'steam_transport__salt_pumps_per_circuit'),'salt_pump_design_kg_s':inp(row,'steam_transport__selected_salt_design_flow_kg_s'),'gas':ledger(row,'gas'),'steam':ledger(row,'steam')}
  for branch in ('steam','gas'):
   d=r[branch];d['net_fraction_of_delivered_heat']=d['net_electric']/r['delivered_heat_MW']
   if not failed:close(r['delivered_heat_MW'],d['net_electric']+d['total_rejected'])
  r['energy_decomposition']={
   'steam':{'cycle_pumps_MW':channel(row,'steam_cycle','p_cycle_pumps_MW'),'salt_pumps_MW':channel(row,'steam_transport','salt_electric_MW'),'water_pumps_MW':channel(row,'steam_water','p_cooling_pump_electric_MW'),'controller_MW':inp(row,'steam_boundary__actuation')},
   'gas':{'compressor_shaft_MW':channel(row,'electrical','compressor_demand'),'turbine_shaft_MW':channel(row,'turbine','shaft_produced'),'net_shaft_MW':channel(row,'electrical','net_shaft'),'generator_loss_MW':channel(row,'electrical','generator_loss'),'shaft_import_MW':channel(row,'electrical','shaft_import'),'water_pumps_MW':sum(channel(row,c,'pump_electric') for c in ('water_ic1','water_ic2','water_pre'))+channel(row,'gas_loss_water','p_cooling_pump_electric_MW'),'controller_MW':inp(row,'gas_boundary__actuation')},
   'upstream_circulation_electric_excluded_MW':channel(row,'primary_loop','p_elec')}
  close(sum(r['energy_decomposition']['steam'].values()),r['steam']['electrical_load'])
  gd=r['energy_decomposition']['gas'];close(gd['shaft_import_MW']+gd['water_pumps_MW']+gd['controller_MW'],r['gas']['electrical_load'])
  rows.append(r)
 byid={r['case']:r for r in rows};resolve=lambda name:byid[index[name]['case']]
 anchors=[]
 ga=read(record/'gas-anchor-selection.json')['anchors'];sa=read(record/'matched-anchor-selection.json')['anchors']
 for g,s in zip(ga,sa):
  assert g['source_MW']==s['source_MW'];q=g['source_MW'];fixed=resolve(g['case']);selected=resolve(s['case'])
  assert fixed['all_checks_pass'] and selected['all_checks_pass']
  for field in ('source_MW','delivered_heat_MW','source_hot_K','source_return_K'):close(fixed[field],selected[field])
  gc=[r for r in rows if 'gas_catalog' in r['roles'] and r['source_MW']==q and r['all_checks_pass']]
  sc=[r for r in rows if 'steam_connector_catalog' in r['roles'] and r['source_MW']==q and r['all_checks_pass']]
  close(fixed['gas']['cost_per_net_MWh'],min(r['gas']['cost_per_net_MWh'] for r in gc))
  close(selected['steam']['cost_per_net_MWh'],min(r['steam']['cost_per_net_MWh'] for r in sc))
  E_S,E_B=selected['steam']['discounted_energy'],selected['gas']['discounted_energy'];K_S,K_B=selected['steam']['accounted_pv'],selected['gas']['accounted_pv']
  slope=E_S/E_B;intercept=slope*K_B-K_S;denom=1/E_S-1/E_B;delta=K_S/E_S-K_B/E_B
  anchors.append({'source_MW':q,'gas_case':fixed['case'],'fixed_steam_case':fixed['case'],'selected_steam_case':selected['case'],'gas_passing_catalog_count':len(gc),'steam_passing_catalog_count':len(sc),'fixed':fixed,'selected':selected,'steam_minus_gas_net_MW':selected['steam']['net_electric']-selected['gas']['net_electric'],'steam_minus_gas_cost_per_MWh':delta,'cost_gap_exceeds_5_USD_materiality':abs(delta)>5,'fixed_connector_cost_penalty_per_MWh':fixed['steam']['cost_per_net_MWh']-selected['steam']['cost_per_net_MWh'],'frontier':{'equation':'X_steam = slope * X_gas + intercept_USD2025','slope':slope,'intercept_USD2025':intercept,'common_source_difference_coefficient_per_USD':denom,'common_source_break_even_PV_USD2025':-delta/denom}})
 counts={}
 for role in sorted({k for r in rows for k in r['roles']}):
  rr=[r for r in rows if role in r['roles']];counts[role]=dict(collections.Counter(r['status'] for r in rr))|{'total':len(rr)}
 sensitivity=[r for r in rows if 'sensitivity' in r['roles'] or 'adverse_controller_offer' in r['roles']]
 for r in sensitivity:
  a=next(a for a in anchors if a['source_MW']==r['source_MW']);r['steam_minus_gas_cost_per_MWh']=r['steam']['cost_per_net_MWh']-r['gas']['cost_per_net_MWh']
  r['steam_minus_gas_net_MW']=r['steam']['net_electric']-r['gas']['net_electric']
  r['delta_cost_gap_from_anchor']=r['steam_minus_gas_cost_per_MWh']-a['steam_minus_gas_cost_per_MWh']
  r['within_cost_materiality']=abs(r['steam_minus_gas_cost_per_MWh'])<=5
  if 'common-source-pv' in r['case']:
   C0=inp(native[r['case']],'steam_ledger__common_source_pv');close(C0,inp(native[r['case']],'gas_ledger__common_source_pv'))
   r['common_source_PV_USD2025']=C0;close(r['steam_minus_gas_cost_per_MWh'],a['steam_minus_gas_cost_per_MWh']+C0*a['frontier']['common_source_difference_coefficient_per_USD'])
 sources=['results/verification-diagnostics.json','results/cases.json','window.json','proposed-points.json','gas-anchor-selection.json','matched-anchor-selection.json']
 summary={'authority':'UNRELEASED NATIVE DIAGNOSTICS. Verification blocked by c0206 numerical disagreement; no model/oracle evaluation in this analysis' ,'verification_status':'blocked','status_semantics':'pass means stored native constraints only; independent study verification remains blocked' ,'record':str(record.relative_to(ROOT)),'source_hashes':{s:digest(record/s) for s in sources},'native_unique_cases':len(rows),'duplicate_aliases':window['duplicate_aliases'],'counts':counts,'overall_status':dict(collections.Counter(r['status'] for r in rows)),'verification_diagnostics':{'numeric_mismatch_cases':[r['case'] for r in rows if r['numerical_verification_mismatch']],'native_passing_numeric_mismatch_cases':[r['case'] for r in rows if r['numerical_verification_mismatch'] and r['all_checks_pass']],'predicate_mismatch_cases':[r['case'] for r in rows if r['predicate_mismatches']]},'failed_predicate_counts':dict(collections.Counter(k for r in rows for k in r['failed_constraints'])),'anchors':anchors,'sensitivities':sensitivity,'materiality':{'power_MW':5,'cost_USD2025_per_net_MWh':5},'limits':'Finite tested offers, conditional pressure-service/off-design/quote assumptions; supplied steam cycle versus tested gas, not equal optimization or whole-plant LCOE.'}
 return summary,rows

def style():
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','axes.grid':True,'grid.alpha':.2,'svg.fonttype':'none','savefig.facecolor':'white'})
def save(fig,out,name):
 fig.savefig(out/(name+'.svg'),bbox_inches='tight');fig.savefig(out/(name+'.png'),dpi=190,bbox_inches='tight');plt.close(fig)

def figures(summary,rows,out):
 style();anchors=summary['anchors'];qs=[a['source_MW'] for a in anchors]
 fig=plt.figure(figsize=(15,11),layout='constrained');grid=fig.add_gridspec(3,3,height_ratios=[1.15,1,.65]);ax=fig.add_subplot(grid[0,:2])
 for branch,kind,label,color,ls,marker in [('steam','fixed','Steam · fixed 14-circuit connector',C['fixed'],'--','s'),('steam','selected','Steam · least-cost passing connector',C['steam'],'-','o'),('gas','selected','Brayton · least-cost tested offer',C['gas'],'-','D')]:
  yy=[a[kind][branch]['net_electric'] for a in anchors];ax.plot(qs,yy,color=color,linestyle=ls,marker=marker,label=label,linewidth=2)
  if kind=='selected':
   for x,y in zip(qs,yy):ax.annotate(f'{y:.1f}',(x,y),xytext=(0,8 if branch=='steam' else -17),textcoords='offset points',ha='center',color=color)
 ax.set(title='Net electricity at matched source conditions',xlabel='Selected reactor heat input (MW)',ylabel='Conversion-subsystem net electricity (MW)',xticks=qs);ax.legend(loc='center left',fontsize=9);ax.set_ylim(460,1220);ax.text(.02,.96,'Steam net curves coincide; connector costs differ.',transform=ax.transAxes,va='top',fontsize=9,color=C['steam'])
 ax=fig.add_subplot(grid[0,2]);a=anchors[1];base=a['selected'];xx=np.arange(2);bottom=np.zeros(2)
 for field,label,color in [('net_electric','Net electricity','#287f9d'),('electrical_load','Included electric loads','#edbd5b'),('total_rejected','Rejected heat','#b9c3cd')]:
  vals=[base[b][field] for b in ('steam','gas')]
  # Gross-to-net waterfall is displayed separately from rejection: heat split uses net + rejection only.
  if field=='electrical_load':continue
  ax.bar(xx,vals,bottom=bottom,label=label,color=color);bottom+=vals
 ax.set(title='Delivered heat disposition · 2800 MW source',xticks=xx,xticklabels=['Steam','Brayton'],ylabel='MW');ax.legend(fontsize=8)
 for x,b in zip(xx,('steam','gas')):ax.text(x,base[b]['net_electric']/2,f"Net {base[b]['net_electric']:.0f}\nLoads {base[b]['electrical_load']:.1f}",ha='center',va='center',color='white',fontsize=9)
 offers=[(25,25,20),(25,25,25),(25,25,40),(30,30,50),(40,40,60)]
 for i,q in enumerate(qs):
  ax=fig.add_subplot(grid[1,i]);rr=[r for r in rows if 'gas_catalog' in r['roles'] and r['source_MW']==q]
  for r in rr:
   offset=(offers.index(tuple(r['cooler_UA']))-2)*.022;x=r['stage_ratio']+offset;y=r['gas_flow_kg_s'];status=r['status'];color=C['gas'] if status=='pass' else C['no_root'] if status.startswith('cooler') else C['failed'];marker='o' if status=='pass' else 'x' if status.startswith('cooler') else '+'
   ax.scatter(x,y,c=color,marker=marker,s=28,linewidths=1.3)
   if r['numerical_verification_mismatch']:ax.scatter(x,y,facecolors='none',edgecolors='#5c224f',marker='D',s=72,linewidths=1.2)
  cc=collections.Counter(r['status'] for r in rr);ax.set(title=f"{q:g} MW · {cc['pass']}/125 offers pass",xlabel='Chosen stage ratio · small offset distinguishes offers',ylabel='Chosen gas flow (kg/s)',xticks=[1.2,1.35,1.5,1.65,1.8],yticks=[1500,1750,2000,2250,2500]);ax.set_xlim(1.13,1.87)
 for i,q in enumerate(qs):
  ax=fig.add_subplot(grid[2,i]);rr=[r for r in rows if 'steam_connector_catalog' in r['roles'] and r['source_MW']==q]
  for r in rr:
   offset=-.13 if r['salt_pump_design_kg_s']==225 else .13
   ax.scatter(r['steam_circuits']+offset,r['salt_pumps_per_circuit'],c=C['gas'] if r['all_checks_pass'] else C['failed'],marker='o' if r['all_checks_pass'] else '+',s=35,linewidths=1.3)
  ax.set(title=f"Steam connector · {sum(r['all_checks_pass'] for r in rr)}/24 pass",xlabel='Installed IHX circuits · offset: 225 / 250 kg/s pump',ylabel='Salt pumps per circuit',xticks=[10,11,12,14],yticks=[2,3,4]);ax.set_ylim(1.7,4.3)
 fig.legend(handles=[Line2D([],[],marker='o',color=C['gas'],ls='',label='Native checks pass'),Line2D([],[],marker='+',color=C['failed'],ls='',label='Equipment or coupling check fails'),Line2D([],[],marker='x',color=C['no_root'],ls='',label='Cooler has no admissible root'),Line2D([],[],marker='D',markerfacecolor='none',color='#5c224f',ls='',label='Numerical mismatch')],loc='outside lower center',ncol=4)
 fig.suptitle('VERIFICATION BLOCKED · unreleased native diagnostics\nSelected steam offer versus tested Brayton offers',fontsize=16)
 save(fig,out,'matched-output')
 fig,(ax,bx)=plt.subplots(1,2,figsize=(14,5.5),layout='constrained')
 for branch,kind,label,color,ls in [('steam','fixed','Steam · fixed 14 circuits',C['fixed'],'--'),('steam','selected','Steam · selected connector',C['steam'],'-'),('gas','selected','Brayton · selected offer',C['gas'],'-')]:
  yy=[a[kind][branch]['cost_per_net_MWh'] for a in anchors];ax.plot(qs,yy,'o',color=color,linestyle=ls,label=label,linewidth=2)
  if kind=='selected':
   for x,y in zip(qs,yy):ax.annotate(f'{y:.2f}',(x,y),xytext=(0,8 if branch=='steam' else -15),textcoords='offset points',ha='center',color=color)
 ax.set(title='Nominal hypothetical price scenario',xlabel='Selected reactor heat input (MW)',ylabel='USD2025 per net MWh',xticks=qs);ax.legend(fontsize=9);ax.set_ylim(24,48)
 xx=np.arange(6);bottom=np.zeros(6);rr=[a['selected'][b] for a in anchors for b in ('steam','gas')]
 for label,color in [('Capital','#527e98'),('Service','#adc6d2'),('Makeup','#ead4aa'),('Replacement','#d69058')]:
  v=[r['cost_components_per_MWh'][label] for r in rr];bx.bar(xx,v,bottom=bottom,label=label,color=color);bottom+=v
 bx.set(title='Present-value cost / discounted net energy',ylabel='USD2025 per net MWh',xticks=xx,xticklabels=['S\n2500','B\n2500','S\n2800','B\n2800','S\n3000','B\n3000']);bx.legend(fontsize=8,ncol=2)
 fig.suptitle('VERIFICATION BLOCKED · unreleased native diagnostics\nConversion-subsystem costs · upstream equipment and fuel excluded',fontsize=15)
 fig.supxlabel('S: supplied steam cycle with selected connector; B: tested Brayton offer. Quotes and installed scope remain conditional.',fontsize=10)
 save(fig,out,'matched-cost')
 fig,axes=plt.subplots(1,3,figsize=(16,6.7),layout='constrained');sen=summary['sensitivities']
 for ax,kind,title,labels in [(axes[0],'eta','Efficiency assumptions', [('gas-eta-0.03','Gas −3 pp'),('gas-eta+0.03','Gas +3 pp'),('steam-eta-0.03','Steam −3 pp'),('steam-eta+0.03','Steam +3 pp'),('both-eta-0.03','Both −3 pp'),('both-eta+0.03','Both +3 pp')]),(axes[1],'quote','Quote / recurring-cost assumptions',[('gas-quote-x0.5','Gas quote ×0.5'),('gas-quote-x1.5','Gas quote ×1.5'),('steam-quote-x0.5','Steam quote ×0.5'),('steam-quote-x1.5','Steam quote ×1.5'),('recurring-x0.5','Recurring ×0.5'),('recurring-x1.5','Recurring ×1.5'),('controller-gas','Gas bypass 500 (fails)'),('controller-steam','Steam bypass 500 (passes)')])]:
  for i,q in enumerate(qs):
   vals=[]
   for suffix,label in labels:
    name=f'controller-q{q:g}-{suffix.removeprefix("controller-")}-500' if suffix.startswith('controller-') else f'sensitivity-q{q:g}-{suffix}'
    r=next(r for r in sen if r['case']==name);vals.append(r['steam_minus_gas_cost_per_MWh']);ax.scatter(vals[-1],labels.index((suffix,label))+(i-1)*.19,marker='o' if r['all_checks_pass'] else 'x',s=35,color=['#b65a26','#407d88','#713f81'][i])
    if r['numerical_verification_mismatch']:ax.scatter(vals[-1],labels.index((suffix,label))+(i-1)*.19,facecolors='none',edgecolors='#111',marker='D',s=100,linewidths=1.5)
  ax.axvspan(-5,5,color='#e7e7e7',zorder=-2);ax.axvline(0,color='#666',lw=.8);ax.set(title=title,yticks=range(len(labels)),yticklabels=[v for _,v in labels],xlabel='Steam minus Brayton (USD2025/net MWh)');ax.invert_yaxis()
 ax=axes[2]
 for i,a in enumerate(anchors):
  q=a['source_MW'];rr=[r for r in sen if r['source_MW']==q and 'common_source_PV_USD2025' in r];xx=[0]+[r['common_source_PV_USD2025']/1e9 for r in rr];yy=[a['steam_minus_gas_cost_per_MWh']]+[r['steam_minus_gas_cost_per_MWh'] for r in rr];ax.plot(xx,yy,'o-',label=f'{q:g} MW',color=['#b65a26','#407d88','#713f81'][i])
 ax.axhspan(-5,5,color='#e7e7e7',zorder=-2);ax.axhline(0,color='#666',lw=.8);ax.set(title='Same source-service PV charge',xlabel='Added common PV charge (billion USD2025)',ylabel='Steam minus Brayton (USD2025/net MWh)');ax.legend(fontsize=9)
 fig.suptitle('VERIFICATION BLOCKED · unreleased native diagnostics\nRanking depends on conditional prices and performance',fontsize=16);fig.supxlabel('Positive: steam costs more. ×: failed native checks; ◇: numerical mismatch. Gray band: predeclared ±5 USD/net MWh materiality. No fuel price is inferred.',fontsize=10)
 save(fig,out,'matched-sensitivity')

def main():
 p=argparse.ArgumentParser();p.add_argument('--record',type=Path,default=DEFAULT);p.add_argument('--out-dir',type=Path,default=Path(__file__).resolve().parent);args=p.parse_args();out=args.out_dir;out.mkdir(parents=True,exist_ok=True)
 summary,rows=summarize(args.record)
 (out/'matched-study-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 (out/'plot-data.json').write_text(json.dumps({'record':summary['record'],'source_hashes':summary['source_hashes'],'cases':rows,'aliases':summary['duplicate_aliases']},indent=2)+'\n')
 fields=['case','candidate_id','state','roles','aliases','status','all_checks_pass','verification_status','numerical_verification_mismatch','numeric_mismatches','predicate_mismatches','failed_constraints','cooler_no_root','cooler_invalid','source_MW','delivered_heat_MW','gas_flow_kg_s','stage_ratio','cooler_UA','steam_circuits','salt_pumps_per_circuit','salt_pump_design_kg_s','steam_net_MW','gas_net_MW','steam_cost_per_MWh','gas_cost_per_MWh']
 for branch in ('steam','gas'):
  fields += [branch+'_'+f for f in LEDGER+['service_pv','makeup_pv']]
 with (out/'plot-data.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for r in rows:
   rr={k:r.get(k) for k in fields};rr.update({branch+'_'+f:r[branch][f] for branch in ('steam','gas') for f in LEDGER+['service_pv','makeup_pv']});rr.update(steam_net_MW=r['steam']['net_electric'],gas_net_MW=r['gas']['net_electric'],steam_cost_per_MWh=r['steam']['cost_per_net_MWh'],gas_cost_per_MWh=r['gas']['cost_per_net_MWh']);w.writerow({k:json.dumps(v) if isinstance(v,(list,dict)) else v for k,v in rr.items()})
 figures(summary,rows,out)
 print(json.dumps({'counts':summary['counts'],'anchors':[{k:v for k,v in a.items() if k not in ('selected','fixed')} for a in summary['anchors']]},indent=2))
if __name__=='__main__':main()
