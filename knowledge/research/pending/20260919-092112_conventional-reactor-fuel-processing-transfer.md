---
date: 2026-09-19
researcher: Codex cost_basis
topic: Conventional reactor processing capacity transfer
research_type: domain
tags: [fuel-processing, source-applicability, ITER, cryogenic-distillation]
---

# Conventional reactor processing capacity transfer

## Result and proposed transfer

[AGENT] Primary ITER engineering designs do support conventional exhaust cleanup followed by cryogenic isotope separation at greater molecular feed than the existing stellarator's approximately13kg D+T/day. This resolves the narrow concern that the source process exists only at the smaller TSTA scale. It does not validate the ORNL price exponent empirically or establish this stellarator's feed conditioning. A conditional conventional-process costing scenario is now technically supportable for independent review.

[AGENT] Proposed scenario: all represented plasma exhaust D+T enters conventional fuel cleanup, with palladium-alloy permeation and impurity treatment, then a cryogenic isotope-separation cascade producing reusable D/T fuel. Use the existing operating D+T feed as the ORNL cost driver; retain 99% represented recovery and all existing fuel-loss assumptions. Do not reduce capacity using annual availability, replace processing with direct internal recycle, change stock residence assumptions, or add arbitrary parallel trains. The technology is an explicit new cost-scenario premise because the model currently specifies functions rather than selected hardware. Whether accepting it is a major process-technology choice remains the owner's reserved judgment; the report does not settle that decision.

[AGENT] The source-compatible condition for that scenario is a near-equimolar primary isotope stream with source-like minor impurities, cleaned to the original TSTA ISS requirement of less than1ppm noncondensibles, with the original roughly1mol%protium primary feed as the costing reference. The new ITER designs show that somewhat greater protium burdens and richer separation duties can be engineered at larger scale. They do not show that arbitrary impurities can be ignored or priced by D+T mass alone. Feed composition/conditioning must be stated as an external applicability condition, not as something the current flow model verifies. Failure to meet that condition invalidates the transferred cost scenario.

## Primary evidence

| Source | Observed evidence | Durable source |
|---|---|---|
| Ladd et al., *ITER Fuel Cycle*, IAEA conference paper | Page1 names50/50DT as nominal fueling composition. Page3 specifies317mole/hour processing for later3000s pulses, versus about100mole/hour time-averaged processing early in operation. The front end uses Pd/Ag permeators and impurity detritiation before isotope separation. Page4 explicitly describes steady-state tritium-plant operation during long pulses and reuse of D2,DT,T2 products. | `knowledge/sources/ladd_et_al_iter_fuel_cycle_conventional_long_pulse/`; URL https://www-pub.iaea.org/mtcd/publications/pdf/csp_008c/pdf/iterp_12.pdf; raw SHA256 `56880453c4bd069d62dd9db44e115ff07962f2dda5ebb1ff66e216063cd4a00a` |
| Iwai, Yamanishi and Nishi, *Study on Cascade Configuration and Hydrogen Isotope Inventory of Cryogenic Distillation Columns for Isotope Separation System of the ITER Tritium Plant*, JAERI-Tech2000-002 | English abstract describes four-column design for ITER-FDR steady-state10000s operation at200Pa·m³/s fueling. Section3.1 gives plasma feed320mol/h,5%H, D/T from50:50 to75:25 after removal of noncondensibles including C and He. Separate feeds are20mol/h from water processing and40mol/h from NBI. Table1 lists exact molecular fractions. | `knowledge/sources/iwai_yamanishi_nishi_jaeri_tech_2000_002_iter_cryogenic/`; original URL https://www.osti.gov/etdeweb/servlets/purl/20063405 |

Original images were inspected: Ladd PDF indices0,2,3; JAERI English abstract index3, Japanese design conditions indices10–11, and Table1 index25. The JAERI main text is scanned Japanese; its numerical design conditions and Table1 were read directly, not inferred from lossy extraction. The English abstract independently states the four-column technology and operating duty. The molecular-fraction columns H2,HD,HT,D2,DT,T2 establish that mol/h denotes molecules, not atomic moles.

[SOURCE FACT] JAERI Table1's equal-D/T case is H/D/T atomic fractions5/47.5/47.5%, with320mol/h total molecular feed. The table's other plasma cases are5/57/38 and5/71.25/23.75. A320mol/h flow is the plasma-exhaust stream alone; do not add the separate water/NBI streams when comparing that primary capacity to the existing plasma-exhaust function. Four interlinked columns form a process cascade, not redundant trains.

## Capacity comparison and duty

[INHERITED: fuel-inventory-and-startup/evidence/throughput-interface.md] Operating exhaust processing is12.911794045kg D+T/day with7.742681kg T/day. [AGENT CALCULATION] Using nominal5g/mol for equimolar D+T molecular gas, this is107.5983mol/h. Using actual isotope molecular masses changes it by less than1%; exact code verification should use the same masses as the producer. The JAERI design's320mol/h with95%of its atoms D+T corresponds to approximately36.48kg D+T/day at equal D/T, about2.825times the current demand. This is a conceptual envelope comparison; it is not an adopted plant throughput limit or physical sizing calculation.

[AGENT] The present case is also below the Ladd317mol/h long-pulse requirement. It is above Ladd's early100mol/h time-averaged case. Therefore only the later duty is relevant. Neither source demonstrates year-round plant reliability:3000s and10000s pulses are finite. Both explicitly consider steady processing during those pulses, so the comparison concerns instantaneous operating capacity, not annual-average duty. Continuous-service maintainability and spare capacity remain conditional, with no unsupported redundancy allowance.

## Why this can support ORNL transfer

[AGENT] The joined argument is: ORNL explicitly supplies a reactor-oriented feed-based engineering cost method; TSTA anchors its historical subsystem equipment/cost scope; independent ITER design work extends the same class of cleanup and cryogenic-separation functions above the present isotope flow. Thus the present flow is not being extrapolated into a process regime shown only by the TSTA experiment. This is a reasoned conceptual transfer, not a claim that ITER validates the historical0.3 cost exponent or that ITER hardware costs equal TSTA prices.

[AGENT] Retain ORNL's exact1.79712kgDT/day cost reference and row-specific0.3 exponent. The new process evidence does not supply replacement coefficients, modern prices or an independent economic scaling fit. Do not infer a new exponent, a certified320mol/h limit or a cost multiplier from the capacity ratio. Price-year conversion remains separate work.

## Necessary boundaries and remaining assumptions

- [AGENT] **Cleanup scope:** conventional treatment must actually remove helium and impurities before cryogenic separation. Isotope mass is the source's costing proxy, while raw total-gas composition remains an applicability condition. Assume source-like feed burden only as an explicit conditional scenario; no assertion that unmodeled impurity mass is zero.
- [AGENT] **Separation service:** near-equimolar D/T is compatible with the primary source feed, but product purity and protium removal still matter. Preserve a conventional separation-service allowance; do not subtract expensive columns just because the plant only needs remixed DT.
- [AGENT] **Pressure and temperature:** retain the TSTA cost reference's near-atmospheric cryogenic service and20K-class refrigeration. These new capacity papers do not justify changing cost to high-pressure operation. No source transfer to arbitrary pressure is claimed.
- [AGENT] **Recovery:** existing99%functional recovery is preserved, but these source comparisons do not certify that recovery for a particular feed. No throughput decrease from an invented bypass is justified.
- [AGENT] **Blanket stream:** this scenario prices the already represented plasma-exhaust cleanup/separation function. Helium/PbLi extraction remains a separate function. Recovered blanket T is not assigned an invented D companion or raw gas volume. If it joins ISS, its conditioning/composition and actual additional isotope flow need an explicit interface and cost scope before claiming that branch is covered.
- [AGENT] **Account replacement:** the two process rows exclude parts of containment, transfer pumps, analytical equipment, storage, buildings and safety equipment. Replacing a broader processing-plus-containment account requires an explicit coverage decision. New process-size evidence does not cure omitted equipment or installation-design charges.
- [AGENT] **Technology choice:** an owner-accepted conditional conventional-process scenario is narrower than a detailed hardware redesign. The coordinator and fresh reviewer must decide whether this is an acceptable interpretation of the authorized S2 work or crosses the reserved major-technology gate.

## Acquisition and limits

Native request `knowledge/research/requests/REQ-fuel-processing-transfer-02.json`; run `knowledge/research/requests/runs/REQ-fuel-processing-transfer-02/20260919T161649033371/`. Six targeted searches were used. Two native capture/registration slots were used for the Ladd and JAERI primary sources. Before registration, source dates/titles and token screening were checked. No barred source was opened.

A screened ITER Engineering Basis Handbook chapter was also read in scratch as corroboration: https://www.iter.org/sites/default/files/media/2026-01/vol.1_ch.04_role_and_distinctive_feature_dv4qgd_v2_0.pdf, printed pp.57–58, describes steady-state exhaust processing and cryogenic separation for ITER/power-reactor throughput. It was not registered because the two capture slots were prioritized for explicit primary design-capacity evidence. It is not needed for the proposal's quantitative claims. Search results for a later simulation, JAERI journal version and ITER design requirements were not adopted as substitute cost evidence.

[AGENT] Submit this joined transfer proposal to the same fresh reviewer. If its remaining feed/technology conditions are acceptable as a conditional S2 scenario, proceed to price/accounting work. If those conditions require an owner choice, present the conventional scenario and its precise limits. Do not call the whole fuel plant priced or S2 achieved from this research alone. No model files, goal records or approved insights were changed by this task.
