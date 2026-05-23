# Diff: 27-polywell

**Generated:** 2026-05-22T11:04:30-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 7 | 6 | -1 |
| important_count  | 4 | 9 | - |
| overall_rating   | Significant Gaps | Significant Gaps | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
155:4. **Generic D-T MFE BOP cost references** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — applicable as cost analog for balance of plant, O&M, and indirect costs, since Polywell D-T uses standard thermal conversion and tritium handling infrastructure once the plasma core is resolved. Recommend reading for CAS account methodology applicable to Section 5 LCOE construction.
157:5. **ARIES cost account documentation** (`knowledge/sources/aries_cost_account_documentation/`) — applicable for CAS framework structure. Polywell has a novel core but standard BOP; ARIES CAS accounts 21 (structures), 22 (reactor plant), 26 (heat transfer/thermal), 27 (fuel handling) likely all applicable. Recommend reading for cost analog methodology.
```

## Blocking-tier lines (baseline)

```
33:- Thermal cycle specification — `truly-unknown` (EMC2 has not published this) — **blocking**
78:- Superconducting polyhedral coil design — `proprietary` (EMC2 may have internal work from 2012+) / `truly-unknown` — **blocking**
79:- Tritium breeding blanket design and TRL — `truly-unknown` — **blocking**
```

## Blocking-tier lines (new)

```
56:- γ=0.1 is an unvalidated assumption spanning 1 order of magnitude of uncertainty — `truly-unknown` (EMC2 acknowledges it) — **blocking** for any quantitative Q assessment
58:- Potential well formation undemonstrated at reactor-relevant density — `truly-unknown` — **blocking** for physics credibility claims
79:- Steady-state high-beta operation not demonstrated — `truly-unknown` — **blocking** for TRL advancement
80:- Integrated system (M1+M2+M3 simultaneously) never demonstrated — `truly-unknown` — **blocking**
130:| Gross electric output (MWe) | truly-unknown | blocking | No thermal cycle specified; cannot compute plant output |
131:| Thermal conversion efficiency | truly-unknown | blocking | Cycle type (Rankine/sCO₂) not specified in any source |
132:| Net electric output | truly-unknown | blocking | Requires gross output minus recirculating power |
133:| Recirculating power fraction | derivable | blocking | E-beam at 78 MW + magnet power; no magnet power estimated |
135:| Total capital cost ($/kWe) | truly-unknown | blocking | No engineering design, no cost study |
136:| Capital cost by CAS account | truly-unknown | blocking | No plant study exists |
137:| O&M cost ($/MWh) | truly-unknown | blocking | No operations concept |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/27-polywell.md	2026-05-22 09:21:13.875642800 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/27-polywell/gap_report.md	2026-05-22 11:04:30.757044065 -0700
@@ -1,60 +1,61 @@
-Now I have all the source material. Let me write the gap assessment.
+I now have sufficient information to write the gap assessment. Let me compile it:
+
+---
 
 # Gap Assessment: Polywell (D-T)
 
 ## Overall Readiness
 **Rating**: Significant Gaps
 
-**Summary**: The Polywell D-T concept has a single credible reactor-scale physics study (Park et al. 2025) and a handful of experimental records, but no engineering plant study, no capital cost estimates, and no specified thermal cycle or blanket design. The physics model rests on an unvalidated free parameter (γ=0.1 loss reduction factor). An LCOE analysis is possible but will be almost entirely analogy-based and assumption-driven — the error bars will be enormous. Two potentially relevant sources from the dossier (Rogers 2018, Sporer 2022) were not extracted and may partially close gaps.
+**Summary**: The Polywell (D-T) has meaningful physics documentation from the Park 2025 preprint and the WB-series experimental history, but remains firmly in the realm of physics scaling studies with no engineering design, no capital cost data, and no techno-economic analysis in the public literature. The one reactor-scale design reference (Park et al., arXiv:2508.06761) is a parametric physics paper that explicitly acknowledges multiple optimistic free parameters — notably the unvalidated loss reduction factor γ=0.1 on which the Q=10.5 result entirely depends. A qualitative analysis is feasible; a quantitative LCOE analysis requires deriving nearly every cost parameter from generic MFE analogues with very low concept-specific confidence.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Limited
+**Coverage**: Partial
 
 **Available**:
-- Park et al. 2025 (arXiv:2508.06761): The only EMC2-authored reactor design study. Provides physics scaling to Q=10.5, 980 MW fusion power, and some qualitative engineering observations. This is a preprint, not a full engineering design report.
-- Park et al. 2015 (Phys. Rev. X): Peer-reviewed experimental result demonstrating high-beta electron confinement in WB-X. No reactor extrapolation.
-- EMC2 website: High-level technology description, FPNS program overview, broad performance claims (100 MW–1 GW).
-- FPNS/SHINE DOE proposal (2023–2024): FPNS hardware parameters at neutron source scale (350 kW fusion power, 8.5 cm radius). Real engineering constraints but not a power plant.
-- Experimental history (WB-1 through WB-X): Documented via secondary sources. Resistive-coil pulsed devices only; no sustained fusion burn.
+- ~40 years of experimental history (WB-1 through WB-X) documented across Wikipedia/polywell-technical-details.md (109 KB), the Fusion Report interview, and the dossier. Covers physics concept, key milestones, funding history, and scaling rationale.
+- WB-X high-beta electron confinement demonstration (Phys. Rev. X 2015) — the one peer-reviewed experimental result, cited throughout sources but not directly extracted.
+- Park et al. 2025 (arXiv:2508.06761, 89 KB extracted): detailed physics scaling model, Q=10.5 reactor parameters, ECsim PIC simulation results, and a summary of essential mechanism validation status.
+- FPNS proposal (iter-02/emc2-fpns-talk-polywell-2023.md): device parameters for the neutron-source intermediate step (8.5 cm plasma radius, 2–3 T, 350 kW fusion power, 5–6 MW ion beam input).
+- EMC2 website summary: company posture, ongoing research framing, D-T focus confirmed.
 
 **Missing**:
-- No published plant study or system code analysis for a D-T power plant
-- No EMC2 engineering white paper or techno-economic report
-- Rogers 2018 (J. Fusion Energy) covers p-B11, not D-T, but may contain engineering cost structure useful as analogue — **not extracted in Phase 1a**
-- Sporer 2022 ("Analysis of Two Fusion Reactor Designs Based on Magnetic Electrostatic Plasma Confinement") likely contains engineering/cost analysis of Polywell-type designs — **not extracted in Phase 1a**
-- Lynceans/EMC2 "Fork in the Road" document may contain economic framing — **not extracted in Phase 1a**
+- No published power plant engineering design (no blanket, shield, BOP, thermal cycle, or structural design)
+- No independent techno-economic study of Polywell specifically
+- Rogers (2018) reactor design study is cited in the dossier but not extracted (journal paywall); Sporer (2022) analysis also unextracted
+- No disclosure of any EMC2 internal cost modeling or funding milestones post-2015
 
 **Gaps**:
-- No power plant engineering design study — `proprietary` (unlikely to exist even internally at current stage) / `not-yet-sourced` (Rogers 2018, Sporer 2022 may provide analogues) — **blocking for LCOE**
-- Thermal cycle specification — `truly-unknown` (EMC2 has not published this) — **blocking**
-- Blanket design — `truly-unknown` at this stage — **blocking for tritium self-sufficiency assessment**
+- No independently authored techno-economic assessment — `truly-unknown` for published work, `proprietary` for EMC2 internal — **important**
+- Rogers 2018 and Sporer 2022 reactor design papers not captured — `not-yet-sourced` — **important** (Rogers addresses net-power D-T design; Sporer compares two MESC designs including cost implications)
+- EMC2's superconducting Polywell development (reportedly started 2012) produced no publications — `proprietary` — **nice-to-have**
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Partial (challenges are well-characterized; resolutions are not)
+**Coverage**: Partial
 
 **Available**:
-- The γ=0.1 loss reduction factor is explicitly flagged by Park et al. 2025 as a free parameter derived from 2D PIC simulations extrapolated to 3D. Authors acknowledge "several optimistic projections."
-- Electron confinement scaling: WB-X demonstrated high-beta electron confinement at small scale; extrapolation to reactor scale is theoretically justified but experimentally unvalidated.
-- Steady-state operation: Park et al. 2025 models it explicitly; WB-series devices were all pulsed. No demonstrated steady-state plasma.
-- Electron beam injection at 60 keV, 1.3 kA: Park et al. notes "off-the-shelf availability" of such injectors, which is the strongest engineering grounding in any source.
-- Neutron shadowing by polyhedral coils: acknowledged in Park et al. 2025 as a novel blanket engineering challenge.
+- The three essential Polywell mechanisms (M1–M3) are well described in Park 2025: high-beta cusp confinement, potential well formation by electron beam injection, electrostatic ion confinement.
+- Critical unresolved physics explicitly acknowledged: loss reduction factor γ is a free parameter (γ=0.1 assumed, not experimentally validated); potential well formation at fusion-relevant density not demonstrated.
+- Startup challenge: WB-X required 700 MW pulsed power (coaxial plasma guns) to achieve high-beta. Park 2025 acknowledges future devices need new startup systems.
+- Non-standard confinement (not Maxwellian plasma, non-toroidal geometry) makes standard plasma scaling laws inapplicable without concept-specific validation.
+- Tritium breeding geometry challenge identified: "neutron shadowing caused by internal coil structures" (Park 2025), but no solution proposed.
 
 **Missing**:
-- No experimental demonstration of Q > 0 (net fusion gain)
-- No validated confinement scaling law — the critical physics bet is unresolved
-- No PIC simulation results for reactor-scale parameters
-- No thermal-hydraulic or neutronics analysis of the polyhedral geometry
+- Steady-state startup solution for a power plant (the coaxial gun approach used in WB-X was pulsed and high-impurity)
+- How potential well formation behaves at reactor-scale plasma density (10²¹ m⁻³ vs. demonstrated conditions)
+- Quantitative model for γ (loss reduction factor) — the entire Q budget depends on this
+- Energy balance accounting for recirculating power (electron beam at 78 MW must be driven by plant output)
 
 **Gaps**:
-- Confinement scaling validity (γ extrapolation) — `truly-unknown` — **blocking for any credible performance projection**
-- Stability of high-density plasma (~10²¹/m³) in the potential well — `truly-unknown` — **important**
-- First-wall/PFC heat flux management at reactor scale — `not-yet-sourced` (FPNS has some PFC data; Sporer 2022 may have more) — **important**
+- γ=0.1 is an unvalidated assumption spanning 1 order of magnitude of uncertainty — `truly-unknown` (EMC2 acknowledges it) — **blocking** for any quantitative Q assessment
+- No steady-state startup system demonstrated or designed — `truly-unknown` — **important**
+- Potential well formation undemonstrated at reactor-relevant density — `truly-unknown` — **blocking** for physics credibility claims
 
 ---
 
@@ -62,22 +63,23 @@
 **Coverage**: Partial
 
 **Available**:
-- **Polyhedral cusp coils (resistive)**: TRL ~4–5. WB-X demonstrated high-beta confinement. WB-8 (0.8 T) achieved 6× higher plasma density. No superconducting version demonstrated.
-- **Electron beam injectors**: TRL ~7–8. Park et al. 2025 states "off-the-shelf availability of steady-state electron beam injectors" at 60 keV. FPNS uses similar technology.
-- **Ion beam injectors (for FPNS mode)**: TRL ~5–6. FPNS specifies 150–200 keV, 5–6 MW ion beams — not demonstrated at this scale for Polywell specifically.
-- **Superconducting polyhedral coils**: TRL ~2–3. EMC2 reportedly began superconducting Polywell work in 2012; no published results. Required for reactor-scale steady-state operation at 4.5 T.
-- **Vacuum vessel**: Not described specifically. Conventional technology; TRL ~8–9 for analogous confinement systems.
+- Electron beam injection: Park 2025 notes "off-the-shelf availability of steady-state electron beam injectors" at MW-class — TRL 6+ for the electron beam technology itself. FPNS proposal specifies 150–200 keV, 5–6 MW ion beam injectors (for neutron source variant).
+- High-beta cusp plasma formation: demonstrated at small scale (WB-X, 13.8 cm coil diameter) — TRL 3 (physics demonstrated at small scale, pulsed).
+- Polyhedral coil arrangement: tested in resistive form WB-1 through WB-X. Superconducting version reportedly initiated in 2012 but no results — TRL 2–3 for HTS variant.
+- Plasma diagnostics: mature tools (microwave interferometry, x-ray, flux loops) used in experiments.
 
 **Missing**:
-- **Tritium breeding blanket**: TRL ~1 (concept only; coil-shadowing challenge acknowledged but unresolved). No material or geometry specified.
-- **First wall/PFC for reactor scale**: TRL ~2–3 (FPNS data at 350 kW fusion power only; 980 MW reactor is 2800× more powerful)
-- **Energy conversion system (thermal cycle)**: TRL unknown — not specified anywhere in available sources
-- **Tritium handling and processing**: TRL ~5–6 by analogy to D-T fusion community; Polywell-specific challenges not documented
+- TRL for potential well formation integrated system: no published demonstration — TRL 2 at best.
+- Tritium breeding blanket: geometry not specified, TRL 1 (concept acknowledged only).
+- Thermal conversion system: cycle type not specified, TRL 1 (concept-specific).
+- Steady-state high-beta operation: never demonstrated (all WB-X shots were <20 µs in high-beta phase).
+- First wall / plasma-facing component design for 14 MeV neutron flux at ~780 MW neutron power.
 
 **Gaps**:
-- Superconducting polyhedral coil design — `proprietary` (EMC2 may have internal work from 2012+) / `truly-unknown` — **blocking**
-- Tritium breeding blanket design and TRL — `truly-unknown` — **blocking**
-- Thermal conversion system — `truly-unknown` for this concept specifically; **important** (derivable by analogy)
+- Steady-state high-beta operation not demonstrated — `truly-unknown` — **blocking** for TRL advancement
+- Integrated system (M1+M2+M3 simultaneously) never demonstrated — `truly-unknown` — **blocking**
+- Tritium blanket TRL effectively 1 — `truly-unknown` for concept-specific geometry — **important**
+- HTS coil design for 4.5 T steady-state cubic geometry — `not-yet-sourced` (likely exists for analogous compact devices) — **important**
 
 ---
 
@@ -85,102 +87,96 @@
 **Coverage**: Poor
 
 **Available**:
-- **Tritium**: General D-T supply challenge applies. No Polywell-specific tritium consumption rate published; derivable from Park et al. 2025 fusion power (980 MW → ~56 g/day tritium burn at 100% burnup, TBR unknown).
-- **Magnet conductor**: All demonstrated devices use copper (resistive). Reactor requires superconducting coils at 4.5 T — LTS (NbTi/Nb₃Sn) or HTS (REBCO) unspecified. Both are available commercially.
-- **Electron beam system components**: Relatively standard accelerator technology per Park et al. 2025; no supply chain concerns flagged.
-- **Neutron shielding materials**: Standard; no concept-specific challenge beyond polyhedral geometry.
+- D-T fuel cycle: standard challenge, well-characterized in fleet-wide literature. Tritium supply from fission reactors acknowledged as needed.
+- 14.1 MeV neutrons at ~780 MW neutron power: standard challenge for D-T concepts, neutron activation and first-wall erosion well-characterized generically.
+- FPNS proposal mentions "tritium handling and shielding" as required system elements.
 
 **Missing**:
-- Blanket material (Li₂TiO₃, Li₄SiO₄, LiPb, etc.) — unspecified; cannot assess Li-6 supply implications
-- Coil conductor specification (LTS vs HTS) — unspecified
-- PFC material (W, CFC, etc.) — not addressed
-- Manufacturing complexity of the polyhedral coil geometry — noted as advantageous (non-interlocking) but not costed
+- No concept-specific materials selection for first wall, blanket, or coil casing
+- No specification of breeding material (Li ceramics, LiPb, FLiBe) — coil shadowing challenge noted but not resolved
+- No supply chain analysis for any Polywell-specific component
+- Magnet material unspecified for reactor scale (copper vs. HTS vs. NbTi/Nb₃Sn)
+- Coil casing material for plasma-facing surfaces (WB-8 used boron nitride cylinders as PFC insulation — reactor-scale equivalent unspecified)
 
 **Gaps**:
-- Blanket material and lithium supply chain — `truly-unknown` at this stage — **important** (for D-T self-sufficiency)
-- Superconductor type and quantity — `derivable` from coil geometry once specified, but geometry not specified — **important**
-- PFC material specification — `not-yet-sourced` — **nice-to-have** for first pass
+- No first-wall material selection — `not-yet-sourced` for generic 14 MeV D-T studies, `truly-unknown` for Polywell-specific geometry — **important**
+- No blanket material or supply chain analysis — `truly-unknown` — **important**
+- Magnet technology for reactor scale not specified — `derivable` from HTS analogs if geometry assumed — **important**
+- No tritium self-sufficiency analysis — `derivable` from breeding ratio assumptions once blanket is specified — **nice-to-have** at this stage
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor
-
 **Available Parameters**:
 
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Fusion power | ~980 MW | Park et al. 2025 | m |
-| Input (driver) power | 78 MW (60 keV, 1.3 kA e-beam) | Park et al. 2025 | m |
-| Q value | 10.5 | Park et al. 2025 | l (γ=0.1 unvalidated) |
-| Device size | 1.6 m cube (coil-to-coil) | Park et al. 2025 | m |
-| Magnetic field | 4.5 T boundary | Park et al. 2025 | m |
-| Plasma volume | ~4.1 m³ | Park et al. 2025 | m |
-| Thermal efficiency (rough) | ~40% | polywell-technical-details.md | l (no primary source cited) |
-| FPNS R&D cost | $20M / 24 months | EMC2/SHINE proposal | l (neutron source only; not power plant) |
-| Navy program cost | ~$12M total | polywell-technical-details.md | h (historical) |
-| Operation mode | Steady-state (design intent) | Park et al. 2025 | m |
-| Electron beam "off-the-shelf" | Implies moderate cost | Park et al. 2025 | l (no $ cited) |
+| Fusion power | ~980 MW | Park 2025 (arXiv:2508.06761) | low — depends on γ=0.1 |
+| Input power (e-beam) | 78 MW at 60 keV, 1.3 kA | Park 2025 | low — tied to γ=0.1 |
+| Q value | ~10.5 | Park 2025 | low — unvalidated assumption chain |
+| Plasma temperature | 20 keV | Park 2025 | medium — design target |
+| Plasma density | 1.3×10²¹ m⁻³ | Park 2025 | medium — design target |
+| Device size | 1.6 m cube | Park 2025 | medium — design geometry |
+| Cusp field (boundary) | 4.5 T | Park 2025 | medium — design parameter |
+| Operation mode | Steady-state (intended) | Park 2025 | medium |
+| Bremsstrahlung loss | 15.5 MW | Park 2025 | medium — calculable from parameters |
+| Neutron power fraction | ~80% (~784 MW) | Derived from D-T physics | high — standard D-T |
+| FPNS fusion power | 350 kW | FPNS proposal (2023) | medium — near-term device only |
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Capital cost by subsystem | truly-unknown | Blocking | No plant study; analogy to accelerator/magnet costs required |
-| Total plant capital cost (overnight) | truly-unknown | Blocking | No published estimate |
-| Thermal cycle type and efficiency | truly-unknown | Blocking | Not specified anywhere; Rankine/sCO2 analogy required |
-| Blanket cost and design | truly-unknown | Blocking | No blanket design; standard tokamak breeding blanket costs not applicable due to polyhedral geometry |
-| Superconducting coil cost | derivable | Blocking | Coil geometry compact (1.6 m), non-interlocking; cost derivable once conductor type assumed |
-| O&M cost rate | truly-unknown | Blocking | No published O&M estimate |
-| Capacity factor / availability | derivable | Important | No published value; analogy to steady-state MFE concepts (~80–90%) is reasonable |
-| Component replacement schedule | truly-unknown | Important | First wall lifetime at 980 MW fusion power not addressed |
-| Tritium breeding ratio (TBR) | truly-unknown | Important | Blanket unspecified; TBR < 1 unless novel blanket designed for polyhedral shadowing |
-| Electrical output (gross/net) | derivable | Blocking | Derivable from 980 MW fusion × ~40% thermal eff. × recirculating power; ~320–350 MWe estimated |
-| Scaling assumptions / plant size | derivable | Important | Only one reactor design point; scaling not explored |
+| Gross electric output (MWe) | truly-unknown | blocking | No thermal cycle specified; cannot compute plant output |
+| Thermal conversion efficiency | truly-unknown | blocking | Cycle type (Rankine/sCO₂) not specified in any source |
+| Net electric output | truly-unknown | blocking | Requires gross output minus recirculating power |
+| Recirculating power fraction | derivable | blocking | E-beam at 78 MW + magnet power; no magnet power estimated |
+| Capacity factor / availability | truly-unknown | important | No engineering operations analysis; Park 2025 notes "high facility availability factor" qualitatively but no number |
+| Total capital cost ($/kWe) | truly-unknown | blocking | No engineering design, no cost study |
+| Capital cost by CAS account | truly-unknown | blocking | No plant study exists |
+| O&M cost ($/MWh) | truly-unknown | blocking | No operations concept |
+| Magnet system cost | derivable | important | Can analog from HTS compact devices if magnet type resolved |
+| Electron beam injector cost | not-yet-sourced | important | Off-the-shelf MW-class injectors exist; pricing may be in industrial catalogs or DoE procurement records |
+| Tritium breeding blanket cost | truly-unknown | important | Geometry not specified; cannot apply standard blanket cost models |
+| First-wall / shield cost | derivable | important | Generic D-T first-wall analogs possible but geometry complicates it |
+| Fuel cost | derivable | nice-to-have | Standard D-T fuel cycle cost applies |
+| Decommissioning | derivable | nice-to-have | Generic activated structure decommissioning models apply |
 
 ---
 
 ## Source Recommendations
 
-1. **Rogers 2018** — J. Fusion Energy 37, 1-17: "A Polywell Fusion Reactor Designed for Net Power Generation." This is explicitly about net power generation, not just physics. Even though it's p-B11, it likely contains cost structure, BOP assumptions, and scaling that can inform D-T analogues. Listed in dossier citations but **not extracted**. Priority: **high** — `not-yet-sourced`.
+1. **Rogers, J.G. (2018), "A Polywell Fusion Reactor Designed for Net Power Generation," J. Fusion Energy 37, 1-17** — `not-yet-sourced`. Appears in dossier citations. This is the one published attempt at a Polywell power plant design. Should be extracted — may contain capital cost estimates or engineering subsystem sizing. *Confirm existence before searching: citation provided in dossier, link given as `https://link.springer.com/article/10.1007/s10894-017-0147-9`.*
 
-2. **Sporer 2022** — "Analysis of Two Fusion Reactor Designs Based on Magnetic Electrostatic Plasma Confinement" (Michigan plasma lab). The title suggests capital cost / engineering analysis of Polywell-type designs. Listed in dossier citations but **not extracted**. Priority: **high** — `not-yet-sourced`. `unverified — confirm existence before searching`.
+2. **Sporer, A. (2022), "Analysis of Two Fusion Reactor Designs Based on Magnetic Electrostatic Plasma Confinement"** — `not-yet-sourced`. Cited in dossier with URL. University of Michigan thesis-level paper comparing two MESC designs; may contain cost or sizing analysis. *Link given as `https://plasmabay.engin.umich.edu/...`.*
 
-3. **Lynceans/EMC2 "Fork in the Road" PDF** — EMC2 internal/presentation document. May contain economic framing or cost comparisons. Listed in dossier but **not extracted**. Priority: **medium** — `not-yet-sourced`. `unverified — confirm existence before searching`.
+3. **ARPA-E ALPHA program final reports for EMC2** — `not-yet-sourced`. EMC2 was an ALPHA performer. ARPA-E public reports may contain performance targets and cost projections. Search ARPA-E OPEN database for EMC2 project deliverables.
 
-4. **Park 2015 Phys. Rev. X (full paper)** — Peer-reviewed; may contain more detail on plasma parameters useful for loss rate derivation than the summary captured. `not-yet-sourced` — priority: **low** (physics, not cost).
+4. **Generic D-T MFE BOP cost references** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — applicable as cost analog for balance of plant, O&M, and indirect costs, since Polywell D-T uses standard thermal conversion and tritium handling infrastructure once the plasma core is resolved. Recommend reading for CAS account methodology applicable to Section 5 LCOE construction.
 
-5. **OSTI / DOE search for FPNS final report** — The FPNS DOE report was anticipated March 2025. If published, it may contain engineering design detail (PFC heat loads, coil design, tritium handling) that provides a scaling bridge to a power reactor. Search: OSTI.gov for "Fusion Prototypic Neutron Source EMC2 SHINE 2025." `not-yet-sourced`. Priority: **medium**.
+5. **ARIES cost account documentation** (`knowledge/sources/aries_cost_account_documentation/`) — applicable for CAS framework structure. Polywell has a novel core but standard BOP; ARIES CAS accounts 21 (structures), 22 (reactor plant), 26 (heat transfer/thermal), 27 (fuel handling) likely all applicable. Recommend reading for cost analog methodology.
 
-6. **APS-DPP conference proceedings (2025)** — Park et al. 2025 was presented at APS-DPP. Supplementary slides may contain cost or engineering detail not in the preprint. `not-yet-sourced`. Priority: **low**. `unverified — confirm existence before searching`.
+6. **Search OSTI for "polywell cost" or "IEC fusion economics"** — `unverified — confirm existence before searching`. Any DoD-funded EMC2 reports may have been deposited in OSTI under the N68936-09-0125 contract. Low probability of public cost data given defense classification of prior work.
 
 ---
 
 ## Summary
 
-**Proceed to full analysis with flagged assumptions**, but extract Rogers 2018 and Sporer 2022 first if time permits — these are the most likely to partially fill capital cost and BOP gaps.
-
-The Park et al. 2025 paper gives sufficient reactor design parameters (power, gain, device geometry, input power) to anchor a first-pass LCOE model, but virtually every cost parameter must be derived by analogy or assumption:
+Proceed to a qualitative analysis (physics principles, confinement mechanism, experimental status, system function challenges, TRL assessment) using the available sources — this is well-supported. For quantitative LCOE analysis, acquire Rogers (2018) and Sporer (2022) first; they are the only published attempts at Polywell power plant sizing and may unlock subsystem cost analogs. Without them, all capital cost parameters must be derived from MFE analogues with low concept-specific confidence, and the γ=0.1 free parameter means even the physics Q-value is a speculation rather than an estimate. A quantitative LCOE section written today would require extensive "derivable with stated assumptions" caveats across nearly every line item.
 
-- **Capital costs**: Use coil geometry (small, non-interlocking) + superconductor technology cost analogues; no primary estimate exists
-- **Thermal cycle**: Assume Rankine or sCO2 at 40% efficiency (rough literature cite available from polywell-technical-details.md, though sourcing is weak)
-- **BOP**: Analogy to compact tokamak or stellarator of similar electrical output
-- **Blanket**: Acknowledge as a blocking unknown for tritium self-sufficiency; assign a cost range from tokamak breeding blanket analogues with a large uncertainty multiplier for the polyhedral geometry challenge
-- **O&M**: Analogy to other steady-state MFE concepts
-
-The critical caveat for the entire analysis: the reactor design's viability rests on γ=0.1, an unvalidated free parameter. The LCOE model should treat Q (and by extension, gross electrical output and recirculating power fraction) as a highly uncertain input and show sensitivity sweeps. A Q significantly below 10 rapidly makes the concept nonviable for power production.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Significant Gaps"
-blocking_count: 7
-important_count: 4
-counting_method: "section_5_missing_parameters"
+blocking_count: 6
+important_count: 9
+counting_method: "blocking: thermal conversion efficiency, gross electric output, net electric output, total capital cost, capital cost by CAS account, O&M cost (all LCOE section) plus 2 physics gaps (γ unvalidated, potential well undemonstrated) counted once each — deduplicated to 6 distinct blocking gaps. important: Rogers/Sporer sources not captured, HTS coil design, blanket material/TRL, steady-state startup, first-wall material, electron beam injector cost, capacity factor, magnet system cost — deduplicated to 9."
 section_coverage:
-  availability_of_data:       "Limited"
-  system_function:            "Partial (challenges are well-characterized; resolutions are not)"
+  availability_of_data:       "Partial"
+  system_function:            "Partial"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Poor"
   lcoe_parameter_extraction:  "Poor"
-```
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
