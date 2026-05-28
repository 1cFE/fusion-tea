# Diff: 18-p-b11-frc

**Generated:** 2026-05-22T10:31:57-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 8 | 5 | -3 |
| important_count  | 5 | 6 | - |
| overall_rating   | Mostly Ready (with significant quantitative constraints) | Significant Gaps | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
152:3. **FRC/compact confinement cost analogs**: The ARPA-E ALPHA revisit study (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) covers compact confinement concepts in a CAS framework. While none of the four concepts is a p-B11 FRC, the methodology and BOP/indirect cost structure are directly applicable. Recommend reading this source.
```

## Blocking-tier lines (baseline)

```
34:- No published plant study — `proprietary` — **blocking** for quantitative LCOE; must rely on analogues
36:- No published system code or power balance study — `proprietary` — **blocking** for recirculating power and net efficiency
57:- Q value (fusion gain) for Da Vinci — `proprietary` — **blocking** for any LCOE model; must assume or bracket
58:- NBI wall-plug efficiency at reactor-relevant energies — `not-yet-sourced` — **blocking** for recirculating power calculation; NBI literature exists but TAE specifics are proprietary
59:- Recirculating power fraction — `derivable` from NBI efficiency assumptions + power balance — **blocking** if not derived
61:- Alpha particle confinement in FRC at burn temperatures — `truly-unknown` (open physics question) — **blocking** for high-fidelity analysis; use TBD/range approach
143:| Q value / fusion gain (Da Vinci) | proprietary | blocking | No public statement; C-2W is far sub-breakeven; must bracket (e.g., Q=2–10) |
144:| NBI wall-plug efficiency at reactor scale | not-yet-sourced | blocking | Determines recirculating power; current C-2W NBI is 13 MW input; Da Vinci NBI scale/efficiency unknown |
145:| Recirculating power fraction | derivable | blocking | Must derive from Q + NBI efficiency assumptions; dominates net LCOE for beam-driven concepts |
146:| Total plant capital cost | proprietary | blocking | No estimate published; no plant study exists; will need analogue-based estimate |
147:| Capital cost by subsystem (CAS breakdown) | proprietary | blocking | No published breakdown; rough analogues only |
148:| O&M cost estimate | proprietary | blocking | No published data; must estimate from fusion plant analogues |
154:| Plant construction cost (Da Vinci) | proprietary | blocking | Only "smaller and less expensive" claims; no dollar figure |
156:| Alpha particle confinement fraction in FRC | truly-unknown | blocking | Required for effective Q calculation; open physics research question |
```

## Blocking-tier lines (new)

```
34:- No plant study or TEA for TAE concept — `proprietary` — **blocking**: no cost basis without this
58:- NBI wall-plug efficiency at reactor scale (15–40 keV vs. needed MeV-class?) — `proprietary/truly-unknown` — **blocking**: determines whether net energy is even physically achievable at any Q
59:- Q_plasma target for Da Vinci not published — `proprietary` — **blocking**: required for all recirculating power calculations
60:- Bremsstrahlung loss balance vs. fusion power at 250 keV — `truly-unknown` (active physics research) — **blocking**: fundamental physics question, not yet answered
83:- p-B11 net energy gain (Q > 1) — `truly-unknown` — **blocking**: the single most fundamental unresolved issue
84:- NBI at reactor scale and energy (>40 keV for efficient p-B11 heating) — `not-yet-sourced` / `derivable from accelerator literature` — **blocking** for cost modeling
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/18-p-b11-frc.md	2026-05-22 09:21:13.860164179 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/18-p-b11-frc/gap_report.md	2026-05-22 10:31:57.171833801 -0700
@@ -1,190 +1,187 @@
-Now I have everything I need. Let me write the assessment.
+I now have enough information to write the full gap assessment.
 
 ---
 
-# Gap Assessment: p-B11 FRC
+# Gap Assessment: p-B11 FRC (p-B11)
 
 ## Overall Readiness
-**Rating**: Mostly Ready (with significant quantitative constraints)
-**Summary**: TAE Technologies is unusually transparent for a private fusion company — public press releases, a 2025 Nature Communications paper, multiple New Atlas interviews, and a detailed FAQ provide solid coverage of concept architecture and physics strategy. The qualitative write-up can be produced at high quality. However, the quantitative LCOE model will be severely constrained: no plant cost study exists, no Q value or power balance has been published, and the physics gap between current experiments (~1 keV electrons, 40 ms lifetimes) and Da Vinci targets (~250 keV ions, sustained) is multi-order-of-magnitude and not publicly bridged. LCOE modeling will require heavy use of analogues and explicit assumptions about parameters that are either proprietary or genuinely unknown.
+**Rating**: Significant Gaps
+**Summary**: The available data is unusually rich on plasma physics and machine design at the experimental scale (C-2W/Norman), with over 200 peer-reviewed publications, and the concept is well-characterized for the differentiation taxonomy. However, no published cost estimates, plant study, or techno-economic analysis exists for Da Vinci, the commercial prototype. More critically, p-B11 net energy gain has never been demonstrated—current devices operate at electron temperatures of ~1 keV versus the ~100–250 keV ion temperature required—creating a fundamental physics-to-economics uncertainty that propagates into every LCOE parameter. A qualitative analysis can be excellent; quantitative LCOE modeling requires heavily assumption-laden analogues.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Moderate
+**Coverage**: Partial
 
 **Available**:
-- Machine architecture and concept physics: well-covered by Grokipedia summary, Nature Comm 2025 paper, TAE FAQ, and C-2W machine details
-- Development roadmap and timeline: DJT merger announcement provides construction (2026), first plasma (2029), net energy (2030), power ops (2031)
-- Plant size targets: 50 MWe initial, 350–500 MWe at scale (ANS Nuclear Newswire, DJT merger)
-- Company financials: $1.2–1.3B raised, DJT merger >$6B valuation, 2,500+ patents
-- NBI system: eight-injector spec, 13 MW at 15–40 keV (C-2W), formation breakthrough in Nature Comm 2025
-- Energy conversion pathway: thermal/steam confirmed for Da Vinci (TAE FAQ); ICC patents documented (US7459654, US6628740, US6888907)
-- p-B11 fuel cycle: physics well-known; 2023 first magnetically-confined p-B11 fusion (with NIFS Japan)
+- TAE has published 200+ peer-reviewed papers in *Nature Communications*, *Nuclear Fusion*, *Physical Review Letters*, and others (`grokipedia-tae-technologies.md`; `osti-pages-servlets-purl-2441289.md`). Physics research is unusually transparent for a private company.
+- The 2025 *Nature Communications* NBI-only FRC formation paper provides peer-reviewed confirmation of a major physics milestone (`nature-articles-s41467-025-58849-5.md`).
+- The 2024 *Nuclear Fusion* C-2W enhanced performance paper provides detailed machine parameters, subsystem descriptions, and plasma performance data (`osti-pages-servlets-purl-2441289.md`).
+- Da Vinci commercial specs (50 MWe initial, 350–500 MWe at scale, thermal steam conversion) confirmed in public announcements (`tae-djt-merger-davinci-specs.md`; `tae-energy-conversion-clarification.md`).
+- Company funding history, roadmap, and milestone structure well documented (`grokipedia-tae-technologies.md`).
+- Fuel cycle physics (p-B11, 8.7 MeV, 3α products, aneutronic) fully established and uncontroversial.
+- National lab collaborations (Argonne, PPPL, NIFS Japan) provide independent corroboration of key claims.
 
 **Missing**:
-- Peer-reviewed engineering or plant design papers (only one physics paper; no system code publications)
-- Published cost estimates or techno-economic analysis for Da Vinci
-- Investor technical presentations (likely contain more detail; not publicly available)
-- Engineering design documents for Da Vinci (none published)
+- No published techno-economic analysis or plant study for Da Vinci or any TAE commercial concept.
+- No cost breakdown by subsystem published anywhere in the literature.
+- No independent third-party LCOE estimate.
+- Published plasma performance data for C-2W/Norman exists, but performance at Da Vinci scale (>>1 keV temperature, Q > 1) has never been demonstrated by anyone.
 
 **Gaps**:
-- No published plant study — `proprietary` — **blocking** for quantitative LCOE; must rely on analogues
-- No peer-reviewed papers on Da Vinci engineering design — `proprietary/not-yet-sourced` — **important** for subsystem TRL assessment
-- No published system code or power balance study — `proprietary` — **blocking** for recirculating power and net efficiency
+- No plant study or TEA for TAE concept — `proprietary` — **blocking**: no cost basis without this
+- No independent validation of commercial claims (50% cost reduction vs tokamak) — `proprietary` — **important**
+- Copernicus intermediate device skipped in updated plans; performance data gap between Norman and Da Vinci — `proprietary` — **important**
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Partial
+**Coverage**: Good (qualitatively); Poor (quantitatively)
 
 **Available**:
-- High-level identification of novel subsystems: NBI-only formation (new), ICC direct conversion (patented but not deployed), X-ray capture (early research)
-- Known physics challenge: p-B11 requires ~100–250 keV plasma temperatures; C-2W achieves ~1 keV electrons — a ~2-order-of-magnitude gap
-- Energy conversion tension: steam turbine (Da Vinci baseline) vs. ICC (future) — sources resolve this clearly
-- NBI as quadruple-duty system (formation, heating, current drive, stabilization) is well-documented
+- p-B11 reaction requirements thoroughly documented: ~600 keV cross-section peak, 100–250 keV ion temperature needed, bremsstrahlung losses are severe at these temperatures (`grokipedia-tae-technologies.md`; patent US7459654B2).
+- NBI quadruple-duty function (formation, heating, current drive, stabilization) is well characterized; machine physics is well understood from C-2W publications.
+- FRC stability challenges (tilt mode, rotational instability, anomalous transport) documented in `grokipedia-tae-technologies.md` and the Nature Communications paper.
+- Recirculating power fraction problem identified: the 2021 arxiv paper (`arxiv-2103-12451.md`) specifically analyzes how high recirculated power + low capacity factor devastates plant efficiency—directly applicable to NBI-sustained FRC.
+- Edge biasing requirement for MHD stabilization creates additional recirculating power load (described in detail in `osti-pages-servlets-purl-2441289.md`).
+- Energy conversion path confirmed: thermal/steam for Da Vinci, with ICC as future research option.
 
 **Missing**:
-- Recirculating power fraction: NBI wall-plug efficiency at reactor scale (~10–30% typical for NBIs; critical for p-B11 power balance) — not in any source
-- Q value target for Da Vinci: nowhere stated publicly; C-2W is orders of magnitude below Q=1
-- Alpha particle confinement efficiency in FRC geometry at reactor temperatures
-- Soft X-ray energy fraction: p-B11 produces significant bremsstrahlung and synchrotron losses; how these are handled in Da Vinci's heat balance is not discussed
-- Detailed power flow model (NBI in → plasma heating losses → fusion alpha energy → thermal/steam extraction → net electricity)
+- Wall-plug efficiency of NBI at Da Vinci scale and energies (~MeV-class for p-B11 fuel) not published.
+- Q value target for Da Vinci not stated in any source.
+- Recirculating power fraction at reactor scale not calculable from available data.
+- Whether bremsstrahlung losses can actually be managed at 250 keV plasma temperature to permit net energy remains a deep open question in the physics literature—not specific to TAE.
 
 **Gaps**:
-- Q value (fusion gain) for Da Vinci — `proprietary` — **blocking** for any LCOE model; must assume or bracket
-- NBI wall-plug efficiency at reactor-relevant energies — `not-yet-sourced` — **blocking** for recirculating power calculation; NBI literature exists but TAE specifics are proprietary
-- Recirculating power fraction — `derivable` from NBI efficiency assumptions + power balance — **blocking** if not derived
-- X-ray/bremsstrahlung losses at 250 keV — `derivable` from p-B11 physics — **important**; this is the key loss channel for aneutronic p-B11 and substantially degrades effective Q
-- Alpha particle confinement in FRC at burn temperatures — `truly-unknown` (open physics question) — **blocking** for high-fidelity analysis; use TBD/range approach
+- NBI wall-plug efficiency at reactor scale (15–40 keV vs. needed MeV-class?) — `proprietary/truly-unknown` — **blocking**: determines whether net energy is even physically achievable at any Q
+- Q_plasma target for Da Vinci not published — `proprietary` — **blocking**: required for all recirculating power calculations
+- Bremsstrahlung loss balance vs. fusion power at 250 keV — `truly-unknown` (active physics research) — **blocking**: fundamental physics question, not yet answered
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
-**Coverage**: Partial
+**Coverage**: Good (experimental scale); Poor (reactor scale)
 
 **Available**:
-- NBI system (experimental scale): well-characterized at 13 MW, 15–40 keV; TRL ~6 for current implementation
-- FRC plasma formation (NBI-only): demonstrated on Norm (2025); TRL ~4–5 for NBI-only approach
-- p-B11 fusion in magnetically confined plasma: first demonstration 2023 (with NIFS); TRL ~2–3
-- Steam turbine BOP: commercial technology, TRL ~9
-- Copper/resistive coil magnets for FRC equilibrium: demonstrated on C-2W/Norman; TRL ~6
+- C-2W machine hardware comprehensively described: 8 NBI injectors (15–40 keV tunable, 13 MW), Inconel CV, resistive copper coil magnet system, divertor cryogenic pumping, Thomson scattering diagnostics (`osti-pages-servlets-purl-2441289.md`).
+- NBI system: TRL ~6-7 for current machine (13 MW demonstrated, 40 ms pulse, real-time feedback control).
+- FRC formation via NBI-only: TRL ~5-6 (demonstrated on Norman, first of its kind; `nature-articles-s41467-025-58849-5.md`).
+- Plasma confinement at 1 keV electron temperature for 40 ms: demonstrated.
+- Balance of plant (steam turbine): TRL 9 (fully mature technology, no innovation needed).
+- ICC direct energy conversion: TRL 3-4 (patents granted, concept validated theoretically, not demonstrated at scale).
 
 **Missing**:
-- NBI at reactor-relevant energies: Da Vinci will need MeV-range beams for p-B11 (vs. 15–40 keV on C-2W); no sources address this upgrade path
-- ICC direct conversion hardware: only patents and theoretical descriptions; no prototype demonstrated
-- Da Vinci magnet design: unconfirmed whether resistive or superconducting at reactor scale
-- First wall materials for high-X-ray aneutronic environment: not discussed in any source
-- Divertor/exhaust system for FRC at reactor scale: FRC's open-field-line exhaust is a known challenge; not addressed in sources
-- High-temperature plasma sustainment: C-2W achieves ~1 keV; Da Vinci needs ~250 keV — the intermediate steps are entirely unspecified
+- Plasma confinement at reactor-relevant ion temperatures (~100–250 keV): **not demonstrated anywhere**. Current C-2W achieves ~few keV ion temperatures, approximately 2 orders of magnitude below Da Vinci target.
+- NBI system scaled to Da Vinci power levels (tens of MW at higher energies than current 15–40 keV): TRL 2-3 at required scale.
+- First wall / vacuum vessel material and lifetime at near-aneutronic neutron flux (secondary reactions): not characterized for Da Vinci.
+- Electrode biasing system at reactor scale and duration: not published.
+- Plasma Q > 1 achievement: not demonstrated for any FRC or p-B11 system.
 
 **Gaps**:
-- High-energy NBI at reactor scale (MeV-range) — `not-yet-sourced` — **important**; ITER NBI and SNL neutral beam literature may provide analogues
-- ICC prototype/TRL — `proprietary` — **important** for long-term cost modeling; treat as speculative future upgrade
-- Da Vinci magnet design specification — `proprietary` — **important**; low impact given FRC's near-unity beta, but needed for completeness
-- First wall materials spec — `proprietary` — **important**; X-ray and alpha bombardment environment differs substantially from D-T
-- FRC divertor at reactor scale — `not-yet-sourced` — **important**; FRC open field line exhaust design is an active research area
+- p-B11 net energy gain (Q > 1) — `truly-unknown` — **blocking**: the single most fundamental unresolved issue
+- NBI at reactor scale and energy (>40 keV for efficient p-B11 heating) — `not-yet-sourced` / `derivable from accelerator literature` — **blocking** for cost modeling
+- First wall lifetime and replacement schedule for Da Vinci — `proprietary` — **important**
+- Electrode biasing system cost and longevity at reactor scale — `proprietary` — **nice-to-have**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Poor
+**Coverage**: Good (qualitatively)
 
 **Available**:
-- Fuel: hydrogen (abundant) and boron-11; TAE notes fuel is "virtually inexhaustible"
-- No tritium required — explicitly documented; eliminates Li-6, Li breeding blanket
-- No heavy neutron shielding — documented; hands-on maintenance possible
-- Copper coils for current machines (standard, no special supply chain)
-- TAE holds 2,500+ patents, suggesting significant proprietary manufacturing IP
+- Boron-11: ~80% of natural boron, globally abundant in borax deposits (Chile, Turkey, USA). No critical supply constraint. Commodity industrial chemical (`grokipedia-tae-technologies.md`).
+- Hydrogen (proton fuel): completely abundant, no supply issues.
+- No tritium requirement: major structural simplification; eliminates tritium processing, breeding blankets, and tritium supply chain entirely.
+- No HTS/superconducting magnet requirement: TAE explicitly avoids cryogenic superconducting systems, confirmed for C-2W and strongly implied for Da Vinci (`grokipedia-tae-technologies.md`, dossier).
+- Copper resistive coils for C-2W: standard manufacturing, no supply chain concern.
+- Inconel vacuum vessel: mature industrial manufacturing.
+- NBI ion source components (tungsten filaments, acceleration grids): established accelerator supply chain from ITER and fusion experimental programs.
 
 **Missing**:
-- Boron-11 enrichment: natural boron is ~80% B-11 / ~20% B-10; reactor-grade enrichment requirements, supply chain, and cost not discussed in any source
-- NBI injector materials at high energy: ion source grids, accelerator electrodes subject to erosion; reactor-scale replacement cycle
-- ICC electrode materials: segmented electrodes operating in 5 MHz / 0.6 T fields; no materials specification exists publicly
-- First wall material for soft X-ray and alpha environment
-- Any manufacturing bottleneck analysis
+- Specific alloy/material requirements for first wall and divertor at Da Vinci operating conditions (higher X-ray flux from p-B11 than D-T neutrons).
+- Electrode materials for edge biasing at sustained reactor conditions.
+- Detailed magnet material specification for Da Vinci (confirmed resistive but alloy/coolant not stated).
 
 **Gaps**:
-- B-11 enrichment supply chain and cost — `not-yet-sourced` — **important**; this is a recurring gap in p-B11 concept analyses; IAEA/DOE boron isotope reports likely exist
-- NBI injector longevity and replacement schedule — `not-yet-sourced` — **important** for O&M cost; ITER NBI maintenance data may provide analogues
-- ICC materials and manufacturing — `proprietary/truly-unknown` — **nice-to-have** for baseline Da Vinci (steam BOP), **important** if modeling long-term direct conversion path
-- First wall erosion lifetime — `truly-unknown` — **important** for capacity factor and O&M; p-B11 alpha bombardment of vessel walls is a novel environment
+- X-ray/UV flux effects on first wall material at 250 keV plasma (higher than D-T X-ray environment) — `not-yet-sourced` — **important**: affects replacement schedule and cost
+- Boron powder injection system at scale (method for introducing B-11 fuel during operation) — `not-yet-sourced` — **nice-to-have**
 
 ---
 
 ### 5. LCOE Parameter Extraction
-
 **Available Parameters**:
-
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Plant electrical output (initial) | 50 MWe | DJT merger announcement / ANS Newswire | h |
-| Plant electrical output (mature) | 350–500 MWe | DJT merger announcement | m |
-| Construction start | 2026 | DJT merger announcement | h |
-| First plasma | 2029 | DJT merger announcement | h |
-| Net energy capability | 2030 | DJT merger announcement | h |
-| Power operations | 2031 | DJT merger announcement | m |
-| Energy conversion type | Thermal/steam (Da Vinci baseline) | TAE FAQ, New Atlas | h |
-| Thermal efficiency (steam) | ~30–35% (analogue, not stated) | Standard steam cycle | m (analogue) |
-| Fusion reaction energy per event | 8.7 MeV (3 alphas) | p-B11 physics | h |
-| Target plasma temperature | ~250 keV (~3 billion °C) | Grokipedia (Da Vinci target) | m |
-| Fuel cost (H, B-11) | Very low (order: negligible) | General knowledge | m |
-| No tritium breeding blanket cost | N/A (eliminated) | Multiple sources | h |
-| No heavy shielding cost | Minimal (eliminated) | TAE website | h |
-| Operation mode | Steady-state | Multiple sources | h |
-| Magnet type (experimental) | Copper/resistive | C-2W machine details | h |
+| Net electrical output | 50 MWe (initial) / 350–500 MWe (at scale) | `tae-djt-merger-davinci-specs.md`; dossier | High |
+| Energy conversion method | Thermal steam (Rankine) | `tae-energy-conversion-clarification.md` | High |
+| Thermal efficiency (assumed) | ~33–38% (standard steam cycle) | Derivable from standard engineering | Medium |
+| Fuel cycle | p-B11 aneutronic | All sources | High |
+| Fuel cost | Near-zero (abundant H and B-11) | Derivable | High |
+| Neutron management cost | Minimal shielding only | TAE FAQ; dossier | High |
+| Tritium cost | N/A | Dossier | High |
+| Operation mode | Steady-state | All sources | High |
+| Capacity factor (target) | ~90% (standard baseload assumption) | `osti-servlets-purl-1001677.md` (Waganer PPPL methodology) | Low (assumed) |
+| Maintenance approach | Hands-on possible (no activation) | TAE FAQ | Medium |
+| Confinement magnet type | Resistive copper (likely) | C-2W confirmed; Da Vinci inferred | Medium |
+| Timeline | Construction 2026, power operations 2031 | `tae-djt-merger-davinci-specs.md` | Medium |
 
 **Missing Parameters**:
-
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Q value / fusion gain (Da Vinci) | proprietary | blocking | No public statement; C-2W is far sub-breakeven; must bracket (e.g., Q=2–10) |
-| NBI wall-plug efficiency at reactor scale | not-yet-sourced | blocking | Determines recirculating power; current C-2W NBI is 13 MW input; Da Vinci NBI scale/efficiency unknown |
-| Recirculating power fraction | derivable | blocking | Must derive from Q + NBI efficiency assumptions; dominates net LCOE for beam-driven concepts |
-| Total plant capital cost | proprietary | blocking | No estimate published; no plant study exists; will need analogue-based estimate |
-| Capital cost by subsystem (CAS breakdown) | proprietary | blocking | No published breakdown; rough analogues only |
-| O&M cost estimate | proprietary | blocking | No published data; must estimate from fusion plant analogues |
-| NBI system capital cost at reactor scale | not-yet-sourced | important | ITER NBI cost data may provide analogue (unverified — confirm existence before searching) |
-| Capacity factor / availability | truly-unknown | important | Steady-state is favorable, but first wall and NBI maintenance schedules unknown |
-| NBI injector replacement schedule | not-yet-sourced | important | Drives O&M; ITER injector maintenance literature may help (unverified) |
-| ICC capital cost (if modeled) | proprietary/truly-unknown | nice-to-have | Only relevant if modeling long-term direct conversion path |
-| B-11 fuel cost (enriched) | not-yet-sourced | important | Enrichment cost largely unknown; natural boron is cheap but reactor-grade B-11 may not be |
-| Plant construction cost (Da Vinci) | proprietary | blocking | Only "smaller and less expensive" claims; no dollar figure |
-| Bremsstrahlung/synchrotron loss fraction | derivable | important | Physics is known; p-B11 at 250 keV loses significant energy to radiation; quantifiable from first principles |
-| Alpha particle confinement fraction in FRC | truly-unknown | blocking | Required for effective Q calculation; open physics research question |
+| Capital cost estimate (any subsystem) | proprietary | Blocking | No cost data published anywhere for Da Vinci or commercial FRC |
+| NBI system capital cost at Da Vinci scale | proprietary | Blocking | NBI likely dominant cost driver; no analogues directly applicable |
+| Fusion power / Q_plasma | truly-unknown | Blocking | Q > 1 never achieved; no target Q published for Da Vinci |
+| NBI wall-plug efficiency at reactor scale | proprietary/truly-unknown | Blocking | Determines recirculating power fraction, which is the single biggest LCOE lever |
+| First wall / chamber replacement schedule | proprietary | Important | Affects O&M cost; aneutronic conditions reduce damage but X-ray/UV flux still exists |
+| O&M cost estimate | proprietary | Important | No analog published; hands-on maintenance simplifies vs D-T |
+| NBI electrical power demand (continuous) | proprietary | Blocking | Must be derived from Q and NBI efficiency; neither known |
+| Confinement magnet power (continuous) | derivable | Important | Resistive magnets have continuous power draw; field ~0.1–0.3 T (C-2W) |
+| ICC direct conversion efficiency | truly-unknown | Nice-to-have | Long-term upgrade path; Da Vinci uses thermal steam |
+| Plant scaling law (50 MWe → 350–500 MWe) | proprietary | Important | Determines whether economics improve with scale |
 
 ---
 
 ## Source Recommendations
 
-1. **B-11 enrichment costs and supply chain** — search IAEA Nuclear Data Section, DOE isotope program reports, or ORNL stable isotope production literature — `not-yet-sourced`
-2. **High-energy NBI capital and O&M cost analogues** — ITER NBI system cost estimates from ITER Organization project documentation or F4E procurement reports — `not-yet-sourced` — *unverified — confirm existence before searching*
-3. **p-B11 plasma physics: bremsstrahlung losses and effective Q ceiling** — published plasma physics literature (e.g., Nevins & Swain, Nuclear Fusion 2000, on p-B11 reactivity; Rider critique papers) — `not-yet-sourced` — these papers are well-known in the fusion community and likely exist; search Google Scholar for "proton boron-11 reactivity bremsstrahlung"
-4. **FRC power plant conceptual studies** — search OSTI for "field-reversed configuration power plant" or "FRC reactor study"; older DOE system studies (1980s–1990s) may give rough cost analogues even if based on different FRC physics — `not-yet-sourced` — *unverified — confirm existence before searching*
-5. **TAE engineering publications** — IAEA Fusion Energy Conference proceedings (FEC) often include TAE contributions (Gota et al.); these may contain more detailed machine parameters than press materials — `not-yet-sourced`; dossier cites "IAEA FEC papers (Gota et al.)" as a source type but none are extracted
-6. **Da Vinci reactor design details** — likely in TAE investor presentations or technical roadmap documents; not public — `proprietary`; no search strategy will resolve this
+1. **NBI system cost at scale**: Search ITER NBI design documentation and Fusion Engineering and Design literature for neutral beam cost scaling. ITER's 16.5 MW NBI system has published cost estimates that could provide an analog — `unverified — confirm existence before searching`. Search terms: "ITER neutral beam injector cost" or "neutral beam injection cost scaling fusion."
+
+2. **p-B11 reactivity and bremsstrahlung balance**: The Putvinski, Ryutov & Yushmanov 2019 *Nuclear Fusion* paper ("Fusion reactivity of the pB11 plasma revisited," Nucl. Fusion 59 076018) is cited in `osti-pages-servlets-purl-2441289.md` and directly addresses the physics feasibility question. This paper is likely accessible via OSTI. High priority for understanding the physics feasibility ceiling.
+
+3. **FRC/compact confinement cost analogs**: The ARPA-E ALPHA revisit study (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) covers compact confinement concepts in a CAS framework. While none of the four concepts is a p-B11 FRC, the methodology and BOP/indirect cost structure are directly applicable. Recommend reading this source.
+
+4. **Plant availability methodology**: The Waganer PPPL availability paper (`iter-02/sources/osti-servlets-purl-1001677.md`) was already sourced and provides the 10th-OAK / first-OAK / one-OAK framework. Use for capacity factor assumptions: 87.6% for mature plant, ~46% for one-OAK.
+
+5. **Recirculating power analysis**: The Mulder et al. 2021 arxiv paper (`arxiv-2103-12451.md`) was captured only as an abstract. The full paper analyzes high-recirculated-power fusion plants and should be obtained to support quantitative recirculating power fraction estimates. Search arXiv:2103.12451.
+
+6. **p-B11 cross section and ignition requirements**: Academic literature on p-B11 physics feasibility (particularly Nevins & Swain, 2000 *Nuclear Fusion*; and the 2019 Putvinski et al. paper) would fill the physics foundation. Search OSTI or Google Scholar for "p-B11 aneutronic fusion ignition requirements" — `unverified — confirm existence before searching`.
 
 ---
 
 ## Summary
 
-**Proceed to full analysis**, with explicit acknowledgment of quantitative constraints. The qualitative write-up (data availability, system function challenges, subsystem maturity, materials) can be produced at high quality with available sources — TAE is more communicative than most private fusion companies and the physics architecture is well-documented.
+Proceed to full analysis, but with clear expectations about what is and is not knowable. The qualitative sections (data availability, system function challenges, subsystem maturity, materials) can be written at high quality using available sources. The quantitative LCOE model will necessarily be built on assumptions rather than published cost data, with the following structure:
 
-The quantitative LCOE model is feasible but will be built almost entirely on assumptions and analogues for the cost-driving parameters. The two binding constraints are: **(1) Q value** — must be assumed; literature on p-B11 physics suggests a ceiling well below tokamak-class D-T concepts due to bremsstrahlung losses, and this should be quantified using published reactivity data rather than TAE's aspirational claims; and **(2) NBI recirculating power** — for a beam-driven concept, this is the dominant factor in net LCOE and is essentially unknown at reactor scale. Before running the model, sourcing the Nevins & Swain (or equivalent) p-B11 reactivity analysis would substantially improve the Q-ceiling estimate and is likely the highest-value pre-analysis data acquisition step.
+- **What is solid**: Power output target, energy conversion pathway, fuel cost, maintenance simplification, magnet type, and fuel supply chain.
+- **What must be assumed from analogues**: Capital cost per MWe (use ARPA-E ALPHA ranges for compact MFE), O&M costs (use standard fusion O&M analogs), thermal efficiency (standard steam cycle).
+- **What requires explicit flagging as blocking uncertainties**: Q value, NBI recirculating power fraction, and whether p-B11 net energy is physically achievable at any reasonable machine scale. The 1 c/kWh back-solve will reveal that this concept requires extraordinary breakthroughs in plasma performance well beyond current demonstrations.
+
+The $0.01/kWh back-solve will be a particularly illuminating section: the combination of very low fuel cost, no tritium breeding, and simplified shielding creates a favorable cost structure in principle—but it is entirely negated if Q is low (forcing NBI recirculation to dominate) or if plasma performance requires repeated machine upgrades before commercial operation.
+
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Mostly Ready (with significant quantitative constraints)"
-blocking_count: 8
-important_count: 5
-counting_method: "section_5_missing_parameters"
+overall_rating: "Significant Gaps"
+blocking_count: 5
+important_count: 6
+counting_method: "deduplicated across all sections; only counted once per distinct gap — Q/net energy, NBI efficiency/recirculating power, NBI cost at scale, capital cost absence, and bremsstrahlung physics as blocking; first wall lifetime, O&M costs, plant scaling law, magnet power draw, Da Vinci magnet confirmation, and X-ray wall effects as important"
 section_coverage:
-  availability_of_data:       "Moderate"
+  availability_of_data:       "Partial"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
-  materials_supply_chain:     "Poor"
-  lcoe_parameter_extraction:  "Unknown"
-```
+  materials_supply_chain:     "Good"
+  lcoe_parameter_extraction:  "Poor"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
