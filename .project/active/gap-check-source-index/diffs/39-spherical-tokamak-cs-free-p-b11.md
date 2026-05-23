# Diff: 39-spherical-tokamak-cs-free-p-b11

**Generated:** 2026-05-22T11:34:17-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 8 | 7 | -1 |
| important_count  | 3 | 5 | - |
| overall_rating   | Significant Gaps | Insufficient Data | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
152:5. **Fleet-wide cost analogs** — `knowledge/sources/tea_dt_mfe_cost_analysis/` and `knowledge/sources/aries_cost_account_documentation/` are applicable for BOP, indirect costs, and CAS framework, but cannot fill any concept-specific gap. Use only as methodology scaffolding. No additional fleet-wide source is likely to be concept-specific.
```

## Blocking-tier lines (baseline)

```
30:- **No commercial plant design point published** — `truly-unknown` — **blocking** (LCOE inputs are entirely absent; the published material is a physics-verification roadmap, not a plant study).
31:- **Direct energy conversion design** — `truly-unknown` — **blocking** (the central economic-case dependency; TRL 1–2).
53:- **p-B11 ignition feasibility in a thermal spherical tokamak** — `truly-unknown` — **blocking** (the most fundamental gap; Li 2024 quantitatively challenges the proposed hot-ion-mode path).
54:- **Hot-ion-mode maintenance power** — `truly-unknown` — **blocking** (Li 2024: ~20× fusion power for Ti/Te = 4 at Ti = 150 keV → Q_engineering deeply negative).
55:- **Direct energy converter design and efficiency** — `truly-unknown` — **blocking** (central economic-case dependency; no published design).
56:- **ECRH recirculating power at commercial scale** — `truly-unknown` — **blocking** (depends on commercial plasma current; ~30–50% of gross plausible).
75:- **Direct energy conversion at tokamak scale** — `truly-unknown` — **blocking** (no hardware, no engineering design, no efficiency demonstration).
125:| Commercial plant Q | truly-unknown | blocking |
126:| Fusion power (gross), net electric output | truly-unknown | blocking |
127:| Capital cost (any subsystem) | truly-unknown | blocking |
128:| Direct energy converter efficiency (achieved) | truly-unknown | blocking |
129:| Direct energy converter capital cost | truly-unknown | blocking |
130:| Commercial plasma current | truly-unknown | blocking |
131:| ECRH recirculating power at commercial scale | truly-unknown | blocking |
132:| Hot-ion-mode maintenance power | truly-unknown | blocking |
```

## Blocking-tier lines (new)

```
33:- Plant-level design study — `truly-unknown` (not yet developed; EHL-2 is physics-first) — **blocking**
35:- Any public LCOE or capital cost estimate — `truly-unknown` — **blocking**
57:- Hot-ion mode physics feasibility at ignition temperatures — `truly-unknown` (contested; no experimental precedent above ~1 keV for p-B11 plasma) — **blocking**
58:- Direct energy conversion (DEC) system engineering — `truly-unknown` (conceptual only) — **blocking**
81:- p-B11 burning plasma demonstration — `truly-unknown` (decade+ away; EHL-2 is only step 2 of a multi-step roadmap) — **blocking**
82:- Alpha-particle DEC device — `truly-unknown` for this specific application — **blocking**
127:| Fusion power output (commercial plant) | truly-unknown | blocking | No plant study; EHL-2 is non-power |
128:| Net electrical output | truly-unknown | blocking | No plant design |
129:| Capital cost — any subsystem | truly-unknown | blocking | No plant study or estimate exists |
130:| O&M cost | truly-unknown | blocking | No plant design basis |
131:| Direct conversion efficiency | truly-unknown | blocking | DEC system not designed; alpha from p-B11 at 2.9 MeV each |
132:| Capacity factor / availability | truly-unknown | blocking | No plant design basis |
133:| Fusion Q (commercial target) | truly-unknown | blocking | EHL-2 is gain-negative by design |
134:| Recirculating power fraction | derivable (partial) | blocking | Depends on DEC efficiency and heating power — no target plant parameters |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/39-spherical-tokamak-cs-free-p-b11.md	2026-05-22 09:21:13.891579046 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/39-spherical-tokamak-cs-free-p-b11/gap_report.md	2026-05-22 11:34:17.378820433 -0700
@@ -1,61 +1,63 @@
-# Gap Assessment: Spherical Tokamak - CS-free p-B11 (ENN Energy)
+Now I have all the material I need. Let me write the gap assessment.
 
-## Overall Readiness
-**Rating**: Significant Gaps
+---
 
-**Summary**: ENN Energy has published two peer-reviewed papers on its concept (arXiv:2401.11338 in *Phys. Plasmas* 31, 062507, 2024; and the EHL-2 physics design overview in *Plasma Science and Technology*), plus EXL-50 ECRH current drive results in arXiv:2104.14844. Experimental devices (EXL-50U operating; EHL-2 in design) provide concrete plasma-physics-program data. However, the published material describes a *physics verification* program — EHL-2 targets Ti ≈ 30 keV, ~10× below the >100 keV needed for net p-B11 fusion power. No commercial plant design point exists. Two fundamental physics gates remain unresolved by published evidence: (1) whether p-B11 ignition is achievable in a thermal tokamak at all, with a quantified critique by Li (2024) finding that the required hot-ion-mode Ti/Te = 4 is "far from accessible" under self-heating (would require external heating ~20× fusion power output); and (2) whether direct energy conversion of the alpha products to electricity — central to the economic case — is engineerable for a tokamak geometry (TRL 1–2, no engineering design published). Without these, an LCOE model is speculative.
+# Gap Assessment: Spherical Tokamak - CS-free p-B11 (p-B11)
+
+## Overall Readiness
+**Rating**: Insufficient Data
+**Summary**: ENN's CS-free p-B11 spherical tokamak is a pre-commercial physics-verification program — no plant study exists, no capital cost estimates have been published, and the central physics requirement (hot-ion mode, Ti/Te ≥ 2–4) is contested in peer review. The available sources document the experimental device (EHL-2) parameters and roadmap intent, but provide essentially nothing for LCOE modeling: no fusion power targets, no energy conversion engineering, no operating cost data, and no scaling assumptions for a commercial plant. The data gap is structural, not a sourcing shortfall.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Partial
+**Coverage**: Poor
 
 **Available**:
-- arXiv:2401.11338 / *Phys. Plasmas* 31, 062507 (2024) — ENN's flagship roadmap paper covering EXL-50U parameters, EHL-2 mission, and the commercial vision.
-- EHL-2 physics design paper (doi:10.1088/2058-6272/ad981a) — device parameters (R₀ ≈ 1.05 m, A ≈ 1.85, B₀ ≈ 3 T, Ip ≈ 3 MA), heating design (17 MW NBI + 6 MW ECRH), target conditions (Ti ≈ 30 keV, Ti/Te ≥ 2).
-- arXiv:2104.14844 — EXL-50 ECRH current drive with ~1 A/W efficiency.
-- arXiv:2406.15495 — Li (2024) comment paper critiquing the hot-ion-mode feasibility.
-- ENN English-language website — high-level commercial strategy statement (direct energy conversion, aneutronic).
-- Adjacent concept: 21-spherical-tokamak-hts (Tokamak Energy ST-E1) provides D-T spherical-tokamak analog for geometry and ECRH efficiency.
+- Peer-reviewed roadmap paper (arXiv 2401.11338 / Phys. Plasmas 31, 062507, 2024): EHL-2 device parameters, physics objectives, heating scheme, timeline
+- EHL-2 physics design overview (PST, doi:10.1088/2058-6272/ad981a): mentioned in dossier; abstract/preview accessible but full PDF not parseable
+- EXL-50 / EXL-50U experimental papers (arXiv 2104.14844; IAEA overview): CS-free ECRH startup demonstration, 1 MA achieved Jan 2024
+- Frontiersin 2026 paper (10.3389/fnuen.2026.1714531): independent p-B11 Lawson criterion analysis (not ENN-specific; general physics modeling)
+- Peer-reviewed critique (arXiv 2406.15495): challenges the feasibility of Ti/Te = 4 hot-ion mode
+- ENN website materials: direct conversion intent stated, TF coil currents, device milestones
 
 **Missing**:
-- Commercial plant design point — no Q value, no fusion power target, no net electric output, no capital cost.
-- Direct energy converter engineering design — no electrostatic decelerator geometry, no inertial collector design, no efficiency target supported by hardware.
-- EHL-2 magnet conductor type (resistive copper inferred for EXL-50U; EHL-2 type not stated).
-- Independent TEA or plant study of ENN's concept.
+- Full-text EHL-2 engineering paper (PDF not extractable)
+- Any published plant-level design or power plant study
+- English-language ENN engineering reports on EHL-2 coil system, power supply, or vacuum vessel
+- Any post-EHL-2 commercial device design or cost estimate
 
 **Gaps**:
-- **No commercial plant design point published** — `truly-unknown` — **blocking** (LCOE inputs are entirely absent; the published material is a physics-verification roadmap, not a plant study).
-- **Direct energy conversion design** — `truly-unknown` — **blocking** (the central economic-case dependency; TRL 1–2).
-- **EHL-2 magnet engineering design** — `not-yet-sourced` — important (PST paper full text not yet ingested).
+- Plant-level design study — `truly-unknown` (not yet developed; EHL-2 is physics-first) — **blocking**
+- Full EHL-2 engineering data (coil, PSU, structure) — `proprietary` / language-barrier — **important**
+- Any public LCOE or capital cost estimate — `truly-unknown` — **blocking**
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Partial — physics is well-discussed in the literature; commercial economics absent.
+**Coverage**: Partial
 
 **Available**:
-- Rider 1997, Nevins 1998, and the Frontiers (2026) paper on p-B11 Lawson criterion establish that net energy production at Te = Ti is impossible across the full 75–500 keV range; net-energy windows exist only for Ti/Te > 1 hot-ion modes.
-- Updated Tentori-Belloni (2023) cross-sections place the minimum Lawson triple product at ~1.5 × 10²² m⁻³s at Ti ≈ 270 keV (Te = 0.25 Ti).
-- Li (2024) quantitatively critiques ENN's Ti/Te = 4 requirement: achievable Ti/Te < 1.5 at Ti = 150 keV under self-heating; external maintenance would cost ~20× fusion power.
-- EHL-2 challenges identified: divertor heat flux >20 MW/m² at low density.
-- Tokamak Energy ST-E1 D-T analog for the geometry and ECRH wall-plug efficiency assumption (~50–55%).
+- The hot-ion mode requirement for p-B11 is well-documented: net energy requires Te < Ti, specifically Te/Ti ≤ 0.5 at Ti ≈ 190–330 keV (Frontiers 2026; arXiv 2406.15495)
+- Critique paper (arXiv 2406.15495) establishes that Ti/Te = 4 is far outside reach under most favorable conditions — heating power requirement would need to be ~20× fusion power at 150 keV
+- Bremsstrahlung loss dominance at Te = Ti is quantified (net energy impossible unless Te << Ti)
+- CS-free startup challenge explicitly identified in roadmap paper
+- EHL-2 targets Ti₀ ≈ 30 keV — far below the 125–190 keV minimum Lawson window for p-B11
 
 **Missing**:
-- ENN's published response to the Li (2024) critique.
-- Engineering path for a tokamak-geometry direct energy converter.
-- Recirculating-power fraction at commercial plant scale (depends on undisclosed commercial plasma current and coil system).
-- Divertor design for all-charged-particle heat flux.
+- Any engineering model of the direct energy conversion system (alpha-particle capture from 3-alpha products at ~2.9 MeV each)
+- Divertor heat flux handling strategy (EHL-2 note: >20 MW/m² at low density — no solution published)
+- Synchrotron radiation loss model (high-field, high-temperature plasma — not addressed in current sources)
+- Wall reflection coefficient requirements for synchrotron recycling (required for p-B11 viability in MCF)
+- Impurity control strategy for boron in plasma
 
 **Gaps**:
-- **p-B11 ignition feasibility in a thermal spherical tokamak** — `truly-unknown` — **blocking** (the most fundamental gap; Li 2024 quantitatively challenges the proposed hot-ion-mode path).
-- **Hot-ion-mode maintenance power** — `truly-unknown` — **blocking** (Li 2024: ~20× fusion power for Ti/Te = 4 at Ti = 150 keV → Q_engineering deeply negative).
-- **Direct energy converter design and efficiency** — `truly-unknown` — **blocking** (central economic-case dependency; no published design).
-- **ECRH recirculating power at commercial scale** — `truly-unknown` — **blocking** (depends on commercial plasma current; ~30–50% of gross plausible).
-- **Divertor solution for all-charged-particle heating** — `truly-unknown` — important (p-B11 puts 100% of fusion energy into the divertor as charged-particle heat — qualitatively more severe than D-T).
-- **Fallback thermal-cycle scenario** — `derivable` from D-T MFE analogs — important (the DEC-failure economic case is the primary go/no-go test the LCOE model should evaluate).
+- Hot-ion mode physics feasibility at ignition temperatures — `truly-unknown` (contested; no experimental precedent above ~1 keV for p-B11 plasma) — **blocking**
+- Direct energy conversion (DEC) system engineering — `truly-unknown` (conceptual only) — **blocking**
+- Divertor solution at >20 MW/m² heat flux — `not-yet-sourced` (active research area but no ENN-specific publication) — **important**
+- Synchrotron/wall-reflection engineering — `truly-unknown` — **important**
 
 ---
 
@@ -63,111 +65,113 @@
 **Coverage**: Partial
 
 **Available**:
-- TRL assessments by subsystem: p-B11 plasma at reactor conditions TRL 1–2; direct energy conversion TRL 1–2 (Venetian-blind LLNL 1970s, mirror-machine geometry); CS-free non-inductive current drive TRL 3–4 (EXL-50 demonstrated, EHL-2 will scale); ST plasma confinement at Ti/Te >> 1 TRL 2–3; divertor at p-B11 conditions TRL 3–4; ECRH/NBI heating TRL 5–7 (mature at EHL-2 scale); ST vacuum vessel + resistive copper magnets TRL 5–6 (EHL-2 level).
-- EXL-50U operates at 1 MA / 1.2 T with 150 kA TF coil current — concrete data point for resistive-magnet ST engineering.
+- CS-free ECRH startup: demonstrated at 1 MA on EXL-50U (TRL ~4) — well-documented
+- NBI at 17 MW: standard fusion engineering, well-developed technology (TRL ~7–8 for comparable devices)
+- ECRH at 6 MW: mature heating technology (TRL ~7–8)
+- Spherical tokamak plasma physics: broad base from START, MAST, NSTX — applicable framework
+- Resistive magnets at EXL-50U scale: proven technology (TRL ~8)
 
 **Missing**:
-- Any ST plasma data at Ti > 30 keV.
-- DEC hardware for tokamak geometry.
-- HTS magnet transition for ENN's commercial plant (not announced; resistive copper has prohibitive recirculating power at reactor scale).
+- p-B11 burning plasma physics: EHL-2 targets 30 keV (vs. 150–300 keV needed) — no burning plasma experiment exists or is planned in this roadmap. TRL ~1–2.
+- Direct energy conversion for 2.9 MeV alpha particles: no device demonstrated at any scale for this specific application. TRL ~1–2.
+- High-temperature divertor for low-density ST: unsolved engineering challenge
+- Commercial power plant magnets: type not confirmed; if copper resistive, large recirculating power penalty at plant scale
 
 **Gaps**:
-- **Direct energy conversion at tokamak scale** — `truly-unknown` — **blocking** (no hardware, no engineering design, no efficiency demonstration).
-- **Commercial-scale magnet conductor decision** — `truly-unknown` — important (resistive copper → ~300 MW ohmic loss at ITER-scale current; HTS transition unannounced).
-- **Divertor materials for combined alpha + radiation heat flux** — `not-yet-sourced` — important.
+- p-B11 burning plasma demonstration — `truly-unknown` (decade+ away; EHL-2 is only step 2 of a multi-step roadmap) — **blocking**
+- Alpha-particle DEC device — `truly-unknown` for this specific application — **blocking**
+- EHL-2 magnet conductor specification — `proprietary` / `not-yet-sourced` — **important** (low criticality for full analysis but needed for recirculating power estimates)
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Good
+**Coverage**: Poor
 
 **Available**:
-- Boron-11: natural boron is ~80% ¹¹B, global production ~10 Mt/yr. Isotopic enrichment to >95% ¹¹B is industrially feasible (¹⁰B enrichment is mature for fission control rods).
-- No tritium / FLiBe / Li-6 / beryllium required — major structural supply-chain advantage relative to D-T MFE concepts.
-- Copper coils: unconstrained supply.
-- ECRH gyrotrons at ITER class (1 MW CW): commercially available.
-- HTS REBCO (if ENN transitions): same supply chain as 21-spherical-tokamak-hts (Tokamak Energy); production capacity is the bottleneck for any HTS-based fusion fleet.
+- p-B11 fuel cycle: no tritium required — major supply chain simplification (confirmed)
+- Natural boron is ~80% B-11 (vs. 20% B-10) — isotopic separation required but manageable relative to Li-6 enrichment for D-T
+- No HTS magnets identified (resistive copper inferred) — avoids REBCO tape supply concerns
 
 **Missing**:
-- Quantitative ¹¹B enrichment demand at plant scale.
-- HTS supply commitment from ENN (none announced; concept currently uses resistive copper).
+- Boron-11 enrichment scale and cost for a commercial plant (no published estimate)
+- Fuel injection and recycling system for boron in plasma (undesigned)
+- First wall and plasma-facing component materials for p-B11 reactor (no neutron activation, but alpha bombardment and erosion still relevant)
+- Balance of plant materials for DEC system (undesigned)
+- Manufacturing process for any novel DEC hardware
 
 **Gaps**:
-- ¹¹B enrichment demand at plant scale — `derivable` once plant design exists — nice-to-have.
-- ENN HTS supply agreement — `not-yet-sourced` (and may not exist; copper magnets unrealistic at reactor scale) — important.
+- B-11 enrichment supply chain at plant scale — `not-yet-sourced` (isotope enrichment literature exists; not captured for this concept) — **important**
+- DEC hardware materials and supply chain — `truly-unknown` (system not designed) — **important**
+- First wall / PFC materials specification — `truly-unknown` for p-B11 commercial plant — **nice-to-have** at this stage
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Available Parameters**:
+**Coverage**: Poor
 
-| Parameter | Value | Source | Confidence |
-|---|---|---|---|
-| EHL-2 R₀ | ~1.05 m | dossier, roadmap paper | high |
-| EHL-2 A (aspect ratio) | ~1.85 | dossier | high |
-| EHL-2 B₀ | ~3 T | dossier | high |
-| EHL-2 Ip | ~3 MA | roadmap paper | high |
-| EHL-2 heating | 17 MW NBI + 6 MW ECRH | dossier | high |
-| EHL-2 target Ti | ~30 keV | roadmap paper | high |
-| EHL-2 Ti/Te target | ≥2 | roadmap paper | high |
-| EXL-50U Ip / B₀ | 1 MA / 1.2 T | dossier | high |
-| ECRH current drive efficiency (EXL-50) | ~1 A/W | dossier | medium |
-| p-B11 peak cross-section energy | ~650 keV CM (~ 10× D-T) | nuclear physics | high |
-| p-B11 minimum Lawson (Te = 0.25 Ti) | ~1.5 × 10²² m⁻³s at Ti ≈ 270 keV | Frontiers (2026) | high |
-| Hot ion mode Ti/Te achievable under self-heating | < 1.5 at Ti = 150 keV | Li (2024) | high |
-| Theoretical DEC efficiency | 70–90% | DEC literature (upper bound) | low |
-| Operation mode | Steady-state | dossier | high |
+**Available Parameters**:
+| Parameter | Value/Range | Source | Confidence |
+|-----------|-------------|--------|------------|
+| Major radius (EHL-2) | 1.05 m | arXiv 2401.11338 | h |
+| Toroidal field (EHL-2) | 3 T | arXiv 2401.11338 | h |
+| Plasma current (EHL-2) | 3 MA | arXiv 2401.11338 | h |
+| Target ion temperature | 30 keV (EHL-2 goal) | arXiv 2401.11338 | h |
+| Heating power (EHL-2) | 23 MW (17 NBI + 6 ECRH) | arXiv 2401.11338 | h |
+| Minimum ignition triple product (p-B11) | ~1.3×10²² m⁻³s (no rad losses) to ~1.2×10²³ m⁻³s (Te=0.5Ti) | Frontiers 2026 | m |
+| Required Ti for net energy (Te=0.5Ti) | 190–330 keV | Frontiers 2026 | m |
+| Energy capture intent | Direct (charged particle) | ENN website; arXiv 2401.11338 | m |
 
 **Missing Parameters**:
-
-| Parameter | Gap Type | Criticality |
-|---|---|---|
-| Commercial plant Q | truly-unknown | blocking |
-| Fusion power (gross), net electric output | truly-unknown | blocking |
-| Capital cost (any subsystem) | truly-unknown | blocking |
-| Direct energy converter efficiency (achieved) | truly-unknown | blocking |
-| Direct energy converter capital cost | truly-unknown | blocking |
-| Commercial plasma current | truly-unknown | blocking |
-| ECRH recirculating power at commercial scale | truly-unknown | blocking |
-| Hot-ion-mode maintenance power | truly-unknown | blocking |
-| Capacity factor | truly-unknown | important |
-| Power conversion cycle thermal efficiency (DEC failure case) | not-yet-sourced | important |
-| Commercial magnet type | truly-unknown | important |
+| Parameter | Gap Type | Criticality | Notes |
+|-----------|----------|-------------|-------|
+| Fusion power output (commercial plant) | truly-unknown | blocking | No plant study; EHL-2 is non-power |
+| Net electrical output | truly-unknown | blocking | No plant design |
+| Capital cost — any subsystem | truly-unknown | blocking | No plant study or estimate exists |
+| O&M cost | truly-unknown | blocking | No plant design basis |
+| Direct conversion efficiency | truly-unknown | blocking | DEC system not designed; alpha from p-B11 at 2.9 MeV each |
+| Capacity factor / availability | truly-unknown | blocking | No plant design basis |
+| Fusion Q (commercial target) | truly-unknown | blocking | EHL-2 is gain-negative by design |
+| Recirculating power fraction | derivable (partial) | blocking | Depends on DEC efficiency and heating power — no target plant parameters |
+| Balance of plant cost | derivable (analog) | important | D-T MFE analog possible; concept-specific BOP unknown |
+| Magnet system cost | derivable (analog) | important | Resistive coil analog available; conductor type unconfirmed |
+| B-11 fuel cost | not-yet-sourced | important | Isotope pricing literature exists, not captured |
+| Maintenance / replacement schedule | truly-unknown | important | No commercial device design |
 
 ---
 
 ## Source Recommendations
 
-1. **EHL-2 PST paper full text** (doi:10.1088/2058-6272/ad981a) — should be ingested to confirm magnet conductor and detailed engineering design.
-2. **ENN response (if any) to Li (2024) critique** — would clarify ENN's position on the hot-ion-mode feasibility.
-3. **Rider (1997) and Nevins (1998) papers** — the foundational analyses of p-B11 Lawson criterion; should be formally ingested as sources.
-4. **ARIES-ST plant study** — D-T spherical-tokamak commercial design analog; provides geometry and BoP cost-structure baselines.
-5. **Comparable Chinese state fusion program filings** — ENN is a private subsidiary of a state-adjacent conglomerate; if ENN files for national R&D program funding, milestone details may enter the public domain.
-6. **Tokamak Energy ST-E1 analysis** (21-spherical-tokamak-hts) — the most direct D-T cross-reference for ECRH efficiency, ST geometry, and HTS supply chain.
+1. **EHL-2 full engineering paper** (doi:10.1088/2058-6272/ad981a, Plasma Sci. Technol.) — magnet system, vacuum vessel, power supply — `not-yet-sourced`. PDF extraction failed in iter-02; retry with agentic-mbse or docling. This is the highest-priority concept-scoped source not yet captured.
 
----
+2. **p-B11 direct energy conversion literature** — search OSTI and arXiv for "proton-boron direct energy conversion," "aneutronic fusion energy capture," "alpha particle electrostatic converter." Lawrenceville Plasma Physics (Focus Fusion) has published on DEC for p-B11; `not-yet-sourced` — `unverified — confirm existence before searching`.
 
-## Summary
+3. **EXL-50U strategy and experimental progress paper** (doi:10.1088/2058-6272/ad9e8f) — listed in dossier key sources but not extracted. Contains EXL-50U current status relevant to EHL-2 readiness assessment; `not-yet-sourced`.
+
+4. **Boron isotope enrichment supply chain** — search for B-11 isotope production, electromagnetic separation costs; IAEA isotope production reports. `not-yet-sourced` — `unverified — confirm existence before searching`.
 
-**Proceed to full analysis**: Yes, with significant caveats.
+5. **Fleet-wide cost analogs** — `knowledge/sources/tea_dt_mfe_cost_analysis/` and `knowledge/sources/aries_cost_account_documentation/` are applicable for BOP, indirect costs, and CAS framework, but cannot fill any concept-specific gap. Use only as methodology scaffolding. No additional fleet-wide source is likely to be concept-specific.
 
-ENN's concept is the only p-B11 spherical tokamak in the catalog, and its published material is enough to define the device geometry, fuel cycle, and high-level commercial strategy. A *speculative-placeholder* LCOE model is buildable: 500 MWe / 1 GWe scaling cases under the assumption that p-B11 ignition and direct energy conversion are achievable, producing rough $/MWh estimates (analyst placeholder ~96 $/MWh at 500 MWe, ~61 $/MWh at 1 GWe). These should be reported as best-case bounds, not forecasts.
+6. **Critique paper full text** (arXiv 2406.15495) — only abstract captured. Full PDF would provide quantitative bounds on heating power requirements for hot-ion mode — important for characterizing the physics uncertainty. `not-yet-sourced`.
+
+---
+
+## Summary
 
-The dominant LCOE-relevant gaps are not engineering uncertainties — they are physics go/no-go gates: (1) can a thermal spherical tokamak achieve p-B11 ignition at all, given Li (2024)'s analysis that the required hot-ion mode is infeasible under self-heating? and (2) can direct energy conversion at the tokamak geometry actually be engineered? If either gate fails, the entire LCOE case collapses regardless of magnet type or BoP cost. The model should explicitly include a DEC-failure scenario (alpha power routed through a fallback thermal cycle at η ≈ 0.35) and a hot-ion-mode-heating-multiplier scenario (1× → 20×) to characterize the boundary of viability.
+**Proceed to full analysis or acquire more sources first?** The gap is structural, not a sourcing problem. ENN has not published a commercial plant design, capital cost estimates, or DEC engineering — because those things do not yet exist. No additional source retrieval will fill the LCOE parameter table in any meaningful way. A D1+ analysis is feasible as a qualitative and physics-framing exercise (data availability rating, system function challenges, TRL by subsystem), but the quantitative LCOE model will be almost entirely built on analogues and assumptions rather than concept-specific data. Flag this explicitly in the write-up: this concept is too early-stage for a grounded LCOE estimate, and the primary analysis value is in characterizing the physics risk stack (hot-ion mode feasibility, DEC development gap, bremsstrahlung problem) rather than producing a number.
 
 ---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Significant Gaps"
-blocking_count: 8
-important_count: 3
-counting_method: "section_5_missing_parameters"
+overall_rating: "Insufficient Data"
+blocking_count: 7
+important_count: 5
+counting_method: "deduplicated_across_all_sections — blocking: (1) no plant study/capital cost data, (2) DEC system undesigned (energy conversion), (3) hot-ion mode physics contested/undemonstrated, (4) p-B11 burning plasma TRL ~1, (5) fusion Q/power output unknown, (6) capacity factor unknown, (7) recirculating power unknown. Important: (1) EHL-2 magnet conductor unconfirmed, (2) divertor/heat flux solution absent, (3) B-11 enrichment supply chain, (4) DEC hardware materials, (5) O&M/maintenance schedule"
 section_coverage:
-  availability_of_data:       "Partial"
-  system_function:            "Partial — physics is well-discussed in the literature; commercial economics absent."
+  availability_of_data:       "Poor"
+  system_function:            "Partial"
   subsystem_maturity:         "Partial"
-  materials_supply_chain:     "Good"
-  lcoe_parameter_extraction:  "Unknown"
-```
+  materials_supply_chain:     "Poor"
+  lcoe_parameter_extraction:  "Poor"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
