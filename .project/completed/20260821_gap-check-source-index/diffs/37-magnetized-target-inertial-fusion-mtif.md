# Diff: 37-magnetized-target-inertial-fusion-mtif

**Generated:** 2026-05-22T11:30:19-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 6 | 9 | 3 |
| important_count  | 3 | 6 | - |
| overall_rating   | Insufficient Data | Insufficient Data | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
141:- **ARPA-E ALPHA costing revisit** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): Already ingested; applicable for CAS-structured BOP and modular-plant capital cost analogues (~$2.4/W, ~43 $/MWh at 500 MWe). The four ALPHA concepts are modular MIF/MTF-adjacent systems. Use as a cost floor analog with large uncertainty.
143:- **Simplified IFE economic model** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`): Already ingested; provides 14-parameter Monte Carlo framework for IFE LCOE. Applicable to MTIF with wide parameter ranges. Most useful for back-solve analysis (which Q / driver efficiency values would be needed for competitive LCOE).
```

## Blocking-tier lines (baseline)

```
27:- No peer-reviewed or company-published technical document — `not-yet-available` — **blocking** (the concept's physics and engineering case is unsupported by public evidence).
48:- **D-D magnetized target ignition physics** — `truly-unknown` — **blocking** (the concept's central viability question; no published simulation or experimental data for this geometry).
49:- **Fusion gain target Q** — `truly-unknown` — **blocking** (LCOE has no physics anchor without a gain assumption; modest changes in assumed gain shift LCOE by an order of magnitude).
50:- **Net electrical output design point** — `truly-unknown` — **blocking** (capital cost denominator is missing).
51:- **Railgun rail lifetime at 1 Hz, 10 km/s, 50 g plasma-armature duty** — `truly-unknown` — **blocking** (best documented defense result ~400 shots vs commercial requirement ~840M shots — 8 orders of magnitude gap; replacement cadence at 400-shot life = every 7 minutes, incompatible with sustained operation).
71:- **Experimental validation of any MTIF-relevant subsystem** — `truly-unknown` — **blocking** (no published shot data, no plasma-armature characterization, no neutron yield).
72:- **Railgun electrical efficiency at the required duty cycle** — `truly-unknown` — **blocking** (determines actual electrical energy cost per shot; experimental railguns ~20–40%, but fusion-relevant variant not characterized).
114:| Fusion gain Q | truly-unknown | blocking |
115:| Net electrical output | truly-unknown | blocking |
116:| Capital cost (any subsystem) | truly-unknown | blocking |
117:| Railgun electrical efficiency | truly-unknown | blocking |
118:| Rail lifetime and replacement cost | truly-unknown | blocking |
119:| D-D ignition conditions for railgun geometry | truly-unknown | blocking |
```

## Blocking-tier lines (new)

```
33:- No peer-reviewed physics basis for the concept — `proprietary`/`truly-unknown` — **blocking**
34:- Data availability effectively opaque for all technical and economic parameters — **blocking**
55:- No energy gain or Q target published — `proprietary`/`truly-unknown` — **blocking**
56:- Railgun durability at 1 Hz / >1 MJ shot / 10⁹-cycle plant life: no analogue in engineering literature — `truly-unknown` — **blocking**
79:- No published TRL assessment for any MTIF subsystem — `proprietary` — **blocking**
80:- Railgun durability and rep-rate TRL for fusion application: TRL 2–3, decades away from commercial readiness — `truly-unknown` — **blocking**
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/37-magnetized-target-inertial-fusion-mtif.md	2026-05-22 09:21:13.888690897 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/37-magnetized-target-inertial-fusion-mtif/gap_report.md	2026-05-22 11:30:19.797920523 -0700
@@ -1,9 +1,13 @@
-# Gap Assessment: Magnetized Target Inertial Fusion - MTIF (NearStar Fusion)
+I now have sufficient material to write the assessment. The concept-scoped sources are very thin (only marketing materials), the IOP source was bot-blocked, and the National Academies chapter is a general IFE technology review with no MTIF-specific content. The Woodruff ARPA-E ALPHA source is useful for CAS/BOP cost structure analogs.
+
+---
+
+# Gap Assessment: Magnetized Target Inertial Fusion - MTIF (D-D)
 
 ## Overall Readiness
 **Rating**: Insufficient Data
 
-**Summary**: NearStar Fusion is an early-stage company with essentially no public technical disclosures beyond its corporate website and a small set of investor-facing materials. The sole published quantitative facts are capsule mass (~50 g), velocity (~10 km/s), kinetic energy per shot (>1 MJ), and repetition rate (1 Hz). No fusion gain target, no net electric output, no capital cost, no experimental results, and no published simulation of D-D magnetized target ignition for this geometry are available. The most severe gap is *physics-level*: there is no peer-reviewed argument or simulation supporting net energy production from a railgun-driven magnetized D-D target. Compounding this, the U.S. Navy terminated its hypervelocity railgun program in 2022 after reaching only ~400-shot rail life — eight orders of magnitude below NearStar's commercial requirement of ~840M shots over a plant lifetime. An LCOE model is not credibly buildable until at minimum a fusion-gain target and an experimental validation of the driver–target chain exist.
+**Summary**: NearStar Fusion's MTIF concept is a very early-stage private venture (founded 2021) with no published peer-reviewed physics results, no demonstrated energy gain, and no public cost or LCOE estimates of any kind. Available data is limited to company marketing materials and a few confirmed architectural parameters (fuel, driver type, rep rate, first-wall material, and heat-extraction family). Every quantitative LCOE parameter is either `truly-unknown` or `proprietary`, making a credible D1+ quantitative analysis impossible without significant additional sourcing.
 
 ---
 
@@ -13,19 +17,21 @@
 **Coverage**: Poor
 
 **Available**:
-- NearStar website summary: capsule mass, velocity, kinetic energy, rep rate, D-D fuel choice, molten Pb first wall, coal-plant retrofit framing.
-- NRC licensing context: none — NearStar's operations are pre-licensing.
-- Investor press releases confirming venture capital investment (Virginia Venture Partners, Ecosphere Ventures) but no funding quantum or technical milestones.
-- Adjacent concepts (General Fusion concept 14, First Light concept 22) provide analog data for MIF and projectile-impact architectures.
+- Company website and marketing materials (`iter-01/sources/nearstar-mtif-technical-overview.md`, `nearstar-website-summary.md`): confirm driver architecture (plasma-armature railgun, 50 g capsules at 10 km/s, >1 MJ KE), fuel (D-D), rep rate (1 Hz), first wall (molten Pb), heat-extraction strategy (steam Rankine / coal-plant retrofit), and scalability claim (50 MW–1 GW+)
+- `iter-02/sources/nearstar-energy-capture-research.md`: resolves energy-capture cycle family to thermal (steam Rankine) from coal-plant retrofit framing
+- General IFE technology review (`nationalacademies-read-18289-chapter-5.md`): covers target fabrication, liquid-wall chambers, chamber clearing at 0.1–10 Hz, pulsed-power chamber issues — applicable by analogy but not MTIF-specific
+- IOP paper (`iopscience-10-1088-1741-4326-ac2dbe.md`): **bot-blocked, zero usable content**
+- No peer-reviewed publications on NearStar MTIF physics performance, implosion modeling results, or system-level studies are available in the ingested sources or referenced in the dossier
 
 **Missing**:
-- Any technical paper, preprint, or conference abstract authored by NearStar.
-- Any experimental result from NearStar (no shot data, no neutron yield, no plasma-armature characterization at the stated capsule mass and velocity).
-- Funding quantum, milestone schedule, or DOE/ARPA-E participation.
+- Any peer-reviewed or preprint physics paper on MTIF implosion performance, neutron yield, or compression efficiency
+- University of Alabama Huntsville (UAH) modeling results referenced by company but not published
+- Texas A&M HVIL impact experiment data referenced by company but not published
+- Fusion Energy Base profile adds no technical depth beyond the company website
 
 **Gaps**:
-- No peer-reviewed or company-published technical document — `not-yet-available` — **blocking** (the concept's physics and engineering case is unsupported by public evidence).
-- No DOE program affiliation that would force milestone disclosure — `proprietary` — important.
+- No peer-reviewed physics basis for the concept — `proprietary`/`truly-unknown` — **blocking**
+- Data availability effectively opaque for all technical and economic parameters — **blocking**
 
 ---
 
@@ -33,111 +39,122 @@
 **Coverage**: Poor
 
 **Available**:
-- General MIF physics from MagLIF (Sandia/Pacific Fusion) and General Fusion (pneumatic MTF) provides a framework for magnetized target compression.
-- Defense railgun program documentation (US Navy, BAE, General Atomics electromagnetic launch) provides quantitative bounds on rail erosion and shot life.
-- National Academies IFE study benchmarks target-factory cost per shot for laser ICF (~$0.25–$0.30 for plant viability; current research targets are 10,000× more expensive).
+- Basic system architecture is clear from marketing materials: railgun launches magnetized D-D capsule into molten Pb pool; shockwave-driven implosion; thermal extraction via molten Pb intermediate loop to steam turbine
+- Liquid-wall IFE chamber analogues exist in literature (LIFE, thick liquid wall concepts in National Academies review); chamber clearing at ~1 Hz, liquid jet re-establishment, and debris management are discussed generically
+- Pulsed-power IFE analog: National Academies notes ~0.1 Hz for pulsed-power concepts; MTIF's 1 Hz is ten times faster and has no published feasibility validation
 
 **Missing**:
-- Fusion gain (Q) target for the NearStar configuration.
-- Net electrical output design point.
-- Energy balance derivation (driver electrical → kinetic → fusion → thermal → electrical).
-- Pellet pre-magnetization mechanism and survivability through Mach 30 launch.
-- D-D ignition conditions in railgun-driven magnetized geometry (no published simulation).
+- Compression physics: magnetization seed-field geometry, convergence ratio, achievable ρR, and implosion symmetry are undisclosed
+- Energy balance: railgun input (>1 MJ electrical) vs. fusion yield — no Q value, even as a target
+- Repetitive-shot energy balance including recirculating power for the railgun power supply
+- Railgun barrel erosion and replacement cadence at 1 Hz / >1 MJ per shot over a 30-year plant life (~10⁹ shots) — unprecedented in any published railgun literature
+- Chamber clearing: resetting the molten Pb target pool between 1 Hz shots — hydrodynamics of rapid liquid refill/settling not addressed
+- Pre-magnetization mechanism for 50 g capsules at production scale (embedded coil? θ-pinch? capacitor bank?) — not disclosed
 
 **Gaps**:
-- **D-D magnetized target ignition physics** — `truly-unknown` — **blocking** (the concept's central viability question; no published simulation or experimental data for this geometry).
-- **Fusion gain target Q** — `truly-unknown` — **blocking** (LCOE has no physics anchor without a gain assumption; modest changes in assumed gain shift LCOE by an order of magnitude).
-- **Net electrical output design point** — `truly-unknown` — **blocking** (capital cost denominator is missing).
-- **Railgun rail lifetime at 1 Hz, 10 km/s, 50 g plasma-armature duty** — `truly-unknown` — **blocking** (best documented defense result ~400 shots vs commercial requirement ~840M shots — 8 orders of magnitude gap; replacement cadence at 400-shot life = every 7 minutes, incompatible with sustained operation).
-- **Pellet pre-magnetization mechanism** — `proprietary` — important (affects per-shot cost, complexity, and failure modes).
-- **Capacity factor** — `truly-unknown` — important (rail replacement schedule and chamber maintenance not bounded).
+- No energy gain or Q target published — `proprietary`/`truly-unknown` — **blocking**
+- Railgun durability at 1 Hz / >1 MJ shot / 10⁹-cycle plant life: no analogue in engineering literature — `truly-unknown` — **blocking**
+- Chamber clearing and molten Pb re-establishment at 1 Hz: not studied publicly — `not-yet-sourced` (analogous work exists for HIF thick liquid walls, but at ~5 Hz; 1 Hz Pb-pool filling physics differs) — **important**
+- Pre-magnetization mechanism details — `proprietary` — **important**
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
-**Coverage**: Partial
+**Coverage**: Poor
 
 **Available**:
-- TRL estimates by analogy: D-D magnetized target physics TRL 1–2; pellet pre-magnetization TRL 2–3; plasma-armature railgun TRL 3–4 (defense programs terminated); molten Pb first wall TRL 3–4 (LFR fission analogues); BOP TRL 7–9 (coal retrofit).
-- Defense railgun rail-life literature (terminated Navy program).
-- Lead-cooled fast reactor (MYRRHA, BREST) engineering database for Pb thermal hydraulics.
+- Plasma-armature railguns exist at research scale (hypervelocity impact ranges like TAMU HVIL); Wikipedia railgun article (`en-wiki-railgun.md`) confirms state of art for defense and research applications but is not fusion-specific
+- Molten Pb containment is used in fission (lead-bismuth eutectic reactors, BREST-OD-300) and IFE chamber studies — materials data exists but not yet sourced for this context
+- Steam Rankine balance of plant is fully mature (TRL 9) — no gap here
+- Sandia Z-machine heritage claimed for liner implosion physics, but Z-machine is a pulsed-power machine at very different scale and configuration from a railgun-launched projectile
 
 **Missing**:
-- Any experimental validation of MTIF-relevant subsystems at NearStar.
-- University partnership outputs (UAH, Texas A&M) — no published experiments yet.
-- Driver electrical efficiency (wall-plug to kinetic) for the specific NearStar railgun design.
+- Integrated MTIF system TRL assessment — no published document
+- Railgun component TRL for fusion application (barrel, armature, power supply for 1 Hz / >1 MJ at >10⁸ shots): TRL 2–3 by available evidence
+- Magnetized capsule fabrication TRL: TRL 2–3 (no fabrication process described publicly)
+- Molten Pb intermediate loop (pumps, heat exchangers, corrosion, activation management): TRL 3–4 by analogy to fission LBE reactors, but not characterized for this application
+- Fusion neutron shield geometry and first-wall structural assessment: not disclosed
 
 **Gaps**:
-- **Experimental validation of any MTIF-relevant subsystem** — `truly-unknown` — **blocking** (no published shot data, no plasma-armature characterization, no neutron yield).
-- **Railgun electrical efficiency at the required duty cycle** — `truly-unknown` — **blocking** (determines actual electrical energy cost per shot; experimental railguns ~20–40%, but fusion-relevant variant not characterized).
-- **Pb chamber thermal hydraulics under hypervelocity impact** — `not-yet-sourced` — important (shockwave dynamics in molten Pb from a Mach 30 impactor at 1 Hz is not in the LFR literature).
-- **Target factory throughput at 28M precision capsules/year** — `not-yet-sourced` — important.
+- No published TRL assessment for any MTIF subsystem — `proprietary` — **blocking**
+- Railgun durability and rep-rate TRL for fusion application: TRL 2–3, decades away from commercial readiness — `truly-unknown` — **blocking**
+- Capsule fabrication at rate (86,400/day at 1 Hz): no process described; analogous IFE target fabrication challenge is a known hard problem (National Academies Conclusion 3-9) — `not-yet-sourced` — **important**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Good
+**Coverage**: Poor
 
 **Available**:
-- Lead supply: commodity metal, ~10 Mt/yr global production. No constraint.
-- Deuterium supply: ~$300–600/kg, no constraint, fuel cost is negligible.
-- Railgun rail material (oxygen-free copper or molybdenum-copper composites): industrial supply chain exists for defense applications.
-- No tritium / REBCO / Be / FLiBe required — a structural supply-chain advantage relative to D-T MFE concepts.
+- Molten Pb first wall: Pb is abundant and inexpensive; National Academies notes Pb as a candidate hohlraum/chamber material with manageable activation; not a supply-chain bottleneck
+- D-D fuel: deuterium extracted from seawater, essentially unlimited supply — not a constraint; no tritium required (NearStar's explicit rationale)
+- No HTS magnets (no external confinement) — no REBCO supply issue
+- Plasma-armature railgun barrel materials (copper or composite conductors, structural steel or composite rails) — mature industrial supply chains
 
 **Missing**:
-- Quantitative rail material consumption at 28M shots/year.
-- Pb activation product inventory (Po-210 pathway) at D-D neutron spectrum.
+- Capsule material composition and fabrication materials — not disclosed; could involve exotic magnetizable materials or engineered microspheres
+- Railgun barrel material longevity and replacement volume at commercial scale
+- Molten Pb corrosion data for long-term structural material compatibility (steel, ceramic, or refractory liners) — published LBE fission literature is partially applicable but not yet sourced
+- Activation and waste stream characterization for Pb under 14 MeV D-D neutrons (D-D produces 2.45 MeV neutrons, not 14 MeV; activation products differ from D-T)
 
 **Gaps**:
-- Pb activation management — `derivable` from LFR literature — important.
-- Rail material throughput at fusion plant cadence — `derivable` — nice-to-have (tens of tonnes/year scale; no existing precision-rail supply industry, but copper is unconstrained).
+- Capsule materials and fabrication process: `proprietary` — **important**
+- Molten Pb structural compatibility and long-term activation data for D-D neutron spectrum: `not-yet-sourced` — **important**
+- No critical material bottleneck identified (good), but no supply chain analysis published: `not-yet-sourced` — **nice-to-have**
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Available Parameters**:
+**Coverage**: Poor
 
-| Parameter | Value | Source | Confidence |
-|---|---|---|---|
-| Capsule mass | ~50 g | NearStar website | high |
-| Projectile velocity | ~10 km/s | NearStar website | high |
-| Kinetic energy per shot | >1 MJ | NearStar website | high |
-| Repetition rate | 1 Hz | NearStar website | high |
-| Fuel | D-D | NearStar website | high |
-| First wall | Molten Pb | NearStar website | high |
-| Energy capture | Thermal Rankine (inferred) | NearStar website (coal retrofit framing) | medium |
+**Available Parameters**:
+| Parameter | Value/Range | Source | Confidence |
+|-----------|-------------|--------|------------|
+| Rep rate | ~1 Hz | Company website | High |
+| Capsule KE per shot | >1 MJ | Company website | High |
+| Capsule mass | ~50 g | Company website | High |
+| Target plant size | 50 MW–1 GW+ (claim) | Company website | Low |
+| Energy conversion cycle | Thermal (steam Rankine) | Company website (coal retrofit framing) | Medium |
+| Thermal efficiency (analog) | ~33–38% | Derivable from steam Rankine assumption | Low |
+| Fuel cost (D-D) | Near-zero (deuterium from seawater) | Derivable | High |
+| BOP capital cost (analog) | ~$1–2B for ~500 MWe | `revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` (CAS framework analog) | Low |
 
 **Missing Parameters**:
-
-| Parameter | Gap Type | Criticality |
-|---|---|---|
-| Fusion gain Q | truly-unknown | blocking |
-| Net electrical output | truly-unknown | blocking |
-| Capital cost (any subsystem) | truly-unknown | blocking |
-| Railgun electrical efficiency | truly-unknown | blocking |
-| Rail lifetime and replacement cost | truly-unknown | blocking |
-| D-D ignition conditions for railgun geometry | truly-unknown | blocking |
-| Capacity factor | truly-unknown | important |
-| Capsule fabrication cost per shot | truly-unknown | important |
-| Pb primary loop operating temperature | proprietary | important |
+| Parameter | Gap Type | Criticality | Notes |
+|-----------|----------|-------------|-------|
+| Energy gain Q (fusion yield / driver input) | truly-unknown | Blocking | No target value or physics estimate published |
+| Driver wall-plug efficiency (railgun electrical → KE) | proprietary | Blocking | ~10–40% typical for railguns; fusion-relevant value undisclosed |
+| Recirculating power fraction | truly-unknown | Blocking | Depends on Q and driver efficiency; Q must be known first |
+| Capital cost by subsystem (CAS) | proprietary | Blocking | No plant study, no cost estimate of any kind published |
+| Capsule fabrication cost per shot | truly-unknown | Blocking | Process undisclosed; ~86,400/day at 1 Hz |
+| Railgun replacement/maintenance schedule | truly-unknown | Blocking | Barrel erosion at >1 MJ/shot; no analogue at this scale |
+| Capacity factor / availability | truly-unknown | Blocking | Depends on railgun reliability, chamber maintenance; not estimated |
+| O&M costs | truly-unknown | Important | No analogue study for this concept type |
+| Molten Pb loop thermal design (ΔT, flow rate) | proprietary | Important | Sets intermediate loop capital and pump costs |
+| Neutron shielding and structural costs | proprietary | Important | D-D produces fewer 14 MeV neutrons but still significant shielding required |
+| Plant power balance (gross electric, auxiliary loads) | truly-unknown | Important | Required for net electric output and capacity factor |
 
 ---
 
 ## Source Recommendations
 
-1. **Patent search (assignee NearStar Fusion)** via USPTO — would surface any disclosed pellet pre-magnetization mechanism or railgun design parameters.
-2. **APS DPP / IEEE SOFE / SOFT conference abstracts** for UAH and Texas A&M collaborators — most likely venue for early experimental results.
-3. **DOE Milestone-based Fusion Development program filings** — if NearStar participates, milestone disclosures would be public.
-4. **NRC pre-application interactions** — if NearStar files for a research/test reactor license, technical specifications would enter the public docket.
-5. **Defense railgun program post-mortem analyses** (US Navy IETM, BAE final reports) for rail life and erosion modeling baselines.
+- **ARPA-E ALPHA costing revisit** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): Already ingested; applicable for CAS-structured BOP and modular-plant capital cost analogues (~$2.4/W, ~43 $/MWh at 500 MWe). The four ALPHA concepts are modular MIF/MTF-adjacent systems. Use as a cost floor analog with large uncertainty.
+
+- **Simplified IFE economic model** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`): Already ingested; provides 14-parameter Monte Carlo framework for IFE LCOE. Applicable to MTIF with wide parameter ranges. Most useful for back-solve analysis (which Q / driver efficiency values would be needed for competitive LCOE).
+
+- **Search OSTI for NearStar / Witherspoon / railgun fusion papers**: Dr. Douglas Witherspoon (NearStar founder) has a prior publication record on plasma railguns and compact fusion at HyperV Technologies Corp (OSTI full-text search: "Witherspoon railgun fusion" or "HyperV railgun MTF"). Any published HyperV/Witherspoon papers from ~2008–2021 would provide physics basis for the driver architecture — `unverified — confirm existence before searching`.
+
+- **Search APS-DPP conference proceedings for NearStar / UAH MTIF modeling**: UAH is named as a modeling partner; APS-DPP abstract database (2022–2025) may contain preliminary implosion modeling results — `unverified — confirm existence before searching`.
+
+- **LBE fission reactor materials literature** (BREST-OD-300, MYRRHA): Published data on structural material compatibility with molten lead/LBE at 400–550°C is directly applicable to the MTIF molten Pb intermediate loop. IAEA NDS or OECD NEA documents would be relevant — `unverified — confirm existence before searching`.
+
+- **Search DOE ARPA-E award database**: NearStar's website claims DOE, ARPA-E, NASA, and NSF funding. Any ARPA-E award would come with a public project description and potentially a final report — `unverified — confirm existence before searching`.
 
 ---
 
 ## Summary
 
-**Proceed to full analysis**: No, not yet.
-
-NearStar's concept faces two compounding blocking gaps: (1) the physics case for net energy production from a railgun-driven magnetized D-D target is unsupported by any public simulation or experiment, and (2) the engineering case for railgun durability at fusion duty cycles is contradicted by the only large-scale defense precedent (terminated Navy program). Without one or both of these gates being addressed, LCOE modeling produces speculation rather than analysis. The concept should be re-evaluated when NearStar (or a university collaborator) publishes either a peer-reviewed gain analysis or experimental shot data.
+The available data for MTIF (D-D) / NearStar Fusion is insufficient to produce a credible D1+ quantitative LCOE analysis. The concept is at TRL 2–3 across all non-BOP subsystems, and the company has not published any physics results, energy gain targets, cost estimates, or engineering design documents. All LCOE parameters beyond the conversion cycle family and fuel type are either `truly-unknown` or `proprietary`. The most productive path forward is to search for prior Witherspoon/HyperV publications (which may establish the physics heritage) and ARPA-E award disclosures (which may contain a project abstract with performance targets). Absent new sources, the quantitative section of the D1+ analysis must be built on very wide parameter ranges using IFE analogues from the Hawker simplified model and the Woodruff ALPHA revisit, with Q and driver efficiency as the two dominant free parameters.
 
 ---
 
@@ -145,13 +162,13 @@
 
 ```yaml
 overall_rating: "Insufficient Data"
-blocking_count: 6
-important_count: 3
-counting_method: "section_5_missing_parameters"
+blocking_count: 9
+important_count: 6
+counting_method: "all_sections_deduplicated — blocking: no physics basis, no Q/gain, no driver efficiency, no capital costs, no capsule fabrication process/cost, no railgun durability data, no plant study, no TRL assessment, no capacity factor; important: pre-magnetization mechanism, molten Pb loop design, capsule materials, molten Pb activation data, O&M costs, plant power balance"
 section_coverage:
   availability_of_data:       "Poor"
   system_function:            "Poor"
-  subsystem_maturity:         "Partial"
-  materials_supply_chain:     "Good"
-  lcoe_parameter_extraction:  "Unknown"
-```
+  subsystem_maturity:         "Poor"
+  materials_supply_chain:     "Poor"
+  lcoe_parameter_extraction:  "Poor"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
