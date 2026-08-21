# Diff: 16-muon-catalyzed-fusion

**Generated:** 2026-05-22T10:19:22-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 6 | 5 | -1 |
| important_count  | 6 | 6 | - |
| overall_rating   | Insufficient Data | Significant Gaps | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
(none)
```

## Blocking-tier lines (baseline)

```
28:- Academic and historical μCF TEA literature — `not-yet-sourced` — **blocking**: would provide the only independent LCOE baseline
30:- Any independent system-level analysis — `not-yet-sourced` — **blocking**
52:- Alpha-sticking reduction mechanism — `proprietary` — **blocking**: this is the central unsolved physics problem; the analysis must bound it
78:- Energy recovery subsystem existence and TRL — `truly-unknown` — **blocking**: without this the energy balance claimed cannot be evaluated
79:- Integrated system test results — `truly-unknown` — **blocking**: no integrated system has been built
103:- Scalable replacement for diamond anvil cell — `truly-unknown` — **blocking**: PSI experiments use lab-scale pressure apparatus; no commercial analog identified
```

## Blocking-tier lines (new)

```
34:- Plant-level engineering design document — `proprietary` — **blocking**: without a design, capital cost estimation has no anchor
57:- Commercial D-T target design (scalable beyond diamond anvil cell) — `truly-unknown` — **blocking**: the fusion cell is one of the two major system components; no design concept is published
101:- Commercial fusion target material — `truly-unknown` — **blocking**: current diamond anvil cell approach is explicitly a test apparatus, not a scalable approach; commercial replacement is unspecified
126:| Capital cost by subsystem (CAS structure) | proprietary | blocking | No published breakdown; accelerator dominates but no cost given |
127:| O&M cost | proprietary | blocking | No plant-level operational cost estimate available |
128:| Capacity factor / availability | not-yet-sourced | blocking | SNS linac achieves 92% availability as analog; μCF-specific estimate absent |
131:| Muon source capital cost scaling | truly-unknown | blocking | No published cost model for active-target muon source |
132:| D-T fusion cell capital cost | truly-unknown | blocking | No commercial design exists to cost |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/16-muon-catalyzed-fusion.md	2026-05-22 09:21:13.854932289 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/16-muon-catalyzed-fusion/gap_report.md	2026-05-22 10:19:22.946411898 -0700
@@ -1,33 +1,39 @@
+I have all the information needed. The OSTI source is about the SNS SRF accelerator at ORNL (a useful TRL analog for the muon source), not a fusion economics study. No fleet-wide sources offer useful cost analogs for the dominant cost driver (muon production accelerator). Now I'll write the assessment.
+
+---
+
 # Gap Assessment: Muon-Catalyzed Fusion (D-T)
 
 ## Overall Readiness
-**Rating**: Insufficient Data
-**Summary**: The source base is extremely thin — three short company-generated or physics-background documents totaling ~6 KB. Acceleron has published no plant study, no cost breakdown, and no independent system-level analysis. The sole quantitative LCOE figure ($0.025/kWh) comes from a single slide claim with assumptions stated but no supporting model. The concept is in early R&D (energy breakeven targeted ~2030), and the most critical physics parameters (300 fusions/muon, 3 GeV/muon production cost) are undemonstrated targets, not validated measurements.
+**Rating**: Significant Gaps
+**Summary**: The physics of muon-catalyzed fusion is well-documented in peer-reviewed literature, and Acceleron's ARPA-E 2025 presentation provides a credible (if unvalidated) system-level LCOE target and key performance parameters. However, no plant-level engineering design or capital cost breakdown has been published — the concept sits at TRL 2–3 for commercial scale — making quantitative LCOE extraction reliant on high-level approximation rather than traceable parameter chains. A rich qualitative analysis is possible; a defensible quantitative LCOE requires explicitly flagging its speculative basis.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Poor
+**Coverage**: Partial
 
 **Available**:
-- Company-generated materials: ARPA-E BETHE presentation (July 2025) and company overview provide system-level intent, energy balance diagram, LCOE target, and roadmap
-- Physics background: Wikipedia-derived summary of muon catalysis mechanism, historical experiments (PSI, TRIUMF, RAL), and key parameters (alpha-sticking, fusions/muon at conventional conditions)
-- Experimental milestone: Oct 2024 PSI run with compressed D-T — 28 hours continuous fusion (proof-of-concept beam physics, not energy-positive)
-- Funding context: ARPA-E BETHE grants + $24M Series A (Dec 2024)
+- Acceleron ARPA-E 2025 presentation: system-level LCOE target ($0.025/kWh), recirculating power fraction (47%), muon energy cost target (3.4 GeV/muon), fusions/muon target (300), Brayton cycle BOP mention, LCOE parametric contour plot vs. beam energy and fusions/muon, revenue-from-heat-sales assumption, Brookhaven energy breakeven test timeline (~2030)
+- Acceleron company website: plant size target (~100 MW), partner labs (PSI, Fermilab, ORNL, Argonne), Series A funding ($24M closed)
+- Wikipedia physics article (`muon-catalyzed-fusion-physics.md`): comprehensive history, experimental best of 150 fusions/muon (Jones, LAMPF), alpha-sticking probability range (0.3–0.9%), conventional electrical energy cost per muon (~6 GeV), Kelly/Hart/Rose 2021 analysis (Q~130% thermal, ~14% electrical return at current parameters), Pusch recirculating-power alternative estimate (3–5× input vs. output)
+- PMC 2022 (Yamashita et al.): new kinetics model for CF in high-temperature compressed gas targets; shows cycle rate increases with temperature; directly relevant to Acceleron's high-density target concept
+- OSTI (SNS SRF Linac, ORNL): 10-year operational data for a ~1 GeV SC proton linac at 92% availability — relevant analog for the muon source accelerator; no cost data but establishes TRL reference
+- arXiv 2021 (Kamimura): sticking probability calculation 0.857%, slightly lower than literature (0.91–0.93%), relevant to fusions/muon ceiling
 
 **Missing**:
-- Peer-reviewed papers from Acceleron (none identified; company founded 2023)
-- Published plant studies or techno-economic analyses from any source
-- Independent analysis from national labs or academic groups
-- ARPA-E BETHE technical progress reports (may exist but not sourced)
-- Historical μCF plant studies from 1980s–90s literature (Soviet, LANL, TRIUMF groups did publish some)
+- No published plant design study (no ARIES- or SOMBRERO-equivalent)
+- No independent techno-economic analysis of Acceleron's approach
+- Norrønt (Norwegian competitor) technical publications not in source set
+- Pre-2021 JINR experimental data on muon energy cost (INIS record is metadata only — full content not extracted)
+- Historical accelerator cost scaling studies for proton linacs at GeV scale
 
 **Gaps**:
-- Academic and historical μCF TEA literature — `not-yet-sourced` — **blocking**: would provide the only independent LCOE baseline
-- ARPA-E BETHE progress reports — `proprietary/not-yet-sourced` — **important**: may contain engineering detail beyond the slide deck
-- Any independent system-level analysis — `not-yet-sourced` — **blocking**
+- Plant-level engineering design document — `proprietary` — **blocking**: without a design, capital cost estimation has no anchor
+- Independent techno-economic review of Acceleron's 47% recirculating power claim — `not-yet-sourced` — **important**: Pusch/Kelly estimates suggest 300–500% recirculating power at current physics; Acceleron's claim requires validation
+- Norrønt technical publications — `not-yet-sourced` — **nice-to-have**: competitive comparison would strengthen analysis
 
 ---
 
@@ -35,24 +41,22 @@
 **Coverage**: Partial
 
 **Available**:
-- Energy balance structure is documented: 3 GeV/muon → 300 fusions/muon → 25 MeV/fusion → 47% recirculating power fraction (from ARPA-E slide)
-- Key physics problem identified: alpha-sticking limits fusions/muon; historical ceiling 100–150, theoretical limit ~300
-- Accelerator design concept described: ML-optimized active-target with GEANT4 simulation, 64% assumed electrical-to-beam efficiency
-- Heat recycling concept noted (2.5 GeV recovered per muon)
-- Fusion cell concept: high-density D-T at 500–1000°C under compression
+- Alpha-sticking physics is well-understood: 0.3–0.5% sticking means theoretical ceiling of ~200–350 fusions/muon (Wikipedia); Acceleron targets 300 but only 150 demonstrated experimentally
+- Energy balance at system level is described by Acceleron at a high level: 3.4 GeV/muon in, 47% recirculating, Brayton BOP
+- Kelly et al. (2021) parametric analysis provides an independent model of the energy balance as a function of accelerator efficiency, fusions/muon, and heat conversion efficiency — a key secondary source for checking Acceleron's claims
+- PMC (Yamashita 2022) demonstrates that higher temperatures increase cycle rate, supporting Acceleron's high-density, high-temperature target approach
+- OSTI (SNS) shows a mature reference system (pulsed SC linac at GeV scale) with known reliability characteristics — directly analogous to the muon source accelerator
 
 **Missing**:
-- Mechanism for heat recycling is not described — how 2.5 GeV is recovered from the muon source/accelerator exhaust is unspecified
-- Fusion cell physics at commercial density: pressure, temperature, geometry, and fusion rate per unit volume are not documented
-- How 300 fusions/muon is achieved: what conditions reduce alpha-sticking below the current ~0.5% minimum is not described beyond stating it is the goal
-- Revenue from heat sales in LCOE: the slide assumes this as an offset but provides no basis — what heat is being sold, at what temperature, to whom?
-- Accelerator efficiency (64%) is assumed; basis not stated
+- Commercial-scale D-T target design: diamond anvil cell demonstrated in lab but fundamentally unscalable; no published concept for a commercial-scale high-density D-T fusion cell
+- Detailed energy flow diagram: how fusion heat couples to Brayton cycle from a high-density D-T target is not described
+- Muon transport efficiency from source to target (beam optics losses)
+- Alpha particle heat deposition and management in the target
 
 **Gaps**:
-- Alpha-sticking reduction mechanism — `proprietary` — **blocking**: this is the central unsolved physics problem; the analysis must bound it
-- Heat recycling subsystem design — `proprietary` — **important**: affects recirculating power fraction significantly
-- Commercial fusion cell design (pressure vessel, geometry, material) — `proprietary` — **important**: no cost analogue can be built without this
-- Revenue-from-heat-sales assumption basis — `proprietary` — **important**: affects apparent LCOE significantly and is non-standard
+- Commercial D-T target design (scalable beyond diamond anvil cell) — `truly-unknown` — **blocking**: the fusion cell is one of the two major system components; no design concept is published
+- Muon beam transport and coupling efficiency — `proprietary/not-yet-sourced` — **important**: determines effective muon utilization rate and energy balance
+- Target heat extraction mechanism and coupling to power cycle — `proprietary` — **important**: determines achievable thermal efficiency
 
 ---
 
@@ -60,23 +64,21 @@
 **Coverage**: Partial
 
 **Available**:
-- Muon source (accelerator): GEANT4 simulations at R&D stage; active-target concept novel; superconducting version planned for commercial — TRL ~2–3
-- Fusion cell: PSI experiments demonstrate proof-of-concept μCF in compressed D-T; commercial-scale cell entirely undesigned — TRL ~3–4 for physics, ~1–2 for engineering
-- Balance of plant (Brayton cycle): mature commercial technology — TRL 8–9
-- Experimental validation: Oct 2024 PSI run (28 hours) — demonstrates muon-catalyzed fusion in compressed D-T but at beam intensity orders of magnitude below commercial scale
+- Muon source (conventional proton linac → pion target → muon beam): TRL 6–7 at facilities like PSI, TRIUMF; well-characterized technology
+- Active-target muon source (Acceleron's innovation — ML-optimized geometry): TRL 2–3; GEANT4 simulations completed, Bayesian optimization used, hardware "Muon Generation Vacuum Assembly" under test, beamline tests at PSI πE1.2 conducted (Sep 2024)
+- D-T target at high density: TRL 3; diamond anvil cell demonstrated to 2.2 LHD with DT cycling (Oct 2024 data shown in ARPA-E presentation), but this is a measurement apparatus, not a heat-extracting power target
+- Tritium breeding blanket: TRL 4–5 for D-T blanket technology generically; specific design unspecified for μCF
+- Brayton cycle power conversion: TRL 8–9; mature technology from gas turbine and sCO2 programs
+- Superconducting accelerator for commercial system: TRL 4–5 (SNS/CEBAF provide existence proof; Acceleron's specific design is not yet developed)
 
 **Missing**:
-- TRL assessment for energy recovery system (heat recycling)
-- TRL for tritium breeding blanket (design unspecified)
-- TRL for high-density D-T fuel handling/circulation at scale
-- No accelerator cost scaling or design maturity documentation
-- No demonstration of any integrated system (all subsystems tested independently or not at all)
+- TRL for the full integrated system: not formally assessed
+- Commercial fusion cell (heat-extracting, scalable): TRL 1–2, no published design
+- Energy gain (Q>1) demonstration: planned at Brookhaven ~2030
 
 **Gaps**:
-- Breeding blanket design and TRL — `proprietary/not-yet-sourced` — **important**: determines tritium self-sufficiency
-- Muon source cost and engineering readiness — `proprietary` — **important**: dominant capital cost driver
-- Energy recovery subsystem existence and TRL — `truly-unknown` — **blocking**: without this the energy balance claimed cannot be evaluated
-- Integrated system test results — `truly-unknown` — **blocking**: no integrated system has been built
+- No TRL self-assessment from Acceleron or third party — `proprietary/not-yet-sourced` — **important**: ARPA-E BETHE program context implies TRL 2–4 for key components
+- Commercial-scale fusion cell TRL — `truly-unknown` — **important**: no design path published
 
 ---
 
@@ -84,101 +86,95 @@
 **Coverage**: Poor
 
 **Available**:
-- D-T fuel: standard D-T supply chain challenge (tritium production, handling)
-- Lithium-6 for breeding: implied by D-T concept; standard breeder material
-- 14.1 MeV neutron flux: requires heavy shielding — standard D-T challenge
-- Superconducting accelerator: mentioned as commercial design direction but magnet type unspecified
+- D-T fuel: standard supply chain considerations apply (lithium-6 for tritium breeding, same as all D-T concepts)
+- Niobium for SRF cavities: SNS operational experience confirms supply chain is mature and reliable for multi-cryomodule systems
+- Diamond (current test system): diamond anvil cell used for DT compression in lab setting; clearly not a commercial supply chain item
 
 **Missing**:
-- Muon source target material: what the proton beam hits is not specified (tungsten? liquid metal? exotic target?)
-- Fusion cell material and pressure vessel specifications: operates at 500–1000°C under compression — material is unspecified
-- Superconducting magnet type for accelerator (NbTi, Nb3Sn, REBCO): cost and supply chain implications differ significantly
-- Diamond anvil cell used in PSI experiments — this technology is not scalable; what replaces it at commercial scale is not stated
-- Tritium inventory estimate for 100 MW plant
+- Blanket material specification (FLiBe, LiPb, solid ceramic — not disclosed)
+- Accelerator material quantities at commercial scale (niobium, cryogenic helium)
+- High-density D-T target material for commercial system (diamond anvil cell cannot scale; replacement material/geometry not specified)
+- Tritium breeding ratio (TBR) for the blanket design
 
 **Gaps**:
-- Muon source target material — `proprietary` — **important**: may involve exotic or limited-supply materials
-- Commercial fusion cell material — `proprietary` — **important**: must survive neutron flux + high pressure at elevated temperature
-- SC accelerator magnet type — `proprietary` — **important**: REBCO vs. conventional SC has major cost implications
-- Scalable replacement for diamond anvil cell — `truly-unknown` — **blocking**: PSI experiments use lab-scale pressure apparatus; no commercial analog identified
+- Blanket material and TBR — `proprietary` — **important**: determines tritium self-sufficiency
+- Commercial fusion target material — `truly-unknown` — **blocking**: current diamond anvil cell approach is explicitly a test apparatus, not a scalable approach; commercial replacement is unspecified
+- Accelerator material quantities and supply chain — `derivable` (from SNS analog + published accelerator design rules) — **nice-to-have**
 
 ---
 
 ### 5. LCOE Parameter Extraction
+**Coverage**: Poor
 
 **Available Parameters**:
-
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| LCOE target | $0.025/kWh | ARPA-E presentation (slide 21) | Low — aspirational claim, no model |
-| Recirculating power fraction | 47% | ARPA-E presentation (slide 5) | Low — derived from unvalidated targets |
-| Energy per D-T fusion | 17.6 MeV + ~4.8 MeV breeding = ~22–25 MeV | Physics source + ARPA-E | Medium — physics well-established |
-| Muon production energy target | 3 GeV/muon | ARPA-E presentation | Low — GEANT4 simulation target, not demonstrated |
-| Conventional muon production energy | 5–6 GeV/muon | Physics source | High — experimentally established |
-| Fusions per muon (experimental) | 100–150 | Physics source | High — experimentally measured |
-| Fusions per muon (target) | 300 | ARPA-E presentation | Low — theoretical limit, not demonstrated |
-| Alpha-sticking probability (measured) | ~0.3–1% | Physics source | High — experimentally measured |
-| Plant size target | 100 MW (electrical) | Company overview | Low — target only |
-| Energy conversion | Brayton cycle | ARPA-E presentation | Medium — mentioned but unspecified |
-| Accelerator efficiency (assumed) | 64% | ARPA-E presentation | Low — basis unstated |
-| Heat recycled per muon | 2.5 GeV | ARPA-E presentation | Low — mechanism not described |
+| LCOE target | $0.025/kWh | ARPA-E 2025 | low (target, not validated) |
+| Recirculating power fraction | 47% | ARPA-E 2025 | low (claimed; conflicts with Kelly et al. 2021 at current physics) |
+| Beam energy per muon | 3.4 GeV (target) | ARPA-E 2025 | low (not yet demonstrated) |
+| Fusions per muon | 300 (target) / 150 (demonstrated) | ARPA-E 2025 / Wikipedia | medium for experimental, low for target |
+| Alpha-sticking probability | 0.3–0.9% | Wikipedia / Kamimura 2021 | medium |
+| Plant electric output | ~100 MW (target) | Company website | low |
+| Energy conversion cycle | Brayton (unspecified type) | ARPA-E 2025 | low |
+| Revenue model | Heat sales included in LCOE | ARPA-E 2025 | medium |
+| Independent electrical Q | ~14% of input (current physics) | Kelly/Hart/Rose 2021 (via Wikipedia) | medium |
+| Muon source type | SC proton linac (commercial design) | ARPA-E 2025 | low |
 
 **Missing Parameters**:
-
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Capital cost breakdown (any subsystem) | proprietary | Blocking | No cost model published; no plant study exists |
-| Accelerator capital cost ($/muon/s or $/MW) | proprietary | Blocking | Dominant cost driver; no analog cost data provided |
-| Fusion cell capital cost | proprietary | Blocking | No design exists at commercial scale |
-| Thermal efficiency of Brayton cycle | derivable | Important | Type unspecified; sCO2 vs. air vs. He — can range 40–55% |
-| Capacity factor / availability | truly-unknown | Blocking | No maintenance model; accelerator uptime not discussed |
-| O&M cost estimates | truly-unknown | Blocking | No staffing, replacement schedule, or maintenance model |
-| Tritium handling cost | derivable | Important | Can be estimated from D-T plant analogs (ITER, DEMO studies) |
-| Plant lifetime assumption | truly-unknown | Important | Not stated; affects capital cost amortization |
-| Fuel cost (D-T, Li-6) | derivable | Important | Tritium market price well-characterized |
-| Revenue from heat sales | proprietary | Important | Included in LCOE claim; basis and magnitude not stated |
-| Fusion power density (MW/m³ in cell) | proprietary | Blocking | Required to size fusion cell and derive capital cost |
-| Neutron wall loading | truly-unknown | Important | Determines blanket/shield replacement schedule |
+| Capital cost by subsystem (CAS structure) | proprietary | blocking | No published breakdown; accelerator dominates but no cost given |
+| O&M cost | proprietary | blocking | No plant-level operational cost estimate available |
+| Capacity factor / availability | not-yet-sourced | blocking | SNS linac achieves 92% availability as analog; μCF-specific estimate absent |
+| Thermal-to-electric efficiency (Brayton cycle) | derivable | important | sCO2 ~45–50%; not confirmed for this design |
+| Tritium breeding ratio | proprietary | important | Blanket design unspecified |
+| Muon source capital cost scaling | truly-unknown | blocking | No published cost model for active-target muon source |
+| D-T fusion cell capital cost | truly-unknown | blocking | No commercial design exists to cost |
+| Plant-level energy balance | proprietary | important | 47% recirculating is a headline number; subsystem breakdown missing |
+| Decommissioning cost | derivable | nice-to-have | Can use D-T MFE analogs |
+| Heat-sale revenue assumption | not-yet-sourced | nice-to-have | Mentioned but revenue split not defined |
 
 ---
 
 ## Source Recommendations
 
-1. **Historical μCF plant studies (1980s–90s)** — `not-yet-sourced` — search OSTI or Google Scholar for "muon catalyzed fusion power plant" or "muon catalyzed fusion economics" (Petrov, Jones, Jändel, Rafelski). These groups published techno-economic analyses when μCF was seriously considered; they would provide the only published capital cost structure analog. `unverified — confirm existence before searching`
+1. **Kelly, Hart & Rose (2021), "An investigation of efficient muon production for use in muon catalyzed fusion," *J. Phys.: Energy* 3, 035003** — `not-yet-sourced`. This paper (cited in Wikipedia, DOI available) provides the most rigorous independent energy balance model for μCF. **Priority acquisition**. It directly fills the gap in validating Acceleron's recirculating power claim.
+
+2. **ARPA-E BETHE program technical reports for Acceleron** — `proprietary/not-yet-sourced`. ARPA-E publishes some progress reports for funded projects. Search ARPA-E project database for "Acceleron" or "Conditions for High-Yield Muon Catalyzed Fusion" (the BETHE project title visible in Wikipedia reference [9]). May contain more engineering detail than the public presentation.
 
-2. **ARPA-E BETHE program technical reports** — `not-yet-sourced` — ARPA-E publishes project-level technical reports for BETHE awards. Acceleron had two NK Labs BETHE grants (2020, 2023); search ARPA-E project database for "NK Labs" or "Acceleron muon" for any published deliverables. `unverified — confirm existence before searching`
+3. **Jändel, Danos & Rafelski (1988), "Active target production of muons for muon-catalyzed fusion," *Phys. Rev. C* 37, 403** — `not-yet-sourced`. This paper introduced the active-target concept that Acceleron is implementing. Would clarify physics basis and original energy cost estimates. Available via DOI in Wikipedia references.
 
-3. **PSI experimental papers (2023–2025)** — `not-yet-sourced` — Acceleron ran experiments at PSI in 2024; any co-authored or PSI-authored papers describing fusion yields, pressures, or alpha-sticking at compressed conditions would provide the most current validated physics parameters. Search PSI publications database. `unverified — confirm existence before searching`
+4. **SNS/CEBAF accelerator cost reports** — `not-yet-sourced`. Published DOE project reports for the Spallation Neutron Source (SNS) include capital cost breakdowns for a ~1 GeV SC proton linac, which is the closest engineering analog to Acceleron's muon source. Search OSTI for "SNS construction cost" or "SNS project baseline." `unverified — confirm existence before searching`.
 
-4. **Proton accelerator cost literature** — `not-yet-sourced` — SNS (Spallation Neutron Source), ESS (European Spallation Source), and similar GeV-class proton accelerators have published construction cost data. These provide order-of-magnitude analogs for the muon source cost (even if Acceleron's active-target design is more compact). Available from DOE/OSTI reports.
+5. **Pusch (1996) alternative breakeven analysis and migma concept** — `not-yet-sourced`. Referenced in Wikipedia; available as a Usenet archive post. Provides an alternative energy balance model for μCF that includes target heat deposition, affecting the recirculating power estimate.
 
-5. **Alpha-sticking experimental papers (RIKEN-RAL, PSI)** — `not-yet-sourced` — The most precise alpha-sticking measurements came from RIKEN-RAL and PSI. These are published in journals (e.g., *Physical Review Letters*, *Hyperfine Interactions*). They set the hard floor on fusions/muon and are needed to bound the "300 fusions/muon" claim. Author: Ishida, Matsuzaki, and collaborators. `unverified — confirm existence before searching`
+6. **Norrønt AS technical publications** — `not-yet-sourced`. Second commercial μCF company. Any published materials would enable competitive comparison. `unverified — confirm existence before searching`.
 
 ---
 
 ## Summary
 
-**Do not proceed to full analysis without additional sourcing.** The current source base — three short documents, all company-generated — is insufficient to support a credible D1+ analysis. The LCOE target ($0.025/kWh) is a slide-deck aspiration with no published cost model behind it. Every capital cost line item is missing. The two most critical physics parameters (300 fusions/muon, 3 GeV/muon production) are undemonstrated simulation targets, not validated measurements.
+**Proceed to full qualitative + partial quantitative analysis, but flag limitations explicitly.**
 
-What a first-pass analysis *can* do with current sources:
-- Build a parametric physics model (energy balance as a function of fusions/muon and muon cost) using the well-established experimental physics
-- Bound the minimum requirements for energy breakeven (~300–500 fusions/muon depending on efficiency assumptions)
-- Perform a back-solve to show what Acceleron's claimed parameters would need to deliver at $0.025/kWh vs. $0.01/kWh
-- Use proton accelerator cost analogs and D-T plant cost analogs as order-of-magnitude capital cost proxies
+The physics of muon-catalyzed fusion is well-documented and can support a thorough qualitative analysis of system function, TRL, and challenges. The Kelly et al. (2021) parametric model (accessible via cited DOI) provides an independent energy balance framework superior to Acceleron's single-headline numbers. Acceleron's ARPA-E 2025 presentation gives enough parameters for a first-order LCOE sensitivity analysis against the physics space (the parametric contour plot they show is itself a useful starting point).
 
-What it cannot do: produce a defensible absolute LCOE estimate. The analysis should be framed explicitly as a parametric sensitivity study with all capital costs flagged as highly uncertain or missing, and the $0.025/kWh claim treated as a target to audit rather than a baseline to refine.
+However, quantitative LCOE extraction is blocked by the absence of any published capital cost breakdown — the muon source and fusion cell together constitute the concept-defining cost structure, and neither has a published design or cost estimate at commercial scale. The analysis should present the physics-derived parameter sensitivity (fusions/muon vs. beam energy/muon vs. LCOE) as the primary quantitative output, with a clear statement that bottom-up capital cost estimation is not possible from available sources.
+
+Acquiring the Kelly et al. (2021) paper should be the first priority before finalizing the analysis.
+
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Insufficient Data"
-blocking_count: 6
+overall_rating: "Significant Gaps"
+blocking_count: 5
 important_count: 6
-counting_method: "section_5_missing_parameters"
+counting_method: "all_sections_deduplicated — blocking: (1) plant engineering design absent, (2) muon source capital cost unknown, (3) commercial fusion cell design/cost unknown, (4) O&M cost unpublished, (5) capacity factor not estimated; important: (1) Kelly et al. energy balance not sourced, (2) thermal efficiency unspecified, (3) TBR/blanket design unknown, (4) muon beam transport efficiency, (5) target heat extraction mechanism, (6) plant-level energy balance subsystem detail"
 section_coverage:
-  availability_of_data:       "Poor"
+  availability_of_data:       "Partial"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Poor"
-  lcoe_parameter_extraction:  "Unknown"
-```
+  lcoe_parameter_extraction:  "Poor"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
