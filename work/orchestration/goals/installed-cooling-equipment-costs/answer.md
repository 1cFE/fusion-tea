# Cooling equipment costs: source and accounting gap remains

The cooling-cost gap is not closed. The model calculates helium flow, pressure loss, pumping electricity and exchanger duty, but it still prices heat transport through aggregate plant-power relationships. No new equipment price has been admitted or substituted. Independent preimplementation review holds the change pending applicable cost evidence and a concrete equipment/accounting design. The [fresh independent assessment](evidence/final-review-and-grade.md) assigns **R7.S2, unchanged; S3 is not met**. The goal remains open.

## What is established

The [account-boundary map](evidence/account-boundary-map.md) traces current physics, cost accounts and lifecycle. The [retained-case extraction](evidence/starting-cases.json) confirms the owner's starting facts from native results. A [fresh replay](evidence/entering-replay.json) executes those exact overrides on today's model and reproduces all 23 selected historical cooling/economic channels for each case exactly.

The latest selected design has eighteen representative helium circuits, implying 36 circulators and eighteen intermediate heat exchangers (IHXs). Its total required exchanger duty is 3,013.915 MW, or 167.440 MW per circuit. The matched fourteen-circuit design also passed the earlier model's checks. These are calculated requirements under a representative-circuit assumption, not equipment selections or an optimum.

Today's model includes a newer calculated tritium-breeding check. Both selected designs now fail that check. The saved r2 controls retain their previous three failures and also fail breeding. Their cooling/economic values remain unchanged. This work preserves those failures and the historical records.

| Current replay of retained inputs | Circuits | Pump electricity, MW | Net electricity, MW | Existing coolant allowance, $million | Total modeled capital, $million | LCOE, $/MWh |
|---|---:|---:|---:|---:|---:|---:|
| Selected design | 18 | 86.776 | 1,010.112 | 205.073 | 9,465.696 | 150.430 |
| Same design, fourteen circuits | 14 | 143.796 | 975.844 | 199.772 | 9,490.637 | 156.052 |
| Saved r2 forward control | 14 | 166.241 | 1,003.739 | 205.518 | 10,204.510 | 162.871 |
| Saved r2 Table 5-conditioned control | 14 | 164.995 | 1,003.767 | 205.464 | 10,214.050 | 162.947 |

LCOE means levelized cost of electricity. These are the existing mixed-basis model estimates, not complete installed plant prices. No cost or LCOE change is attributable to this goal: the model and executable have not changed. That does not mean the missing equipment is free. The eighteen-versus-fourteen differences come from existing hydraulic and aggregate-cost relationships, not newly priced equipment.

## What determines the equipment requirements

The current model calculates total helium mass flow from source heat divided by helium heat capacity and temperature rise. Circuit count divides the flow; a reference squared-flow law determines circuit pressure loss. A compressor calculation determines fluid work and electricity use. The exchanger must remove reactor heat plus recovered compressor work. These dependencies already affect net electricity and engineering checks.

The [independent physical-source review](evidence/sizing-source-review.md) verifies a useful exchanger-area anchor: approximately 87,277 m² across the source's nine unequal circuits, consistent with its rounded 87,300 m². Its implied heat-transfer coefficient includes an unknown multipass correction. Transferring it near the source conditions could support a stated conceptual assumption, but it is not a complete exchanger design or a price.

Important inputs remain unresolved:

- **Circulators:** the source establishes two machines per loop; its energy balance supports both operating but does not establish their series/parallel arrangement. A stated equal-parallel assumption would give half the circuit flow and full circuit pressure rise per machine. Applicable pricing still needs pressure, inlet temperature/density, power, construction and drive/package inclusions.
- **Exchangers:** pricing needs the secondary fluid/conditions, pressure boundary, material and exchanger technology. The source helium-to-salt design is not interchangeable with a helium-to-helium printed-circuit exchanger. Actual terminal temperatures must determine the temperature driving force.
- **Piping:** the source supplies selected nominal diameters, material, a maximum hot-leg wall thickness and total network length. It does not supply a complete bill of quantities. Applying the largest pipe section to the entire network would invent its mass. Layout allowances and their hydraulic consequences need explicit treatment.

No pumps, pipes or exchangers are newly priced in the executable.

## What would be replaced and how double counting was checked

The Cost Account Structure (CAS) is the hierarchy that totals plant costs. Its coolant account, C220200, currently combines a primary estimate proportional to net electrical power and an intermediate estimate proportional to thermal power raised to 0.55. Neither term depends directly on circulator count, exchanger area or pipe quantity.

A supported equipment estimate must replace its overlapping part of that allowance. Adding it on top would duplicate unknown scope. The [independent accounting review](evidence/accounting-preimplementation-review.md) checked the actual equations and identified further boundaries:

- Reactor equipment installation excludes cooling; it does not supply an installation basis for the replacement account.
- Contingency, indirects, shipping, tax and insurance already propagate through the capital hierarchy. An inclusive source estimate needs reconciliation before entry.
- Buildings, electrical services, instrumentation, auxiliary cooling, turbine equipment and ultimate heat rejection have separate allowances. Dedicated equipment inclusions must be distinguished from shared plant services.
- Existing coolant fill prices breeder material, not primary helium inventory. Cooling spares and equipment replacement are absent from their respective accounts. General staffing-based O&M does not establish a cooling maintenance allocation.
- Pump electricity already reduces net generation. Charging it again as purchased operating electricity would duplicate its effect.

These checks locate omissions and overlap risks; they do not establish a complete reconciled installed estimate. No old allowance has yet been removed.

## Research and implementation gate

The [native research summary](evidence/source-methods.md) records the methods investigated, source retrieval outcomes and applicability limits. Existing DEMO evidence reports preliminary supplier offers but does not supply a transferable installed price and excludes large piping. The continuation ended with four original reports queued after retrieval failures: General Atomics 911105 (helium heat transport), Dominion M-6914-00-04 (major equipment costs), General Atomics 911120 (steam-generator alternatives), and Stewart et al. 2021 (compact HTGR economics). Original institutional downloads returned 404; publisher/author-copy routes returned access errors. Cached numerical snippets were not admitted as model prices. The accessible 2024 INL follow-up supplied no equipment-specific method. This is a bounded acquisition failure, not evidence that the literature contains no suitable method. The registered low-temperature INL installation methodology describes equipment-based estimation; its water-system prices do not establish 8 MPa, 300–500 °C helium costs.

A vendor quotation is not mandatory. An original conceptual estimate or documented estimating method can suffice if its equipment domain, scaling, price year, fabrication/installation boundaries and uncertainty can be checked. The missing requirement is that defensible bridge, not a particular commercial document format.

[WI-067](../../../active/WI-067_installed-cooling-equipment-costs/spec.md) records the native implementation contract. Substantial model changes, a new generated package and the requested equipment-cost study remain unperformed while the source/design gate is held. The four-case replay is a diagnostic continuity check, not that study.

## Verification and next step

The entering targeted batch returned **131 passes and six failures**. The failures are existing consumer mapping/output-contract mismatches. Several tests stop before their later heat-balance or parity assertions, so those later assertions are not certified by this batch. The [full log](evidence/entering-cooling-tests.log) is retained. The supplied reassessment's eight failures are a separate earlier batch; no full-suite pass is claimed.

The next useful deliverable is a checked equipment estimate basis containing original prices or estimating equations, actual price years, operating/material/size ranges, installed-scope inclusions, a pipe layout allowance and lifecycle treatment. It must then pass the already commissioned source/accounting review before integration and a matched native study. The concrete first step is to acquire and image-check the queued original tables, especially 911120’s installed heat-transport breakdown and 911105’s separate equipment estimates, then determine whether their technology and cost boundaries transfer. An equivalent accessible published estimating method can replace that route. The goal and WI-067 remain open; formal closure remains the owner's decision.

The [preservation check](evidence/preservation.json) confirms unchanged models, generated package and both cited historical studies, and the published r2 archive retains SHA256 `fa42cb32c1a51989871ba15a3bf2c51ca0a88c9a506b27c8e314c88b42960a21`. Two goal-contract checks pass. ARIES remains sealed; unrelated changes were preserved.

The discovery-log join check returned **26 passes and one unrelated existing failure**: the current parser finds no finding IDs in the unchanged `20260918-computed-tritium-breeding` record. The two studies receiving this round's six disposition rows pass. The failure occurs while parsing that other record, before checking log membership; neither its record nor the parser was changed here. See [join-check log](evidence/discovery-join-tests.log).
