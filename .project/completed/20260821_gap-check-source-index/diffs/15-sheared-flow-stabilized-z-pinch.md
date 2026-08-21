# Diff: 15-sheared-flow-stabilized-z-pinch

**Generated:** 2026-05-22T10:16:03-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 5 | 6 | 1 |
| important_count  | 7 | 9 | - |
| overall_rating   | Mostly Ready | Mostly Ready | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
163:3. **ARPA-E ALPHA program — Z-pinch costing** — `not-yet-sourced` — The ALPHA program funded University of Washington Z-pinch work (Uri Shumlak's group, Zap's origin). If the revisit of 2017 ALPHA costing (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) includes the UW SFS Z-pinch as one of the four concepts, it would be the only published CAS-level cost analysis for this concept. *Unverified — open the ALPHA costing source to check concept list before relying on it.*
167:5. **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — applicable as BOP, steam cycle, and tritium handling cost analog. Not Z-pinch-specific but provides CAS-level cost methodology for D-T fusion with steam extraction. Use as analog for CAS 22 (heat transfer), CAS 25 (fuel handling), CAS 26 (power conversion).
169:6. **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/`) — applicable as the CAS framework reference for structuring any cost estimate. Should be used to structure LCOE placeholder table with clearly flagged unknowns.
```

## Blocking-tier lines (baseline)

```
60:- Q value / fusion gain demonstrated — `truly-unknown` (not yet achieved experimentally) — **blocking**: LCOE depends critically on Q
61:- Recirculating power fraction at 10 Hz commercial scale — `proprietary` — **blocking**: determines net electrical output
138:| Q value (fusion gain) | truly-unknown | blocking | FuZE-Q targets Q=1, not yet demonstrated; current devices likely Q << 1 |
139:| Net electrical output (MWe) | derivable | blocking | Requires Q and recirculating power fraction; ~63 MWe if 33% thermal efficiency, but recirculating power could dominate |
140:| Recirculating power fraction at 10 Hz | proprietary | blocking | At 10 MW avg input and 190 MWt output, this is ~5% — but unconfirmed |
141:| Capital cost by subsystem | truly-unknown | blocking | No published estimates; no analogues cited in sources |
142:| Pulsed power system specific cost ($/kWe or $/J) | not-yet-sourced | blocking | Analogues from NIF, Z Machine, ICF drivers may exist |
```

## Blocking-tier lines (new)

```
31:- No published plant-level economic analysis — `proprietary` — **blocking** for LCOE
140:| Net electrical output (MWe per module/plant) | derivable | blocking | Thermal power known; need Rankine efficiency and recirculating power fraction |
141:| Rankine cycle thermal efficiency | derivable | blocking | Not stated; D-T MFE analogs suggest ~35–40%; LiPb outlet temperature unspecified |
142:| Recirculating power fraction | derivable | blocking | Qualitatively stated as advantageous vs. tokamak; no numerical estimate |
143:| Capacity factor | proprietary | blocking | No target stated; pulsed mode enables high availability in principle; 0.2→10 Hz gap is the current constraint |
144:| Direct capital cost (CAS 20–27) | proprietary | blocking | No published cost estimate; no plant study |
145:| Indirect capital costs (CAS 90–98) | proprietary | blocking | No data |
146:| O&M cost (annual) | proprietary | blocking | No data; cathode replacement and capacitor bank maintenance are key unknown drivers |
151:| LCOE projection | proprietary | blocking | No published estimate from Zap or third party |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/15-sheared-flow-stabilized-z-pinch.md	2026-05-22 09:21:13.853195203 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/15-sheared-flow-stabilized-z-pinch/gap_report.md	2026-05-22 10:16:03.465453967 -0700
@@ -1,192 +1,198 @@
-Now I have everything I need. Let me write the gap assessment.
+I have enough information to write the gap assessment. Let me compile the report now.
 
 ---
 
-# Gap Assessment: Sheared-Flow Stabilized Z-Pinch
+# Gap Assessment: Sheared-Flow Stabilized Z-Pinch (D-T)
 
 ## Overall Readiness
 **Rating**: Mostly Ready
-
-**Summary**: The qualitative picture is well-supported — Zap Energy has published a reactor concept paper (Engineering Paradigms, FST 2023) and maintains an active public communications cadence, providing solid coverage of physics, architecture, and subsystem design intent. However, both key technical papers (FST 2023 and Physics of Plasmas 2023) are paywalled with only snippets captured in Phase 1a, and no capital cost estimates or quantitative plant studies have been published. The quantitative LCOE model will require substantial derivation and analogues, with Q value and recirculating power fraction being the critical unknowns.
+**Summary**: Zap Energy's SFS Z-pinch is unusually well-documented at the physics and engineering-concept level for an early-stage private fusion company. The Thompson et al. (FST 2023) paper provides a coherent conceptual power plant design with specific parameters, and the Century/FuZE-3 press releases provide current experimental status. The critical gap is economics: Zap has published no capital cost estimates, no O&M projections, no capacity factor targets, and no LCOE analysis. A D1+ qualitative analysis can proceed confidently; quantitative LCOE parametrization requires analogs from fleet-wide sources and explicit derivation assumptions.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Moderate
+**Coverage**: Partial
 
 **Available**:
-- Zap Energy website explains the concept clearly and publicly (`zap-energy-website-how-it-works.md`)
-- Engineering Paradigms paper (FST 2023) provides reactor-level specs: 190 MWt, 10 Hz, LiPb blanket, TBR ~1.1, ~70% driver efficiency, steam Rankine, ~3 m reactor height — captured via search snippets and a third-party summary (`engineering-paradigms-paper-summary.md`)
-- Physics of Plasmas 2023 overview paper exists but is paywalled (no extracted content in Phase 1a)
-- Century paper (FST 2025) published — paywalled, but press releases and APS DPP abstract provide operational details (`century-and-fuze-a-updates-2025.md`)
-- FuZE-3 results confirmed via ScienceDaily summary (`fuze-3-gigapascal-results-2025.md`) and direct press release
-- ARPA-E project page confirms DOE-funded electrode development program
-- IEEE Spectrum article available for context
+- Full physics and concept description from the Engineering Paradigms paper (`iter-01/sources/engineering-paradigms-paper-summary.md`), Zap's website (`iter-01/sources/zap-energy-website-how-it-works.md`), and FuZE-3 press releases (`iter-02/sources/fuze-3-gigapascal-results-2025.md`). These cover: plasma formation mechanism, self-pinching physics, sheared-flow stabilization, liquid metal blanket design, pulsed power driver architecture, and qualitative economics arguments.
+- Experimental progress: FuZE device series (FuZE → FuZE-Q → FuZE-3 → FuZE-A upcoming), with performance data through FuZE-3's 1.6 GPa plasma pressure milestone.
+- Company status: $330M raised, 150 employees, Century operational at 0.2 Hz (`iter-01/sources/century-demo-system.md`), DOE Milestone-Based program participation.
+- Pulsed power technology challenges (supply chain, component lifetimes) documented in OSTI pre-roadmap (`iter-03/sources/osti-servlets-purl-2588719.md`).
 
 **Missing**:
-- Full text of Engineering Paradigms paper (FST 2023) — contains the most complete reactor design details
-- Full text of Physics of Plasmas 2023 overview paper
-- Any published power plant study with cost breakdown or economic projections
-- Zap Energy investor materials or company-published cost projections
+- No published full plant study or systems code analysis (the Engineering Paradigms paper is a preconceptual conceptual overview, not a plant design study).
+- No independent peer-reviewed techno-economic analysis of Zap's concept.
+- No access to full text of the Physics of Plasmas 2023 paper ("The Zap Energy approach to commercial fusion") — listed in dossier as paywalled, detailed content absent.
+- No cost modeling or economic projections from Zap or third parties.
 
 **Gaps**:
-- Full Engineering Paradigms paper (FST 2023) — `not-yet-sourced` — **important**: snippets provide the key parameters but reactor design details (electrode geometry, blanket thickness, component masses) may be in the full paper
-- Full Physics of Plasmas 2023 overview — `not-yet-sourced` — **important**: likely contains confinement scaling and plasma parameter projections
-- Any cost or economic analysis — `truly-unknown` (no published estimates identified) — **blocking for quantitative model**
+- No published plant-level economic analysis — `proprietary` — **blocking** for LCOE
+- Full text of PoP 2023 paper unavailable — `not-yet-sourced` — **important** (may contain additional plasma parameter details)
+- Full text of Century FST 2025 paper unavailable — `not-yet-sourced` — **important** (Century details from press releases only)
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Partial
+**Coverage**: Good
 
 **Available**:
-- Core physics understood: ohmic heating via axial current, self-generated B-field, sheared-flow stabilization mechanism
-- Driver architecture clear: pulsed power capacitor bank + pulse-forming networks, passive design
-- Energy flow pathway clear: driver → plasma → neutrons + alphas → LiPb → steam cycle
-- Recirculating power pathway partially understood: wall-plug to cathode efficiency ~70%, but end-to-end Q and net electrical output not published
-- Rep rate scaling challenge explicitly documented: 0.2 Hz (Century) → 10 Hz (commercial), with power requirement scaling from 39 kW to ~10 MW average input
-- Electrode engineering is an active open problem (dedicated ARPA-E project)
+- **Plasma confinement and heating**: Complete from Engineering Paradigms paper. J×B self-pinch with ohmic heating driven by axial current; sheared flow extends stability. No external magnets. Unity beta plasma at ~0.15 mm radius, 0.5 m length at plant scale. Described quantitatively in Table I of the paper.
+- **Pulsed power driver**: Capacitor bank → PFN → plasma cathode pathway, ~70% wall-plug efficiency. Solid-state thyristor switches demonstrated at 80% efficiency at 5 Hz. FuZE-3 uses two separate capacitor banks and three-electrode design for independent acceleration/compression control.
+- **Liquid metal blanket**: LiPb eutectic weir-wall design described conceptually. Gravity-driven cascade forms first wall, terminates pinch current, absorbs fusion neutrons, breeds tritium. TBR ~1.1. Century uses liquid bismuth (non-DT engineering testbed).
+- **Power conversion**: Steam Rankine cycle extracting heat from LiPb, confirmed in Engineering Paradigms paper and corroborated by independent blog summary.
+- **Pulsed power scale-up challenge**: Century at 0.2 Hz / 100 kW average power; commercial target is 10 Hz / ~10 MW average input power. Gap is well-characterized in the sources.
 
 **Missing**:
-- Q value — FuZE-Q is designed for Q=1 but has not yet demonstrated breakeven; actual current Q is unquantified from available sources
-- Plasma scaling laws from current experiments to reactor conditions (1.5 MA FuZE-Q → commercial reactor current requirements)
-- Recirculating power fraction at commercial rep rate — this directly determines whether the concept is economically viable
-- Confinement time scaling with current and plasma conditions
-- Plasma-wall interaction details at high rep rate (electrode erosion, impurity injection)
+- **Tritium extraction loop**: Mentioned (pumped out, through heat exchanger and "tritium extraction stage") but no process details.
+- **LiPb pumping system design**: Mentioned but not quantified (power, flow rate, pump type). High density of LiPb makes pumping power non-trivial.
+- **Cathode wear mechanism and replacement cycle**: Qualitative discussion (arc smelting analogy, "small volume and mass") but no replacement interval or maintenance schedule specified.
+- **Thermal cycle efficiency**: Specific Rankine cycle conditions (steam temperature/pressure, efficiency) not stated.
+- **Plasma stability at high currents**: Explicitly acknowledged as unresolved in Engineering Paradigms paper. Whether sheared-flow stabilization holds at 1.2–1.5 MA is an open physics question.
 
 **Gaps**:
-- Q value / fusion gain demonstrated — `truly-unknown` (not yet achieved experimentally) — **blocking**: LCOE depends critically on Q
-- Recirculating power fraction at 10 Hz commercial scale — `proprietary` — **blocking**: determines net electrical output
-- Plasma scaling from FuZE-3/FuZE-Q to reactor current levels — `not-yet-sourced` (likely in Physics of Plasmas 2023 paper) — **important**
-- Electrode erosion/impurity injection rates — `truly-unknown` at the required rep rate — **important**
+- Tritium extraction process design — `not-yet-sourced` — **important** (search LLNL/ITER tritium handling analogs)
+- Rankine cycle efficiency specification — `derivable` from steam cycle analogs in TEA sources — **important**
+- Cathode replacement interval — `proprietary` — **important**
+- High-current stability scaling — `truly-unknown` (experimentally unresolved) — **important** (key physics risk)
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
 **Coverage**: Partial
 
-**Available**:
-- **Plasma physics / sheared-flow stabilization**: FuZE demonstrated D-T fusion neutrons (confirmed by LLNL, 2021); FuZE-3 achieved 1.6 GPa total pressure — TRL ~4
-- **Pulsed power driver**: Century operating at 39 kW average, 500 kA per pulse, 0.2 Hz; passive PFN design is mature at single-shot scale — TRL ~4 at current rep rate, TRL ~2 at 10 Hz target
-- **Liquid metal wall system**: Century demonstrates liquid bismuth circulation with thermal management at 100 kW scale; vertically-oriented design validated at engineering level — TRL ~4 for Bi, TRL ~2-3 for LiPb with D-T plasma
-- **Steam Rankine energy conversion**: fully mature technology, applicable directly — TRL ~9
-- **Electrode technology**: ARPA-E project underway, explicitly described as needing development — TRL ~2-3
+**Available**: Per-subsystem TRL can be inferred from experimental status in the sources.
+
+| Subsystem | TRL Estimate | Basis |
+|-----------|-------------|-------|
+| SFS Z-pinch plasma (physics) | 3–4 | FuZE demonstrated thermonuclear neutrons; FuZE-3 at 1.6 GPa; still ~3 orders of magnitude below power plant density/temperature/current |
+| Repetitive pulsed power | 4–5 | Century at 0.2 Hz / 100 kW; target 10 Hz / 10 MW; subscale demonstration at 5 Hz in literature |
+| Cathode / electrode tech | 3–4 | Century testing cathode durability; 1000+ shots demonstrated; no lifetime data |
+| Liquid metal wall system | 3 | First integrated test at Century (liquid Bi, non-fusing); no fusing plasma + LiPb co-test |
+| Tritium breeding blanket | 2–3 | LiPb design with TBR ~1.1 calculated; no prototype tritium loop |
+| Steam power conversion | 8–9 | Commercial technology; applicable directly |
+| Solid-state pulsed power switches | 4–5 | Demonstrated at 5 Hz calorimetrically; long-lifetime at 10 Hz not demonstrated |
+| High-voltage capacitor bank | 4–5 | Functional at research scale; lifetime-at-rep-rate not demonstrated |
 
 **Missing**:
-- TRL assessment for tritium breeding loop (LiPb processing, extraction, reinjection)
-- Tritium breeding has no experimental validation in this system
-- High-rep-rate electrode lifetime data
-- Capacity factor projections (maintenance intervals, component replacement schedules)
+- No formal TRL assessment from Zap or DOE published.
+- FuZE-Q performance data not directly available in sources (FuZE-Q undergoing operations alongside FuZE-3 per press release).
+- No MHD analysis of LiPb flow near the electrode current termination region.
 
 **Gaps**:
-- Electrode lifetime under commercial conditions (500 kA+ at 10 Hz) — `truly-unknown` — **important**: drives replacement cost and availability
-- LiPb tritium breeding validation — `truly-unknown` (Century uses Bi, no D-T testing) — **important**
-- Rep rate scaling path from 0.2 Hz to 10 Hz — `proprietary` (internal roadmap) / `not-yet-sourced` — **important**
-- Capacitor bank lifetime and replacement at commercial rep rate — `truly-unknown` — **important**
+- Independent TRL assessment — `not-yet-sourced` — **important** (search DOE Milestone program reports)
+- FuZE-Q performance data and current/neutron yield — `not-yet-sourced` — **important**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Poor
+**Coverage**: Partial
 
 **Available**:
-- Tritium supply dependency confirmed (D-T fuel); TBR ~1.1 from LiPb blanket, marginally self-sufficient
-- LiPb composition confirmed (17% Li, 83% Pb by mass); Li-6 enrichment likely needed for adequate TBR but not explicitly stated
-- No superconducting magnets, cryogens, or beryllium — eliminates several common critical material concerns
-- No target fabrication requirement (unlike ICF) — eliminates that supply chain challenge
-- Lead (Pb): abundant, no supply concerns
-- Bismuth: used only for Century (engineering demo), not commercial concept
+- **Capacitor supply chain**: Covered in depth in the OSTI pulsed power pre-roadmap (`iter-03/sources/osti-servlets-purl-2588719.md`). Finding: current commercial capacitor production could supply 150 plants in 125–250 years. Each plant requires 10,000–216,000 capacitors. Lifetime gap: need 10⁹ shots, current state of art is 10⁴–10⁵. This is a sector-wide critical bottleneck — especially severe for Zap's high-rep-rate capacitor-discharge approach.
+- **High-voltage switching**: Same OSTI source identifies solid-state switch development as a near-term priority; 50–200 kV, 50–200 kA, microsecond timescales required.
+- **LiPb blanket**: Material choice discussed in Engineering Paradigms paper. Lead-lithium eutectic, activation products (²¹⁰Po, ²⁰³Hg) mentioned with mitigation by isotope control. No supply chain analysis.
+- **No external magnet materials**: Absence of HTS or superconducting coils is a deliberate differentiator — eliminates a major supply chain concern present in other MFE concepts.
 
 **Missing**:
-- Whether Li-6 enrichment is required (Li-6 fraction in natural Li is ~7.5%; enrichment affects blanket cost significantly)
-- Electrode material specifications and supply (high-current-density cathodes at 10 Hz)
-- Capacitor bank component supply chain at required scale (large pulsed-power capacitors)
-- LiPb total inventory requirement and lead activation concerns
-- Tritium inventory requirements and permeation through liquid metal
+- **Lithium supply chain**: Not analyzed. Lithium demand from EV industry creates competition; TBR ~1.1 means tritium self-sufficiency is marginal and lithium supply matters.
+- **Lead supply chain**: LiPb is 83% lead by fraction. Lead is abundant industrially but activation (²¹⁰Po) and its handling/disposal are not analyzed.
+- **Cathode material**: Not specified. Arc smelting furnace analogy cited but specific cathode material undefined.
+- **Dielectric film supply chain**: Key capacitor dielectric; OSTI notes 10–15 year lead time for new materials, and existing manufacturers underscale for fusion.
+- **Specialty steel/structural**: No first-wall materials analysis (LiPb is the first wall, but structural materials behind it unspecified).
 
 **Gaps**:
-- Li-6 enrichment requirement — `derivable` from TBR analysis — **important**: cost driver if enrichment needed
-- Electrode material specification and supply — `proprietary` — **nice-to-have**
-- High-rep-rate capacitor bank supply chain — `not-yet-sourced` — **nice-to-have**: analogues from pulsed power industry exist
-- Tritium inventory and permeation — `not-yet-sourced` (likely in FST 2023 paper or D-T fusion literature) — **important**
+- Lithium supply chain (EV competition) — `not-yet-sourced` — **important**
+- Capacitor dielectric supply chain scale-up — `not-yet-sourced` (partially covered in OSTI) — **important**
+- Cathode material specification and supply chain — `proprietary` — **important**
+- Lead activation product handling at scale — `not-yet-sourced` — **nice-to-have**
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Partial
+**Coverage**: Poor
 
 **Available Parameters**:
+
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Reactor thermal power | 190 MWt | Engineering Paradigms, FST 2023 | m (snippet only) |
-| Repetition rate (target) | 10 Hz | FST 2023; Zap website | h |
-| Current rep rate (Century) | 0.2 Hz | Century press releases | h |
-| Drive efficiency (wall-plug → cathode) | ~70% | Engineering Paradigms, FST 2023 | m |
-| Energy conversion pathway | Steam Rankine | FST 2023; Ben Bridger blog | h |
-| Tritium breeding ratio | ~1.1 | Engineering Paradigms, FST 2023 | m |
-| Blanket material | LiPb (17% Li, 83% Pb) | FST 2023; Zap website | h |
-| Reactor footprint | ~3 m tall | Engineering Paradigms, FST 2023 | m |
-| No external magnets | Confirmed | Multiple sources | h |
-| Plasma current range | 650 kA – 1.5 MA | FuZE-Q specs | h |
-| Driver bank energy (FuZE-Q scale) | ~1 MJ | fuze-q-and-fuze-3.md | h |
+| Thermal power per core | ~190–200 MWt | Engineering Paradigms paper, Table II | high |
+| Fusion pulse energy | 19 MJ | Engineering Paradigms paper, Table I | high |
+| Repetition rate (target) | 10 Hz | Engineering Paradigms paper; Zap website | high |
+| Plasma length | 0.5 m | Engineering Paradigms paper | high |
+| Pinch current (plant) | 1.2–1.5 MA | Engineering Paradigms paper, Table I | high |
+| Driver efficiency (wall-plug → plasma) | ~70% | Engineering Paradigms paper (90% AC-DC × 80% modulator) | medium |
+| Fusion Q (implied at plant currents) | >10 | Engineering Paradigms paper (stated qualitatively) | low |
+| TBR | ~1.1 | Engineering Paradigms paper | medium |
+| Core volume | ~25 m³ | Engineering Paradigms paper, Table II | medium |
+| Plant modules | Multiple cores for scale | Engineering Paradigms paper (qualitative) | medium |
+| Average input power (Century) | 100 kW | Century press release | high |
+| Plant-scale average input power (implied) | ~10 MW at 10 Hz | Derived from Century scaling | low |
+| Fuel type | D-T | Dossier, multiple sources | high |
+| Energy capture cycle | Steam Rankine | Engineering Paradigms paper | high |
+| Module target output | ~50 MWe (inferred from Century press release) | Century press release (size comparison) | low |
 
 **Missing Parameters**:
+
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Q value (fusion gain) | truly-unknown | blocking | FuZE-Q targets Q=1, not yet demonstrated; current devices likely Q << 1 |
-| Net electrical output (MWe) | derivable | blocking | Requires Q and recirculating power fraction; ~63 MWe if 33% thermal efficiency, but recirculating power could dominate |
-| Recirculating power fraction at 10 Hz | proprietary | blocking | At 10 MW avg input and 190 MWt output, this is ~5% — but unconfirmed |
-| Capital cost by subsystem | truly-unknown | blocking | No published estimates; no analogues cited in sources |
-| Pulsed power system specific cost ($/kWe or $/J) | not-yet-sourced | blocking | Analogues from NIF, Z Machine, ICF drivers may exist |
-| Electrode replacement cost and lifetime | truly-unknown | important | ARPA-E project active — no data yet |
-| Capacity factor / availability | truly-unknown | important | No published maintenance schedule; pulsed systems can achieve high availability in principle |
-| Thermal efficiency of steam cycle | derivable | important | ~30-35% for steam Rankine at LiPb temperatures; LiPb operating temperature not published |
-| LiPb operating temperature | not-yet-sourced | important | Needed for steam cycle efficiency; likely in full FST 2023 paper |
-| Blanket capital cost | not-yet-sourced | important | Liquid metal system analogues (FNSF, tokamak blankets) may provide rough bounds |
-| O&M cost fraction | truly-unknown | important | No published estimates; comparable pulsed concepts (Z Machine) are research tools, not commercial analogues |
-| Plant electrical output target | proprietary | important | 190 MWt × efficiency − recirculation; Zap hasn't published a MWe target |
+| Net electrical output (MWe per module/plant) | derivable | blocking | Thermal power known; need Rankine efficiency and recirculating power fraction |
+| Rankine cycle thermal efficiency | derivable | blocking | Not stated; D-T MFE analogs suggest ~35–40%; LiPb outlet temperature unspecified |
+| Recirculating power fraction | derivable | blocking | Qualitatively stated as advantageous vs. tokamak; no numerical estimate |
+| Capacity factor | proprietary | blocking | No target stated; pulsed mode enables high availability in principle; 0.2→10 Hz gap is the current constraint |
+| Direct capital cost (CAS 20–27) | proprietary | blocking | No published cost estimate; no plant study |
+| Indirect capital costs (CAS 90–98) | proprietary | blocking | No data |
+| O&M cost (annual) | proprietary | blocking | No data; cathode replacement and capacitor bank maintenance are key unknown drivers |
+| Cathode replacement interval | proprietary | important | "Small volume and mass" mentioned; arc furnace analogy; no specific number |
+| Capacitor bank replacement schedule | not-yet-sourced | important | OSTI notes 10⁴–10⁵ shot lifetime; at 10 Hz this is 1–10 days → replacement cost is potentially enormous |
+| Tritium fuel cost | derivable | important | TBR ~1.1 gives margin; startup inventory needs quantification |
+| Decommissioning cost | derivable | nice-to-have | LiPb activation products (²¹⁰Po) are the main concern; standard fission-derived analogs may overestimate |
+| LCOE projection | proprietary | blocking | No published estimate from Zap or third party |
+
+**Critical derivation note on capacitor replacement**: The OSTI source documents that current high-voltage capacitor lifetime is 10⁴–10⁵ shots under research conditions. At 10 Hz operation (10 shots/second = 864,000 shots/day), a plant would exhaust the rated lifetime of current capacitors in under a day. This is a commercially non-viable gap that would dominate O&M costs and represents a sector-defining supply chain challenge. This is not blocking for analysis but is a critical engineering risk that must be prominently featured in the concept analysis.
 
 ---
 
 ## Source Recommendations
 
-1. **Full text of Engineering Paradigms for SFS Z-Pinch Fusion Energy (FST 2023)** — `not-yet-sourced` — institutional library access to Fusion Science & Technology would unlock blanket geometry, electrode design, and possibly cost discussion. Search: tandfonline.com DOI 10.1080/15361055.2023.2209131. *Flag: paper confirmed to exist; content beyond snippets unverified.*
+1. **Zap Energy Physics of Plasmas 2023 paper** ("The Zap Energy approach to commercial fusion," Levitt et al., PoP 30, 090603, 2023) — `not-yet-sourced` — may contain quantitative plasma parameter projections and Q estimates. Search OSTI or request preprint; DOI: 10.1063/5.0122381. *Unverified — confirm open-access availability before sourcing.*
 
-2. **Full text of "The Zap Energy approach to commercial fusion" (Physics of Plasmas 2023)** — `not-yet-sourced` — AIP open access check or institutional access. DOI: pubs.aip.org/aip/pop/article/30/9/090603. *Flag: confirmed to exist; AIP PoP articles are sometimes open access after a year.*
+2. **DOE Milestone-Based Fusion Development Program reports for Zap Energy** — `not-yet-sourced` — DOE certifies milestones publicly (one example already in dossier). FOIA or DOE fusion program pages may have milestone specifications and possibly performance targets. *Unverified — check DOE fusion portal.*
 
-3. **Full text of Century paper (FST 2025)** — `not-yet-sourced` — same journal; details on power handling architecture would inform rep-rate scaling and pulsed power cost modeling. *Flag: confirmed to exist; paywalled.*
+3. **ARPA-E ALPHA program — Z-pinch costing** — `not-yet-sourced` — The ALPHA program funded University of Washington Z-pinch work (Uri Shumlak's group, Zap's origin). If the revisit of 2017 ALPHA costing (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) includes the UW SFS Z-pinch as one of the four concepts, it would be the only published CAS-level cost analysis for this concept. *Unverified — open the ALPHA costing source to check concept list before relying on it.*
 
-4. **Pulsed power system cost analogues from ICF or defense literature** — `not-yet-sourced` — search OSTI for pulsed power driver cost studies (e.g., from Z Machine, NIF pulsed power, or NNSA driver technology reports). Z pinch pulsed power is architecturally similar to Z Machine drivers. *Flag: unverified — confirm existence before searching.*
+4. **Forbes et al. (FST 2019)** — "Progress Toward a Compact Fusion Reactor Using the Sheared-Flow-Stabilized Z-Pinch" — cited as Ref. 14 in Engineering Paradigms paper, including TBR and LiPb calculations. May contain additional plant parameter details not in the 2023 paper. *Unverified — check OSTI availability.*
 
-5. **ARPA-E project reports on electrode technology development** — `not-yet-sourced` — ARPA-E project page links are indexed; final technical reports may be on OSTI. Search ARPA-E DE-AR0001554 or similar project number for electrode development deliverables. *Flag: unverified — ARPA-E project confirmed, but final reports may not be public.*
+5. **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — applicable as BOP, steam cycle, and tritium handling cost analog. Not Z-pinch-specific but provides CAS-level cost methodology for D-T fusion with steam extraction. Use as analog for CAS 22 (heat transfer), CAS 25 (fuel handling), CAS 26 (power conversion).
 
-6. **Ben Levitt APS DPP 2025 presentation slides or proceedings** — `not-yet-sourced` — APS DPP proceedings sometimes have extended abstracts with quantitative data. The abstract cited mentions "progress towards commercial fusion." *Flag: abstract confirmed; full slides unverified.*
+6. **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/`) — applicable as the CAS framework reference for structuring any cost estimate. Should be used to structure LCOE placeholder table with clearly flagged unknowns.
 
-7. **Tritium permeation and inventory literature for LiPb systems** — `not-yet-sourced` — large body of work from ITER TBM programs, FTF studies. Tritium behavior in flowing LiPb is well-studied in the tokamak context and could provide bounds for SFS Z-pinch. Search OSTI for "LiPb tritium permeation" or "flowing liquid metal tritium inventory."
+7. **Pulsed power capacitor cost literature** — `not-yet-sourced` — Search IEEE Transactions on Plasma Science or PPPS conference proceedings for $/J or $/kJ capacitor cost data, enabling rough pulsed power bank capital cost estimate. Hegeler et al. (IEEE Trans. Dielectr. Electr. Insul., 2011 — Ref. 20 in Engineering Paradigms paper) may contain cost-relevant efficiency data.
 
 ---
 
 ## Summary
 
-**Proceed to full analysis.** The qualitative write-up is well-supported: physics rationale, architecture, device lineage, and the reactor concept's major design choices are all documented from public sources. The Engineering Paradigms paper (FST 2023) provides sufficient anchors (190 MWt, 10 Hz, LiPb, TBR ~1.1, steam Rankine, ~70% driver efficiency) for a first-pass quantitative model.
+**Proceed to full analysis.** The concept description, physics basis, and engineering design rationale are well enough documented for a D1+ qualitative analysis covering system function, subsystem maturity, and supply chain challenges. The Engineering Paradigms paper (Thompson et al., FST 2023) is an unusually comprehensive source for a private company at this stage. The OSTI pulsed power roadmap document provides strong coverage of the sector's critical supply chain gap (capacitor lifetime and manufacturing scale-up).
+
+The LCOE section will require explicit analog-based estimation with acknowledged uncertainty. The most important pre-analysis step is checking whether the ARPA-E ALPHA 2017 revisit covers the UW SFS Z-pinch concept, as that would be the only CAS-level cost reference in the repo applicable to this concept.
 
-The quantitative LCOE model will require explicit `derivable` assumptions for most economic parameters, since no capital cost estimates exist in the literature. The critical path is: assume Q=1 (FuZE-Q target, not yet achieved), assume recirculating power from the 10 Hz pulsed power system, estimate thermal efficiency from LiPb operating temperatures, and apply pulsed-power cost analogues for the driver system. The analysis should clearly flag that these are model assumptions, not published data, and the back-solve to $0.01/kWh will be highly informative precisely because no one has published whether this concept can plausibly reach that target.
+The commercially critical finding to highlight: at 10 Hz operation, current-generation capacitors would require replacement after ~1 day of operation — this gap (10⁴–10⁵ shot lifetime vs. 10⁹+ needed) is the dominant O&M risk and may be the single largest economic uncertainty in the entire concept.
 
-The two most critical data gaps — **Q value** and **capital cost structure** — are endemic to the current state of the technology (pre-breakeven, no plant study), not sourcing gaps. The qualitative uncertainty section should feature both prominently.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Mostly Ready"
-blocking_count: 5
-important_count: 7
-counting_method: "section_5_missing_parameters"
+blocking_count: 6
+important_count: 9
+counting_method: "section_5_missing_parameters_blocking_count_plus_section_1_economic_analysis_gap; important from sections 2-4 plus section 5 important row count; deduplicated across sections"
 section_coverage:
-  availability_of_data:       "Moderate"
-  system_function:            "Partial"
+  availability_of_data:       "Partial"
+  system_function:            "Good"
   subsystem_maturity:         "Partial"
-  materials_supply_chain:     "Poor"
-  lcoe_parameter_extraction:  "Partial"
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
