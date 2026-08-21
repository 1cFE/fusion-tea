# Diff: 07-maglif

**Generated:** 2026-05-22T09:48:52-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 3 | 3 | 0 |
| important_count  | 0 | 8 | - |
| overall_rating   | Mostly Ready | Mostly Ready | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
148:2. **ARPA-E ALPHA program costing studies** — The ALPHA program (2014–2018) funded MIF concepts; some results are in `revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts` (already registered). Read this fleet-wide source — it likely contains MIFE/MagLIF-adjacent cost frameworks at the ARPA-E level. **Recommended: read `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/output.md`**
152:4. **Hawker simplified IFE economic model** — `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/` provides a 14-parameter Monte Carlo model directly applicable to MIF concepts (parametric over gain, yield, rep rate, conversion efficiency). Highly relevant for sensitivity analysis. **Already in fleet-wide index; recommend reading.**
```

## Blocking-tier lines (baseline)

```
(none)
```

## Blocking-tier lines (new)

```
53:- Target fabrication cost at 0.1–1 Hz production rate — `proprietary` — **blocking** for LCOE model; must use analog (General Atomics laser IFE target cost × 2 from Z-IFE model, or Hawker simplified model parameter range)
77:- TRL for integrated rep-rate operation (target + RTL + chamber clearing + re-shot) — `truly-unknown` (not yet demonstrated at any rep-rate in integrated configuration) — **blocking** for credible capacity factor estimate
100:- IMG capacitor/switch cost trajectory and replacement schedule — `proprietary` — **blocking** for driver O&M cost
132:| Commercial IMG driver capital cost | proprietary | blocking | Pacific Fusion claims "5x cheaper" than LTD but gives no $/J for commercial IMG; $372M Z-IFE LTD is the only data point |
133:| Target fabrication cost at commercial scale | proprietary | blocking | Z-IFE used GA laser IFE analogy ×2; Pacific Fusion claims dramatically lower cost but gives no number |
134:| IMG capacitor/switch replacement schedule and O&M | proprietary | blocking | Millions of shots needed; current prototype data insufficient for commercial extrapolation |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/07-maglif.md	2026-05-22 09:21:13.839480284 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/07-maglif/gap_report.md	2026-05-22 09:48:52.958763902 -0700
@@ -1,39 +1,179 @@
-Here is the gap assessment, written to `analyses/07-maglif/gap_report.md`. Key findings:
+I now have enough information across all sources to write the gap assessment. Let me compile it.
+
+# Gap Assessment: MagLIF (D-T)
+
+## Overall Readiness
+**Rating**: Mostly Ready
+
+**Summary**: MagLIF (D-T) has unusually strong physics and engineering documentation for a pre-commercial concept — the Z-IFE plant study (SAND2006-7148) provides a complete costed plant model, and Pacific Fusion's 2025 AMPS paper covers the physics basis, DS architecture, and a commercial roadmap with explicit engineering requirements. The primary gaps are commercial-scale capital cost breakdowns (proprietary, unavailable) and power-plant-specific tritium breeding details. The February 2026 Pacific Fusion breakthrough (self-magnetizing targets eliminating external coils) materially changes the architecture assumptions from the Z-IFE baseline, requiring careful handling when adapting Z-IFE cost data. A D1+ analysis is feasible now with explicit assumptions bridging the 2006 Z-IFE model to the modern IMG-based concept.
+
+---
+
+## Section Coverage
+
+### 1. Availability of Data
+
+**Coverage**: Good
+
+**Available**:
+- Peer-reviewed physics basis: arXiv:2408.15206 (community white paper, 2024) and arXiv:2504.10680 AMPS paper (Pacific Fusion, 2025) cover MagLIF physics from first principles with validated scaling relations
+- 70+ fusion-producing experiments on Sandia Z Machine provide an experimental track record unmatched by most private fusion companies
+- SAND2006-7148 (Z-IFE) is a complete plant study with integrated systems cost model including driver, chamber, blanket, RTL, target factory, and balance of plant — the most thorough pulsed-power fusion plant TEA in the public domain
+- Pacific Fusion has released multiple transparency pieces (founders' letter, Fusion Report interview, ANS coverage, breakthrough update, $900M fundraise announcement) with meaningful technical specifics (156 modules, 80 MJ stored, 60+ MA, 73×80 m footprint)
+- Fuse Energy Not Boring deep-dive gives TITAN I specs and Apeiron I hybrid concept details
+- The CATF IWG extension (arXiv:2602-19389) explicitly includes a MIFE pulsed-power cost account (Section 7.3.3) applicable to MagLIF
+
+**Missing**:
+- No published commercial plant study from Pacific Fusion or Fuse Energy (commercial TEA deferred explicitly to "subsequent papers" per AMPS paper)
+- Z-IFE study uses LTD (linear transformer driver) architecture, not IMG — direct cost transfer to modern IMG-based designs requires bridging assumptions
+- Company-specific LCOE projections are entirely private
+
+**Gaps**:
+- No commercial-scale Pacific Fusion plant study published — `proprietary` — **important** (limits quantitative precision; Z-IFE provides workable analog)
+- Fuse Energy pure-fusion (non-Apeiron-I) plant design undisclosed — `proprietary` — **nice-to-have**
+
+---
+
+### 2. Challenges in Capturing System Function
+
+**Coverage**: Good
+
+**Available**:
+- The key system-function challenge — pulsed energy delivery at rep rate, target destruction and replacement, RTL recycling — is extensively documented in Z-IFE SAND2006-7148 (Section 3.5: Automation, RTL cycle times Table 4.6) and arXiv:2408.15206 (Section 7: Chamber design and engineering)
+- AMPS paper Section 4 covers commercial engineering requirements in detail: component lifetime (Section 4.1), fusion chamber design with replaceable electrode disassembly (Section 4.2), chamber pumping and reloading, post-shot impulse response, and tritium breeding (Section 4.3)
+- The pulsed-power uniquely couples driver to target (electrical, not optical), creating both advantages (mm-scale positioning vs. 10-μm for laser, no line-of-sight optics damage) and challenges (RTL must sublimate during pulse, chamber debris management)
+- Self-magnetizing target breakthrough (Feb 2026) eliminates external coil subsystem, simplifying architecture but requiring updated cost basis for targets
+- Shock mitigation to protect chamber walls is well-documented — thick liquid FLiBe curtain (baseline), gas, aerosol alternatives all studied in SAND2006-7148 Section 4
+
+**Missing**:
+- Quantified target fabrication cost at commercial rep rate not published; only qualitative claims of "low cost" and analogy to "22-caliber bullet casings"
+- Commercial chamber clearing timescale and automation specifications not validated beyond concept level
+
+**Gaps**:
+- Target fabrication cost at 0.1–1 Hz production rate — `proprietary` — **blocking** for LCOE model; must use analog (General Atomics laser IFE target cost × 2 from Z-IFE model, or Hawker simplified model parameter range)
+- RTL per-shot cost and remanufacturing economics at commercial scale — `derivable` from Z-IFE analysis with stated assumptions — **important**
+- Chamber debris clearing rate at 0.5 Hz not experimentally demonstrated — `truly-unknown` — **important** for capacity factor
+
+---
+
+### 3. Maturity of Key Subsystems and Components
+
+**Coverage**: Partial
+
+**Available**:
+- **Driver (IMG)**: TRL 4-5. Sirius-1 prototype (4-stage, 8-brick, 60 GW) demonstrated. Pacific Fusion has tested individual module components meeting specs (announced April 2025). Full production-scale module test planned before DS construction. TITAN I (Fuse, 238 bricks, 1 TW) is operational
+- **Target physics**: TRL 3-4. 70+ D-D experiments on Z at 20 MA; χ=0.084 demonstrated; self-magnetizing target concept validated experimentally (Feb 2026, 22 MA on Z). D-T ignition-scale experiments remain ahead of DS completion (targeting 60 MA)
+- **Thick liquid blanket / FLiBe**: TRL 2-3. Z-IFE characterization of frozen FLiBe properties, FLiBe-steel interactions, and basic flow dynamics conducted (SAND2006-7148 Sections 3.3-3.4). Not demonstrated at rep-rate
+- **RTL (recyclable transmission line)**: TRL 2-3. Conceptual design done; RTL cycle time ~30 s analyzed; physical demonstration at rep-rate not completed
+- **Thermal conversion**: TRL 6-7 (conventional); heat exchanger and Brayton/Rankine cycles mature from conventional energy sector; specific Z-IFE integration not demonstrated
+- **Automation and rep-rate operation**: TRL 2. Fuse Energy demonstrated >0.1 Hz on TITAN I for repetitive shots (100+ shots claimed); full automation not demonstrated
+
+**Missing**:
+- No systematic TRL table published by either company
+- FLiBe tritium recovery at power-plant scale not experimentally demonstrated
+- Target injection at rep-rate not demonstrated
+
+**Gaps**:
+- TRL for integrated rep-rate operation (target + RTL + chamber clearing + re-shot) — `truly-unknown` (not yet demonstrated at any rep-rate in integrated configuration) — **blocking** for credible capacity factor estimate
+- Tritium breeding blanket at power-plant scale — `not-yet-sourced` (ITER and fission molten salt literature would help) — **important**
+- MITL (magnetically insulated transmission line) lifetime and replacement schedule at commercial rep rate — `derivable` from Z-IFE analysis extended to IMG architecture — **important**
+
+---
+
+### 4. Key Materials and Supply Chain Considerations
+
+**Coverage**: Partial
+
+**Available**:
+- **Capacitors and switches**: Identified in arXiv:2408.15206 as the critical supply chain bottleneck. "Energy storage and switching component replacement lifespan must extend by at least a factor of 1000 at Hertz operating rate. Cost of energy storage and switching must decrease by a factor of 5 to 10." Commodity capacitors used in IMG architecture enable mass manufacturing but multi-million shot lifetime is unproven
+- **Tritium**: arXiv:2408.15206 and AMPS paper both note need for tritium-producing blanket; Z-IFE identified FLiBe as baseline breeder; Z-IFE tritium permeation analysis done for piping (SAND2006-7148 Section 3.3)
+- **Chamber materials**: Z-IFE identifies F82H steel as baseline chamber material; analyzed for neutron activation, radionuclide inventory (Tables 4.7-4.10), and fatigue
+- **Blanket material (FLiBe)**: Characterized chemically and electrically; FLiBe-steel interaction studied under pulse conditions
+- **Target materials**: Aluminum and plastic (self-magnetizing target), beryllium-free — no exotic materials. Target materials are straightforward compared to ICF hohlraums
+
+**Missing**:
+- Mass manufacturing cost trajectory for IMG capacitors and switches (the dominant supply chain concern) is not quantified publicly
+- Li-6 enrichment requirements for FLiBe blanket tritium breeding not specified for Pacific Fusion commercial design
+- FLiBe supply chain (beryllium sourcing) not addressed in company materials
+
+**Gaps**:
+- IMG capacitor/switch cost trajectory and replacement schedule — `proprietary` — **blocking** for driver O&M cost
+- Li-6 enrichment requirement and cost for commercial blanket — `not-yet-sourced` — **important** (search ITER tritium breeding analyses)
+- Beryllium supply chain concerns for FLiBe (BeF₂ component) — `derivable` from ITER/molten salt reactor literature — **nice-to-have**
+
+---
+
+### 5. LCOE Parameter Extraction
+
+**Available Parameters**:
+
+| Parameter | Value/Range | Source | Confidence |
+|-----------|-------------|--------|------------|
+| Plant electrical output | 1000 MWe (Z-IFE baseline); 250 MWe mentioned by Pacific Fusion | SAND2006-7148; ANS 2025 | m |
+| Repetition rate | 0.1 Hz (Z-IFE baseline); 0.5 Hz stretch; ~1 Hz Pacific Fusion target | SAND2006-7148; arXiv:2408.15206 | m |
+| Target yield (commercial) | 2–30 GJ (Z-IFE range); ~4,600 MJ at 0.5 Hz/1 chamber | SAND2006-7148 | m |
+| DS target yield (demo) | ~60 MJ (Qf>1 demonstration, not commercial) | AMPS paper arXiv:2504.10680 | h |
+| Driver stored energy (DS) | ~80 MJ | AMPS paper; Pacific Fusion interview | h |
+| Driver delivered to target | ~8 MJ (10% of stored) | AMPS paper | h |
+| Driver wall-plug efficiency | ~90% (IMG); 60% (LTD baseline) | arXiv:2408.15206; SAND2006-7148 | h/m |
+| Thermal-to-electric efficiency | 42% (steel F82H chamber); 50% (carbon composite) | SAND2006-7148 | m |
+| Plant capacity factor | 85% (Z-IFE assumption) | SAND2006-7148 | l (unvalidated) |
+| Driver capital cost (LTD) | $372M per 1 PW LTD; ~$15/J unit cost | SAND2006-7148 | l (2006, LTD not IMG) |
+| COE range (Z-IFE) | 7–20 ¢/kWh depending on chambers/rep-rate/yield | SAND2006-7148 | l (2006, old architecture) |
+| Indirect cost factor | 93.6% of direct capital (consistent with ARIES) | SAND2006-7148 | m |
+| Fixed charge rate | 9.66% | SAND2006-7148 | m |
+| Annual O&M | Included in Z-IFE model (not broken out quantitatively in extracted text) | SAND2006-7148 | l |
+| Neutron energy fraction | ~80% as 14 MeV neutrons, ~20% alphas | arXiv:2408.15206 | h |
+
+**Missing Parameters**:
+
+| Parameter | Gap Type | Criticality | Notes |
+|-----------|----------|-------------|-------|
+| Commercial IMG driver capital cost | proprietary | blocking | Pacific Fusion claims "5x cheaper" than LTD but gives no $/J for commercial IMG; $372M Z-IFE LTD is the only data point |
+| Target fabrication cost at commercial scale | proprietary | blocking | Z-IFE used GA laser IFE analogy ×2; Pacific Fusion claims dramatically lower cost but gives no number |
+| IMG capacitor/switch replacement schedule and O&M | proprietary | blocking | Millions of shots needed; current prototype data insufficient for commercial extrapolation |
+| Commercial tritium breeding blanket design | proprietary | important | Pacific Fusion has not disclosed commercial blanket; Z-IFE FLiBe is the only public design |
+| Commercial plant footprint and site cost | proprietary | important | DS is 73×80 m; commercial plant larger/different; no published data |
+| RTL per-shot cost and factory throughput | derivable | important | Z-IFE has model but based on LTD/flibe RTL architecture that may differ from IMG approach |
+| Chamber first-wall replacement schedule | derivable | important | Z-IFE provides fatigue analysis for F82H; Pacific Fusion commercial design unspecified |
+| Recirculating power fraction for commercial plant | derivable | important | Z-IFE 2006 model uses 85% capacity and 4% aux power; needs update for IMG efficiency |
+| Tritium breeding ratio and inventory | not-yet-sourced | important | Qualitatively acknowledged; no TBR calculation for Pacific Fusion commercial design |
 
 ---
 
-## Overall Readiness: **Mostly Ready**
+## Source Recommendations
+
+1. **Pacific Fusion commercial TEA paper** — Pacific Fusion AMPS paper (arXiv:2504.10680) explicitly defers technoeconomics to "subsequent papers." Monitor arXiv physics.plasm-ph for follow-on publications. `not-yet-sourced` — **unverified existence; flag as future work**
 
-The most important correction to the prior draft: SAND2006-7148 is **already substantially extracted** (277 KB) and contains real LCOE data — COE estimates of **7–20 ¢/kWh** depending on configuration, driver capital of **$372M/1 PW LTD**, thermal efficiency **42–50%**, and capacity factor **85%**. These are now in the Available Parameters table and the "blocking" flags for those items have been removed.
+2. **ARPA-E ALPHA program costing studies** — The ALPHA program (2014–2018) funded MIF concepts; some results are in `revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts` (already registered). Read this fleet-wide source — it likely contains MIFE/MagLIF-adjacent cost frameworks at the ARPA-E level. **Recommended: read `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/output.md`**
 
-### What's available for each section:
+3. **CATF IWG pyFECONS MIFE extension** — arXiv:2602-19389 Section 7.3.3 explicitly develops a pulsed-power cost account for MIFE in the standard CAS framework. This is the most current public methodology for costing MagLIF-class concepts. **Recommended: read `knowledge/concept_research/07-maglif/iter-03/sources/arxiv-2602-19389.md` Section 7.3.3 in full.**
 
-| Section | Coverage | Key assets |
-|---------|----------|-----------|
-| Data availability | Moderate | arXiv:2408.15206 (physics/IMGs), Pacific Fusion interview (DS specs), Fuse Not Boring (TITAN/Z STAR), SAND2006-7148 (full plant study) |
-| System function challenges | Partial | Energy partitioning, pulsed-system logistics, coupling efficiency, IMG vs. legacy architecture |
-| Subsystem TRL | Partial | IMGs (TRL 4-5), target physics (TRL 3-4), FLiBe blanket (TRL 2-3), RTL automation (TRL 2) |
-| Materials/supply chain | Partial | FLiBe/Li-6, capacitor bottleneck (arXiv explicitly calls this out), liner simplicity |
-| LCOE parameters | Partial | Full SAND2006-7148 cost model available; missing commercial rep rate, yield, and coupling efficiency |
+4. **Hawker simplified IFE economic model** — `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/` provides a 14-parameter Monte Carlo model directly applicable to MIF concepts (parametric over gain, yield, rep rate, conversion efficiency). Highly relevant for sensitivity analysis. **Already in fleet-wide index; recommend reading.**
 
-### Remaining blocking gaps for the LCOE model:
-1. **Commercial rep rate** — 0.1 vs. 1 Hz swings COE by ~3× (both bounded by available data)
-2. **IMG driver capital cost** — derivable from LTD baseline with arXiv's stated 5× reduction factor
-3. **Commercial coupling efficiency** — demo is ~10%; commercial target unknown but constrains effective Q
+5. **ITER tritium breeding and inventory analysis** — Search OSTI for ITER tritium plant design and TBR requirements to establish FLiBe breeding reference. `not-yet-sourced` — `unverified — confirm existence before searching`
 
-The Z-IFE SAND2006-7148 study provides the structural template; the analysis just needs explicit stated assumptions for translating from LTD to IMG architecture.
+6. **General Atomics target fabrication cost study for laser IFE** — Z-IFE cites a GA detailed study on direct-drive laser IFE capsule costs, which was then doubled as MagLIF proxy. This is cited as Reference [14] in SAND2006-7148. Search OSTI for GA laser IFE target factory cost studies ~2003-2006. `not-yet-sourced` — `unverified — confirm existence before searching`
+
+---
+
+## Summary
+
+MagLIF (D-T) is **mostly ready** for a D1+ analysis. The combination of SAND2006-7148 (complete plant cost model with COE results), arXiv:2504.10680 (current physics and engineering roadmap), arXiv:2408.15206 (comprehensive technical review), and Pacific Fusion/Fuse company disclosures provides enough to construct a parameterized LCOE model with stated assumptions. The three blocking gaps — commercial driver cost, target fabrication cost, and component replacement schedule — are all proprietary and cannot be resolved from public sources, but can be handled with sensitivity ranges anchored to the Z-IFE baseline (LTD $15/J) and Pacific Fusion's claimed 5× cost reduction. Before starting the analysis, read the CATF IWG MIFE cost account section (arXiv:2602-19389 §7.3.3) and the Hawker simplified IFE model — both are already in the repo and are directly applicable to building the LCOE model's cost structure.
+
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Mostly Ready"
 blocking_count: 3
-important_count: 0
-counting_method: "manual_prose_count"
+important_count: 8
+counting_method: "deduplicated across all sections; blocking = commercial driver $/J, target fabrication cost at scale, capacitor/switch O&M; important = integrated rep-rate TRL, tritium breeding blanket design, commercial plant capital cost breakdown by CAS, RTL per-shot cost, chamber first-wall replacement, recirculating power fraction, TBR/tritium inventory, commercial site footprint"
 section_coverage:
-  availability_of_data:       "Unknown"
-  system_function:            "Unknown"
-  subsystem_maturity:         "Unknown"
-  materials_supply_chain:     "Unknown"
-  lcoe_parameter_extraction:  "Unknown"
-```
+  availability_of_data:       "Good"
+  system_function:            "Good"
+  subsystem_maturity:         "Partial"
+  materials_supply_chain:     "Partial"
+  lcoe_parameter_extraction:  "Partial"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
