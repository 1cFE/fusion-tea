# Phase 3 diff: 15-sheared-flow-stabilized-z-pinch

**Generated:** 2026-05-22T14:19:51-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 6 | 4 | -2 |
| important_count  | 9 | 6 | - |
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
Now I have all the information needed to write the gap assessment. Let me compile the findings.
```

## Blocking-tier lines (new)

```
133:| Net thermal-to-electric efficiency (quantitative) | derivable | blocking | 50 MWe / 200 MWt implies ~25% gross, but recirculating power fraction unknown; net unclear |
134:| Recirculating power fraction | proprietary | blocking | Thompson FST 2023 argues "better than tokamaks" (0.4–0.6) but gives no number; plant Q > 10 implies substantial recirculation headroom |
135:| Capital cost breakdown (Z-pinch specific, CAS 22.1.7 pulsed power driver) | proprietary | blocking | Widest cost range in ALPHA study ($11.9–140.4M for power supplies) — Zap's specific value proprietary |
141:| Physics performance gap to plant conditions | truly-unknown | blocking | 1.6 GPa / ~1 keV (FuZE-3) vs. 35 keV / Q > 10 required; 2+ orders of magnitude in T, ~3 in density |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/15-sheared-flow-stabilized-z-pinch.md	2026-05-22 12:59:21.069617019 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/15-sheared-flow-stabilized-z-pinch/gap_report.md	2026-05-22 14:19:51.412938073 -0700
@@ -1,88 +1,80 @@
-I have enough information to write the gap assessment. Let me compile the report now.
-
----
+Now I have all the information needed to write the gap assessment. Let me compile the findings.
 
 # Gap Assessment: Sheared-Flow Stabilized Z-Pinch (D-T)
 
 ## Overall Readiness
 **Rating**: Mostly Ready
-**Summary**: Zap Energy's SFS Z-pinch is unusually well-documented at the physics and engineering-concept level for an early-stage private fusion company. The Thompson et al. (FST 2023) paper provides a coherent conceptual power plant design with specific parameters, and the Century/FuZE-3 press releases provide current experimental status. The critical gap is economics: Zap has published no capital cost estimates, no O&M projections, no capacity factor targets, and no LCOE analysis. A D1+ qualitative analysis can proceed confidently; quantitative LCOE parametrization requires analogs from fleet-wide sources and explicit derivation assumptions.
+
+**Summary**: The SFS Z-pinch is unusually well-documented for a pre-commercial fusion concept. The Engineering Paradigms paper (Thompson et al., FST 2023) provides a coherent conceptual plant design with nominal power parameters, energy balance logic, and qualitative cost drivers. The ARPA-E ALPHA concepts study (Woodruff Scientific, 2020) explicitly costed the Zap Energy flow-stabilized Z-pinch alongside three other concepts, providing a CAS-structured LCOE benchmark (~$43/MWh for a ~500 MWe plant) even though concept-specific figures were delivered proprietary. The main gap is physics maturity: FuZE-3's best result (1.6 GPa pressure, ~1 keV electron temperature) is still orders of magnitude below the plant-relevant conditions (35 keV, Q > 10) assumed in the conceptual design, and no published Q estimates from experiments exist. Most cost-model parameters are derivable from published conceptual design values, but the critical pulsed power driver cost is highly uncertain and likely proprietary.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Partial
+**Coverage**: Good
 
 **Available**:
-- Full physics and concept description from the Engineering Paradigms paper (`iter-01/sources/engineering-paradigms-paper-summary.md`), Zap's website (`iter-01/sources/zap-energy-website-how-it-works.md`), and FuZE-3 press releases (`iter-02/sources/fuze-3-gigapascal-results-2025.md`). These cover: plasma formation mechanism, self-pinching physics, sheared-flow stabilization, liquid metal blanket design, pulsed power driver architecture, and qualitative economics arguments.
-- Experimental progress: FuZE device series (FuZE → FuZE-Q → FuZE-3 → FuZE-A upcoming), with performance data through FuZE-3's 1.6 GPa plasma pressure milestone.
-- Company status: $330M raised, 150 employees, Century operational at 0.2 Hz (`iter-01/sources/century-demo-system.md`), DOE Milestone-Based program participation.
-- Pulsed power technology challenges (supply chain, component lifetimes) documented in OSTI pre-roadmap (`iter-03/sources/osti-servlets-purl-2588719.md`).
+- Full conceptual plant design paper (Thompson et al., FST 2023) covering plasma parameters at each development step, plant architecture, blanket concept, and efficiency rationale. Open access.
+- ARPA-E ALPHA concepts costing study (Woodruff Scientific 2020) explicitly includes Zap Energy's flow-stabilized Z-pinch; provides anonymized CAS-level cost averages across four pulsed modular concepts as a benchmark.
+- Experimental device progression (FuZE → FuZE-Q → FuZE-3) documented via press releases and APS DPP abstracts.
+- Century demo platform documented: 100 kW input power, 0.2 Hz, 500 kA, liquid bismuth wall, press releases confirm 50 MWe per module as Zap's stated plant target.
+- OSTI pulsed power roadmap (2025) characterizes pulsed power component supply chain gaps directly relevant to Z-pinch driver systems.
+- Zap Energy company: ~$330M raised, ~150 employees, DOE Milestone-Based Fusion Development Program participant — high corporate transparency relative to most alt-fusion startups.
 
 **Missing**:
-- No published full plant study or systems code analysis (the Engineering Paradigms paper is a preconceptual conceptual overview, not a plant design study).
-- No independent peer-reviewed techno-economic analysis of Zap's concept.
-- No access to full text of the Physics of Plasmas 2023 paper ("The Zap Energy approach to commercial fusion") — listed in dossier as paywalled, detailed content absent.
-- No cost modeling or economic projections from Zap or third parties.
+- Full text of paywalled key papers (Thompson FST 2023 — obtained via extracted PDF; Physics of Plasmas 2023 overview paper — NOT in sources; Century FST 2025 paper — NOT in sources beyond press release snippets).
+- The Physics of Plasmas 2023 paper (Levitt et al.) likely contains updated plasma physics basis but only the APS DPP 2025 abstract is available.
 
 **Gaps**:
-- No published plant-level economic analysis — `proprietary` — **blocking** for LCOE
-- Full text of PoP 2023 paper unavailable — `not-yet-sourced` — **important** (may contain additional plasma parameter details)
-- Full text of Century FST 2025 paper unavailable — `not-yet-sourced` — **important** (Century details from press releases only)
+- Full text of Physics of Plasmas 2023 overview paper — `not-yet-sourced` — nice-to-have (Thompson FST 2023 covers most content)
+- Full text of Century FST 2025 paper — `not-yet-sourced` — important (engineering platform details for plant power handling subsystems)
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Good
+**Coverage**: Partial
 
 **Available**:
-- **Plasma confinement and heating**: Complete from Engineering Paradigms paper. J×B self-pinch with ohmic heating driven by axial current; sheared flow extends stability. No external magnets. Unity beta plasma at ~0.15 mm radius, 0.5 m length at plant scale. Described quantitatively in Table I of the paper.
-- **Pulsed power driver**: Capacitor bank → PFN → plasma cathode pathway, ~70% wall-plug efficiency. Solid-state thyristor switches demonstrated at 80% efficiency at 5 Hz. FuZE-3 uses two separate capacitor banks and three-electrode design for independent acceleration/compression control.
-- **Liquid metal blanket**: LiPb eutectic weir-wall design described conceptually. Gravity-driven cascade forms first wall, terminates pinch current, absorbs fusion neutrons, breeds tritium. TBR ~1.1. Century uses liquid bismuth (non-DT engineering testbed).
-- **Power conversion**: Steam Rankine cycle extracting heat from LiPb, confirmed in Engineering Paradigms paper and corroborated by independent blog summary.
-- **Pulsed power scale-up challenge**: Century at 0.2 Hz / 100 kW average power; commercial target is 10 Hz / ~10 MW average input power. Gap is well-characterized in the sources.
+- Thompson FST 2023 provides clear system function description: pulsed axial current → pinch → ohmic heating → fusion → LiPb absorbs energy → steam Rankine cycle. No external magnets, no auxiliary heating.
+- Wall-plug to plasma electrical efficiency ~70% explicitly documented (AC-DC rectification ~90%, pulsed power modulator ~80%).
+- Pulsed operation analogy to internal combustion engine clearly articulated; load-following capability described.
+- Recirculating power discussion: tokamaks cited at 0.4-0.6 recirculating fraction; SFS Z-pinch argued to be lower due to direct coupling.
+- Engineering Paradigms paper identifies cathode as the primary materials challenge (direct plasma contact, neutron bombardment); all other solid structure shielded by LiPb.
+- OSTI pulsed power roadmap (2025) characterizes the key engineering challenge for all pulsed-power-driven fusion: high-voltage capacitor lifetime (currently 10⁴–10⁵ shots; plant needs 10⁹), solid-state switching for 50–200 kV at repetitive rates, and lead time for large-volume capacitor orders (4–6 years; 10,000–216,000 capacitors per plant).
 
 **Missing**:
-- **Tritium extraction loop**: Mentioned (pumped out, through heat exchanger and "tritium extraction stage") but no process details.
-- **LiPb pumping system design**: Mentioned but not quantified (power, flow rate, pump type). High density of LiPb makes pumping power non-trivial.
-- **Cathode wear mechanism and replacement cycle**: Qualitative discussion (arc smelting analogy, "small volume and mass") but no replacement interval or maintenance schedule specified.
-- **Thermal cycle efficiency**: Specific Rankine cycle conditions (steam temperature/pressure, efficiency) not stated.
-- **Plasma stability at high currents**: Explicitly acknowledged as unresolved in Engineering Paradigms paper. Whether sheared-flow stabilization holds at 1.2–1.5 MA is an open physics question.
+- The path from 0.2 Hz (Century current) to 10 Hz (commercial target) involves a ~50× increase in average input power, from ~100 kW to ~10 MW per module. The engineering challenges of this scaling are acknowledged but not quantified in published sources.
+- Tritium handling and extraction from LiPb at continuous-operation rates is not described in detail in public sources.
+- Actual recirculating power fraction at plant conditions: stated qualitatively as "better than tokamaks" but no published number.
 
 **Gaps**:
-- Tritium extraction process design — `not-yet-sourced` — **important** (search LLNL/ITER tritium handling analogs)
-- Rankine cycle efficiency specification — `derivable` from steam cycle analogs in TEA sources — **important**
-- Cathode replacement interval — `proprietary` — **important**
-- High-current stability scaling — `truly-unknown` (experimentally unresolved) — **important** (key physics risk)
+- Recirculating power fraction (quantitative) — `proprietary` — important (critical for net electric efficiency calculation)
+- Rep-rate scaling from 0.2 Hz to 10 Hz engineering solution — `proprietary` — important (determines capacity factor trajectory)
+- Tritium extraction process details from LiPb — `not-yet-sourced` — nice-to-have (LiPb tritium extraction literature exists from ITER blanket studies)
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
 **Coverage**: Partial
 
-**Available**: Per-subsystem TRL can be inferred from experimental status in the sources.
-
-| Subsystem | TRL Estimate | Basis |
-|-----------|-------------|-------|
-| SFS Z-pinch plasma (physics) | 3–4 | FuZE demonstrated thermonuclear neutrons; FuZE-3 at 1.6 GPa; still ~3 orders of magnitude below power plant density/temperature/current |
-| Repetitive pulsed power | 4–5 | Century at 0.2 Hz / 100 kW; target 10 Hz / 10 MW; subscale demonstration at 5 Hz in literature |
-| Cathode / electrode tech | 3–4 | Century testing cathode durability; 1000+ shots demonstrated; no lifetime data |
-| Liquid metal wall system | 3 | First integrated test at Century (liquid Bi, non-fusing); no fusing plasma + LiPb co-test |
-| Tritium breeding blanket | 2–3 | LiPb design with TBR ~1.1 calculated; no prototype tritium loop |
-| Steam power conversion | 8–9 | Commercial technology; applicable directly |
-| Solid-state pulsed power switches | 4–5 | Demonstrated at 5 Hz calorimetrically; long-lifetime at 10 Hz not demonstrated |
-| High-voltage capacitor bank | 4–5 | Functional at research scale; lifetime-at-rep-rate not demonstrated |
+**Available**:
+- Plasma physics (TRL 3–4): FuZE-3 demonstrated 1.6 GPa total pressure, ~1 keV electron temperature, 3–5×10²⁴ m⁻³ density. Thermonuclear neutron production confirmed on FuZE (Zhang et al., PRL 2019). Still ~2 orders of magnitude below plant-relevant plasma conditions.
+- Pulsed power driver (TRL 4): Solid-state thyristor switches demonstrated at 80% efficiency at 5 Hz (Hegeler et al., 2011, cited in Thompson FST 2023). Century testing at 0.2 Hz with 100 kW. Path to 10 Hz and 10 MW per module not yet demonstrated.
+- Liquid metal wall (TRL 3–4): Century is "one of the largest tests of a plasma-facing liquid metal blanket to date." Liquid bismuth used in Century (not LiPb). 1,080 consecutive shots demonstrated.
+- Cathode durability (TRL 2–3): Identified as key challenge. Decades of arc smelting furnace experience cited as analogy (60 MW, non-nuclear). No direct testing at plant-relevant neutron flux.
+- Blanket/breeding (TRL 2–3): TBR ~1.1 calculated for LiPb; Monte Carlo simulations only. Not tested with actual D-T neutron flux.
+- Pulsed power supply chain (TRL 2–3): OSTI 2025 roadmap explicitly identifies this as a blocking supply chain gap across all pulsed fusion concepts; capacitor lifetime and solid-state switch development are pre-commercial.
 
 **Missing**:
-- No formal TRL assessment from Zap or DOE published.
-- FuZE-Q performance data not directly available in sources (FuZE-Q undergoing operations alongside FuZE-3 per press release).
-- No MHD analysis of LiPb flow near the electrode current termination region.
+- Q > 1 demonstration: Current experiments are sub-breakeven by orders of magnitude. No published estimate of when Q > 1 is expected.
+- TRL assessment for the LiPb tritium breeding system under actual neutron irradiation.
 
 **Gaps**:
-- Independent TRL assessment — `not-yet-sourced` — **important** (search DOE Milestone program reports)
-- FuZE-Q performance data and current/neutron yield — `not-yet-sourced` — **important**
+- Q > 1 / scientific breakeven demonstration — `truly-unknown` (hasn't happened yet) — blocking (required to anchor any cost model Q assumption)
+- Cathode lifetime under DT-relevant neutron flux — `proprietary` — important (drives scheduled replacement cost, major O&M driver)
+- Capacitor/switch lifetime at 10 Hz, 10⁹ shots — `truly-unknown` at required spec — blocking (supply chain fundamentally not ready per OSTI 2025 roadmap; no commercial product at required lifetime)
+- LiPb tritium breeding tested under neutron flux — `truly-unknown` (only Monte Carlo calculations) — important
 
 ---
 
@@ -90,95 +82,85 @@
 **Coverage**: Partial
 
 **Available**:
-- **Capacitor supply chain**: Covered in depth in the OSTI pulsed power pre-roadmap (`iter-03/sources/osti-servlets-purl-2588719.md`). Finding: current commercial capacitor production could supply 150 plants in 125–250 years. Each plant requires 10,000–216,000 capacitors. Lifetime gap: need 10⁹ shots, current state of art is 10⁴–10⁵. This is a sector-wide critical bottleneck — especially severe for Zap's high-rep-rate capacitor-discharge approach.
-- **High-voltage switching**: Same OSTI source identifies solid-state switch development as a near-term priority; 50–200 kV, 50–200 kA, microsecond timescales required.
-- **LiPb blanket**: Material choice discussed in Engineering Paradigms paper. Lead-lithium eutectic, activation products (²¹⁰Po, ²⁰³Hg) mentioned with mitigation by isotope control. No supply chain analysis.
-- **No external magnet materials**: Absence of HTS or superconducting coils is a deliberate differentiator — eliminates a major supply chain concern present in other MFE concepts.
+- LiPb eutectic (17% Li, 83% Pb): Properties documented; neutron multiplication via Pb(n,2n) reaction leveraged for TBR ~1.1. Activation products (²¹⁰Po, ²⁰³Hg) identified; ²⁰³Hg mitigable by isotope control. No superconducting magnets — eliminates dominant ITER/tokamak material cost driver.
+- Cathode material: Unspecified in published sources; arc smelting analogs cited. Copper or graphite-based analogues likely but not confirmed.
+- Capacitor dielectrics: OSTI 2025 roadmap characterizes current BOPP film capacitors at 1–3 J/cm³ energy density, 10⁴–10⁵ shot lifetime; advanced films (Peak Nano NanoPlex) could reduce volume by 4–8×. 10 year–15 year valley-of-death for new dielectric scale-up.
+- OSTI 2025: "If 150 fusion power plants were to be built today to service the United States, the time required to build the required capacitors is approximately 125–250 years given western world available manufacturers." Directly characterizes the Z-pinch supply chain bottleneck.
+- Solid-state switches: WBG materials (SiC MOSFETs at 6.5–10 kV commercial; custom at 15–20 kV); target 100–200 kV/100–200 kA switches do not currently exist.
 
 **Missing**:
-- **Lithium supply chain**: Not analyzed. Lithium demand from EV industry creates competition; TBR ~1.1 means tritium self-sufficiency is marginal and lithium supply matters.
-- **Lead supply chain**: LiPb is 83% lead by fraction. Lead is abundant industrially but activation (²¹⁰Po) and its handling/disposal are not analyzed.
-- **Cathode material**: Not specified. Arc smelting furnace analogy cited but specific cathode material undefined.
-- **Dielectric film supply chain**: Key capacitor dielectric; OSTI notes 10–15 year lead time for new materials, and existing manufacturers underscale for fusion.
-- **Specialty steel/structural**: No first-wall materials analysis (LiPb is the first wall, but structural materials behind it unspecified).
+- Lithium-6 enrichment needs for LiPb with adequate TBR — not explicitly stated in sources.
+- Lead supply chain: Lead is abundant but specific isotope or purity requirements not stated.
+- Structural material (first-wall surroundings, tank): Not specified in published sources.
 
 **Gaps**:
-- Lithium supply chain (EV competition) — `not-yet-sourced` — **important**
-- Capacitor dielectric supply chain scale-up — `not-yet-sourced` (partially covered in OSTI) — **important**
-- Cathode material specification and supply chain — `proprietary` — **important**
-- Lead activation product handling at scale — `not-yet-sourced` — **nice-to-have**
+- Cathode material specification and supply chain — `proprietary` — nice-to-have (small mass, replaceable)
+- Li-6 enrichment fraction needed for TBR — `not-yet-sourced` — important (affects tritium self-sufficiency)
+- High-rep-rate solid-state switch supply chain at 100–200 kV/100–200 kA — `truly-unknown` at required spec — blocking for commercial plant (per OSTI 2025 roadmap)
+- Capacitor supply chain at 10⁹ shot lifetime — `truly-unknown` at required spec — blocking for commercial plant
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor
-
 **Available Parameters**:
-
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Thermal power per core | ~190–200 MWt | Engineering Paradigms paper, Table II | high |
-| Fusion pulse energy | 19 MJ | Engineering Paradigms paper, Table I | high |
-| Repetition rate (target) | 10 Hz | Engineering Paradigms paper; Zap website | high |
-| Plasma length | 0.5 m | Engineering Paradigms paper | high |
-| Pinch current (plant) | 1.2–1.5 MA | Engineering Paradigms paper, Table I | high |
-| Driver efficiency (wall-plug → plasma) | ~70% | Engineering Paradigms paper (90% AC-DC × 80% modulator) | medium |
-| Fusion Q (implied at plant currents) | >10 | Engineering Paradigms paper (stated qualitatively) | low |
-| TBR | ~1.1 | Engineering Paradigms paper | medium |
-| Core volume | ~25 m³ | Engineering Paradigms paper, Table II | medium |
-| Plant modules | Multiple cores for scale | Engineering Paradigms paper (qualitative) | medium |
-| Average input power (Century) | 100 kW | Century press release | high |
-| Plant-scale average input power (implied) | ~10 MW at 10 Hz | Derived from Century scaling | low |
-| Fuel type | D-T | Dossier, multiple sources | high |
-| Energy capture cycle | Steam Rankine | Engineering Paradigms paper | high |
-| Module target output | ~50 MWe (inferred from Century press release) | Century press release (size comparison) | low |
+| Thermal power per core | ~200 MWt | Thompson FST 2023, Table I | h |
+| Net electric power per module | ~50 MWe | Century press release (Zap) | m |
+| Net electric power (plant, 3–4 modules) | ~383–814 MWe | ARPA-E ALPHA (Woodruff 2020), Table 2 | m |
+| Repetition rate (commercial target) | 10 Hz | Thompson FST 2023, Zap website | h |
+| Fusion energy per pulse | 19 MJ | Thompson FST 2023, Table I | m |
+| Plant Q (fusion power / input power) | > 10 | Thompson FST 2023 | m |
+| Wall-plug to plasma efficiency | ~70% | Thompson FST 2023 (AC-DC ~90%, modulator ~80%) | h |
+| Energy conversion cycle | Steam Rankine | Thompson FST 2023, Ben Bridger blog | h |
+| Tritium breeding ratio | ~1.1 | Thompson FST 2023 (Monte Carlo only) | m |
+| Plant availability / capacity factor | 90% | ARPA-E ALPHA (Woodruff 2020, costing assumption) | m |
+| Total Capital Cost (benchmark, ~500 MWe 4-concept avg) | $1.2B avg ($0.8–1.6B range) | ARPA-E ALPHA (Woodruff 2020), Table 3 | l |
+| CapEx (benchmark) | ~2.4 $/W ($2.0–3.3) | ARPA-E ALPHA (Woodruff 2020), Table 4 | l |
+| LCOE (benchmark, learning-curve COE2) | ~43 $/MWh ($34–54 range) | ARPA-E ALPHA (Woodruff 2020), Table 4 | l |
+| O&M costs (benchmark) | ~48 M$/year ($42–61) | ARPA-E ALPHA (Woodruff 2020), Table 4 | l |
+| Scheduled replacement costs (benchmark) | ~17 M$/year ($6–30) | ARPA-E ALPHA (Woodruff 2020), Table 4 | l |
+| Power supplies CAS 22.1.7 (benchmark) | $55.8M avg ($11.9–140.4M) | ARPA-E ALPHA (Woodruff 2020), Table 3 | l |
+| First wall/blanket CAS 22.1.1 (benchmark) | $57.3M avg ($3.6–116.5M) | ARPA-E ALPHA (Woodruff 2020), Table 3 | l |
+| Special materials CAS 27 (LiPb, benchmark) | $103.1M avg ($1.4–266.9M) | ARPA-E ALPHA (Woodruff 2020), Table 3 | l |
+| Fuel cost | ~negligible | ARPA-E ALPHA (Woodruff 2020) ~$0.1M/yr | h |
 
-**Missing Parameters**:
+*Note: ARPA-E ALPHA values are anonymized averages across four concepts (Plasma-Jet MIF, Stabilized Liner Compressor, Staged Z-Pinch, and Flow-stabilized Z-Pinch). Zap Energy-specific CAS line items were delivered proprietary. Low confidence for Z-pinch-specific cost application.*
 
+**Missing Parameters**:
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Net electrical output (MWe per module/plant) | derivable | blocking | Thermal power known; need Rankine efficiency and recirculating power fraction |
-| Rankine cycle thermal efficiency | derivable | blocking | Not stated; D-T MFE analogs suggest ~35–40%; LiPb outlet temperature unspecified |
-| Recirculating power fraction | derivable | blocking | Qualitatively stated as advantageous vs. tokamak; no numerical estimate |
-| Capacity factor | proprietary | blocking | No target stated; pulsed mode enables high availability in principle; 0.2→10 Hz gap is the current constraint |
-| Direct capital cost (CAS 20–27) | proprietary | blocking | No published cost estimate; no plant study |
-| Indirect capital costs (CAS 90–98) | proprietary | blocking | No data |
-| O&M cost (annual) | proprietary | blocking | No data; cathode replacement and capacitor bank maintenance are key unknown drivers |
-| Cathode replacement interval | proprietary | important | "Small volume and mass" mentioned; arc furnace analogy; no specific number |
-| Capacitor bank replacement schedule | not-yet-sourced | important | OSTI notes 10⁴–10⁵ shot lifetime; at 10 Hz this is 1–10 days → replacement cost is potentially enormous |
-| Tritium fuel cost | derivable | important | TBR ~1.1 gives margin; startup inventory needs quantification |
-| Decommissioning cost | derivable | nice-to-have | LiPb activation products (²¹⁰Po) are the main concern; standard fission-derived analogs may overestimate |
-| LCOE projection | proprietary | blocking | No published estimate from Zap or third party |
-
-**Critical derivation note on capacitor replacement**: The OSTI source documents that current high-voltage capacitor lifetime is 10⁴–10⁵ shots under research conditions. At 10 Hz operation (10 shots/second = 864,000 shots/day), a plant would exhaust the rated lifetime of current capacitors in under a day. This is a commercially non-viable gap that would dominate O&M costs and represents a sector-defining supply chain challenge. This is not blocking for analysis but is a critical engineering risk that must be prominently featured in the concept analysis.
+| Net thermal-to-electric efficiency (quantitative) | derivable | blocking | 50 MWe / 200 MWt implies ~25% gross, but recirculating power fraction unknown; net unclear |
+| Recirculating power fraction | proprietary | blocking | Thompson FST 2023 argues "better than tokamaks" (0.4–0.6) but gives no number; plant Q > 10 implies substantial recirculation headroom |
+| Capital cost breakdown (Z-pinch specific, CAS 22.1.7 pulsed power driver) | proprietary | blocking | Widest cost range in ALPHA study ($11.9–140.4M for power supplies) — Zap's specific value proprietary |
+| Cathode replacement schedule and unit cost | proprietary | important | Dominant scheduled replacement cost driver; only qualitative treatment in published sources |
+| LiPb loop cost (pumps, heat exchangers, tritium extraction) | derivable | important | ITER/DEMO LiPb loop engineering studies exist; LiPb is common blanket material |
+| Plant scaling: modules per plant, shared infrastructure | proprietary | important | Thompson FST 2023 mentions multi-module plants sharing tritium infrastructure but no specific module count or cost allocation |
+| Capacity factor trajectory to commercial operation | proprietary | important | Century at 0.2 Hz; commercial at 10 Hz — no published ramp schedule or first-plant CF estimate |
+| O&M staffing and annual costs (Z-pinch specific) | derivable | important | Could use ARPA-E ALPHA analog ($48M/yr) scaled to single-concept estimates |
+| Physics performance gap to plant conditions | truly-unknown | blocking | 1.6 GPa / ~1 keV (FuZE-3) vs. 35 keV / Q > 10 required; 2+ orders of magnitude in T, ~3 in density |
 
 ---
 
 ## Source Recommendations
 
-1. **Zap Energy Physics of Plasmas 2023 paper** ("The Zap Energy approach to commercial fusion," Levitt et al., PoP 30, 090603, 2023) — `not-yet-sourced` — may contain quantitative plasma parameter projections and Q estimates. Search OSTI or request preprint; DOI: 10.1063/5.0122381. *Unverified — confirm open-access availability before sourcing.*
-
-2. **DOE Milestone-Based Fusion Development Program reports for Zap Energy** — `not-yet-sourced` — DOE certifies milestones publicly (one example already in dossier). FOIA or DOE fusion program pages may have milestone specifications and possibly performance targets. *Unverified — check DOE fusion portal.*
+1. **Physics of Plasmas 2023 — "The Zap Energy approach to commercial fusion" (Levitt et al.)** — `not-yet-sourced`. This appears to be the primary peer-reviewed overview paper for the commercialization strategy. DOI: 10.1063/5.0211179 (AIP). May be open-access or available via OSTI. Search OSTI for the DOI. Would improve physics basis section.
 
-3. **ARPA-E ALPHA program — Z-pinch costing** — `not-yet-sourced` — The ALPHA program funded University of Washington Z-pinch work (Uri Shumlak's group, Zap's origin). If the revisit of 2017 ALPHA costing (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) includes the UW SFS Z-pinch as one of the four concepts, it would be the only published CAS-level cost analysis for this concept. *Unverified — open the ALPHA costing source to check concept list before relying on it.*
+2. **Century FST 2025 paper** — `not-yet-sourced`. Full engineering platform paper. DOI: 10.1080/15361055.2025.2532331 (Taylor & Francis). Likely paywalled; check if OSTI preprint available. Would provide quantitative Century performance data (shot count, thermal load, electrode erosion rates).
 
-4. **Forbes et al. (FST 2019)** — "Progress Toward a Compact Fusion Reactor Using the Sheared-Flow-Stabilized Z-Pinch" — cited as Ref. 14 in Engineering Paradigms paper, including TBR and LiPb calculations. May contain additional plant parameter details not in the 2023 paper. *Unverified — check OSTI availability.*
+3. **FuZE-3 journal publication (planned for 2026 per Zap press release)** — `not-yet-sourced` (paper announced but not yet published as of research date). Monitor arXiv physics.plasm-ph for Zap Energy FuZE-3 results. Would provide triple product data at 1 keV / high density.
 
-5. **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — applicable as BOP, steam cycle, and tritium handling cost analog. Not Z-pinch-specific but provides CAS-level cost methodology for D-T fusion with steam extraction. Use as analog for CAS 22 (heat transfer), CAS 25 (fuel handling), CAS 26 (power conversion).
+4. **ARPA-E ALPHA proprietary Z-pinch costing report** — `proprietary`. The Woodruff Scientific study delivered a proprietary CAS-level cost breakdown to Zap Energy. Not publicly available. The public report provides only four-concept anonymized averages. A future public release (e.g., DOE report database) is possible; search OSTI for Woodruff/Zap/ALPHA updates.
 
-6. **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/`) — applicable as the CAS framework reference for structuring any cost estimate. Should be used to structure LCOE placeholder table with clearly flagged unknowns.
+5. **ITER/DEMO LiPb blanket engineering literature** — `not-yet-sourced`. Published LiPb loop cost scaling models from ITER and DEMO studies could provide analogous cost for LiPb heat transfer system (CAS 22.2 / 27). Search OSTI for "LiPb blanket cost" or "lithium lead tritium extraction cost."
 
-7. **Pulsed power capacitor cost literature** — `not-yet-sourced` — Search IEEE Transactions on Plasma Science or PPPS conference proceedings for $/J or $/kJ capacitor cost data, enabling rough pulsed power bank capital cost estimate. Hegeler et al. (IEEE Trans. Dielectr. Electr. Insul., 2011 — Ref. 20 in Engineering Paradigms paper) may contain cost-relevant efficiency data.
+6. **Zap Energy DOE Milestone-Based Fusion Development Program milestone reports** — `not-yet-sourced`. DOE FES Milestone reports may contain performance data and cost projections. Search DOE FES website and OSTI for Zap Energy milestone program deliverables (`unverified — confirm existence before searching`).
 
 ---
 
 ## Summary
 
-**Proceed to full analysis.** The concept description, physics basis, and engineering design rationale are well enough documented for a D1+ qualitative analysis covering system function, subsystem maturity, and supply chain challenges. The Engineering Paradigms paper (Thompson et al., FST 2023) is an unusually comprehensive source for a private company at this stage. The OSTI pulsed power roadmap document provides strong coverage of the sector's critical supply chain gap (capacitor lifetime and manufacturing scale-up).
-
-The LCOE section will require explicit analog-based estimation with acknowledged uncertainty. The most important pre-analysis step is checking whether the ARPA-E ALPHA 2017 revisit covers the UW SFS Z-pinch concept, as that would be the only CAS-level cost reference in the repo applicable to this concept.
-
-The commercially critical finding to highlight: at 10 Hz operation, current-generation capacitors would require replacement after ~1 day of operation — this gap (10⁴–10⁵ shot lifetime vs. 10⁹+ needed) is the dominant O&M risk and may be the single largest economic uncertainty in the entire concept.
+The SFS Z-pinch is **ready for a D1+ qualitative analysis** and a **partial quantitative analysis**. The engineering concept is exceptionally well-articulated for its development stage — Thompson FST 2023 provides the most detailed public plant design of any pre-commercial alt-fusion concept in this project. The ARPA-E ALPHA study provides a CAS-structured LCOE estimate (~$43/MWh) directly applicable as a benchmark for the concept, though Zap-specific cost line items are proprietary. The main qualitative caveat — which should be prominently flagged in the analysis — is that demonstrated physics performance (1.6 GPa, ~1 keV) remains far from plant conditions (35 keV, Q > 10), making any cost model highly sensitive to whether sheared-flow stabilization holds at MA-scale currents. The pulsed power supply chain (capacitor lifetime, solid-state switch availability) is a genuinely blocking commercialization constraint identified by the 2025 OSTI roadmap. Proceed to full analysis with explicit uncertainty framing on: (1) physics extrapolation from current experiments to breakeven, (2) pulsed power driver cost (widest CAS variance in the ALPHA study), and (3) recirculating power fraction.
 
 ---
 
@@ -186,13 +168,13 @@
 
 ```yaml
 overall_rating: "Mostly Ready"
-blocking_count: 6
-important_count: 9
-counting_method: "section_5_missing_parameters_blocking_count_plus_section_1_economic_analysis_gap; important from sections 2-4 plus section 5 important row count; deduplicated across sections"
+blocking_count: 4
+important_count: 6
+counting_method: "section_5_missing_parameters_plus_sections_3_4_deduplicated: physics_gap_to_plant_conditions, net_electric_efficiency, pulsed_power_driver_cost (all blocking); capacitor_lifetime and solid_state_switch_availability collapsed into single supply_chain blocking gap from sections 3+4"
 section_coverage:
-  availability_of_data:       "Partial"
-  system_function:            "Good"
+  availability_of_data:       "Good"
+  system_function:            "Partial"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Partial"
-  lcoe_parameter_extraction:  "Poor"
+  lcoe_parameter_extraction:  "Partial"
 ```
\ No newline at end of file
```
