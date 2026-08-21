# Diff: 06-magnetic-mirror

**Generated:** 2026-05-22T09:39:50-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 13 | 8 | -5 |
| important_count  | 3 | 9 | - |
| overall_rating   | Significant Gaps | Insufficient Data | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
141:| Balance of plant cost | derivable | important | Standard thermal/electrical BOP; ALPHA costing study (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) provides ~$500M BOP analog for ~500 MWe |
161:5. **Revisit of 2017 ARPA-E ALPHA Concepts costing** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) — already ingested. Covers four compact modular fusion concepts with CAS-level cost breakdowns at ~500 MWe. The BOP costs (~$500M of ~$1.2B total CapEx) and LCOE methodology (43 $/MWh average) are applicable as analog for balance-of-plant estimation even though none of the four concepts is a mirror. Useful for non-fusion-core LCOE parameters.
```

## Blocking-tier lines (baseline)

```
35:- Plant study / system-level design — `truly-unknown` (does not yet exist) — **blocking** for quantitative LCOE
37:- (PB)² power balance code results — `proprietary` — **blocking** for Q and power balance numbers
60:- Quantified plasma operating point (T, n, τ, Q) — `proprietary` (exists in (PB)² but unpublished) — **blocking** for any LCOE model
61:- Alpha channeling efficiency η_α — `not-yet-sourced` (likely in one of the 29 papers not fully read) — **blocking**
62:- Net electrical efficiency end-to-end — `truly-unknown` at this stage — **blocking**
131:| Q (fusion gain) / net gain | proprietary | blocking | (PB)² code exists but results unpublished |
132:| Plant electrical output target (MWe) | truly-unknown | blocking | No plant study |
133:| Capital cost — magnet system | proprietary/truly-unknown | blocking | Conductor not specified; no reactor design |
134:| Capital cost — vacuum vessel / structural | truly-unknown | blocking | No engineering design |
135:| Capital cost — DEC system | truly-unknown | blocking | No prototype, no cost study |
136:| Capital cost — RF system (alpha channeling) | truly-unknown | blocking | No antenna design |
137:| Capital cost — balance of plant | truly-unknown | blocking | No plant study |
138:| DEC electrical efficiency (%) | not-yet-sourced | blocking | PRX Energy 2025 may contain theoretical bounds — paper not fully read |
139:| Alpha channeling efficiency η_α (%) | not-yet-sourced | blocking | Likely in one of the 29 publications |
140:| Plasma temperature operating point | proprietary | blocking | Needed to compute bremsstrahlung losses |
141:| Plasma density operating point | proprietary | blocking | Needed for fusion power density |
142:| Mirror ratio / device dimensions | truly-unknown | blocking | No reactor design disclosed |
146:| Recirculating power fraction | proprietary | blocking | RF drive + rotation maintenance power not quantified |
```

## Blocking-tier lines (new)

```
34:- Quantitative reactor parameters (Q, power output, plasma density/temperature operating point) — `proprietary`/`not-yet-sourced` — **blocking**
59:- Recirculating power fraction (RF heating + DEC round-trip efficiency) — `truly-unknown` at system level — **blocking**; this is the central viability question for p-B11
60:- Self-consistent integrated power balance at reactor scale — `truly-unknown` — **blocking**
85:- Alpha channeling experimental validation — `truly-unknown` at present in rotating mirror; experimental work is future work for Pale Blue Fusion — **blocking** for any credible physics Q estimate
86:- Full CHARM architecture experimental demonstration — `truly-unknown` — **blocking** at concept level
134:| Net electric power output (MWe) | truly-unknown | blocking | No plant study; no target disclosed |
135:| Target engineering Q value | truly-unknown | blocking | 0D PB² code exists internally but results not published |
136:| Capital cost by CAS subsystem | truly-unknown | blocking | No plant study; no engineering design |
137:| Magnet system cost | not-yet-sourced / derivable | blocking | Magnet type not specified; if HTS solenoidal, REBCO cost models exist |
138:| RF system cost (alpha channeling) | truly-unknown | blocking | Novel application; no cost analogue |
139:| Direct energy converter cost | truly-unknown | blocking | Novel hardware; no commercial DEC exists for mirror geometry |
140:| Recirculating power fraction (system level) | truly-unknown | blocking | The central viability question; only theoretical components available |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/06-magnetic-mirror.md	2026-05-22 09:21:13.837821928 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/06-magnetic-mirror/gap_report.md	2026-05-22 09:39:50.428520984 -0700
@@ -1,114 +1,112 @@
-Now I have everything needed. Let me write the gap assessment.
+I have all I need. Now I'll write the gap assessment.
 
 ---
 
 # Gap Assessment: Magnetic Mirror (p-B11)
 
 ## Overall Readiness
-**Rating**: Significant Gaps
+**Rating**: Insufficient Data
 
-**Summary**: The available data supports a qualitative narrative and physics-level discussion, but the concept is essentially pre-engineering — the Fisch group has published 29 plasma physics papers and filed 4 patents with no reactor engineering, cost estimates, or system-level design. There is enough for an honest qualitative section and a heavily assumption-laden LCOE skeleton, but virtually every quantitative LCOE parameter will require explicit "assumed by analogy" flagging. A first-pass analysis is feasible with appropriate caveats; the analyst should not expect to extract numbers from sources.
+**Summary**: Pale Blue Fusion (CHARM concept) is a pre-incorporation academic spinout from Princeton with a strong theoretical physics corpus — 29 peer-reviewed papers, 4 patent applications, and multiple specialized computational codes — but zero published engineering content. No plant study, no reactor design, no device built by this team, no capital cost estimates, no Q target, and no power output target have been disclosed. The available sources are exclusively plasma physics papers and a 2025 ARPA-E pitch deck. LCOE analysis at this stage would be almost entirely assumption-driven with essentially no concept-specific anchors.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Limited
+**Coverage**: Poor
 
 **Available**:
-- ARPA-E 2025 presentation (20 slides): CHARM architecture, derisked physics questions, computational tools summary, patent portfolio, company pivot intent — the single most complete public disclosure [arpa-e-fisch-2025-presentation.md, arpa-e-2025-fisch-presentation-notes.md]
-- 29 peer-reviewed publications (2022–2025) under ARPA-E support — all plasma physics / wave physics; titles and some content captured in technical-papers-summary.md
-- Princeton press release (2022): $1.5M ARPA-E OPEN grant, confirms purely theoretical start [princeton-arpa-e-funding-2022.md]
-- PRX Energy 2025 paper (Rax, Kolmes, Fisch) on adiabatic DEC efficiency — most engineering-adjacent publication in the corpus
-- 4 patent applications (March–April 2025): plasma physics and confinement innovations, no engineering specifications
-- CMFX at UMD: external experiment validating centrifugal mirror physics (not Pale Blue's device)
+- ARPA-E 2025 presentation (20 slides) covering CHARM concept architecture, derisked physics questions, computational tools, patent portfolio, and company pivot announcement — the single primary source covering both Phase 1a iterations (`iter-01/sources/arpa-e-fisch-2025-presentation.md`, `iter-02/sources/arpa-e-2025-fisch-presentation-notes.md`)
+- Princeton press release (2022) on ARPA-E OPEN 2021 funding ($1.5M grant) with conceptual framing
+- Technical papers summary (29 peer-reviewed publications, all plasma physics) — titles and brief summaries only, full papers not extracted
+- CMFX at UMD: a separate group's centrifugal mirror experiment that validates the general centrifugal mirror confinement physics but is not the Pale Blue/Fisch concept
+- Qualitative statements in the ARPA-E presentation that the physics components "suggest feasibility" but components have not yet been validated to work together "self-consistently"
 
 **Missing**:
-- Published plant study or reactor concept study
-- Any engineering design (magnets, vacuum vessel, first wall, balance of plant)
-- Company technical disclosures (website listed as "coming soon" as of July 2025)
-- System code outputs (the (PB)² power balance code exists but results are not published beyond a schematic diagram)
-- Funding announcements or investor disclosures post-July 2025
+- No published reactor concept or plant study
+- No system-code output (their PB² power balance code results are internal; only the 0D code description is public)
+- No company website, investor deck, or technical whitepaper from Pale Blue Fusion (incorporation announced but not complete as of July 2025)
+- No experimental results from the CHARM architecture itself (CMFX is a different team/device)
+- Full text of 29 papers not extracted — some contain quantitative power balance estimates
 
 **Gaps**:
-- Plant study / system-level design — `truly-unknown` (does not yet exist) — **blocking** for quantitative LCOE
-- Company technical disclosures — `proprietary` (company not yet incorporated as of July 2025) — **important**
-- (PB)² power balance code results — `proprietary` — **blocking** for Q and power balance numbers
+- Quantitative reactor parameters (Q, power output, plasma density/temperature operating point) — `proprietary`/`not-yet-sourced` — **blocking**
+- Full text of key physics papers (especially Ochs & Fisch 2024 on breakeven requirements, Ochs et al. 2022 on hybrid p-B11 scheme) that contain internal quantitative performance estimates — `not-yet-sourced` — **important**
+- Company technical disclosure or investor materials from Pale Blue Fusion — `proprietary` — **important**
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Good (qualitatively)
+**Coverage**: Partial (physics challenges well-documented; engineering modeling path absent)
 
 **Available**:
-- Clear description of why thermal p-B11 fails (bremsstrahlung, helium poisoning) and why CHARM's nonthermal approach is needed [ARPA-E presentation]
-- Alpha channeling mechanism well-described: RF waves in ICR range extract energy from fusion-born helium and redirect to fuel protons
-- Multi-chamber architecture described: fusion chamber + heat exchange chamber + plug [slides 4, 6]
-- Nine open research questions from the 2021 grant proposal — shows what was unknown at project start
-- Summary of "derisked questions" as of July 2025 — shows what the team claims is resolved computationally
-- Power balance structure: external heating P_H, alpha channeling efficiency η_α, DEC recovery — schematic only
-- S5 PIC code: XB mode conversion simulation mentioned but results not detailed in sources
+- Detailed physics rationale for why a thermal p-B11 plasma cannot work (bremsstrahlung losses exceed fusion power, helium poisoning) — well-covered in ARPA-E presentation and papers
+- Description of the five-mechanism solution stack: centrifugal species separation, alpha channeling (RF waves in ICR range), ponderomotive barriers, multi-chamber architecture, biased electrode for rotation establishment
+- Acknowledgment that the team has answered 9 derisking questions theoretically/computationally but has not yet validated that these components work together self-consistently
+- Clear identification of recirculating power as a critical unknown ("engineering Q" must exceed 0 — but no quantitative estimate given)
+- Synchrotron radiation identified and addressed theoretically (manageable via reabsorption)
 
 **Missing**:
-- Quantified efficiency for each subsystem (alpha channeling efficiency η_α, DEC efficiency, rotation drive efficiency)
-- Plasma parameter operating point (temperature, density, confinement time, mirror ratio) for the reactor design
-- Bremsstrahlung and synchrotron radiation management numbers (qualitative reassurance given but no quantified loss fractions)
-- End-to-end power balance with numbers
+- No systems-level integration analysis showing how the five mechanisms interact in a closed power loop
+- No RF system sizing (antenna type, power, frequency for alpha channeling at reactor scale)
+- No direct energy converter engineering design — only theoretical efficiency bounds from PRX Energy 2025 paper
+- No electrode design for high-voltage rotation establishment (Patent 19/175,473 covers "ultra-high DC voltages" but engineering detail not public)
+- No first-wall / plasma-facing component design (charged particle flux from mirror losses poses engineering challenge even without neutrons)
+- No quantitative recirculating power budget
 
 **Gaps**:
-- Quantified plasma operating point (T, n, τ, Q) — `proprietary` (exists in (PB)² but unpublished) — **blocking** for any LCOE model
-- Alpha channeling efficiency η_α — `not-yet-sourced` (likely in one of the 29 papers not fully read) — **blocking**
-- Net electrical efficiency end-to-end — `truly-unknown` at this stage — **blocking**
-- Synchrotron radiation loss fraction — `not-yet-sourced` (paper likely exists in the 29; Ochs & Fisch 2024 "Lowering reactor breakeven" may contain this) — **important**
+- Recirculating power fraction (RF heating + DEC round-trip efficiency) — `truly-unknown` at system level — **blocking**; this is the central viability question for p-B11
+- Self-consistent integrated power balance at reactor scale — `truly-unknown` — **blocking**
+- RF antenna / wave-coupling system engineering — `truly-unknown` — **important**
+- Plasma-facing component and end-loss collector engineering — `truly-unknown` — **important**
+- Whether DEC approach is SWDEC (2023 patent) or adiabatic (2025 PRX Energy paper) — `proprietary` — **nice-to-have** (either way, DEC is assumed; efficiency range can be bounded)
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
-**Coverage**: Partial
+**Coverage**: Poor
 
 **Available**:
-- Overall concept: TRL 1–2 confirmed — theoretical with computational validation only; no Pale Blue hardware exists
-- Centrifugal mirror confinement physics: TRL 3 via CMFX (UMD), which demonstrated first plasma Oct 2022 and reported fusion yield measurements (arXiv:2505.23047, 2025) — validates the underlying centrifugal mirror physics
-- Alpha channeling (wave-particle interaction): TRL 2 — theoretical and computational only (S5 PIC code), no experimental demonstration in rotating mirror geometry
-- Ponderomotive barriers: TRL 2 — theoretical treatment published (Rubin & Fisch 2025), not experimentally demonstrated
-- Direct energy conversion (adiabatic DEC): TRL 1–2 — theoretical framework published (PRX Energy 2025), no prototype
-- Multi-chamber species separation: TRL 1–2 — theoretical (Ochs, Kolmes & Fisch 2025 ash poisoning paper), not demonstrated
-- Biased central electrode: TRL 3 via CMFX (rotational confinement at 100 kV demonstrated)
-- Magnets: TRL unassessable — conductor technology not specified by Pale Blue
+- Centrifugal mirror physics: validated at CMFX (UMD, separate group) — general confinement physics TRL 3–4, but the CHARM multi-chamber architecture is undemonstrated
+- Alpha channeling in mirror machines: theoretical TRL 3 (Fisch 2006 landmark paper, confirmed in simulations); no experimental demonstration in a rotating plasma
+- Ponderomotive barriers in rotating plasma: theoretical TRL 3 (published papers, patents); no experimental demonstration
+- Direct energy conversion (adiabatic, axisymmetric): theoretical TRL 2–3 (PRX Energy 2025 paper); no experimental hardware
+- Biased electrode for E×B rotation: TRL 4–5 in non-fusion plasma contexts (the CMFX experiment at UMD uses 100 kV, 100 kW power supply as of May 2024)
 
 **Missing**:
-- Any Pale Blue-specific experiment or prototype — none exists
-- TRL assessment for reactor-scale magnet system
-- Vacuum vessel, first wall, and structural design — no engineering work published
+- No TRL assessment for any subsystem has been published by the team
+- No magnet technology specified → no magnet TRL or cost anchor
+- No RF system hardware (antenna, power conditioning) for alpha channeling at any scale
+- No integrated device demonstrating even one chamber of the CHARM concept
 
 **Gaps**:
-- Pale Blue experimental program (devices, milestones, timelines) — `proprietary` — **important** for TRL narrative
-- Magnet technology choice — `proprietary` — **important** (affects cost analogy selection)
-- RF antenna/launcher design for alpha channeling — `truly-unknown` at this stage — **nice-to-have**
+- Magnet type and TRL — `proprietary` (likely an engineering decision not yet made) — **important** for cost
+- Alpha channeling experimental validation — `truly-unknown` at present in rotating mirror; experimental work is future work for Pale Blue Fusion — **blocking** for any credible physics Q estimate
+- Full CHARM architecture experimental demonstration — `truly-unknown` — **blocking** at concept level
+- DEC hardware TRL — `truly-unknown` for their specific approach — **important**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Poor
+**Coverage**: Partial (aneutronic advantages clear; engineering material needs absent)
 
 **Available**:
-- Fuel: p-B11 explicitly described as "cheap and non-radioactive" — boron is abundant, naturally occurring, no supply chain concern [ARPA-E presentation slide 1]
-- No tritium required (aneutronic) — eliminates the most critical supply chain constraint facing D-T concepts
-- No breeding blanket required — eliminates Li-6 and beryllium supply concerns
-- CMFX uses LTS (repurposed MRI) magnets — provides a lower-bound cost analogue for small experiment scale
+- Fuel: p (proton from water/hydrogen — abundant, no supply chain concern) and B-11 (naturally 80% of boron, cheap and non-radioactive) — explicitly cited as advantages
+- No tritium: eliminates Li-6, Be breeding blanket, and tritium handling entirely
+- No significant neutron flux: eliminates activation constraints on structural materials, allows conventional steel/aluminum structures in principle
+- No waste storage: no long-lived activation products
 
 **Missing**:
-- Magnet conductor technology for reactor-scale device (HTS vs. LTS vs. normal conducting — unspecified)
-- First wall / vacuum vessel material (no engineering design exists)
-- RF antenna materials and lifetime (critical given plasma-facing duty cycle)
-- Electrode material and lifetime (central electrode at high voltage in plasma environment)
+- Magnet conductor material and supply chain — completely unknown since magnet type unspecified; if HTS (REBCO tape), supply chain considerations apply; if LTS (NbTi/Nb₃Sn), mature supply exists
+- RF antenna and power conditioning materials — not specified
+- High-voltage electrode materials for sustained 100 kV operation in plasma — `not-yet-sourced`; relevant research exists in the plasma propulsion and centrifugal mirror communities but not cited
+- Vacuum vessel materials — not addressed
 
 **Gaps**:
-- Magnet conductor specification — `proprietary` (company hasn't chosen yet) — **important** for cost modeling (HTS vs. LTS is order-of-magnitude cost difference for mirrors)
-- Electrode material and replacement schedule — `truly-unknown` — **important** (the biased central electrode is a novel plasma-facing component with no clear analogue)
-- RF antenna/launcher materials — `truly-unknown` — **nice-to-have**
-- Vacuum vessel and structural material — `truly-unknown` at this stage — **nice-to-have** (standard materials likely, but no basis to specify)
+- Magnet conductor material identity — `proprietary`/`not-yet-sourced` — **important**
+- Electrode materials for sustained high-voltage plasma operation — `not-yet-sourced` — **nice-to-have**
+- (No blocking supply chain gaps identified beyond magnet uncertainty; the aneutronic fuel cycle removes the most severe supply chain constraints present in D-T concepts)
 
 ---
 
@@ -116,72 +114,84 @@
 **Coverage**: Poor
 
 **Available Parameters**:
+
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Fuel cycle | p-B11, no breeding, no tritium | ARPA-E presentation | high |
-| Operation mode | Steady-state | ARPA-E presentation | high |
-| Aneutronic fraction | <1% neutron energy | ARPA-E presentation; p-B11 physics | high |
-| Confinement reduction factor (alpha channeling) | 2.6× (thermal) to 6.9× (fast proton) improvement in required τ_E | Ochs & Fisch 2024, technical-papers-summary.md | medium |
-| Capacity factor (implied) | ~90% (steady-state, no pulsed downtime) | Derived from steady-state operation | low |
-| DEC efficiency framework | Adiabatic DEC in axisymmetric fields — theoretical framework | PRX Energy 2025 (Rax, Kolmes, Fisch) | low |
+| Fuel type | p-B11 (proton + boron-11) | ARPA-E 2025 presentation | high |
+| Fuel cost | Near-zero (abundant, non-radioactive) | ARPA-E 2025 presentation | high |
+| Tritium breeding cost | None (N/A) | ARPA-E 2025 presentation | high |
+| Neutron shielding cost | Minimal | ARPA-E 2025 presentation | high |
+| Operation mode | Steady-state | Dossier / presentation | high |
+| Energy capture type | Direct (charged particle) — adiabatic DEC or SWDEC | Dossier / PRX Energy 2025 | medium |
+| DEC theoretical efficiency bound | Studied in PRX Energy 2025 (axisymmetric limits) | PRX Energy 4, 013007 (2025) | low — theoretical only |
+| Recirculating power concept | Alpha channeling recycling fraction η_α into proton heating; radial E-field energy recoverable | ARPA-E 2025 slides 5, 14, 19 | low — no system-level number |
+| Engineering Q requirement | Must exceed 0 (breakeven); lowered by factor 2.6–6.9 via alpha channeling | Technical papers summary / Ochs & Fisch 2024 | low — qualitative bounds only |
 
 **Missing Parameters**:
+
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Q (fusion gain) / net gain | proprietary | blocking | (PB)² code exists but results unpublished |
-| Plant electrical output target (MWe) | truly-unknown | blocking | No plant study |
-| Capital cost — magnet system | proprietary/truly-unknown | blocking | Conductor not specified; no reactor design |
-| Capital cost — vacuum vessel / structural | truly-unknown | blocking | No engineering design |
-| Capital cost — DEC system | truly-unknown | blocking | No prototype, no cost study |
-| Capital cost — RF system (alpha channeling) | truly-unknown | blocking | No antenna design |
-| Capital cost — balance of plant | truly-unknown | blocking | No plant study |
-| DEC electrical efficiency (%) | not-yet-sourced | blocking | PRX Energy 2025 may contain theoretical bounds — paper not fully read |
-| Alpha channeling efficiency η_α (%) | not-yet-sourced | blocking | Likely in one of the 29 publications |
-| Plasma temperature operating point | proprietary | blocking | Needed to compute bremsstrahlung losses |
-| Plasma density operating point | proprietary | blocking | Needed for fusion power density |
-| Mirror ratio / device dimensions | truly-unknown | blocking | No reactor design disclosed |
-| Component replacement schedule | truly-unknown | important | No engineering design |
-| Operating cost — electrode replacement | truly-unknown | important | Novel plasma-facing component |
-| Maintenance approach (remote vs. contact) | truly-unknown | important | No engineering work |
-| Recirculating power fraction | proprietary | blocking | RF drive + rotation maintenance power not quantified |
+| Net electric power output (MWe) | truly-unknown | blocking | No plant study; no target disclosed |
+| Target engineering Q value | truly-unknown | blocking | 0D PB² code exists internally but results not published |
+| Capital cost by CAS subsystem | truly-unknown | blocking | No plant study; no engineering design |
+| Magnet system cost | not-yet-sourced / derivable | blocking | Magnet type not specified; if HTS solenoidal, REBCO cost models exist |
+| RF system cost (alpha channeling) | truly-unknown | blocking | Novel application; no cost analogue |
+| Direct energy converter cost | truly-unknown | blocking | Novel hardware; no commercial DEC exists for mirror geometry |
+| Recirculating power fraction (system level) | truly-unknown | blocking | The central viability question; only theoretical components available |
+| Balance of plant cost | derivable | important | Standard thermal/electrical BOP; ALPHA costing study (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) provides ~$500M BOP analog for ~500 MWe |
+| O&M costs | derivable | important | Aneutronic → no tritium handling, no waste management; analogs from MFE plant studies apply for staffing/maintenance |
+| Capacity factor | derivable | important | Steady-state, aneutronic → no blanket replacement outages, no tritium inventory limit; theoretical CF likely high (>90%?) but no engineering basis stated |
+| Thermal/electrical conversion efficiency | not-yet-sourced | important | DEC efficiency is the key parameter; theoretical bounds exist in PRX Energy 2025 but system-level number requires engineering |
+| Plasma density and temperature operating point | not-yet-sourced | important | PB² code produces these internally; some bounds visible in published papers (relativistic regime ~GK temperatures) |
+| First wall / end collector cost | truly-unknown | important | No design; charged particle flux from mirror losses must be managed |
+| Electrode power supply cost | not-yet-sourced | important | High-voltage rotating plasma bias (100 kV+ at reactor scale); CMFX uses 100 kW supply at experiment scale |
 
 ---
 
 ## Source Recommendations
 
-1. **PRX Energy 2025 (Rax, Kolmes, Fisch) — full text**: Read to extract DEC efficiency bounds and operating parameter ranges. This is the most engineering-adjacent paper in the corpus and likely contains quantitative efficiency estimates useful for LCOE parameterization. *Source confirmed in dossier as Rax, Kolmes & Fisch, PRX Energy 4, 013007 (2025).*
+1. **Full text of Ochs & Fisch (2024), "Lowering the reactor breakeven requirements for proton-Boron 11 fusion," Physics of Plasmas 31, 012503** — contains quantitative breakeven analysis with power balance ratios. Should be ingested via Zotero. `not-yet-sourced` — this paper exists and would provide the most authoritative public Q estimate.
 
-2. **Ochs & Fisch 2024 — "Lowering the reactor breakeven requirements for p-B11 fusion"** (Phys. Plasmas 31, 012503): Full text likely contains plasma parameter requirements (τ_E, T, n) needed for the power balance — these are the closest thing to a device operating point in the public record. *Source confirmed in dossier and technical-papers-summary.md.*
+2. **Full text of Ochs et al. (2022), "Improving the Feasibility of Economical Proton-Boron 11 Fusion via Alpha Channeling," Phys. Rev. E 106, 055215** — contains quantitative alpha channeling efficiency estimates (η_α) that directly feed recirculating power calculations. `not-yet-sourced`.
 
-3. **arXiv:2502.13300 (Ochs, Kolmes, Fisch 2025 — ash poisoning paper)**: May contain plasma parameter assumptions for the multi-chamber design. *Source confirmed in dossier.*
+3. **Full text of Rax, Kolmes & Fisch (2025), "Efficiency and Physical Limitations of Adiabatic Direct Energy Conversion in Axisymmetric Fields," PRX Energy 4, 013007** — DEC efficiency bounds from the core team; essential for any recirculating power model. `not-yet-sourced`.
 
-4. **CMFX fusion yield paper (arXiv:2505.23047, 2025)**: May contain centrifugal mirror performance data (confinement, density, temperature achieved) useful as an experimental lower bound. *Source confirmed in dossier.*
+4. **CMFX publications (arXiv:2505.23047 — fusion yield measurements, 2025)** — while CMFX is a separate group, the centrifugal mirror plasma parameters (density, rotation speed, confinement time) achieved experimentally provide the closest available validation data for mirror plasma physics at the experiment scale. `not-yet-sourced`.
 
-5. **Search for analogous centrifugal mirror power plant studies**: The TAE (field-reversed + beams) and WHAM/Wisconsin centrifugal mirror projects have done some system-level work. A search for "centrifugal mirror power plant study" or "rotating mirror reactor economics" on OSTI or arXiv may find relevant analogues. *Existence unverified — confirm before searching.*
+5. **Revisit of 2017 ARPA-E ALPHA Concepts costing** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) — already ingested. Covers four compact modular fusion concepts with CAS-level cost breakdowns at ~500 MWe. The BOP costs (~$500M of ~$1.2B total CapEx) and LCOE methodology (43 $/MWh average) are applicable as analog for balance-of-plant estimation even though none of the four concepts is a mirror. Useful for non-fusion-core LCOE parameters.
 
-6. **Search for generic magnetic mirror reactor cost studies**: Pre-1990 DOE mirror fusion studies (MFTF-B, tandem mirror reactor) contain capital cost structures for mirror geometry that could provide analogues for magnets and vacuum vessel. Search OSTI for "tandem mirror reactor cost" or "magnetic mirror power plant economics." *Existence unverified — confirm before searching; note technology era gap.*
+6. **Pale Blue Fusion company materials** — once the website launches (announced July 2025 as "coming soon"). Monitor palebluefusion.com. `proprietary` gap — may partially resolve with company launch. Flag as `unverified — confirm existence before searching`.
 
-7. **Pale Blue Fusion company disclosures (post-July 2025)**: A targeted search for "Pale Blue Fusion" news, FIA membership, or investment announcements in late 2025 / early 2026 may reveal company status, first device milestones, or technical disclosures. The July 2025 presentation confirmed incorporation was imminent. *Not yet searched per dossier.*
+7. **Search OSTI and arXiv for "centrifugal mirror" + "power balance" or "reactor study"** — there may be pre-2021 reactor studies on centrifugal mirror concepts (e.g., Gas Dynamic Trap at Novosibirsk, Budker Institute work) that provide relevant plasma parameter ranges. `unverified — confirm existence before searching`.
+
+8. **TAE Technologies or other p-B11 company publications** — TAE (tri-alpha energy) targets p-B11 with a different architecture (FRC) but their published power balance analyses may provide boundary conditions on the p-B11 challenge (bremsstrahlung wall, minimum Q requirements). `not-yet-sourced` for the specific plasma physics constraints shared across all p-B11 approaches.
 
 ---
 
 ## Summary
 
-**Proceed to full analysis with explicit caveat framing.** The qualitative sections (data availability, system function challenges, maturity) can be written with substance — the 29 papers and ARPA-E presentation provide enough to construct a rigorous narrative about why CHARM is physically interesting and where the major uncertainties lie. The materials section will be thin but honest.
+The available data is insufficient to produce a high-quality D1+ concept analysis at this time. The concept sits firmly in the theoretical physics stage — 29 strong peer-reviewed papers establish the physics rationale and de-risk individual components, but no engineering design, plant study, experimental results from the CHARM architecture, or system-level power balance output has been published. Every LCOE parameter beyond fuel cost and operation mode requires either pure assumption or analog borrowing from unrelated concepts.
+
+**Before proceeding to full analysis**, the recommended path is:
+1. Ingest the three key physics papers (Ochs & Fisch 2024; Ochs et al. 2022; Rax et al. 2025 PRX Energy) — these contain the closest available approximation to a public power balance.
+2. Ingest CMFX 2025 experimental results for physics validation context.
+3. Check palebluefusion.com for any launched technical content.
 
-The quantitative LCOE model will require the analyst to construct almost every parameter from analogy or assumption — there are essentially no published capital cost estimates, no confirmed operating point, and no efficiency numbers for the novel subsystems (DEC, alpha channeling, rotation maintenance). Before coding, it is worth pulling the full text of the PRX Energy 2025 paper and the Ochs & Fisch 2024 breakeven paper, as these are the most likely sources of usable quantitative bounds. The back-solve to $0.01/kWh section may end up being the most informative part of the analysis, since this concept's case for competitive LCOE rests entirely on theoretical claims (no neutron damage, no tritium, direct energy conversion) that can be explored parametrically even without confirmed numbers.
+With those additions, a qualitative analysis can be written with well-documented physics context and honest uncertainty bounds. A quantitative LCOE model would be almost entirely parameterized on assumptions, with only fuel cost, steady-state operation, and aneutronic advantages as concept-specific anchors.
+
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Significant Gaps"
-blocking_count: 13
-important_count: 3
-counting_method: "section_5_missing_parameters"
+overall_rating: "Insufficient Data"
+blocking_count: 8
+important_count: 9
+counting_method: "section_5_missing_parameters (6 blocking LCOE params) + sections_1_through_4 unique blocking gaps (recirculating power fraction, alpha channeling experimental validation, self-consistent integrated power balance) deduplicated; important counts all non-blocking important gaps across sections 1-5 deduplicated"
 section_coverage:
-  availability_of_data:       "Limited"
-  system_function:            "Good (qualitatively)"
-  subsystem_maturity:         "Partial"
-  materials_supply_chain:     "Poor"
+  availability_of_data:       "Poor"
+  system_function:            "Partial"
+  subsystem_maturity:         "Poor"
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
