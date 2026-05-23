# Diff: 04-laser-icf

**Generated:** 2026-05-22T09:34:19-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 4 | 7 | 3 |
| important_count  | 7 | 8 | - |
| overall_rating   | Significant Gaps | Significant Gaps | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
151:1. **Hawker (fleet-wide) IFE simplified economic model** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — directly applicable as structural analog. The 14-parameter model covers gain, efficiency, rep rate, and driver cost sensitivity in a technology-agnostic IFE framework. Use this to build the parameterized LCOE model skeleton for HB11 even where HB11-specific values are missing. `not-yet-sourced` for HB11-specific analysis.
153:2. **Xcimer Energy commercialization whitepaper** (`knowledge/sources/commercialization_of_laser_fusion_energy/`) — provides laser cost breakdown by component for KrF excimer architecture (<$100/J). Serves as laser cost lower bound; HB11's DPSSL will be more expensive per joule but less power is needed per shot (30 kJ vs. MJ-class). Use as analog with noted differences. `not-yet-sourced` relative to HB11 analysis.
155:3. **ARIES cost accounts** (`knowledge/sources/aries_cost_account_documentation/`) — provides CAS framework (accounts 20–27) that can structure the capital cost estimate even without HB11-specific values. Use for BoP, direct costs, indirect cost conventions.
```

## Blocking-tier lines (baseline)

```
35:- Phys. Rev. Research (2025) and Mehlhorn (2024) not extracted — `not-yet-sourced` — **blocking** (these are the most recent quantitative physics results; needed for current experimental state section)
60:- Laser wall-plug efficiency: current petawatt systems ~0.1–1%; target is >10% — `not-yet-sourced` (Adelaide USPL group may publish) — **blocking** (recirculating power fraction is the dominant LCOE driver)
61:- Avalanche enhancement mechanism: theoretical basis not validated — `truly-unknown` (controversial in literature) — **blocking** (gain of >500 relies on this; without it, concept is not viable)
84:- 1 Hz petawatt laser TRL: ~2–3 at best (Adelaide project is a goal, not a result) — `not-yet-sourced` (check laser physics literature for rep-rate petawatt progress) — **blocking** (no 1 Hz petawatt exists; this is a fundamental enabling technology gap)
85:- Combined kT field + fast ignition demonstration: not yet performed — `truly-unknown` (no experiment has combined both elements) — **blocking**
139:| Laser system capital cost (array of thousands) | truly-unknown | blocking | No cost model for commercial petawatt array at this scale; NIF-analogues would drastically overestimate |
140:| Wall-plug efficiency (achieved, not target) | truly-unknown | blocking | Current petawatt systems ~0.1–1%; >10% is a research goal. Dominates recirculating power fraction |
141:| Target cost per shot at 1 Hz | truly-unknown | blocking | No manufacturing cost data; ICF DT target analogues exist but p-B11 pellet specs differ |
149:| Published system code / plant study | truly-unknown | blocking | Does not exist publicly |
```

## Blocking-tier lines (new)

```
31:- No plant study of any form — `truly-unknown` — **blocking** (no cost structure baseline)
32:- Company holds internal techno-economic model (`link-10-1007...` references it exists) but details are unpublished — `proprietary` — **blocking** for subsystem-level cost
54:- Fundamental fusion gain not yet demonstrated at any scale — `truly-unknown` — **blocking** (the entire LCOE depends on achievable G, which is undemonstrated and 4 orders of magnitude from needed range)
55:- Energy conversion architecture not finalized — `proprietary` / `truly-unknown` — **blocking** (efficiency ε swings from ~40% steam to ~50–64% advanced; choice determines recirculating power fraction)
57:- Laser architecture at 1 Hz, 30 kJ, >10% WP efficiency is beyond current capability — `truly-unknown` — **blocking** (no laser system in existence meets all three requirements simultaneously)
81:- No subsystem has been demonstrated at power-plant-relevant parameters — `truly-unknown` — **blocking** for TRL completeness
136:| Capital cost by subsystem (CAS20–27) | truly-unknown | blocking | No plant study; no analogous p-B11 design published anywhere |
137:| Total laser system installed cost | truly-unknown / proprietary | blocking | Adelaide grant hints at laser cost work; not published |
138:| Laser cost per joule (for hybrid burn DPSSL) | not-yet-sourced | blocking | Xcimer has KrF data at <$100/J; DPSSL baseline from NIF era is $700–1000/J — but HB11 targets "commercial lasers" at unknown cost |
141:| Capacity factor / availability | truly-unknown | blocking | No maintenance schedule, no downtime analysis; target "baseload" but no quantification |
142:| Fusion power per shot (Joules) | truly-unknown | blocking | Depends on G (undemonstrated); can only parameterize |
144:| Target fabrication cost at scale | derivable/proprietary | blocking | "Few dollars/target" mentioned but not derived; 1 Hz × 500 MW implies ~$600M/yr at $1/target — very sensitive |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/04-laser-icf.md	2026-05-22 09:21:13.834292550 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/04-laser-icf/gap_report.md	2026-05-22 09:34:19.974594399 -0700
@@ -1,13 +1,10 @@
-Now I have everything I need. Let me write the assessment.
+I have enough information to write the full gap assessment now.
 
----
-
-# Gap Assessment: Laser ICF - p-B11 Fast Ignition
+# Gap Assessment: Laser ICF (p-B11)
 
 ## Overall Readiness
 **Rating**: Significant Gaps
-
-**Summary**: HB11 Energy is an extremely early-stage startup (~TRL 2-3 overall) with a small public literature footprint, no published plant study, and no techno-economic analysis in the captured sources. Enough material exists for a qualitative write-up covering physics rationale, technology risks, and subsystem maturity — but quantitative LCOE modeling requires heavy use of analogues and first-principles estimates, with wide uncertainty bands. Two key papers (Phys. Rev. Research 2025, Mehlhorn 2024) remain unextracted and should be retrieved before analysis begins.
+**Summary**: HB11 Energy is 4 orders of magnitude from breakeven and has not yet published a plant study, CAS-level cost breakdown, or any peer-reviewed LCOE analysis. The one quantitative TEA source (McKenzie et al., J. Fusion Energy 2023) provides a useful power-balance framework with several key parameters but contains no subsystem cost estimates or capital cost structure. A qualitative analysis is feasible with honest uncertainty framing; a quantitative LCOE model is possible only in a parameterized "what would need to be true" mode using IFE analogs from the fleet-wide source pool, with wide confidence intervals throughout.
 
 ---
 
@@ -17,24 +14,23 @@
 **Coverage**: Poor
 
 **Available**:
-- Company website (2025) — high-level reactor description, fuel, rep rate, power target, steam cycle claim (`hb11-technology-page-2025.md`)
-- Patent US10410752B2 (2018) — reactor geometry, laser specs, performance targets, original direct conversion design (`hb11-patent-reactor-design.md`)
-- Osaka LFEX experiment (Applied Sciences 2022) — alpha yield at 10^10/sr, confirms in-target geometry advantage (`hb11-osaka-experiment-2022.md`)
-- Company overview — funding (~A$12.8M total), team, commercial model, partnerships (`hb11-company-overview.md`)
-- Recent developments (2024–2025) — TINEX, Adelaide laser partnership (targeting >10% wall-plug), DOE INFUSE, Optica OPN profile (`hb11-recent-developments-2024-2025.md`)
-- New Atlas 2020 article — early direct conversion design (superseded) (`hb11-newatlas-article.md`)
+- One semi-quantitative TEA review paper: McKenzie et al. (J. Fusion Energy, 2023) — power loop model, recirculating power fraction formula, economic targets, key parameter ranges (`iter-03/sources/link-10-1007-s10894-023-00349-9.md`)
+- Conceptual reactor patent US10410752B2 (2018): fuel geometry, two-laser architecture, 1 Hz rep rate, 1 GW target, early direct-conversion design (`iter-01/sources/hb11-patent-reactor-design.md`)
+- Peer-reviewed physics paper: Margarone et al. (Appl. Sci. 2022) — 10^10 α/sr Osaka LFEX demonstration (`iter-01/sources/hb11-osaka-experiment-2022.md`)
+- Company technology pages (2019–2025): high-level reactor concept, energy conversion pivot, laser architecture vision (`iter-01/sources/hb11-technology-page.md`, `iter-02/sources/hb11-technology-page-2025.md`, `iter-03/sources/hb11-our-technology.md`)
+- News and PR compilations: funding, milestones, TINEX membership, ELI ERIC partnership (`iter-02/sources/hb11-recent-developments-2024-2025.md`, multiple iter-03 sources)
 
 **Missing**:
-- Published plant/system study (none exists publicly)
-- Detailed techno-economic analysis
-- Phys. Rev. Research (2025) — "Alpha particle production from Novel Targets" — not extracted (PDF binary)
-- Mehlhorn (2024) Physics of Plasmas perspective — not extracted (PDF binary)
-- Hora et al. theoretical papers underlying the "avalanche" p-B11 enhancement mechanism
+- No plant study or system code output (HYLIFE-II, SOMBRERO, etc.)
+- No CAS-level capital cost breakdown
+- No published LCOE sensitivity analysis
+- Phys. Rev. Research 2025 paper on novel targets not extracted (`dossier.md` notes as "not extracted")
+- Mehlhorn (2024, Physics of Plasmas) — historical/personal perspective, not extracted
 
 **Gaps**:
-- Phys. Rev. Research (2025) and Mehlhorn (2024) not extracted — `not-yet-sourced` — **blocking** (these are the most recent quantitative physics results; needed for current experimental state section)
-- No published plant study or system code — `truly-unknown` (does not exist publicly) — **important** (limits quantitative analysis to first-principles estimation)
-- No peer-reviewed techno-economic analysis of this concept — `truly-unknown` — **important**
+- No plant study of any form — `truly-unknown` — **blocking** (no cost structure baseline)
+- Company holds internal techno-economic model (`link-10-1007...` references it exists) but details are unpublished — `proprietary` — **blocking** for subsystem-level cost
+- Phys. Rev. Research (2025) content unavailable — `not-yet-sourced` — **important** (most recent experimental physics data)
 
 ---
 
@@ -42,24 +38,23 @@
 **Coverage**: Partial
 
 **Available**:
-- Core physics mechanism described (two-laser scheme, kT field, proton fast ignition) with enough detail to identify modeling challenges
-- Energy conversion pivot (direct → steam) documented, rationale unclear
-- Performance gap documented: ~4 orders of magnitude from net energy gain
-- "Thousands of commercial lasers" architecture stated but not detailed
-- Adelaide partnership targets >10% wall-plug laser efficiency (currently undemonstrated)
+- Physics deficit quantified: 4 orders of magnitude from breakeven in terms of α-particle yield per kJ (`iter-03/sources/link-10-1007-s10894-023-00349-9.md`)
+- Required gain target stated: G = 100–300 at laser efficiency η = 20% for economic viability (`link-10-1007...`)
+- Power amplifier model described: f = 1/(εηG), with engineering breakeven at f = 1 and commercial target f ≤ 0.25 (`link-10-1007...`)
+- Known physics uncertainties catalogued: p-B11 cross-section at low energies poorly measured, avalanche mechanism debated, bremsstrahlung loss severity, degenerate plasma behavior (`link-10-1007...`)
+- Energy conversion pivot documented: patent (2018) described direct electrostatic conversion at −1.4 MV; 2025 website states conventional steam cycle — design not stabilized (`dossier.md`, `iter-02/sources/hb11-technology-page-2025.md`)
 
 **Missing**:
-- Technical rationale for the direct→steam conversion pivot (no paper or technical note)
-- Detailed recirculating power fraction (laser wall-plug efficiency is the dominant system-function uncertainty)
-- Status of the "avalanche" mechanism: Hora's non-linear resonance enhancement is theoretically controversial — no experimental confirmation in sources
-- Integration challenge between kT field generation and fast ignition timing (not discussed)
-- Target injection system design at 1 Hz (not described beyond "pellet injection ~1/second")
+- No simulations or code outputs for hybrid burn target gain projections
+- No analysis of how "thousands of commercial lasers" at 1 Hz aggregate to 1 GW baseload
+- No chamber design or debris management analysis (TINEX addresses this generically for IFE)
+- No quantified driver efficiency roadmap (20% WP efficiency is a target, not demonstrated)
 
 **Gaps**:
-- No technical explanation for energy conversion pivot — `proprietary` (likely internal engineering decision) — **important** (changes the energy conversion efficiency and cost structure significantly)
-- Laser wall-plug efficiency: current petawatt systems ~0.1–1%; target is >10% — `not-yet-sourced` (Adelaide USPL group may publish) — **blocking** (recirculating power fraction is the dominant LCOE driver)
-- Avalanche enhancement mechanism: theoretical basis not validated — `truly-unknown` (controversial in literature) — **blocking** (gain of >500 relies on this; without it, concept is not viable)
-- Target injection/positioning at 1 Hz: no design published — `proprietary` — **important**
+- Fundamental fusion gain not yet demonstrated at any scale — `truly-unknown` — **blocking** (the entire LCOE depends on achievable G, which is undemonstrated and 4 orders of magnitude from needed range)
+- Energy conversion architecture not finalized — `proprietary` / `truly-unknown` — **blocking** (efficiency ε swings from ~40% steam to ~50–64% advanced; choice determines recirculating power fraction)
+- Avalanche mechanism magnitude is physically contested — `truly-unknown` — **important** (if avalanche is significant it enables lower gain requirements; if absent, gain requirements are much more severe)
+- Laser architecture at 1 Hz, 30 kJ, >10% WP efficiency is beyond current capability — `truly-unknown` — **blocking** (no laser system in existence meets all three requirements simultaneously)
 
 ---
 
@@ -67,48 +62,49 @@
 **Coverage**: Partial
 
 **Available**:
-- Fusion physics: ~10^10 alpha/sr at LFEX (2022), TARANIS, PALS experiments documented — establishes TRL 2–3 for core reaction
-- Petawatt ps laser: commercially available technology (CPA, TRL 6+), but not at 1 Hz rep rate
-- Kilotesla field generation: demonstrated in laser labs (patent basis, cited in company materials)
-- Steam cycle: TRL 9 (conventional technology)
-- Company explicitly describes "components first" commercialization — implies recognition that integrated system is far from demonstration
+- Fusion physics demonstrations: 12 experiments at LFEX (Osaka), TARANIS (Belfast), PALS (Prague) — all TRL 2–3 (`dossier.md`, `iter-01/sources/hb11-osaka-experiment-2022.md`)
+- Petawatt CPA laser technology: commercially available at single-shot scale (Nobel 2018), TRL 5–6 for the laser itself; not demonstrated at fusion-relevant rep rates or wall-plug efficiency
+- Capacitor-coil kT field generation: demonstrated in laboratory settings (`link-10-1007...`), TRL ~3–4
+- Boron-nitride targets: manufactured and tested, TRL 4–5 for current experimental targets
+- Novel target materials (borophene, "white graphene"): in early development, TRL 1–2 (`link-10-1007...`)
+- DOE INFUSE grant (LLE/Rochester collaboration) ongoing for H2-boron fuel target development
+- TINEX membership: participating in DOE-funded target injection/chamber engineering program (`iter-03/sources/globenewswire-news-release-2025-02-10-3023820-0-en-general.md`)
 
 **Missing**:
-- TRL of 1 Hz repetition rate petawatt laser (specifically: thermal management, component lifetime at rep rate)
-- TRL of kT field generation + fast ignition integrated demonstration (no combined experiment documented)
-- TRL of p-B11 pellet fabrication at commercial scale
-- Lifetime/replacement schedule for any reactor component
-- Target injection system TRL
+- No TRL assessment document
+- No laser system rep-rate demonstration at fusion-relevant parameters
+- No chamber design for alpha particle collection/energy conversion
+- No target injection system at 1 Hz demonstrated
+- No first wall or chamber material study for alpha bombardment damage
 
 **Gaps**:
-- 1 Hz petawatt laser TRL: ~2–3 at best (Adelaide project is a goal, not a result) — `not-yet-sourced` (check laser physics literature for rep-rate petawatt progress) — **blocking** (no 1 Hz petawatt exists; this is a fundamental enabling technology gap)
-- Combined kT field + fast ignition demonstration: not yet performed — `truly-unknown` (no experiment has combined both elements) — **blocking**
-- Pellet fabrication at 1 Hz, commercial scale: no data — `truly-unknown` — **important**
-- Lifetime data for any reactor component: none — `truly-unknown` — **nice-to-have** at this stage
+- No subsystem has been demonstrated at power-plant-relevant parameters — `truly-unknown` — **blocking** for TRL completeness
+- High-rep-rate DPSSL at >10% WP efficiency — `truly-unknown` — **important** (Adelaide A$8.2M grant is working on this but results unpublished)
+- Alpha energy collection system (DEC or MHD or steam) — `truly-unknown` at engineering level — **important**
+- Target fabrication at hundreds of millions shots per year scale — `truly-unknown` — **important**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Partial (inferable, not explicitly analyzed in sources)
+**Coverage**: Partial
 
 **Available**:
-- Fuel: p-B11 — natural boron is 80.1% B-11; no enrichment required for basic use (though enriched B-11 targets likely preferred for performance)
-- No tritium required — eliminates breeding blanket, Li-6, and tritium handling (significant advantage)
-- Minimal neutron shielding needed (aneutronic) — reduces activation, simplifies maintenance
-- Laser system uses "thousands of commercial lasers" — implies supply chain scalability by design
-- Nickel plates for capacitor-coil targets: commodity material
+- Boron-11 fuel: natural abundance ~80%, no enrichment required, ~10^9 ton confirmed global reserves — explicitly analyzed in `link-10-1007...` TEA paper as adequate for global deployment
+- No tritium required → eliminates entire tritium breeding/handling supply chain
+- No superconducting magnets required
+- Laser diode replacement identified as key cost driver: $1/W cost, 2.2 billion shot lifetime assumed (`link-10-1007...`)
+- High-power laser diodes: industrial supply chain exists for telecom/materials processing; fusion-scale manufacturing would require scale-up
 
 **Missing**:
-- No supply chain analysis in any source
-- CPA grating supply chain at scale: large-area diffraction gratings are a manufacturing bottleneck for petawatt lasers
-- Rare-earth gain media (e.g., Nd:glass, Ti:sapphire) at "thousands of units" scale
-- Boron enrichment supply chain (if enriched B-11 pellets are needed)
-- Target fabrication infrastructure (precision pellet manufacturing at 1 Hz)
+- No analysis of laser glass or optical component supply chain (if DPSSL)
+- No materials study for chamber wall alpha irradiation damage and replacement rate
+- No analysis of target substrate materials (borophene, white graphene) supply and manufacturing
+- No cost breakdown for laser diode supply at scale (total diode count for 500 MW plant)
 
 **Gaps**:
-- CPA grating and laser gain media at thousands-of-units scale: `not-yet-sourced` — **important** (search: high-power laser manufacturing supply chain literature, DARPA/DOD laser programs)
-- Enriched B-11 target supply: `not-yet-sourced` — **important** (search: boron isotope separation literature)
-- No materials or supply chain section exists in any source — all of the above requires inference and external research — `not-yet-sourced` — **important** overall
+- Laser diode supply chain at fusion scale (gigawatts of installed diode capacity) — `not-yet-sourced` — **important** (search: fusion laser diode manufacturing scale-up, DPSSL diode cost trends)
+- Novel target material supply chain (borophene is not commercially produced) — `truly-unknown` for commercial scale — **important** (would block hybrid burn approach)
+- Chamber wall materials for alpha irradiation — `not-yet-sourced` — **nice-to-have** at this stage given pre-net-gain status
 
 ---
 
@@ -116,77 +112,77 @@
 **Coverage**: Poor
 
 **Available Parameters**:
-
 | Parameter | Value/Range | Source | Confidence |
-|-----------|-------------|--------|------------|
-| Target plant power output | 1 GW baseload | Company website (hb11-technology-page-2025.md) | low — conceptual only |
-| Repetition rate | ~1 Hz | Patent + company website | medium — design intent, undemonstrated |
-| Energy per reaction (patent basis) | ~1 GJ (~280 kWh) | Patent US10410752B2 | low — based on gain >500, which is undemonstrated |
-| Laser input energy (ignition pulse) | ~30 kJ (patent) | Patent US10410752B2 | low — patent-era spec, may have evolved |
-| Laser input energy (field pulse) | >100 J (ns) | Patent US10410752B2 | low |
-| Fuel type | p-B11 (no tritium) | All sources | high |
-| Energy conversion | Steam cycle (conventional) | Company website 2025 | medium — no efficiency spec given |
-| Wall-plug laser efficiency target | >10% | Adelaide partnership 2025 | low — goal, not demonstrated |
-| Recirculating power | "A portion" recycled | Company website | very low — no fraction given |
-| Gain (Q) target | >500 (patent) | Patent US10410752B2 | very low — ~4 orders of magnitude from demonstrated |
-| Current alpha yield | ~10^10 /sr | Osaka 2022 experiment | high — experimental result |
-| Fuel cost analogue | Negligible (B-11 abundant) | Inferred | medium |
+|---|---|---|---|
+| Recirculating power fraction formula | f = 1/(εηG) | `link-10-1007...` McKenzie 2023 | h |
+| Target gain required (economic) | G = 100–300 | `link-10-1007...` | m |
+| Laser wall-plug efficiency target | η = 20% (DPSSL) | `link-10-1007...` | m (undemonstrated) |
+| Thermal conversion efficiency (steam) | ε = 36–40% | `link-10-1007...` | m |
+| Advanced conversion efficiency (DEC) | ε = 45–64% | `link-10-1007...` | l (theoretical) |
+| Commercial LCOE target | ≤ $35/MWh | `link-10-1007...` | h (constraint) |
+| Diode replacement cost | $1/W | `link-10-1007...` | l (assumed) |
+| Diode shot lifetime | 2.2 × 10^9 shots | `link-10-1007...` | l (assumed) |
+| Target cost (hybrid burn, G=200) | ~few $/target (acceptable) | `link-10-1007...` | l (estimated) |
+| Rep rate | ~1 Hz | `dossier.md`, patent | h |
+| Plant output target | ~500 MWe | `link-10-1007...` | m |
+| Reactor lifetime | 25 years | `link-10-1007...` | l (assumed) |
+| Pellet geometry | 1 cm × 0.2 mm HB11 cylinder | patent | m |
+| Boron fuel cost | Negligible (abundant) | `link-10-1007...` | h |
+| Current physics gain | ~10^−4 (4 OOM from breakeven) | `iter-01/sources/hb11-osaka-experiment-2022.md` | h |
 
 **Missing Parameters**:
-
 | Parameter | Gap Type | Criticality | Notes |
-|-----------|----------|-------------|-------|
-| Laser system capital cost (array of thousands) | truly-unknown | blocking | No cost model for commercial petawatt array at this scale; NIF-analogues would drastically overestimate |
-| Wall-plug efficiency (achieved, not target) | truly-unknown | blocking | Current petawatt systems ~0.1–1%; >10% is a research goal. Dominates recirculating power fraction |
-| Target cost per shot at 1 Hz | truly-unknown | blocking | No manufacturing cost data; ICF DT target analogues exist but p-B11 pellet specs differ |
-| Steam cycle thermal efficiency | derivable | important | Can use conventional steam cycle values (33–40%) but no p-B11→thermal coupling design published |
-| Reactor vessel capital cost | truly-unknown | important | Patent gives geometry (1m sphere, SS), but no cost estimate |
-| Capacity factor / availability | truly-unknown | important | No maintenance schedule, no component lifetime data |
-| Balance of plant cost | derivable | important | Can use generic 1 GW steam plant analogues |
-| Target injection system cost | truly-unknown | important | No design beyond "pellet injection ~1/second" |
-| O&M cost structure | truly-unknown | important | No staffing, maintenance, or replacement schedule data |
-| Net electrical output (after recirculation) | derivable | important | Requires laser wall-plug efficiency — currently unknown |
-| Published system code / plant study | truly-unknown | blocking | Does not exist publicly |
+|---|---|---|---|
+| Capital cost by subsystem (CAS20–27) | truly-unknown | blocking | No plant study; no analogous p-B11 design published anywhere |
+| Total laser system installed cost | truly-unknown / proprietary | blocking | Adelaide grant hints at laser cost work; not published |
+| Laser cost per joule (for hybrid burn DPSSL) | not-yet-sourced | blocking | Xcimer has KrF data at <$100/J; DPSSL baseline from NIF era is $700–1000/J — but HB11 targets "commercial lasers" at unknown cost |
+| Balance of plant cost | derivable | important | Can use fleet-wide analogs (TEA D-T MFE, ARIES) — IFE BoP structurally similar |
+| O&M costs (beyond diode replacement) | derivable | important | Can estimate from fission/IFE analogs; no HB11-specific data |
+| Capacity factor / availability | truly-unknown | blocking | No maintenance schedule, no downtime analysis; target "baseload" but no quantification |
+| Fusion power per shot (Joules) | truly-unknown | blocking | Depends on G (undemonstrated); can only parameterize |
+| Chamber/first wall cost and replacement | truly-unknown | important | Alpha bombardment damage rate unknown; no materials data |
+| Target fabrication cost at scale | derivable/proprietary | blocking | "Few dollars/target" mentioned but not derived; 1 Hz × 500 MW implies ~$600M/yr at $1/target — very sensitive |
+| Actual laser energy on target required | truly-unknown | important | 30 kJ mentioned in patent but "hybrid burn" parameters unspecified |
 
 ---
 
 ## Source Recommendations
 
-1. **Extract Phys. Rev. Research (2025)** — DOI: PhysRevResearch.7.013230. Alpha particle production from novel targets. This is the most recent quantitative experimental result and likely contains updated yield data and target geometry details. PDF URL noted in dossier. — `not-yet-sourced`
+1. **Hawker (fleet-wide) IFE simplified economic model** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — directly applicable as structural analog. The 14-parameter model covers gain, efficiency, rep rate, and driver cost sensitivity in a technology-agnostic IFE framework. Use this to build the parameterized LCOE model skeleton for HB11 even where HB11-specific values are missing. `not-yet-sourced` for HB11-specific analysis.
+
+2. **Xcimer Energy commercialization whitepaper** (`knowledge/sources/commercialization_of_laser_fusion_energy/`) — provides laser cost breakdown by component for KrF excimer architecture (<$100/J). Serves as laser cost lower bound; HB11's DPSSL will be more expensive per joule but less power is needed per shot (30 kJ vs. MJ-class). Use as analog with noted differences. `not-yet-sourced` relative to HB11 analysis.
 
-2. **Extract Mehlhorn (2024) Physics of Plasmas perspective** — DOI: 10.1063/5.0170661. "From KMS Fusion to HB11 Energy, a personal 50 year IFE perspective." As a 50-year IFE retrospective by HB11's lead theoretician, this may contain the most substantive technical and programmatic assessment available publicly. High priority. — `not-yet-sourced`
+3. **ARIES cost accounts** (`knowledge/sources/aries_cost_account_documentation/`) — provides CAS framework (accounts 20–27) that can structure the capital cost estimate even without HB11-specific values. Use for BoP, direct costs, indirect cost conventions.
 
-3. **Search for Hora et al. p-B11 theoretical papers** — Heinrich Hora's nonlinear resonance / "avalanche" enhancement mechanism is the theoretical basis for HB11's gain claims. Understanding whether this has independent experimental support is essential for assessing the credibility of Q>500. Search: "Hora hydrogen boron fusion avalanche" on OSTI, arXiv, or Google Scholar. — `not-yet-sourced`, `unverified — confirm existence before searching`
+4. **Mehlhorn (2024), Physics of Plasmas** — "From KMS Fusion to HB11 Energy, a personal 50-year IFE perspective" — listed in dossier but not extracted. May contain the most detailed techno-economic discussion from HB11's own team. Flag: `not-yet-sourced` — **search OSTI/DOI 10.1063/5.0170661 and extract**. High priority.
 
-4. **Search for rep-rate petawatt laser literature** — The 1 Hz petawatt requirement is the key enabling technology. Search: "repetition rate petawatt laser wall-plug efficiency" on OSTI or in proceedings from CLEO/SPIE. The ELI-NP and ELI-Beamlines facilities have published on rep-rate petawatt development. — `not-yet-sourced`, `unverified — confirm existence before searching`
+5. **Phys. Rev. Research (2025), PhysRevResearch.7.013230** — "Alpha particle production, novel targets, laser-driven PB fusion" — listed in dossier but not extracted. Contains most recent experimental physics data needed to update the current-state-of-the-art section. `not-yet-sourced` — extract from open-access source.
 
-5. **Search for IFE target fabrication cost literature** — General Atomics, NRL, and LLNL have published target fabrication cost analyses for DT ICF targets. These are not direct analogues but provide a costing framework adaptable to p-B11 pellets. Search: "ICF target fabrication cost mass production" on OSTI. — `not-yet-sourced`, `unverified — confirm existence before searching`
+6. **DOE INFUSE/FIRE target design publications from LLE collaboration** — HB11's DOE INFUSE project with LLE/Rochester on H2-boron fuel targets may have produced technical reports or preprints. `not-yet-sourced` — search arXiv and OSTI for "proton boron fuel target" + Sefkow/Mehlhorn. `unverified — confirm existence before searching`.
 
-6. **Search for direct energy conversion from charged particles literature** — Even though HB11 has pivoted to steam, the original direct conversion approach may be more physically motivated for an aneutronic fuel. Papers on inertial electrostatic conversion or alpha particle direct conversion would enable a comparison. Search: "direct energy conversion alpha particles inertial fusion" — `not-yet-sourced`, `unverified — confirm existence before searching`
+7. **Hora et al. (Optical Engineering, 2021)** — "Green energy generation via optical laser pressure initiated nonthermal nuclear fusion" — cited in the J. Fusion Energy paper, likely contains reactor model details from the theoretical side. `not-yet-sourced` — DOI: 10.1117/1.OE.61.2.021004. `unverified — confirm existence before searching`.
 
 ---
 
 ## Summary
 
-**Proceed to qualitative analysis now; defer quantitative model pending source extraction.**
+Proceed to full qualitative analysis with explicit caveats. The McKenzie/Batani (2023) J. Fusion Energy paper, the patent, and the Osaka experiment paper together provide enough material for a D1-level write-up covering system function, subsystem maturity, and supply chain. The materials and supply chain section benefits strongly from the aneutronic advantage (no tritium, no HTS magnets) which is well-documented.
 
-The available sources support a solid **qualitative write-up** covering HB11's physics approach, the extraordinary technology gap (~4 orders of magnitude from net gain), the pivot from direct to steam conversion, subsystem maturity assessments, and the dominant risk profile (laser wall-plug efficiency and Q validation). The aneutronic fuel cycle is a genuine structural advantage worth highlighting, as it eliminates tritium breeding costs entirely.
+For the quantitative LCOE model: build a parameterized IFE power-balance model using the Hawker 14-parameter framework from the fleet-wide sources, populated where possible with HB11-specific values from `link-10-1007...` (η=20%, G=100–300, ε=36–40%). The model is necessarily a "what would need to be true" tool with gain G as the dominant free variable. Capital cost structure should borrow from Xcimer (laser cost $/J) and ARIES (BoP) with clear analog notes. Two missing sources should be extracted before finalizing: Mehlhorn (2024) and PhysRevResearch (2025).
 
-The **quantitative LCOE model** faces two blocking unknowns that cannot be responsibly estimated without external analogues: (1) laser system capital cost at "thousands of commercial petawatt units" scale — no precedent exists, and (2) laser wall-plug efficiency — the difference between 1% and 10% changes recirculating power from ~3× to ~0.3× net output, a factor of 10 in effective plant capacity. Both of these must be treated as wide parametric sweeps rather than point estimates.
-
-Before running the quantitative model, extract the two unextracted papers (Phys. Rev. Research 2025 and Mehlhorn 2024 Physics of Plasmas) — the Mehlhorn perspective in particular may contain the only publicly available integrated technical assessment of this concept's feasibility and cost challenges. Without these, the model will rest almost entirely on the 2018 patent and company website claims, both of which are conceptual-stage documents with significant internal contradictions (energy conversion design pivot).
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Significant Gaps"
-blocking_count: 4
-important_count: 7
-counting_method: "section_5_missing_parameters"
+blocking_count: 7
+important_count: 8
+counting_method: "deduplicated across all sections — blocking gaps are those where no analog or derivation path exists and which prevent any credible value from being assigned to a model parameter; important gaps are those where analog-based estimates are possible but carry major uncertainty"
 section_coverage:
   availability_of_data:       "Poor"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
-  materials_supply_chain:     "Partial (inferable, not explicitly analyzed in sources)"
+  materials_supply_chain:     "Partial"
   lcoe_parameter_extraction:  "Poor"
-```
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
