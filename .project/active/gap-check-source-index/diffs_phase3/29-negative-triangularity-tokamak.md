# Phase 3 diff: 29-negative-triangularity-tokamak

**Generated:** 2026-05-22T15:44:12-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 2 | 0 | -2 |
| important_count  | 8 | 9 | - |
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
I now have all the information needed to write the gap assessment. Let me synthesize my findings across all sources read.
```

## Blocking-tier lines (new)

```
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/29-negative-triangularity-tokamak.md	2026-05-22 12:59:21.085458310 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/29-negative-triangularity-tokamak/gap_report.md	2026-05-22 15:44:12.287384986 -0700
@@ -1,13 +1,10 @@
-I now have sufficient data to write the full gap assessment. Let me compile it.
-
----
+I now have all the information needed to write the gap assessment. Let me synthesize my findings across all sources read.
 
 # Gap Assessment: Negative Triangularity Tokamak (D-T)
 
 ## Overall Readiness
 **Rating**: Mostly Ready
-
-**Summary**: The MANTA design study (Rutherford et al. 2024) is an unusually detailed academic reference — a fully integrated NT ARC-class pilot plant with explicit overnight cost ($3.4B), LCOE projection ($396/MWh for scaled commercial plant), balance-of-plant modeling, neutronics, and magnet lifetimes. This makes MANTA the best available proxy for an NT D-T tokamak concept analysis, compensating for Firefly Fusion's near-total lack of public technical disclosure (founded 2024, no published engineering parameters). The primary gaps are (1) NT confinement scaling at reactor conditions remains experimentally unvalidated at power-plant scale, creating genuine physics uncertainty ranges, and (2) Firefly's compact design (R≈2–2.5 m) is substantially smaller than MANTA (R=4.55 m), so direct cost transfer requires explicit scaling assumptions.
+**Summary**: The concept is anchored by the MANTA reference design (Rutherford et al. 2024), a comprehensive published pilot plant study covering plasma physics, magnets, blanket, balance of plant, and economics. NT confinement physics is experimentally validated at DIII-D, TCV, and ASDEX Upgrade. The TEA D-T MFE cost analysis (Araiinejad & Shirvan 2025) provides a closely analogous NOAK cost framework. The primary limitation is that Firefly Fusion itself has published almost nothing — MANTA is an MIT/Columbia academic study, not Firefly's design — and the concept's commercial-scale economics remain far from competitive based on current extrapolations ($396/MWh for a scaled MANTA). A D1+ analysis is feasible using MANTA as the design proxy with explicitly stated assumptions, but cannot be attributed to Firefly specifically.
 
 ---
 
@@ -17,22 +14,24 @@
 **Coverage**: Partial
 
 **Available**:
-- **MANTA reference design** (`iter-02/sources/manta-reference-design.md`): ~160 KB fully extracted paper covering all major subsystems, power balance (P_fus=450 MW, Q=11.5, P_net=90 MWe), overnight cost ($3.4B), and an explicit LCOE analysis for an NT pilot plant. This is the dominant technical source for the concept.
-- **Balestri, Ball, Coda 2024** (`iter-01/sources/ball-balestri-ohmic-nt-paper.md`): Full paper (55 KB) on ohmic-only NT tokamak feasibility across MANTA, SPARC, ITER, and DEMO parameter spaces. Directly authored by Firefly co-founder Justin Ball (EPFL/SPC). Quantitative confinement and Q projections under different heating assumptions.
-- **GreyB/Scouted interview** (`iter-01/sources/greyb-firefly-interview.md`): CEO Rustem Ospanov interview providing top-level Firefly parameters: R=2–2.5 m, B=10–12 T, Q>5, P_fusion=50–100 MW, 20–30 MW heating input.
-- **DIII-D collaboration page** (`iter-01/sources/firefly-fusion-diii-d-collaboration.md`): Confirms DIII-D collaboration, LUCIOLE prototype (copper magnets), and NT experimental program.
-- **ARIES-ACT studies** (`iter-04/sources/osti-servlets-purl-*.md`): Conventional PT tokamak power plant parametric studies (advanced R=6.25 m/58% efficiency; conservative R=9.75 m/45%) — useful as cost analogs and CAS framework references.
-- **ARIES Cost Account Documentation** (`iter-04/sources/qedfusion-lib-report-aries-act-ucsd-cer-13-01.md`): CAS methodology reference (Accounts 20–27 direct, 90–98 indirect); provides the costing framework applicable to MANTA-derived estimates.
-- **Arxiv abstracts** (2401.15217, 2405.01514, 2501.14682): NT vertical stability analysis, fusion plant maintenance grid economics, and NT electromagnetic system design — abstracts only (3–4 KB each); content limited to titles and abstracts.
+- CEO interview (GreyB/Scouted, `iter-01/sources/greyb-firefly-interview.md`): R=2–2.5 m, B=10–12 T, Q>5, P_fus=50–100 MW, HTS magnets commercial target
+- DIII-D collaboration page (`iter-01/sources/firefly-fusion-diii-d-collaboration.md`): confirms LUCIOLE prototype with copper magnets, NT focus, DIII-D experimental partnership
+- MANTA reference design (`iter-02/sources/manta-reference-design.md`): the most detailed NT tokamak pilot plant study published to date — full plasma parameters, magnet design, FLiBe blanket, ICRF heating, steam Rankine cycle, $3.4B overnight cost, Table 1 key parameters
+- Balestri, Ball & Coda 2024 (`iter-01/sources/ball-balestri-ohmic-nt-paper.md`): physics basis for ohmic-only NT operation; applies MANTA, SPARC, ITER, DEMO to 0D power balance
+- Vertical stability study (abstract, `iter-04/sources/arxiv-2401-15217.md`): confirms NT is less vertically stable than PT; passive stabilizing plates mitigate growth rates to ~16% of baseline
+- NT EM system pre-conceptual design (abstract, `iter-04/sources/arxiv-2501-14682.md`): R₀=1m, 3T copper NT tokamak EM design using TokaMaker — relevant to Firefly's LUCIOLE scale
+- Maintenance economics (abstract, `iter-04/sources/arxiv-2405-01514.md`): value of fusion plant maintenance strategies in decarbonized 2050 US grid; seasonal scheduling can increase plant value 15%
+- ARIES ACT studies (`iter-04/sources/osti-servlets-purl-1127358.md`, `osti-servlets-purl-1178069.md`): advanced/conservative PT tokamak designs at ~1000 MWe scale; provide tokamak cost methodology and BOP analog
+- ARIES cost account documentation (`iter-04/sources/qedfusion-lib-report-aries-act-ucsd-cer-13-01.md`): full CAS framework (accounts 20–27 direct, 90–98 indirect) from Starfire through ARIES series
 
 **Missing**:
-- Firefly's actual reactor design parameters (dimensions, magnet design, blanket, heating system) beyond CEO interview
-- Published engineering data from Firefly's DIII-D collaboration (ongoing, unpublished)
-- Any Firefly financial model or cost estimate
+- Any Firefly publication on LUCIOLE design parameters (geometry, plasma performance targets, heating systems, blanket approach)
+- Firefly conference presentations or FIA white paper with technical content
+- Dedicated NT tokamak commercial plant study (MANTA is a pilot plant, not a commercial design)
 
 **Gaps**:
-- No Firefly-specific engineering publication — `proprietary` — **blocking**: forces reliance on MANTA proxy for all engineering details; explicitly scope the analysis as "NT ARC-class, with Firefly parameters as available"
-- NT confinement experiments at reactor-relevant conditions (burning plasma, D-T) — `truly-unknown` — **important**: DIII-D/TCV results are at low B and DD plasma; scaling to 11 T REBCO D-T burning plasma is extrapolated
+- Firefly design parameters beyond CEO-level ballparks — proprietary — important
+- NT tokamak pilot-to-commercial extrapolation relies on a single major published study (MANTA) — not-yet-sourced — important
 
 ---
 
@@ -40,142 +39,130 @@
 **Coverage**: Partial
 
 **Available**:
-- **NT confinement physics**: MANTA uses H₉₈y₂ = 0.79–1.44 depending on scenario; Ball et al. show H₈₉ enhancement factor range 1.4–2.0 as the dominant physics uncertainty. This uncertainty range is explicitly quantified and bounded.
-- **Ohmic vs. auxiliary heating system function**: Ball et al. show that at MANTA/SPARC parameters, ohmic-only NT achieves Q~500 vs. Q~30–80 for heated scenarios — a fundamentally different system architecture. Firefly's actual choice is unknown, creating a forked system-function model.
-- **Pulsed operation thermal management**: MANTA's molten salt thermal storage (60% NaNO₃/40% KNO₃ secondary loop) handles 15-min pulses with 2-min inter-pulse. Full thermodynamic analysis available.
-- **Divertor/power handling with NT**: MANTA's UEDGE simulations show peak heat flux 2.8 MW/m² (vs. 10 MW/m² limit), with ELM-free NT enabling higher impurity seeding fractions and lower P_SOL (23.5 MW for 450 MW fusion). This is a quantitative result with explicit uncertainty discussion.
-- **Vertical stability**: arXiv:2401.15217 (abstract only) confirms NT is less vertically stable than PT at equivalent parameters and requires passive stabilizing plates. MANTA addresses this in design.
-- **VV material compatibility with FLiBe**: MANTA identifies V-4Cr-4Ti + MoF6 self-healing barrier as the chosen approach; acknowledges this is a novel, low-TRL approach requiring future validation.
+- NT L-mode-enhanced confinement mechanism is well-described: H98~1.44 achieved in MANTA integrated modeling (TGYRO + TGLF + CHEASE + UEDGE workflow); experimental validation shows H98~1.0 achievable on TCV and DIII-D (`manta-reference-design.md` §2, §Appendix B)
+- Ballestri et al. demonstrate ohmic operation feasibility at MANTA/SPARC parameters (Q~500 Ohmic vs Q~30 with 40MW heating) (`ball-balestri-ohmic-nt-paper.md`)
+- Divertor challenge quantified: MANTA achieves peak heat flux 2.8 MW/m² via ELM-free + impurity seeding (Kr) + NT geometry placing divertor at larger major radius; M₂ metric 10–20× lower than EU-DEMO (`manta-reference-design.md` §3, Table 2)
+- FLiBe liquid immersion blanket integration with demountable TF coils described (`manta-reference-design.md` §5); conformal VV with FLiBe channels used to cool divertor targets
+- Vertical stability challenge identified and mitigation via passive stabilizers demonstrated (abstract, `arxiv-2401-15217.md`)
 
 **Missing**:
-- Experimental validation of NT confinement at burning plasma conditions or D-T (not yet achieved anywhere)
-- Experimental data on NT stability with FLiBe blanket or high-Z first wall in NT geometry
-- How Firefly's compact design (R~2 m) handles the power-exhaust problem at high power density relative to MANTA (R=4.55 m)
+- Experimental demonstration of ELM-free NT operation at burning plasma parameters (nτT approaching NT pilot plant targets) — current NT experiments are far below fusion conditions
+- NT-specific system code modeling: standard tokamak system codes (PROCESS, BLUEPRINT) use H-mode assumptions and may not handle NT L-mode operation correctly
+- MANTA's integrated modeling uses full-physics codes (TGYRO, TGLF) — no simplified system-code-level model of NT exists for fast LCOE sensitivity scans
+- Confinement degradation with impurity seeding in NT: MANTA assumes Kr seeding compatible with L-mode transport, but experimental basis is limited
 
 **Gaps**:
-- NT confinement enhancement factor at reactor-relevant D-T conditions — `truly-unknown` — **blocking**: the H₉₈ uncertainty range (0.79–1.44 in MANTA) translates directly into whether ignition/high-Q is achievable; this is the fundamental physics bet
-- Heating architecture choice (ohmic vs. ICRH vs. ECRH) — `proprietary`/`not-yet-sourced` — **important**: different heating approaches imply very different capital costs ($0 vs. tens of millions for an ICRF system) and recirculating power fractions
-- First-wall material compatibility in NT geometry (different divertor location) — `not-yet-sourced` — **important**: NT puts the broad face outboard; MANTA acknowledges divertor target asymmetries
+- NT confinement scaling uncertainty at reactor-relevant parameters (H98 enhancement factors from TCV/DIII-D may not extrapolate to burning plasma regimes) — derivable with stated uncertainty — important
+- Absence of NT-compatible system code (standard codes assume H-mode) prevents rapid parameter scans needed for cost sensitivity — truly-unknown (no NT system code yet published) — important
+- Vertical stability solutions engineering at pilot-plant scale — not-yet-sourced (full paper exists but only abstract captured) — important
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
 **Coverage**: Partial
 
-**Available**: MANTA provides TRL-relevant detail on most subsystems:
-
-| Subsystem | TRL Basis from Sources | Source |
-|-----------|----------------------|--------|
-| NT plasma confinement | TRL 4–5 (DIII-D, TCV experiments at low B/DD; no reactor-scale data) | MANTA Sec. 2; Ball et al. |
-| REBCO HTS TF coils (18-coil, 11 T) | TRL 5–6 (SPARC TFMC demonstrated; MANTA design extrapolates from TFMC) | MANTA Sec. 4 |
-| Non-insulated REBCO coil operation | TRL 4–5 (SPARC TFMC; MANTA's 67-day ramp problem → oversized cryoplant required) | MANTA Sec. 4.2 |
-| ICRF heating (40 MW at 110 MHz) | TRL 7–8 (established at JET, WEST; SPARC uses same minority-3He scheme) | MANTA Sec. 2, Sec. 3 |
-| FLiBe liquid immersion blanket | TRL 3–4 (material well-characterized; no reactor-scale system operated) | MANTA Sec. 5 |
-| V-4Cr-4Ti VV with MoF₆ barrier | TRL 2–3 (proposed material; MoF₆ self-healing barrier is novel/unvalidated) | MANTA Sec. 5 |
-| Sub-critical Rankine with molten salt storage | TRL 6–7 (solar thermal heritage; FLiBe primary coupling is lower TRL) | MANTA Sec. 6 |
-| Tritium fuel cycle | TRL 2–3 (no closed D-T tritium cycle at scale; MANTA uses conservative estimates) | MANTA Sec. 5.4 |
-| Tungsten plasma-facing divertor | TRL 5–6 (ITER heritage; NT-specific divertor geometry novel) | MANTA Sec. 3.3 |
+**Available**:
+- **REBCO HTS TF coils (TRL 5–6)**: SPARC TFMC demonstrated 20 T at CFS; MANTA uses 11 T on-axis, well within REBCO demonstrated range. MANTA TF coil design detailed (non-insulated wound, window-pane geometry, 18 coils, max von Mises stress 600 MPa) (`manta-reference-design.md` §4)
+- **ICRF heating (TRL 7–8)**: 40 MW at 110 MHz (existing high-power tetrodes); He-3 minority species. MANTA design cites frequency achievable with existing technology (`manta-reference-design.md` §2.2.1)
+- **FLiBe blanket (TRL 2–3)**: liquid immersion blanket design detailed; TBR=1.15, blanket power multiplication 1.11; FLiBe chemistry management (MoF₆ dissolved for self-healing Mo barrier) specified; no reactor-scale FLiBe blanket has operated (`manta-reference-design.md` §5)
+- **Tungsten first wall (TRL 7)**: 0.3 cm W PFCs described; UEDGE-predicted sputtering rate 0.0016 mm/yr from 0.315% Ne (`manta-reference-design.md` §3.1–3.2)
+- **V-4Cr-4Ti vacuum vessel (TRL 3–4)**: activation 3 orders of magnitude lower than SS316LN; DPA tolerance estimated but requires experimental validation (`manta-reference-design.md` §5.3); 2 DPA/100 MW-yr average
+- **Steam Rankine cycle (TRL 9)**: two-stage molten-salt heat exchange loop; standard technology selected over Brayton/supercritical Rankine (`manta-reference-design.md` §6)
+- **Central solenoid (TRL 5)**: REBCO PIT-VIPER-like cables; insulated for low AC losses; PF2 minimum lifetime 890 MW-yr (~2 full-power years at 450 MW) (`manta-reference-design.md` §4.3, Table 7)
 
 **Missing**:
-- TRL assessment for Firefly's specific prototype path (LUCIOLE with copper magnets → no TRL data)
-- Independent TRL assessments from any government or regulatory source for NT-specific systems
+- TRL of NT plasma control algorithms at pilot plant scale — LUCIOLE will validate this but doesn't exist yet
+- Tritium fuel cycle maturity: MANTA models startup inventory 440g, reserve 75g; notes fuel cycle is "not fully developed or tested" (`manta-reference-design.md` §5.4); TRL 2–3 for fusion-scale tritium processing
 
 **Gaps**:
-- FLiBe blanket and tritium fuel cycle TRL detail — `not-yet-sourced` — **important**: fusion TBR demonstration and closed tritium loop are universally recognized as program-pacing items; more detailed sources (e.g., FLiBe-2 program, FNSF studies) likely exist on OSTI
-- NT-specific first-wall erosion lifetime data — `truly-unknown` — **nice-to-have**: NT's wider outboard plasma face changes the erosion geometry
+- REBCO tape production at commercial scale (5730 km cables per ARC-class device per TEA D-T MFE cost analysis, `knowledge/sources/tea_dt_mfe_cost_analysis/output.md`) — not-yet-sourced — important
+- FLiBe blanket first-of-a-kind risk: no operating precedent for molten salt lithium-beryllium blanket in fusion environment — truly-unknown (reactor-scale data doesn't exist) — important
+- Tritium fuel cycle full integration at pilot plant scale — truly-unknown — important
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Poor
+**Coverage**: Partial
 
 **Available**:
-- MANTA provides material quantities: 18 REBCO TF coils requiring 13.6 MA-turns (REBCO tape quantity computable from the 570 A/mm² operating density and coil geometry parameters in Table 4); ~1.1 million kg Inconel-718 structural material
-- MANTA identifies REBCO tape cost as the single largest cost uncertainty driver (sensitivity ±50% keeps plant under $5B NASEM limit)
-- Tritium startup inventory: 440g needed; global annual production ~2.7 kg/yr (explicitly stated in MANTA Sec. 7.2 as potentially market-saturating)
-- FLiBe identified as a high-TBR breeder/coolant; beryllium content (BeF₂) implies supply constraints (not explicitly discussed in MANTA)
-- Li-6 enrichment requirement for FLiBe implied but not quantified
-- Tungsten first wall and W-C shielding quantities noted in MANTA Table 6
+- **REBCO tape cost**: MANTA TF coil cost $1.5B (~44% of total overnight cost $3.4B); sensitivity: ±50% REBCO cost → ±25% overnight cost, remaining under $5B limit (`manta-reference-design.md` §7.1, Fig. 25)
+- TEA D-T MFE cost analysis identifies 5730 km REBCO cable per ARC-class device; REBCO material is the single largest cost uncertainty (`knowledge/sources/tea_dt_mfe_cost_analysis/output.md` §2.2.1)
+- **FLiBe**: MANTA uses FLiBe as both blanket and primary coolant; cost included in sensitivity analysis; Be supply is a concern (US strategic material)
+- **Tungsten**: commercially available; W sputtering in MANTA divertor modeled as negligible (0.0016 mm/yr)
+- **V-4Cr-4Ti**: MANTA identifies as low-activation VV material; limited industrial production capacity currently
 
 **Missing**:
-- Explicit REBCO tape quantity calculation for MANTA's TF coils
-- FLiBe supply chain analysis (BeF₂ supplier landscape, Be safety handling costs)
-- Li-6 enrichment supply and export control implications
-- REBCO tape supply chain deep-dive (commercial suppliers, pricing trend)
-- V-4Cr-4Ti production scale (specialty alloy with limited commercial production)
+- REBCO production trajectory: current global capacity vs. demand from multiple ARC-class devices
+- Beryllium supply chain: FLiBe contains Be; US Be reserves at Spor Mountain (Utah) are the dominant global source; strategic material with export controls
+- Li-6 enrichment for tritium breeding: TBR=1.15 based on natural Li; enriched Li-6 would reduce blanket volume but requires isotope separation capacity
 
 **Gaps**:
-- REBCO supply chain capacity and cost trajectory — `not-yet-sourced` — **important**: TF coil cost ($1.5B) is the dominant MANTA capital cost driver; REBCO supply/price uncertainty is the largest cost sensitivity; CFS/ITER magnet program may have updated supply data
-- Li-6 enrichment for FLiBe breeder blanket — `not-yet-sourced` — **important**: 6Li enrichment is export-controlled; supply constraints could affect deployment timeline
-- BeF₂/FLiBe supply and safety costs — `not-yet-sourced` — **important**: beryllium is toxic and tightly regulated; handling infrastructure cost is not captured in MANTA's cost model
-- Tritium availability for startup — `derivable` (from MANTA's 440g estimate + known CANDU production rate) — **important**: tritium startup cost is a known first-plant blocker
+- REBCO supply chain bottleneck quantification for commercial deployment — not-yet-sourced — important
+- Beryllium supply constraints for FLiBe blanket at scale — not-yet-sourced — important
+- Li-6 enrichment supply chain — not-yet-sourced — nice-to-have
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Partial
-
-**Available Parameters** (from MANTA as NT pilot plant proxy):
-
+**Available Parameters**:
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Fusion power | 450 MW (MANTA); 50–100 MW (Firefly target) | MANTA Table 1; GreyB interview | h (MANTA); m (Firefly) |
-| Net electric power | 90 MWe | MANTA Table 1, Sec. 6.3 | h (MANTA) |
-| Plasma gain Q | 11.5 | MANTA Table 1 | h (MANTA) |
-| Electricity gain Q_E | 2.4 | MANTA Table 1 | h (MANTA) |
-| Thermal efficiency | 36% (sub-Rankine), 39% (super-Rankine) | MANTA Table 8 | h (MANTA) |
-| Power cycle type | Sub-critical Rankine + molten salt storage | MANTA Sec. 6 | h (MANTA) |
-| Overnight capital cost (pilot) | $3.4B ≈ $38M/MWe | MANTA Sec. 7.1 | m (pilot-scale proxy) |
-| TF coil cost (dominant driver) | $1.5B of $3.1B tokamak cost | MANTA Sec. 7.1 | m |
-| Commercial LCOE projection | $396/MWh (550 MW, 30 yr project) | MANTA Sec. 7.2 | l (explicitly too high; path to competitiveness requires higher magnet lifetime + power) |
-| TBR | 1.15 | MANTA Sec. 5 | h (MANTA design) |
-| Blanket power multiplication | 1.11 | MANTA Sec. 5 | h (MANTA design) |
-| Tritium startup inventory | 440g | MANTA Sec. 5.4 | m |
-| Pulse length | ~15 min / 2 min inter-pulse | MANTA Table 1 | h (MANTA design) |
-| TF coil lifetime | ~3,100–30,400 MW-yr (min–mean) | MANTA Table 7 | m |
-| PF coil lifetime (limiting) | ~890 MW-yr (PF2 minimum) → replacement every ~2 full-power years | MANTA Table 7 | m |
-| Major radius | 4.55 m (MANTA proxy); 2–2.5 m (Firefly target) | MANTA Table 1; GreyB | h/m |
-| Toroidal field | 11 T (MANTA); 10–12 T (Firefly) | MANTA; GreyB | h |
-| Auxiliary heating power | 40 MW ICRF (MANTA); possibly 0–30 MW (Firefly) | MANTA Sec. 2; Ball et al. | m |
-| Recirculating power | ~62 MWe (RF 57 MWe + cryo 1 MWe + pumps ~4 MWe) | MANTA Table 8 | h (MANTA) |
+| Fusion power | 450 MW (MANTA proxy); 50–100 MW (Firefly target) | `manta-reference-design.md` Table 1; GreyB interview | m |
+| Net electric power | 90 MWe (MANTA pilot) | `manta-reference-design.md` Table 1 | m |
+| Electricity gain Q_E | 2.4 | `manta-reference-design.md` Table 1 | m |
+| Plasma gain Q | 11.5 | `manta-reference-design.md` Table 1 | m |
+| Thermal power | 530 MW total (MANTA) | `manta-reference-design.md` Table 1 | m |
+| ICRF heating power | 40 MW at 110 MHz | `manta-reference-design.md` §2.2.1 | m |
+| Overnight cost (pilot) | $3.4B (~$38M/MWe) | `manta-reference-design.md` §7.1 | m |
+| Overnight cost (NOAK ARC-class) | $8,800–$22,200/kW for 350 MWe | `knowledge/sources/tea_dt_mfe_cost_analysis/output.md` | m |
+| TF coil cost (dominant) | $1.5B (~44% of overnight) | `manta-reference-design.md` §7.1, Fig. 24 | m |
+| LCOE (MANTA scaled to 550 MW, 30 yr) | $396/MWh | `manta-reference-design.md` §7.2 | l |
+| LCOE analog (NOAK D-T MC tokamak) | $140–$550/MWh | `knowledge/sources/tea_dt_mfe_cost_analysis/output.md` | m |
+| TF coil lifetime | 3,100±400 MW-yr (~7 yr at 450 MW) | `manta-reference-design.md` Table 7 | m |
+| PF2 coil lifetime (binding) | 890±40 MW-yr (~2 full-power yr) | `manta-reference-design.md` Table 7 | m |
+| Energy conversion cycle | Steam Rankine (two-stage molten salt) | `manta-reference-design.md` §6 | m |
+| Tritium breeding ratio | 1.15 (min needed: 1.02) | `manta-reference-design.md` §5, Table 9 | m |
+| Tritium startup inventory | 440g | `manta-reference-design.md` §5.4 | m |
+| Major radius (MANTA) | 4.55 m | `manta-reference-design.md` Table 1 | h |
+| Toroidal field on axis | 11 T | `manta-reference-design.md` Table 1 | h |
+| Plasma current | 10 MA | `manta-reference-design.md` Table 1 | h |
+| Pulse length | ~15 min inductive | `manta-reference-design.md` Table 1 | h |
+| Inter-pulse length | ~2 min | `manta-reference-design.md` Table 1 | h |
+| Bootstrap fraction | 18% | `manta-reference-design.md` Table 1 | m |
 
 **Missing Parameters**:
-
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Availability factor / capacity factor (explicit %) | derivable | important | MANTA's 16.1-day maintenance cycle provides inputs; annual availability estimate requires unscheduled outage frequency assumption. Not stated as a single number. |
-| O&M cost breakdown (personnel, consumables, annual capital replacement) | derivable | important | MANTA references Table C5 in appendix, but that appendix content was not fully captured in extraction; total annual O&M not given as a line item |
-| Firefly-specific capital cost model (for R~2 m design) | proprietary | blocking | MANTA's $3.4B is for R=4.55 m; cost scaling to R~2 m is not straightforward due to non-linear magnet cost scaling |
-| REBCO cost per kg/unit length at production scale | not-yet-sourced | important | Current tape costs are $40–100/m² commercial; power plant scale discount trajectory unknown |
-| Li-6 enrichment cost for FLiBe | not-yet-sourced | important | Cost not addressed in MANTA; needed for blanket cost estimation |
-| Decommissioning cost | derivable | nice-to-have | MANTA mentions VV activation is 3 orders of magnitude lower than SS316LN; decommissioning cost not computed |
-| Fuel cost (D-T, excluding startup tritium) | derivable | nice-to-have | Tritium cost dominates; deuterium cost negligible; MANTA models tritium revenue not cost in equilibrium |
+| Thermal efficiency (cycle) | derivable | important | MANTA uses sub-critical Rankine; efficiency not explicitly stated. FLiBe outlet temperature limits cycle performance. Estimated ~25% gross; MANTA Q_E=2.4 implies ~17% net efficiency (P_net=90 / P_th=530). High-temperature Rankine or Brayton could reach 45–58% (ARIES ACT SiC/Brayton). |
+| Capacity factor (commercial) | derivable | important | MANTA pilot plant limited by PF2 replacement every ~2 full-power years. Commercial plant would require extended PF lifetimes or modular replacement. No formal availability study published for NT pilot plant. |
+| O&M costs (annual, commercial) | derivable | important | MANTA reports 8.5-year gross loss of $512M; magnet replacement dominates. NOAK O&M not independently estimated in any source. |
+| Heating system cost breakdown | proprietary | important | MANTA ICRF 40 MW cost not itemized separately in available economic tables. Three competing hypotheses for Firefly (ECRH vs. ICRH vs. ohmic). |
+| Firefly-target-scale plant economics | proprietary | important | Firefly targets R≈2–2.5m, P_fus=50–100 MW — significantly smaller than MANTA (R=4.55m, 450 MW). Direct cost scaling to smaller NT tokamak not published. |
+| Decommissioning cost estimate | not-yet-sourced | nice-to-have | MANTA assumes brownfield site saving ~$400M; decommissioning cost not explicitly calculated. ARIES CAS accounts 90-98 cover this category. |
+| Fuel costs (D-T acquisition) | derivable | nice-to-have | Tritium startup inventory 440g at ~$30,000/g → ~$13M; ongoing T² production (MANTA generates 1.8 kg/yr net excess). D costs negligible. |
 
 ---
 
 ## Source Recommendations
 
-1. **MANTA Appendix C** (Tables C1–C5): The MANTA paper references detailed cost breakdowns in Appendix C that were not fully extracted from the PDF. A targeted re-extraction of the appendix pages would fill the O&M cost breakdown gap. [Not yet sourced — the appendix content is likely in the same PDF]
-
-2. **REBCO supply chain analysis**: Search OSTI or IEEE for Commonwealth Fusion Systems REBCO tape procurement studies or APS/SOFE conference papers on REBCO production scale-up. Query: "REBCO high temperature superconductor production scale fusion magnet cost" on OSTI. — `unverified — confirm existence before searching`
-
-3. **FLiBe supply and handling costs**: DOE FES has funded FLiBe studies (e.g., FLiBe Advances); search OSTI for "FLiBe fluoride salt tritium breeding blanket supply chain". Flibe Energy LLC (private, US) is also a potential source. — `unverified — confirm existence before searching`
-
-4. **Li-6 enrichment for fusion**: ORNL has published on Li-6 isotope production (Y-12 complex). Search OSTI for "lithium-6 enrichment fusion tritium breeding blanket" — government lab reports likely exist. — `unverified — confirm existence before searching`
-
-5. **NT confinement at high field / reactor-relevant conditions**: DIII-D NT experimental campaign publications (Paz-Soldan et al., cited in MANTA) would provide the most current confinement data; specific papers are cited in MANTA references [24], [29] — these would be the highest-value physics sources to add. One is directly cited: C. Paz-Soldan et al. DIII-D team, *Plasma Physics and Controlled Fusion*, 2021. — `unverified for individual paper quality but referenced in MANTA`
-
-6. **TEA D-T MFE Cost Analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): This fleet-wide source covers D-T MFE CAS cost methodology. Applicable for validating MANTA cost account structure against standard D-T tokamak CAS and for O&M cost analogs — **directly applicable to this concept; recommend reading for CAS cross-check**.
-
-7. **Revisit of 2017 ARPA-E ALPHA Costing** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`): Covers CAS cost structures across four compact fusion concepts; useful for cross-checking MANTA's cost account methodology and confirming whether $38M/MWe is reasonable for a pilot plant — **moderately applicable; read for CAS validation**.
+- **NT confinement scaling at reactor parameters**: The MANTA paper (`iter-02/sources/manta-reference-design.md`) cites Wilson et al. 2024 ("Characterizing the negative triangularity reactor core operating space with integrated modeling," *PPCF*) — this paper provides integrated modeling validation of NT operating space but was not ingested. Search OSTI/arXiv for NT TGYRO/integrated modeling papers from Columbia/MIT group. `unverified — confirm existence before searching`
+- **Capacity factor and availability modeling**: Schwartz et al. 2024 (`iter-04/sources/arxiv-2405-01514.md`) addresses maintenance economics for fusion plants — the full paper was not read (only abstract). Ingest full paper for seasonal availability and maintenance strategy quantification.
+- **REBCO supply chain**: Fusion Industry Association supply chain reports (annual) or CFS/REBCO manufacturer supply agreements would provide production capacity data. Search FIA.org for supply chain working group outputs. `unverified — confirm existence before searching`
+- **NT system code**: No NT-compatible systems code appears to exist in the literature yet. This is a genuine modeling gap. The Firefly/MANTA approach requires case-by-case integrated modeling (TGYRO-class), which is computationally expensive. Flag this clearly in the analysis.
+- **Beryllium supply constraints for FLiBe**: IAEA documents on Be availability and IFE literature (energy_from_inertial_fusion has Be target discussion) provide partial analog; a formal FLiBe supply chain study for fusion does not appear to exist publicly.
+- **ARIES ACT cost data for BOP analog**: The two OSTI ARIES ACT sources (`osti-servlets-purl-1127358.md`, `osti-servlets-purl-1178069.md`) were read and are applicable for BOP and indirect cost structure. These are PT tokamaks at 1000 MWe scale with Nb3Sn magnets — different architecture — but turbine plant (CAS 23), electrical plant (CAS 24), and site structure (CAS 21) costs are transferable analogs. Explicitly disqualified as direct reactor core cost analog due to different scale, magnet technology (Nb3Sn vs. REBCO), and plasma regime (H-mode vs. NT L-mode).
+- **ARPA-E ALPHA revisit** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/output.md`): Read. Reports ~$43/MWh LCOE for ~500 MWe modular non-tokamak concepts (FRC, MTF, Z-pinch) under CAS framework. Not applicable as a direct tokamak cost analog — architectures differ fundamentally, and the $43/MWh optimistic figure targets commercial-scale modular concepts with very different cost structures. Disqualified as direct LCOE analog for NT tokamak pilot plant.
+- **Progress toward fusion breakeven (Wurzel & Hsu)** (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/output.md`): Read. Provides TRL context for NT tokamak concept: tokamak MCF has the highest demonstrated nτT values, approaching burning plasma threshold. NT-specific data is not broken out separately from tokamak MCF (TCV/DIII-D NT plasmas are at far lower nτT than JET/ITER/SPARC targets). Useful for §3 TRL framing — confirms that NT physics at burning plasma scale is extrapolated, not demonstrated. Integrated into TRL assessments above.
 
 ---
 
 ## Summary
 
-**Proceed to full D1+ analysis, with explicit proxy scoping.** The MANTA 2024 reference design provides the most detailed publicly available NT D-T tokamak engineering and economic model. All five D1+ sections can be populated, but the analysis should be framed as "NT ARC-class tokamak (MANTA proxy) with Firefly-specific context where available." The two areas requiring explicit uncertainty treatment are: (1) NT confinement enhancement at reactor scale, which remains an unvalidated extrapolation, and (2) capital cost scaling from MANTA's R=4.55 m to Firefly's R~2 m target, which requires order-of-magnitude reasoning rather than direct transfer. The commercial LCOE projection ($396/MWh) is available but explicitly uncompetitive, with MANTA's own analysis identifying the path (longer magnet lifetimes, higher fusion power, better thermal efficiency) — this should be treated as the current baseline with a clearly stated improvement pathway, not a competitive LCOE claim.
-
-Before starting the full analysis, consider extracting the MANTA Appendix C tables (cost breakdown Tables C1–C5) and cross-checking against `knowledge/sources/tea_dt_mfe_cost_analysis/` for CAS alignment.
+**Proceed to full analysis.** The MANTA reference design provides sufficient coverage to produce a high-quality D1+ analysis of the negative triangularity tokamak concept with MANTA as the explicit proxy design. The analysis should:
+1. Clearly distinguish Firefly Fusion (early-stage company, no published design) from the MANTA academic pilot plant study that serves as the NT tokamak reference
+2. Use the TEA D-T MFE cost analysis (Araiinejad & Shirvan 2025) for NOAK cost scaling ($140–$550/MWh LCOE range, $8,800–$22,200/kW capital) — this is the best available NOAK economic framework for an ARC-class REBCO D-T tokamak
+3. Flag the NT system-code gap explicitly: standard tokamak system codes assume H-mode, not NT L-mode; cost sensitivity scans require either code adaptation or direct use of MANTA/Balestri 0D power balance
+4. Note that current pilot plant economics ($396/MWh scaled-up MANTA) are far from competitive, and identify the specific engineering improvements needed (extended magnet lifetimes, higher beta, high-temperature cycle) that MANTA itself quantifies
 
 ---
 
@@ -183,13 +170,13 @@
 
 ```yaml
 overall_rating: "Mostly Ready"
-blocking_count: 2
-important_count: 8
-counting_method: "all_sections_deduplicated — Section 1: 1 blocking (no Firefly engineering parameters → MANTA proxy required); Section 2: 1 blocking (NT confinement scaling at reactor scale truly-unknown); Sections 3–5 yielded important and nice-to-have gaps only; deduplicated across sections"
+blocking_count: 0
+important_count: 9
+counting_method: "deduplicated across all five sections: (1) NT tokamak pilot-to-commercial extrapolation limited to single study, (2) NT confinement scaling at reactor parameters, (3) NT system code absence, (4) vertical stability engineering at pilot-plant scale, (5) REBCO supply chain bottleneck, (6) FLiBe blanket TRL and operating precedent, (7) tritium fuel cycle TRL, (8) commercial-scale capacity factor, (9) Firefly-specific reactor design parameters"
 section_coverage:
   availability_of_data:       "Partial"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
-  materials_supply_chain:     "Poor"
+  materials_supply_chain:     "Partial"
   lcoe_parameter_extraction:  "Partial"
 ```
\ No newline at end of file
```
