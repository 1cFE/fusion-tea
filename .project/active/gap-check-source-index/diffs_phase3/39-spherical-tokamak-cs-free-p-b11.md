# Phase 3 diff: 39-spherical-tokamak-cs-free-p-b11

**Generated:** 2026-05-22T16:30:13-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 7 | 8 | 1 |
| important_count  | 5 | 6 | - |
| overall_rating   | Insufficient Data | Insufficient Data | - |

## Fleet-source dispositions in new report

```
```

## Forbidden-phrase check (should be empty)

```
1:I now have sufficient information from all relevant sources. Let me write the assessment.
```

## First line of new report (should start with `# Gap Assessment`)

```
I now have sufficient information from all relevant sources. Let me write the assessment.
```

## Blocking-tier lines (new)

```
30:- No commercial plant study exists — proprietary (ENN may be developing internal roadmaps) + not-yet-sourced (no indication published) — **blocking**
52:- Hot-ion mode physics feasibility (Ti/Te >> 1) is actively contested — will require experimental resolution; cannot be assumed for economic modeling — truly-unknown — **blocking**
53:- DEC technology: no published engineering design, efficiency unknown — truly-unknown — **blocking**
54:- Divertor engineering solution at 20+ MW/m² in a low-density p-B11 plasma — truly-unknown — **blocking**
76:- p-B11 plasma at required temperatures (Ti ~ 100-300 keV with Ti/Te >> 1): no experimental precedent anywhere — truly-unknown — **blocking**
77:- DEC at relevant alpha energies: TRL 1-2, no power-plant-scale design — truly-unknown — **blocking**
130:| Net electrical output (MWe) | truly-unknown | blocking | No power plant design exists; EHL-2 is experimental |
131:| Engineering gain Q (Qeng) | truly-unknown | blocking | Physics verification has not begun; required Lawson criterion not yet approached |
132:| Energy conversion efficiency (DEC) | truly-unknown | blocking | DEC technology unspecified; theoretical efficiency 60-90% cited for alpha capture but no design exists |
133:| Capacity factor / availability | truly-unknown | blocking | No basis for estimate without operational device or design |
134:| Capital cost by CAS account | derivable (rough D-T analog only) | blocking | BOP and structures can be estimated from D-T analog; power conversion (DEC) and first-wall systems cannot |
135:| O&M cost (annual) | derivable (rough analog) | blocking | No concept-specific basis; D-T analogs available but power conversion system is fundamentally different |
137:| Recirculating power fraction | truly-unknown | blocking | Heating efficiency and recirculation requirements at power-plant scale not defined |
139:| Plant thermal power (MWth) | truly-unknown | blocking | No net-power design; EHL-2 is non-power |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/39-spherical-tokamak-cs-free-p-b11.md	2026-05-22 12:59:21.093948665 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/39-spherical-tokamak-cs-free-p-b11/gap_report.md	2026-05-22 16:30:13.859672341 -0700
@@ -1,14 +1,10 @@
-Now I have all the material I need. Let me write the gap assessment.
-
----
+I now have sufficient information from all relevant sources. Let me write the assessment.
 
 # Gap Assessment: Spherical Tokamak - CS-free p-B11 (p-B11)
 
 ## Overall Readiness
 **Rating**: Insufficient Data
-**Summary**: ENN's CS-free p-B11 spherical tokamak is a pre-commercial physics-verification program — no plant study exists, no capital cost estimates have been published, and the central physics requirement (hot-ion mode, Ti/Te ≥ 2–4) is contested in peer review. The available sources document the experimental device (EHL-2) parameters and roadmap intent, but provide essentially nothing for LCOE modeling: no fusion power targets, no energy conversion engineering, no operating cost data, and no scaling assumptions for a commercial plant. The data gap is structural, not a sourcing shortfall.
-
----
+**Summary**: ENN's CS-free p-B11 spherical tokamak concept is at TRL ~2: EHL-2 (the next device) remains under construction and targets physics verification, not power production. No power plant design, blanket, energy conversion system, or economic data has been published. The physics basis for the critical hot-ion mode (Ti/Te >> 1) required for p-B11 net energy is actively contested in peer-reviewed literature. While the device parameters and roadmap are well-documented, the concept cannot support a quantitative LCOE analysis in its current state — a qualitative feasibility and challenge assessment is possible, but only the physics-challenge and subsystem-TRL sections can be populated with meaningful specificity.
 
 ## Section Coverage
 
@@ -16,23 +12,23 @@
 **Coverage**: Poor
 
 **Available**:
-- Peer-reviewed roadmap paper (arXiv 2401.11338 / Phys. Plasmas 31, 062507, 2024): EHL-2 device parameters, physics objectives, heating scheme, timeline
-- EHL-2 physics design overview (PST, doi:10.1088/2058-6272/ad981a): mentioned in dossier; abstract/preview accessible but full PDF not parseable
-- EXL-50 / EXL-50U experimental papers (arXiv 2104.14844; IAEA overview): CS-free ECRH startup demonstration, 1 MA achieved Jan 2024
-- Frontiersin 2026 paper (10.3389/fnuen.2026.1714531): independent p-B11 Lawson criterion analysis (not ENN-specific; general physics modeling)
-- Peer-reviewed critique (arXiv 2406.15495): challenges the feasibility of Ti/Te = 4 hot-ion mode
-- ENN website materials: direct conversion intent stated, TF coil currents, device milestones
+- ENN roadmap (arXiv:2401.11338 / Phys. Plasmas 31, 062507, 2024): EHL-2 device parameters (R₀ ≈ 1.05 m, A ≈ 1.85, B₀ ≈ 3 T, Ip ≈ 3 MA, Ti0 ≈ 30 keV target), heating system (17 MW NBI + 6 MW ECRH), CS-free startup approach, and a multi-step roadmap toward a burning plasma device.
+- EHL-2 physics design overview (PST, doi:10.1088/2058-6272/ad981a): magnet/vacuum vessel geometry, heat flux estimates (~20 MW/m² at divertor at low density).
+- EXL-50U experimental results (ENN Research site): 1 MA plasma current at 1.2 T, TF coils at 150 kA — the predecessor device milestone.
+- Peer-reviewed physics critique (arXiv:2406.15495, Li & Zhi 2024): argues the required Ti/Te = 4 hot-ion mode is inaccessible under physically achievable conditions.
+- Independent Lawson criterion analysis (Frontiers in Nuclear Engineering, Ahmad et al. 2026): quantifies net-energy conditions for p-B11 — only achievable at Ti ≥ 125–190 keV with Te/Ti ≤ 0.5, minimum Lawson parameter 1.3×10²² – 1.2×10²³ m⁻³s.
+- ENN website disclosures: explicit intent for direct energy conversion as the commercial capture pathway; no engineering design provided.
 
 **Missing**:
-- Full-text EHL-2 engineering paper (PDF not extractable)
-- Any published plant-level design or power plant study
-- English-language ENN engineering reports on EHL-2 coil system, power supply, or vacuum vessel
-- Any post-EHL-2 commercial device design or cost estimate
+- Any published power plant design, system study, or commercial reactor concept.
+- Plant-level performance parameters (net Q, gross/net electric output, recirculating power fraction).
+- Any cost or economic analysis.
+- Detailed English-language coil engineering paper for EHL-2 (conductor type, current density, structural design).
+- Post-EHL-2 roadmap with design parameters for the next-stage burning plasma device.
 
 **Gaps**:
-- Plant-level design study — `truly-unknown` (not yet developed; EHL-2 is physics-first) — **blocking**
-- Full EHL-2 engineering data (coil, PSU, structure) — `proprietary` / language-barrier — **important**
-- Any public LCOE or capital cost estimate — `truly-unknown` — **blocking**
+- No commercial plant study exists — proprietary (ENN may be developing internal roadmaps) + not-yet-sourced (no indication published) — **blocking**
+- EHL-2 engineering detail limited; Chinese-language technical reports likely contain more specifics — not-yet-sourced — **important**
 
 ---
 
@@ -40,24 +36,23 @@
 **Coverage**: Partial
 
 **Available**:
-- The hot-ion mode requirement for p-B11 is well-documented: net energy requires Te < Ti, specifically Te/Ti ≤ 0.5 at Ti ≈ 190–330 keV (Frontiers 2026; arXiv 2406.15495)
-- Critique paper (arXiv 2406.15495) establishes that Ti/Te = 4 is far outside reach under most favorable conditions — heating power requirement would need to be ~20× fusion power at 150 keV
-- Bremsstrahlung loss dominance at Te = Ti is quantified (net energy impossible unless Te << Ti)
-- CS-free startup challenge explicitly identified in roadmap paper
-- EHL-2 targets Ti₀ ≈ 30 keV — far below the 125–190 keV minimum Lawson window for p-B11
+- Hot-ion mode feasibility is the central physics challenge: the Frontiersin paper (Ahmad et al. 2026) establishes that net energy requires Te/Ti ≤ 0.5 at Ti = 190–330 keV, or Te/Ti ≤ 0.25 for a wider window. The Li & Zhi comment (arXiv:2406.15495) argues that even under the most optimistic heating assumptions, Ti/Te < 1.5 is realistic (not 4 as ENN's roadmap assumes), and that achieving Ti/Te = 4 by external heating would require ~20× fusion power in heating input — making the system economically nonsensical.
+- CS-free startup challenge is well-documented: the central solenoid provides very limited volt-seconds; non-inductive ECRH ramp-up to MA-scale currents is identified as the key engineering bet. EXL-50 demonstrated ~1 A/W ECRH current drive efficiency.
+- Bremsstrahlung dominance: at Te = Ti, the bremsstrahlung radiation rate exceeds the p-B11 fusion energy rate across the full 75–500 keV range (Ahmad et al. 2026, Fig. 2). The high effective charge of the p-B11 mixture (Zeff ~ 2.4) amplifies this.
+- Divertor heat flux: EHL-2 physics paper notes ~20 MW/m² target heat flux at low density, which is at or beyond current tokamak divertor limits. The engineering solution is not specified.
+- Direct energy conversion (DEC): ENN's commercial strategy depends on capturing charged alpha particles from p-B11 (3 alphas, ~8.68 MeV total). No DEC engineering design has been published; the technology is exploratory.
 
 **Missing**:
-- Any engineering model of the direct energy conversion system (alpha-particle capture from 3-alpha products at ~2.9 MeV each)
-- Divertor heat flux handling strategy (EHL-2 note: >20 MW/m² at low density — no solution published)
-- Synchrotron radiation loss model (high-field, high-temperature plasma — not addressed in current sources)
-- Wall reflection coefficient requirements for synchrotron recycling (required for p-B11 viability in MCF)
-- Impurity control strategy for boron in plasma
+- Engineering solution for divertor/plasma-facing components at p-B11 conditions (high temperature, high alpha flux, low density).
+- Assessment of plasma-wall interactions with boron-containing plasma.
+- Alpha particle energy deposition and confinement analysis for a power-plant-scale device.
+- Specific DEC technology selection and efficiency projections.
 
 **Gaps**:
-- Hot-ion mode physics feasibility at ignition temperatures — `truly-unknown` (contested; no experimental precedent above ~1 keV for p-B11 plasma) — **blocking**
-- Direct energy conversion (DEC) system engineering — `truly-unknown` (conceptual only) — **blocking**
-- Divertor solution at >20 MW/m² heat flux — `not-yet-sourced` (active research area but no ENN-specific publication) — **important**
-- Synchrotron/wall-reflection engineering — `truly-unknown` — **important**
+- Hot-ion mode physics feasibility (Ti/Te >> 1) is actively contested — will require experimental resolution; cannot be assumed for economic modeling — truly-unknown — **blocking**
+- DEC technology: no published engineering design, efficiency unknown — truly-unknown — **blocking**
+- Divertor engineering solution at 20+ MW/m² in a low-density p-B11 plasma — truly-unknown — **blocking**
+- Bremsstrahlung mitigation strategy beyond hot-ion mode remains speculative — truly-unknown — **important**
 
 ---
 
@@ -65,22 +60,23 @@
 **Coverage**: Partial
 
 **Available**:
-- CS-free ECRH startup: demonstrated at 1 MA on EXL-50U (TRL ~4) — well-documented
-- NBI at 17 MW: standard fusion engineering, well-developed technology (TRL ~7–8 for comparable devices)
-- ECRH at 6 MW: mature heating technology (TRL ~7–8)
-- Spherical tokamak plasma physics: broad base from START, MAST, NSTX — applicable framework
-- Resistive magnets at EXL-50U scale: proven technology (TRL ~8)
+- CS-free spherical tokamak plasma: EXL-50U demonstrated 1 MA / 1.2 T with ECRH-only current drive (TRL ~3-4 for this specific capability). EHL-2 targeting 3 MA / 3 T — a significant scale-up not yet demonstrated.
+- NBI heating: 17 MW NBI for EHL-2 is demanding but within range of existing neutral beam technology. Mature at this scale (TRL ~6 for NBI subsystem).
+- ECRH current drive: demonstrated at ~1 A/W efficiency on EXL-50 (TRL ~4 for this application).
+- Resistive (copper) magnets: EXL-50U TF at 150 kA / 1.2 T is consistent with copper Bitter-plate coils. EHL-2 at 3 T / 1.05 m is within copper-coil range. TRL ~5-6 for the magnet subsystem if copper.
+- p-B11 fuel cycle basics: proton (hydrogen) + boron-11 fuel is well-characterized as chemistry; no tritium breeding needed (simplification vs. D-T). No fuel cycle engineering for a power plant exists.
 
 **Missing**:
-- p-B11 burning plasma physics: EHL-2 targets 30 keV (vs. 150–300 keV needed) — no burning plasma experiment exists or is planned in this roadmap. TRL ~1–2.
-- Direct energy conversion for 2.9 MeV alpha particles: no device demonstrated at any scale for this specific application. TRL ~1–2.
-- High-temperature divertor for low-density ST: unsolved engineering challenge
-- Commercial power plant magnets: type not confirmed; if copper resistive, large recirculating power penalty at plant scale
+- TRL assessment for direct energy conversion (DEC) at relevant alpha-particle energies (~2.9 MeV per alpha). Electrostatic DEC exists in theoretical literature; prototype demonstrations are at TRL 2-3 at most.
+- Plasma performance at power-plant-relevant Ti (100-300 keV) in any device — not yet approached (EHL-2 targets 30 keV, a factor of ~5-10 below what is needed for net energy).
+- EHL-2 coil engineering: conductor type (copper vs HTS) not definitively stated in public English-language sources.
+- Long-pulse/steady-state operation assessment.
 
 **Gaps**:
-- p-B11 burning plasma demonstration — `truly-unknown` (decade+ away; EHL-2 is only step 2 of a multi-step roadmap) — **blocking**
-- Alpha-particle DEC device — `truly-unknown` for this specific application — **blocking**
-- EHL-2 magnet conductor specification — `proprietary` / `not-yet-sourced` — **important** (low criticality for full analysis but needed for recirculating power estimates)
+- p-B11 plasma at required temperatures (Ti ~ 100-300 keV with Ti/Te >> 1): no experimental precedent anywhere — truly-unknown — **blocking**
+- DEC at relevant alpha energies: TRL 1-2, no power-plant-scale design — truly-unknown — **blocking**
+- EHL-2 magnet conductor type unconfirmed — not-yet-sourced (EHL-2 coil paper likely exists in Chinese literature) — **important**
+- CS-free current drive scalability to power-plant plasma currents (>10 MA) — truly-unknown — **important**
 
 ---
 
@@ -88,21 +84,22 @@
 **Coverage**: Poor
 
 **Available**:
-- p-B11 fuel cycle: no tritium required — major supply chain simplification (confirmed)
-- Natural boron is ~80% B-11 (vs. 20% B-10) — isotopic separation required but manageable relative to Li-6 enrichment for D-T
-- No HTS magnets identified (resistive copper inferred) — avoids REBCO tape supply concerns
+- p-B11 fuel: Natural boron is ~80% ¹¹B / 20% ¹⁰B by abundance. Some isotope enrichment is needed but the starting isotopic fraction is favorable. Proton fuel (hydrogen) is abundant and straightforward.
+- No tritium breeding required (aneutronic): eliminates lithium blanket supply chain, tritium processing infrastructure, and associated cost and regulatory overhead — a significant simplification vs. D-T.
+- Copper coils (if confirmed): copper supply chain is mature; no exotic materials expected for resistive magnets at this scale.
+- Low neutron flux: structural material activation is greatly reduced vs. D-T; first-wall replacement cycle expected to be much less frequent.
 
 **Missing**:
-- Boron-11 enrichment scale and cost for a commercial plant (no published estimate)
-- Fuel injection and recycling system for boron in plasma (undesigned)
-- First wall and plasma-facing component materials for p-B11 reactor (no neutron activation, but alpha bombardment and erosion still relevant)
-- Balance of plant materials for DEC system (undesigned)
-- Manufacturing process for any novel DEC hardware
+- Boron-11 enrichment cost and supply chain at commercial scale (no published analysis found in Phase 1a sources).
+- First-wall/plasma-facing material selection for high-temperature, high-alpha-flux, low-neutron p-B11 conditions.
+- DEC component materials (high-voltage electrodes, particle collectors at MeV energies) — not yet defined.
+- Alpha particle management at 8.68 MeV: helium ash exhaust strategy in steady-state operation.
 
 **Gaps**:
-- B-11 enrichment supply chain at plant scale — `not-yet-sourced` (isotope enrichment literature exists; not captured for this concept) — **important**
-- DEC hardware materials and supply chain — `truly-unknown` (system not designed) — **important**
-- First wall / PFC materials specification — `truly-unknown` for p-B11 commercial plant — **nice-to-have** at this stage
+- Boron-11 enrichment supply chain and cost at power-plant scale: no published analysis — not-yet-sourced — **important**
+- First-wall material specification for p-B11 plasma conditions (alpha bombardment, no neutron breeding driver) — not-yet-sourced — **important**
+- DEC component materials and manufacturing — truly-unknown — **important**
+- Helium ash exhaust design (alpha particles accumulate in steady-state plasma) — truly-unknown — **important**
 
 ---
 
@@ -112,62 +109,84 @@
 **Available Parameters**:
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Major radius (EHL-2) | 1.05 m | arXiv 2401.11338 | h |
-| Toroidal field (EHL-2) | 3 T | arXiv 2401.11338 | h |
-| Plasma current (EHL-2) | 3 MA | arXiv 2401.11338 | h |
-| Target ion temperature | 30 keV (EHL-2 goal) | arXiv 2401.11338 | h |
-| Heating power (EHL-2) | 23 MW (17 NBI + 6 ECRH) | arXiv 2401.11338 | h |
-| Minimum ignition triple product (p-B11) | ~1.3×10²² m⁻³s (no rad losses) to ~1.2×10²³ m⁻³s (Te=0.5Ti) | Frontiers 2026 | m |
-| Required Ti for net energy (Te=0.5Ti) | 190–330 keV | Frontiers 2026 | m |
-| Energy capture intent | Direct (charged particle) | ENN website; arXiv 2401.11338 | m |
+| Major radius (R₀) | 1.05 m (EHL-2) | arXiv:2401.11338 | high |
+| Toroidal field (B₀) | 3 T (EHL-2) | arXiv:2401.11338 | high |
+| Plasma current (Ip) | 3 MA (EHL-2 target) | arXiv:2401.11338 | high |
+| Ion temperature target (Ti0) | 30 keV (EHL-2 physics phase) | arXiv:2401.11338 | high |
+| Required Ti for net energy | 125–330 keV (depending on Te/Ti) | Frontiersin (Ahmad et al. 2026) | medium |
+| Heating power (EHL-2) | 23 MW (17 NBI + 6 ECRH) | arXiv:2401.11338 | high |
+| Energy capture mode | Direct (charged particle) — intent only | ENN website; arXiv:2401.11338 | medium |
+| Magnet type | Resistive (copper inferred) | EXL-50U datapoints | low |
+| Fuel | p-B11 (aneutronic) | arXiv:2401.11338 | high |
+| D-T tokamak LCOE analog | $140–550/MWh | TEA D-T MFE (knowledge/sources/tea_dt_mfe_cost_analysis/) | low analog |
+| D-T tokamak capital cost analog | $8,800–22,200/kW (350 MWe plant) | TEA D-T MFE | low analog |
+| ARIES-ST blanket cost analog | ~$155.7M (LiPb+He, D-T blanket) | ARIES Cost Account (knowledge/sources/aries_cost_account_documentation/) | low analog |
+
+*Note on fleet-wide analogs: The D-T MFE TEA and ARIES-ST cost data are methodology references only. p-B11 eliminates the blanket/tritium system (removing a major cost driver) but replaces the steam Rankine cycle with an undesigned DEC system. Net LCOE impact of these substitutions cannot be estimated without a plant design.*
 
 **Missing Parameters**:
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Fusion power output (commercial plant) | truly-unknown | blocking | No plant study; EHL-2 is non-power |
-| Net electrical output | truly-unknown | blocking | No plant design |
-| Capital cost — any subsystem | truly-unknown | blocking | No plant study or estimate exists |
-| O&M cost | truly-unknown | blocking | No plant design basis |
-| Direct conversion efficiency | truly-unknown | blocking | DEC system not designed; alpha from p-B11 at 2.9 MeV each |
-| Capacity factor / availability | truly-unknown | blocking | No plant design basis |
-| Fusion Q (commercial target) | truly-unknown | blocking | EHL-2 is gain-negative by design |
-| Recirculating power fraction | derivable (partial) | blocking | Depends on DEC efficiency and heating power — no target plant parameters |
-| Balance of plant cost | derivable (analog) | important | D-T MFE analog possible; concept-specific BOP unknown |
-| Magnet system cost | derivable (analog) | important | Resistive coil analog available; conductor type unconfirmed |
-| B-11 fuel cost | not-yet-sourced | important | Isotope pricing literature exists, not captured |
-| Maintenance / replacement schedule | truly-unknown | important | No commercial device design |
+| Net electrical output (MWe) | truly-unknown | blocking | No power plant design exists; EHL-2 is experimental |
+| Engineering gain Q (Qeng) | truly-unknown | blocking | Physics verification has not begun; required Lawson criterion not yet approached |
+| Energy conversion efficiency (DEC) | truly-unknown | blocking | DEC technology unspecified; theoretical efficiency 60-90% cited for alpha capture but no design exists |
+| Capacity factor / availability | truly-unknown | blocking | No basis for estimate without operational device or design |
+| Capital cost by CAS account | derivable (rough D-T analog only) | blocking | BOP and structures can be estimated from D-T analog; power conversion (DEC) and first-wall systems cannot |
+| O&M cost (annual) | derivable (rough analog) | blocking | No concept-specific basis; D-T analogs available but power conversion system is fundamentally different |
+| Fuel cycle cost (B-11 enrichment) | not-yet-sourced | important | Natural boron ~80% ¹¹B; enrichment cost not published |
+| Recirculating power fraction | truly-unknown | blocking | Heating efficiency and recirculation requirements at power-plant scale not defined |
+| Replacement/maintenance schedule | truly-unknown | important | First-wall lifetime under alpha bombardment not characterized |
+| Plant thermal power (MWth) | truly-unknown | blocking | No net-power design; EHL-2 is non-power |
 
 ---
 
 ## Source Recommendations
 
-1. **EHL-2 full engineering paper** (doi:10.1088/2058-6272/ad981a, Plasma Sci. Technol.) — magnet system, vacuum vessel, power supply — `not-yet-sourced`. PDF extraction failed in iter-02; retry with agentic-mbse or docling. This is the highest-priority concept-scoped source not yet captured.
+**Integrated fleet-wide sources:**
 
-2. **p-B11 direct energy conversion literature** — search OSTI and arXiv for "proton-boron direct energy conversion," "aneutronic fusion energy capture," "alpha particle electrostatic converter." Lawrenceville Plasma Physics (Focus Fusion) has published on DEC for p-B11; `not-yet-sourced` — `unverified — confirm existence before searching`.
+- **TEA D-T MFE cost analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): Read and integrated. Covers CAS methodology (COA 21-27) and LCOE $140–550/MWh for a 350 MWe D-T tokamak. Useful as a methodology template and for BOP/structures analog costs. Cannot resolve p-B11-specific blocking gaps (DEC replaces Rankine cycle; no blanket/tritium system). Does not downgrade any blocking gap to important.
 
-3. **EXL-50U strategy and experimental progress paper** (doi:10.1088/2058-6272/ad9e8f) — listed in dossier key sources but not extracted. Contains EXL-50U current status relevant to EHL-2 readiness assessment; `not-yet-sourced`.
+- **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/`): Read and integrated. Contains ARIES-ST (spherical torus with normal conducting coils, LiPb+He D-T blanket) cost data — the closest architectural analog in the fleet-wide sources. ARIES-ST direct costs (~$54–58/kW level from table, CAS 22 blanket at ~$155.7M) confirm that the spherical torus architecture is costed in the ARIES framework. However, ARIES-ST's LiPb blanket and steam cycle are absent from p-B11; the DEC system has no ARIES analog. Does not downgrade any blocking gap.
 
-4. **Boron isotope enrichment supply chain** — search for B-11 isotope production, electromagnetic separation costs; IAEA isotope production reports. `not-yet-sourced` — `unverified — confirm existence before searching`.
+- **Wurzel & Hsu Lawson criterion** (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`): Read and integrated. Provides the physics benchmark framework. For p-B11, the required Lawson parameter is orders of magnitude above any achieved value and far above EHL-2's design target (Ti0 = 30 keV vs. the 125–330 keV needed for net energy). This source reinforces the "blocking" classification for the physics-feasibility gap but cannot resolve it.
 
-5. **Fleet-wide cost analogs** — `knowledge/sources/tea_dt_mfe_cost_analysis/` and `knowledge/sources/aries_cost_account_documentation/` are applicable for BOP, indirect costs, and CAS framework, but cannot fill any concept-specific gap. Use only as methodology scaffolding. No additional fleet-wide source is likely to be concept-specific.
+**Disqualified fleet-wide sources:**
 
-6. **Critique paper full text** (arXiv 2406.15495) — only abstract captured. Full PDF would provide quantitative bounds on heating power requirements for hot-ion mode — important for characterizing the physics uncertainty. `not-yet-sourced`.
+- **Revisit of the 2017 Costing for Four ARPA-E ALPHA Concepts** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): Read (grep). The four ALPHA concepts are compact modular systems (liner compression, HyperJet, Z-pinch type) — none are spherical tokamaks or p-B11 concepts. The $43/MWh LCOE figure applies to D-T compact concepts with conventional power conversion. Not applicable to this concept.
 
----
+- **A simplified economic model for inertial fusion** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`): IFE-specific (target, driver, rep rate). Not applicable to MFE.
 
-## Summary
+- **Economic studies for heavy-ion fusion** (`knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/`): HIF driver-dominated economics. Not applicable.
+
+- **Energy from Inertial Fusion**, **Accelerators for IFE**, **AMPS high-yield IFE**, **Commercialization of laser fusion energy**: All IFE-specific. Not applicable.
+
+- **Overview of the Helios Design** (`knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`): Stellarator architecture with HTS coils — different confinement topology and power conversion system. Not applicable.
 
-**Proceed to full analysis or acquire more sources first?** The gap is structural, not a sourcing problem. ENN has not published a commercial plant design, capital cost estimates, or DEC engineering — because those things do not yet exist. No additional source retrieval will fill the LCOE parameter table in any meaningful way. A D1+ analysis is feasible as a qualitative and physics-framing exercise (data availability rating, system function challenges, TRL by subsystem), but the quantitative LCOE model will be almost entirely built on analogues and assumptions rather than concept-specific data. Flag this explicitly in the write-up: this concept is too early-stage for a grounded LCOE estimate, and the primary analysis value is in characterizing the physics risk stack (hot-ion mode feasibility, DEC development gap, bremsstrahlung problem) rather than producing a number.
+- **An Assessment of the Economics of Future Electric Power** (`knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/`): Historical LCOE benchmark. General energy context only; does not address p-B11 or spherical tokamaks specifically. Disqualified as not filling any specific gap.
+
+**Recommended searches for not-yet-sourced gaps:**
+
+1. *EHL-2 magnet / coil engineering*: Search Fusion Engineering and Design, Plasma Science and Technology, and IEEE Trans. Applied Superconductivity for "EHL-2" + coil/magnet. Chinese-language technical reports at ENN Research or CNKI may contain specifics. Flag: `unverified — confirm existence before searching`
+
+2. *Boron-11 enrichment economics*: Search OSTI and commercial isotope supply literature for boron-11 enrichment cost estimates and supply chain capacity. Companies like Ames Laboratory and 5N Plus supply enriched boron; pricing may be available. Flag: `unverified — confirm existence before searching`
+
+3. *Direct energy conversion for aneutronic fusion*: Search for publications from Rostoker/UC Irvine group (Field Reversed Configuration DEC), TAE Technologies, and the broader MFE DEC literature. Kulcinski/Santarius Wisconsin papers on p-B11 DEC may provide efficiency ranges. Flag: `unverified — confirm existence before searching`
+
+4. *p-B11 burning plasma studies*: Lawson criterion analysis tailored to spherical tokamak geometry (e.g., Meschini et al. 2021/2023 cited in the Frontiersin paper). Search OSTI / arXiv for p-B11 + spherical tokamak + burning plasma.
 
 ---
 
+## Summary
+
+This concept cannot support a D1+ analysis at the full quantitative level. **Proceed to a qualitative analysis only**: the physics challenges (hot-ion mode feasibility, bremsstrahlung dominance, CS-free current drive scalability), subsystem TRL assessment, and technology risk analysis are well-supported by available sources. LCOE parameter extraction is not possible — every major economic input is absent or physically undefined. The path forward requires either (a) additional ENN publications post-EHL-2 completion, or (b) construction of a bottom-up analog analysis using D-T MFE plant costs as a baseline, with explicit placeholder assumptions for DEC efficiency, capacity factor, and capital costs — clearly flagged as speculative.
+
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Insufficient Data"
-blocking_count: 7
-important_count: 5
-counting_method: "deduplicated_across_all_sections — blocking: (1) no plant study/capital cost data, (2) DEC system undesigned (energy conversion), (3) hot-ion mode physics contested/undemonstrated, (4) p-B11 burning plasma TRL ~1, (5) fusion Q/power output unknown, (6) capacity factor unknown, (7) recirculating power unknown. Important: (1) EHL-2 magnet conductor unconfirmed, (2) divertor/heat flux solution absent, (3) B-11 enrichment supply chain, (4) DEC hardware materials, (5) O&M/maintenance schedule"
+blocking_count: 8
+important_count: 6
+counting_method: "all_sections_deduplicated — unique blocking gaps: (1) no power plant design/net electric output, (2) Q/Lawson criterion not approached, (3) DEC technology undefined, (4) hot-ion mode physics contested, (5) capital cost (no concept-specific data), (6) capacity factor undefined, (7) O&M undefined, (8) recirculating power fraction undefined. Important gaps: magnet type unconfirmed, CS-free scalability, boron-11 supply chain, first-wall materials, DEC materials, helium ash exhaust."
 section_coverage:
   availability_of_data:       "Poor"
   system_function:            "Partial"
```
