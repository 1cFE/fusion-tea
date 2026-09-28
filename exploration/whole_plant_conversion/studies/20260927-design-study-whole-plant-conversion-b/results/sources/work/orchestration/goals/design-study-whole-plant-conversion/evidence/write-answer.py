"""Present independently verified native metrics; no physical or LCOE calculations."""
import argparse,json
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--record',type=Path,required=True);a=p.parse_args()
r=a.record;g=Path(__file__).resolve().parent.parent
load=lambda path:json.loads(path.read_text())
v=load(r/'results/verification_summary.json');assert v['outcome']=='pass'
d=load(r/'results/presentation/native-ranking.json');assert d['native_cases']==2496
assert sum(s['sampling']['sampled_rows'] for s in v['stores'])==d['native_cases']
assert len(v['channels_checked'])==1192 and len(v['constraints_rederived'])==125
rank={(x['scenario'],int(x['source_MW']),x['branch']):x for x in d['rankings']}
get=lambda s,q,b:rank[s,q,b]['metrics']
steam=get('nominal',2500,'steam');gas=get('nominal',2500,'gas')
combo='gas-favourable-gas-quote-x0.5-steam-x1.5'
cs,cg=get(combo,2800,'steam'),get(combo,2800,'gas')
prefix='../../../../'+r.as_posix()+'/'
lines=['# Whole-plant conversion choice','',
 f'For the declared supplied-source reactor, steam is the lower-cost choice at both supported nominal heat loads. At 2,500 MW of source heat, changing from helium Brayton to steam raises net export from {gas["power.net_export_MW"]:.1f} to {steam["power.net_export_MW"]:.1f} MW and lowers whole-plant LCOE from {gas["whole.lcoe_USD2025_MWh"]:.1f} to {steam["whole.lcoe_USD2025_MWh"]:.1f} USD2025/MWh. Steam buys more conversion equipment, but its higher electricity output spreads the common reactor and lifecycle costs over more MWh.','',
 '[AGENT] This is a conditional engineering comparison of a finite priced equipment catalog. It does not qualify a working fusion reactor or establish vendor prices. The same selected reactor and common assumptions apply within each pair. The conversion equipment is reselected at each source load.','',
 '## The reactor held fixed','',
 'The supplied configuration is a Stellaris-derived stellarator inventory: major radius 12.7 m, minor radius 1.3 m, 48 coils at 48 kA per turn, and 14 selected primary helium paths at 8 MPa. The primary stream rises from 300 to 500°C. The baseline source supplies 2,500 MW before recovered primary circulator work; it includes 50 MW of deposited auxiliary heating. The corresponding model-owned fusion heat is about 2,112 MW. External heating draws 100 MW of electricity. A selected 40/60 kW cryoplant serves the captured cold/intercept demands.','',
 'The comparison uses 2025 USD, 80% availability, a 30-year operating life, a 5% real discount rate and eight construction years. Prices and several common account allowances are assumptions documented with their sources and stress ranges. Plasma sustainment, neutron transport for the changed geometry and global manufactured fit remain unqualified. The implemented local hardware, cooling, return-temperature, electrical, fuel-processing and outage checks still apply.','',
 f'[Complete configuration]({prefix}supporting/configuration.md) · [Assembly diagram]({prefix}supporting/figures/assembly-comparison.svg)','',
 '## Nominal results','',
 '| Hot source MW | Conversion | Net export MW | Annual export TWh | Initial capital $bn | Financed initial capital $bn | Whole-plant LCOE $/MWh |',
 '|---:|---|---:|---:|---:|---:|---:|']
for q in (2500,2800):
 for b in ('steam','gas'):
  m=get('nominal',q,b);lines.append(f'| {q:,} | {"Steam" if b=="steam" else "Helium Brayton"} | {m["power.net_export_MW"]:.2f} | {m["power.annual_export_MWh"]/1e6:.3f} | {m["initial.initial_capital"]/1e9:.3f} | {m["whole.initial_financed_capital"]/1e9:.3f} | {m["whole.lcoe_USD2025_MWh"]:.2f} |')
lines += ['| 3,000 | Both | Unsupported | — | — | — | — |','',
 'Capital and LCOE use USD2025. Initial capital includes the declared purchases, overheads and startup fuel before financing. Annual export is the online LCOE denominator; each nominal plant also imports about 0.015 TWh/year while offline, with its cost included. Annual net grid delivery is reported separately. At 3,000 MW the selected primary pressure and divertor limits fail, so neither branch has an admissible whole-plant ranking.','',
 f'[Exact cases, fuel, service, replacements and terminal accounts]({prefix}results/presentation/matched-account-table.csv) · [All attempted cases and check status]({prefix}results/presentation/attempted-case-ledger.csv)','',
 '## Why the choice changes at plant scale','',
 f'At 2,500 MW, steam produces {steam["conversion.gross_electric"]:.1f} MW before its {steam["conversion.electrical_load"]:.1f} MW conversion auxiliaries. Brayton produces {gas["conversion.gross_electric"]:.1f} MW after compressor shaft work, then uses {gas["conversion.electrical_load"]:.1f} MW in conversion auxiliaries. Both pay the same {steam["power.upstream_electric_MW"]:.1f} MW upstream electrical bill, including primary circulation, heating, refrigeration and reactor services. Compressor work is already included in the Brayton gross output and is not subtracted again.','',
 f'The common initial purchases total about {steam["initial.common_purchases"]/1e9:.2f} billion USD2025. Steam adds {steam["initial.branch_purchases"]/1e9:.2f} billion in conversion purchases; Brayton adds {gas["initial.branch_purchases"]/1e9:.2f} billion. The full lifecycle accounts include fuel and standby imports, routine service, blanket/magnet/primary/conversion replacements and terminal costs. Common expenses matter strongly because the branches export different amounts of electricity. The figures normalize published native present-value contributions by published energy; they do not recompute the headline LCOE.','',
 'For the 2,500 MW pair, the native operating and future-event accounts are:','',
 '| Account | Steam | Brayton | Basis, USD2025 |','|---|---:|---:|---|',
 f'| Fuel | {steam["fuel.annual_fuel"]/1e6:.3f} | {gas["fuel.annual_fuel"]/1e6:.3f} | million/year |',
 f'| Nonfuel service | {steam["whole.annual_service"]/1e6:.3f} | {gas["whole.annual_service"]/1e6:.3f} | million/year |',
 f'| Makeup materials | {steam["whole.annual_makeup"]:.0f} | {gas["whole.annual_makeup"]:.0f} | USD/year |',
 f'| Offline electricity imports | {steam["power.annual_import_cost"]/1e6:.3f} | {gas["power.annual_import_cost"]/1e6:.3f} | million/year |',
 f'| Common plant replacements | {steam["whole.source_replacement_pv"]/1e9:.3f} | {gas["whole.source_replacement_pv"]/1e9:.3f} | billion, present value |',
 f'| Conversion replacements | {steam["whole.conversion_replacement_pv"]/1e9:.3f} | {gas["whole.conversion_replacement_pv"]/1e9:.3f} | billion, present value |',
 f'| Net terminal cost | {steam["whole.terminal_pv"]/1e9:.3f} | {gas["whole.terminal_pv"]/1e9:.3f} | billion, present value |','',
 'Annual streams and discounted future events use different bases and should not be added directly. The cost figure shows their model-owned present values per exported MWh. Fuel purchase remains conditional on the modeled breeding, recycling and stock assumptions.','',
 'At 2,800 MW the finite catalog selects a different Brayton operating offer. The nominal 2,500 MW winner fails the source-interface adequacy check there. This is why the selected Brayton export falls despite the larger source. These two minima are separate equipment/operating selections, not the load curve of one unchanged conversion plant.','',
 'The predecessor measured conversion-subsystem cost per net MWh, excluded the common plant boundary and used 85% availability. Its differences at 2,500 and 2,800 MW lay within the same 5 USD/MWh reporting band; its larger Brayton advantage at 3,000 MW cannot carry into this plant because the upstream hardware fails. This study reranked the offers using native whole-plant results. The comparison with the predecessor is a change of accounting boundary and assumptions, not a pure surcharge experiment.','',
 f'[Power contribution figure]({prefix}results/presentation/power-budget.svg) · [Lifecycle cost figure]({prefix}results/presentation/whole-cost-contributions.svg) · [Predecessor context]({prefix}results/presentation/predecessor-context.csv)','',
 '## When Brayton can become preferable','',
 'Steam retains its material advantage under the separately tested conversion prices, common capital and overheads, primary/other electrical loads, fuel assumptions and supported availability scenarios. Failed cryogenic, outage and source cases remain unsupported. The tested endpoints are engineered stresses, not confidence intervals.','',
 f'A combined hypothetical improvement can reverse the result at 2,800 MW: raise each Brayton compressor efficiency and turbine efficiency by 0.03 absolute, lower the steam HP/LP efficiencies by 0.03, halve Brayton conversion quotes and raise steam quotes by 50%. After reranking, Brayton gives {cg["whole.lcoe_USD2025_MWh"]:.2f} USD2025/MWh versus steam’s {cs["whole.lcoe_USD2025_MWh"]:.2f}. This is a conditional technology/price scenario, not a validated equipment offer or market forecast. At 2,500 MW that same combination still favors steam.','',
 'Holding those gas-favourable efficiency assumptions at 2,800 MW, vary the paired quote discount/premium continuously. Native full-catalog brackets place entry into the ±5 USD2025/MWh indeterminate band near a 24.12% Brayton discount and steam premium. Strict numerical equality is near 27.89%; Brayton becomes materially cheaper near 31.65%. The signed differences and both sides of each bracket are retained. The exact-zero bracket itself is indeterminate under the reporting convention.','',
 'The selected cryoplant reaches its cold-capacity boundary near 75.43 W/m³ of the supplied nuclear-heating input, with zero extra structural heat. Native tests at 75.42260 and 75.44260 W/m³ pass and fail respectively. This is a capacity threshold under the declared demand model; it is not a neutron-transport uncertainty bound.','',
 f'[Sensitivity figure]({prefix}results/presentation/preference-sensitivity.svg) · [Preference and thresholds]({prefix}results/presentation/preference-gap.svg) · [Threshold detail]({prefix}results/presentation/economic-boundary-detail.svg) · [Exact paired results]({prefix}results/presentation/matched-pairs.csv)','',
 '## Evidence and practical limit','',
 'Every one of the 2,496 native cases passes independent numerical verification of 1,192 scalar channels and 125 rederived predicates. This includes cases with failed engineering checks; numerical agreement does not make those cases feasible. The first failed study remains sealed separately. Its independently diagnosed oracle stopping-precision defect was corrected, and four cryogenic diagnostic points were moved farther from zero margin. Acceptance tolerances and native plant equations remain unchanged.','',
 'Use the result to prioritize steam for this declared reactor and finite catalog, and to identify what performance and price assumptions a Brayton alternative would need to challenge it. Absolute costs remain conditional on the supplied reactor, common account scope and unqualified source/transport assumptions. Open catalog edges and different modeled operating freedoms prevent a claim of global technology optimization.','',
 f'[Study record]({prefix}record.md) · [Independent final review]({prefix}supporting/final-results-review.md) · [Replay and rendering commands]({prefix}REPLAY.md) · [What transferred and what needed new work](findings-log.md)','']
text='\n'.join(lines);(g/'answer.md').write_text(text)
(r/'study-conclusion.md').write_text(text.replace(prefix,'').replace('(findings-log.md)','(supporting/findings-log.md)'))
article=f'''# Proposed article passage

We used the expanded component library to compare steam and helium Brayton conversion for the same declared stellarator reactor. The comparison includes the reactor’s capital, primary circulation, heating, refrigeration, fuel and lifecycle costs, and selects equipment from a finite catalog. At a supplied heat load of 2,500 MW, steam exports {steam['power.net_export_MW']:.0f} MW against Brayton’s {gas['power.net_export_MW']:.0f} MW. Its conditional whole-plant LCOE is about {steam['whole.lcoe_USD2025_MWh']:.0f} rather than {gas['whole.lcoe_USD2025_MWh']:.0f} USD2025/MWh. Steam needs more conversion equipment, but produces substantially more electricity over which to spread the common plant costs.

Steam also leads at 2,800 MW under nominal assumptions. Brayton becomes cheaper in a combined scenario with better compressor/turbine efficiency, worse steam efficiency and favorable relative equipment prices. The previously studied 3,000 MW subsystem advantage does not establish a plant-level winner: the selected primary and divertor hardware cannot support that source condition. The result shows why a component comparison needs the complete plant boundary. It remains conditional on a supplied reactor source, assumed prices and the modeled equipment catalog; plasma sustainment, neutron transport and global construction fit are not qualified.
'''
(g/'proposed-article.md').write_text(article);(r/'proposed-article.md').write_text(article)
print(json.dumps({'answer':str(g/'answer.md'),'article':str(g/'proposed-article.md'),'native_cases':d['native_cases']}))
