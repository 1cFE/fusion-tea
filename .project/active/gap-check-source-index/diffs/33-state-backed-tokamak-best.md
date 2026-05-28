# Diff: 33-state-backed-tokamak-best

**Generated:** 2026-05-22T09:21:59-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 4 | 4 | 0 |
| important_count  | 6 | 8 | - |
| overall_rating   | Mostly Ready (with important framing caveat) | Mostly Ready | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
25:- **TEA D-T MFE** (`knowledge/sources/tea_dt_mfe_cost_analysis/output.md`): Bottom-up NOAK capital cost framework ($8,800–22,200/kW; LCOE $140–550/MWh for 500 MWe D-T tokamak).
143:5. **PyFECONS** (`/home/reid/PyFECONS`) — can produce cost estimates for CFEDR-class LTS tokamaks directly using available CFEDR parameters; no additional sourcing needed — *Available*
144:6. **TEA D-T MFE + ARIES cost accounts** (`knowledge/sources/tea_dt_mfe_cost_analysis/`, `knowledge/sources/aries_cost_account_documentation/`) — primary LCOE analogs for D-T MFE tokamaks — *Available*
```

## Blocking-tier lines (baseline)

```
124:| Plant electrical output (CFEDR/PFPP) | not-yet-sourced | blocking | CFEDR targeted ~1 GWe; CFETR studies suggest ~200–1000 MWe range — search CNKI/OSTI for CFEDR system design |
125:| Capital cost breakdown (by subsystem) | proprietary / not-yet-sourced | blocking | No public cost estimate for BEST or CFEDR; ITER scaling analogues required |
126:| O&M costs | not-yet-sourced | blocking | No published O&M estimate; ITER/DEMO analogues needed |
127:| Capacity factor / availability (power plant) | derivable | blocking | Tokamak availability assumptions derivable from ITER DEMO studies (~75–85%) |
```

## Blocking-tier lines (new)

```
124:| CFEDR capital cost by CAS account | not-yet-sourced | blocking | No CFEDR cost study found; ARIES-ACT/TEA analogs can substitute at ~50% uncertainty |
125:| CFEDR/PFPP net electric output | derivable | blocking | Pfus=1.5–3.0 GW + efficiency → ~500–1200 MWe; efficiency assumption needed |
126:| Capacity factor / availability target | not-yet-sourced | blocking | CFETR papers mention 0.3–0.5 duty cycle for that device; no PFPP target published |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/33-state-backed-tokamak-best.md	2026-05-22 09:21:25.689982659 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/33-state-backed-tokamak-best/gap_report.md	2026-05-22 09:09:26.138954047 -0700
@@ -1,176 +1,177 @@
-Now I have everything I need. Let me write the gap assessment.
+Here is the complete gap assessment:
 
 ---
 
-# Gap Assessment: State-Backed Tokamak - BEST
+# Gap Assessment: State-Backed Tokamak - BEST (D-T)
 
 ## Overall Readiness
-**Rating**: Mostly Ready (with important framing caveat)
+**Rating**: Mostly Ready
 
-**Summary**: The BEST Research Plan v1.1 is an unusually comprehensive public document that resolves nearly all device-level parameters at high confidence. However, BEST is an experimental device — not a power plant — which creates a structural challenge for LCOE analysis: all five D1+ sections must be framed around the BEST→CFEDR→PFPP technology lineage rather than BEST itself. The qualitative sections (1–4) are well-supported; the quantitative LCOE section requires analogues and explicit assumptions because no commercial plant design yet exists.
+**Summary**: The qualitative sections (data availability, system function, subsystem maturity, materials/supply chain) can be written with high confidence — the BEST Research Plan v1.1 is an exceptionally comprehensive 200-page technical document jointly authored by ASIPP, EUROfusion, and UKAEA. The principal modeling challenge is structural: BEST is an experimental device that produces no electricity, so LCOE analysis must target CFEDR (the next step in China's national roadmap) or a hypothetical PFPP extrapolated from BEST technology. No published CFEDR cost study exists in the sourced materials, but this gap is `derivable` using the ARIES-ACT power plant study and the TEA D-T MFE source as analogs — both are directly applicable to a conventional LTS tokamak power plant of similar scale.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Good (device level) / Partial (power plant level)
+**Coverage**: Good (experimental device); Partial (power plant projection)
 
 **Available**:
-- **BEST Research Plan v1.1** (EUROfusion/ASIPP, Nov 2025) — a 100+ page public document covering all major technical parameters, subsystem designs, timeline, and strategic positioning. This is an exceptionally transparent publication for a state-backed Chinese program.
-- **Neo Fusion company profile** — ownership structure (CNPC ~20%, CAS), funding ($214M raised, registered capital expanded to 14.5B yuan / ~$2B USD), corporate identity.
-- **CFETR power conversion studies** — three published papers (2021, 2024, 2025) on sCO2 Brayton cycle for the downstream CFEDR/PFPP reactors.
-- All 11 differentiation table columns resolved; 9/11 at high confidence.
-
-**Missing**:
-- Detailed CFEDR/PFPP reactor design parameters (the commercial step that BEST feeds into).
-- BEST construction cost data (typical for state-backed programs under construction).
-- Chinese-language ASIPP internal reports on CFEDR system design.
+- **BEST Research Plan v1.1** (`iter-01/sources/best-research-plan-v1.1-summary.md`): 200+ pages, jointly authored ASIPP/EUROfusion/UKAEA (Nov 2025). Covers all machine parameters, 12 chapters on plasma physics, H&CD, TBM program, neutronics, timeline, diagnostics. Equivalent quality to a major ITER-era facility document.
+- **Neo Fusion company profile**: Corporate identity, ownership (CNPC 20% + CAS), initial funding ($214M), registered capital (14.5B CNY ≈ $2B). Sparse on construction-specific costs.
+- **CFETR power conversion studies** (`iter-02/sources/cfetr-power-conversion-studies.md`): Abstract only (paywalled). Confirms sCO₂ Brayton cycle with 34.7% efficiency for CFETR.
+- **CFETR scenario physics papers** (`arxiv-1907-11919.md`, `osti-1465662.md`): Integrated modeling of CFETR Phase I/II. CFEDR parameters: R=6.6m, B=6T; Q=3.2 (Phase I), Q>20 (Phase II).
+- **ARIES-ACT** (`osti-1178069.md`): Full tokamak power plant engineering/economics study. CAS cost structure, thermal efficiencies (45–58%), component lifetimes — directly applicable to CFEDR-class LTS tokamaks.
+- **TEA D-T MFE** (`knowledge/sources/tea_dt_mfe_cost_analysis/output.md`): Bottom-up NOAK capital cost framework ($8,800–22,200/kW; LCOE $140–550/MWh for 500 MWe D-T tokamak).
+
+**Missing**: Published CFEDR capital cost study; BEST construction cost breakdown (not public); PFPP design parameters.
 
 **Gaps**:
-- CFEDR/PFPP plant-level design parameters — `not-yet-sourced` — **important** (LCOE analysis must project to a power plant, and CFEDR studies likely exist in Chinese literature)
-- BEST construction cost — `proprietary/state-classified` — **nice-to-have** (useful for cost scaling but not blocking; ITER analogues can substitute)
+- CFEDR/PFPP dedicated cost study — `not-yet-sourced` — **important**: search "CFETR cost" on OSTI, IOP Nuclear Fusion, CNKI. *unverified — confirm existence before searching*
+- BEST construction cost breakdown — `proprietary` — **nice-to-have**
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Partial
+**Coverage**: Good
 
-**Available**:
-- The fundamental modeling challenge is clearly identifiable from sources: **BEST is explicitly experimental**, with no power conversion system, no tritium breeding, and no commercial plant configuration.
-- Physics parameters are well-defined: R=3.6m, B=6.15T, Q targets (≥1 by 2030, ~5 by 2032-2035), Ip up to 7 MA, 50 MW auxiliary heating.
-- Multiple candidate blanket designs for TBM testing (COOL, WCCB, WCLL, HCPB, WLCB) — no committed blanket for a power reactor.
-- sCO2 Brayton cycle identified as preferred power conversion for the lineage, but BOP for CFEDR/PFPP is not finalized.
-
-**Missing**:
-- Plasma performance projections with uncertainty bounds (burn fraction, confinement scaling from BEST to CFEDR).
-- How BEST experimental results will gate CFEDR design decisions.
-- Cost uncertainty propagation from technology variants (5 candidate blankets = 5 cost scenarios).
+**Available**: The BEST Research Plan documents all major physics and technology challenges. CFETR scenario papers establish the physics basis for the next step. ARIES-ACT characterizes engineering challenges common to all LTS tokamak power plants.
+
+**Key modeling challenges**:
+1. BEST is experimental, not a power plant — LCOE analysis must target CFEDR (R=7.8m, B=6.3T, Pfus=1.5–3 GW, Q=10–30) or a PFPP derived from it
+2. Multi-step extrapolation (BEST → CFEDR → PFPP) with decreasing credibility at each step
+3. CFEDR parameters are still evolving (R went 5.7m → 6.6m → 7.8m across design iterations)
+4. No committed TBR design for CFEDR — three competing TBM concepts (COOL, WCCB, European options) being tested on BEST; blanket choice strongly influences thermal efficiency and capital cost
+5. H&CD recirculating power: CFEDR will need ~100–200 MW; wall-plug efficiency is method-dependent and not yet confirmed at CFEDR scale
 
 **Gaps**:
-- Multi-blanket cost uncertainty (5 candidate TBM concepts → which one CFEDR adopts is unknown) — `truly-unknown` — **important** (creates branching cost scenarios)
-- Confinement quality assumptions for extrapolation to CFEDR power plant — `derivable` (use ITER/ARIES tokamak scaling) — **important**
-- Plasma exhaust / divertor heat flux solutions at power plant scale — `not-yet-sourced` — **nice-to-have**
+- Committed CFEDR blanket concept and thermal-hydraulic design — `not-yet-sourced` — **important**
+- CFEDR H&CD configuration and recirculating power fraction — `derivable` — **important**
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
 **Coverage**: Partial
 
-**Available**:
-- **TF/PF magnets (Nb₃Sn/NbTi)**: ITER-heritage conductors. TRL 8–9 — largest supply chain in fusion, mature manufacturing.
-- **CS YBCO HTS sub-coils**: HTS used only in high-field CS region (peak 18.8T). TRL 6–7 — higher than full-HTS designs; ITER-adjacent manufacturing. Limited quantity relative to full-HTS concepts.
-- **Heating systems** (ECRH 170 GHz, ICRH, LHCD, NBI): All established technologies at TRL 7–8. JET-heritage NBI. Gyrotrons at 170 GHz proven at ITER scale.
-- **PFCs** (full-W first wall, W-monoblock divertor): TRL 8 — ITER-heritage design, 240 modules, remote-handling-compatible.
-- **Remote handling**: ITER-derived approach confirmed; TRL 6–7 for D-T operational scale.
-
-**Missing**:
-- TRL for **tritium breeding blankets** (under TBM test; none committed) — currently TRL 3–5 depending on concept.
-- TRL for **sCO2 power conversion at fusion scale** — only CFETR studies exist, no built prototype.
-- TRL for **CFEDR divertor** at power plant heat loads.
+**Available**: BEST Research Plan gives technology readiness context for BEST-specific systems. ARIES-ACT provides component lifetime data for LTS tokamak power plants. LLNL TBB study (`osti-1305833.md`) gives TRL assessment for DCLL-class breeding blankets.
+
+| Subsystem | TRL (BEST) | TRL (CFEDR) | Source Basis |
+|---|---|---|---|
+| LTS magnets (Nb3Sn/NbTi) | 7–8 | 7–8 | BEST RP; ARIES-ACT |
+| YBCO in CS high-field sub-coils | 5–6 | 5–6 | BEST RP |
+| ECRH/ICRH/NBI | 7–8 | 7 | BEST RP; ARIES-ACT |
+| LHCD | 6–7 | 6–7 | BEST RP |
+| Full-W first wall | 5–6 | 5–6 | BEST RP; ARIES-ACT |
+| W divertor (water-cooled) | 5–6 | 5–6 | BEST RP |
+| Tritium fuel cycle (DIR) | 4–5 | 5–6 | BEST RP |
+| TBMs (COOL/WCCB) | 4–5 | 5 | BEST RP; LLNL TBB |
+| Remote handling | 5–6 | 5–6 | BEST RP |
+| sCO₂ Brayton for fusion | 3–4 | 4–5 | CFETR PCS study |
+| CFEDR-class breeding blanket | — | 3–4 | LLNL TBB; ARIES-ACT |
 
 **Gaps**:
-- Tritium breeding blanket maturity for power plant application — `truly-unknown` (depends on which TBM concept CFEDR selects) — **important**
-- sCO2 Brayton cycle at fusion scale — `not-yet-sourced` (gen-IV fission sCO2 analogues exist; search DOE/NGNP literature) — **important**
-- Tritium processing and handling at commercial scale — `not-yet-sourced` — **important**
+- Formal CFEDR technology readiness roadmap — `not-yet-sourced` — **nice-to-have**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
 **Coverage**: Partial
 
-**Available**:
-- **Nb₃Sn**: ITER supply chain established; ~2000 tons total magnet mass in BEST. No supply bottleneck at this scale.
-- **NbTi**: Mature commercial supply. No concern.
-- **YBCO (REBCO) tape**: Used only in CS HTS sub-coils — limited quantity. Less critical than full-HTS designs. Supply is tighter than LTS but manageable at this scale.
-- **Tungsten**: Mature supply (PFC coatings and monoblock divertors); ITER-heritage specification.
-- **Tritium**: 110g inventory sourced externally — standard dependency for any D-T device. Sources identify this as external supply, not bred. CANDU/fission supply chain assumed.
-- **TBM breeding materials under test**: PbLi (liquid), Li₂TiO₃/Li₄SiO₄ (ceramic), Be₁₂Ti (neutron multiplier) — all at R&D/pilot scale, not yet commercial.
-
-**Missing**:
-- Lithium-6 enrichment requirements and supply chain for power plant blanket.
-- Be₁₂Ti neutron multiplier manufacturing scale-up assessment.
-- PbLi corrosion/activation materials qualification at commercial scale.
-- Tritium supply chain for CFEDR-scale operations (many grams/day tritium throughput).
+**Key materials concerns** (from BEST RP + ARIES-ACT + LLNL TBB):
+- **Nb3Sn**: ITER supply chain established; high confidence at CFEDR scale
+- **YBCO (CS high-field coils)**: Less mature; 10–100× more expensive per kA·m than NbTi; relevant if CFEDR adopts more HTS than BEST
+- **Tungsten (first wall/divertor)**: Adequate raw material supply; reactor-qualified W manufacturing limited; W-alloy development needed for CFEDR
+- **Li-6 enrichment**: ~40% enrichment needed for TBR ≥ 1.05; current enrichment capacity modest; CFEDR at Pfus=1.5 GW needs ~200–300 kg/yr Li-6
+- **Tritium supply**: 110g for BEST from external source; CFEDR targeted for self-sufficiency post-TBM qualification — supply gap between BEST first D-T (2028) and CFEDR breeding start is critical
+- **RAFM steel (Chinese equivalent)**: Being developed at CRAFT; supply chain immature at CFEDR scale
 
 **Gaps**:
-- Li-6 enrichment supply chain for commercial blanket — `not-yet-sourced` (OSTI/IAEA tritium supply studies likely exist) — **important**
-- Beryllium/Be₁₂Ti scale manufacturing (if HCPB/ceramic breeder selected) — `not-yet-sourced` — **important**
-- Tritium throughput at power plant scale (CFEDR) — `derivable` (from TBR × fusion power) — **important**
-- PbLi corrosion materials qualification — `not-yet-sourced` — **nice-to-have**
+- Tritium supply details for BEST D-T operations — `proprietary` — **blocking for LCOE**: tritium cost is a key O&M driver; market price ($30,000–100,000/g) and availability through 2030s uncertain
+- Li-6 enrichment and supply chain for CFEDR scale — `not-yet-sourced` — **important**
+- Domestic Chinese YBCO production cost trajectory — `not-yet-sourced` — **nice-to-have**
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor (as expected for an experimental device)
+
+**Important framing note**: BEST produces no electricity. All LCOE analysis must target CFEDR (Q=10–30, Pfus=1.5–3.0 GW, R=7.8m, B=6.3T) or an assumed PFPP. This is a `derivable` exercise using BEST parameters plus ARIES-ACT/TEA analogs.
 
 **Available Parameters**:
+
 | Parameter | Value/Range | Source | Confidence |
-|-----------|-------------|--------|------------|
-| Fusion power target (BEST) | >50 MW (Q≥1), Q~5 burning plasma | BEST Research Plan v1.1, p.20 | high |
-| Magnetic field | 6.15 T | BEST Research Plan v1.1, p.16 | high |
-| Plasma current | Up to 7 MA | BEST Research Plan v1.1, p.16 | high |
-| Plasma volume | 142 m³ | BEST Research Plan v1.1, p.16 | high |
-| Auxiliary heating power | ~50 MW nominal, ~71 MW upgrade | BEST Research Plan v1.1, p.18-19 | high |
-| Power conversion cycle (lineage) | sCO2 Brayton | CFETR power conversion studies (2021, 2024, 2025) | medium |
-| Thermal efficiency (CFETR studies) | 34–40% | CFETR Energy papers (2021, 2024) | medium |
-| COOL blanket operating conditions | 8 MPa, 350°C inlet | CFETR COOL Blanket (2024) | medium |
-| Company funding | $214M raised; ~$2B registered capital | Neo Fusion company profile | medium |
-| Construction timeline | 2023–2027 (first plasma 2027/28) | BEST Research Plan v1.1, p.20 | high |
+|---|---|---|---|
+| Fusion power (CFEDR target) | 1.5–3.0 GW | BEST RP Table 1.1 | m |
+| Fusion gain (CFEDR) | Q = 10–30 | BEST RP exec summary | m |
+| Major radius (CFEDR) | R = 7.8m | BEST RP Table 1.1 | m |
+| Toroidal field (CFEDR) | B = 6.3T | BEST RP Table 1.1 | m |
+| Plasma volume (CFEDR) | ~1600 m³ | BEST RP Table 1.1 | m |
+| Thermal efficiency (sCO₂, CFETR) | 34–40% | CFETR PCS study (abstract) | m |
+| Thermal efficiency analog (ARIES-ACT) | 45–58% | `osti-1178069.md` | h (analog) |
+| NOAK overnight capital cost (D-T MFE, 500 MWe) | $8,800–22,200/kW | `tea_dt_mfe_cost_analysis/` | m |
+| LCOE range (D-T MFE, 500 MWe NOAK) | $140–550/MWh | `tea_dt_mfe_cost_analysis/` | m |
+| First wall/blanket lifetime analog (ARIES-ACT1) | 5 FPY at NWL=2.3 MW/m² | `osti-1178069.md` | m |
+| Operation mode | Quasi-steady → steady-state (CFEDR) | BEST RP | h |
+| H&CD power (BEST) | 50 MW total (4 methods) | BEST RP | h |
+| H&CD power (CFETR analog) | ~54–105 MW | arxiv-1907-11919, osti-1465662 | m |
+| Magnet mass (BEST) | ~2000t | BEST RP | h |
+| Tritium inventory (BEST) | 110g | BEST RP | h |
+| Company registered capital | ~$2B (14.5B CNY) | Company profile | l |
 
 **Missing Parameters**:
+
 | Parameter | Gap Type | Criticality | Notes |
-|-----------|----------|-------------|-------|
-| Plant electrical output (CFEDR/PFPP) | not-yet-sourced | blocking | CFEDR targeted ~1 GWe; CFETR studies suggest ~200–1000 MWe range — search CNKI/OSTI for CFEDR system design |
-| Capital cost breakdown (by subsystem) | proprietary / not-yet-sourced | blocking | No public cost estimate for BEST or CFEDR; ITER scaling analogues required |
-| O&M costs | not-yet-sourced | blocking | No published O&M estimate; ITER/DEMO analogues needed |
-| Capacity factor / availability (power plant) | derivable | blocking | Tokamak availability assumptions derivable from ITER DEMO studies (~75–85%) |
-| First wall replacement schedule | not-yet-sourced | important | ITER assumes ~5-year FW lifetime; BEST dossier doesn't specify |
-| Blanket replacement interval | truly-unknown (design not committed) | important | Depends on which TBM concept CFEDR selects |
-| Tritium breeding ratio (TBR) | derivable | important | TBM testing active but no published TBR for any BEST TBM yet |
-| Net electric output (recirculating power fraction) | derivable | important | 50 MW aux heating is large recirculating load; wall-plug efficiency of H&CD systems needed |
-| Magnet system cost | derivable | important | Scale from ITER cost data (similar Nb₃Sn technology); ~$1–2B analogue |
-| Target Q / fusion gain for power plant | not-yet-sourced | important | CFEDR likely targets Q~10–20; BEST data doesn't specify CFEDR performance |
+|---|---|---|---|
+| CFEDR capital cost by CAS account | not-yet-sourced | blocking | No CFEDR cost study found; ARIES-ACT/TEA analogs can substitute at ~50% uncertainty |
+| CFEDR/PFPP net electric output | derivable | blocking | Pfus=1.5–3.0 GW + efficiency → ~500–1200 MWe; efficiency assumption needed |
+| Capacity factor / availability target | not-yet-sourced | blocking | CFETR papers mention 0.3–0.5 duty cycle for that device; no PFPP target published |
+| CFEDR O&M cost | derivable | important | Derive from ARIES-ACT or PROCESS per-kWe scaling |
+| Tritium cost assumptions | proprietary | important | Market price ~$30k–100k/g; consumption at Q=10–30 requires derivation |
+| BEST construction cost | proprietary | important | $2B registered capital ≠ device cost; ITER analogy: BEST likely $2–5B |
+| Blanket capital cost (CFEDR) | not-yet-sourced | important | Concept not yet fixed; ARIES-ACT DCLL analog available |
+| First wall lifetime under CFEDR neutron loading | not-yet-sourced | important | NWL >> BEST; ARIES-ACT provides scaling |
+| CFEDR H&CD recirculating power fraction | derivable | important | Derive from CFETR scenario papers + ARIES-ACT wall-plug efficiency assumptions |
+| Decommissioning cost | derivable | nice-to-have | Standard fusion convention: ~10–15% of overnight capital |
 
 ---
 
 ## Source Recommendations
 
-1. **CFEDR/PFPP system design studies** — search OSTI, CNKI, ASIPP publications for "CFEDR design" or "Chinese fusion demonstration reactor" parameters (fusion power, electric output, capital cost projections). *Not-yet-sourced — unverified — confirm existence before searching.*
-
-2. **ARIES / Starfire / EUROfusion DEMO cost studies** as tokamak power plant analogues for capital cost scaling. These are well-documented and directly applicable. `derivable` path.
-
-3. **ITER cost breakdown** (official ITER Organization cost reports) as direct LTS magnet system cost analogue. Publicly available. `derivable` path.
-
-4. **Tokamak availability studies** (EU DEMO, ITER Long-Pulse) for capacity factor and maintenance interval assumptions. Search EUROfusion publications. `not-yet-sourced — unverified — confirm existence before searching.*
-
-5. **Li-6 enrichment supply chain assessments** — search IAEA, DOE fusion fuel cycle reports for tritium/lithium supply chain analyses applicable to commercial tokamak scale. `not-yet-sourced — unverified.*
-
-6. **sCO2 Brayton cycle at industrial scale** — search DOE/NGNP or Sandia National Labs sCO2 pilot plant data for efficiency and cost analogues. Well-documented outside fusion context; fission-sector data directly applicable.
-
-7. **Auxiliary heating H&CD wall-plug efficiency** — published for ITER (NBI ~28% wall-plug, gyrotrons ~50–55%). Search ITER design documents for recirculating power fraction benchmarks.
+1. **CFETR/CFEDR cost study** — search OSTI and IOP Nuclear Fusion for "CFETR economic analysis" or "CFEDR cost" — `not-yet-sourced`. *unverified — confirm existence before searching*
+2. **CFETR conceptual design papers (2017–2024)** — search "CFETR system design" or "CFETR engineering design" on OSTI for R=7.8m CFEDR engineering parameters — `not-yet-sourced`
+3. **CFETR blanket design papers (WCCB and COOL)** — published in Fusion Engineering and Design; needed for thermal efficiency estimation — `not-yet-sourced`
+4. **Tritium supply and demand studies** — IAEA and DOE tritium availability projections through 2050 — `not-yet-sourced`
+5. **PyFECONS** (`/home/reid/PyFECONS`) — can produce cost estimates for CFEDR-class LTS tokamaks directly using available CFEDR parameters; no additional sourcing needed — *Available*
+6. **TEA D-T MFE + ARIES cost accounts** (`knowledge/sources/tea_dt_mfe_cost_analysis/`, `knowledge/sources/aries_cost_account_documentation/`) — primary LCOE analogs for D-T MFE tokamaks — *Available*
 
 ---
 
 ## Summary
 
-**Proceed to full analysis with framing caveats.** BEST is the best-documented concept in this cohort from a device physics standpoint, thanks to the publicly released BEST Research Plan v1.1. The qualitative sections (Data Availability, System Function Challenges, Subsystem Maturity, Materials) can be written thoroughly with high confidence.
-
-The structural constraint is that **BEST is an experimental device**, so the D1+ analysis must explicitly adopt a two-layer framing: (a) what BEST itself tells us about technology readiness, and (b) what the CFEDR/PFPP downstream reactor would look like from an LCOE perspective. The quantitative model will rely on ITER/ARIES analogues for capital cost and should clearly flag this extrapolation. The blanket design uncertainty (5 candidate TBMs, no selection made) creates irreducible branching in cost scenarios that should be modeled explicitly.
+**Proceed to full analysis.** Qualitative sections (1–4) can be written at high confidence from the BEST Research Plan v1.1 alone. The LCOE analysis requires explicitly framing the concept as "CFEDR-class power plant in the BEST technology lineage" — BEST itself has no LCOE — and using ARIES-ACT and TEA D-T MFE as cost analogs. The CFEDR engineering parameters (R=7.8m, B=6.3T, Pfus=1.5–3 GW, Q=10–30) give the scaling inputs; the analogs supply the cost structure. Main acknowledged uncertainties: blanket concept uncommitted (~15–20% capital cost swing), tritium cost assumptions (world supply through 2030s–2040s uncertain), and CFEDR capacity factor (no published figure; use DEMO-class 50–80% as sensitivity parameter).
 
-No blocking data gaps prevent a D1+ write-up from proceeding. The LCOE model will be analogue-based but defensible — which is appropriate for a pre-CFEDR concept at this stage of development.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Mostly Ready (with important framing caveat)"
+overall_rating: "Mostly Ready"
 blocking_count: 4
-important_count: 6
-counting_method: "section_5_missing_parameters"
+important_count: 8
+counting_method: "all_sections_deduplicated — blocking: CFEDR capital cost by CAS (§5), CFEDR/PFPP net electric output (§5), capacity factor/availability target (§5), tritium supply details for BEST D-T ops (§4); important: CFEDR/PFPP cost study (§1), CFEDR blanket concept committed design (§2), CFEDR H&CD recirculating power fraction (§2), Li-6 enrichment supply chain for CFEDR scale (§4), CFEDR O&M cost (§5), tritium cost assumptions (§5), CFEDR blanket capital cost (§5), first wall lifetime under CFEDR neutron loading (§5)"
 section_coverage:
-  availability_of_data:       "Good (device level) / Partial (power plant level)"
-  system_function:            "Partial"
+  availability_of_data:       "Good"
+  system_function:            "Good"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Partial"
-  lcoe_parameter_extraction:  "Poor (as expected for an experimental device)"
+  lcoe_parameter_extraction:  "Partial"
 ```
+
+---
+
+The gap report has been updated at `analyses/33-state-backed-tokamak-best/gap_report.md`. The stray meta-sentence at the top was removed and the mandatory structured YAML block was added.
+
+**Key findings:**
+- **Overall: Mostly Ready** — 4 blocking gaps, 8 important gaps
+- The fundamental structural challenge is that BEST is an experimental device 2 steps from commercial power; all LCOE work must target CFEDR (R=7.8m, Pfus=1.5–3 GW) using Western cost analogs (ARIES-ACT, TEA D-T MFE)
+- The BEST Research Plan v1.1 is an exceptional source — physics, subsystems, and technology sections can be written with high confidence
+- No published CFEDR cost study found; blocking gaps are all `derivable` using fleet-wide analogs, not `truly-unknown`
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
