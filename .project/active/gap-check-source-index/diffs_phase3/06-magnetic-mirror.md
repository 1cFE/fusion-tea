# Phase 3 diff: 06-magnetic-mirror

**Generated:** 2026-05-22T13:33:51-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 8 | 4 | -4 |
| important_count  | 9 | 8 | - |
| overall_rating   | Insufficient Data | Significant Gaps | - |

## Fleet-source dispositions in new report

```
```

## Forbidden-phrase check (should be empty)

```
(none — good)
```

## First line of new report (should start with `# Gap Assessment`)

```
# Gap Assessment: Magnetic Mirror (p-B11)
```

## Blocking-tier lines (new)

```
34:- Integrated self-consistent power balance producing Q_eng — truly-unknown (the group's stated next objective) — **blocking**
35:- Alpha channeling efficiency (η_alpha) in a real rotating plasma device — truly-unknown (only theoretical/PIC, no experiment) — **blocking**
36:- RF system wall-plug efficiency for sustaining rotation and channeling — truly-unknown (no experimental or engineering data) — **blocking**
58:- Alpha channeling TRL in actual rotating plasma — truly-unknown — **blocking** (no demonstration exists anywhere)
109:| Engineering Q (Q_eng = net grid power / recirculating power) | truly-unknown | **blocking** | No integrated power balance published; Pale Blue's stated next objective. Cannot construct LCOE without net electric output. |
110:| Net electric power output (MWe) | truly-unknown | **blocking** | Depends on Q_eng. No plant sizing study exists. |
111:| DEC efficiency (η_DEC, fraction of alpha/rotation energy converted to electricity) | truly-unknown | **blocking** | PRX Energy 2025 paper gives theoretical limits but no demonstrated device efficiency. This IS the primary electrical conversion pathway. |
112:| RF system wall-plug efficiency (η_RF, includes RF drivers for alpha channeling + ponderomotive barriers + electrode) | truly-unknown | **blocking** | Determines recirculating power. ICRH wall-plug efficiency ~40-60% for tokamaks, but alpha channeling application may differ substantially. |
135:- `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` — **Integrated.** The four ALPHA concepts (Plasma-Jet MIF/HyperJet, Stabilized Liner Compressor/Compact Fusion Systems, Staged Z-Pinch/MIFTI, Flow-stabilized Z-Pinch/Zap Energy) are alternative compact MFE, not mirrors or p-B11, but share the modular architecture profile. Their CAS cost breakdown (Table 3) provides the best available analog for compact alternative MFE capital costs; their LCOE range ($33.8–53.7/MWh with learning credits at 90% availability for ~500 MWe) is the only published cost benchmark applicable as an order-of-magnitude reference. Notably, CAS 22.1.9 (Direct Energy Conversion) = $0 for all four concepts, meaning CHARM's DEC subsystem capital cost has no analog here. CAS 22.5 (Fuel Processing, $124M in D-T analog) would be greatly reduced for CHARM given no tritium, providing a modest favorable cost difference. This source partially resolves the `important` O&M and CapEx structure gaps but does NOT resolve any `blocking` gaps (Q_eng, DEC efficiency, α channeling efficiency, RF wall-plug efficiency).
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/06-magnetic-mirror.md	2026-05-22 12:59:21.060221939 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/06-magnetic-mirror/gap_report.md	2026-05-22 13:33:51.484885491 -0700
@@ -1,197 +1,172 @@
-I have all I need. Now I'll write the gap assessment.
-
----
-
 # Gap Assessment: Magnetic Mirror (p-B11)
 
 ## Overall Readiness
-**Rating**: Insufficient Data
-
-**Summary**: Pale Blue Fusion (CHARM concept) is a pre-incorporation academic spinout from Princeton with a strong theoretical physics corpus — 29 peer-reviewed papers, 4 patent applications, and multiple specialized computational codes — but zero published engineering content. No plant study, no reactor design, no device built by this team, no capital cost estimates, no Q target, and no power output target have been disclosed. The available sources are exclusively plasma physics papers and a 2025 ARPA-E pitch deck. LCOE analysis at this stage would be almost entirely assumption-driven with essentially no concept-specific anchors.
+**Rating**: Significant Gaps
+**Summary**: The Pale Blue Fusion CHARM concept has a remarkably rich theoretical physics literature (29 peer-reviewed papers, 4 patent applications, a 0D power balance code, and PIC simulations) that makes the concept architecture and physical mechanisms clear. However, the group is still pre-incorporation with no experimental device of their own, no engineering design study, and no integrated power balance demonstrating Q_eng > 1. Four physics parameters central to LCOE construction — engineering Q, alpha channeling efficiency in a real device, DEC efficiency, and RF system wall-plug efficiency — are either unmeasured or undemonstrated. A qualitative D1+ analysis is well-supported, but quantitative LCOE modeling requires either additional sources or heavily stated-assumption derivations.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Poor
+**Coverage**: Partial
 
-**Available**:
-- ARPA-E 2025 presentation (20 slides) covering CHARM concept architecture, derisked physics questions, computational tools, patent portfolio, and company pivot announcement — the single primary source covering both Phase 1a iterations (`iter-01/sources/arpa-e-fisch-2025-presentation.md`, `iter-02/sources/arpa-e-2025-fisch-presentation-notes.md`)
-- Princeton press release (2022) on ARPA-E OPEN 2021 funding ($1.5M grant) with conceptual framing
-- Technical papers summary (29 peer-reviewed publications, all plasma physics) — titles and brief summaries only, full papers not extracted
-- CMFX at UMD: a separate group's centrifugal mirror experiment that validates the general centrifugal mirror confinement physics but is not the Pale Blue/Fisch concept
-- Qualitative statements in the ARPA-E presentation that the physics components "suggest feasibility" but components have not yet been validated to work together "self-consistently"
-
-**Missing**:
-- No published reactor concept or plant study
-- No system-code output (their PB² power balance code results are internal; only the 0D code description is public)
-- No company website, investor deck, or technical whitepaper from Pale Blue Fusion (incorporation announced but not complete as of July 2025)
-- No experimental results from the CHARM architecture itself (CMFX is a different team/device)
-- Full text of 29 papers not extracted — some contain quantitative power balance estimates
+**Available**: The primary concept source is the ARPA-E 2025 annual meeting presentation (Fisch, Princeton, July 9 2025 — `iter-01/sources/arpa-e-fisch-2025-presentation.md`, `iter-02/sources/arpa-e-2025-fisch-presentation-notes.md`), which gives a complete architectural overview of the CHARM concept, derisking status, computational tools, patent portfolio, and company pivot to Pale Blue Fusion. The 29 peer-reviewed publications (listed in the presentation) cover alpha channeling theory, centrifugal confinement, ponderomotive barriers, synchrotron radiation suppression, DEC in axisymmetric fields, and the multi-chamber ash removal approach. The Princeton 2022 press release (`iter-01/sources/princeton-arpa-e-funding-2022.md`) contextualizes the concept's motivation and early stage. The related CMFX experiment at UMD (independent group, 3T/0.3T LTS magnets, 100 kV electrode, 6.7 m chamber, first plasma Oct 2022, fusion yield results arXiv:2505.23047 2025) provides the only adjacent experimental validation of centrifugal mirror physics, though CMFX is optimized for D-D not p-B11. Fuel-side data is excellent: p-B11 fuel is publicly characterized (reactivity, energy output, aneutronic nature, alpha particle spectrum). No plant study, no company engineering disclosures, and no FIA or investor funding announcements have been found beyond the initial ARPA-E OPEN 2021 award ($1.5M).
+
+**Missing**: No plant study or engineering design study exists. Pale Blue Fusion had not yet formally incorporated as of July 2025. No series-A or later funding rounds are publicly documented. No independent engineering assessment of the concept has been published. The CMFX results (arXiv:2505.23047) were not captured in Phase 1a research and may contain experimental performance data for the centrifugal mirror geometry.
 
 **Gaps**:
-- Quantitative reactor parameters (Q, power output, plasma density/temperature operating point) — `proprietary`/`not-yet-sourced` — **blocking**
-- Full text of key physics papers (especially Ochs & Fisch 2024 on breakeven requirements, Ochs et al. 2022 on hybrid p-B11 scheme) that contain internal quantitative performance estimates — `not-yet-sourced` — **important**
-- Company technical disclosure or investor materials from Pale Blue Fusion — `proprietary` — **important**
+- Plant engineering design study — proprietary/not-yet-sourced — important (company has not matured to this stage yet; no external study either)
+- Experimental validation from Pale Blue's own device — truly-unknown (no device built) — important
+- CMFX fusion yield data (arXiv:2505.23047) — not-yet-sourced — important (validates centrifugal mirror geometry)
+- Company funding and roadmap transparency — proprietary — important
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Partial (physics challenges well-documented; engineering modeling path absent)
+**Coverage**: Partial
+
+**Available**: The CHARM concept's operating principle is thoroughly described in open literature. The multi-chamber architecture (fusion chamber + heat exchange chamber + plug) is clearly laid out. The ARPA-E 2025 presentation explicitly enumerates nine derisking questions and their answers, confirming that individual mechanisms — alpha channeling for ash removal, centrifugal differential confinement, ponderomotive barriers for ion traffic, synchrotron radiation management via reabsorption, and rotation energy recovery — have each been theoretically validated. The (PB)² 0D power balance code (described in the presentation) incorporates fusion cross sections, reduced kinetic effects, relativistic collisions, bremsstrahlung, and self-consistent helium poisoning. The technical papers summary (`iter-01/sources/technical-papers-summary.md`) shows alpha channeling can reduce required confinement time by 2.6× to 6.9×. Key physics challenges are publicly documented: bremsstrahlung dominance at high T, helium poisoning, maintenance of nonthermal proton distribution.
 
-**Available**:
-- Detailed physics rationale for why a thermal p-B11 plasma cannot work (bremsstrahlung losses exceed fusion power, helium poisoning) — well-covered in ARPA-E presentation and papers
-- Description of the five-mechanism solution stack: centrifugal species separation, alpha channeling (RF waves in ICR range), ponderomotive barriers, multi-chamber architecture, biased electrode for rotation establishment
-- Acknowledgment that the team has answered 9 derisking questions theoretically/computationally but has not yet validated that these components work together self-consistently
-- Clear identification of recirculating power as a critical unknown ("engineering Q" must exceed 0 — but no quantitative estimate given)
-- Synchrotron radiation identified and addressed theoretically (manageable via reabsorption)
-
-**Missing**:
-- No systems-level integration analysis showing how the five mechanisms interact in a closed power loop
-- No RF system sizing (antenna type, power, frequency for alpha channeling at reactor scale)
-- No direct energy converter engineering design — only theoretical efficiency bounds from PRX Energy 2025 paper
-- No electrode design for high-voltage rotation establishment (Patent 19/175,473 covers "ultra-high DC voltages" but engineering detail not public)
-- No first-wall / plasma-facing component design (charged particle flux from mirror losses poses engineering challenge even without neutrons)
-- No quantitative recirculating power budget
+**Missing**: The presentation itself flags the critical remaining gap: "Now we need to see if these components work together self-consistently." No integrated system power balance with quantitative engineering Q has been published. The multi-chamber design involves simultaneous operation of RF alpha channeling, centrifugal confinement, ponderomotive barriers, and DEC — no simulation combines all these simultaneously. Synchrotron radiation quantitative suppression factor under actual reactor plasma conditions (high temperature, relativistic electrons) remains uncertain despite the Mlodik papers.
 
 **Gaps**:
-- Recirculating power fraction (RF heating + DEC round-trip efficiency) — `truly-unknown` at system level — **blocking**; this is the central viability question for p-B11
-- Self-consistent integrated power balance at reactor scale — `truly-unknown` — **blocking**
-- RF antenna / wave-coupling system engineering — `truly-unknown` — **important**
-- Plasma-facing component and end-loss collector engineering — `truly-unknown` — **important**
-- Whether DEC approach is SWDEC (2023 patent) or adiabatic (2025 PRX Energy paper) — `proprietary` — **nice-to-have** (either way, DEC is assumed; efficiency range can be bounded)
+- Integrated self-consistent power balance producing Q_eng — truly-unknown (the group's stated next objective) — **blocking**
+- Alpha channeling efficiency (η_alpha) in a real rotating plasma device — truly-unknown (only theoretical/PIC, no experiment) — **blocking**
+- RF system wall-plug efficiency for sustaining rotation and channeling — truly-unknown (no experimental or engineering data) — **blocking**
+- Quantitative synchrotron radiation suppression factor in reactor-relevant conditions — derivable/truly-unknown — important
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
-**Coverage**: Poor
+**Coverage**: Partial
+
+**Available**: The following TRL assessments can be made from available sources:
+- *Solenoidal mirror coil geometry*: TRL 6-7 for the geometry itself (validated in CMFX at UMD with LTS, in WHAM at Wisconsin with HTS REBCO at 17T). Simple axisymmetric wound coils, well-understood manufacturing.
+- *Biased central electrode for rotation*: TRL 4-5. CMFX at UMD demonstrated 100 kV, 100 kW DC biased electrode driving rotation. Related technology in plasma mass filters.
+- *Vacuum system and plasma chamber*: TRL 8-9. Standard technology from existing mirror and tokamak programs.
+- *Fuel injection (hydrogen + boron)*: TRL 5-6. Gas injection of hydrogen is routine. Boron injection into plasmas has been demonstrated for impurity seeding.
+- *RF heating (ICRH-range waves)*: TRL 6-7 for conventional ICRH. The specific XB mode conversion coupling scheme in a rotating plasma is TRL 2-3 (S5 PIC simulations only, no hardware demonstration).
+- *Alpha channeling via RF waves*: TRL 2-3. Theory since 2006 (Fisch), 29 papers, no experimental demonstration of the energy extraction mechanism.
+- *Ponderomotive barriers (static field perturbations)*: TRL 2 (theory and PIC only, no experimental validation).
+- *Direct energy conversion (adiabatic DEC for rotating plasma)*: TRL 2-3. PRX Energy 2025 paper provides theoretical efficiency limits, SWDEC patent exists. No hardware demonstration for this geometry.
+- *Multi-chamber plasma interface*: TRL 1-2 (novel architecture, no experiments).
 
-**Available**:
-- Centrifugal mirror physics: validated at CMFX (UMD, separate group) — general confinement physics TRL 3–4, but the CHARM multi-chamber architecture is undemonstrated
-- Alpha channeling in mirror machines: theoretical TRL 3 (Fisch 2006 landmark paper, confirmed in simulations); no experimental demonstration in a rotating plasma
-- Ponderomotive barriers in rotating plasma: theoretical TRL 3 (published papers, patents); no experimental demonstration
-- Direct energy conversion (adiabatic, axisymmetric): theoretical TRL 2–3 (PRX Energy 2025 paper); no experimental hardware
-- Biased electrode for E×B rotation: TRL 4–5 in non-fusion plasma contexts (the CMFX experiment at UMD uses 100 kV, 100 kW power supply as of May 2024)
-
-**Missing**:
-- No TRL assessment for any subsystem has been published by the team
-- No magnet technology specified → no magnet TRL or cost anchor
-- No RF system hardware (antenna, power conditioning) for alpha channeling at any scale
-- No integrated device demonstrating even one chamber of the CHARM concept
+**Missing**: Magnet conductor type (HTS vs. LTS vs. normal conducting) not specified by Pale Blue — affects cost, performance, and TRL of the coil system. No TRL data from Pale Blue's own experimental program.
 
 **Gaps**:
-- Magnet type and TRL — `proprietary` (likely an engineering decision not yet made) — **important** for cost
-- Alpha channeling experimental validation — `truly-unknown` at present in rotating mirror; experimental work is future work for Pale Blue Fusion — **blocking** for any credible physics Q estimate
-- Full CHARM architecture experimental demonstration — `truly-unknown` — **blocking** at concept level
-- DEC hardware TRL — `truly-unknown` for their specific approach — **important**
+- Alpha channeling TRL in actual rotating plasma — truly-unknown — **blocking** (no demonstration exists anywhere)
+- DEC hardware TRL for mirror geometry — truly-unknown — important
+- Ponderomotive barrier experimental demonstration — truly-unknown — important
+- Magnet conductor type — not-yet-sourced/proprietary — important
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Partial (aneutronic advantages clear; engineering material needs absent)
+**Coverage**: Good
 
-**Available**:
-- Fuel: p (proton from water/hydrogen — abundant, no supply chain concern) and B-11 (naturally 80% of boron, cheap and non-radioactive) — explicitly cited as advantages
-- No tritium: eliminates Li-6, Be breeding blanket, and tritium handling entirely
-- No significant neutron flux: eliminates activation constraints on structural materials, allows conventional steel/aluminum structures in principle
-- No waste storage: no long-lived activation products
-
-**Missing**:
-- Magnet conductor material and supply chain — completely unknown since magnet type unspecified; if HTS (REBCO tape), supply chain considerations apply; if LTS (NbTi/Nb₃Sn), mature supply exists
-- RF antenna and power conditioning materials — not specified
-- High-voltage electrode materials for sustained 100 kV operation in plasma — `not-yet-sourced`; relevant research exists in the plasma propulsion and centrifugal mirror communities but not cited
-- Vacuum vessel materials — not addressed
+**Available**: The p-B11 fuel cycle is a significant advantage for materials and supply chain:
+- *Protons*: Hydrogen, the most abundant element. No supply chain concern.
+- *Boron-11*: Naturally ~80% B-11 by isotopic abundance. Commercially mined as borax/boric acid at large industrial scale for ~$1/kg. Isotopic enrichment possible if higher purity needed.
+- *No tritium*: Eliminates the tritium breeding blanket, lithium supply, tritium handling facilities, and associated NRC licensing burden.
+- *No neutron damage*: Minimal material activation means no radiation-hardened first wall materials, no beryllium/tungsten tile programs, no remote handling for activated components. This is a structural cost advantage over D-T MFE.
+- *Vacuum vessel*: Conventional stainless steel or similar — no neutron-specific materials required.
+- *Magnets*: If HTS (REBCO likely for high-field), REBCO tape supply chain exists (AMSC, SuperPower, Fujikura) and is being scaled up for tokamak programs. If LTS, NbTi/Nb3Sn conventional — mature supply chain.
+
+**Missing**: Pale Blue has not disclosed magnet conductor choice, which is the primary materials supply chain question. RF antenna materials in a rotating plasma environment (potential sputtering or erosion by the supersonic plasma flow past the electrode/antenna structures) are not discussed.
 
 **Gaps**:
-- Magnet conductor material identity — `proprietary`/`not-yet-sourced` — **important**
-- Electrode materials for sustained high-voltage plasma operation — `not-yet-sourced` — **nice-to-have**
-- (No blocking supply chain gaps identified beyond magnet uncertainty; the aneutronic fuel cycle removes the most severe supply chain constraints present in D-T concepts)
+- Magnet conductor specification — not-yet-sourced/proprietary — important
+- RF antenna/electrode materials compatibility with supersonic rotating plasma — not-yet-sourced — nice-to-have
+- Boron isotopic enrichment requirement — not-yet-sourced — nice-to-have (probably not needed at 80% natural abundance but worth confirming)
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor
-
 **Available Parameters**:
 
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Fuel type | p-B11 (proton + boron-11) | ARPA-E 2025 presentation | high |
-| Fuel cost | Near-zero (abundant, non-radioactive) | ARPA-E 2025 presentation | high |
-| Tritium breeding cost | None (N/A) | ARPA-E 2025 presentation | high |
-| Neutron shielding cost | Minimal | ARPA-E 2025 presentation | high |
-| Operation mode | Steady-state | Dossier / presentation | high |
-| Energy capture type | Direct (charged particle) — adiabatic DEC or SWDEC | Dossier / PRX Energy 2025 | medium |
-| DEC theoretical efficiency bound | Studied in PRX Energy 2025 (axisymmetric limits) | PRX Energy 4, 013007 (2025) | low — theoretical only |
-| Recirculating power concept | Alpha channeling recycling fraction η_α into proton heating; radial E-field energy recoverable | ARPA-E 2025 slides 5, 14, 19 | low — no system-level number |
-| Engineering Q requirement | Must exceed 0 (breakeven); lowered by factor 2.6–6.9 via alpha channeling | Technical papers summary / Ochs & Fisch 2024 | low — qualitative bounds only |
+| Fuel cost | ~$0/MWh (protons + B-11 abundant and cheap) | ARPA-E presentation, slide 1 | h |
+| Operation mode | Steady-state, continuous | ARPA-E presentation | h |
+| Tritium breeding/blanket cost | $0 (aneutronic) | ARPA-E presentation, slide 1 | h |
+| Neutron-related costs (activation, shielding, first wall replacement) | Negligible | ARPA-E presentation, slide 1; p-B11 physics | h |
+| Fuel processing capital cost analog | ~$124M (D-T analog) → CHARM much lower (no T) | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` Table 3 | m (analog only) |
+| Plant availability factor | ~90% (analog from ALPHA compact MFE study) | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` Table 4 | l (assumed, analog) |
+| Compact modular MFE LCOE analog | $33.8–53.7/MWh (with learning curve credits) for ~500 MWe | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` Table 4 | l (analog only; different concepts) |
+| Compact modular MFE CapEx analog | $2.0–3.3/W; $838M–$1.64B total for ~500 MWe | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` Table 3 | l (analog only) |
+| O&M cost analog | $42–61M/yr for ~500 MWe | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` Table 4 | l (analog) |
+| Replacement cost analog | $6–30M/yr | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` Table 4 | l (analog) |
+| Structures/site analog | $174–370M | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` Table 3 | l (analog) |
+| Power supplies cost analog (CAS 22.1.7) | $12–140M (wide range reflecting concept diversity) | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` Table 3 | l (analog) |
+| DEC cost in ALPHA analogs | $0 (none of four ALPHA concepts used DEC) | `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` Table 3, CAS 22.1.9 | — (not applicable) |
+| α channeling improvement on confinement | 2.6× to 6.9× reduction in required τE | `iter-01/sources/technical-papers-summary.md` | m |
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Net electric power output (MWe) | truly-unknown | blocking | No plant study; no target disclosed |
-| Target engineering Q value | truly-unknown | blocking | 0D PB² code exists internally but results not published |
-| Capital cost by CAS subsystem | truly-unknown | blocking | No plant study; no engineering design |
-| Magnet system cost | not-yet-sourced / derivable | blocking | Magnet type not specified; if HTS solenoidal, REBCO cost models exist |
-| RF system cost (alpha channeling) | truly-unknown | blocking | Novel application; no cost analogue |
-| Direct energy converter cost | truly-unknown | blocking | Novel hardware; no commercial DEC exists for mirror geometry |
-| Recirculating power fraction (system level) | truly-unknown | blocking | The central viability question; only theoretical components available |
-| Balance of plant cost | derivable | important | Standard thermal/electrical BOP; ALPHA costing study (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) provides ~$500M BOP analog for ~500 MWe |
-| O&M costs | derivable | important | Aneutronic → no tritium handling, no waste management; analogs from MFE plant studies apply for staffing/maintenance |
-| Capacity factor | derivable | important | Steady-state, aneutronic → no blanket replacement outages, no tritium inventory limit; theoretical CF likely high (>90%?) but no engineering basis stated |
-| Thermal/electrical conversion efficiency | not-yet-sourced | important | DEC efficiency is the key parameter; theoretical bounds exist in PRX Energy 2025 but system-level number requires engineering |
-| Plasma density and temperature operating point | not-yet-sourced | important | PB² code produces these internally; some bounds visible in published papers (relativistic regime ~GK temperatures) |
-| First wall / end collector cost | truly-unknown | important | No design; charged particle flux from mirror losses must be managed |
-| Electrode power supply cost | not-yet-sourced | important | High-voltage rotating plasma bias (100 kV+ at reactor scale); CMFX uses 100 kW supply at experiment scale |
+| Engineering Q (Q_eng = net grid power / recirculating power) | truly-unknown | **blocking** | No integrated power balance published; Pale Blue's stated next objective. Cannot construct LCOE without net electric output. |
+| Net electric power output (MWe) | truly-unknown | **blocking** | Depends on Q_eng. No plant sizing study exists. |
+| DEC efficiency (η_DEC, fraction of alpha/rotation energy converted to electricity) | truly-unknown | **blocking** | PRX Energy 2025 paper gives theoretical limits but no demonstrated device efficiency. This IS the primary electrical conversion pathway. |
+| RF system wall-plug efficiency (η_RF, includes RF drivers for alpha channeling + ponderomotive barriers + electrode) | truly-unknown | **blocking** | Determines recirculating power. ICRH wall-plug efficiency ~40-60% for tokamaks, but alpha channeling application may differ substantially. |
+| Capital cost of DEC hardware | truly-unknown | important | No commercial DEC for mirror geometry exists; only patent concepts. |
+| Capital cost of ponderomotive barrier system (RF walls / static field perturbations) | truly-unknown | important | Novel subsystem with no cost analogs. |
+| Capital cost of magnet system | not-yet-sourced | important | Simple solenoidal geometry; derivable once conductor type known. ALPHA analog: CAS 22.1.3 Coils $0–22.8M (low for non-superconducting concepts). |
+| Thermal conversion efficiency | truly-unknown | important | CHARM may be all-DEC with no steam cycle; if synchrotron radiation is partially recovered thermally, a thermal cycle may be needed. Architecture not specified. |
+| Capacity factor | derivable | important | Assume 85–90% for steady-state; consistent with ALPHA compact MFE analog at 90%. Uncertain for first-of-kind novel device. |
 
 ---
 
 ## Source Recommendations
 
-1. **Full text of Ochs & Fisch (2024), "Lowering the reactor breakeven requirements for proton-Boron 11 fusion," Physics of Plasmas 31, 012503** — contains quantitative breakeven analysis with power balance ratios. Should be ingested via Zotero. `not-yet-sourced` — this paper exists and would provide the most authoritative public Q estimate.
+**CHARM-specific:**
+- Search arXiv and Physics of Plasmas for CMFX fusion yield report (arXiv:2505.23047, 2025) — `not-yet-sourced` — will contain the first centrifugal mirror fusion yield data and may constrain confinement time scaling relevant to CHARM's physics basis.
+- Search for "Pale Blue Fusion" incorporation news and FIA (Fusion Industry Association) membership listing — `not-yet-sourced` — may exist by early 2026 given "coming soon" website at July 2025 ARPA-E meeting.
+- Search OSTI for any Nat Fisch-group engineering studies or system-level cost estimates for p-B11 centrifugal mirror — `not-yet-sourced; confirm existence before searching`.
+- Watch for Ochs, Kolmes, Fisch preprints describing the integrated CHARM power balance — the ARPA-E presentation explicitly flagged this as their next objective ("in silico power-positive reactor").
 
-2. **Full text of Ochs et al. (2022), "Improving the Feasibility of Economical Proton-Boron 11 Fusion via Alpha Channeling," Phys. Rev. E 106, 055215** — contains quantitative alpha channeling efficiency estimates (η_α) that directly feed recirculating power calculations. `not-yet-sourced`.
+**DEC analog:**
+- Search for TAE Technologies / FRC direct energy converter publications, or Princeton mirror-DEC prior art (MFTF program, Fowler & Rankin era) — `not-yet-sourced` — centrifugal mirrors share the open-field-line geometry where classical mirror DEC was developed.
+- Ambipolar direct conversion for mirror machines (Moir et al., LLNL, 1970s-1980s) may provide efficiency analogs — `not-yet-sourced; unverified — confirm existence before searching`.
 
-3. **Full text of Rax, Kolmes & Fisch (2025), "Efficiency and Physical Limitations of Adiabatic Direct Energy Conversion in Axisymmetric Fields," PRX Energy 4, 013007** — DEC efficiency bounds from the core team; essential for any recirculating power model. `not-yet-sourced`.
+**Fleet-wide sources — integration notes and disqualifications:**
 
-4. **CMFX publications (arXiv:2505.23047 — fusion yield measurements, 2025)** — while CMFX is a separate group, the centrifugal mirror plasma parameters (density, rotation speed, confinement time) achieved experimentally provide the closest available validation data for mirror plasma physics at the experiment scale. `not-yet-sourced`.
+- `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` — **Integrated.** The four ALPHA concepts (Plasma-Jet MIF/HyperJet, Stabilized Liner Compressor/Compact Fusion Systems, Staged Z-Pinch/MIFTI, Flow-stabilized Z-Pinch/Zap Energy) are alternative compact MFE, not mirrors or p-B11, but share the modular architecture profile. Their CAS cost breakdown (Table 3) provides the best available analog for compact alternative MFE capital costs; their LCOE range ($33.8–53.7/MWh with learning credits at 90% availability for ~500 MWe) is the only published cost benchmark applicable as an order-of-magnitude reference. Notably, CAS 22.1.9 (Direct Energy Conversion) = $0 for all four concepts, meaning CHARM's DEC subsystem capital cost has no analog here. CAS 22.5 (Fuel Processing, $124M in D-T analog) would be greatly reduced for CHARM given no tritium, providing a modest favorable cost difference. This source partially resolves the `important` O&M and CapEx structure gaps but does NOT resolve any `blocking` gaps (Q_eng, DEC efficiency, α channeling efficiency, RF wall-plug efficiency).
 
-5. **Revisit of 2017 ARPA-E ALPHA Concepts costing** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) — already ingested. Covers four compact modular fusion concepts with CAS-level cost breakdowns at ~500 MWe. The BOP costs (~$500M of ~$1.2B total CapEx) and LCOE methodology (43 $/MWh average) are applicable as analog for balance-of-plant estimation even though none of the four concepts is a mirror. Useful for non-fusion-core LCOE parameters.
+- `knowledge/sources/aries_cost_account_documentation/` — **Integrated for methodology.** Provides the definitive CAS framework (accounts 20-27, 90-99) used across all fusion plant studies. CHARM would use this same CAS structure. The escalation methodology and historical cost basis (Starfire 1980 through ARIES series) are the foundation for any future plant costing study. However, this source does not contain CHARM-specific cost data and does not resolve any gaps. It provides the formal structure into which CHARM costs would be organized.
 
-6. **Pale Blue Fusion company materials** — once the website launches (announced July 2025 as "coming soon"). Monitor palebluefusion.com. `proprietary` gap — may partially resolve with company launch. Flag as `unverified — confirm existence before searching`.
+- `knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/` — **Partially integrated for TRL context.** The Wurzel & Hsu 2021 paper compiles Lawson parameters and triple products across MCF, ICF, and MIF experiments. As of the 2021 publication cutoff, CMFX had not yet achieved first plasma (Oct 2022) and no mirror physics data from the Pale Blue team existed. The paper is useful for confirming how far centrifugal mirrors and p-B11 approaches generally sit from the Lawson criterion (p-B11 requires nTτ roughly 500× higher than D-T at the same gain due to lower reactivity and bremsstrahlung losses — this is documented in Appendix C of the paper). This context supports the TRL assessment in §3 but does not contain CHARM-specific experimental data.
 
-7. **Search OSTI and arXiv for "centrifugal mirror" + "power balance" or "reactor study"** — there may be pre-2021 reactor studies on centrifugal mirror concepts (e.g., Gas Dynamic Trap at Novosibirsk, Budker Institute work) that provide relevant plasma parameter ranges. `unverified — confirm existence before searching`.
+- `knowledge/sources/tea_dt_mfe_cost_analysis/` — **Disqualified.** This source covers D-T tokamak TEA methodology including tritium breeding blanket, high-heat-flux first wall, and steam turbine thermal cycle — precisely the subsystems CHARM eliminates. The BOP analog costs differ structurally from CHARM's DEC-primary architecture. Applying D-T thermal conversion assumptions to an all-DEC concept would produce systematically misleading LCOE estimates without further decomposition.
 
-8. **TAE Technologies or other p-B11 company publications** — TAE (tri-alpha energy) targets p-B11 with a different architecture (FRC) but their published power balance analyses may provide boundary conditions on the p-B11 challenge (bremsstrahlung wall, minimum Q requirements). `not-yet-sourced` for the specific plasma physics constraints shared across all p-B11 approaches.
+- `knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/` — **Disqualified.** This ORNL historical assessment benchmarks fusion LCOE against coal, nuclear, and wind in a generic energy context. It does not contain cost structure data specific to any confinement approach and adds no signal beyond the ALPHA compact MFE analog already integrated.
 
----
+- All IFE and HIF sources (`a_simplified_economic_model_for_inertial_fusion/`, `energy_from_inertial_fusion/`, `accelerators_for_inertial_fusion_energy_production/`, `economic_studies_for_heavy_ion_fusion_electric_power_plants/`, `affordable_manageable_practical_and_scalable_amps_high/`, `commercialization_of_laser_fusion_energy/`) — **Disqualified.** These sources cover pulse-driven, target-based fusion concepts. CHARM is a steady-state MFE device with completely different physics, subsystems (no driver, no target, no rep-rate), and cost structure. None address centrifugal mirror, rotating plasma, or p-B11 fuel cycle.
 
-## Summary
+- `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/` — **Disqualified.** Helios is a steady-state HTS stellarator with D-T fuel and a thermal cycle; its costing would emphasize complex coil fabrication and neutronics. CHARM's simple solenoidal coils and aneutronic fuel make the stellarator's dominant cost drivers irrelevant.
 
-The available data is insufficient to produce a high-quality D1+ concept analysis at this time. The concept sits firmly in the theoretical physics stage — 29 strong peer-reviewed papers establish the physics rationale and de-risk individual components, but no engineering design, plant study, experimental results from the CHARM architecture, or system-level power balance output has been published. Every LCOE parameter beyond fuel cost and operation mode requires either pure assumption or analog borrowing from unrelated concepts.
+- `/home/reid/PyFECONS` — **Disqualified for this concept.** PyFECONS is calibrated to D-T MFE and IFE (tokamaks, stellarators, mirrors in thermal equilibrium). CHARM's nonthermal, DEC-primary, aneutronic design would require substantial modification of PyFECONS assumptions to produce meaningful output. Using it without modification would produce misleading results.
 
-**Before proceeding to full analysis**, the recommended path is:
-1. Ingest the three key physics papers (Ochs & Fisch 2024; Ochs et al. 2022; Rax et al. 2025 PRX Energy) — these contain the closest available approximation to a public power balance.
-2. Ingest CMFX 2025 experimental results for physics validation context.
-3. Check palebluefusion.com for any launched technical content.
+---
+
+## Summary
 
-With those additions, a qualitative analysis can be written with well-documented physics context and honest uncertainty bounds. A quantitative LCOE model would be almost entirely parameterized on assumptions, with only fuel cost, steady-state operation, and aneutronic advantages as concept-specific anchors.
+The Magnetic Mirror (p-B11) / CHARM concept by Pale Blue Fusion (Princeton spinout) is in a pre-engineering, theoretical physics stage. The available data supports a strong qualitative D1+ analysis: the concept architecture is clear, the operating principles are well-published, the fuel cycle advantages are significant (no T, no neutrons, cheap fuel, simpler materials), and the modular MFE LCOE analog from the ALPHA costing study ($34–54/MWh) provides an order-of-magnitude cost bracket. However, the concept lacks any demonstration of physics feasibility (Q_eng > 1 has not been computed for the integrated system), no DEC efficiency has been measured, no alpha channeling has been demonstrated experimentally, and no engineering design study exists. Quantitative LCOE construction is not feasible without either (a) published integrated power balance results from Pale Blue, (b) experimental efficiency data from CMFX or a future Pale Blue device, or (c) explicit assumption-driven parameter derivations that must be clearly flagged as speculative. **Proceed to full qualitative analysis with stated-assumption LCOE bounds; do not report a point LCOE estimate without clearly labeling it as analog-derived with large uncertainty.**
 
 ---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Insufficient Data"
-blocking_count: 8
-important_count: 9
-counting_method: "section_5_missing_parameters (6 blocking LCOE params) + sections_1_through_4 unique blocking gaps (recirculating power fraction, alpha channeling experimental validation, self-consistent integrated power balance) deduplicated; important counts all non-blocking important gaps across sections 1-5 deduplicated"
+overall_rating: "Significant Gaps"
+blocking_count: 4
+important_count: 8
+counting_method: "all_sections_deduplicated — blocking: (1) integrated engineering Q / net power output, (2) alpha channeling efficiency in real device, (3) DEC efficiency, (4) RF system wall-plug efficiency; important: plant engineering study, CMFX fusion yield data, DEC hardware capital cost, ponderomotive barrier cost, magnet conductor specification, thermal conversion architecture, capacity factor, company funding/roadmap"
 section_coverage:
-  availability_of_data:       "Poor"
+  availability_of_data:       "Partial"
   system_function:            "Partial"
-  subsystem_maturity:         "Poor"
-  materials_supply_chain:     "Partial"
+  subsystem_maturity:         "Partial"
+  materials_supply_chain:     "Good"
   lcoe_parameter_extraction:  "Poor"
 ```
\ No newline at end of file
```
