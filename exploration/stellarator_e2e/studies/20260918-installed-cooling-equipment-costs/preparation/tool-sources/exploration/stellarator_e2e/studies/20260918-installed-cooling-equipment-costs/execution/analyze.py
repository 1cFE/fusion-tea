"""Summarize retained native evidence; performs no model evaluations."""
from pathlib import Path
import json
H=Path(__file__).resolve().parents[1];R=H/'results';P='stellarator_09__stellaris__';E=P+'heat_transport__equipment__'
read=lambda p:json.loads(p.read_text())

def main():
    verification=read(R/'oracle-all-points.json')
    generic=read(R/'verification_summary.json') if (R/'verification_summary.json').exists() else {'outcome':'refused; generic-verification.log retains the error; no success receipt emitted'}
    rows=read(R/'interpreted-cases.json');byid={r['proposal_id']:r for r in rows};catalog=read(R/'predicate-catalog.json')
    selected=byid['lhs-0224-full'];lcoe=P+'lcoe_calc__lcoe'
    retained=[r for r in rows if r['family'].startswith('retained-')]
    sensitivity=[r for r in rows if r['family']=='selected18-full-sensitivity']
    quantities=['circulator_count','circulator_flow','circulator_volume','circulator_shaft_MW','circulator_electric_MW','circulator_suction_Pa','ihx_count','ihx_duty_MW','ihx_installed_area','ihx_required_area','hx_mass','primary_pipe_mass','secondary_pipe_mass','helium_inventory_mass','salt_inventory_mass','salt_pump_count','salt_pump_flow','salt_pump_shaft_MW','pump_shaft_hp','motor_electric_hp','salt_electric_MW','salt_shaft_MW','salt_straight_loss','salt_head_remaining','cycle_temperature_gap','helium_inventory_volume','primary_pipe_volume','helium_hx_volume','salt_inventory_volume','salt_pipe_volume','salt_hx_volume','source_volume_ratio']
    costs=['primary_vendor','primary_installation','primary_design','primary_spare','secondary_vendor','secondary_installation','secondary_spare','hx_purchase','hx_installation','primary_pipe_purchase','primary_pipe_installation','secondary_pipe_purchase','secondary_pipe_installation','primary_circulators_cost','primary_piping_cost','exchangers_cost','secondary_pumps_cost','secondary_piping_cost','inventory_cost','spares_cost','purchased_total','installation_total','installed_total','primary_design','delivered_total','replacement_annual','consumables_annual','machine_event_purchase','machine_event_installation','machine_event_removal','bundle_event_purchase','bundle_event_installation','bundle_event_removal','machine_events','bundle_events','salt_price_raw','salt_price_year','salt_unit_price','helium_price_raw','helium_price_year']
    diagnostics=[k.removeprefix(E) for k in selected if k.startswith(E) and (k.endswith('_ok') or k.endswith('_validated') or k.endswith('_qualified') or k.endswith('_complete'))]
    summary={'cases':len(rows),'wholeplant_satisfied':sum(r['wholeplant_satisfied'] for r in rows),'selected_quantities':{k:selected[E+k] for k in quantities},'selected_costs':{k:selected[E+k] for k in costs},'selected_diagnostics':{k:selected[E+k] for k in diagnostics},'diagnostic_failures':{r['proposal_id']:[k for k in diagnostics if not r[E+k]] for r in rows},'constraint_cases':{cid:{status:[r['proposal_id'] for r in rows if r[cid]==status] for status in ['satisfied','violated','indeterminate']} for cid in catalog},'sensitivity_deltas':[{'proposal_id':r['proposal_id'],'lcoe':r[lcoe],'delta_lcoe':r[lcoe]-selected[lcoe],'total_capital':r[P+'total_capital__total_capital'],'primary_electric_MW':r[P+'heat_transport__primary_loop__p_elec'],'salt_electric_MW':r[E+'salt_electric_MW'],'net_MW':r[P+'pb__p_net'],'installed_total':r[E+'installed_total'],'replacement_annual':r[E+'replacement_annual'],'consumables_annual':r[E+'consumables_annual'],'violated':r['violated']} for r in sensitivity]}
    (R/'analysis.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
    lines=['# Installed cooling equipment study results','',f"All {len(rows)} native candidates are retained; {summary['wholeplant_satisfied']} satisfy every whole-plant predicate. The default baseline is recorded separately. This is an engineered sensitivity study, not a feasible design or an optimum.",'',f"Verification status: all-point {verification['outcome']}; generic {generic['outcome']}. The original boundary mismatch and refusal remain in results/verification-boundary-attempt/. The reviewed oracle correction preserves authored operation order and all native negative verdicts; it changes no native case or physical limit.",'', '## Retained case and mode comparisons','','| Proposal | LCOE, $/MWh | Net MW | Total capital, $million | Selected cooling account, $million | Primary pump electric MW | Selected salt pump electric MW | Failed predicates |','|---|---:|---:|---:|---:|---:|---:|---|']
    baseline=read(R/'baseline_result.json')['channels']
    for r in retained:
        salt=r[E+'salt_electric_MW']*r['input:'+P+'heat_transport__secondary_energy_mode']
        lines.append(f"| {r['proposal_id']} | {r[lcoe]:.6f} | {r[P+'pb__p_net']:.3f} | {r[P+'total_capital__total_capital']/1e6:,.3f} | {r[P+'heat_transport__cooling_selection__cost']/1e6:,.3f} | {r[P+'heat_transport__primary_loop__p_elec']:.3f} | {salt:.3f} | {r['violated']} |")
    lines+=['','Equipment diagnostics remain enabled in legacy mode; its installed diagnostic total does not mean that equipment cost is selected into the legacy accounts. Cost-only and full modes select new accounts. The full mode also selects secondary electric demand and recovered shaft heat.','',f"Default baseline (separate authored case): LCOE {baseline[lcoe]:.6f} dollars/MWh and net electric {baseline[P+'pb__p_net']:.6f} MW; total capital {baseline[P+'total_capital__total_capital']/1e6:,.3f} million dollars; primary/salt pump electric demand {baseline[P+'heat_transport__primary_loop__p_elec']:.3f}/{baseline[E+'salt_electric_MW']:.3f} MW. It is not selected18.",'',f"Selected full CAS72 total: {selected[P+'cooling_annual__cas72_total']:.2f} dollars/year. Cooling adds {selected[E+'replacement_annual']:.2f} dollars/year to existing calendar replacements of {selected[P+'calendar__cas72_annual']:.2f} dollars/year.",'', '## Selected eighteen-circuit equipment','','The raw quantities and source scope are preserved in analysis.json and points.csv. Machine quantities are per machine, exchanger geometry and duty per exchanger, salt flow per circuit, and aggregate costs/masses plant totals according to preparation/equipment-interface.json.','', '| Quantity | Value | Unit / basis |','|---|---:|---|']
    labels={
      'circulator_count':('Active helium circulators','machines, plant'),
      'circulator_flow':('Helium mass flow','kg/s per circulator'),
      'circulator_volume':('Helium inlet volume flow','m³/s per circulator'),
      'circulator_shaft_MW':('Helium circulator shaft power','MW per circulator'),
      'circulator_electric_MW':('Helium circulator electric power','MW per circulator'),
      'circulator_suction_Pa':('Helium suction pressure','Pa'),
      'ihx_count':('Intermediate heat exchangers','exchangers, plant'),
      'ihx_duty_MW':('Intermediate exchanger heat duty','MW per exchanger'),
      'ihx_installed_area':('Installed heat-transfer area','m² per exchanger'),
      'ihx_required_area':('Required heat-transfer area','m² per exchanger'),
      'hx_mass':('Exchanger steel mass','kg per exchanger'),
      'primary_pipe_mass':('Helium piping mass','kg, plant'),
      'secondary_pipe_mass':('Salt piping mass','kg, plant'),
      'helium_inventory_mass':('Helium inventory with reserve','kg, plant'),
      'salt_inventory_mass':('Salt inventory with reserve','kg, plant'),
      'salt_pump_count':('Active salt pumps','pumps, plant'),
      'salt_pump_flow':('Salt mass flow','kg/s per pump'),
      'salt_pump_shaft_MW':('Salt pump shaft power','MW per pump'),
      'pump_shaft_hp':('Salt pump shaft power for price correlation','hp per pump'),
      'motor_electric_hp':('Salt pump motor electric power','hp per pump'),
      'salt_electric_MW':('Salt pump electric power','MW, plant'),
      'salt_shaft_MW':('Salt pump shaft heat','MW, plant'),
      'salt_straight_loss':('Salt straight-pipe head loss','m of salt'),
      'salt_head_remaining':('Head remaining for other salt components','m of salt'),
      'cycle_temperature_gap':('Salt outlet minus cycle-fit temperature','K'),
      'helium_inventory_volume':('Modeled helium volume before reserve','m³, plant'),
      'primary_pipe_volume':('Helium pipe internal volume','m³, plant'),
      'helium_hx_volume':('Helium exchanger internal volume','m³, plant'),
      'salt_inventory_volume':('Modeled salt volume before reserve','m³, plant'),
      'salt_pipe_volume':('Salt pipe internal volume','m³, plant'),
      'salt_hx_volume':('Salt exchanger internal volume','m³, plant'),
      'source_volume_ratio':('Modeled versus source helium inventory volume','dimensionless ratio')}
    for k,v in summary['selected_quantities'].items():
        label,unit=labels[k];lines.append(f'| {label} | {v:,.6f} | {unit} |')
    lines+=['','## Selected cost breakdown','','Equipment costs below are millions of 2025 US dollars using the stated CPI purchasing-power proxy. Procurement includes source-specific fabricated or vendor package scope; field installation is separate. The inherited whole-plant total capital uses its existing mixed basis.','','| Cost component | Value | Unit / scope |','|---|---:|---|']
    costlabels={'primary_vendor':'Helium circulators: vendor packages','primary_installation':'Helium circulators: field installation','primary_design':'Helium circulators: first design fee','primary_spare':'Helium circulator spare','secondary_vendor':'Salt pumps: purchased packages','secondary_installation':'Salt pumps: field installation','secondary_spare':'Salt pump spare','hx_purchase':'Exchangers: fabricated purchase','hx_installation':'Exchangers: field installation','primary_pipe_purchase':'Helium piping: fabricated purchase','primary_pipe_installation':'Helium piping: field installation','secondary_pipe_purchase':'Salt piping: fabricated purchase','secondary_pipe_installation':'Salt piping: field installation','primary_circulators_cost':'Helium circulators: installed account','primary_piping_cost':'Helium piping: installed account','exchangers_cost':'Exchangers: installed account','secondary_pumps_cost':'Salt pumps: installed account','secondary_piping_cost':'Salt piping: installed account','inventory_cost':'Initial fluid inventory','spares_cost':'Initial spares','purchased_total':'All purchase scope including inventory/spares/design','installation_total':'All field installation','installed_total':'Total seven equipment accounts','delivered_total':'Eligible delivered basis for downstream freight','replacement_annual':'Additional annual cooling replacements','consumables_annual':'Annual fluid makeup'}
    for k,v in summary['selected_costs'].items():
        label=costlabels.get(k,k.replace('_',' ').capitalize())
        if k.endswith('_events'):unit='events strictly before plant horizon';value=v
        elif k.endswith('_year'):unit='source calendar year';value=v
        elif k=='salt_price_raw':unit='2011 USD/kg';value=v
        elif k=='salt_unit_price':unit='2025 USD/kg, CPI proxy';value=v
        elif k=='helium_price_raw':unit='2024 USD/standard m³';value=v
        else:unit='million USD2025/year' if k.endswith('_annual') else 'million USD2025';value=v/1e6
        lines.append(f'| {label} | {value:,.6f} | {unit} |')
    lines+=['','## Local sensitivities','','| Proposal | LCOE, $/MWh | Change vs selected full | Installed cooling, million USD2025 | Total capital, $million | Primary / salt pump MW | Net MW | Failed predicates |','|---|---:|---:|---:|---:|---:|---:|---|']
    for r in summary['sensitivity_deltas']:lines.append(f"| {r['proposal_id']} | {r['lcoe']:.6f} | {r['delta_lcoe']:+.6f} | {r['installed_total']/1e6:,.3f} | {r['total_capital']/1e6:,.3f} | {r['primary_electric_MW']:.3f} / {r['salt_electric_MW']:.3f} | {r['net_MW']:.3f} | {r['violated']} |")
    lines+=['','## Equipment diagnostic flags','','These are Boolean equipment diagnostics, distinct from the twenty authored whole-plant acceptance predicates. A failed flag is retained even when it does not change the predicate verdict.','','| Proposal | False equipment flags |','|---|---|']
    for name,flags in summary['diagnostic_failures'].items():lines.append(f"| {name} | {'; '.join(flags)} |")
    lines+=['','## Applicability and boundaries','','The 480°C source-fit temperature exceeds the 465°C salt interface. Lower-cost cases do not resolve this physical interface failure. The current breeding screen and all pump source applicability checks remain visible. Helium cost scaling, nuclear fabrication transfer, salt-pump fluid transfer, reserve, geometry and lifecycle assumptions remain conditional; these cases are not vendor quotations or pressure-qualified hardware.','','The CPI proxy converts cited equipment prices to 2025 purchasing power and does not rebase inherited whole-plant accounts. Existing CAS71 staffing covers routine cooling work as an ownership assumption. Replacements retain modeled availability; coincident maintenance is assumed, not demonstrated. Steam-generator CAS23 coverage, full in-vessel inventories, drain/expansion and trace-heating auxiliaries remain unresolved scope.','','Independent equation agreement verifies software implementation. It does not validate the shared transport data or physical applicability of source transfers. Every authored predicate and required numeric channel is retained. See oracle-all-points.json, verification_summary.json and points.csv for exact coverage.','']
    (H/'report.md').write_text('\n'.join(lines))
    print('Wrote analysis.json and report.md from stored evidence only; verification outcome preserved')
if __name__=='__main__':main()
