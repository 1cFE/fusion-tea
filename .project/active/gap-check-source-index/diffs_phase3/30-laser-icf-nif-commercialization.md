# Phase 3 diff: 30-laser-icf-nif-commercialization

**Generated:** 2026-05-22T15:49:24-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 4 | 4 | 0 |
| important_count  | 6 | 6 | - |
| overall_rating   | Mostly Ready | Mostly Ready | - |

## Fleet-source dispositions in new report

```
```

## Forbidden-phrase check (should be empty)

```
(none — good)
```

## First line of new report (should start with `# Gap Assessment`)

```
# Gap Assessment: Laser ICF - NIF Commercialization (D-T)
```

## Blocking-tier lines (new)

```
104:| Laser system CAPEX ($/J or $/beamline) | proprietary | blocking | Xcimer argues $700–1,000/J for DPSSL; Inertia claims competitive but undisclosed. Dominates total plant cost. |
105:| Rep-rated target gain at 10 MJ DPSSL | truly-unknown | blocking | NIF single-shot only; commercial extrapolation unvalidated. Wall-plug gain depends critically on this. |
106:| Laser optics replacement cost/schedule at 10 Hz | truly-unknown | blocking | No analog exists for rep-rated solid-state optics at fusion-class fluence. |
107:| Capital cost breakdown by CAS | not-yet-sourced | blocking | LIFE 2011 is closest analog; no Inertia-specific or post-ignition IFE CAS breakdown published. |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/30-laser-icf-nif-commercialization.md	2026-05-22 12:59:21.086411101 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/30-laser-icf-nif-commercialization/gap_report.md	2026-05-22 15:49:24.882764473 -0700
@@ -1,173 +1,142 @@
-Now I have sufficient information from all sources to write the gap assessment.
-
----
-
 # Gap Assessment: Laser ICF - NIF Commercialization (D-T)
 
 ## Overall Readiness
 **Rating**: Mostly Ready
-
-**Summary**: The physics underpinning is extremely well-documented — NIF achieved Qsci up to 4.13 by April 2025 (Wurzel/Hsu 2025), and the LIFE program (2008–2013) produced detailed pre-conceptual plant designs, CoE studies, and chamber engineering that serve as direct heritage. Inertia's public communications establish key architecture and performance targets. However, the company has published no cost, capital, or detailed engineering data — all economic parameters must be derived from LIFE heritage studies that are 12+ years old and use 2011-era technology cost assumptions. The most critical economic sensitivity (laser diode cost trajectory) is explicitly a gap in all sources.
+**Summary**: Inertia Enterprises benefits from extensive LIFE-era (2008–2013) engineering heritage, active public physics documentation from NIF, and a limited but informative set of public statements from founders. Enough exists for a credible qualitative analysis and a bounded first-pass LCOE estimate. The primary obstacle to a high-confidence quantitative analysis is that the laser system — which historically accounts for ~30% of IFE plant cost of electricity — has a factor-of-10+ cost uncertainty range: LIFE-era vendor quotes suggested a manageable capital share, while Xcimer's 2026 analysis argues that DPSSL diode costs alone would reach $7–10B for a 10 MJ system even with massive supply-chain investment. Inertia's actual Thunderwall beamline costs are proprietary and unvalidated in any published plant study.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Good
+**Coverage**: Partial
 
-**Available**:
-- NIF ignition physics is exhaustively documented; Wurzel/Hsu (2025) tracks all shots to Qsci=4.13 (`iter-01/sources/arxiv-2505-03834v5.md`)
-- LLNL LIFE program (2010–2014) published pre-conceptual chamber design, CoE study, and TBR blanket system engineering — the closest analog to what Inertia is building (`osti-servlets-purl-1022881`, `osti-servlets-purl-1028880`, `osti-servlets-purl-1305833`)
-- Inertia's public-facing technical parameters are captured: 10 MJ/10 Hz/10% WPE laser, ~1000 beamlines, <$1/target goal, 50 MWe pilot, 1.5 GW grid-scale, target gain ~18 (pilot) / >30 (grid) (`enr-mike-dunne-interview`, `globenewswire-series-a-press-release`, `inertia-website-technical`)
-- DPSSL technology development and cost requirements documented in Haefner (2022) IFE drive workshop white paper (`lasers-sites-lasers-files-2023-11-haefner-ilt-ife-workshop`)
-- IFE target fabrication cost modeling (Goodin 2004) provides nth-of-kind manufacturing estimates (`osti-servlets-purl-828518`)
-
-**Missing**:
-- No Inertia-published technical papers, design documents, or cost studies
-- No formal power plant design document from Inertia (LIFE studies are the closest analog but are 12+ years old)
-- No updated LIFE-variant studies post-2022 ignition
+**Available**: NIF ignition physics well-documented (Wurzel & Hsu 2025 update, `arxiv-2505-03834v5`: Q_sci = 1.5 achieved Dec 2022, up to 4.13 by April 2025, 8 shots total above scientific breakeven). Company architecture described in ENR Dunne interview and GlobeNewsWire press release: 1000 DPSSL beamlines at 10 kJ/10 Hz/10% wallplug efficiency = 10 MJ total, lead hohlraum indirect-drive targets, liquid lithium blanket, steam turbine conversion. Pre-commercial plant (LIFE.1/LIFE.2, 2008–2013) provides the closest published engineering analog: LIFE COE ~$70/MWhr for ~900 MWe (2011 dollars, `osti-1022881`), chamber design (`osti-1028880`), tritium blanket assessment (`osti-1305833`), and target fabrication cost study (`osti-828518`). Hawker (2020) IFE LCOE model (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) and Xcimer (2026) laser IFE commercialization whitepaper (`knowledge/sources/commercialization_of_laser_fusion_energy/`) provide fleet-level IFE economic framing.
+
+**Missing**: No published Inertia reactor design document, no Thunderwall cost data, no target manufacturing cost model specific to lead hohlraum indirect-drive at commercial scale, no availability or O&M projections from the company itself.
 
 **Gaps**:
-- Inertia technical papers/plant study — `proprietary` — important (LIFE heritage partially fills this, but Thunderwall-specific architecture is not published)
-- Post-ignition updated LIFE-variant studies — `not-yet-sourced` — nice-to-have (LLNL may have internal updates; search OSTI for post-2022 LIFE/IFE commercial studies)
+- Published reactor design / plant study from Inertia — not-yet-sourced — important (LIFE heritage partially fills this but is 15 years old and pre-ignition)
+- Inertia-specific laser beamline cost data — proprietary — blocking
+- Target manufacturing cost model for lead hohlraum at scale — not-yet-sourced — important
 
 ---
 
 ### 2. Challenges in Capturing System Function
 **Coverage**: Partial
 
-**Available**:
-- Indirect drive target physics and chamber interaction are well-understood from LIFE — xenon gas fill at 6 µg/cc mitigates ion damage, limits first-wall thermal pulsing to 210–230°C increments, enables near-term steel materials (`osti-servlets-purl-1028880`)
-- 10 Hz rep-rate requirement for baseload established; LIFE.2 design assumed 10–15 Hz (`osti-servlets-purl-1028880`)
-- DPSSL architecture path validated at sub-scale via HAPLS (200 J pump laser at 10 Hz, ~15% WPE) (`lasers-sites-lasers-files-2023-11-haefner-ilt-ife-workshop`)
-- Tritium extraction from liquid Li via Maroni process demonstrated in bench-scale in the 1970s (`osti-servlets-purl-1028880`)
-- Pilot plant has a wall-plug gain problem: at gain=18, thermal efficiency=44%, and laser WPE=10%, the ratio needed for wall-plug breakeven is Q_eng ≥ 1/(η_th × η_laser) = 1/(0.44 × 0.10) = 22.7. The stated gain of 18 for the pilot falls below this threshold — the 50 MWe "net" figure is not reconciled in any source
-
-**Missing**:
-- No published energy balance for the pilot plant explaining how 50 MWe net is achieved at gain=18 (below wall-plug breakeven threshold)
-- No published Thunderwall full-system integration design (1000 beamlines with target tracking and chamber)
-- Lead hohlraum-specific chamber physics (LIFE used gold/U hohlraums; Inertia uses lead — interaction with Xe gas, clearing dynamics not addressed in available sources)
-- No published target injection/tracking system design at 10 Hz with cryogenic lead hohlraum targets
+**Available**: The key challenge is the non-linear interaction between laser wallplug efficiency, target gain, and thermal conversion efficiency that determines whether the plant is net energy positive. Using available parameters: wall-plug gain = η_laser × G_target × η_thermal = 0.10 × 18 × 0.44 = 0.79 for the claimed pilot configuration (gain ~18). This is below unity, implying the 50 MWe net pilot is net energy negative at the plant level unless the accounting includes thermal storage or the gain figure is understated. Grid-scale (gain >30): 0.10 × 30 × 0.44 = 1.32 — marginally net positive. This fundamental energy balance tension is well-characterized from the available sources.
+
+Laser optics damage at 10 Hz is a qualitatively identified but unquantified challenge. The Xcimer paper (`knowledge/sources/commercialization_of_laser_fusion_energy/`) explicitly documents that at 10 Hz, NIF-derived solid-state optics architectures damage at every full-power shot, requiring a refurbishment loop that is impractical at power-plant rep rates. LIFE's approach (modular LRU design, Monte Carlo availability modeling) is documented but LIFE's optics lifetime at rep rate was modeled, not experimentally validated.
+
+Target injection and tracking at 10 Hz is a TRL-limited subsystem with no rep-rate demonstration for cryogenic indirect-drive targets. The Haefner (2023) IFE workshop paper documents that rep-rated target delivery is one of the three principal R&D pillars.
+
+**Missing**: Optics lifetime under sustained rep-rated 10 Hz irradiation (no published data), chamber reset dynamics at 10 Hz (modeled but not demonstrated), rep-rate consistency of target performance.
 
 **Gaps**:
-- Pilot plant energy balance / Q_eng reconciliation — `proprietary` (possibly `derivable` with stated assumptions) — **blocking** (affects all LCOE modeling: whether pilot produces net power or is a technology demonstration at partial output)
-- Lead hohlraum–Xe chamber interaction — `not-yet-sourced` — important (search LLNL/OSTI for lead hohlraum indirect-drive IFE chamber studies post-2022)
-- 10 Hz cryogenic target injection at scale — `truly-unknown` (not demonstrated; only sub-Hz injection demonstrated for NIF; no engineering prototype)
+- Laser optics lifetime and replacement cost at 10 Hz rep rate — truly-unknown — blocking
+- Rep-rated target gain consistency at 10 MJ DPSSL indirect drive — truly-unknown — blocking (only single-shot NIF data exists; Inertia's commercial gain is extrapolated via physics scaling)
+- Recirculating power budget at pilot scale — derivable — important (wall-plug gain <1 at gain=18 requires explicit accounting of "net" vs "gross" claims)
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
 **Coverage**: Partial
 
-**Available**:
-- Physics demonstration: NIF ignition baseline is at TRL 8–9 for the target physics
-- DPSSL prototype (Thunderwall): a single 10 kJ/10 Hz/10% WPE beamline is the funded development goal; HAPLS validated design choices at 200 J scale → full beamline at TRL 3–4
-- IFE chamber concept (Latkowski 2010): modular 8-section liquid-Li/Xe design analyzed at pre-conceptual level, TRL 3–4 for concept, TRL 2 for ODS-FS structural materials (12YWT not qualified for fusion neutron environment)
-- Liquid-Li tritium blanket: TBR=1.59 calculated for LIFE; Maroni T-extraction process bench-demonstrated → system TRL ~3
-- Power conversion (steam turbine at 44%): conventional technology, TRL 9
-- Target injection/tracking: no engineering demonstration at 10 Hz; TRL ~2
-- Target mass manufacturing: 2004 Goodin study shows nth-of-kind path for indirect-drive ID targets at ~$0.41/target; no Inertia-specific lead hohlraum manufacturing prototype → TRL 2–3
-
-**Missing**:
-- No Inertia-published TRL assessments by subsystem
-- No data on Thunderwall diode array lifetime (MTTF target: 14–20 GShots per Haefner; current MTTF not disclosed)
-- No published first-wall lifetime data under LIFE.2-class conditions (irradiation database for 12YWT insufficient)
+**Available**: NIF physics (ignition, propagating burn): TRL 7–8 in single-shot configuration. Target gain scaling physics is well-understood for indirect drive. LIFE chamber design (xenon fill gas, liquid Li coolant, HT9/ODS-FS structural materials) is at TRL 3–4, supported by detailed LLNL reports (`osti-1028880`). Steam turbine BOP: TRL 9. Hawker (2020) model quantifies the parameter ranges that could achieve competitive LCOE, placing target cost, gain, and driver cost as the dominant sensitivities.
+
+**Missing**: No TRL assessment for Thunderwall prototype beamline (described as in development). No rep-rated 10 Hz laser at kJ-scale is public. Cryogenic target delivery/injection at 10 Hz: no demonstrated system. Tritium extraction from flowing liquid Li: "active development" per Inertia website.
 
 **Gaps**:
-- Diode lifetime at required MTTF (14–20 GShots) — `proprietary/not-yet-sourced` — **blocking** (diode replacement schedule drives O&M costs and plant availability)
-- First-wall replacement schedule under neutron damage — `not-yet-sourced` — important (search for LIFE materials irradiation test results; LIFE.1 proposed this but program ended ~2013)
-- Lead hohlraum mass manufacturing at scale — `truly-unknown` — important (no published prototype; Inertia is developing but timeline/cost not disclosed)
+- DPSSL beamline (Thunderwall) TRL at rep rate — proprietary/not-yet-sourced — important
+- Rep-rated cryogenic indirect-drive target delivery/injection system — truly-unknown (TRL ~2) — blocking
+- Integrated tritium extraction system — not-yet-sourced — important (Maroni process demonstrated at sub-scale per `osti-1028880`, but no integrated system exists)
+- First wall replacement schedule under 10–25 dpa/fpy neutron flux — derivable from LIFE heritage — important
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
 **Coverage**: Partial
 
-**Available**:
-- Semiconductor laser diodes: largest supply chain constraint. Haefner specifies target cost of ~$0.007/W for packaged diode arrays; current cost requires ~100x reduction, and MTTF needs 7–10x improvement. Diodes account for ~1/3 of total laser system cost (`lasers-sites-lasers-files-2023-11-haefner-ilt-ife-workshop`)
-- Inertia explicitly identifies semiconductor laser diode supply chain expansion as a key partnership priority (confidential details not published) (`enr-mike-dunne-interview`)
-- Lead for hohlraums: abundant, cheap commodity — not a supply chain risk
-- Tritium: initial supply from US government-controlled stockpile, breed on-site thereafter. Inertia claims ~hundreds of grams on-site inventory vs. tokamaks' 20× more. Li consumption ~20 EV battery equivalents/year for 1.5 GW plant (`inertia-website-technical`)
-- Beryllium NOT required (positive) — LIFE liquid Li achieves TBR >1.5 without Be (`osti-servlets-purl-1028880`)
-- Li-7 enrichment NOT required for LIFE/Inertia natural Li blanket (LIFE TBR=1.59 without enrichment)
-
-**Missing**:
-- No published supply chain analysis for Thunderwall diode arrays (volume requirements, vendor landscape, cost trajectory)
-- No published tritium acquisition cost or startup inventory procurement cost
-- ODS ferritic steel (12YWT): not commercially produced at scale; no industrial supply chain exists for nuclear-grade quantities
-- No published liquid lithium handling/procurement plan at the tonnage scale required for 1.5 GW plant
+**Available**: Semiconductor laser diodes: Inertia explicitly acknowledges ~100x supply chain scale-up required (ENR interview). Haefner (2023) documents current diode specifications vs. IFE requirements: current diodes need 100x cost reduction (target: $0.007/W packaged) and 7–10x lifetime extension. Xcimer (2026, `knowledge/sources/commercialization_of_laser_fusion_energy/`) quantifies this as a floor of $0.02/W even with massive investment, implying a 10 MJ DPSSL laser system would cost $50B+ in diodes at today's prices, and at the asymptotic floor still $7–10B for diodes alone. Lead hohlraum targets: Goodin (2004) estimates $0.17–0.41/target for Nth-of-a-kind indirect-drive hohlraum targets (`osti-828518`); Inertia claims <$1/target. Liquid lithium: LIFE chamber used natural Li without enrichment, TBR = 1.59 (`osti-1028880`); Li supply not a constraint at ~20 EV battery-equivalents/year/1.5 GW plant (per Inertia FAQ). D-T tritium: US government stockpile for startup; breeding required at scale.
+
+**Missing**: Lead hohlraum mass manufacturing cost data for Inertia's specific design (vs. generic indirect-drive estimates). Diode procurement pathway and contracted costs from Inertia.
 
 **Gaps**:
-- Semiconductor diode supply chain cost trajectory — `proprietary` (Inertia is building this but hasn't published) — **blocking** (largest single LCOE sensitivity lever)
-- 12YWT / ODS-FS commercial manufacturing scale-up — `truly-unknown` — important (no commercial producer; materials testing insufficient for qualification; LIFE.1 was proposed as the test platform but LIFE was cancelled)
-- Tritium acquisition cost and startup inventory — `not-yet-sourced` — important (DOE/NNSA publishes tritium pricing; estimate ~$30,000/g → hundreds of grams startup = tens of millions)
+- Semiconductor laser diode cost trajectory — derivable/not-yet-sourced — blocking (Xcimer analysis makes this credible concern; without independent diode cost roadmap, laser CAPEX is unresolvable)
+- Lead hohlraum mass production cost and quality at scale — not-yet-sourced — important (Goodin 2004 analog is for a different hohlraum material)
+- ODS ferritic steel availability at production scale — not-yet-sourced — important (LIFE.2-class materials not commercially available; Inertia may defer this to later iterations)
+- Tritium supply chain (initial government inventory size, breeding ramp-up timeline) — not-yet-sourced — important
 
 ---
 
 ### 5. LCOE Parameter Extraction
 **Available Parameters**:
-
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Target gain (pilot) | ~18 | ENR Dunne interview | m |
-| Target gain (grid-scale) | >30 | ENR Dunne interview | m |
-| Laser WPE | ~10% | ENR interview; GlobeNewsWire | h |
-| Rep rate | 10 Hz | All Inertia sources | h |
-| Total laser energy | 10 MJ | ENR interview; GlobeNewsWire | h |
-| Pilot plant net output | 50 MWe | ENR interview | m |
-| Grid-scale plant size | 1.5 GW | All Inertia sources | m |
-| Target cost goal | <$1/each | Inertia website | m |
-| Target cost (LIFE analog) | ~$0.38–0.41/target nth-of-kind | OSTI-828518; OSTI-1022881 | m |
-| Thermal efficiency | ~44% | OSTI-1022881 (LIFE analog) | m |
-| Plant availability (nth) | 92% | OSTI-1022881 (LIFE analog) | m |
-| Plant availability (first) | 70% | OSTI-1022881 (LIFE analog) | l |
-| CoE baseline (LIFE analog) | ~$70/MWh (900 MWe, 2011$) | OSTI-1022881 | l |
-| Laser share of CoE | ~27–30% | OSTI-1022881 | l |
-| Fuel share of CoE | ~22% | OSTI-1022881 | l |
-| O&M share of CoE | ~19% | OSTI-1022881 | l |
-| TBR (LIFE analog) | 1.59 | OSTI-1028880 | m |
-| Chamber energy gain | 1.10 | OSTI-1028880 | m |
-| First wall damage rate | 10–25 dpa/fpy | OSTI-1028880 | m |
-| Chamber wall lifetime (LIFE.1 analog) | 1–2 fpy | OSTI-1028880 | l |
-| Discount rate (LIFE study) | 8% nominal | OSTI-1022881 | h |
+| Laser energy (total) | 10 MJ | ENR interview; GlobeNewsWire | h |
+| Rep rate | 10 Hz | ENR interview; Inertia website | h |
+| Laser wallplug efficiency (claimed) | 10% | ENR interview | m (claimed, unvalidated) |
+| D-T fuel | Confirmed | Inertia website FAQ | h |
+| Target gain — pilot | ~18 | ENR interview | l (extrapolated) |
+| Target gain — grid | >30 | ENR interview | l (extrapolated) |
+| Net electrical output — pilot | 50 MWe | ENR interview | m |
+| Net electrical output — full scale | 1.5 GW | Inertia website | m |
+| Thermal efficiency | ~44% | LIFE heritage (osti-1022881) | m |
+| Plant availability — first plant | ~70% | LIFE heritage (osti-1022881) | m |
+| Plant availability — NOAK | ~92% | LIFE heritage (osti-1022881) | m |
+| Target cost goal | <$1/target | Inertia website | l (unvalidated) |
+| Target cost analog (indirect drive Nth-of-a-kind) | $0.17–0.41/target | osti-828518 (Goodin 2004) | m |
+| LIFE COE analog | ~$70/MWhr (2011 $, 900 MWe) | osti-1022881 | m (old, pre-ignition) |
+| Laser share of COE | ~30% | osti-1022881 | m |
+| Fusion fuel (target) share of COE | ~21% | osti-1022881 | m |
+| Fusion engine (chamber) share of COE | ~15% | osti-1022881 | m |
+| TBR (liquid Li natural) | 1.59 | LIFE chamber (osti-1028880) | m |
+| Chamber energy gain | 1.10 | LIFE chamber (osti-1028880) | m |
+| Plant cost constant α (IFE analog) | $1,000–$6,000/kWe | Hawker 2020 (IFE model) | m |
+| Driver cost constant γ (laser) | $0.02–$10/J (massive range) | Xcimer 2026; Hawker 2020 | l |
+| DPSSL absolute cost floor | ~$10/J at 0.02 $/W diode floor | Xcimer 2026 (knowledge/sources/commercialization_of_laser_fusion_energy/) | m |
+| O&M cost | ~$100/kWe-yr analog | LIFE heritage; Hawker 2020 | l |
 
 **Missing Parameters**:
-
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Thunderwall beamline capital cost ($/beamline) | proprietary | **blocking** | Laser is ~30% of CoE; requires diode cost trajectory. Haefner gives target ($0.007/W) but not current cost. |
-| Pilot plant Q_eng reconciliation | derivable | **blocking** | Gain 18 < wall-plug breakeven threshold (22.7); 50 MWe net claim needs explanation. Affects all LCOE scaling. |
-| Overnight capital cost (Inertia design) | proprietary | **blocking** | No Inertia estimate published. LIFE 2011 gives ~$3,900–4,500/kWe (back-calculated), but 12-year-old estimate with obsolete technology costs. |
-| Diode replacement O&M cost | proprietary | **blocking** | Largest O&M uncertainty; diode MTTF not disclosed; replacement schedule drives unplanned availability loss. |
-| First wall / chamber replacement schedule | not-yet-sourced | important | LIFE.1 assumed 1-year lifetime, 10 dpa/fpy. Commercial plant replacement cost and frequency needed. |
-| Lead hohlraum target manufacturing capital + opex | not-yet-sourced | important | 2004 Goodin covers ID targets generically at $0.41; lead-specific hohlraum manufacturing not analyzed. |
-| Capacity factor / planned outage schedule | proprietary | important | LIFE assumed 92% nth-of-kind; Inertia modular design claims similar but not validated. |
-| Target injection system cost | not-yet-sourced | important | Not in any published cost study; LIFE WBS had this at 0.3% of CoE (very small) but no bottom-up estimate. |
-| Tritium startup inventory cost | derivable | nice-to-have | DOE pricing public; estimate ~$30k/g × hundreds of grams = $3–30M, small vs. total capital. |
-| Decommissioning cost | derivable | nice-to-have | Use ARIES/Gen IV methodology (OSTI-1022881 reference) as analog. |
+| Laser system CAPEX ($/J or $/beamline) | proprietary | blocking | Xcimer argues $700–1,000/J for DPSSL; Inertia claims competitive but undisclosed. Dominates total plant cost. |
+| Rep-rated target gain at 10 MJ DPSSL | truly-unknown | blocking | NIF single-shot only; commercial extrapolation unvalidated. Wall-plug gain depends critically on this. |
+| Laser optics replacement cost/schedule at 10 Hz | truly-unknown | blocking | No analog exists for rep-rated solid-state optics at fusion-class fluence. |
+| Capital cost breakdown by CAS | not-yet-sourced | blocking | LIFE 2011 is closest analog; no Inertia-specific or post-ignition IFE CAS breakdown published. |
+| Chamber first wall replacement schedule | not-yet-sourced | important | LIFE.1: ~1 fpy; Inertia design unspecified. Xcimer notes solid first wall requires replacement every ~1 year at 10+ Hz. |
+| Recirculating power fraction (pilot vs. full scale) | derivable | important | At gain=18, 10% η_laser, 44% η_thermal: plant-level Q_wp = 0.79 — net energy negative unless gain or η_laser are higher than claimed. |
+| Target mass manufacturing validation cost | not-yet-sourced | important | <$1/target claimed; Goodin 2004 ($0.17–0.41) is pre-lead-hohlraum and Nth-of-a-kind. |
+| Tritium extraction efficiency from liquid Li | not-yet-sourced | important | Maroni process demonstrated at bench scale but no integrated system published. |
+| Diode/optics component lifetime (GShots MTTF) | not-yet-sourced | important | Haefner requires 14–20 GShots MTTF; current diodes well below this. Drives OPEX replacement cycle. |
+| O&M cost structure | not-yet-sourced | important | LIFE analog (~20% of COE) is available but Inertia's modular design may differ significantly. |
 
 ---
 
 ## Source Recommendations
 
-1. **LLNL LIFE post-2013 studies** — search OSTI for "LIFE laser inertial fusion commercialization" or "LLNL IFE commercial pathway" for any updates to the Anklam 2011 CoE study that account for more recent ignition milestones. `not-yet-sourced` — `unverified — confirm existence before searching`
-
-2. **`knowledge/sources/commercialization_of_laser_fusion_energy/`** (Xcimer 2026 whitepaper) — laser IFE commercial cost breakdown by component; KrF vs. DPSSL laser cost comparison relevant to calibrating Thunderwall capital cost. Already in source index, recommend reading for laser cost analog.
-
-3. **`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`** (Hawker) — Monte Carlo LCOE sensitivity across 14 IFE parameters; identifies gain and fusion energy per shot as highest-sensitivity parameters. Directly applicable for parameter sensitivity analysis and back-solving to $0.01/kWh.
-
-4. **NIF shot N230901 and subsequent high-gain shots** — LLNL announced Qsci=4.13 in April 2025. Peer-reviewed publication of shots beyond N221204 would update target gain expectations. Search OSTI or arXiv for LLNL NIF high-yield publications 2023–2025. `not-yet-sourced`
-
-5. **LIFE target fabrication cost study (Miles 2009)** — cited in OSTI-1022881 as "LLNL TR-416932"; estimated target manufacturing costs for LIFE. Directly applicable to Inertia's cost targets. `not-yet-sourced` — search OSTI for LLNL-TR-416932.
-
-6. **Semiconductor diode roadmap for IFE** — search for post-2022 DOE IFE science & technology roadmap publications or DPSSL community workshops that quantify diode cost trajectory. `not-yet-sourced` — `unverified — confirm existence before searching`
+- **DPSSL laser cost roadmaps**: Search SPIE Photonics West proceedings for "semiconductor laser costs for inertial fusion energy" — McDougall et al. (2026) is cited in the Xcimer paper and likely contains the most current DPSSL cost analysis. Search SPIE 13888-3. `unverified — confirm existence before searching`
+- **LIFE target fabrication cost study (Miles 2009)**: LLNL TR-416932 on LIFE target fabrication costs is cited in osti-1022881 and would provide more up-to-date IFE target cost data specific to indirect-drive lead hohlraum designs. Search OSTI for LLNL-TR-416932.
+- **LIFE commercial and economic pathway (Anklam et al. 2011)**: Referenced as "LIFE Economic and Commercial Pathway" in osti-1028880. More detailed than osti-1022881, likely in the same TOFE proceedings issue. Search OSTI.
+- **Bayramian et al. (2011), "Compact, Efficient Laser Systems Required for Laser IFE"**: Cited in Haefner (2023) and Xcimer (2026). Provides detailed DPSSL beamline architecture and cost breakdown specific to IFE. Search OSTI or Fusion Science and Technology vol. 60(1).
+- **DOE Inertial Fusion Energy Roadmap (2023 or 2024)**: Following NIF ignition, DOE released updated IFE strategy documents. These likely contain updated plant-level cost estimates. Search DOE Office of Science IFE program documentation. `unverified — confirm existence before searching`
+- **Meier et al. (2014) LIFE fusion technology aspects**: Cited in Xcimer paper as reference [17] ("Fusion technology aspects of laser inertial fusion energy (LIFE)," Fusion Engineering and Design 89(9–10), 2489–2492). Provides updated LIFE system parameters closer to commercial scale. Available via DOI.
+
+**Fleet-wide source disqualifications**:
+- `knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/`: Pacific Fusion's AMPS paper covers pulser-driven (MagLIF-type) IFE. It does not provide cost data applicable to laser indirect-drive IFE and explicitly argues against the NIF-derived approach as the commercial path. No integration into this assessment.
+- `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`: Stellarator-specific plant design. Not applicable to IFE.
+- `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`: Covers four MFE/MIF concepts (none laser ICF). CAS methodology is transferable but concept-specific cost data is not applicable here.
+- `knowledge/sources/tea_dt_mfe_cost_analysis/`: MFE (tokamak) focused. BOP and thermal cycle cost analogs could theoretically apply but are superseded by the IFE-specific LIFE COE document (osti-1022881).
+- `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/`: Heavy-ion driver (not laser). IFE plant architecture analogs (chamber, BOP) partially applicable, but laser driver cost — the dominant gap — has no analog in HIF studies.
+- `knowledge/sources/accelerators_for_inertial_fusion_energy_production/`: Covers accelerator drivers for IFE, not laser drivers. Not applicable to the dominant DPSSL cost gap.
+- `knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/`: Historical ORNL benchmarking study. Provides LCOE context (~$100/MWh for nuclear in current market) but no fusion-specific cost data. Low additional value given osti-1022881 already covers the direct COE comparison.
 
 ---
 
 ## Summary
 
-Proceed to full analysis with LIFE heritage as the primary cost analog. The physics is the best-documented of any fusion concept (NIF ignition achieved, Qsci to 4.13 confirmed). The LIFE OSTI studies provide a solid CoE framework at pre-conceptual level. However, three blocking gaps require explicit modeling assumptions with stated uncertainty ranges rather than sourced values: (1) the pilot plant energy balance at gain=18 vs. the wall-plug breakeven threshold; (2) laser capital cost (derive from LIFE ratio + diode cost trajectory target from Haefner); (3) diode replacement O&M. For the back-solve to $0.01/kWh, the Hawker simplified IFE model and Xcimer laser cost data (both in-repo) should be pulled in as fleet-wide analogs before writing the quantitative section.
+Proceed to full analysis with stated uncertainty bounds. The conceptual physics, architecture, and plant-level parameter set are sufficiently documented to produce a meaningful qualitative analysis (Deliverable 1) and a first-pass LCOE estimate (Deliverable 2). The critical structural move for the quantitative model is to make the laser CAPEX a first-class variable with wide uncertainty: the LIFE-era estimate implied manageable laser costs (~$2–3B for 900 MWe), but the Xcimer 2026 analysis argues DPSSL architectures cannot be built below $7–10B for a 10 MJ system even with massive supply-chain investment. The analysis should bracket this range explicitly and show what gain must be achieved to close the economics under each scenario. The undemonstrated rep-rate target gain (claimed ~18–30 vs. NIF single-shot Q_sci = 1.5–4.13) is the physics uncertainty that, combined with laser CAPEX, defines the whole economic case: if gain is only 18 at pilot scale, wall-plug gain = 0.79 and the pilot plant is a net consumer of electricity — a fundamental viability question the analysis must surface.
 
 ---
 
@@ -177,9 +146,9 @@
 overall_rating: "Mostly Ready"
 blocking_count: 4
 important_count: 6
-counting_method: "section_gaps_deduplicated — blocking: pilot Q_eng reconciliation, laser capital cost (Thunderwall), diode O&M replacement cost, overnight capital cost; important: first wall replacement schedule, lead hohlraum target manufacturing cost, capacity factor/planned outage, target injection system cost, lead hohlraum chamber physics, 12YWT supply chain"
+counting_method: "deduplicated across all 5 sections: blocking = laser CAPEX, rep-rated target gain, laser optics lifetime at 10 Hz, CAS capital breakdown; important = chamber replacement schedule, recirculating power balance, target cost validation, tritium extraction, diode lifetime, O&M structure"
 section_coverage:
-  availability_of_data:       "Good"
+  availability_of_data:       "Partial"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Partial"
```
