# Diff: 02-acoustic-icf-sonofusion

**Generated:** 2026-05-22T09:28:50-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 8 | 8 | 0 |
| important_count  | 4 | 5 | - |
| overall_rating   | Insufficient Data | Insufficient Data | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
162:7. **Hawker (2020) IFE simplified economic model** — `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/` — the 14-parameter technology-agnostic IFE LCOE model is applicable here as a parametric framework. It does not resolve physics unknowns, but provides the correct mathematical structure for a back-solve exercise showing what Q and shot yield would need to be. Confirmed relevant; already in repo.
```

## Blocking-tier lines (baseline)

```
28:- Company technical thesis (mechanism for exceeding sonoluminescence temperature limits) — `truly-unknown` — **blocking** (the entire concept validity rests on this)
51:- Mechanism for temperature amplification — `truly-unknown` — **blocking**
52:- System architecture (chamber, transducer count, liquid loop) — `proprietary` — **blocking** for engineering LCOE
53:- Energy gain (Q) projection — `truly-unknown` / `proprietary` — **blocking**
54:- Repetition rate needed for net power at plant scale — `derivable` from assumed Q and target power, but requires Q which is unknown — **blocking**
74:- Acoustic-to-fusion demonstration (TRL 1–2 claimed) — `truly-unknown` — **blocking**
75:- Energy capture subsystem TRL — `truly-unknown` — **blocking**
76:- Chamber materials qualification under neutron flux — `truly-unknown` — **blocking**
122:| Fusion gain (Q) | truly-unknown | blocking | No fusion achieved; Q is undefined |
123:| Fusion power per bubble | truly-unknown | blocking | Requires demonstrated fusion yield |
124:| Plant electrical output (MWe) | truly-unknown | blocking | No plant design exists |
125:| Capital cost (reactor chamber) | derivable | blocking | Could use Impulse Devices ~$250K as low-TRL proxy, but no plant-scale analogue |
128:| Energy conversion efficiency | truly-unknown | blocking | No energy capture mechanism disclosed |
129:| Thermal cycle type | truly-unknown | blocking | Speculative: liquid thermalization → steam turbine |
131:| First-wall / chamber lifetime | truly-unknown | blocking | No design; no neutron flux calculation |
134:| Repetition rate needed for net power | derivable | blocking | Requires Q to calculate; Q is unknown |
```

## Blocking-tier lines (new)

```
33:- Company technical thesis (mechanism for exceeding sonoluminescence temperature limits) — `truly-unknown` — **blocking** (the entire concept validity rests on this)
56:- Mechanism for temperature amplification — `truly-unknown` — **blocking**
57:- System architecture (chamber geometry, transducer array count and layout, liquid loop) — `proprietary` — **blocking** for any engineering LCOE model
58:- Energy gain (Q) projection — `truly-unknown` / `proprietary` — **blocking**
59:- Repetition rate needed for net power at plant scale — `derivable` from assumed Q and target power, but Q is unknown — **blocking**
81:- Acoustic-to-fusion demonstration — `truly-unknown` — **blocking**
82:- Energy capture subsystem design and TRL — `truly-unknown` — **blocking**
83:- Chamber wall materials qualification under neutron flux — `truly-unknown` — **blocking**
132:| Fusion gain (Q) | truly-unknown | blocking | No fusion achieved; Q is undefined |
133:| Fusion power per bubble collapse | truly-unknown | blocking | Requires demonstrated fusion yield |
134:| Plant electrical output (MWe) | truly-unknown | blocking | No plant design exists |
135:| Capital cost (reaction chamber at plant scale) | derivable | blocking | Impulse Devices ~$250K is only analogue; far from plant scale |
138:| Energy conversion efficiency | truly-unknown | blocking | No energy capture mechanism disclosed |
139:| Thermal cycle type | truly-unknown | blocking | Speculative: liquid thermalization → steam turbine |
141:| First-wall / chamber lifetime under neutron flux | truly-unknown | blocking | No design; no neutron flux calculation |
144:| Repetition rate needed for net power | derivable | blocking | Requires Q; Q is unknown |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/02-acoustic-icf-sonofusion.md	2026-05-22 09:21:13.830780374 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/02-acoustic-icf-sonofusion/gap_report.md	2026-05-22 09:28:50.095407601 -0700
@@ -1,8 +1,12 @@
+The gap report already exists and is comprehensive. I've read all the source documents and can validate it. Let me produce the assessment, incorporating observations from the transducer industry sources (Hielscher, APC) that provide some driver cost data.
+
+---
+
 # Gap Assessment: Acoustic ICF / Sonofusion (D-D)
 
 ## Overall Readiness
 **Rating**: Insufficient Data
-**Summary**: Sonofusion Energy is a pre-publication, opaque company with essentially no disclosed technical or engineering specifications. The publicly available literature addresses the physics of sonoluminescence — not a fusion reactor — and the concept's primary scientific challenge (achieving ~10⁸ K from a ~16,000 K demonstrated baseline) remains entirely unaddressed in public sources. A standard D1+ analysis is feasible only if it focuses on the physics gap, historical context, and analogue-based speculation; no LCOE modeling grounded in actual performance parameters is possible.
+**Summary**: Sonofusion Energy is a pre-publication, opaque company with essentially no disclosed technical or engineering specifications. The publicly available literature addresses the physics of sonoluminescence — not a fusion reactor — and the concept's primary scientific challenge (achieving ~10⁸ K from a ~16,000 K demonstrated baseline) remains entirely unaddressed in public sources. A standard D1+ analysis is feasible only if it focuses on the physics gap, historical context, and analogue-based parametric bounding; no LCOE modeling grounded in actual performance parameters is possible.
 
 ---
 
@@ -14,44 +18,45 @@
 **Available**:
 - Basic company identity (UCLA spin-off, co-founders Putterman and Camara) — `sonofusion-energy-website.md`
 - General marketing claims (modular, scalable, simple, low cost) without technical substance — `sonofusion-energy-website.md`
-- Underlying sonoluminescence physics: energy concentration ~12 orders of magnitude, plasma density >10²¹ cm⁻³, temperatures 7,000–16,000 K, 40 kHz operating regime — `ucla-putterman-group-sonoluminescence.md`, `bubble-fusion-scientific-history.md`
-- Full history of the Taleyarkhan fraud and failed replications across 4+ independent labs — `bubble-fusion-scientific-history.md`
-- Putterman's own negative neutron result (null fusion signal ≥100,000× below Taleyarkhan claims) — `bubble-fusion-scientific-history.md`, `ucla-putterman-group-sonoluminescence.md`
-- One historical comparator: Impulse Devices built a ~$250K 1-foot stainless steel sphere sonofusion research reactor — `bubble-fusion-scientific-history.md`
+- Underlying sonoluminescence physics: energy concentration ~12 orders of magnitude, plasma density >10²¹ cm⁻³, temperatures 7,000–16,000 K, 40 kHz operating regime — `ucla-putterman-group-sonoluminescence.md`
+- Full history of Taleyarkhan fraud and failed replications across 4+ independent labs (including Putterman's own null neutron result) — `bubble-fusion-scientific-history.md`
+- Historical comparator: Impulse Devices built a ~$250K 1-foot stainless steel sphere sonofusion research reactor — `bubble-fusion-scientific-history.md`
+- Commercial ultrasonic transducer specifications: APC catalog 50W/28kHz to 50kHz units, Hielscher UIP4000hdT at 4kW industrial grade (~24/7 operation) — `americanpiezo-products-services-ultrasonic-power-transducers.md`, `hielscher-uip4000hdt-4kw-high-performance-ultrasonics.md`
+- Statement: >$10M government funding at UCLA — `sonofusion-energy-website.md`
 
 **Missing**:
-- Any technical white paper, conference presentation, or DOE/ARPA-E award document from Sonofusion Energy
-- Independent assessment of the company's specific thesis for crossing the ~10⁴ K → ~10⁸ K temperature gap
+- Any technical white paper, conference presentation, or DOE/ARPA-E award document from Sonofusion Energy as a company
+- Independent assessment of the company's specific thesis for crossing the ~16,000 K → ~10⁸ K temperature gap
 - Any peer-reviewed paper attributable to the Sonofusion Energy entity (as distinct from Putterman's academic UCLA work)
 
 **Gaps**:
 - Company technical thesis (mechanism for exceeding sonoluminescence temperature limits) — `truly-unknown` — **blocking** (the entire concept validity rests on this)
-- Funding status and investor disclosures — `proprietary` — important (signals whether concept is active)
-- Any ARPA-E or DOE program records — `not-yet-sourced` — important; search ARPA-E Explorer and USASpending.gov for "Sonofusion Energy" or "Seth Putterman" grant awards post-2020 (`unverified — confirm existence before searching`)
+- Funding status and investor disclosures — `proprietary` — **important** (signals whether concept is active beyond website)
+- ARPA-E or DOE program records post-2020 — `not-yet-sourced` — **important**; search ARPA-E Explorer and USASpending.gov for "Sonofusion Energy" or "Seth Putterman" grant awards (`unverified — confirm existence before searching`)
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Partial (physics challenges well-understood; engineering challenges entirely absent)
+**Coverage**: Partial
 
 **Available**:
-- The core physics challenge is clearly documented: demonstrated temperatures (~16,000 K) are ~4 orders of magnitude below D-D ignition (~10⁸ K). This is quantified and sourced (Flannigan & Suslick 2010).
-- The driver mechanism is well-understood: ultrasonic transducers, piezoelectric, 20–40 kHz, standing-wave liquid chamber.
-- The pulse structure is understood: each bubble collapse is a discrete picosecond event; 40 kHz → 40,000 events/second with potential up to 10⁷/s.
-- The liquid medium implies inherent neutron thermalization — a natural shielding/energy deposition mechanism if D-D fusion were achieved.
-- Driver simplicity relative to laser or magnetic systems is a genuine claimed advantage.
+- Core physics challenge is precisely quantified: demonstrated temperatures (~16,000 K per Flannigan & Suslick 2010) are ~4 orders of magnitude below D-D ignition (~10⁸ K) — `bubble-fusion-scientific-history.md`, `ucla-putterman-group-sonoluminescence.md`
+- Driver mechanism well-understood: piezoelectric ultrasonic transducers, 20–40 kHz, standing-wave liquid chamber; Putterman group achieves 10⁶–10⁷ events/second
+- Pulse structure understood: each bubble collapse is a discrete picosecond event; 40 kHz → 40,000 events/second minimum
+- Liquid medium implies inherent neutron thermalization — natural energy deposition pathway if D-D fusion were achieved
+- Driver simplicity relative to laser or magnetic systems is a genuine claimed advantage; no laser, magnets, particle beams, or pulsed power needed
 
 **Missing**:
 - No disclosed path from sonoluminescence plasma (~16,000 K) to fusion-relevant plasma (~10⁸ K) — the company's core scientific claim
-- No system-level description: bubble nucleation, chamber geometry, transducer array, liquid recirculation
-- No energy balance or Q-value projection
-- No failure mode or plasma instability analysis
+- No system-level description: bubble nucleation technique, chamber geometry, transducer array configuration, liquid recirculation design
+- No energy balance or Q-value projection under any assumption set
+- No failure-mode or plasma stability analysis
 
 **Gaps**:
 - Mechanism for temperature amplification — `truly-unknown` — **blocking**
-- System architecture (chamber, transducer count, liquid loop) — `proprietary` — **blocking** for engineering LCOE
+- System architecture (chamber geometry, transducer array count and layout, liquid loop) — `proprietary` — **blocking** for any engineering LCOE model
 - Energy gain (Q) projection — `truly-unknown` / `proprietary` — **blocking**
-- Repetition rate needed for net power at plant scale — `derivable` from assumed Q and target power, but requires Q which is unknown — **blocking**
+- Repetition rate needed for net power at plant scale — `derivable` from assumed Q and target power, but Q is unknown — **blocking**
 
 ---
 
@@ -59,79 +64,84 @@
 **Coverage**: Poor
 
 **Available**:
-- **Ultrasonic transducers**: Commercially mature (TRL 9) for industrial and medical use. Well-characterized at 20–40 kHz. This subsystem is not a development risk.
-- **Liquid deuterium medium** (heavy water or deuterated acetone): Available commercially; no supply constraints at laboratory scale.
-- **Neutron detection**: Putterman group designed high-efficiency (20%) nanosecond-timing detectors — relevant to diagnostics, not power production.
-- **Historical comparator TRL**: Impulse Devices research reactor (~$250K, tabletop) was TRL 2–3, built for basic science, not power.
-- **Sonoluminescence itself**: TRL 9 as a phenomenon; well-established and reproducible.
+- **Ultrasonic transducers**: Commercially mature (TRL 9) for industrial, medical, and sonochemical use. APC standard units at 28–120 kHz; Hielscher industrial units up to 16 kW/unit, 24/7 continuous rated — `americanpiezo-products-services-ultrasonic-power-transducers.md`, `hielscher-uip4000hdt-4kw-high-performance-ultrasonics.md`
+- **Liquid deuterium medium** (heavy water or deuterated acetone): commercially available; no supply constraints at laboratory scale
+- **Sonoluminescence phenomenon itself**: TRL 9 as a physics phenomenon; well-established, reproducible
+- **Neutron detection**: Putterman group designed high-efficiency (20%) nanosecond-timing detectors — relevant to diagnostics only
+- **Historical comparator TRL**: Impulse Devices research reactor (~$250K, tabletop) was TRL 2–3 for basic science, not power generation
+- **Sonofusion as a fusion energy source**: TRL 1 at best; no credible independent fusion demonstration exists
 
 **Missing**:
-- Any demonstrated fusion yield from acoustic cavitation (the concept is TRL 1 at best as a fusion energy source)
+- Any demonstrated fusion yield from acoustic cavitation (concept is TRL 1 as a fusion energy source)
 - No disclosed engineering design for energy capture, power conversion, or plant integration
 - No materials qualification for neutron-irradiated liquid medium or chamber walls under sustained operation
+- No radiation hardness data for piezoelectric transducers in fusion-relevant neutron flux environments
 
 **Gaps**:
-- Acoustic-to-fusion demonstration (TRL 1–2 claimed) — `truly-unknown` — **blocking**
-- Energy capture subsystem TRL — `truly-unknown` — **blocking**
-- Chamber materials qualification under neutron flux — `truly-unknown` — **blocking**
-- Tritium handling (if D-D → tritium by-product) — `not-yet-sourced` — important; D-D produces tritium in ~50% of reactions; tritium buildup in liquid medium is an engineering challenge not yet addressed anywhere
+- Acoustic-to-fusion demonstration — `truly-unknown` — **blocking**
+- Energy capture subsystem design and TRL — `truly-unknown` — **blocking**
+- Chamber wall materials qualification under neutron flux — `truly-unknown` — **blocking**
+- Radiation hardness of piezoelectric transducers in D-D neutron environment — `not-yet-sourced` — **important**; PZT ceramics are radiation-sensitive but no data exists for this application
+- Tritium buildup in liquid medium (D-D produces tritium in ~50% of reactions) — `not-yet-sourced` — **important**; no treatment in any available source
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Partial (generic D-D fuel; no engineering-specific materials data)
+**Coverage**: Partial
 
 **Available**:
-- Fuel: deuterium (heavy water / deuterated acetone) — globally available, no supply constraint, low cost
-- No rare earth magnets, no HTS tape, no tritium supply, no beryllium — the concept's claimed simplicity is legitimate in this dimension
-- Ultrasonic transducers: piezoelectric ceramics (PZT or similar) — commercial supply chain mature
-- No high-energy laser systems, cryogenic targets, or pulsed-power components needed
+- Fuel: deuterium (heavy water ~$1/g, deuterated acetone) — globally available, no supply constraint
+- No rare-earth magnets, no HTS tape, no tritium supply, no beryllium, no cryogenic targets — concept's claimed material simplicity is legitimate
+- Ultrasonic transducers: PZT piezoelectric ceramics — commercial supply chain mature; multiple vendors (APC, Hielscher, others); no strategic material constraints
+- No high-energy laser systems, pulsed power, or cryogenic infrastructure needed
 
 **Missing**:
-- Chamber wall materials specification (stainless steel used in Impulse Devices prototype — adequate for neutron flux?)
+- Chamber wall materials specification under sustained D-D neutron flux (2.45 MeV, lower penetrating than 14.1 MeV D-T but still activating)
 - Long-term deuterium consumption and recirculation system design
-- Tritium accumulation management (D-D produces tritium; tritium in aqueous or organic liquid is a regulatory and safety issue)
+- Tritium accumulation management in liquid medium (regulatory and safety issue, especially for organic liquids like deuterated acetone)
+- Radiolysis of liquid medium under sustained neutron and gamma flux (potential maintenance cost driver)
 
 **Gaps**:
-- Tritium accumulation in liquid medium — `not-yet-sourced` — important; this is a known challenge in D-D liquid systems; search for fission industry analogues (tritium in heavy water moderators) — analogues exist in CANDU reactor literature (`unverified — confirm existence before searching`)
-- Radiation damage to liquid medium (deuterated acetone radiolysis under neutron/gamma flux) — `not-yet-sourced` — important; radiolysis of organic liquid medium could be significant maintenance cost driver
-- Long-term transducer degradation under radiation exposure — `truly-unknown` — important
+- Tritium accumulation in liquid medium — `not-yet-sourced` — **important**; CANDU heavy water moderator literature provides closest analogue; AECL/CNL reports likely relevant (`unverified — confirm existence before searching`)
+- Radiation damage to liquid medium (deuterated acetone radiolysis) — `not-yet-sourced` — **important**; no data in available sources
+- Long-term transducer degradation under radiation exposure — `truly-unknown` — **important**
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor — no LCOE-relevant engineering data exists in available sources
+**Coverage**: Poor
 
 **Available Parameters**:
 
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Driver frequency | 20–40 kHz | UCLA Putterman group | high |
-| Plasma density (achieved) | >10²¹ cm⁻³ | Flannigan & Suslick 2010 | high |
-| Plasma temperature (achieved) | 7,000–16,000 K | Flannigan & Suslick 2010 | high |
+| Driver frequency | 20–40 kHz | UCLA Putterman group (`ucla-putterman-group-sonoluminescence.md`) | high |
+| Plasma density (demonstrated) | >10²¹ cm⁻³ | Flannigan & Suslick 2010, via `bubble-fusion-scientific-history.md` | high |
+| Plasma temperature (demonstrated) | 7,000–16,000 K | Flannigan & Suslick 2010 | high |
 | Flash duration | <50 picoseconds | UCLA Putterman group | high |
-| Repetition rate (demonstrated) | 40,000–10,000,000/s | UCLA Putterman group | medium |
-| Research reactor cost (comparator) | ~$250K (Impulse Devices, 1-ft sphere) | bubble-fusion-scientific-history.md | low |
-| Government R&D invested | >$10M (at UCLA) | sonofusion-energy-website.md | low |
-| Fuel availability / cost | Low (heavy water ~$1/g) | general knowledge | high |
+| Repetition rate (demonstrated) | 40,000–10,000,000/s | `ucla-putterman-group-sonoluminescence.md` | medium |
+| Industrial transducer cost (analogue) | ~$1,000–10,000 per unit at 4 kW | Hielscher UIP4000hdT market price range | low |
+| Research reactor cost (comparator) | ~$250K (Impulse Devices, 1-ft sphere) | `bubble-fusion-scientific-history.md` | low |
+| Government R&D invested | >$10M (UCLA program) | `sonofusion-energy-website.md` | low |
+| Deuterium fuel cost | ~$1/g heavy water | general market data | high |
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
 | Fusion gain (Q) | truly-unknown | blocking | No fusion achieved; Q is undefined |
-| Fusion power per bubble | truly-unknown | blocking | Requires demonstrated fusion yield |
+| Fusion power per bubble collapse | truly-unknown | blocking | Requires demonstrated fusion yield |
 | Plant electrical output (MWe) | truly-unknown | blocking | No plant design exists |
-| Capital cost (reactor chamber) | derivable | blocking | Could use Impulse Devices ~$250K as low-TRL proxy, but no plant-scale analogue |
-| Capital cost (transducer array) | derivable | important | Commercial transducer costs well-known but array size for plant is unknown |
-| Capital cost (balance of plant) | derivable | important | Standard thermal BOP if Carnot cycle assumed |
+| Capital cost (reaction chamber at plant scale) | derivable | blocking | Impulse Devices ~$250K is only analogue; far from plant scale |
+| Capital cost (transducer array at plant scale) | derivable | important | Unit cost analogue exists (Hielscher 4kW); array size unknown |
+| Capital cost (balance of plant) | derivable | important | Standard thermal BOP if Carnot/steam cycle assumed |
 | Energy conversion efficiency | truly-unknown | blocking | No energy capture mechanism disclosed |
 | Thermal cycle type | truly-unknown | blocking | Speculative: liquid thermalization → steam turbine |
-| Capacity factor | derivable | important | Transducer systems have high availability; limited by liquid medium management |
-| First-wall / chamber lifetime | truly-unknown | blocking | No design; no neutron flux calculation |
-| Fuel cost (deuterium) | derivable | low | Heavy water: ~$1/g; consumption rate unknown but low compared to ICF targets |
-| O&M staffing | truly-unknown | important | No plant concept to derive from |
-| Repetition rate needed for net power | derivable | blocking | Requires Q to calculate; Q is unknown |
+| Capacity factor | derivable | important | Transducer systems have high availability; limiting factor unknown |
+| First-wall / chamber lifetime under neutron flux | truly-unknown | blocking | No design; no neutron flux calculation |
+| O&M staffing requirements | truly-unknown | important | No plant concept to derive from |
+| Fuel cost (deuterium consumption rate) | derivable | low | Rate unknown but low cost relative to ICF targets |
+| Repetition rate needed for net power | derivable | blocking | Requires Q; Q is unknown |
 
 ---
 
@@ -139,15 +149,17 @@
 
 1. **ARPA-E Explorer** — search "Sonofusion" or "Seth Putterman" for any awarded programs post-2015. Award abstracts sometimes contain the only public technical disclosures for early-stage companies. `not-yet-sourced` — `unverified — confirm existence before searching`
 
-2. **USASpending.gov / SBIR/STTR database** — search for Sonofusion Energy as a contractor/awardee. Any SBIR Phase I/II award would contain a technical abstract. `not-yet-sourced` — `unverified — confirm existence before searching`
+2. **USASpending.gov / SBIR/STTR database** — search for "Sonofusion Energy" as a contractor or awardee. Any SBIR Phase I/II award would include a technical abstract. `not-yet-sourced` — `unverified — confirm existence before searching`
 
-3. **IEEE Xplore / AIP / ASA** (Acoustical Society of America) — Putterman group publications post-2020, particularly anything using the term "inertial confinement" or with energy-balance framing (as opposed to basic sonoluminescence physics). `not-yet-sourced` — `unverified — confirm existence before searching`
+3. **IEEE Xplore / AIP / ASA** (Acoustical Society of America) — Putterman group publications post-2020, particularly any paper using "inertial confinement" framing or with energy-balance data (as opposed to basic sonoluminescence physics). `not-yet-sourced` — `unverified — confirm existence before searching`
 
-4. **CANDU reactor literature** — tritium accumulation in heavy water moderator systems provides the closest analogue for managing tritium in a D-D liquid-medium reactor. AECL/CNL reports are relevant to the materials/supply-chain section. `not-yet-sourced` — `unverified — confirm existence before searching`
+4. **CANDU reactor / AECL literature** — tritium accumulation in heavy water moderator systems provides the closest available analogue for managing tritium in a D-D liquid-medium concept. Relevant for Section 4 materials/supply-chain analysis. `not-yet-sourced` — `unverified — confirm existence before searching`
 
-5. **IEEE Spectrum article** (cited in dossier: `https://spectrum.ieee.org/bubble-power`) — this was referenced but not extracted. May contain additional historical detail and technical commentary from independent physicists. `not-yet-sourced`
+5. **IEEE Spectrum "bubble-power" article** — referenced in dossier (`https://spectrum.ieee.org/bubble-power`) but not extracted. Likely contains historical context and independent physicist commentary. `not-yet-sourced`
 
-6. **Impulse Devices, Inc.** — the dossier mentions they built a ~$250K research reactor. A FOIA request or archived news coverage may yield basic engineering specifications useful as a cost analogue. Historical coverage in SpaceDaily is already cited. `not-yet-sourced` — `unverified — confirm existence before searching`
+6. **Impulse Devices, Inc. records** — dossier mentions a ~$250K research reactor built by this company. Archived news coverage (SpaceDaily already cited) or FOIA-accessible records may yield basic engineering specs usable as a cost analogue. `not-yet-sourced` — `unverified — confirm existence before searching`
+
+7. **Hawker (2020) IFE simplified economic model** — `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/` — the 14-parameter technology-agnostic IFE LCOE model is applicable here as a parametric framework. It does not resolve physics unknowns, but provides the correct mathematical structure for a back-solve exercise showing what Q and shot yield would need to be. Confirmed relevant; already in repo.
 
 ---
 
@@ -155,26 +167,28 @@
 
 **Recommendation: Proceed to analysis with explicit "Insufficient Data" framing — do not attempt a standard LCOE model.**
 
-The available data is sufficient to write a thorough **qualitative** analysis covering sections 1–4, with honest assessment of the concept's scientific status (pre-fusion demonstration, ~10⁴ K temperature gap, fraud history, null neutron results from Putterman himself). The data is **not** sufficient to produce a credible LCOE model — there are no Q values, no plant design, no energy conversion pathway, and no capital cost basis beyond a ~$250K research reactor comparator.
+The available data is sufficient to write a thorough **qualitative** analysis covering sections 1–4, with an honest treatment of the concept's scientific status (pre-fusion demonstration, ~10⁴ K temperature gap, fraud history in the field, null neutron results from Putterman's own lab). The data is **not** sufficient to produce a credible LCOE model — there are no Q values, no plant design, no energy conversion pathway, and no capital cost basis beyond a ~$250K research reactor comparator.
 
 For the quantitative deliverable, the appropriate approach is:
-- Build a **parametric placeholder model** that takes Q, plant size, and conversion efficiency as free parameters
-- Back-solve from $0.01/kWh to show what would need to be true (Q >> 1, massive rep rate, high efficiency)
-- Contrast the required parameters against the physics ceiling (~16,000 K demonstrated vs. ~10⁸ K needed) to bound the implausibility gap
+- Adapt Hawker's 14-parameter IFE LCOE framework as a parametric placeholder, treating Q, plant size, rep rate, and conversion efficiency as free parameters
+- Back-solve from $0.01/kWh to show what would need to be true under optimistic and pessimistic assumptions
+- Contrast the required parameters against the physics ceiling (~16,000 K demonstrated vs. ~10⁸ K needed) to bound the implausibility gap quantitatively
+
+This is analytically informative: the back-solve will show that even under heroic assumptions, the concept requires physics advances ~4 orders of magnitude beyond what has been demonstrated. That quantified gap is itself a meaningful output for the comparative study.
 
-This is actually **analytically informative**: the back-solve exercise will show that even under heroic assumptions, the concept requires physics breakthroughs that are currently undemonstrated by 4 orders of magnitude. That conclusion is itself a useful output for the comparative study.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Insufficient Data"
 blocking_count: 8
-important_count: 4
-counting_method: "section_5_missing_parameters"
+important_count: 5
+counting_method: "section_5_missing_parameters_blocking_rows_only; important_count from sections_1_to_4_important_gaps_deduplicated"
 section_coverage:
   availability_of_data:       "Poor"
-  system_function:            "Partial (physics challenges well-understood; engineering challenges entirely absent)"
+  system_function:            "Partial"
   subsystem_maturity:         "Poor"
-  materials_supply_chain:     "Partial (generic D-D fuel; no engineering-specific materials data)"
-  lcoe_parameter_extraction:  "Poor — no LCOE-relevant engineering data exists in available sources"
-```
+  materials_supply_chain:     "Partial"
+  lcoe_parameter_extraction:  "Poor"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
