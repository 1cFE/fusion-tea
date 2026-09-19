---
date: 2026-09-19
researcher: Codex cost_basis
topic: Throughput-based DT processing capital source applicability
tags: [fuel-processing, capital-cost, throughput, source-applicability]
research_type: domain
---

# Throughput-based DT processing capital source applicability

## Recommendation

[AGENT] The strongest admissible relationship found is the historical reactor-oriented TETRA method in ORNL/FEDC-87/7, Section 4.5.6 and Table 4.24. It explicitly assigns fuel cleanup and cryogenic isotope separation a cost exponent of 0.3 against total D+T feed mass rate. This is a source-supported conceptual engineering algorithm, not an experimentally validated commercial-plant scaling law. Submit its applicability and accounting scope to the required fresh reviewer before implementation. Do not present source registration as scientific acceptance or claim S2 from this report.

[AGENT] A conditional estimate for the existing combined cleanup/isotope-separation function is possible if that review accepts transfer of the historical process technology and the extrapolation. The source's measured reference is smaller than this plant's flow; no validated scale range or replicated-train rule was established. If the reviewer requires a qualified power-plant capacity range, the concrete missing evidence is a documented design/cost basis or vendor estimate for a continuous approximately 13 kg D+T/day cleanup and isotope-separation train with the retained recovery requirement. No cost implementation is authorized by this research report itself.

## Authority and clean-room scope

[INHERITED: work/orchestration/goals/throughput-based-fuel-processing-costs/evidence/owner-prompt.md] The owner permits S2 aggregate processing costs, requires actual operating throughput and applicable sources, and forbids inventing exponents or assuming experimental hardware transfers directly to a power plant. Insight approval was not authorized. No DI was promoted. The prior inventory research supplies topology and flow semantics, not equipment prices. No conflicting fuel-processing DI was identified.

The quarantine protocol was read first. No sealed PDF, barred costing document, excluded concept, or barred derivative was opened. Searches excluded named barred topics where possible. Search listings included excluded or potentially mixed-source titles; these were not opened or adopted. Historical 1970s/1980s source dates establish separation from the later holdout design. The TETRA, ISS design and official PROCESS code texts additionally passed a token screen before content inspection; native registration applied its own guard. These checks supplement content judgment and do not imply that a token screen certifies applicability.

## Source identity and verification

| Source | Durable location | Verified original |
|---|---|---|
| R. L. Reid, editor, *ETR/ITER Systems Code*, ORNL/FEDC-87/7, April 1988 | `knowledge/sources/etr_iter_systems_code_ornl_fedc_87_7_1988/` | Original URL https://engineering.purdue.edu/CMUXE/Publications/AHR/R88ORNL-FEDC-87-7.pdf; SHA256 `23e24fb7e722fbb74eb6cff7212881c199f6d9707c9c7b3f5c89ec5398ba3754`; printed pp.128–132, PDF indices137–141; Table4.24 and p.130 rendered and visually checked. Existing extraction is image-heavy and must not replace original-page inspection. |
| Bartlit, Anderson and Rexroth, *Subsystem cost data for the tritium systems test assembly*, LA-UR-83-3415, 1983 | `knowledge/sources/bartlit_1983_tsta_subsystem_costs_original_osti_paper/` | https://www.osti.gov/servlets/purl/5435513; raw SHA256 `01ee45acad5e8796c02df945102f364e1f237be39dc9e9adb3dfd5549254f9b3`; original Tables I–III, PDF indices3,4,6, rendered and visually checked. |
| Bartlit, Denton and Sherman, *Hydrogen isotope distillation for the Tritium Systems Test Assembly* | `knowledge/sources/bartlit_denton_sherman_hydrogen_isotope_distillation_for/` | https://www.osti.gov/servlets/purl/6715858; raw SHA256 `1f3833667dd103f8a25fa114794a811f0c74ffd2a08aecf0563c0cc08cb0fa81`; feed/product, pressure/refrigeration and final-design pages at PDF indices2,4,5 rendered and visually checked. |

[AGENT] The source index had registered TETRA for facilities costing; the initial fuel-keyword search did not identify that existing source. External retrieval was correctly deduplicated against its raw hash. The duplicate receipt contains the existing path even though the native return's pre-existing entry emits null slug/path. Use the receipt and path above.

## Capacity and technology mapping

[SOURCE FACT] TETRA printed p.128 defines process feed as plasma exhaust plus fueler exhaust plus blanket exhaust. It sums computed D and T rates from other system modules; fractional plasma burn controls exhaust. It explicitly lists lithium-lead among blanket options. This is a reactor systems-code costing method, not a casual relabeling of electrical or fusion power. Printed pp.129–130 specify palladium-diffuser or molecular-sieve cleanup followed by cryogenic distillation and separate storage, analysis, monitoring, containment, waste treatment and control systems. A day means a 24-hour operational day.

[SOURCE FACT] Table4.24 footnote defines F as total D+T flow, reference `2.08e-5 kg D-T/s`, equivalent to `1.79712 kg D+T/day`. It separately defines a tritium-inventory driver for storage and room-volume driver for monitoring. These quantities cannot substitute for F.

[INHERITED: work/orchestration/goals/fuel-inventory-and-startup/evidence/throughput-interface.md] The represented cleanup/separation reference processes `12.911794 kg D+T/day`, including `7.742681 kg T/day`, during operation. Recovery is applied after entering processing. Carrier gas and impurities are not represented. Annual availability cannot reduce this capacity. [AGENT CALCULATION] The flow ratio to TETRA is `7.18471443198`; its `F^0.3` multiplier is `1.80685313392`. These are capacity comparison values, not an endorsed contemporary price.

[AGENT] Apply a cleanup/separation relationship to the represented exhaust boundary only if the scope is expressly limited to it. TETRA's full process feed also includes fueler and blanket exhaust. Do not silently claim those omitted branches are costed. Adding blanket-recovered tritium to isotope separation needs a documented interface and gas composition, rather than adding raw PbLi mass or relabeling the blanket inventory. No change to fuel-loss assumptions or direct-recycle fraction is supported here.

[SOURCE FACT] The original ISS design describes four interlinked continuous cryogenic columns. Its main cleaned feed is roughly equimolar D/T, `360 gram-moles/day D-T` plus `1 mol% H2`, with less than `1 ppm` total noncondensable impurities. Products include near-equimolar DT for refueling, high-purity D2 for neutral-beam service, high-purity T2 and a hydrogen-rich waste stream. Additional feeds/recycles serve the neutral-beam and water-recovery interfaces. Nominal column pressure is `101.35 kPa (760 torr)`. The early design refrigerator is `450 W at 20 K`; the later as-built cost paper lists `420 W at 20 K`. Preserve these as distinct design/as-built values. Redundant instrumentation is described; redundant processing trains or an N+1 design are not.

[AGENT] The existing equimolar DT architecture is chemically closer to this basis than a hydrogen-diluted blanket purge or water-detritiation plant, but missing impurity loading, cleanup outlet purity and product specification prevent a qualification claim. The source's extra product flexibility may overstate this plant's required separation service; that is not permission to remove equipment or discount cost without evidence.

## Raw costs and source relationship

[SOURCE FACT] TETRA Table4.24 reproduces these historical expenditure values. Its text describes algorithm outputs in 1986 US dollars; the table expressly retains the original expenditure years. The table values must not simply be called 1986 USD.

| Component | Raw capital, thousand USD | Raw installation, thousand USD | Capital expenditure year | Cost exponent and driver |
|---|---:|---:|---|---|
| Fuel cleanup | 1000 | 70 | 1980 | 0.3 on total D+T feed F |
| Cryogenic distiller | 1237 | 63 | 1978 | 0.3 on total D+T feed F |
| Transfer pumps | 111 | 112 | 1977 | 0.3 on F |
| Secondary containment | 182 | 30 | 1978–1982 | 0.3 on F |
| Storage beds | 60 | 10 | 1981 | 0.6 on tritium inventory, not feed |

[AGENT] For each accepted row, preserve `C_raw`, its year and the source exponent. A candidate structure is `C_year = C_raw * price_index(year)/price_index(raw_year) * (F/F_ref)^0.3`. Apply purchased/fabricated capital and installation components separately. A relevant engineering price-index series and the installation expenditure-year convention still need selection and traceability. Do not combine unlike raw-year dollars into a supposed reference-year total. No escalation series, present price or future contingency is established by this report.

[SOURCE FACT] TETRA p.130 explicitly adopts chemical-industry power functions: 0.6 for large units, 0.3–0.5 for small installations or extreme temperature/pressure processes, and zero for fixed costs. Table4.24 selects 0.3 for cleanup and cryogenic separation. Its references35–37 point to Peters/Timmerhaus, Aries/Newton (the chemical-engineering authors, unrelated to the holdout program) and Bartlit1983. This is an engineering modeling assumption published by the reactor-code authors; it is not a regression demonstrated over the present target range.

[SOURCE FACT] Bartlit1983 TableIII says cleanup costs are nearly independent of a plus/minus three-to-fivefold flow change and isotope-separation costs nearly independent of a plus/minus threefold flow change around `360 gram-moles DT/day`. Thus the primary facility paper alone does not establish the later 0.3 exponent or the 7.18-fold extrapolation. TETRA is the explicit authority for that later cost approximation. No supported maximum flow, minimum turndown or multiple-train economic rule was found. Do not invent modularization to turn the current point into an apparently validated one.

## Equipment and accounting scope

[SOURCE FACT] Bartlit1983 distinguishes capital, installation, staff, overhead, and installation design/inspection. Process design and small specialized fabrication partly sit in project staff costs rather than subsystem rows. TableI installation excludes installation design and inspection. Industrial-contract mechanical design/fabrication is in capital. These are historical constructed-subsystem costs, not bare catalog purchase prices and not all-in modern EPC totals.

[SOURCE FACT] Cleanup removes and decomposes impurities to recover D/T. Its row includes instruments/control and integrity testing; TableII inconsistently lists software in included and excluded columns, so software inclusion remains unresolved. Its glovebox and guaranteed purification are excluded. The isotope-separation row includes the refrigerator, integrity tests and LN2 distribution; guaranteed separation and LN2 storage dewars are excluded. Main analysis and tritium monitoring are separate subsystems. The explanatory text assigns the isotope-separation glovebox to that subsystem while other gloveboxes are mostly in secondary containment. Preserve that exception when summing containment.

[AGENT] A limited cleanup-plus-separation capital block can exclude existing vacuum evacuation, fueling hardware, isotope purchases, startup fuel stock, facilities, electrical backup and broad safety systems. It must still disclose the omitted transfer-pump, storage, instrumentation, controls, confinement and blanket-extraction costs. The current account reportedly includes processing and containment; wholesale replacement with the two-row estimate would remove containment coverage unless a separately justified retained/replacement scope is identified. The coordinator's account map owns that decision. Do not retain a hidden residual of the old power-based allowance and claim it is a derived processing price.

[AGENT] Source recurrence, replacement schedules, consumables and operational staffing are insufficient for added OPEX or replacement terms. Redundancy margin, design capacity margin, modern reliability and the guaranteed recovery/purity requirement remain unpriced. A capacity margin may be an explicit scenario assumption; it is not source-validated reliability.

## Other methods investigated

The twelve logged searches examined TSTA historical prices, official PROCESS/TETRA algorithms, ITER procurement prices, DEMO process architecture and broader isotope separation costs. TFCX search metadata supplies a 600–2000 g DT/day package estimate excluding design/engineering/installation; it does not solve the present scale issue. ITER procurement totals lack an applicable cost-versus-capacity law in the searched evidence. DEMO direct internal recycling changes process architecture and cannot be imported merely to obtain lower costs. Hydrogen-diluted blanket recovery and water detritiation have different feed composition and capacity drivers.

The official current PROCESS `acc2272` code was downloaded and screened clean before reading. It defines `wtgpd` from fusion reaction rate, two nuclei per reaction, mean fuel mass and seconds/day, then applies a 60 g/day reference and 0.67 exponent. That calculation is burn-consumption mass, despite the processing label. It is rejected as a direct mapping of the existing exhaust throughput. It was not registered or adopted; the original TETRA method is the useful source. Code URL: https://raw.githubusercontent.com/ukaea/PROCESS/main/process/models/costs/costs.py, inspected 2026-09-19, lines2344–2383 in the retrieved version.

## Native acquisition outcome and defects

Request: `knowledge/research/requests/REQ-fuel-processing-cost-01.json`. Run: `knowledge/research/requests/runs/REQ-fuel-processing-cost-01/20260919T160645691363/`. Twelve searches were logged, and four material capture attempts occurred: one unusable challenge page, the valid OSTI cost paper, the pre-existing TETRA duplicate, and the valid ISS design. The additional initial local-file precondition failure occurred before capture. The native close returned `REGISTERED` with the search limit reached, not a bounded negative. Candidate dispositions and receipts remain in the run directory.

**Unusable registration:** `knowledge/sources/bartlit_1983_subsystem_cost_data_for_the_tritium_systems/` contains only a UNT “Validating your request” challenge page. Its successful registration does not make it source evidence. Its raw hash is `9c70185c020dd5e3bca0163811d58ecc7d76258a95ac84753dfa839c5b33ebad`. The report and candidate triage reject it. The valid OSTI source above replaces its evidentiary role. The registry has no remove/update operation; no registry row or native receipt was manually rewritten.

The native return also retains a queued `/tmp/fuel-tsta.pdf` missing-file precondition from the first network-denied download. That transport issue was resolved by the later downloads and is not an outstanding scientific source request. Keep the native receipt as history; do not mistake that queue entry for missing cost evidence. Registration-tool quality defects are distinct from the scientific scale and scope limitations above.

## Proposed next step

[AGENT] Have the fresh applicability reviewer decide whether the TETRA reactor-oriented engineering method supports a conditional S2 estimate at the actual stream size, with explicit source-transfer limits. The review should require a declared process/purity boundary, replacement of overlap, dated price conversion and a preserved scale qualification. If it does, use total operating D+T flow, reproduce the source rows, vary real throughput separately from price and process assumptions, and retain the source-range limitation. If it does not, acquire a contemporary continuous-train cost/design envelope near13 kg DT/day. No unsupported commercial qualification or new process topology is recommended.

Candidate insight for later owner approval: a fuel-system cost driver must identify its stream and unit convention; total isotope feed, burned tritium, stored inventory and carrier-gas flow are not interchangeable. No insight approval is requested or applied in this delegated report.
