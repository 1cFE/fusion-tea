# Phase 3 diff: 18-p-b11-frc

**Generated:** 2026-05-22T14:40:07-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 5 | 5 | 0 |
| important_count  | 6 | 6 | - |
| overall_rating   | Significant Gaps | Significant Gaps | - |

## Fleet-source dispositions in new report

```
```

## Forbidden-phrase check (should be empty)

```
1:I now have sufficient information from all sources to write the gap assessment report.
```

## First line of new report (should start with `# Gap Assessment`)

```
I now have sufficient information from all sources to write the gap assessment report.
```

## Blocking-tier lines (new)

```
27:- Plant study or pre-conceptual design for Da Vinci — `proprietary` — **blocking**: no quantitative capital cost structure exists anywhere in the public domain
28:- Published Q-factor projections or energy balance for reactor-scale p-B11 FRC — `truly-unknown`: no validated reactor design exists — **blocking**
46:- NBI recirculating power fraction at reactor-scale Q — `truly-unknown` — **blocking**: all LCOE models are unconstrained without this; Mulder et al. framework exists but requires Q and NBI efficiency inputs that are not published
47:- Bremsstrahlung power fraction and wall loading at 250 keV operational temperature — `truly-unknown` — **blocking**: determines whether thermal extraction is viable and what wall lifetime is
48:- FRC confinement scaling law validation from ~10 keV (C-2W) to ~250 keV (Da Vinci target) — `truly-unknown` — **blocking**: the energy scaling law cited in C-2W papers has not been extrapolated to p-B11 reactor conditions in any public source
69:- FRC tilt-mode and stability control at reactor separatrix radius (~1–2 m needed for net gain vs. 0.4 m at C-2W) — `truly-unknown` — **blocking**: TAE claims kinetic stabilization by fast ions, but this mechanism weakens at larger scales; documented in `grokipedia-tae-technologies.md`
115:| Fusion gain Q at reactor conditions (p-B11, 250 keV) | truly-unknown | blocking | Central unknown; determines power balance; undemonstrated for p-B11 in any device |
116:| NBI recirculating power fraction at reactor Q | truly-unknown | blocking | NBI is entire heating system; high recirculating power at low Q makes LCOE extremely sensitive; Mulder et al. (arxiv-2103-12451) framework is applicable but requires Q input |
117:| Capital cost by CAS account for Da Vinci | proprietary / not-yet-sourced | blocking | No plant study exists; TAE claims "50% cheaper than tokamak" but no absolute figures published |
119:| NBI system capital cost at reactor scale | proprietary | blocking | NBI is the dominant power core cost; no published estimates for reactor-grade NBI systems at the required power level |
134:- **Waganer 2011 Availability Methodology** (`iter-02/sources/osti-servlets-purl-1001677.md`) — **Integrated.** Read. Provides a framework for estimating plant availability from 1st-of-kind to 10th-of-kind fusion plants. ARIES-AT achieved 87.6% for a 10th-of-kind tokamak. A 1st-of-kind p-B11 FRC plant would be significantly lower. This methodology can be used to bound capacity factor assumptions, downgrading the capacity factor gap from `blocking` → `derivable` with stated assumptions. Does not substitute for concept-specific maintenance data.
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/18-p-b11-frc.md	2026-05-22 12:59:21.073584431 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/18-p-b11-frc/gap_report.md	2026-05-22 14:40:07.338431269 -0700
@@ -1,12 +1,10 @@
-I now have enough information to write the full gap assessment.
-
----
+I now have sufficient information from all sources to write the gap assessment report.
 
 # Gap Assessment: p-B11 FRC (p-B11)
 
 ## Overall Readiness
 **Rating**: Significant Gaps
-**Summary**: The available data is unusually rich on plasma physics and machine design at the experimental scale (C-2W/Norman), with over 200 peer-reviewed publications, and the concept is well-characterized for the differentiation taxonomy. However, no published cost estimates, plant study, or techno-economic analysis exists for Da Vinci, the commercial prototype. More critically, p-B11 net energy gain has never been demonstrated—current devices operate at electron temperatures of ~1 keV versus the ~100–250 keV ion temperature required—creating a fundamental physics-to-economics uncertainty that propagates into every LCOE parameter. A qualitative analysis can be excellent; quantitative LCOE modeling requires heavily assumption-laden analogues.
+**Summary**: TAE Technologies is unusually transparent for a private fusion company, providing rich physics documentation through peer-reviewed publications, press releases, and FAQ content. However, the concept sits at a unique gap between deep experimental physics data (NBI-only FRC formation, C-2W parameters, Nature Communications 2025) and an almost complete absence of plant economics data. No published plant study, capital cost estimate, or power balance for a reactor-scale p-B11 FRC system exists. The physics basis for the key LCOE drivers — fusion gain Q at p-B11 conditions, NBI recirculating power fraction, and FRC confinement at 250 keV — remains undemonstrated and unquantified.
 
 ---
 
@@ -15,98 +13,83 @@
 ### 1. Availability of Data
 **Coverage**: Partial
 
-**Available**:
-- TAE has published 200+ peer-reviewed papers in *Nature Communications*, *Nuclear Fusion*, *Physical Review Letters*, and others (`grokipedia-tae-technologies.md`; `osti-pages-servlets-purl-2441289.md`). Physics research is unusually transparent for a private company.
-- The 2025 *Nature Communications* NBI-only FRC formation paper provides peer-reviewed confirmation of a major physics milestone (`nature-articles-s41467-025-58849-5.md`).
-- The 2024 *Nuclear Fusion* C-2W enhanced performance paper provides detailed machine parameters, subsystem descriptions, and plasma performance data (`osti-pages-servlets-purl-2441289.md`).
-- Da Vinci commercial specs (50 MWe initial, 350–500 MWe at scale, thermal steam conversion) confirmed in public announcements (`tae-djt-merger-davinci-specs.md`; `tae-energy-conversion-clarification.md`).
-- Company funding history, roadmap, and milestone structure well documented (`grokipedia-tae-technologies.md`).
-- Fuel cycle physics (p-B11, 8.7 MeV, 3α products, aneutronic) fully established and uncontroversial.
-- National lab collaborations (Argonne, PPPL, NIFS Japan) provide independent corroboration of key claims.
-
-**Missing**:
-- No published techno-economic analysis or plant study for Da Vinci or any TAE commercial concept.
-- No cost breakdown by subsystem published anywhere in the literature.
-- No independent third-party LCOE estimate.
-- Published plasma performance data for C-2W/Norman exists, but performance at Da Vinci scale (>>1 keV temperature, Q > 1) has never been demonstrated by anyone.
+**Available**: TAE is among the more transparent private fusion companies. Available data include:
+- Peer-reviewed experimental physics: Nature Communications 2025 (NBI-only FRC formation, `iter-02/sources/nature-articles-s41467-025-58849-5.md`), Nuclear Fusion 2024 (C-2W enhanced performance, `iter-02/sources/osti-pages-servlets-purl-2441289.md`), IAEA FEC 2020 (`iter-02/sources/tae-c2w-machine-details.md`)
+- Comprehensive company communications: TAE FAQ (`iter-02/sources/tae-energy-conversion-clarification.md`), NBI breakthrough press release (`iter-01/sources/tae-nbi-breakthrough-2025.md`), DJT merger announcement (`iter-02/sources/tae-djt-merger-davinci-specs.md`)
+- Corporate history and technology overview: Grokipedia compilation (`iter-01/sources/grokipedia-tae-technologies.md`)
+- Patent literature: ICC design (US7459654B2, `iter-01/sources/tae-energy-conversion-notes.md`)
+- OSTI availability methodology: Waganer 2011 (`iter-02/sources/osti-servlets-purl-1001677.md`) — applicable for estimating plant availability scaling
+- Arxiv capacity factor paper (`iter-02/sources/arxiv-2103-12451.md`) — useful framework for recirculating power analysis
+
+**Missing**: No published plant study for Da Vinci or any p-B11 FRC commercial concept. No published system code outputs. No CAS cost breakdown. All cost projections are qualitative ("50% less than tokamaks") without absolute values.
 
 **Gaps**:
-- No plant study or TEA for TAE concept — `proprietary` — **blocking**: no cost basis without this
-- No independent validation of commercial claims (50% cost reduction vs tokamak) — `proprietary` — **important**
-- Copernicus intermediate device skipped in updated plans; performance data gap between Norman and Da Vinci — `proprietary` — **important**
+- Plant study or pre-conceptual design for Da Vinci — `proprietary` — **blocking**: no quantitative capital cost structure exists anywhere in the public domain
+- Published Q-factor projections or energy balance for reactor-scale p-B11 FRC — `truly-unknown`: no validated reactor design exists — **blocking**
+- Independent techno-economic assessment of p-B11 FRC — `not-yet-sourced` — **important**: TAE's own claims are unvetted by independent cost studies
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Good (qualitatively); Poor (quantitatively)
+**Coverage**: Good
 
-**Available**:
-- p-B11 reaction requirements thoroughly documented: ~600 keV cross-section peak, 100–250 keV ion temperature needed, bremsstrahlung losses are severe at these temperatures (`grokipedia-tae-technologies.md`; patent US7459654B2).
-- NBI quadruple-duty function (formation, heating, current drive, stabilization) is well characterized; machine physics is well understood from C-2W publications.
-- FRC stability challenges (tilt mode, rotational instability, anomalous transport) documented in `grokipedia-tae-technologies.md` and the Nature Communications paper.
-- Recirculating power fraction problem identified: the 2021 arxiv paper (`arxiv-2103-12451.md`) specifically analyzes how high recirculated power + low capacity factor devastates plant efficiency—directly applicable to NBI-sustained FRC.
-- Edge biasing requirement for MHD stabilization creates additional recirculating power load (described in detail in `osti-pages-servlets-purl-2441289.md`).
-- Energy conversion path confirmed: thermal/steam for Da Vinci, with ICC as future research option.
-
-**Missing**:
-- Wall-plug efficiency of NBI at Da Vinci scale and energies (~MeV-class for p-B11 fuel) not published.
-- Q value target for Da Vinci not stated in any source.
-- Recirculating power fraction at reactor scale not calculable from available data.
-- Whether bremsstrahlung losses can actually be managed at 250 keV plasma temperature to permit net energy remains a deep open question in the physics literature—not specific to TAE.
+**Available**: Sources clearly identify the key modeling challenges:
+- p-B11 physics challenges documented in `grokipedia-tae-technologies.md` and `nature-articles-s41467-025-58849-5.md`: bremsstrahlung dominance at high temperatures, low reaction cross-section requiring ~250 keV (vs current C-2W ~10 keV), no demonstrated net gain
+- NBI quadruple-duty architecture (formation + heating + current drive + stabilization) documented in Nature Comms 2025 and `tae-c2w-machine-details.md`; the recirculating power penalty of continuous NBI is the central LCOE risk
+- FRC stability challenges at reactor scale (tilt mode, interchange, anomalous transport) documented in `grokipedia-tae-technologies.md`
+- Capacity factor / recirculating power interaction analyzed conceptually in `arxiv-2103-12451.md` (Mulder et al. 2021) — shows that high recirculating power fraction combined with low capacity factor severely degrades plant efficiency; this is directly relevant to an NBI-driven concept
+- Energy conversion ambiguity: thermal steam confirmed for Da Vinci baseline (`tae-energy-conversion-clarification.md`), but ICC direct conversion research path is unresolved
+
+**Missing**: No published power balance for a reactor-scale FRC. The wall power loading from Bremsstrahlung radiation (dominant energy channel at p-B11 temperatures) has not been quantified publicly. The transition from ~40 ms plasma pulses to steady-state reactor operation is not analyzed in any published source.
 
 **Gaps**:
-- NBI wall-plug efficiency at reactor scale (15–40 keV vs. needed MeV-class?) — `proprietary/truly-unknown` — **blocking**: determines whether net energy is even physically achievable at any Q
-- Q_plasma target for Da Vinci not published — `proprietary` — **blocking**: required for all recirculating power calculations
-- Bremsstrahlung loss balance vs. fusion power at 250 keV — `truly-unknown` (active physics research) — **blocking**: fundamental physics question, not yet answered
+- NBI recirculating power fraction at reactor-scale Q — `truly-unknown` — **blocking**: all LCOE models are unconstrained without this; Mulder et al. framework exists but requires Q and NBI efficiency inputs that are not published
+- Bremsstrahlung power fraction and wall loading at 250 keV operational temperature — `truly-unknown` — **blocking**: determines whether thermal extraction is viable and what wall lifetime is
+- FRC confinement scaling law validation from ~10 keV (C-2W) to ~250 keV (Da Vinci target) — `truly-unknown` — **blocking**: the energy scaling law cited in C-2W papers has not been extrapolated to p-B11 reactor conditions in any public source
+- Steady-state plasma lifetime vs. fueling/impurity management at reactor scale — `not-yet-sourced` — **important**: current 40 ms limit is NBI-power-supply limited, but reactor-scale sustainment physics are not published
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
-**Coverage**: Good (experimental scale); Poor (reactor scale)
+**Coverage**: Partial
 
-**Available**:
-- C-2W machine hardware comprehensively described: 8 NBI injectors (15–40 keV tunable, 13 MW), Inconel CV, resistive copper coil magnet system, divertor cryogenic pumping, Thomson scattering diagnostics (`osti-pages-servlets-purl-2441289.md`).
-- NBI system: TRL ~6-7 for current machine (13 MW demonstrated, 40 ms pulse, real-time feedback control).
-- FRC formation via NBI-only: TRL ~5-6 (demonstrated on Norman, first of its kind; `nature-articles-s41467-025-58849-5.md`).
-- Plasma confinement at 1 keV electron temperature for 40 ms: demonstrated.
-- Balance of plant (steam turbine): TRL 9 (fully mature technology, no innovation needed).
-- ICC direct energy conversion: TRL 3-4 (patents granted, concept validated theoretically, not demonstrated at scale).
-
-**Missing**:
-- Plasma confinement at reactor-relevant ion temperatures (~100–250 keV): **not demonstrated anywhere**. Current C-2W achieves ~few keV ion temperatures, approximately 2 orders of magnitude below Da Vinci target.
-- NBI system scaled to Da Vinci power levels (tens of MW at higher energies than current 15–40 keV): TRL 2-3 at required scale.
-- First wall / vacuum vessel material and lifetime at near-aneutronic neutron flux (secondary reactions): not characterized for Da Vinci.
-- Electrode biasing system at reactor scale and duration: not published.
-- Plasma Q > 1 achievement: not demonstrated for any FRC or p-B11 system.
+**Available**: TRL assessments are well-supported for current experimental systems:
+- **NBI system** (TRL 5–6): Eight injectors, 13 MW total, 15–40 keV tunable energy, demonstrated at C-2W/Norm scale; NBI-only FRC formation is a peer-reviewed breakthrough (Nature Comms 2025). Reactor-scale NBI (likely much higher power) is not designed.
+- **FRC plasma confinement** (TRL 4): Demonstrated sustained beam-driven FRC at ~10 keV total temperature, ~40 ms (beam-limited), ~13 kJ total plasma energy at C-2W scale. The ~250 keV target for p-B11 is ~25× higher than achieved and has no demonstrated path.
+- **p-B11 fusion reactions** (TRL 2–3): First measurements of p-B11 fusion in magnetically confined plasma achieved at NIFS LHD in 2023 (cited in `grokipedia-tae-technologies.md`). No Q measurement. Far below breakeven.
+- **Steam turbine / thermal conversion** (TRL 9): Fully commercial; no development risk for this subsystem.
+- **Plasma control systems** (TRL 5–6): ML-assisted feedback control demonstrated at C-2W via Google collaboration; active edge biasing and magnetic coil feedback documented.
+- **Inverse Cyclotron Converter / ICC** (TRL 2–3): Patents exist (US7459654B2), but no prototype demonstrated. Claims >90% efficiency, but this is theoretical.
+- **Da Vinci reactor design** (TRL 1): Pre-conceptual; no published engineering design for any Da Vinci subsystem.
+
+**Missing**: No TRL assessment for reactor-scale magnet systems (resistive coil design at Da Vinci dimensions). No divertor / exhaust system design for p-B11 alpha particle handling. No first wall design for Bremsstrahlung-dominated X-ray loading.
 
 **Gaps**:
-- p-B11 net energy gain (Q > 1) — `truly-unknown` — **blocking**: the single most fundamental unresolved issue
-- NBI at reactor scale and energy (>40 keV for efficient p-B11 heating) — `not-yet-sourced` / `derivable from accelerator literature` — **blocking** for cost modeling
-- First wall lifetime and replacement schedule for Da Vinci — `proprietary` — **important**
-- Electrode biasing system cost and longevity at reactor scale — `proprietary` — **nice-to-have**
+- Reactor-scale NBI system design (power level, injector count, beam energy for p-B11 operation) — `proprietary` — **important**
+- FRC tilt-mode and stability control at reactor separatrix radius (~1–2 m needed for net gain vs. 0.4 m at C-2W) — `truly-unknown` — **blocking**: TAE claims kinetic stabilization by fast ions, but this mechanism weakens at larger scales; documented in `grokipedia-tae-technologies.md`
+- Divertor and exhaust system for alpha particle and impurity management — `not-yet-sourced` — **important**
+- First wall / vessel design for Bremsstrahlung loading at 250 keV — `not-yet-sourced` — **important**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Good (qualitatively)
+**Coverage**: Poor
 
 **Available**:
-- Boron-11: ~80% of natural boron, globally abundant in borax deposits (Chile, Turkey, USA). No critical supply constraint. Commodity industrial chemical (`grokipedia-tae-technologies.md`).
-- Hydrogen (proton fuel): completely abundant, no supply issues.
-- No tritium requirement: major structural simplification; eliminates tritium processing, breeding blankets, and tritium supply chain entirely.
-- No HTS/superconducting magnet requirement: TAE explicitly avoids cryogenic superconducting systems, confirmed for C-2W and strongly implied for Da Vinci (`grokipedia-tae-technologies.md`, dossier).
-- Copper resistive coils for C-2W: standard manufacturing, no supply chain concern.
-- Inconel vacuum vessel: mature industrial manufacturing.
-- NBI ion source components (tungsten filaments, acceleration grids): established accelerator supply chain from ITER and fusion experimental programs.
-
-**Missing**:
-- Specific alloy/material requirements for first wall and divertor at Da Vinci operating conditions (higher X-ray flux from p-B11 than D-T neutrons).
-- Electrode materials for edge biasing at sustained reactor conditions.
-- Detailed magnet material specification for Da Vinci (confirmed resistive but alloy/coolant not stated).
+- No tritium supply chain required (aneutronic fuel confirmed, high confidence)
+- No heavy neutron shielding or remote handling infrastructure required
+- No beryllium, REBCO, or superconducting material dependencies evident from available sources
+- Copper resistive coils confirmed for experimental machines; likely for Da Vinci based on "simple geometry magnets" positioning (`grokipedia-tae-technologies.md`)
+- Boron-11 is 80% of natural boron (abundant, borax mineral deposits), documented in `grokipedia-tae-technologies.md`
+- NBI ion source components (gas injection, neutralizer, electrostatic acceleration) are established technology with industrial supply chains
+
+**Missing**: No data on the degree of B-11 isotopic enrichment required for reactor-grade fuel (reactor-grade likely requires >99% B-11 vs. 80% natural abundance). No industrial-scale B-11 enrichment capacity exists. No analysis of NBI component lifetime at reactor power levels. No first wall material selection for X-ray dominated wall loading environment.
 
 **Gaps**:
-- X-ray/UV flux effects on first wall material at 250 keV plasma (higher than D-T X-ray environment) — `not-yet-sourced` — **important**: affects replacement schedule and cost
-- Boron powder injection system at scale (method for introducing B-11 fuel during operation) — `not-yet-sourced` — **nice-to-have**
+- B-11 isotopic enrichment at commercial scale — `not-yet-sourced` — **important**: natural boron (80% B-11) may be sufficient or may not; reactor-grade requirements are unpublished; no commercial B-11 enrichment industry exists for fusion application
+- NBI component lifetime and replacement schedule at reactor power — `proprietary` — **important**: determines a major O&M cost driver
+- First wall material selection and lifetime under Bremsstrahlung X-ray loading — `truly-unknown` — **important**: p-B11 at 250 keV is Bremsstrahlung-dominated; wall design is conceptually different from neutron-shielded D-T concepts
+- Copper coil power dissipation and resistive magnet lifetime at Da Vinci scale — `proprietary` — **nice-to-have**
 
 ---
 
@@ -114,60 +97,63 @@
 **Available Parameters**:
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Net electrical output | 50 MWe (initial) / 350–500 MWe (at scale) | `tae-djt-merger-davinci-specs.md`; dossier | High |
-| Energy conversion method | Thermal steam (Rankine) | `tae-energy-conversion-clarification.md` | High |
-| Thermal efficiency (assumed) | ~33–38% (standard steam cycle) | Derivable from standard engineering | Medium |
-| Fuel cycle | p-B11 aneutronic | All sources | High |
-| Fuel cost | Near-zero (abundant H and B-11) | Derivable | High |
-| Neutron management cost | Minimal shielding only | TAE FAQ; dossier | High |
-| Tritium cost | N/A | Dossier | High |
-| Operation mode | Steady-state | All sources | High |
-| Capacity factor (target) | ~90% (standard baseload assumption) | `osti-servlets-purl-1001677.md` (Waganer PPPL methodology) | Low (assumed) |
-| Maintenance approach | Hands-on possible (no activation) | TAE FAQ | Medium |
-| Confinement magnet type | Resistive copper (likely) | C-2W confirmed; Da Vinci inferred | Medium |
-| Timeline | Construction 2026, power operations 2031 | `tae-djt-merger-davinci-specs.md` | Medium |
+| Target plant electrical output | 50 MWe (initial), 350–500 MWe (scale) | DJT merger/ANS Newswire (`iter-02/sources/tae-djt-merger-davinci-specs.md`) | m |
+| Energy conversion pathway | Thermal steam turbine (Da Vinci baseline) | TAE FAQ (`iter-02/sources/tae-energy-conversion-clarification.md`) | h |
+| Thermal efficiency (steam cycle) | ~33–38% | Standard steam cycle (derivable) | h |
+| Fuel type | p-B11 (abundant, low fuel cost) | TAE website, all sources | h |
+| Primary heating system | NBI, 8 injectors, 13 MW at C-2W scale | Nature Comms 2025; `iter-02/sources/tae-c2w-machine-details.md` | h (current device), l (reactor) |
+| Plasma temperature target (Da Vinci) | ~250 keV (~3 × 10⁹ °C) | `grokipedia-tae-technologies.md` | m |
+| Construction start target | 2026 (Da Vinci) | DJT merger press (`iter-02/sources/tae-djt-merger-davinci-specs.md`) | l (very optimistic) |
+| No tritium handling required | N/A | Fuel cycle definition | h |
+| No heavy neutron shielding | Minimal | TAE FAQ, concept definition | h |
+| Capacity factor framework | 1st-of-kind plants significantly below 87.6% (ARIES-AT 10th-OAK) | Waganer 2011 (`iter-02/sources/osti-servlets-purl-1001677.md`) | h (methodology), l (applied to p-B11 FRC) |
+| Approximate LCOE analog (modular fusion) | $34–54/MWh for ~500 MWe modular D-T concepts | ALPHA Revisit 2020 (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) | l (different fuel/concept) |
 
 **Missing Parameters**:
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Capital cost estimate (any subsystem) | proprietary | Blocking | No cost data published anywhere for Da Vinci or commercial FRC |
-| NBI system capital cost at Da Vinci scale | proprietary | Blocking | NBI likely dominant cost driver; no analogues directly applicable |
-| Fusion power / Q_plasma | truly-unknown | Blocking | Q > 1 never achieved; no target Q published for Da Vinci |
-| NBI wall-plug efficiency at reactor scale | proprietary/truly-unknown | Blocking | Determines recirculating power fraction, which is the single biggest LCOE lever |
-| First wall / chamber replacement schedule | proprietary | Important | Affects O&M cost; aneutronic conditions reduce damage but X-ray/UV flux still exists |
-| O&M cost estimate | proprietary | Important | No analog published; hands-on maintenance simplifies vs D-T |
-| NBI electrical power demand (continuous) | proprietary | Blocking | Must be derived from Q and NBI efficiency; neither known |
-| Confinement magnet power (continuous) | derivable | Important | Resistive magnets have continuous power draw; field ~0.1–0.3 T (C-2W) |
-| ICC direct conversion efficiency | truly-unknown | Nice-to-have | Long-term upgrade path; Da Vinci uses thermal steam |
-| Plant scaling law (50 MWe → 350–500 MWe) | proprietary | Important | Determines whether economics improve with scale |
+| Fusion gain Q at reactor conditions (p-B11, 250 keV) | truly-unknown | blocking | Central unknown; determines power balance; undemonstrated for p-B11 in any device |
+| NBI recirculating power fraction at reactor Q | truly-unknown | blocking | NBI is entire heating system; high recirculating power at low Q makes LCOE extremely sensitive; Mulder et al. (arxiv-2103-12451) framework is applicable but requires Q input |
+| Capital cost by CAS account for Da Vinci | proprietary / not-yet-sourced | blocking | No plant study exists; TAE claims "50% cheaper than tokamak" but no absolute figures published |
+| Balance of plant capital cost | derivable | important | No p-B11 FRC plant study; ALPHA costing BOP at ~$2.4/W CapEx for modular 500 MWe D-T concepts (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) provides order-of-magnitude analog but different concept |
+| NBI system capital cost at reactor scale | proprietary | blocking | NBI is the dominant power core cost; no published estimates for reactor-grade NBI systems at the required power level |
+| O&M cost (staffing, component replacement) | not-yet-sourced | important | No published estimates; major O&M driver will be NBI system maintenance |
+| Capacity factor / plant availability | derivable | important | Waganer 2011 methodology (`iter-02/sources/osti-servlets-purl-1001677.md`) can bound this; 1st-of-kind likely 50–70%; no TAE-specific figure |
+| ICC direct conversion efficiency and cost | proprietary | nice-to-have | Patents claim >90%; not Da Vinci baseline; relevant for long-term LCOE projection |
+| B-11 fuel cycle cost (enrichment) | not-yet-sourced | important | Natural boron may or may not suffice; no commercial B-11 enrichment precedent |
+| First wall / vessel capital cost | truly-unknown | important | X-ray rather than neutron loading environment; no design exists |
 
 ---
 
 ## Source Recommendations
 
-1. **NBI system cost at scale**: Search ITER NBI design documentation and Fusion Engineering and Design literature for neutral beam cost scaling. ITER's 16.5 MW NBI system has published cost estimates that could provide an analog — `unverified — confirm existence before searching`. Search terms: "ITER neutral beam injector cost" or "neutral beam injection cost scaling fusion."
+**Fleet-wide source integrations and disqualifications:**
+
+- **ALPHA Revisit 2020** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) — **Integrated (methodology analog, not direct).** Opened and read. The four costed concepts are Plasma-Jet MIF, Stabilized Liner, Staged Z-Pinch, and Flow-stabilized Z-Pinch — all D-T pulsed pinch/liner concepts, not p-B11 FRC. Their neutron power fraction (~80% of fusion power) and tritium/blanket systems are fundamentally absent from p-B11 FRC. However, the BOP methodology and modular plant cost results ($34–54/MWh LCOE, ~$2.4/W CapEx for 500 MWe) provide an order-of-magnitude analog for compact modular fusion LCOE with similar plant size. This addresses the "LCOE ballpark" question but does not resolve the concept-specific capital cost gap (which remains blocking).
+
+- **Waganer 2011 Availability Methodology** (`iter-02/sources/osti-servlets-purl-1001677.md`) — **Integrated.** Read. Provides a framework for estimating plant availability from 1st-of-kind to 10th-of-kind fusion plants. ARIES-AT achieved 87.6% for a 10th-of-kind tokamak. A 1st-of-kind p-B11 FRC plant would be significantly lower. This methodology can be used to bound capacity factor assumptions, downgrading the capacity factor gap from `blocking` → `derivable` with stated assumptions. Does not substitute for concept-specific maintenance data.
+
+- **Mulder et al. 2021** (`iter-02/sources/arxiv-2103-12451.md`) — **Integrated.** Read. Provides an analytical framework showing that high recirculating power combined with low capacity factor produces poor plant efficiency — directly applicable to NBI-driven TAE concept where recirculating power is inherently high. Demonstrates why Q and NBI wall-plug efficiency are the critical sensitivity parameters. Confirms that the NBI recirculating power gap is a blocking issue, not merely important.
 
-2. **p-B11 reactivity and bremsstrahlung balance**: The Putvinski, Ryutov & Yushmanov 2019 *Nuclear Fusion* paper ("Fusion reactivity of the pB11 plasma revisited," Nucl. Fusion 59 076018) is cited in `osti-pages-servlets-purl-2441289.md` and directly addresses the physics feasibility question. This paper is likely accessible via OSTI. High priority for understanding the physics feasibility ceiling.
+**Concept-specific gaps, `not-yet-sourced` recommendations:**
 
-3. **FRC/compact confinement cost analogs**: The ARPA-E ALPHA revisit study (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) covers compact confinement concepts in a CAS framework. While none of the four concepts is a p-B11 FRC, the methodology and BOP/indirect cost structure are directly applicable. Recommend reading this source.
+1. **TAE's Copernicus design documentation** — TAE has described Copernicus as the net-energy validation machine preceding Da Vinci. If any public engineering specifications exist (conference papers, INFUSE reports), they would constrain reactor-scale NBI power requirements and magnet design. Search OSTI and DOE INFUSE program publications for TAE INFUSE awards (confirmed in DJT merger press, `iter-02/sources/tae-djt-merger-davinci-specs.md`). `unverified — confirm existence before searching`
 
-4. **Plant availability methodology**: The Waganer PPPL availability paper (`iter-02/sources/osti-servlets-purl-1001677.md`) was already sourced and provides the 10th-OAK / first-OAK / one-OAK framework. Use for capacity factor assumptions: 87.6% for mature plant, ~46% for one-OAK.
+2. **Independent p-B11 physics assessments** — Papers analyzing the physics feasibility of net energy gain via p-B11 (e.g., Putvinski et al., Rider 1997 critique, Hay et al.) would anchor the Q-factor uncertainty and the bremsstrahlung/fusion power balance. These exist in the published literature. Search OSTI and arXiv for "proton boron-11 fusion power balance" and "aneutronic fusion bremsstrahlung breakeven." These directly address the blocking physics gaps.
 
-5. **Recirculating power analysis**: The Mulder et al. 2021 arxiv paper (`arxiv-2103-12451.md`) was captured only as an abstract. The full paper analyzes high-recirculated-power fusion plants and should be obtained to support quantitative recirculating power fraction estimates. Search arXiv:2103.12451.
+3. **NBI system cost studies** — NBI capital costs are relevant from ITER and JT-60SA programs. NBI injector cost data from ITER-scale studies would provide an analog for high-power NBI costs per MW. Search OSTI for "neutral beam injector capital cost" or ITER NBI cost estimates. `unverified — confirm existence before searching`
 
-6. **p-B11 cross section and ignition requirements**: Academic literature on p-B11 physics feasibility (particularly Nevins & Swain, 2000 *Nuclear Fusion*; and the 2019 Putvinski et al. paper) would fill the physics foundation. Search OSTI or Google Scholar for "p-B11 aneutronic fusion ignition requirements" — `unverified — confirm existence before searching`.
+4. **TAE INFUSE program technical reports** — DOE INFUSE program has funded TAE projects on spheromak injectors, simulations, and diagnostics since 2019 (documented in `grokipedia-tae-technologies.md`). These reports may contain more design detail than public press releases. Search DOE INFUSE award database for TAE Technologies.
 
 ---
 
 ## Summary
 
-Proceed to full analysis, but with clear expectations about what is and is not knowable. The qualitative sections (data availability, system function challenges, subsystem maturity, materials) can be written at high quality using available sources. The quantitative LCOE model will necessarily be built on assumptions rather than published cost data, with the following structure:
+The available data is sufficient to characterize the p-B11 FRC concept qualitatively and perform a semi-quantitative LCOE analysis with large stated uncertainties. The physics architecture is well-documented (FRC confinement, NBI-only formation, p-B11 fuel cycle, thermal steam conversion for Da Vinci). The concept's cost advantages relative to D-T MFE are qualitatively clear (no tritium, no heavy shielding, simpler magnets).
 
-- **What is solid**: Power output target, energy conversion pathway, fuel cost, maintenance simplification, magnet type, and fuel supply chain.
-- **What must be assumed from analogues**: Capital cost per MWe (use ARPA-E ALPHA ranges for compact MFE), O&M costs (use standard fusion O&M analogs), thermal efficiency (standard steam cycle).
-- **What requires explicit flagging as blocking uncertainties**: Q value, NBI recirculating power fraction, and whether p-B11 net energy is physically achievable at any reasonable machine scale. The 1 c/kWh back-solve will reveal that this concept requires extraordinary breakthroughs in plasma performance well beyond current demonstrations.
+However, the fundamental LCOE drivers are all blocking unknowns: the fusion gain Q at p-B11 conditions is undemonstrated, the NBI recirculating power fraction that will determine whether the concept can achieve net electricity export is unconstrained, no capital cost structure for any reactor-scale FRC system exists in the public literature, and the FRC confinement scaling from C-2W's ~10 keV to Da Vinci's ~250 keV target has no experimental validation. The concept sits at TRL 3–4 overall with the most optimistic element being the Norm machine's NBI-only formation breakthrough.
 
-The $0.01/kWh back-solve will be a particularly illuminating section: the combination of very low fuel cost, no tritium breeding, and simplified shielding creates a favorable cost structure in principle—but it is entirely negated if Q is low (forcing NBI recirculation to dominate) or if plasma performance requires repeated machine upgrades before commercial operation.
+**Recommendation**: Proceed to a full qualitative analysis using available physics data. For the quantitative LCOE model, construct a parametric model with Q and NBI efficiency as the two primary free parameters, use the Waganer (2011) methodology to bound capacity factor, and use the ALPHA Revisit BOP costs as order-of-magnitude anchors for plant-level costs. Explicitly flag that all cost estimates are order-of-magnitude until a p-B11 FRC plant study exists. Before building the model, read the independent p-B11 bremsstrahlung breakeven literature to bound the Q parameter space physically.
 
 ---
 
@@ -177,11 +163,11 @@
 overall_rating: "Significant Gaps"
 blocking_count: 5
 important_count: 6
-counting_method: "deduplicated across all sections; only counted once per distinct gap — Q/net energy, NBI efficiency/recirculating power, NBI cost at scale, capital cost absence, and bremsstrahlung physics as blocking; first wall lifetime, O&M costs, plant scaling law, magnet power draw, Da Vinci magnet confirmation, and X-ray wall effects as important"
+counting_method: "sections 1-5 deduplicated: blocking = proprietary plant study absence (§1), Q-factor/energy gain (§2+§5), NBI recirculating power fraction (§2+§5), FRC stability scaling to reactor size (§3), NBI system capital cost (§5); important = B-11 enrichment (§4), BOP capital cost (§5), O&M costs (§5), capacity factor (§5), divertor/first wall design (§3+§4), independent TEA assessment (§1)"
 section_coverage:
   availability_of_data:       "Partial"
-  system_function:            "Partial"
+  system_function:            "Good"
   subsystem_maturity:         "Partial"
-  materials_supply_chain:     "Good"
+  materials_supply_chain:     "Poor"
   lcoe_parameter_extraction:  "Poor"
 ```
\ No newline at end of file
```
