# Diff: 20b-renaissance-stellarator

**Generated:** 2026-05-22T10:41:55-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 4 | 4 | 0 |
| important_count  | 7 | 8 | - |
| overall_rating   | Mostly Ready (with one critical extraction gap) | Mostly Ready | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
45:- Helios design (`knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`) provides a comparable HTS stellarator BOP as a cost analog — different geometry (8m vs. 4m, 6T vs. 10T) but same confinement family and energy conversion approach.
159:3. **Use Helios stellarator (Thea Energy, `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`) as BOP cost analog** — a preconceptual stellarator plant design with comparable architecture (HTS, steady-state, D-T, planar modular coils). Note: Helios is 8m / 6T vs. Renaissance's 4m / 10T — different compactness regime but same confinement family and BOP structure. 88% capacity factor with biennial maintenance (84 days) is the best available stellarator-specific capacity factor assumption.
161:4. **Use TEA D-T MFE source (`knowledge/sources/tea_dt_mfe_cost_analysis/`) for CAS indirect costs and O&M structure** — provides tokamak-based CAS breakdown applicable to MFE BOP costs. Note this is tokamak-centric; stellarator-specific differences (no current drive, no disruptions, different coil geometry) should be flagged as deviations.
```

## Blocking-tier lines (baseline)

```
31:- Full NF 2024 paper content not extracted — `not-yet-sourced` — **blocking** (high probability of containing capital cost parameters and design trade-off data not in the dossier)
53:- Magnet manufacturing cost model for laser-patterned HTS film — `truly-unknown` — **blocking** (no analogous manufacturing process exists at scale; must use engineering estimate or REBCO tape area analogy)
77:- Laser-patterning HTS for complex 3D stellarator coil geometry (beyond Helmholtz) — `proprietary` — **blocking** (the Helmholtz demo doesn't prove the full stellarator field can be produced this way; company likely has additional internal results)
100:- REBCO film deposition capacity / supply chain (novel process — not tape winding) — `truly-unknown` — **blocking** (no analogue manufacturing process at scale; this is a first-of-kind manufacturing challenge)
133:| Capital cost by subsystem (CAS 20–70) | not-yet-sourced / proprietary | blocking | NF 2024 "economically optimized" title suggests some cost content — extract first |
134:| Magnet system capital cost | truly-unknown | blocking | Novel film deposition process has no existing cost model; REBCO tape cost analogues apply only partially |
135:| Liquid metal wall system cost | truly-unknown | blocking | No commercial analogues at this scale or field strength |
136:| Total plant overnight cost ($/kWe) | proprietary | blocking | No published figure |
```

## Blocking-tier lines (new)

```
33:- Primary design paper not extracted — `not-yet-sourced` — **blocking** (this is the key quantitative source)
54:- MHD/flow dynamics of the liquid metal wall under high magnetic field — `truly-unknown` at engineering prototype scale — **blocking** (controls wall heat removal reliability and replacement frequency, which dominates O&M cost)
78:- Laser-patterned HTS manufacturing at stellarator scale — `proprietary` / `truly-unknown` — **blocking** (dominant cost driver with no published data)
139:| Capital cost by subsystem (magnet, blanket, BOP) | proprietary + not-yet-sourced | blocking | NF 2024 design paper likely has economic optimization; not extracted |
140:| Magnet cost (laser-patterned HTS film) | proprietary | blocking | Novel manufacturing; no published unit cost data anywhere |
141:| First wall / blanket replacement schedule and cost | truly-unknown | blocking | No engineering prototype; replacement frequency drives O&M |
142:| O&M cost estimate | not-yet-sourced | blocking | No concept-specific O&M data; need analogue from HELIAS/ARIES-CS |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/20b-renaissance-stellarator.md	2026-05-22 09:21:13.865231782 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20b-renaissance-stellarator/gap_report.md	2026-05-22 10:41:55.932336263 -0700
@@ -1,36 +1,38 @@
-Now I have sufficient information to write the gap assessment. No extracted source documents are in the repo — only the dossier summary exists. Let me produce the report.
+I now have enough information to write the full gap assessment. Let me compile the analysis.
 
 ---
 
-# Gap Assessment: Compact Liquid-Wall HTS Stellarator
+# Gap Assessment: Renaissance Stellarator (D-T)
 
 ## Overall Readiness
-**Rating**: Mostly Ready (with one critical extraction gap)
-**Summary**: Renaissance Fusion has published three peer-reviewed papers covering the core design point, blanket/neutron management, and power conversion — an unusually strong publication record for a private fusion company. The dossier captures all 12 schema columns at high confidence, and technical parameters supporting an LCOE model (efficiency, geometry, power output, wall loading) are available in outline. The principal gap is that none of the primary sources have been extracted into the knowledge base, meaning the analysis must work from the dossier summaries rather than the full technical content. The Nuclear Fusion 2024 paper is titled "economically optimized design point" and almost certainly contains cost-relevant data not captured in the dossier — this is the most important single source to retrieve.
+**Rating**: Mostly Ready
+
+**Summary**: Renaissance Fusion has published three peer-reviewed papers (2023–2024) directly on this concept's blanket, power conversion, and design point optimization. The dossier is well-populated with high-confidence entries on all 12 Phase 1a columns. The primary blocking gap is that the main design paper (Prost & Volpe, *Nuclear Fusion* 64, 2024 — "Economically optimized design point") is cited throughout the dossier but was **not extracted** in Phase 1a; it almost certainly contains the capital cost optimization and LCOE-relevant parameter sweeps that are absent from all extracted sources. A qualitative D1 write-up is fully supportable now; the quantitative LCOE model will need either that paper or explicit analogue-based substitution with acknowledged uncertainty.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Moderate-to-Good (strong publications, no full plant study, sources not yet extracted)
+**Coverage**: Moderate
 
 **Available**:
-- *Nuclear Fusion 64 (2024) 026007*: Peer-reviewed design point paper. Covers geometry (A~4, R≤4 m), magnet design (10 T nominal, 15 T at coil, 20–40 T peak at coil surface), fuel (D-T at 10 keV), heating (NNBI, 60% neutralization efficiency), and claims to present an "economically optimized design point" — implying cost trade-off content that the dossier does not fully capture.
-- *J. Nuclear Materials 599 (2024) 155239*: Peer-reviewed blanket paper. Covers liquid Li-LiH wall architecture (15 cm Pb + 18 cm Li-LiH), 25 MW/m² wall loading, fm=1.24 neutron energy multiplication, 99.99% neutron energy absorption, and full radial build (wall + 50 cm VH₂ + 1.3 m concrete bioshield).
-- *Energy Conversion and Management 276 (2023) 116572*: Peer-reviewed power conversion paper. Covers sCO2 Brayton-Rankine combined cycle optimized via genetic algorithm, 49–51% cycle efficiency, 34% net plant efficiency.
-- Company website and MT29 abstract: Confirms 6 T peak Helmholtz magnet demo at 1.2 m diameter and 20 K; steady-state operation; 1 GWe target.
-- UC Berkeley seminar: Additional context on HTS magnet approach and liquid metal wall.
+- *J. Nuclear Materials* 599 (2024) 155239 — fully extracted: blanket neutronics, radial build, TBR=1.60, energy multiplication fm=1.07, 80% availability assumption, 32 FPY lifetime, VCrTi vacuum vessel. This is the most data-rich extracted source.
+- *Energy Conversion and Management* 276 (2023) 116572 — cited in dossier with values (49-51% cycle efficiency, 34% net plant efficiency), but not extracted; values are available secondhand.
+- Dossier summary entries for all 12 Phase 1a columns, all rated high confidence.
+- Company website, UC Berkeley seminar transcript, MT29 conference abstract — accessible but not formally extracted.
+- REBCO critical current scaling paper (arxiv-1512-01930) — only the abstract page was captured; no relevant Renaissance Fusion design data.
+- PROCESS stellarator documentation (UKAEA) — methodology reference for generic stellarator systems codes, not concept-specific.
 
 **Missing**:
-- Full extracted content of the three primary papers — the dossier captures select values but not full parameter tables, sensitivity analyses, or cost breakdowns that likely exist in the papers.
-- No published full-system plant study (comparable to ARIES-CS, HELIAS-5B, or similar stellarator power plant design studies).
-- No techno-economic report or white paper with explicit cost estimates.
+- *Nuclear Fusion* 64 (2024) 026007 (Prost & Volpe) — the PRIMARY design paper ("Economically optimized design point"), which defines the operating point, systems model, and economic optimization. Cited everywhere in the dossier but **not extracted**.
+- *Energy Conversion and Management* 276 (2023) — power conversion paper, not extracted.
+- Any published cost estimate or capital cost breakdown for the concept.
 
 **Gaps**:
-- Full NF 2024 paper content not extracted — `not-yet-sourced` — **blocking** (high probability of containing capital cost parameters and design trade-off data not in the dossier)
-- Full JNM 2024 and ECM 2023 paper content not extracted — `not-yet-sourced` — **important** (may contain component-level cost assumptions)
-- No plant study equivalent — `truly-unknown` / `proprietary` — **important** (company is pre-pilot; no full BOP system integration study is public)
+- Primary design paper not extracted — `not-yet-sourced` — **blocking** (this is the key quantitative source)
+- Power conversion paper not extracted — `not-yet-sourced` — **important** (values available from dossier but no direct access for deeper parameters)
+- No published capital cost data in any extracted source — `proprietary` + `not-yet-sourced` — **blocking for LCOE**
 
 ---
 
@@ -38,22 +40,21 @@
 **Coverage**: Partial
 
 **Available**:
-- The integrated liquid metal wall eliminates the blanket/shield/first-wall cost boundary — the JNM paper gives structural parameters (wall loading, radial build, neutron multiplication) sufficient to begin estimating the "wall system" cost as a single account.
-- The sCO2 cycle paper provides efficiency data (34% net plant) and a specific cycle architecture (combined Brayton-Rankine) — enabling BOP cost analogy to industrial sCO2 demonstrators.
-- Ignition (Q = ∞) target is explicit — eliminates recirculating power fraction as a variable but introduces large physics uncertainty on whether the plasma actually ignites.
-- The NNBI startup heating requirement is specified (60% neutralization efficiency) — bounded startup energy cost.
+- Blanket paper provides detailed neutronics basis for the integrated liquid-metal wall function — confirms 90% nuclear heat extraction in liquid metal, radial build constraints, HTS coil protection requirements.
+- PROCESS stellarator docs describe confinement scaling laws (ISS04) and available modeling methodology, which sets the framework for physics extrapolation.
+- Helios design (`knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`) provides a comparable HTS stellarator BOP as a cost analog — different geometry (8m vs. 4m, 6T vs. 10T) but same confinement family and energy conversion approach.
 
 **Missing**:
-- Laser-patterned REBCO film deposition: no published cost model or manufacturing yield data for this process. This is the most novel manufacturing step and has no direct cost analogue.
-- Plasma confinement quality at operating parameters: QI optimization for compact (A~4) stellarators is not as mature as W7-X (A~10). Confinement scaling from W7-X to A~4 at 10 T is uncertain.
-- Ignition threshold assumptions: the design claims Q = ∞ but the stability and confinement assumptions underpinning that claim are not independently validated.
-- Liquid metal flow dynamics and magnetohydrodynamic (MHD) effects at 25 MW/m² and 10 T: no experimental validation at relevant scale.
+- No MHD analysis of liquid metal flow at 700-900°C under 10+ T field — the magnetohydrodynamic coupling between the flowing Li-LiH wall and the stellarator magnetic field is an open engineering challenge that will dominate wall reliability and replacement rates.
+- No divertor design or exhaust heat analysis in any extracted source — the liquid metal wall is described, but how divertor heat exhaust is handled in a compact stellarator geometry is unaddressed.
+- No validated confinement result at reactor-relevant parameters for QI stellarators — ISS04 extrapolation to ignition conditions at these plasma parameters (A~4, R~4m, B~10T) spans several orders of magnitude beyond experimental data.
+- Ignition physics basis is an extrapolation, not a validated operating regime — the Q=∞ target is ambitious enough to constitute a structural modeling challenge.
 
 **Gaps**:
-- Magnet manufacturing cost model for laser-patterned HTS film — `truly-unknown` — **blocking** (no analogous manufacturing process exists at scale; must use engineering estimate or REBCO tape area analogy)
-- Confinement quality / energy confinement time at operating parameters — `proprietary` (company internal codes) — **important** (affects recirculating power and Q assumptions)
-- MHD compatibility of liquid Li-LiH flow at fusion-relevant field strength and wall loading — `not-yet-sourced` — **important** (search: Liquid metal MHD in high-field stellarators, Muon Catalyzed Fusion literature, ENEA/KIT liquid metal blanket MHD studies)
-- Ignition margin sensitivity — `not-yet-sourced` — **important** (the NF 2024 paper likely addresses this; extraction needed)
+- MHD/flow dynamics of the liquid metal wall under high magnetic field — `truly-unknown` at engineering prototype scale — **blocking** (controls wall heat removal reliability and replacement frequency, which dominates O&M cost)
+- Divertor design and power exhaust — `not-yet-sourced` — **important**
+- Confinement validation at target parameters — `truly-unknown` experimentally, `derivable` from ISS04 scaling with wide uncertainty bands — **important**
+- Q=∞ ignition physics in compact QI stellarator — `truly-unknown` — **important** (propagates large uncertainty into fusion power output and capacity factor)
 
 ---
 
@@ -61,124 +62,127 @@
 **Coverage**: Partial
 
 **Available**:
-- **HTS Magnet Demonstration**: 6 T peak Helmholtz magnet at 1.2 m diameter, 20 K — directly confirms the laser-patterned HTS film approach works at lab scale (MT29 abstract, UC Berkeley seminar). TRL ~3–4.
-- **sCO2 Power Cycle**: Industrial-scale sCO2 Brayton demonstrators exist (e.g., Echogen, NET Power, Sandia). The fusion-specific combined Brayton-Rankine is novel but the underlying cycle TRL is ~5–6. Integration with a liquid metal heat source is undemonstrated.
-- **Stellarator QI physics**: W7-X at IPP Greifswald demonstrates quasi-isodynamic optimization works at full scale. However, W7-X has A~10 vs. A~4 for Renaissance, and is LTS at lower field — significant extrapolation.
-- **Liquid metal wall concept**: Conceptually studied in fusion context (NSTX liquid lithium divertor experiments, ORNL, KIT), but not at Renaissance's claimed 25 MW/m² wall loading or 10 T field environment.
-
-**Missing**:
-- No published TRL assessment from the company or independent review.
-- No prototype-scale demonstration of laser-patterned HTS film producing a 3D stellarator field (beyond the single Helmholtz demo).
-- No flowing liquid metal wall demonstration at fusion-relevant parameters.
-- Vacuum vessel and structural systems at compact stellarator geometry: not discussed in available sources.
-- Remote handling systems: not addressed (though liquid metal wall reduces activation of surrounding structure).
+- **Magnets**: Demonstrated 6T peak Helmholtz magnet at 1.2m diameter and 20K (dossier, MT29 abstract). This validates the laser-patterning deposition concept at a single-coil scale. Target: 10-15T at coil in a 3D stellarator geometry.
+- **Blanket/neutronics**: 1D cylindrical neutronics model fully published (blanket paper). TBR, energy multiplication, shielding performance all analyzed. Li-LiH + Pb pebble configuration selected.
+- **Power conversion**: sCO2 Brayton-Rankine cycles exist industrially (TRL ~6-7 for the thermodynamic cycle); the specific integration with liquid metal at 700-900°C as a heat source is not demonstrated (TRL ~3-4 for this application).
+- **NNBI heating**: NNBI systems are developed technology at ITER scale (TRL ~6), used only for startup in this ignited design.
+
+**Missing / Low Maturity**:
+- **Laser-patterned HTS film deposition at stellarator scale**: Novel manufacturing method. Single-coil demo at 6T exists; multi-coil 3D stellarator field at 10-15T has not been demonstrated. No published manufacturing cost data. TRL ~3-4.
+- **Flowing liquid metal first wall**: Concept-level engineering (1D neutronics), no engineering prototype. MHD stability, pebble suspension dynamics, tritium extraction from liquid metal, vacuum compatibility — all open. TRL ~2-3.
+- **VCrTi vacuum vessel**: Low-activation structural alloy, limited industrial base. No large-scale demonstration in a fusion-relevant environment. TRL ~3.
+- **Plasma at target parameters**: W7-X is the most advanced QI-like stellarator but operates at much lower fields and temperatures. Ignition-class QI stellarator plasma is TRL ~1-2.
+- **Tritium handling system**: Standard D-T fusion challenge. No concept-specific tritium system design published.
 
 **Gaps**:
-- Laser-patterning HTS for complex 3D stellarator coil geometry (beyond Helmholtz) — `proprietary` — **blocking** (the Helmholtz demo doesn't prove the full stellarator field can be produced this way; company likely has additional internal results)
-- Liquid metal wall at operating conditions (25 MW/m², 10 T, steady-state flow) — `not-yet-sourced` — **important** (search: NSTX-U liquid metal PFC results, KIT HCLL/DCLL MHD experiments, ORNL Li wall programs — `unverified — confirm existence before searching`)
-- Integrated plasma-facing first wall endurance / replacement schedule — `truly-unknown` — **important** (liquid metal walls self-renewing in principle but pump/containment lifetime is unaddressed)
-- Balance-of-plant integration TRL — `not-yet-sourced` — **nice-to-have**
+- Laser-patterned HTS manufacturing at stellarator scale — `proprietary` / `truly-unknown` — **blocking** (dominant cost driver with no published data)
+- Flowing liquid metal wall engineering prototype — `truly-unknown` — **important**
+- Tritium extraction from Li-LiH liquid metal — `not-yet-sourced` — **important**
+- Divertor engineering — `not-yet-sourced` — **important**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Poor
+**Coverage**: Partial
 
 **Available**:
-- REBCO HTS tape is identified as the magnet material (from NF 2024 dossier). REBCO tape supply is a known bottleneck for all HTS fusion programs.
-- Liquid Li-LiH is identified as the wall/blanket material (from JNM 2024). Li-6 enrichment is an established but capacity-constrained supply chain.
-- Pb pebbles for neutron multiplication (from JNM 2024) — Pb is abundant with no supply concerns.
+- **REBCO tape supply**: Blanket paper cites multiple manufacturers (American Superconductor, Bruker, Fujikura, SuNAM, SuperOx, SuperPower) in the REBCO scaling paper (arxiv-1512-01930). Commercial tape supply is growing.
+- **Li6 enrichment**: Blanket paper explicitly discusses enrichment as a cost trade-off: "using Li 6 enriched Li-LiH could lead to a further minor reduction in total breeding blanket thickness albeit at substantially higher cost due to the costly process of Li6 enrichment." Giegerich et al. (Fusion Eng. Des. 149, 2019) is cited for Li6 supply chain — not extracted.
+- **Pb pebbles**: Industrial supply relatively accessible; blanket paper identifies Pb as the preferred multiplier over Be (safety), W, Mo (cost).
+- **Tritium**: Standard D-T fusion supply chain concern; well-characterized.
 
 **Missing**:
-- No REBCO tape quantity estimate (meters of tape per machine) in the dossier — this is the critical supply chain figure for HTS magnets. However, the Renaissance approach uses deposited film, not wound tape — the manufacturing process is entirely different and the relevant bottleneck is film deposition equipment, not tape supply.
-- Li-6 enrichment demand: the 15 cm + 18 cm liquid Li-LiH wall at 1 GWe requires a quantity estimate — not in the dossier.
-- No discussion of tritium inventory requirements during startup (the global civilian supply is ~25 kg; startup inventory demand could be significant).
-- No discussion of supply chain for laser deposition equipment at scale.
-- No discussion of Pb pebble bed manufacturing and replacement logistics.
+- No published cost estimate for bulk REBCO film deposition (vs. tape winding) at stellarator scale — the manufacturing process is novel and proprietary.
+- Li6 enrichment supply chain analysis not extracted (Giegerich et al. referenced but not ingested).
+- No VCrTi alloy supply chain analysis.
+- Helium supply for the 20K cryogenic system — reduced vs. LTS but still a strategic supply risk.
+- No pebble (SiC-encapsulated Pb) manufacturing supply chain analysis — a novel component.
 
 **Gaps**:
-- REBCO film deposition capacity / supply chain (novel process — not tape winding) — `truly-unknown` — **blocking** (no analogue manufacturing process at scale; this is a first-of-kind manufacturing challenge)
-- Startup tritium inventory requirement — `derivable` (from plasma volume, density, burn fraction estimates) — **important**
-- Li-6 enrichment capacity for full-scale deployment — `not-yet-sourced` — **important** (search: ORNL Li-6 production assessments, DOE tritium supply studies — `unverified — confirm existence before searching`)
-- Laser film deposition equipment supply chain — `proprietary` — **nice-to-have**
+- REBCO film deposition manufacturing supply chain and cost — `proprietary` — **important**
+- Li6 enrichment supply capacity and cost — `not-yet-sourced` (Giegerich et al.) — **important**
+- SiC-encapsulated Pb pebble manufacturing at scale — `truly-unknown` — **nice-to-have**
+- VCrTi alloy supply — `not-yet-sourced` — **nice-to-have**
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Partial — performance and efficiency parameters available; capital and operating cost data largely absent
+**Coverage**: Partial
 
 **Available Parameters**:
+
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Net electrical output | 1 GWe | NF 2024 (dossier) | high |
-| Thermal-to-electric cycle efficiency | 49–51% | ECM 2023 (dossier) | high |
-| Net plant efficiency | 34% | ECM 2023 (dossier) | high |
-| Power conversion cycle type | sCO2 Brayton-Rankine combined | ECM 2023 (dossier) | high |
-| Plasma gain (Q) | ∞ (ignition target) | NF 2024 (dossier) | high |
-| Major radius | ≤4 m | NF 2024 (dossier) | high |
-| Aspect ratio | ~4 | NF 2024 (dossier) | high |
-| Toroidal field (nominal) | 10 T | NF 2024 (dossier) | high |
-| Peak coil field | 15 T (coil), 20–40 T (peak) | NF 2024 (dossier) | high |
-| Wall loading | 25 MW/m² | JNM 2024 (dossier) | high |
-| Neutron energy multiplication | fm = 1.24 | JNM 2024 (dossier) | high |
-| Neutron energy absorption | 99.99% | JNM 2024 (dossier) | high |
-| Radial build (blanket+shield) | 15 cm Pb + 18 cm Li-LiH + 50 cm VH₂ + 1.3 m concrete | JNM 2024 (dossier) | high |
-| Operation mode | Steady-state (~100% duty cycle) | Company website (dossier) | high |
-| Startup heating | NNBI, 60% neutralization efficiency | NF 2024 (dossier) | high |
-| Magnet operating temperature | 20 K | MT29/Berkeley (dossier) | high |
+| Fusion power | ~2 GW | Blanket paper (Table 1) | high |
+| Net electric output | 1 GWe | Blanket paper, dossier | high |
+| Plant thermal efficiency (cycle) | 49–51% | Dossier (citing Fama 2023) | medium |
+| Net plant efficiency | 34% | Dossier (citing Fama 2023) | medium |
+| Plant availability / capacity factor | 80% | Blanket paper (32 FPY / 40 yr) | medium |
+| Major radius | 3.8 m | Blanket paper Table 1 | high |
+| Aspect ratio | 4.1 | Blanket paper Table 1 | high |
+| On-axis magnetic field | 10.2 T | Blanket paper Table 1 | high |
+| Peak field at coil | ~15 T (up to 20-40 T in design paper) | Dossier | medium |
+| Energy multiplication in blanket | fm = 1.07 (case study), fm = 1.24 (dossier) | Blanket paper / dossier | medium |
+| TBR (1D model) | 1.60 | Blanket paper | medium (1D only) |
+| Radial build (plasma to HTS) | 91 cm total | Blanket paper | high |
+| Operating lifetime | 40 years (32 FPY) | Blanket paper | high |
+| Fuel | D-T | All sources | high |
+| Operation mode | Steady-state | Dossier | high |
+| Energy conversion type | sCO2 Brayton-Rankine combined cycle | Dossier | high |
+| Plasma target | Q = ∞ (ignited) | Dossier, NF 2024 | high |
+| Blanket coolant outlet temperature | 700–900°C | Blanket paper | high |
 
 **Missing Parameters**:
+
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Capital cost by subsystem (CAS 20–70) | not-yet-sourced / proprietary | blocking | NF 2024 "economically optimized" title suggests some cost content — extract first |
-| Magnet system capital cost | truly-unknown | blocking | Novel film deposition process has no existing cost model; REBCO tape cost analogues apply only partially |
-| Liquid metal wall system cost | truly-unknown | blocking | No commercial analogues at this scale or field strength |
-| Total plant overnight cost ($/kWe) | proprietary | blocking | No published figure |
-| Operating & maintenance cost ($/MWh or $/yr) | proprietary | important | Steady-state operation is an advantage but no data |
-| Component replacement schedule and cost | truly-unknown | important | Liquid metal wall self-renewing in principle; pump/plumbing lifetime unknown |
-| Availability / capacity factor target | not-yet-sourced | important | Company claims "near-100%" — need uncertainty bounds; NF 2024 may address |
-| Startup tritium inventory requirement | derivable | important | Can be estimated from plasma parameters |
-| Tritium breeding ratio (TBR exact value) | not-yet-sourced | important | Dossier notes fm=1.24 confirmed but TBR ~1.60 unverified; JNM 2024 full paper may clarify |
-| Recirculating power fraction | derivable | important | At Q=∞ (ignition), recirculating power dominated by magnets + pumps, not heating — need magnet power estimate |
-| Plant lifetime assumption | not-yet-sourced | important | Standard assumption 30–40 yr; design-specific limits from neutron damage or liquid metal corrosion not available |
-| Balance of plant cost (non-power-conversion) | not-yet-sourced | nice-to-have | sCO2 BOP has some industrial cost data; fusion integration adds cost |
-| Contingency and financing assumptions | truly-unknown | nice-to-have | No public project finance analysis |
+| Capital cost by subsystem (magnet, blanket, BOP) | proprietary + not-yet-sourced | blocking | NF 2024 design paper likely has economic optimization; not extracted |
+| Magnet cost (laser-patterned HTS film) | proprietary | blocking | Novel manufacturing; no published unit cost data anywhere |
+| First wall / blanket replacement schedule and cost | truly-unknown | blocking | No engineering prototype; replacement frequency drives O&M |
+| O&M cost estimate | not-yet-sourced | blocking | No concept-specific O&M data; need analogue from HELIAS/ARIES-CS |
+| Tritium inventory requirement and startup cost | derivable | important | Can be estimated from TBR=1.60 and burn rate; no published value |
+| Capacity factor (detailed basis) | derivable | important | 80% availability asserted but no maintenance schedule justifying it |
+| Divertor heat load and replacement cost | not-yet-sourced | important | Not addressed in any extracted source |
+| Recirculating power fraction | not-yet-sourced | important | Needed for net electrical output; only net output stated, not breakdown |
+| NNBI system capital cost (startup heating) | derivable | nice-to-have | ITER NNBI analogue can be used; only startup use lowers cost impact |
+| Decommissioning cost | derivable | nice-to-have | Standard analogue applicable |
+| Li6 enrichment level and cost | not-yet-sourced | nice-to-have | Blanket paper notes this is optional but cost-impactful |
 
 ---
 
 ## Source Recommendations
 
-1. **Extract NF 2024 paper in full** (`not-yet-sourced`, blocking) — Nuclear Fusion 64 (2024) 026007. The "economically optimized design point" title strongly suggests capital cost estimates, design trade-off curves, and sensitivity parameters not captured in the dossier. This is the single highest-priority extraction.
+1. **Extract the main design paper (Prost & Volpe, *Nuclear Fusion* 64, 2024, doi:10.1088/1741-4326/ad142e)** — `not-yet-sourced`. This is the "Economically optimized design point" paper cited across all dossier entries; it almost certainly contains the systems model, parameter optimization, and economic analysis that are the primary missing inputs for LCOE modeling. This is the single highest-priority action before full quantitative modeling.
 
-2. **Extract JNM 2024 paper in full** (`not-yet-sourced`, important) — J. Nuclear Materials 599 (2024) 155239. The radial build and wall loading data in the dossier are summarized; the full paper likely contains detailed neutronics, thermal-hydraulic calculations, and breeding performance that feed blanket cost estimation.
+2. **Extract the power conversion paper (Fama et al., *Energy Conversion and Management* 276, 2023, doi:10.1016/j.enconman.2022.116572)** — `not-yet-sourced`. Provides detailed sCO2 combined cycle efficiency data at the specific operating conditions. Values are available from the dossier summary, but the paper will have efficiency vs. temperature trade-off data needed for sensitivity analysis.
 
-3. **Extract ECM 2023 paper in full** (`not-yet-sourced`, important) — Energy Conversion and Management 276 (2023) 116572. The 34% net efficiency is noted but the optimization paper likely contains component-level heat exchanger sizing, turbine specifications, and auxiliary power estimates.
+3. **Use Helios stellarator (Thea Energy, `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`) as BOP cost analog** — a preconceptual stellarator plant design with comparable architecture (HTS, steady-state, D-T, planar modular coils). Note: Helios is 8m / 6T vs. Renaissance's 4m / 10T — different compactness regime but same confinement family and BOP structure. 88% capacity factor with biennial maintenance (84 days) is the best available stellarator-specific capacity factor assumption.
 
-4. **Search for stellarator power plant studies with cost breakdowns** (`not-yet-sourced`, important) — e.g., HELIAS-5B (IPP/KIT), ARIES-CS (UCSD), MHH2, or similar stellarator plant studies that provide CAS-format cost structures. These provide the closest cost analogues even if geometry and magnet technology differ. Suggest search: OSTI.gov "stellarator power plant cost" or "HELIAS LCOE" — `unverified — confirm existence before searching`.
+4. **Use TEA D-T MFE source (`knowledge/sources/tea_dt_mfe_cost_analysis/`) for CAS indirect costs and O&M structure** — provides tokamak-based CAS breakdown applicable to MFE BOP costs. Note this is tokamak-centric; stellarator-specific differences (no current drive, no disruptions, different coil geometry) should be flagged as deviations.
 
-5. **Search for liquid metal wall cost/performance studies in fusion context** (`not-yet-sourced`, important) — KIT, ORNL, or CNL publications on flowing liquid lithium walls, particularly MHD pressure drop calculations at high field which affect pumping power and cost. Suggest search: OSTI.gov "flowing liquid lithium wall fusion MHD" — `unverified — confirm existence before searching`.
+5. **Search OSTI for HELIAS 5-B power plant cost analysis** (search: "HELIAS 5-B cost" or "stellarator power plant systems code PROCESS cost") — `unverified — confirm existence before searching`. HELIAS 5-B is the canonical large stellarator power plant study modeled in PROCESS; it may have CAS-level cost breakdowns applicable as an analogue for stellarator-specific systems costs.
 
-6. **Search for REBCO film deposition manufacturing cost studies** (`not-yet-sourced`, nice-to-have) — laser ablation deposition of REBCO on large-area substrates is an active research topic in superconductor manufacturing (separate from tape manufacturing). Any published cost-per-m² data would be valuable. Suggest search: "PLD REBCO large area deposition cost" or "REBCO thin film coated conductor cost" — `unverified — confirm existence before searching`.
+6. **Search for Li6 enrichment supply chain and cost data** — recommend: Giegerich et al., *Fusion Engineering and Design* 149 (2019) 111339, cited in the blanket paper. `not-yet-sourced`.
 
 ---
 
 ## Summary
 
-**Proceed to full analysis, with the NF 2024 paper extracted first.**
+**Proceed to full analysis with one priority action first**: extract the Prost & Volpe *Nuclear Fusion* 2024 design paper before beginning quantitative LCOE modeling. The qualitative write-up (Section D1 sections 1–4) is fully supportable from existing sources — the physics basis, blanket design, and power conversion approach are documented in peer-reviewed literature with unusual clarity for a private fusion startup. The concept is harder to model than most due to three novel co-innovations (laser-patterned HTS, liquid metal wall, compact ignited stellarator), none of which have industrial cost analogues, but the physics and engineering rationale is documented well enough to characterize the uncertainty bands. The quantitative LCOE model will be analogue-heavy and uncertainty-wide without the primary design paper, but can be constructed with stated assumptions using Helios and ARIES-CS stellarator analogues for magnet and BOP costs.
 
-The available data is sufficient for a solid qualitative write-up (D1 sections 1–3) and a partial quantitative LCOE model. The performance parameters (1 GWe, 34% net efficiency, steady-state, ~100% capacity factor) provide the denominator for LCOE and the physical framing for the cost model. The novel subsystems (laser-patterned HTS film, liquid metal wall) have no direct cost analogues — the analysis should use bounding estimates with explicit uncertainty ranges rather than precise cost figures. The "economically optimized design point" framing in the NF 2024 paper title is the strongest signal that capital cost data exists in the primary literature and has not been captured. Extracting that paper before writing the analysis is the highest-leverage action available.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Mostly Ready (with one critical extraction gap)"
+overall_rating: "Mostly Ready"
 blocking_count: 4
-important_count: 7
-counting_method: "section_5_missing_parameters"
+important_count: 8
+counting_method: "section_5_missing_parameters_plus_sections_1_to_4_blocking_gaps_deduplicated: primary design paper not extracted (blocking, section 1+5), magnet cost unavailable (blocking, section 3+5), O&M cost unavailable (blocking, section 5), wall replacement schedule unknown (blocking, section 2+5)"
 section_coverage:
-  availability_of_data:       "Moderate-to-Good (strong publications, no full plant study, sources not yet extracted)"
+  availability_of_data:       "Partial"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
-  materials_supply_chain:     "Poor"
-  lcoe_parameter_extraction:  "Partial — performance and efficiency parameters available; capital and operating cost data largely absent"
-```
+  materials_supply_chain:     "Partial"
+  lcoe_parameter_extraction:  "Partial"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
