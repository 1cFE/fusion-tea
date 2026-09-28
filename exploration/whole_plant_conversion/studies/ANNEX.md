# Whole-plant conversion comparison study annex

[AGENT] This package compares steam and helium Brayton conversion using the same declared supplied reactor inventory. The metric is whole-plant lifecycle cost per net MWh in real 2025 USD. Model authority is the independently reviewed design and configuration in `work/active/WI-098_whole-plant-conversion-comparison/`; source, transport and construction qualifications remain explicit conditions on the comparison.

## Package and execution

The generated package is `exploration/whole_plant_conversion/whole_plant_conversion_tea`. Its assembly is `models/designs/whole_plant_conversion/plant.sysml`. The exploration directory contains the reproducible source collection, build script, snapshot, census, development runner and independent verifier.

`study_route.py` uses the stock strict `ProvisionalPackageLoader`, `PreparedEvaluator`, `CandidateBridge`, `StudyRunner`, `PreparedListStrategy`, `StudyStore` and `StudyQuery`. The direct-API route supports coordinated finite offers. Proposal scripts choose inputs; all physical closure, fuel accounting, cashflow and constraint evaluation remain inside the native package. Glue ledger: none.

`execute_study.py` requires a matching successful native integration return, a clean package and complete declared points. Every executed point retains its inputs, outputs and native verdicts. Failed engineering predicates remain failed. Body refusals remain in scan evidence; the main native execution list must satisfy the runbook's requirement that every point evaluate. Existing results are not overwritten.

## Baseline pin

The reviewed baseline is case `whole-baseline2500` in `work/active/WI-098_whole-plant-conversion-comparison/evidence/development-final/native/cases.json`. It selects 2500 MW hot source, 2000 kg/s Brayton flow, three compressor ratios of 1.5, cooler conductances of 25/25/25 MW/K and recuperator conductance of 60 MW/K. Steam uses 10 exchanger circuits and four 225 kg/s salt pumps per circuit. Shared availability is 0.80. All 125 native predicates pass. The gas catalog separately fixes steam to 14 circuits with four 250 kg/s pumps; that is a candidate choice, not the pinned baseline.

The receipt pins executable fingerprint `6915694e74919ebb764445dfc7f0782eda85a9de29fa44c4b55ffa415c1eb30f` and semantic fingerprint `bb284160ba12996bc129ba91c1838aed3281d54dc0e729fe03ca02a9d413d6e3`. The final contract has 637 complete public input entries, 1196 numeric outputs and 125 predicates. Numerical comparison covers 1192 outputs; four inherited solver-iteration diagnostics are excluded from numerical equality.

`prepare_interface.py` reads the actual contract and evaluated receipt, including its structured native constraint report. The manifest pins the complete baseline map, headline and verdicts. The stock integration seam must reproduce that point and verify package identity, source snapshot, regeneration fixed point, model-family coverage, manifest, read coverage and numerical verification. This annex does not substitute for the returned integration candidate or the main study's preflight.

All 498 retained predecessor controls passed at this executable identity. `work/active/WI-098_whole-plant-conversion-comparison/evidence/conversion-controls/comparison.json` records zero difference across 872 inherited channels and 84 predicates per case. `evidence/independent-verification/controls-summary.json` under that work item records all 498 independent whole-plant checks passing. Legacy controls preserve their original finance; the main baseline explicitly uses shared availability 0.80.

## Declared ties

`axes.json` declares 85 proposed attributes and five declined public attributes. Every group names an actual qualified SysML attribute and its complete emitted input-key set. For this assembly, each declared attribute emits one `design_attribute` key in the plant parameter group. Its multiple downstream uses bind to that same key; those consumers are not separate input axes. The source and generated-pipeline checks are recorded in `work/active/WI-098_whole-plant-conversion-comparison/evidence/study-axis-preparation.md`.

There are no cross-attribute ties. Equal compressor ratios, cooler/recuperator/price tuples, coordinated efficiency offsets, common quote factors and paired branch service changes are explicit scenario choices among independent attributes. The two branch controllers are separate equipment offers. The finance owner and steam-named shared operating/lifecycle owners feed both branches through authored bindings; no retired gas finance or shared-load keys are invented.

Stock indicators cover all 90 groups, including declined ones. A reachable constraint is only a possible path through a module. It does not establish an observed response or physical resistance. Monotonicity, same-quantity identity across names and intra-module operand dependence are not derivable from these indicators. Price, financial and performance scenarios remain sensitivities even when the graph reaches domain or economic predicates.

## Oracle

The independent development verifier owns the equations and predicate operands. `oracle_entry.py` exports `evaluate`, `comparison_catalog`, `operand_bindings` and `absolute_tolerances` without adding numerical science. Verification re-derives each executing verdict from the oracle operands and the sealed native predicate definition. It uses the established absolute and relative tolerances; failed engineering margins are not relaxed.

The work item's `evidence/independent-verification/native-check-final.json` verifies 32 evaluated development cases and three consistent domain refusals. `native-behaviors-final.json` records 88 behavior checks. The independent 498-control summary is separate evidence. The final study must still scan its actual candidate window and verify a verdict-stratified sample. Shared inherited property/body implementations are translation-parity evidence where reused, not additional independent source authority.

## Candidate range and validity masks

[INHERITED: predecessor finite conversion catalog] `proposals.py` selects source scenarios of 2500, 2800 and 3000 MW, gas flows of 1500–2500 kg/s, individual stage ratios of 1.2–1.8 and five named cooler/recuperator/service-price offers. The steam catalog selects 10, 11, 12 or 14 circuits, two to four pumps per circuit and selected pump flows of 225 or 250 kg/s. These form 375 gas rows and 24 steam rows per steam anchor. They are finite engineered offers, not sourced continuous operating envelopes or a global optimum.

[AGENT] `scenarios.py` declares shared quote, installation allowance, overhead, discount, availability, lifecycle, service, import-price, breeding/fuel-price, electrical-efficiency, residual-load and cryogenic-heat sensitivities. Joint efficiency stresses rerun complete catalogs. These bounds are engineered stresses, not qualified uncertainty intervals. Dynamic common-quote membership is checked against the actual 637-input baseline; all 28 selected common-account factors remain separately declared axes.

The oracle scans each changed window from the current feasible anchor before fixing the native list. There is no validity mask and no external source, flow, ratio, sizing or matching solver. Numerical results with failed native predicates remain failed candidates. Refused property/domain evaluations retain their full inputs and refusal reasons in the scan. Ranking requires the applicable native equipment, supported-domain, energy and economic admission checks; zero LCOE on an invalid energy denominator cannot rank. A matched operating point requires both branches to pass at the same source and common assumptions. The 3000 MW point retains the selected primary-pressure and divertor failures.

## Declined axes and frozen reactor scenario

The three public steam temperature attributes and salt-pump head remain declared but declined. The reviewed steam property point is 445/445/42 °C; this catalog does not supply new property/equipment offers for varying it. The primary circuit count is also declared but declined: the fixed selected inventory has 14 paths, and changing that count alone fails the native inventory-identity guard. These are five real input groups, all included in indicator coverage.

A reactor geometry or fusion-sizing search is declined at the model boundary. Major/minor radius, winding dimensions, turn current and peak field belong to the retained full-source capture route; they are not editable public attributes of this isolated assembly. Fusion power here is a calculated consequence of supplied hot heat and the declared multiplier/heating assumptions, not an input axis. No fake geometry/fusion input keys are declared. Changing the source demand does not reconstruct a self-consistent plasma design or reprice fixed magnets, cryoplant or primary inventory.

The selected 48 kA capture has 8.64 T axis field and 23.904 T peak field. The failed 50 kA offer and altered full-plasma failures remain in the work-item evidence. Captured identity and hardware are fixed; quote factors change declared prices only. Cryogenic demand varies at the selected 40/60 kW offer and its fixed quote. The transferred 35.5 W/m³ heat assumption, 50 W/m³ reference stress and 80 W/m³ adverse case do not establish a neutronics uncertainty bound. Nuclear transport qualification remains zero.

## Accounting and claim limits

Both branches include their conversion equipment, the same major reactor/source inventory, applicable overheads, purchased fuel, operating imports, routine and conversion service, replacement events, outages and terminal accounts. One shared finance owner controls initial construction finance and all discounted event ledgers. Construction finance applies only to initial eligible spending. The exact disjoint account mapping in the work item's `configuration.md` is authoritative; some generated descriptive CAS labels are incorrect and do not drive executable totals. Gas transport overhead uses the retained installed-cost proxy that includes inseparable helium stock.

The supplied-source, nuclear-transport and global-construction qualification flags remain zero. A passed implemented equipment predicate does not validate plasma sustainment, changed-geometry transport, global assembly or actual vendor prices. Source installation allowance and common quote/load stresses expose material economic assumptions. The auxiliary sink remains a priced, rated offer; uncertain heat cannot disappear into an unlimited sink. The effective hot-source multiplier excludes cryogenic nuclear deposition.

Study conclusions are conditional comparisons of declared finite offers. They do not certify a complete reactor, equally optimized technologies, a global minimum or an unconditional procurement recommendation. Unsupported component performance and failed native admission checks remain outside ranking; the conditional source premise must accompany every economic conclusion.
