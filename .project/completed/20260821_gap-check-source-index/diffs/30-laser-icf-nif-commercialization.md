# Diff: 30-laser-icf-nif-commercialization

**Generated:** 2026-05-22T11:14:36-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 5 | 4 | -1 |
| important_count  | 6 | 6 | - |
| overall_rating   | Significant Gaps | Mostly Ready | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
156:2. **`knowledge/sources/commercialization_of_laser_fusion_energy/`** (Xcimer 2026 whitepaper) — laser IFE commercial cost breakdown by component; KrF vs. DPSSL laser cost comparison relevant to calibrating Thunderwall capital cost. Already in source index, recommend reading for laser cost analog.
158:3. **`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`** (Hawker) — Monte Carlo LCOE sensitivity across 14 IFE parameters; identifies gain and fusion energy per shot as highest-sensitivity parameters. Directly applicable for parameter sensitivity analysis and back-solving to $0.01/kWh.
```

## Blocking-tier lines (baseline)

```
52:- Chamber survivability / shot-to-shot physics — `truly-unknown` for this concept at scale — **blocking** for detailed modeling, acceptable to flag as major uncertainty
75:- First wall material and lifetime — `truly-unknown` for rep-rate IFE — **blocking** for O&M cost modeling
131:| Capital cost breakdown (laser, chamber, blanket, BOP) | proprietary + not-yet-sourced | blocking | No Inertia cost data; LIFE studies are closest analogue |
132:| O&M cost (target fab, laser diode replacement, maintenance) | proprietary + truly-unknown | blocking | Target cost goal is stated but fleet-scale O&M not published |
133:| First wall replacement schedule and cost | truly-unknown | blocking | No IFE concept has operated at 10 Hz — no data basis |
136:| DPSSL capital cost per beamline | proprietary + not-yet-sourced | blocking | Dominant capital cost driver; no published estimates |
137:| Fusion chamber capital cost | truly-unknown | blocking | Novel component; no cost heritage |
```

## Blocking-tier lines (new)

```
54:- Pilot plant energy balance / Q_eng reconciliation — `proprietary` (possibly `derivable` with stated assumptions) — **blocking** (affects all LCOE modeling: whether pilot produces net power or is a technology demonstration at partial output)
78:- Diode lifetime at required MTTF (14–20 GShots) — `proprietary/not-yet-sourced` — **blocking** (diode replacement schedule drives O&M costs and plant availability)
102:- Semiconductor diode supply chain cost trajectory — `proprietary` (Inertia is building this but hasn't published) — **blocking** (largest single LCOE sensitivity lever)
139:| Thunderwall beamline capital cost ($/beamline) | proprietary | **blocking** | Laser is ~30% of CoE; requires diode cost trajectory. Haefner gives target ($0.007/W) but not current cost. |
140:| Pilot plant Q_eng reconciliation | derivable | **blocking** | Gain 18 < wall-plug breakeven threshold (22.7); 50 MWe net claim needs explanation. Affects all LCOE scaling. |
141:| Overnight capital cost (Inertia design) | proprietary | **blocking** | No Inertia estimate published. LIFE 2011 gives ~$3,900–4,500/kWe (back-calculated), but 12-year-old estimate with obsolete technology costs. |
142:| Diode replacement O&M cost | proprietary | **blocking** | Largest O&M uncertainty; diode MTTF not disclosed; replacement schedule drives unplanned availability loss. |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/30-laser-icf-nif-commercialization.md	2026-05-22 09:21:13.879999047 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/30-laser-icf-nif-commercialization/gap_report.md	2026-05-22 11:14:36.248332626 -0700
@@ -1,80 +1,83 @@
+Now I have sufficient information from all sources to write the gap assessment.
+
+---
+
 # Gap Assessment: Laser ICF - NIF Commercialization (D-T)
 
 ## Overall Readiness
-**Rating**: Significant Gaps
+**Rating**: Mostly Ready
 
-**Summary**: Inertia Enterprises is highly transparent about high-level physics and laser architecture, yielding good dossier coverage on the taxonomy columns. However, the company was founded in 2024 and has published no formal plant study, no cost breakdown, and no detailed engineering design. For LCOE modeling, the available data provides a starting point for a few derivable parameters but leaves capital costs, operating costs, capacity factor, and energy conversion efficiency essentially unconstrained. The LLNL LIFE program (2008–2013) is the best available design heritage but predates ignition and uses a different (flashlamp) driver.
+**Summary**: The physics underpinning is extremely well-documented — NIF achieved Qsci up to 4.13 by April 2025 (Wurzel/Hsu 2025), and the LIFE program (2008–2013) produced detailed pre-conceptual plant designs, CoE studies, and chamber engineering that serve as direct heritage. Inertia's public communications establish key architecture and performance targets. However, the company has published no cost, capital, or detailed engineering data — all economic parameters must be derived from LIFE heritage studies that are 12+ years old and use 2011-era technology cost assumptions. The most critical economic sensitivity (laser diode cost trajectory) is explicitly a gap in all sources.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Partial
+**Coverage**: Good
 
-**Available**: Three sources were captured — the Inertia website FAQ, an ENR interview with Mike Dunne (CTO), and the Series A press release. Together these provide:
-- High-level laser architecture (10 MJ DPSSL, ~1,000 beamlines, 10 Hz, 10% wallplug efficiency)
-- Target specifications (lead hohlraum, <$1 goal, Hybrid-E design, 4.5 mm)
-- Plant output targets (50 MWe pilot, 1.5 GW full-scale)
-- Physics validation claim (NIF Dec 2022 ignition, Q_target ~1.5 demonstrated; ~18 for pilot, >30 for grid-scale claimed)
-- Fuel and energy conversion pathway at outline level
+**Available**:
+- NIF ignition physics is exhaustively documented; Wurzel/Hsu (2025) tracks all shots to Qsci=4.13 (`iter-01/sources/arxiv-2505-03834v5.md`)
+- LLNL LIFE program (2010–2014) published pre-conceptual chamber design, CoE study, and TBR blanket system engineering — the closest analog to what Inertia is building (`osti-servlets-purl-1022881`, `osti-servlets-purl-1028880`, `osti-servlets-purl-1305833`)
+- Inertia's public-facing technical parameters are captured: 10 MJ/10 Hz/10% WPE laser, ~1000 beamlines, <$1/target goal, 50 MWe pilot, 1.5 GW grid-scale, target gain ~18 (pilot) / >30 (grid) (`enr-mike-dunne-interview`, `globenewswire-series-a-press-release`, `inertia-website-technical`)
+- DPSSL technology development and cost requirements documented in Haefner (2022) IFE drive workshop white paper (`lasers-sites-lasers-files-2023-11-haefner-ilt-ife-workshop`)
+- IFE target fabrication cost modeling (Goodin 2004) provides nth-of-kind manufacturing estimates (`osti-servlets-purl-828518`)
 
 **Missing**:
-- No peer-reviewed technical papers from Inertia
-- No published plant design study or system code output
-- No engineering design documents of any kind
-- The closest published heritage (LLNL LIFE program, 2008–2013) is not yet sourced
+- No Inertia-published technical papers, design documents, or cost studies
+- No formal power plant design document from Inertia (LIFE studies are the closest analog but are 12+ years old)
+- No updated LIFE-variant studies post-2022 ignition
 
 **Gaps**:
-- Published LIFE-program plant studies — `not-yet-sourced` — **important** (best cost analogue available)
-- Inertia technical papers or white papers — `proprietary` (company is 2 years old; may not exist yet) — **important**
-- NIF ignition experiment data beyond press materials — `not-yet-sourced` — **important** (validates physics baseline)
+- Inertia technical papers/plant study — `proprietary` — important (LIFE heritage partially fills this, but Thunderwall-specific architecture is not published)
+- Post-ignition updated LIFE-variant studies — `not-yet-sourced` — nice-to-have (LLNL may have internal updates; search OSTI for post-2022 LIFE/IFE commercial studies)
 
 ---
 
 ### 2. Challenges in Capturing System Function
 **Coverage**: Partial
 
-**Available**: The dossier and sources establish the system architecture well enough to identify the key modeling challenges:
-- Pulsed operation at 10 Hz creates a recirculating power accounting challenge (laser electrical input vs. gross thermal output)
-- DPSSL driver efficiency (10% wallplug) and target gain (>30) together determine the energy balance, and the required gain for the stated 1.5 GW net output is not fully consistent with published numbers — a ~56× target gain appears needed for 1,000 beamlines at stated thermal efficiency, versus the stated >30 threshold. This tension is not explained in any source.
-- Target manufacturing at millions-per-day scale has no cost analogue
-- Liquid lithium tritium breeding + neutron energy capture is an integrated system with interdependencies that are not described at engineering level
+**Available**:
+- Indirect drive target physics and chamber interaction are well-understood from LIFE — xenon gas fill at 6 µg/cc mitigates ion damage, limits first-wall thermal pulsing to 210–230°C increments, enables near-term steel materials (`osti-servlets-purl-1028880`)
+- 10 Hz rep-rate requirement for baseload established; LIFE.2 design assumed 10–15 Hz (`osti-servlets-purl-1028880`)
+- DPSSL architecture path validated at sub-scale via HAPLS (200 J pump laser at 10 Hz, ~15% WPE) (`lasers-sites-lasers-files-2023-11-haefner-ilt-ife-workshop`)
+- Tritium extraction from liquid Li via Maroni process demonstrated in bench-scale in the 1970s (`osti-servlets-purl-1028880`)
+- Pilot plant has a wall-plug gain problem: at gain=18, thermal efficiency=44%, and laser WPE=10%, the ratio needed for wall-plug breakeven is Q_eng ≥ 1/(η_th × η_laser) = 1/(0.44 × 0.10) = 22.7. The stated gain of 18 for the pilot falls below this threshold — the 50 MWe "net" figure is not reconciled in any source
 
 **Missing**:
-- No published Q-balance or energy flow diagram
-- No rep-rate vs. availability tradeoff analysis
-- Fusion chamber design (geometry, first wall, standoff distance) not published
-- No description of how chamber survives repeated 300+ MJ implosions
+- No published energy balance for the pilot plant explaining how 50 MWe net is achieved at gain=18 (below wall-plug breakeven threshold)
+- No published Thunderwall full-system integration design (1000 beamlines with target tracking and chamber)
+- Lead hohlraum-specific chamber physics (LIFE used gold/U hohlraums; Inertia uses lead — interaction with Xe gas, clearing dynamics not addressed in available sources)
+- No published target injection/tracking system design at 10 Hz with cryogenic lead hohlraum targets
 
 **Gaps**:
-- Energy balance consistency (gain required for 1.5 GW claim) — `derivable` with assumptions — **important** (needed to set baseline)
-- Chamber survivability / shot-to-shot physics — `truly-unknown` for this concept at scale — **blocking** for detailed modeling, acceptable to flag as major uncertainty
-- DPSSL pulse shaping fidelity at scale — `not-yet-sourced` (DPSSL literature exists in laser physics community) — **important**
+- Pilot plant energy balance / Q_eng reconciliation — `proprietary` (possibly `derivable` with stated assumptions) — **blocking** (affects all LCOE modeling: whether pilot produces net power or is a technology demonstration at partial output)
+- Lead hohlraum–Xe chamber interaction — `not-yet-sourced` — important (search LLNL/OSTI for lead hohlraum indirect-drive IFE chamber studies post-2022)
+- 10 Hz cryogenic target injection at scale — `truly-unknown` (not demonstrated; only sub-Hz injection demonstrated for NIF; no engineering prototype)
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
-**Coverage**: Poor
+**Coverage**: Partial
 
-**Available**: The sources provide enough to assign rough TRL estimates, but without engineering detail:
-- **DPSSL laser (Thunderwall)**: Single-beamline prototype described; 10 kJ, 10 Hz, 10% efficiency — TRL ~3–4 (component validated in lab)
-- **Full laser system** (~1,000 beamlines): Concept only — TRL ~2
-- **Fusion target (Hybrid-E)**: Physics validated at NIF; mass manufacturing facility "planned" — target physics TRL ~6 (NIF), mass manufacturing TRL ~2–3
-- **Tritium breeding blanket**: Liquid Li approach described at outline level; "still an area of active development" per Inertia FAQ — TRL ~3 (across fusion community)
-- **Power conversion (steam turbine)**: Mature technology (TRL ~9) but integration with IFE chamber not demonstrated
-- **Fusion chamber**: No design published — TRL ~1–2
+**Available**:
+- Physics demonstration: NIF ignition baseline is at TRL 8–9 for the target physics
+- DPSSL prototype (Thunderwall): a single 10 kJ/10 Hz/10% WPE beamline is the funded development goal; HAPLS validated design choices at 200 J scale → full beamline at TRL 3–4
+- IFE chamber concept (Latkowski 2010): modular 8-section liquid-Li/Xe design analyzed at pre-conceptual level, TRL 3–4 for concept, TRL 2 for ODS-FS structural materials (12YWT not qualified for fusion neutron environment)
+- Liquid-Li tritium blanket: TBR=1.59 calculated for LIFE; Maroni T-extraction process bench-demonstrated → system TRL ~3
+- Power conversion (steam turbine at 44%): conventional technology, TRL 9
+- Target injection/tracking: no engineering demonstration at 10 Hz; TRL ~2
+- Target mass manufacturing: 2004 Goodin study shows nth-of-kind path for indirect-drive ID targets at ~$0.41/target; no Inertia-specific lead hohlraum manufacturing prototype → TRL 2–3
 
 **Missing**:
-- No subsystem-level TRL table or technology roadmap from Inertia
-- No first wall material specified (must withstand debris, X-rays, neutrons between shots at 10 Hz)
-- No target injection/tracking system described
-- Tritium extraction from flowing Li not described beyond "active development" flag
+- No Inertia-published TRL assessments by subsystem
+- No data on Thunderwall diode array lifetime (MTTF target: 14–20 GShots per Haefner; current MTTF not disclosed)
+- No published first-wall lifetime data under LIFE.2-class conditions (irradiation database for 12YWT insufficient)
 
 **Gaps**:
-- First wall material and lifetime — `truly-unknown` for rep-rate IFE — **blocking** for O&M cost modeling
-- Target injection and tracking at 10 Hz — `not-yet-sourced` (IFE community literature) — **important**
-- DPSSL diode lifetime and replacement schedule — `truly-unknown` / `proprietary` — **important**
+- Diode lifetime at required MTTF (14–20 GShots) — `proprietary/not-yet-sourced` — **blocking** (diode replacement schedule drives O&M costs and plant availability)
+- First-wall replacement schedule under neutron damage — `not-yet-sourced` — important (search for LIFE materials irradiation test results; LIFE.1 proposed this but program ended ~2013)
+- Lead hohlraum mass manufacturing at scale — `truly-unknown` — important (no published prototype; Inertia is developing but timeline/cost not disclosed)
 
 ---
 
@@ -82,101 +85,103 @@
 **Coverage**: Partial
 
 **Available**:
-- Semiconductor laser diodes: Inertia explicitly states ~100× supply chain expansion needed — critical bottleneck identified
-- Lead hohlraum vs. gold: Cost motivation stated; lead is abundant vs. gold's supply constraints at NIF scale
-- Tritium: Initial supply from US government; on-site breeding via liquid Li; inventory claimed at hundreds of grams; lithium requirement ~20 EV battery equivalents/year for 1.5 GW plant
-- Deuterium: Not discussed (abundant, not a constraint)
+- Semiconductor laser diodes: largest supply chain constraint. Haefner specifies target cost of ~$0.007/W for packaged diode arrays; current cost requires ~100x reduction, and MTTF needs 7–10x improvement. Diodes account for ~1/3 of total laser system cost (`lasers-sites-lasers-files-2023-11-haefner-ilt-ife-workshop`)
+- Inertia explicitly identifies semiconductor laser diode supply chain expansion as a key partnership priority (confidential details not published) (`enr-mike-dunne-interview`)
+- Lead for hohlraums: abundant, cheap commodity — not a supply chain risk
+- Tritium: initial supply from US government-controlled stockpile, breed on-site thereafter. Inertia claims ~hundreds of grams on-site inventory vs. tokamaks' 20× more. Li consumption ~20 EV battery equivalents/year for 1.5 GW plant (`inertia-website-technical`)
+- Beryllium NOT required (positive) — LIFE liquid Li achieves TBR >1.5 without Be (`osti-servlets-purl-1028880`)
+- Li-7 enrichment NOT required for LIFE/Inertia natural Li blanket (LIFE TBR=1.59 without enrichment)
 
 **Missing**:
-- Lithium-6 enrichment requirement not addressed (natural Li is ~7.5% Li-6; blanket breeding ratio depends on enrichment)
-- Beryllium neutron multiplier use not addressed
-- Target capsule inner layer materials (ablator, DT ice) not specified beyond "Hybrid-E design"
-- First wall material not specified
+- No published supply chain analysis for Thunderwall diode arrays (volume requirements, vendor landscape, cost trajectory)
+- No published tritium acquisition cost or startup inventory procurement cost
+- ODS ferritic steel (12YWT): not commercially produced at scale; no industrial supply chain exists for nuclear-grade quantities
+- No published liquid lithium handling/procurement plan at the tonnage scale required for 1.5 GW plant
 
 **Gaps**:
-- Li-6 enrichment requirement — `not-yet-sourced` (derivable from LIFE blanket studies) — **important**
-- Semiconductor diode manufacturing scale-up cost and timeline — `not-yet-sourced` (semiconductor industry reports) — **important**
-- Target capsule material supply (ablator materials — likely plastic/Be/HDC) — `not-yet-sourced` — **nice-to-have**
-- First wall material (W, SiC, or oxide dispersion strengthened steel?) — `truly-unknown` for this concept — **important**
+- Semiconductor diode supply chain cost trajectory — `proprietary` (Inertia is building this but hasn't published) — **blocking** (largest single LCOE sensitivity lever)
+- 12YWT / ODS-FS commercial manufacturing scale-up — `truly-unknown` — important (no commercial producer; materials testing insufficient for qualification; LIFE.1 was proposed as the test platform but LIFE was cancelled)
+- Tritium acquisition cost and startup inventory — `not-yet-sourced` — important (DOE/NNSA publishes tritium pricing; estimate ~$30,000/g → hundreds of grams startup = tens of millions)
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor
-
 **Available Parameters**:
 
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Net electrical output (pilot) | 50 MWe | ENR interview, Inertia website | h |
-| Net electrical output (full scale) | 1.5 GW | Inertia website, ENR | h |
-| Laser repetition rate | 10 Hz | All three sources | h |
-| Laser total energy | 10 MJ | Inertia website, ENR | h |
-| Laser wallplug efficiency | 10% | GlobeNewsWire, Inertia website | h |
-| Target gain (pilot target) | ~18× | ENR interview | m |
-| Target gain (grid-scale target) | >30× | ENR interview | m |
-| Target cost goal | <$1 each | Inertia website, ENR | m |
-| Target throughput needed | ~10/second | Inertia website | h |
-| Thermal conversion pathway | Liquid Li → steam turbine | Inertia website FAQ | m |
-| Thermal efficiency (analogue) | ~45% | LIFE heritage (not Inertia) | l |
-| Series A funding | $450M | GlobeNewsWire | h |
-| Pilot plant construction start | 2030 | GlobeNewsWire | m |
-| Semiconductor diode scale-up | ~100× needed | Inertia website | h |
-| Li requirement | ~20 EV batteries/year | Inertia website | m |
+| Target gain (pilot) | ~18 | ENR Dunne interview | m |
+| Target gain (grid-scale) | >30 | ENR Dunne interview | m |
+| Laser WPE | ~10% | ENR interview; GlobeNewsWire | h |
+| Rep rate | 10 Hz | All Inertia sources | h |
+| Total laser energy | 10 MJ | ENR interview; GlobeNewsWire | h |
+| Pilot plant net output | 50 MWe | ENR interview | m |
+| Grid-scale plant size | 1.5 GW | All Inertia sources | m |
+| Target cost goal | <$1/each | Inertia website | m |
+| Target cost (LIFE analog) | ~$0.38–0.41/target nth-of-kind | OSTI-828518; OSTI-1022881 | m |
+| Thermal efficiency | ~44% | OSTI-1022881 (LIFE analog) | m |
+| Plant availability (nth) | 92% | OSTI-1022881 (LIFE analog) | m |
+| Plant availability (first) | 70% | OSTI-1022881 (LIFE analog) | l |
+| CoE baseline (LIFE analog) | ~$70/MWh (900 MWe, 2011$) | OSTI-1022881 | l |
+| Laser share of CoE | ~27–30% | OSTI-1022881 | l |
+| Fuel share of CoE | ~22% | OSTI-1022881 | l |
+| O&M share of CoE | ~19% | OSTI-1022881 | l |
+| TBR (LIFE analog) | 1.59 | OSTI-1028880 | m |
+| Chamber energy gain | 1.10 | OSTI-1028880 | m |
+| First wall damage rate | 10–25 dpa/fpy | OSTI-1028880 | m |
+| Chamber wall lifetime (LIFE.1 analog) | 1–2 fpy | OSTI-1028880 | l |
+| Discount rate (LIFE study) | 8% nominal | OSTI-1022881 | h |
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Capital cost breakdown (laser, chamber, blanket, BOP) | proprietary + not-yet-sourced | blocking | No Inertia cost data; LIFE studies are closest analogue |
-| O&M cost (target fab, laser diode replacement, maintenance) | proprietary + truly-unknown | blocking | Target cost goal is stated but fleet-scale O&M not published |
-| First wall replacement schedule and cost | truly-unknown | blocking | No IFE concept has operated at 10 Hz — no data basis |
-| Capacity factor / plant availability | derivable | important | Can estimate from rep-rate and assumed maintenance; no published data |
-| Thermal efficiency (confirmed for Inertia design) | not-yet-sourced | important | LIFE analogue (~45%) may not apply to revised chamber design |
-| DPSSL capital cost per beamline | proprietary + not-yet-sourced | blocking | Dominant capital cost driver; no published estimates |
-| Fusion chamber capital cost | truly-unknown | blocking | Novel component; no cost heritage |
-| Blanket capital cost | not-yet-sourced | important | LIFE blanket studies exist (pre-ignition) |
-| Energy gain (Q_plasma vs. Q_target vs. Q_eng) | derivable | important | Published numbers are Q_target; Q_eng requires driver efficiency chain |
-| Number of chambers / modules for 1.5 GW | not-yet-sourced | important | Website says "1,000–4,000 beamlines" but module architecture unclear |
-| Tritium breeding ratio (TBR) and inventory model | not-yet-sourced | important | LIFE tritium studies exist; Inertia hasn't published |
+| Thunderwall beamline capital cost ($/beamline) | proprietary | **blocking** | Laser is ~30% of CoE; requires diode cost trajectory. Haefner gives target ($0.007/W) but not current cost. |
+| Pilot plant Q_eng reconciliation | derivable | **blocking** | Gain 18 < wall-plug breakeven threshold (22.7); 50 MWe net claim needs explanation. Affects all LCOE scaling. |
+| Overnight capital cost (Inertia design) | proprietary | **blocking** | No Inertia estimate published. LIFE 2011 gives ~$3,900–4,500/kWe (back-calculated), but 12-year-old estimate with obsolete technology costs. |
+| Diode replacement O&M cost | proprietary | **blocking** | Largest O&M uncertainty; diode MTTF not disclosed; replacement schedule drives unplanned availability loss. |
+| First wall / chamber replacement schedule | not-yet-sourced | important | LIFE.1 assumed 1-year lifetime, 10 dpa/fpy. Commercial plant replacement cost and frequency needed. |
+| Lead hohlraum target manufacturing capital + opex | not-yet-sourced | important | 2004 Goodin covers ID targets generically at $0.41; lead-specific hohlraum manufacturing not analyzed. |
+| Capacity factor / planned outage schedule | proprietary | important | LIFE assumed 92% nth-of-kind; Inertia modular design claims similar but not validated. |
+| Target injection system cost | not-yet-sourced | important | Not in any published cost study; LIFE WBS had this at 0.3% of CoE (very small) but no bottom-up estimate. |
+| Tritium startup inventory cost | derivable | nice-to-have | DOE pricing public; estimate ~$30k/g × hundreds of grams = $3–30M, small vs. total capital. |
+| Decommissioning cost | derivable | nice-to-have | Use ARIES/Gen IV methodology (OSTI-1022881 reference) as analog. |
 
 ---
 
 ## Source Recommendations
 
-1. **LLNL LIFE program plant studies (2010–2013)** — `not-yet-sourced` — Search OSTI (`osti.gov`) for "LIFE fusion power plant" or "laser inertial fusion energy plant study." Key authors: Moir, Latkowski, Meier. Provides capital cost analogues for IFE chamber, blanket, and balance of plant. Note: predates ignition and uses flashlamp driver — DPSSL laser costs will differ substantially. `confirm existence before searching — these are likely LLNL reports, OSTI is the right place`
+1. **LLNL LIFE post-2013 studies** — search OSTI for "LIFE laser inertial fusion commercialization" or "LLNL IFE commercial pathway" for any updates to the Anklam 2011 CoE study that account for more recent ignition milestones. `not-yet-sourced` — `unverified — confirm existence before searching`
 
-2. **NIF ignition experiment papers (Nature, 2022–2024)** — `not-yet-sourced` — The Dec 2022 ignition result (Kritcher et al.) and follow-on shots were published in Nature/Physics of Plasmas. Useful for confirmed Q_target values and Hybrid-E target physics. `unverified — confirm existence before searching`
+2. **`knowledge/sources/commercialization_of_laser_fusion_energy/`** (Xcimer 2026 whitepaper) — laser IFE commercial cost breakdown by component; KrF vs. DPSSL laser cost comparison relevant to calibrating Thunderwall capital cost. Already in source index, recommend reading for laser cost analog.
 
-3. **DPSSL laser cost literature** — `not-yet-sourced` — Search for "diode-pumped solid-state laser cost scaling" or "high-energy DPSSL" in laser physics journals (Applied Optics, Optics Express). May yield $/J or $/W cost analogues for laser hardware. `unverified — confirm existence before searching`
+3. **`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`** (Hawker) — Monte Carlo LCOE sensitivity across 14 IFE parameters; identifies gain and fusion energy per shot as highest-sensitivity parameters. Directly applicable for parameter sensitivity analysis and back-solving to $0.01/kWh.
 
-4. **Fusion energy economics reviews covering IFE** — `not-yet-sourced` — Search for IFE techno-economic analyses in Fusion Engineering and Design or Nuclear Fusion. Meier & Dunne (various years) may have co-authored relevant work — Mike Dunne (CTO of Inertia) has a publication record in IFE systems. `unverified — confirm existence before searching`
+4. **NIF shot N230901 and subsequent high-gain shots** — LLNL announced Qsci=4.13 in April 2025. Peer-reviewed publication of shots beyond N221204 would update target gain expectations. Search OSTI or arXiv for LLNL NIF high-yield publications 2023–2025. `not-yet-sourced`
 
-5. **Semiconductor laser diode industry cost data** — `not-yet-sourced` — Industry reports on high-power diode laser costs ($/W) from photonics industry sources (Laser Focus World, Coherent/II-VI investor materials). Would quantify the supply chain constraint Inertia identified. `unverified — confirm existence before searching`
+5. **LIFE target fabrication cost study (Miles 2009)** — cited in OSTI-1022881 as "LLNL TR-416932"; estimated target manufacturing costs for LIFE. Directly applicable to Inertia's cost targets. `not-yet-sourced` — search OSTI for LLNL-TR-416932.
 
-6. **IFE target fabrication cost studies** — `not-yet-sourced` — Search OSTI for "IFE target cost" or "ICF target mass production." General Atomics and Schafer Corp have done target manufacturing studies; NRL has published on target cost reduction. `unverified — confirm existence before searching`
+6. **Semiconductor diode roadmap for IFE** — search for post-2022 DOE IFE science & technology roadmap publications or DPSSL community workshops that quantify diode cost trajectory. `not-yet-sourced` — `unverified — confirm existence before searching`
 
 ---
 
 ## Summary
 
-**Proceed to full analysis with explicit gap handling, but strongly recommend sourcing LIFE plant studies first.**
+Proceed to full analysis with LIFE heritage as the primary cost analog. The physics is the best-documented of any fusion concept (NIF ignition achieved, Qsci to 4.13 confirmed). The LIFE OSTI studies provide a solid CoE framework at pre-conceptual level. However, three blocking gaps require explicit modeling assumptions with stated uncertainty ranges rather than sourced values: (1) the pilot plant energy balance at gain=18 vs. the wall-plug breakeven threshold; (2) laser capital cost (derive from LIFE ratio + diode cost trajectory target from Haefner); (3) diode replacement O&M. For the back-solve to $0.01/kWh, the Hawker simplified IFE model and Xcimer laser cost data (both in-repo) should be pulled in as fleet-wide analogs before writing the quantitative section.
 
-The available sources are sufficient to write a credible qualitative narrative and establish the system architecture. The NIF ignition heritage gives Inertia the strongest physics credibility of any IFE concept, and the high-level performance targets are self-consistent enough to anchor an LCOE model scaffold. However, the LCOE model will be almost entirely driven by assumptions rather than data: no capital cost figures exist for DPSSL hardware, fusion chambers, or blankets; no O&M baseline is published; and the key cost driver (target fabrication at industrial scale — ~315 million targets/year for a 1.5 GW plant at 10 Hz) has no published cost analogue beyond the stated "<$1 goal."
-
-The single highest-value action before modeling: **locate and read the LLNL LIFE program plant studies** (Latkowski, Moir, et al., ~2010–2013). These were detailed engineering cost studies for a flashlamp-driven IFE concept using similar chamber and blanket architecture. They will provide the best available capital cost analogues, even though they predate ignition and use a different driver. The driver (DPSSL vs. flashlamp) is where LIFE costs least apply; the chamber, blanket, tritium system, and BOP are directly analogous.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Significant Gaps"
-blocking_count: 5
+overall_rating: "Mostly Ready"
+blocking_count: 4
 important_count: 6
-counting_method: "section_5_missing_parameters"
+counting_method: "section_gaps_deduplicated — blocking: pilot Q_eng reconciliation, laser capital cost (Thunderwall), diode O&M replacement cost, overnight capital cost; important: first wall replacement schedule, lead hohlraum target manufacturing cost, capacity factor/planned outage, target injection system cost, lead hohlraum chamber physics, 12YWT supply chain"
 section_coverage:
-  availability_of_data:       "Partial"
+  availability_of_data:       "Good"
   system_function:            "Partial"
-  subsystem_maturity:         "Poor"
+  subsystem_maturity:         "Partial"
   materials_supply_chain:     "Partial"
-  lcoe_parameter_extraction:  "Poor"
-```
+  lcoe_parameter_extraction:  "Partial"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
