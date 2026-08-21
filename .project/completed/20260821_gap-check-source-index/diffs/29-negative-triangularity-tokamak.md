# Diff: 29-negative-triangularity-tokamak

**Generated:** 2026-05-22T11:10:55-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 1 | 2 | 1 |
| important_count  | 7 | 8 | - |
| overall_rating   | Mostly Ready | Mostly Ready | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
168:6. **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): This fleet-wide source covers D-T MFE CAS cost methodology. Applicable for validating MANTA cost account structure against standard D-T tokamak CAS and for O&M cost analogs — **directly applicable to this concept; recommend reading for CAS cross-check**.
170:7. **Revisit of 2017 ARPA-E ALPHA Costing** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): Covers CAS cost structures across four compact fusion concepts; useful for cross-checking MANTA's cost account methodology and confirming whether $38M/MWe is reasonable for a pilot plant — **moderately applicable; read for CAS validation**.
178:Before starting the full analysis, consider extracting the MANTA Appendix C tables (cost breakdown Tables C1–C5) and cross-checking against `knowledge/sources/tea_dt_mfe_cost_analysis/` for CAS alignment.
```

## Blocking-tier lines (baseline)

```
52:- Heating method is genuinely uncertain, with >2× variation in recirculating power fraction across the three hypotheses — `truly-unknown` for Firefly specifically — **blocking** (significantly affects LCOE through plant efficiency and capital cost of heating systems)
```

## Blocking-tier lines (new)

```
34:- No Firefly-specific engineering publication — `proprietary` — **blocking**: forces reliance on MANTA proxy for all engineering details; explicitly scope the analysis as "NT ARC-class, with Firefly parameters as available"
56:- NT confinement enhancement factor at reactor-relevant D-T conditions — `truly-unknown` — **blocking**: the H₉₈ uncertainty range (0.79–1.44 in MANTA) translates directly into whether ignition/high-Q is achievable; this is the fundamental physics bet
148:| Firefly-specific capital cost model (for R~2 m design) | proprietary | blocking | MANTA's $3.4B is for R=4.55 m; cost scaling to R~2 m is not straightforward due to non-linear magnet cost scaling |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/29-negative-triangularity-tokamak.md	2026-05-22 09:21:13.878578813 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/29-negative-triangularity-tokamak/gap_report.md	2026-05-22 11:10:55.443533734 -0700
@@ -1,37 +1,38 @@
-Now I have enough to write the full assessment. Let me produce it.
+I now have sufficient data to write the full gap assessment. Let me compile it.
 
 ---
 
-# Gap Assessment: Negative Triangularity Tokamak
+# Gap Assessment: Negative Triangularity Tokamak (D-T)
 
 ## Overall Readiness
 **Rating**: Mostly Ready
 
-**Summary**: The concept class is well-supported by a high-quality published proxy reference design (MANTA, Rutherford et al. 2024) that provides engineering-level parameters, a cost estimate, and subsystem detail. Firefly Fusion itself is opaque — founded 2024, no reactor parameters published on their website — so every Firefly-specific value must be inferred from MANTA or the co-founder's physics paper. The main analytical risk is the scaling uncertainty between MANTA's 450 MW / 90 MWe pilot plant and Firefly's 50–100 MW target. Enough is available for a credible first-pass LCOE model with appropriately wide error bars; a full MANTA subsystem cost breakdown would significantly sharpen it.
+**Summary**: The MANTA design study (Rutherford et al. 2024) is an unusually detailed academic reference — a fully integrated NT ARC-class pilot plant with explicit overnight cost ($3.4B), LCOE projection ($396/MWh for scaled commercial plant), balance-of-plant modeling, neutronics, and magnet lifetimes. This makes MANTA the best available proxy for an NT D-T tokamak concept analysis, compensating for Firefly Fusion's near-total lack of public technical disclosure (founded 2024, no published engineering parameters). The primary gaps are (1) NT confinement scaling at reactor conditions remains experimentally unvalidated at power-plant scale, creating genuine physics uncertainty ranges, and (2) Firefly's compact design (R≈2–2.5 m) is substantially smaller than MANTA (R=4.55 m), so direct cost transfer requires explicit scaling assumptions.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Partial (concept class: Good; Firefly specifically: Opaque)
+**Coverage**: Partial
 
 **Available**:
-- `manta-reference-design.md` — Published peer-reviewed plant study (Rutherford et al. 2024, PPCF). Provides: fusion power (450 MW), net electricity (90 MW), Q (11.5), overnight cost ($3.4B), ICRF heating (40 MW), FLiBe blanket design (TBR 1.15), REBCO HTS magnets (11 T demountable), pulsed operation (~15 min / 2 min inter-pulse). This is the structural backbone for any LCOE model.
-- `ball-balestri-ohmic-nt-paper.md` — Physics feasibility paper by co-founder Justin Ball (EPFL). Provides device parameter space analysis; confirms compact, high-field regime viability.
-- `greyb-firefly-interview.md` — CEO Ospanov interview. Only source of Firefly-specific parameters: R=2–2.5 m, B=10–12 T, Q>5, P_fusion=50–100 MW, P_aux=20–30 MW.
-- `firefly-fusion-diii-d-collaboration.md` — DIII-D collaboration context; confirms research direction (NT edge physics, disruption resilience).
-- `firefly-website-2026.md` — Advisor credentials only; zero technical parameters.
+- **MANTA reference design** (`iter-02/sources/manta-reference-design.md`): ~160 KB fully extracted paper covering all major subsystems, power balance (P_fus=450 MW, Q=11.5, P_net=90 MWe), overnight cost ($3.4B), and an explicit LCOE analysis for an NT pilot plant. This is the dominant technical source for the concept.
+- **Balestri, Ball, Coda 2024** (`iter-01/sources/ball-balestri-ohmic-nt-paper.md`): Full paper (55 KB) on ohmic-only NT tokamak feasibility across MANTA, SPARC, ITER, and DEMO parameter spaces. Directly authored by Firefly co-founder Justin Ball (EPFL/SPC). Quantitative confinement and Q projections under different heating assumptions.
+- **GreyB/Scouted interview** (`iter-01/sources/greyb-firefly-interview.md`): CEO Rustem Ospanov interview providing top-level Firefly parameters: R=2–2.5 m, B=10–12 T, Q>5, P_fusion=50–100 MW, 20–30 MW heating input.
+- **DIII-D collaboration page** (`iter-01/sources/firefly-fusion-diii-d-collaboration.md`): Confirms DIII-D collaboration, LUCIOLE prototype (copper magnets), and NT experimental program.
+- **ARIES-ACT studies** (`iter-04/sources/osti-servlets-purl-*.md`): Conventional PT tokamak power plant parametric studies (advanced R=6.25 m/58% efficiency; conservative R=9.75 m/45%) — useful as cost analogs and CAS framework references.
+- **ARIES Cost Account Documentation** (`iter-04/sources/qedfusion-lib-report-aries-act-ucsd-cer-13-01.md`): CAS methodology reference (Accounts 20–27 direct, 90–98 indirect); provides the costing framework applicable to MANTA-derived estimates.
+- **Arxiv abstracts** (2401.15217, 2405.01514, 2501.14682): NT vertical stability analysis, fusion plant maintenance grid economics, and NT electromagnetic system design — abstracts only (3–4 KB each); content limited to titles and abstracts.
 
 **Missing**:
-- Any Firefly-authored technical publication or engineering report
-- Published plant study sized to Firefly's 50–100 MW target (not 450 MW MANTA)
-- Experimental results from LUCIOLE (not yet built)
+- Firefly's actual reactor design parameters (dimensions, magnet design, blanket, heating system) beyond CEO interview
+- Published engineering data from Firefly's DIII-D collaboration (ongoing, unpublished)
+- Any Firefly financial model or cost estimate
 
 **Gaps**:
-- No Firefly engineering disclosures beyond one press interview — `proprietary` — **important** (limits confidence on all Firefly-specific values, but MANTA proxy partially compensates)
-- No NT tokamak plant study at the 50–100 MW scale — `not-yet-sourced` — **important** (MANTA is 4.5× larger; scaling may not be linear)
-- Kikuchi (2014) "Negative Triangularity Tokamak as Fusion Energy System" (authored by Firefly advisor) not ingested — `not-yet-sourced` — **nice-to-have**
+- No Firefly-specific engineering publication — `proprietary` — **blocking**: forces reliance on MANTA proxy for all engineering details; explicitly scope the analysis as "NT ARC-class, with Firefly parameters as available"
+- NT confinement experiments at reactor-relevant conditions (burning plasma, D-T) — `truly-unknown` — **important**: DIII-D/TCV results are at low B and DD plasma; scaling to 11 T REBCO D-T burning plasma is extrapolated
 
 ---
 
@@ -39,138 +40,156 @@
 **Coverage**: Partial
 
 **Available**:
-- NT physics rationale is well-documented in MANTA and Ball et al.: L-mode edge eliminates ELMs and reduces SOL power load (only 23.5 MW to SOL for 450 MW fusion in MANTA), which is the core claimed advantage.
-- Heating method ambiguity is flagged and documented: three competing hypotheses (ECRH from Venture Kick "microwaves," ICRH from MANTA proxy, ohmic-only from Ball et al.). MANTA uses 40 MW ICRF — no ECRH or NBI.
-- Pulsed operation mode documented (MANTA ~15 min pulses). Inductive current drive via central solenoid is the limiting factor on pulse length.
+- **NT confinement physics**: MANTA uses H₉₈y₂ = 0.79–1.44 depending on scenario; Ball et al. show H₈₉ enhancement factor range 1.4–2.0 as the dominant physics uncertainty. This uncertainty range is explicitly quantified and bounded.
+- **Ohmic vs. auxiliary heating system function**: Ball et al. show that at MANTA/SPARC parameters, ohmic-only NT achieves Q~500 vs. Q~30–80 for heated scenarios — a fundamentally different system architecture. Firefly's actual choice is unknown, creating a forked system-function model.
+- **Pulsed operation thermal management**: MANTA's molten salt thermal storage (60% NaNO₃/40% KNO₃ secondary loop) handles 15-min pulses with 2-min inter-pulse. Full thermodynamic analysis available.
+- **Divertor/power handling with NT**: MANTA's UEDGE simulations show peak heat flux 2.8 MW/m² (vs. 10 MW/m² limit), with ELM-free NT enabling higher impurity seeding fractions and lower P_SOL (23.5 MW for 450 MW fusion). This is a quantitative result with explicit uncertainty discussion.
+- **Vertical stability**: arXiv:2401.15217 (abstract only) confirms NT is less vertically stable than PT at equivalent parameters and requires passive stabilizing plates. MANTA addresses this in design.
+- **VV material compatibility with FLiBe**: MANTA identifies V-4Cr-4Ti + MoF6 self-healing barrier as the chosen approach; acknowledges this is a novel, low-TRL approach requiring future validation.
 
 **Missing**:
-- Recirculating power fraction quantification for Firefly's design point (depends heavily on which heating method is chosen — ohmic-only would have near-zero recirculating power for heating, dramatically changing plant efficiency)
-- Energy storage system requirements between pulses (not addressed in any source)
-- Plasma performance projections for Firefly's smaller device (R=2–2.5 m vs. MANTA R=4.55 m)
+- Experimental validation of NT confinement at burning plasma conditions or D-T (not yet achieved anywhere)
+- Experimental data on NT stability with FLiBe blanket or high-Z first wall in NT geometry
+- How Firefly's compact design (R~2 m) handles the power-exhaust problem at high power density relative to MANTA (R=4.55 m)
 
 **Gaps**:
-- Heating method is genuinely uncertain, with >2× variation in recirculating power fraction across the three hypotheses — `truly-unknown` for Firefly specifically — **blocking** (significantly affects LCOE through plant efficiency and capital cost of heating systems)
-- Pulse-to-pulse energy storage/buffering requirements not addressed — `not-yet-sourced` — **important** (affects BOP cost and grid integration)
-- Confinement quality (H-factor equivalent for NT L-mode) at Firefly's parameters: published DIII-D/TCV data exists but not ingested — `not-yet-sourced` — **nice-to-have**
+- NT confinement enhancement factor at reactor-relevant D-T conditions — `truly-unknown` — **blocking**: the H₉₈ uncertainty range (0.79–1.44 in MANTA) translates directly into whether ignition/high-Q is achievable; this is the fundamental physics bet
+- Heating architecture choice (ohmic vs. ICRH vs. ECRH) — `proprietary`/`not-yet-sourced` — **important**: different heating approaches imply very different capital costs ($0 vs. tens of millions for an ICRF system) and recirculating power fractions
+- First-wall material compatibility in NT geometry (different divertor location) — `not-yet-sourced` — **important**: NT puts the broad face outboard; MANTA acknowledges divertor target asymmetries
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
 **Coverage**: Partial
 
-**Available**:
-- **REBCO HTS magnets**: MANTA specifies TF coil lifetime (3100 ± 400 MW·yr), demountable design, 11 T on-axis. CFS/SPARC demonstrated 20 T REBCO at scale (2021). TRL ~5–6.
-- **NT plasma physics**: Validated on DIII-D (US) and TCV (Switzerland) at experimental scale. TRL ~4–5 for the plasma physics; TRL ~2 for NT reactor engineering.
-- **ICRF heating**: Operational on JET, WEST, ASDEX-U. TRL 7–8. (If Firefly uses ECRH instead, similar TRL; if ohmic-only, no heating subsystem needed.)
-- **LUCIOLE prototype**: Pre-design phase only; copper magnets planned for rapid iteration. TRL 1–2.
-- **Power conversion**: No Firefly disclosure; MANTA implies standard steam cycle. Conventional Rankine steam is TRL 9.
+**Available**: MANTA provides TRL-relevant detail on most subsystems:
+
+| Subsystem | TRL Basis from Sources | Source |
+|-----------|----------------------|--------|
+| NT plasma confinement | TRL 4–5 (DIII-D, TCV experiments at low B/DD; no reactor-scale data) | MANTA Sec. 2; Ball et al. |
+| REBCO HTS TF coils (18-coil, 11 T) | TRL 5–6 (SPARC TFMC demonstrated; MANTA design extrapolates from TFMC) | MANTA Sec. 4 |
+| Non-insulated REBCO coil operation | TRL 4–5 (SPARC TFMC; MANTA's 67-day ramp problem → oversized cryoplant required) | MANTA Sec. 4.2 |
+| ICRF heating (40 MW at 110 MHz) | TRL 7–8 (established at JET, WEST; SPARC uses same minority-3He scheme) | MANTA Sec. 2, Sec. 3 |
+| FLiBe liquid immersion blanket | TRL 3–4 (material well-characterized; no reactor-scale system operated) | MANTA Sec. 5 |
+| V-4Cr-4Ti VV with MoF₆ barrier | TRL 2–3 (proposed material; MoF₆ self-healing barrier is novel/unvalidated) | MANTA Sec. 5 |
+| Sub-critical Rankine with molten salt storage | TRL 6–7 (solar thermal heritage; FLiBe primary coupling is lower TRL) | MANTA Sec. 6 |
+| Tritium fuel cycle | TRL 2–3 (no closed D-T tritium cycle at scale; MANTA uses conservative estimates) | MANTA Sec. 5.4 |
+| Tungsten plasma-facing divertor | TRL 5–6 (ITER heritage; NT-specific divertor geometry novel) | MANTA Sec. 3.3 |
 
 **Missing**:
-- TRL assessment for FLiBe blanket integrated with NT geometry (no integrated test facility exists; FLiBe is at materials-testing stage, TRL 2–3)
-- First wall / PFC lifetime under NT L-mode heat flux conditions — some DIII-D data exists but not at reactor-relevant scale
-- Central solenoid lifetime and replacement schedule (inductive drive degrades the CS over time)
+- TRL assessment for Firefly's specific prototype path (LUCIOLE with copper magnets → no TRL data)
+- Independent TRL assessments from any government or regulatory source for NT-specific systems
 
 **Gaps**:
-- FLiBe blanket TRL is low (~2–3) and no data source was ingested for this — `not-yet-sourced` — **important** (blanket is a major cost driver and schedule risk)
-- First wall materials and lifetime under NT-specific heat load profiles not characterized in sources — `not-yet-sourced` — **important**
-- CS fatigue/lifetime analysis absent — `derivable` from published solenoid studies — **nice-to-have**
+- FLiBe blanket and tritium fuel cycle TRL detail — `not-yet-sourced` — **important**: fusion TBR demonstration and closed tritium loop are universally recognized as program-pacing items; more detailed sources (e.g., FLiBe-2 program, FNSF studies) likely exist on OSTI
+- NT-specific first-wall erosion lifetime data — `truly-unknown` — **nice-to-have**: NT's wider outboard plasma face changes the erosion geometry
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Partial
+**Coverage**: Poor
 
 **Available**:
-- **REBCO HTS tape**: MANTA confirms REBCO for all magnets. Global supply is constrained; CFS/SPARC scale-up is driving capacity investment but supply chain is immature at reactor scale. This is a well-known industry issue.
-- **FLiBe**: MANTA uses FLiBe blanket. Requires Li-6 enrichment (~90%) and beryllium, both of which have supply chain concerns (Be is toxic, limited suppliers; Li-6 enrichment capacity is limited).
-- **Tritium**: Standard D-T concern — initial tritium supply from CANDU/fission reactors; breeding self-sufficiency requires TBR >1 (MANTA achieves 1.15).
+- MANTA provides material quantities: 18 REBCO TF coils requiring 13.6 MA-turns (REBCO tape quantity computable from the 570 A/mm² operating density and coil geometry parameters in Table 4); ~1.1 million kg Inconel-718 structural material
+- MANTA identifies REBCO tape cost as the single largest cost uncertainty driver (sensitivity ±50% keeps plant under $5B NASEM limit)
+- Tritium startup inventory: 440g needed; global annual production ~2.7 kg/yr (explicitly stated in MANTA Sec. 7.2 as potentially market-saturating)
+- FLiBe identified as a high-TBR breeder/coolant; beryllium content (BeF₂) implies supply constraints (not explicitly discussed in MANTA)
+- Li-6 enrichment requirement for FLiBe implied but not quantified
+- Tungsten first wall and W-C shielding quantities noted in MANTA Table 6
 
 **Missing**:
-- Specific REBCO tape quantity estimates for Firefly's device (requires device engineering detail not available)
-- Beryllium supply analysis for FLiBe at commercial scale
-- Lithium enrichment (Li-6) supply chain depth
+- Explicit REBCO tape quantity calculation for MANTA's TF coils
+- FLiBe supply chain analysis (BeF₂ supplier landscape, Be safety handling costs)
+- Li-6 enrichment supply and export control implications
+- REBCO tape supply chain deep-dive (commercial suppliers, pricing trend)
+- V-4Cr-4Ti production scale (specialty alloy with limited commercial production)
 
 **Gaps**:
-- No Be or Li-6 supply chain assessment in any source — `not-yet-sourced` — **nice-to-have** (well-known problem but specific quantification missing)
-- REBCO tape demand per reactor not calculated (requires magnet geometry from a Firefly design) — `derivable` from MANTA scaling — **nice-to-have**
+- REBCO supply chain capacity and cost trajectory — `not-yet-sourced` — **important**: TF coil cost ($1.5B) is the dominant MANTA capital cost driver; REBCO supply/price uncertainty is the largest cost sensitivity; CFS/ITER magnet program may have updated supply data
+- Li-6 enrichment for FLiBe breeder blanket — `not-yet-sourced` — **important**: 6Li enrichment is export-controlled; supply constraints could affect deployment timeline
+- BeF₂/FLiBe supply and safety costs — `not-yet-sourced` — **important**: beryllium is toxic and tightly regulated; handling infrastructure cost is not captured in MANTA's cost model
+- Tritium availability for startup — `derivable` (from MANTA's 440g estimate + known CANDU production rate) — **important**: tritium startup cost is a known first-plant blocker
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Partial — sufficient for a first-pass model using MANTA as proxy; insufficient for Firefly-specific projections
+**Coverage**: Partial
 
-**Available Parameters** (from MANTA unless noted):
+**Available Parameters** (from MANTA as NT pilot plant proxy):
 
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Fusion power | 450 MW (MANTA) / 50–100 MW (Firefly target) | MANTA; GreyB interview | M (proxy) |
-| Net electricity | 90 MW | MANTA | M (proxy) |
-| Plasma gain Q | 11.5 (MANTA) / >5 (Firefly) | MANTA; GreyB | M |
-| Overnight capital cost | $3.4B | MANTA | M (proxy) |
-| Specific capital cost | ~$38k/kWe (MANTA scale) | MANTA (derived) | M |
-| NASEM compliance | <$5B overnight — MANTA meets this | MANTA | M |
-| Auxiliary heating power | 40 MW ICRF (MANTA) / 20–30 MW (Firefly) | MANTA; GreyB | M |
-| Power to SOL | 23.5 MW | MANTA | M (proxy) |
-| Pulse length | ~15 min burn / 2 min inter-pulse | MANTA | M (proxy) |
-| Duty cycle | ~88% (derived from MANTA pulse schedule) | MANTA (derived) | M |
-| TBR | 1.15 | MANTA | M (proxy) |
-| Blanket power multiplication | 1.11 | MANTA | M (proxy) |
-| TF coil lifetime | 3100 ± 400 MW·yr | MANTA | M (proxy) |
-| PF coil lifetime | ≥890 ± 40 MW·yr | MANTA | M (proxy) |
-| Target major radius | 2–2.5 m | GreyB interview | M |
-| Target field | 10–12 T | GreyB interview | M |
+| Fusion power | 450 MW (MANTA); 50–100 MW (Firefly target) | MANTA Table 1; GreyB interview | h (MANTA); m (Firefly) |
+| Net electric power | 90 MWe | MANTA Table 1, Sec. 6.3 | h (MANTA) |
+| Plasma gain Q | 11.5 | MANTA Table 1 | h (MANTA) |
+| Electricity gain Q_E | 2.4 | MANTA Table 1 | h (MANTA) |
+| Thermal efficiency | 36% (sub-Rankine), 39% (super-Rankine) | MANTA Table 8 | h (MANTA) |
+| Power cycle type | Sub-critical Rankine + molten salt storage | MANTA Sec. 6 | h (MANTA) |
+| Overnight capital cost (pilot) | $3.4B ≈ $38M/MWe | MANTA Sec. 7.1 | m (pilot-scale proxy) |
+| TF coil cost (dominant driver) | $1.5B of $3.1B tokamak cost | MANTA Sec. 7.1 | m |
+| Commercial LCOE projection | $396/MWh (550 MW, 30 yr project) | MANTA Sec. 7.2 | l (explicitly too high; path to competitiveness requires higher magnet lifetime + power) |
+| TBR | 1.15 | MANTA Sec. 5 | h (MANTA design) |
+| Blanket power multiplication | 1.11 | MANTA Sec. 5 | h (MANTA design) |
+| Tritium startup inventory | 440g | MANTA Sec. 5.4 | m |
+| Pulse length | ~15 min / 2 min inter-pulse | MANTA Table 1 | h (MANTA design) |
+| TF coil lifetime | ~3,100–30,400 MW-yr (min–mean) | MANTA Table 7 | m |
+| PF coil lifetime (limiting) | ~890 MW-yr (PF2 minimum) → replacement every ~2 full-power years | MANTA Table 7 | m |
+| Major radius | 4.55 m (MANTA proxy); 2–2.5 m (Firefly target) | MANTA Table 1; GreyB | h/m |
+| Toroidal field | 11 T (MANTA); 10–12 T (Firefly) | MANTA; GreyB | h |
+| Auxiliary heating power | 40 MW ICRF (MANTA); possibly 0–30 MW (Firefly) | MANTA Sec. 2; Ball et al. | m |
+| Recirculating power | ~62 MWe (RF 57 MWe + cryo 1 MWe + pumps ~4 MWe) | MANTA Table 8 | h (MANTA) |
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Capital cost breakdown by subsystem (magnets, blanket, BOP, heating, VV) | not-yet-sourced | **Blocking** | Full MANTA paper (Rutherford et al. 2024) likely contains this; only top-line cost captured in extracted source |
-| Thermal cycle type and efficiency | not-yet-sourced | **Important** | No source specifies steam vs. sCO2 or efficiency; conventional ~35% steam assumed but unverified |
-| O&M cost estimate (annual) | not-yet-sourced | **Important** | MANTA may have this; no analogous NT tokamak O&M data in sources |
-| Blanket/VV replacement cost and schedule | not-yet-sourced | **Important** | MANTA notes FLiBe tank + VV are a single replaceable assembly; cost not in extracted source |
-| First wall replacement schedule | not-yet-sourced | **Important** | NT L-mode reduces heat flux but no quantified replacement interval in sources |
-| Plant capacity factor (including maintenance downtime) | derivable | **Important** | ~88% from pulse schedule; maintenance outage unquantified — derivable from analogy with ARC-class studies |
-| Plant electrical output at Firefly's target scale | derivable | **Important** | MANTA's 90 MWe at 450 MW fusion → ~20% net efficiency; scaling to 50–100 MW fusion gives ~10–20 MWe |
-| Fuel costs (tritium + deuterium) | derivable | Nice-to-have | Standard D-T; tritium cost well-characterized from literature |
-| Helium-3 minority species cost (if ICRF) | derivable | Nice-to-have | Small quantity, derivable |
-| Recirculating power fraction | derivable | **Important** | Depends heavily on heating method choice; ranges from near-zero (ohmic) to ~30–40% (ICRF) |
-| Staffing cost model | truly-unknown | Nice-to-have | No source; analogy to ITER or ARC |
+| Availability factor / capacity factor (explicit %) | derivable | important | MANTA's 16.1-day maintenance cycle provides inputs; annual availability estimate requires unscheduled outage frequency assumption. Not stated as a single number. |
+| O&M cost breakdown (personnel, consumables, annual capital replacement) | derivable | important | MANTA references Table C5 in appendix, but that appendix content was not fully captured in extraction; total annual O&M not given as a line item |
+| Firefly-specific capital cost model (for R~2 m design) | proprietary | blocking | MANTA's $3.4B is for R=4.55 m; cost scaling to R~2 m is not straightforward due to non-linear magnet cost scaling |
+| REBCO cost per kg/unit length at production scale | not-yet-sourced | important | Current tape costs are $40–100/m² commercial; power plant scale discount trajectory unknown |
+| Li-6 enrichment cost for FLiBe | not-yet-sourced | important | Cost not addressed in MANTA; needed for blanket cost estimation |
+| Decommissioning cost | derivable | nice-to-have | MANTA mentions VV activation is 3 orders of magnitude lower than SS316LN; decommissioning cost not computed |
+| Fuel cost (D-T, excluding startup tritium) | derivable | nice-to-have | Tritium cost dominates; deuterium cost negligible; MANTA models tritium revenue not cost in equilibrium |
 
 ---
 
 ## Source Recommendations
 
-1. **Full Rutherford et al. 2024 MANTA paper** (already cited, full text at arXiv 2405.20243) — Re-extract at full depth to capture subsystem cost breakdown, thermal efficiency, O&M estimates, and capacity factor assumptions. `not-yet-sourced` — **highest priority**. The extracted source only captured high-level parameters; the full 30+ page paper almost certainly contains the cost accounting needed for LCOE model construction.
+1. **MANTA Appendix C** (Tables C1–C5): The MANTA paper references detailed cost breakdowns in Appendix C that were not fully extracted from the PDF. A targeted re-extraction of the appendix pages would fill the O&M cost breakdown gap. [Not yet sourced — the appendix content is likely in the same PDF]
+
+2. **REBCO supply chain analysis**: Search OSTI or IEEE for Commonwealth Fusion Systems REBCO tape procurement studies or APS/SOFE conference papers on REBCO production scale-up. Query: "REBCO high temperature superconductor production scale fusion magnet cost" on OSTI. — `unverified — confirm existence before searching`
 
-2. **Balestri, Ball & Coda 2024 full paper** (already cited, arXiv 2407.06439) — Re-extract to check whether it contains device-level cost or performance estimates beyond physics feasibility. `not-yet-sourced` — **medium priority**. May contain parameter space mapping useful for Firefly's specific design point.
+3. **FLiBe supply and handling costs**: DOE FES has funded FLiBe studies (e.g., FLiBe Advances); search OSTI for "FLiBe fluoride salt tritium breeding blanket supply chain". Flibe Energy LLC (private, US) is also a potential source. — `unverified — confirm existence before searching`
 
-3. **Kikuchi (2014) "Negative Triangularity Tokamak as Fusion Energy System"** — Firefly advisor Mitsuru Kikuchi authored this early NT reactor concept paper. Search for it via OSTI or IAEA. `not-yet-sourced` — `unverified — confirm existence before searching` — **nice-to-have**.
+4. **Li-6 enrichment for fusion**: ORNL has published on Li-6 isotope production (Y-12 complex). Search OSTI for "lithium-6 enrichment fusion tritium breeding blanket" — government lab reports likely exist. — `unverified — confirm existence before searching`
 
-4. **ARC/SPARC cost studies (CFS or MIT)** — Firefly is ARC-class heritage. Published SPARC cost or ARC pilot plant economics would provide subsystem-level cost analogues at similar device scale. Search OSTI and arXiv for "ARC tokamak cost" or "SPARC pilot plant economics." `not-yet-sourced` — **important**.
+5. **NT confinement at high field / reactor-relevant conditions**: DIII-D NT experimental campaign publications (Paz-Soldan et al., cited in MANTA) would provide the most current confinement data; specific papers are cited in MANTA references [24], [29] — these would be the highest-value physics sources to add. One is directly cited: C. Paz-Soldan et al. DIII-D team, *Plasma Physics and Controlled Fusion*, 2021. — `unverified for individual paper quality but referenced in MANTA`
 
-5. **PROCESS or ARIES system code NT tokamak studies** — System codes (PROCESS at CCFE, ARIES at UCSD) may have run NT configurations. Search OSTI for "negative triangularity system code" or "NT tokamak PROCESS." `not-yet-sourced` — `unverified — confirm existence before searching` — **nice-to-have**.
+6. **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): This fleet-wide source covers D-T MFE CAS cost methodology. Applicable for validating MANTA cost account structure against standard D-T tokamak CAS and for O&M cost analogs — **directly applicable to this concept; recommend reading for CAS cross-check**.
 
-6. **FLiBe blanket TRL and materials readiness literature** — DoE Fusion Materials Program, FNSF studies, or IAEA TECDOC on molten salt blankets. Search OSTI for "FLiBe blanket TRL" or "lithium fluoride beryllium blanket materials readiness." `not-yet-sourced` — **important** (needed for maturity section).
+7. **Revisit of 2017 ARPA-E ALPHA Costing** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): Covers CAS cost structures across four compact fusion concepts; useful for cross-checking MANTA's cost account methodology and confirming whether $38M/MWe is reasonable for a pilot plant — **moderately applicable; read for CAS validation**.
 
 ---
 
 ## Summary
 
-**Proceed to full analysis**, with one priority source acquisition first: re-extract the full MANTA paper (Rutherford et al. 2024) to capture its subsystem cost breakdown. The high-level extracted source (`manta-reference-design.md`) captures enough to confirm MANTA is the right proxy, but the LCOE model will need per-subsystem capital cost fractions that are almost certainly in the full paper.
+**Proceed to full D1+ analysis, with explicit proxy scoping.** The MANTA 2024 reference design provides the most detailed publicly available NT D-T tokamak engineering and economic model. All five D1+ sections can be populated, but the analysis should be framed as "NT ARC-class tokamak (MANTA proxy) with Firefly-specific context where available." The two areas requiring explicit uncertainty treatment are: (1) NT confinement enhancement at reactor scale, which remains an unvalidated extrapolation, and (2) capital cost scaling from MANTA's R=4.55 m to Firefly's R~2 m target, which requires order-of-magnitude reasoning rather than direct transfer. The commercial LCOE projection ($396/MWh) is available but explicitly uncompetitive, with MANTA's own analysis identifying the path (longer magnet lifetimes, higher fusion power, better thermal efficiency) — this should be treated as the current baseline with a clearly stated improvement pathway, not a competitive LCOE claim.
 
-The qualitative write-up can be completed now from current sources — NT plasma physics, MANTA reference design, and the Firefly parameter envelope provide enough material for all five D1+ narrative sections. The quantitative LCOE model will need MANTA's cost detail and should explicitly flag the three key uncertainties: (1) scaling from 450 MW MANTA to 50–100 MW Firefly, (2) heating method choice (ohmic vs. ICRF vs. ECRH — affects recirculating power by potentially 30+ percentage points), and (3) blanket lifetime/replacement cost. These should be treated as explicit sensitivity axes in the model rather than point estimates.
+Before starting the full analysis, consider extracting the MANTA Appendix C tables (cost breakdown Tables C1–C5) and cross-checking against `knowledge/sources/tea_dt_mfe_cost_analysis/` for CAS alignment.
+
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Mostly Ready"
-blocking_count: 1
-important_count: 7
-counting_method: "section_5_missing_parameters"
+blocking_count: 2
+important_count: 8
+counting_method: "all_sections_deduplicated — Section 1: 1 blocking (no Firefly engineering parameters → MANTA proxy required); Section 2: 1 blocking (NT confinement scaling at reactor scale truly-unknown); Sections 3–5 yielded important and nice-to-have gaps only; deduplicated across sections"
 section_coverage:
-  availability_of_data:       "Partial (concept class: Good; Firefly specifically: Opaque)"
+  availability_of_data:       "Partial"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
-  materials_supply_chain:     "Partial"
-  lcoe_parameter_extraction:  "Partial — sufficient for a first-pass model using MANTA as proxy; insufficient for Firefly-specific projections"
-```
+  materials_supply_chain:     "Poor"
+  lcoe_parameter_extraction:  "Partial"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
