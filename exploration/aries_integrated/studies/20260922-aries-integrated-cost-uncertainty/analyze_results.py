"""Reporting only: read native stored outputs; rank and difference, no plant arithmetic."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
P='aries_integrated_plant__'
def ch(owner,name,calc='evaluate'):return P+owner+'__'+calc+'__'+name
CHANNELS={
 'net_MW':ch('plant_ledger','net_electric'),'unmet_MW':ch('heat_exchangers','unmet_heat'),
 'direct_USD2004':ch('cost_ledger','direct'),'overnight_USD2004':ch('cost_ledger','overnight'),
 'annual_operating_USD2004':ch('cost_ledger','annual_operating'),'annual_export_MWh':ch('cost_ledger','annual_export_mwh'),
 'annual_T_USD2004':ch('fuel_inventory','annual_cost','annual'),'annual_external_T_kg':ch('fuel_inventory','annual_external','annual'),
 'annual_OM_USD2004':ch('annual_om','annual_om'),'annual_D_USD2004':ch('fuel_inventory','annual_fuel','deuterium'),
 'annual_import_USD2004':ch('cost_ledger','annual_import_cost'),
 'replacement_event_USD2004':ch('replacement','event_cost'),'replacement_events':ch('replacement','event_count'),
 'replacement_interval_years':ch('replacement','interval_years'),'replacement_last_year':ch('replacement','last_event_year'),
 'lifetime_replacement_USD2004':ch('cost_ledger','lifetime_replacement'),'annual_reserve_USD2004':ch('cost_ledger','annual_replacement_reserve'),
 'source_direct_USD2004':ch('cost_ledger','source_direct'),'source_inclusive_USD2004':ch('cost_ledger','source_inclusive'),
 'he_hx_USD2004':ch('he_hx','capital','purchase'),'he_UA_MW_K':ch('he_hx','ua')}

def main():
 cases=json.loads((R/'results/cases.json').read_text())['cases']; proposals={p['case']:p for p in json.loads((R/'proposed-points.json').read_text())['cases']}
 assert len(cases)==113 and {c['case'] for c in cases}==set(proposals)
 baseline=next(c for c in cases if c['case']=='nominal-calculated')
 metrics=lambda c:{n:c['outputs'][k] for n,k in CHANNELS.items()}
 base=metrics(baseline); rows=[]
 for c in cases:
  assert c['inputs']==proposals[c['case']]['point']
  m=metrics(c); rows.append({'case':c['case'],'family':proposals[c['case']]['arm'],'axis':proposals[c['case']].get('axis'),'metrics':m,'delta_from_baseline':{k:m[k]-v for k,v in base.items()},'violations':[k for k,v in c['verdicts'].items() if v!='satisfied']})
 lookup={r['case']:r for r in rows}
 conditional=[r for r in rows if r['case']=='nominal-calculated' or r['family']!='canonical']
 assert all(r['metrics']['net_MW']==base['net_MW'] for r in conditional)
 assert all(r['metrics']['annual_import_USD2004']==0 for r in conditional)
 support=[k for k in baseline['outputs'] if k.startswith(P+'plant_ledger__evaluate__supported_')]
 assert all(c['outputs'][k]==0 for c in cases for k in support)
 leaves=[{'channel':k,'owner':k.split('__')[1],'USD2004':v} for k,v in baseline['outputs'].items() if '__purchase__' in k and k.endswith(('__capital','__cost','__amount'))]
 leaves.sort(key=lambda x:-x['USD2004'])
 ranks={metric:sorted([{'case':r['case'],'delta':r['delta_from_baseline'][metric]} for r in rows if r['family']=='economic'],key=lambda x:-abs(x['delta'])) for metric in ('overnight_USD2004','annual_operating_USD2004','lifetime_replacement_USD2004')}
 ranges={}
 for metric in ('direct_USD2004','overnight_USD2004','annual_operating_USD2004','lifetime_replacement_USD2004','annual_reserve_USD2004'):
  low=min(conditional,key=lambda r:r['metrics'][metric]); high=max(conditional,key=lambda r:r['metrics'][metric]);ranges[metric]={'min':low['metrics'][metric],'min_case':low['case'],'max':high['metrics'][metric],'max_case':high['case']}
 summary={'baseline':base,'cases':rows,'contributions':leaves,'finite_change_rankings':ranks,'sampled_conditional_ranges':ranges,'completed':len(cases),'all_scoped_checks_satisfied':sum(not r['violations'] for r in rows),'constraint_failures':[r['case'] for r in rows if r['violations']],'conditional_points':len(conditional),'constant_conditional_net_MW':base['net_MW'],'scientific_support_all_zero':True,'constraints':{k:{v:sum(c['verdicts'][k]==v for c in cases) for v in sorted({c['verdicts'][k] for c in cases})} for k in baseline['verdicts']}}
 (R/'results/cost-analysis.json').write_text(json.dumps(summary,indent=2)+'\n')
 lines=['# Native cost results','','[AGENT executor] All amounts below are read from stored native outputs. Differences and ordering summarize these outputs; no caller recomputes plant costs. Money is USD2004. Capital, annual operating expense, lifetime scheduled replacements and the alternative annual reserve are separate boundaries.','', '## Baseline and leaf contributions','','| Metric | Native value |','| --- | ---: |']
 for k,v in base.items(): lines.append(f'| {k} | {v:.12g} |')
 lines+=['','The following 39 purchase leaves include initial tritium stock once. Their order is contribution size, not evidence of price certainty. Source eight-parent comparison amounts are excluded from this purchase list.','','| Purchased owner | Native USD2004 |','| --- | ---: |']
 for x in leaves:lines.append(f"| {x['owner']} | {x['USD2004']:.12g} |")
 lines+=['','## One-factor finite changes','','All 100 economic endpoint rows compare against the same baseline. Windows differ, so absolute delta rankings reflect these assumptions and window sizes. No derivative, probability, optimum or generalized monotonicity is established.','','| Case | Δ overnight USD2004 | Δ annual operating USD2004/year | Δ lifetime replacements USD2004 |','| --- | ---: | ---: | ---: |']
 for r in rows:
  if r['family']=='economic':
   d=r['delta_from_baseline'];lines.append(f"| {r['case']} | {d['overnight_USD2004']:.12g} | {d['annual_operating_USD2004']:.12g} | {d['lifetime_replacement_USD2004']:.12g} |")
 lines+=['','## Recovery, mode and combined scenarios','','Supplied recovery has no incremental recovery-cost or qualification law at fixed installed scope. It is an independently supplied boundary scenario, not purchased-capability optimization. Combined corners coordinate the declared assumptions; they are not probability bounds. No-credit and 100 kg/year boundaries remain separate.','','| Case | Overnight USD2004 | Annual operating USD2004/year | External T kg/year | Lifetime replacement USD2004 | Alternative reserve USD2004/year |','| --- | ---: | ---: | ---: | ---: | ---: |']
 for r in rows:
  if r['family'] in ('recovery','purchase-mode','combined'):
   m=r['metrics'];lines.append(f"| {r['case']} | {m['overnight_USD2004']:.12g} | {m['annual_operating_USD2004']:.12g} | {m['annual_external_T_kg']:.12g} | {m['lifetime_replacement_USD2004']:.12g} | {m['annual_reserve_USD2004']:.12g} |")
 lines+=['','## Observed sampled ranges','','These extrema describe only the 110 sampled assumed-baseline points. The three source-conditioned failing controls are excluded. They are not guarantees over the continuous input window.','','| Metric | Observed minimum | Case | Observed maximum | Case |','| --- | ---: | --- | ---: | --- |']
 for k,v in ranges.items():lines.append(f"| {k} | {v['min']:.12g} | {v['min_case']} | {v['max']:.12g} | {v['max_case']} |")
 lines+=['','## Constraints and support','','All conditional baseline-family points retain the same net output and zero import cost; import-tariff sensitivity is unexercised. The unchanged source-conditioned failures are diagnostic controls with incomplete/constraint-failing net values, not usable generating alternatives. All scientific support flags remain zero.','','| Exact constraint | Status counts |','| --- | --- |']
 for k,v in summary['constraints'].items():lines.append(f'| `{k}` | {v} |')
 (R/'cost-results.md').write_text('\n'.join(lines)+'\n')
 print(json.dumps({k:summary[k] for k in ('completed','all_scoped_checks_satisfied','constraint_failures','sampled_conditional_ranges')},indent=2))
if __name__=='__main__':main()
