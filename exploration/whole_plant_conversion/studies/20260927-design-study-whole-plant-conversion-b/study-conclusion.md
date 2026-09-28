# Whole-plant conversion choice

For the declared supplied-source reactor, steam is the lower-cost choice at both supported nominal heat loads. At 2,500 MW of source heat, changing from helium Brayton to steam raises net export from 285.9 to 664.0 MW and lowers whole-plant LCOE from 875.3 to 408.2 USD2025/MWh. Steam buys more conversion equipment, but its higher electricity output spreads the common reactor and lifecycle costs over more MWh.

[AGENT] This is a conditional engineering comparison of a finite priced equipment catalog. It does not qualify a working fusion reactor or establish vendor prices. The same selected reactor and common assumptions apply within each pair. The conversion equipment is reselected at each source load.

## The reactor held fixed

The supplied configuration is a Stellaris-derived stellarator inventory: major radius 12.7 m, minor radius 1.3 m, 48 coils at 48 kA per turn, and 14 selected primary helium paths at 8 MPa. The primary stream rises from 300 to 500°C. The baseline source supplies 2,500 MW before recovered primary circulator work; it includes 50 MW of deposited auxiliary heating. The corresponding model-owned fusion heat is about 2,112 MW. External heating draws 100 MW of electricity. A selected 40/60 kW cryoplant serves the captured cold/intercept demands.

The comparison uses 2025 USD, 80% availability, a 30-year operating life, a 5% real discount rate and eight construction years. Prices and several common account allowances are assumptions documented with their sources and stress ranges. Plasma sustainment, neutron transport for the changed geometry and global manufactured fit remain unqualified. The implemented local hardware, cooling, return-temperature, electrical, fuel-processing and outage checks still apply.

[Complete configuration](supporting/configuration.md) · [Assembly diagram](supporting/figures/assembly-comparison.svg)

## Nominal results

| Hot source MW | Conversion | Net export MW | Annual export TWh | Initial capital $bn | Financed initial capital $bn | Whole-plant LCOE $/MWh |
|---:|---|---:|---:|---:|---:|---:|
| 2,500 | Steam | 663.97 | 4.653 | 18.407 | 22.374 | 408.16 |
| 2,500 | Helium Brayton | 285.88 | 2.003 | 16.963 | 20.619 | 875.31 |
| 2,800 | Steam | 746.64 | 5.232 | 18.722 | 22.756 | 370.70 |
| 2,800 | Helium Brayton | 204.46 | 1.433 | 16.963 | 20.619 | 1230.28 |
| 3,000 | Both | Unsupported | — | — | — | — |

Capital and LCOE use USD2025. Initial capital includes the declared purchases, overheads and startup fuel before financing. Annual export is the online LCOE denominator; each nominal plant also imports about 0.015 TWh/year while offline, with its cost included. Annual net grid delivery is reported separately. At 3,000 MW the selected primary pressure and divertor limits fail, so neither branch has an admissible whole-plant ranking.

[Exact cases, fuel, service, replacements and terminal accounts](results/presentation/matched-account-table.csv) · [All attempted cases and check status](results/presentation/attempted-case-ledger.csv)

## Why the choice changes at plant scale

At 2,500 MW, steam produces 960.3 MW before its 22.7 MW conversion auxiliaries. Brayton produces 566.9 MW after compressor shaft work, then uses 7.4 MW in conversion auxiliaries. Both pay the same 273.6 MW upstream electrical bill, including primary circulation, heating, refrigeration and reactor services. Compressor work is already included in the Brayton gross output and is not subtracted again.

The common initial purchases total about 10.23 billion USD2025. Steam adds 2.55 billion in conversion purchases; Brayton adds 1.54 billion. The full lifecycle accounts include fuel and standby imports, routine service, blanket/magnet/primary/conversion replacements and terminal costs. Common expenses matter strongly because the branches export different amounts of electricity. The figures normalize published native present-value contributions by published energy; they do not recompute the headline LCOE.

For the 2,500 MW pair, the native operating and future-event accounts are:

| Account | Steam | Brayton | Basis, USD2025 |
|---|---:|---:|---|
| Fuel | 0.390 | 0.390 | million/year |
| Nonfuel service | 80.973 | 71.307 | million/year |
| Makeup materials | 4242 | 1409 | USD/year |
| Offline electricity imports | 0.748 | 0.748 | million/year |
| Common plant replacements | 4.731 | 4.731 | billion, present value |
| Conversion replacements | 0.453 | 0.148 | billion, present value |
| Net terminal cost | 0.375 | 0.347 | billion, present value |

Annual streams and discounted future events use different bases and should not be added directly. The cost figure shows their model-owned present values per exported MWh. Fuel purchase remains conditional on the modeled breeding, recycling and stock assumptions.

At 2,800 MW the finite catalog selects a different Brayton operating offer. The nominal 2,500 MW winner fails the source-interface adequacy check there. This is why the selected Brayton export falls despite the larger source. These two minima are separate equipment/operating selections, not the load curve of one unchanged conversion plant.

The predecessor measured conversion-subsystem cost per net MWh, excluded the common plant boundary and used 85% availability. Its differences at 2,500 and 2,800 MW lay within the same 5 USD/MWh reporting band; its larger Brayton advantage at 3,000 MW cannot carry into this plant because the upstream hardware fails. This study reranked the offers using native whole-plant results. The comparison with the predecessor is a change of accounting boundary and assumptions, not a pure surcharge experiment.

[Power contribution figure](results/presentation/power-budget.svg) · [Lifecycle cost figure](results/presentation/whole-cost-contributions.svg) · [Predecessor context](results/presentation/predecessor-context.csv)

## When Brayton can become preferable

Steam retains its material advantage under the separately tested conversion prices, common capital and overheads, primary/other electrical loads, fuel assumptions and supported availability scenarios. Failed cryogenic, outage and source cases remain unsupported. The tested endpoints are engineered stresses, not confidence intervals.

A combined hypothetical improvement can reverse the result at 2,800 MW: raise each Brayton compressor efficiency and turbine efficiency by 0.03 absolute, lower the steam HP/LP efficiencies by 0.03, halve Brayton conversion quotes and raise steam quotes by 50%. After reranking, Brayton gives 397.38 USD2025/MWh versus steam’s 426.74. This is a conditional technology/price scenario, not a validated equipment offer or market forecast. At 2,500 MW that same combination still favors steam.

Holding those gas-favourable efficiency assumptions at 2,800 MW, vary the paired quote discount/premium continuously. Native full-catalog brackets place entry into the ±5 USD2025/MWh indeterminate band near a 24.12% Brayton discount and steam premium. Strict numerical equality is near 27.89%; Brayton becomes materially cheaper near 31.65%. The signed differences and both sides of each bracket are retained. The exact-zero bracket itself is indeterminate under the reporting convention.

The selected cryoplant reaches its cold-capacity boundary near 75.43 W/m³ of the supplied nuclear-heating input, with zero extra structural heat. Native tests at 75.42260 and 75.44260 W/m³ pass and fail respectively. This is a capacity threshold under the declared demand model; it is not a neutron-transport uncertainty bound.

[Sensitivity figure](results/presentation/preference-sensitivity.svg) · [Preference and thresholds](results/presentation/preference-gap.svg) · [Threshold detail](results/presentation/economic-boundary-detail.svg) · [Exact paired results](results/presentation/matched-pairs.csv)

## Evidence and practical limit

Every one of the 2,496 native cases passes independent numerical verification of 1,192 scalar channels and 125 rederived predicates. This includes cases with failed engineering checks; numerical agreement does not make those cases feasible. The first failed study remains sealed separately. Its independently diagnosed oracle stopping-precision defect was corrected, and four cryogenic diagnostic points were moved farther from zero margin. Acceptance tolerances and native plant equations remain unchanged.

Use the result to prioritize steam for this declared reactor and finite catalog, and to identify what performance and price assumptions a Brayton alternative would need to challenge it. Absolute costs remain conditional on the supplied reactor, common account scope and unqualified source/transport assumptions. Open catalog edges and different modeled operating freedoms prevent a claim of global technology optimization.

[Study record](record.md) · [Independent final review](supporting/final-results-review.md) · [Replay and rendering commands](REPLAY.md) · [What transferred and what needed new work](supporting/findings-log.md)
