# Diff: 28-hts-tokamak-full-hts

**Generated:** 2026-05-22T11:06:34-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 5 | 6 | 1 |
| important_count  | 5 | 9 | - |
| overall_rating   | Significant Gaps | Significant Gaps | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
10:**Summary**: Energy Singularity has produced meaningful prototype-level engineering data (HH70 commissioning, Jingtian magnet) and enough trajectory information to characterize their technology approach, but the company has published essentially nothing about power plant economics, blanket design, energy conversion, or LCOE-relevant parameters. The HH380 demo plant — the only machine where these questions become concrete — is post-2030 with no disclosed specifications. Fleet-wide D-T MFE cost analogs (TEA D-T MFE, ARIES, PyFECONS) can partially substitute for many plant-level parameters, but the full-HTS magnet cost premium over LTS is a novel, poorly-bounded variable with no direct published analog.
28:- Fleet-wide D-T MFE cost methodology applicable as analog: `knowledge/sources/tea_dt_mfe_cost_analysis/`, `knowledge/sources/aries_cost_account_documentation/`, PyFECONS
129:| D-T MFE plant capital cost structure (CAS analog) | CAS 20–27 breakdowns | `knowledge/sources/tea_dt_mfe_cost_analysis/` | medium (analog only) |
159:5. **Fleet-wide TEA D-T MFE source** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — already registered; directly applicable for BOP, O&M, decommissioning, and thermal conversion cost structure as tokamak analog. Read this before attempting LCOE estimation — it will supply most of the plant-level CAS accounts that Energy Singularity hasn't disclosed.
```

## Blocking-tier lines (baseline)

```
31:- HH380 engineering specs — `proprietary` + `truly-unknown` (not yet designed) — **blocking** for power-plant-specific LCOE
77:- Blanket TRL and design approach — `truly-unknown` (company stage) — **blocking** for completeness; manageable via CFETR/ITER blanket analogues for the write-up
127:| Plant net electrical output (HH380 MW_e) | truly-unknown | blocking | No HH380 specs; use SPARC/ARC analogue |
128:| Capital cost by CAS component | truly-unknown | blocking | No published cost data; derive from SPARC ARC study scaled to HH170/HH380 geometry |
129:| REBCO tape cost ($/kA-m or $/m) | not-yet-sourced | blocking | CFS/MIT ARC study has estimates; AMSC published pricing |
130:| Thermal cycle type and efficiency | proprietary/truly-unknown | blocking | Infer as standard Rankine or sCO2; no ES data |
131:| Capacity factor / availability | truly-unknown | blocking | No published target; use 80–90% analogue from tokamak literature |
```

## Blocking-tier lines (new)

```
37:- HH170/HH380 engineering design documents — `proprietary` — **blocking** for concept-specific analysis
38:- Published techno-economic study or LCOE projection from Energy Singularity — `proprietary` — **blocking**
61:- Tritium breeding blanket design — `proprietary` (and not yet designed) — **blocking** for full system function analysis
84:- Blanket/TBR subsystem TRL — `proprietary` + concept not yet designed — **blocking** for full maturity picture
108:- REBCO tape cost at production scale ($/kA·m or $/m) — `not-yet-sourced` (published HTS tape cost literature exists, e.g., SuperPower/Fujikura pricing studies) — **blocking** for magnet capital cost
135:| Net electrical output (MWe) | proprietary | blocking | HH380 has no published specs; CFS ARC (~200 MWe) is the closest published analog for compact HTS tokamak |
136:| Capital cost by CAS account | proprietary | blocking | No plant study published; fleet analog (ARIES, TEA D-T MFE) applies but misses full-HTS magnet premium |
137:| Full-HTS magnet capital cost premium vs. LTS | not-yet-sourced | blocking | Key differentiator for this concept; published academic cost models exist (Whyte et al., SPARC cost papers) but not captured |
138:| Thermal conversion efficiency | proprietary | blocking | No energy cycle disclosed; generic Rankine or supercritical CO2 could be assumed from fleet analogs |
139:| Capacity factor / availability | proprietary | blocking | Steady-state operation is an advantage; no plant-level estimate published |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/28-hts-tokamak-full-hts.md	2026-05-22 09:21:13.876101453 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/28-hts-tokamak-full-hts/gap_report.md	2026-05-22 11:06:34.146649010 -0700
@@ -1,9 +1,13 @@
-# Gap Assessment: HTS Tokamak - Full HTS
+Now I have enough context to write the gap assessment. The second ScienceDirect source (licensing framework paper) is completely irrelevant to this concept — it's about fusion regulation policy globally. Let me compose the report.
+
+---
+
+# Gap Assessment: HTS Tokamak - Full HTS (D-T)
 
 ## Overall Readiness
 **Rating**: Significant Gaps
 
-**Summary**: Energy Singularity has a well-documented prototype (HH70) and magnet demonstration (Jingtian) with strong media coverage, but almost no engineering data relevant to a power plant. The company is at a very early stage — HH380 (the demo power plant) is post-2030 and has zero published specifications. The qualitative write-up is achievable with significant use of analogues and inference, but the quantitative LCOE model will rely heavily on SPARC/ARC scaling rather than any Energy Singularity-specific data.
+**Summary**: Energy Singularity has produced meaningful prototype-level engineering data (HH70 commissioning, Jingtian magnet) and enough trajectory information to characterize their technology approach, but the company has published essentially nothing about power plant economics, blanket design, energy conversion, or LCOE-relevant parameters. The HH380 demo plant — the only machine where these questions become concrete — is post-2030 with no disclosed specifications. Fleet-wide D-T MFE cost analogs (TEA D-T MFE, ARIES, PyFECONS) can partially substitute for many plant-level parameters, but the full-HTS magnet cost premium over LTS is a novel, poorly-bounded variable with no direct published analog.
 
 ---
 
@@ -13,25 +17,27 @@
 **Coverage**: Partial
 
 **Available**:
-- HH70 prototype parameters (major/minor radius, magnet specs, coil count, field strength, plasma records) — well-documented across multiple media sources and FusionEnergyBase
-- Jingtian magnet: 21.7–22.4 T peak field, dimensions, winding pack details, published in IEEE TAS 2025
-- HH170 roadmap: Q > 10 target, ~14 T on-axis, ~70% SPARC volume, 25 T magnet target, 2027 completion
-- Company funding: ~$110M raised, seeking $500M for HH170
-- Construction timeline: HH70 built in under 2 years, >96% domestic component sourcing
-- Two paywalled ScienceDirect papers covering HH70 commissioning and magnet system construction (not accessed)
+- Company profile, funding status (~$110M raised for HH70, seeking $500M for HH170), investor base, and 3-machine roadmap — `iter-01/sources/energy-singularity-overview.md`
+- HH70 engineering specs: major radius (0.7 m), minor radius (0.25–0.3 m), B0 = 0.6 T, Bmax = 2.5 T, 20 K operating temperature, 26 REBCO coils (12 TF + 6 PF + 8 CS), conductor dimensions — `iter-03/sources/sciencedirect-science-article-pii-s092037962500537x.md` (abstract) and `iter-01`
+- Jingtian prototype magnet: 21.7–22.4 T peak field, dimensions (~3 m × 1.4 m, ~7.5 T), 32 single-pancake REBCO coils, operating current 24,300 A — `iter-01`
+- HH70 plasma performance record (1,337 s steady-state, shot #5,755, Feb 2026) — `iter-02/sources/energy-singularity-technical-summary.md` (Xinhua article)
+- HH170 top-level targets: Q > 10, ~25 T peak coil field, ~70% of SPARC volume, completion target 2027 — `iter-01`
+- HH380 existence and timeline (post-2030 demo plant) — `iter-01`
+- Domestic supply chain: >96% localization, Shanghai Superconductor as REBCO supplier — `iter-01`
+- AI-based plasma control as a differentiating engineering feature — `iter-02` (Xinhua)
+- Fleet-wide D-T MFE cost methodology applicable as analog: `knowledge/sources/tea_dt_mfe_cost_analysis/`, `knowledge/sources/aries_cost_account_documentation/`, PyFECONS
 
 **Missing**:
-- HH380 power plant: zero public engineering specifications
-- Thermal/power conversion system design
-- Blanket design and tritium breeding approach
-- Detailed plasma parameters (temperature, density, confinement time)
-- Detailed heating systems for HH170
+- HH170 engineering specifications beyond top-level targets (heating systems, power density, plasma parameters)
+- HH380 any engineering details whatsoever
+- No company-published techno-economic analysis or cost projections
+- The fourth iter-03 ScienceDirect source (pii-s2211467x) is about fusion licensing/regulation globally — zero content relevant to Energy Singularity or this concept
 
 **Gaps**:
-- HH380 engineering specs — `proprietary` + `truly-unknown` (not yet designed) — **blocking** for power-plant-specific LCOE
-- Paywalled HH70 commissioning paper (Fusion Engineering and Design, 2025) — `not-yet-sourced` — **important** (may contain plasma parameters and heating details not in media coverage)
-- Paywalled HH70 magnet paper (Superconductivity, 2024) — `not-yet-sourced` — **important** (likely has detailed magnet cost-relevant manufacturing data)
-- Chinese-language technical publications beyond media — `not-yet-sourced` — **nice-to-have**
+- HH170/HH380 engineering design documents — `proprietary` — **blocking** for concept-specific analysis
+- Published techno-economic study or LCOE projection from Energy Singularity — `proprietary` — **blocking**
+- Full text of HH70 commissioning paper (paywalled; would give complete engineering specs) — `not-yet-sourced` — **important**
+- Full text of Jingtian IEEE TAS paper (2025; magnet cost/manufacturing data) — `not-yet-sourced` — **important**
 
 ---
 
@@ -39,21 +45,23 @@
 **Coverage**: Partial
 
 **Available**:
-- The full-HTS differentiator is well-understood: all TF, PF, and CS coils are REBCO, which is unique among public tokamak programs
-- AI-based plasma control system noted; 100 shots/day vs. 20–30/day at JET suggests operational efficiency
-- Steady-state operation demonstrated at prototype scale (1,337 s)
-- "D-T equivalent" Q > 10 framing for HH170 suggests the machine may not actually burn D-T — this complicates the cost model baseline
+- All-REBCO coil architecture (TF + PF + CS) is documented and understood as the key differentiator — `iter-01`
+- Steady-state operation demonstrated on prototype; AI plasma control confirmed — `iter-01`, `iter-02`
+- ICRF as primary heating on HH70 confirmed — `iter-01`
+- The physics challenges of full HTS at high field (quench management, joint resistance, coil mechanics) are documentable from general HTS tokamak literature, though no Energy Singularity-specific paper covers HH170 design choices
 
 **Missing**:
-- No cost analogues for all-REBCO coil sets at power-plant scale (HTS-only is genuinely novel)
-- Physics basis for Q > 10 claim is not publicly detailed — no published confinement scaling analysis
-- Whether HH170 actually burns D-T or achieves "D-T equivalent" via other means is ambiguous
-- No published system-level integration analysis connecting magnet field → plasma gain → electrical output
+- Heating and current drive strategy for HH170 and HH380 (ECCD? NBI? higher-power ICRF?) — essential for plasma performance and recirculating power fraction
+- Divertor design and plasma-facing component strategy — particularly challenging at high B-field
+- Tritium breeding approach — completely undisclosed across 3 iterations and 20+ sources; structurally unresolvable until HH380 design phase
+- Neutron shielding / blanket integration design
+- Recirculating power fraction estimate (affects net electrical output significantly)
 
 **Gaps**:
-- HTS coil cost scaling law for full-HTS vs. hybrid HTS designs — `not-yet-sourced` — **important** (CFS/SPARC literature has some REBCO cost modeling that could be adapted)
-- Q claim validation / physics basis — `not-yet-sourced` — **important** (SPARC/ARC physics papers could provide analogue; Energy Singularity-specific basis not published)
-- "D-T equivalent" operating mode clarification — `proprietary` — **important** (affects fuel cycle and neutron load assumptions)
+- Tritium breeding blanket design — `proprietary` (and not yet designed) — **blocking** for full system function analysis
+- Heating/CD strategy for power plant — `proprietary` — **important**
+- Divertor/PFC design — `proprietary` — **important**
+- Recirculating power fraction — `derivable` (can estimate from compact tokamak analogs like SPARC/ARC) — **important**
 
 ---
 
@@ -61,47 +69,46 @@
 **Coverage**: Partial
 
 **Available**:
-- **HTS magnets (TF)**: TRL ~5–6. Jingtian demonstrated 21.7 T at sub-coil scale; HH170 TF coil design in progress. Published IEEE TAS paper.
-- **HTS magnets (PF/CS)**: TRL ~4–5. HH70 prototype demonstrated full coil set at low field (0.6–1 T). High-field CS is less demonstrated.
-- **Plasma control system**: TRL ~6. AI-based system demonstrated on HH70 with 5,755 shots and long-pulse capability.
-- **ICRF heating**: TRL ~7. Standard technology, demonstrated on HH70. Scale-up for HH170 unclear.
+- Full-HTS magnet set (TF+PF+CS): TRL 6 demonstrated on HH70; Jingtian magnet demonstrates HH170-class fields at TRL 5–6 — `iter-01`
+- AI plasma control: TRL 5–6 (demonstrated in >5,700 shots on HH70, including 1,337 s hold) — `iter-02`
+- REBCO tape manufacturing (domestic via Shanghai Superconductor): TRL 7–8 at pilot scale — `iter-01`
+- HH70 overall machine integration: TRL 6 (demonstrated operation) — `iter-03` abstract
 
 **Missing**:
-- **Blanket / tritium breeding system**: TRL 1 (not yet conceptually designed at Energy Singularity)
-- **First wall / plasma-facing components**: TRL unknown — no public information
-- **Energy conversion / balance of plant**: TRL unknown — not disclosed
-- **Vacuum vessel at HH380 scale**: TRL unknown
-- **Tritium handling and processing systems**: TRL unknown
+- TRL assessment for blanket/tritium breeding subsystem (not designed yet — effectively TRL 1–2 for this company's specific concept)
+- TRL for energy conversion system (not disclosed; generic D-T thermal cycle)
+- TRL for HH170 heating/CD systems beyond ICRF prototype capability
+- Tritium handling and processing systems (no disclosure at any stage)
 
 **Gaps**:
-- Blanket TRL and design approach — `truly-unknown` (company stage) — **blocking** for completeness; manageable via CFETR/ITER blanket analogues for the write-up
-- First wall material and replacement schedule — `not-yet-sourced` — **important** (tungsten PFC experience from ITER/EAST applicable; search OSTI/FDS for compact tokamak PFC studies)
-- Balance of plant TRL — `not-yet-sourced` — **important** (use generic D-T steam cycle as analogue)
+- Blanket/TBR subsystem TRL — `proprietary` + concept not yet designed — **blocking** for full maturity picture
+- Tritium processing/handling TRL — `truly-unknown` at Energy Singularity level — **important**
+- Divertor/PFC maturity — `not-yet-sourced` (general tokamak literature can inform) — **important**
+- HH380 power conversion system TRL — `proprietary` — **important**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Partial
+**Coverage**: Poor
 
 **Available**:
-- REBCO tape is the dominant material; supplier is Shanghai Superconductor (domestic)
-- >96% domestic component localization confirmed — significant China supply chain concentration
-- HH70 TF coil uses 450 m of HTS conductor per coil, ~480 μm total conductor thickness
-- REBCO = Rare Earth Barium Copper Oxide → rare earth supply dependency (yttrium, barium)
-- China has dominant global rare earth production position
+- REBCO tape: domestic supplier (Shanghai Superconductor) confirmed; >96% localization rate — `iter-01`
+- Tape geometry: 12 mm wide, 10 mm REBCO core, ~230 µm tape, ~480 µm conductor — `iter-01`
+- Scale of conductor use for HH70: ~450 m HTS conductor per TF coil × 12 = ~5,400 m for TF coils alone — calculable from `iter-01`
+- HH170 Jingtian-class magnets will require substantially more conductor (dimensions ~3 m × 1.4 m vs HH70 TF coil 2.015 m × 1.03 m); no tape quantity estimate published
 
 **Missing**:
-- REBCO tape production capacity at power-plant scale (how many km of tape for HH380?)
-- Cost per meter of REBCO tape (Energy Singularity-specific — likely negotiated proprietary pricing)
-- Manufacturing capacity for 25 T D-shaped magnets at the required quantity for a power plant
-- Tritium supply chain (standard D-T issue, not Energy Singularity-specific)
-- Any Li-6 enrichment details for eventual blanket
+- Global REBCO tape supply capacity and cost trajectory — no source covers this for the HH380 scale
+- Lithium-6 supply (for tritium breeding) — not discussed anywhere in concept sources
+- Beryllium, tungsten, or other PFC/blanket-specific materials — not discussed (no blanket design)
+- Conductor quantity estimate for HH170 or HH380 magnets
+- Manufacturing cost per kA·m of REBCO at production scale
 
 **Gaps**:
-- REBCO tape cost and supply chain capacity — `not-yet-sourced` — **important** (SuperPower, Fujikura, AMSC published capacity data; CFS ARC study has REBCO cost estimates that could be adapted; search "REBCO tape manufacturing scale" and "HTS cost projections 2030")
-- HH380 magnet tape requirements (total conductor length) — `derivable` from HH70 scaling — **important**
-- Rare earth supply chain concentration risk quantification — `not-yet-sourced` — **nice-to-have** (USGS critical materials reports)
-- Li-6 isotope enrichment supply — `not-yet-sourced` — **nice-to-have** (generic D-T blanket literature)
+- REBCO tape cost at production scale ($/kA·m or $/m) — `not-yet-sourced` (published HTS tape cost literature exists, e.g., SuperPower/Fujikura pricing studies) — **blocking** for magnet capital cost
+- HH170/HH380 conductor quantity estimate — `derivable` (from magnet geometry scaling, but geometry not yet public) — **important**
+- Li-6 enrichment supply chain — `not-yet-sourced` — **important**
+- Blanket materials (W, Be, structural steel, LiPb) — `truly-unknown` (no blanket design exists) — **important**
 
 ---
 
@@ -109,77 +116,69 @@
 **Coverage**: Poor
 
 **Available Parameters**:
+
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Fusion gain target (Q) | >10 (HH170 target) | dossier / iter-01 | m |
-| Machine size (HH170) | ~70% SPARC volume, ~14 T on-axis | dossier / iter-02 | m |
-| Magnet peak field (HH170) | 25 T (target) | dossier | m |
-| Magnet peak field (demonstrated) | 21.7–22.4 T (Jingtian) | dossier | h |
-| Operation mode | Steady-state | dossier | h |
-| Commercialization target | Before 2035 | iter-01 | l |
-| HH170 funding | ~$500M sought | iter-01 | m |
-| HH70 funding | ~$110M raised | iter-01 | m |
-| Domestic supply chain | >96% | iter-02 | h |
+| Q target (HH170) | Q > 10 | `iter-01` (company claim) | medium |
+| Plant timeline | HH380 post-2030; commercialization <2035 | `iter-01` | low (aspirational) |
+| Magnet field (HH170) | ~25 T peak (HTS coils) | `iter-01` | medium |
+| Device volume (HH170) | ~70% of SPARC | `iter-01` | medium |
+| Confinement approach | Steady-state tokamak | dossier | high |
+| Fuel | D-T | dossier | high |
+| Domestic localization | >96% (HH70) | `iter-01` | medium |
+| D-T MFE plant capital cost structure (CAS analog) | CAS 20–27 breakdowns | `knowledge/sources/tea_dt_mfe_cost_analysis/` | medium (analog only) |
 
 **Missing Parameters**:
+
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Plant net electrical output (HH380 MW_e) | truly-unknown | blocking | No HH380 specs; use SPARC/ARC analogue |
-| Capital cost by CAS component | truly-unknown | blocking | No published cost data; derive from SPARC ARC study scaled to HH170/HH380 geometry |
-| REBCO tape cost ($/kA-m or $/m) | not-yet-sourced | blocking | CFS/MIT ARC study has estimates; AMSC published pricing |
-| Thermal cycle type and efficiency | proprietary/truly-unknown | blocking | Infer as standard Rankine or sCO2; no ES data |
-| Capacity factor / availability | truly-unknown | blocking | No published target; use 80–90% analogue from tokamak literature |
-| Blanket design / TBR | truly-unknown | important | Not yet designed; CFETR/DEMO analogue |
-| First wall replacement schedule | not-yet-sourced | important | ITER/EAST/compact tokamak literature |
-| Heating power requirement (HH380) | not-yet-sourced | important | Derive from Q target and gain framing |
-| Operating cost breakdown | truly-unknown | important | No ES data; generic tokamak O&M analogue |
-| Tritium cost and consumption | derivable | important | Standard D-T fuel cycle; derive from Q and P_fusion |
-| Plant construction time | truly-unknown | nice-to-have | HH70 built in <2 years — not directly extrapolatable |
+| Net electrical output (MWe) | proprietary | blocking | HH380 has no published specs; CFS ARC (~200 MWe) is the closest published analog for compact HTS tokamak |
+| Capital cost by CAS account | proprietary | blocking | No plant study published; fleet analog (ARIES, TEA D-T MFE) applies but misses full-HTS magnet premium |
+| Full-HTS magnet capital cost premium vs. LTS | not-yet-sourced | blocking | Key differentiator for this concept; published academic cost models exist (Whyte et al., SPARC cost papers) but not captured |
+| Thermal conversion efficiency | proprietary | blocking | No energy cycle disclosed; generic Rankine or supercritical CO2 could be assumed from fleet analogs |
+| Capacity factor / availability | proprietary | blocking | Steady-state operation is an advantage; no plant-level estimate published |
+| O&M costs ($/MWh) | derivable | important | Can scale from D-T MFE analogs (TEA D-T MFE source) |
+| Recirculating power fraction | derivable | important | Can estimate from compact tokamak physics (heating, cryogenics at 20 K) |
+| Fuel cycle costs (tritium, D2 supply) | derivable | important | Standard D-T fuel cost is well-characterized in fleet analogs |
+| Decommissioning cost | derivable | important | Standard MFE analog applicable |
+| HTS tape cost contribution to magnet CAPEX | not-yet-sourced | important | Requires REBCO $/kA·m × conductor quantity estimate |
+| Construction time / interest during construction | proprietary | important | HH70 built in 2 years; HH380 unknown |
 
 ---
 
 ## Source Recommendations
 
-1. **CFS/MIT ARC plant study** — for capital cost scaling, REBCO tape quantities, and balance-of-plant design by CAS category. Search: "ARC tokamak plant study Freidberg" or "SPARC cost model". `not-yet-sourced` — confirm existence before searching; ARC papers are published and accessible via OSTI.
-   
-2. **ScienceDirect HH70 commissioning paper** (doi:10.1016/j.fusengdes.2025.115341) — may contain plasma parameters, heating system details, and magnet cost-relevant data not in public media. `not-yet-sourced` — known to exist, paywalled; access via institutional library or Sci-Hub equivalent.
+1. **CFS/SPARC/ARC published literature** — compact HTS tokamak with disclosed parameters (major radius, magnet specs, Q target, power output). Most direct structural analog for cost estimation. `not-yet-sourced` — search SPARC physics basis papers (Journal of Plasma Physics, 2020) and ARC concept design papers. **Unverified — confirm existence before searching.**
 
-3. **ScienceDirect HH70 magnet paper** (doi:10.1016/j.supcon.2024.100119) — likely has detailed REBCO conductor specifications and manufacturing data relevant to cost scaling. `not-yet-sourced` — known to exist, paywalled.
+2. **REBCO tape cost scaling studies** — published academic papers on $/kA·m vs. production volume for YBCO/REBCO tapes (SuperPower, SuNAM, Fujikura). Key input for HTS magnet capital cost. `not-yet-sourced` — search IEEE TAS, Superconductor Science and Technology journals. **Unverified — confirm existence before searching.**
 
-4. **IEEE TAS Jingtian paper** (2025) — cited in IAEA World Fusion Outlook; may contain detailed magnet fabrication and cost data. `not-yet-sourced` — confirm via IEEE Xplore search for "Jingtian" or "Energy Singularity".
+3. **HH70 commissioning paper full text** — `knowledge/concept_research/28-hts-tokamak-full-hts/iter-03/` has abstract only (doi:10.1016/j.fusengdes.2025.115341). Full text would provide complete engineering specs, subsystem list, and potentially cost/schedule data. `not-yet-sourced` — institutional access or Sci-Hub.
 
-5. **REBCO tape cost projections** — search OSTI for "REBCO tape cost manufacturing scale 2030" or "HTS tape cost learning curve". SuperPower and AMSC have published some cost roadmap data. `not-yet-sourced` — `unverified — confirm existence before searching`.
+4. **Jingtian magnet IEEE TAS paper (2025)** — would provide manufacturing data, conductor quantity, coil engineering details useful for magnet cost estimation. `not-yet-sourced` — search IEEE Xplore for "Jingtian" or "Energy Singularity" + "IEEE Transactions on Applied Superconductivity."
 
-6. **CFETR plant study** — China's domestic fusion program has published blanket and balance-of-plant studies that represent a likely analogue for what Energy Singularity would eventually adopt. Search "CFETR plant study WCCB blanket LCOE". `not-yet-sourced` — `unverified — confirm existence before searching`.
+5. **Fleet-wide TEA D-T MFE source** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — already registered; directly applicable for BOP, O&M, decommissioning, and thermal conversion cost structure as tokamak analog. Read this before attempting LCOE estimation — it will supply most of the plant-level CAS accounts that Energy Singularity hasn't disclosed.
 
-7. **Compact tokamak PFC and first wall studies** — search OSTI/IAEA for "compact tokamak first wall replacement schedule" or "ST40 PFC tungsten". `not-yet-sourced` — `unverified — confirm existence before searching`.
+6. **ARIES-ACT or ARIES-AT design study** — advanced tokamak with high-field, steady-state operation closest to HH380 concept. Would provide CAS-level cost breakdowns for compact, steady-state MFE. `not-yet-sourced` — search ARIES project reports or ARIES Cost Account Documentation already registered.
 
 ---
 
 ## Summary
 
-**Proceed to full analysis with explicit analogue strategy.** The qualitative sections (data availability, system function challenges, subsystem maturity, supply chain) are well-supported by what's available — Energy Singularity's prototype work and magnet demonstrations give enough to write a substantive narrative. The key challenge is that this is an early-stage Chinese private company with limited public disclosure, and HH380 (the relevant power plant) is fully undisclosed.
+**Proceed to full analysis with explicit use of fleet-wide analogs.** The concept-specific data is sufficient for qualitative characterization (technology approach, maturity trajectory, key differentiators) and partial quantitative analysis (magnet field, device sizing, Q target). For LCOE estimation, the analysis will need to lean heavily on fleet-wide D-T MFE cost analogs and make explicit the key unknown: the cost premium of a full-HTS magnet system (all coils REBCO) over conventional LTS or partial-HTS designs. Acquiring the HH70 full commissioning paper and a compact HTS tokamak cost study (CFS/ARC analog) before writing the analysis would materially improve confidence. The tritium breeding gap is structurally unresolvable until HH380 design phase (post-2030) and should be flagged as an assumed-standard D-T blanket for analysis purposes.
 
-For the quantitative LCOE model, proceed by:
-1. Using SPARC/ARC as the primary cost analogue (similar field strength, compact tokamak geometry, HTS magnets)
-2. Scaling capital cost estimates to HH170/HH380 geometry (~70% SPARC volume)
-3. Applying standard D-T fuel cycle assumptions (blanket, tritium handling) as placeholder
-4. Using generic Rankine or sCO2 thermal cycle assumptions for energy conversion
-5. Flagging all analogue-derived values explicitly — Energy Singularity has published essentially no cost data
-
-The two paywalled ScienceDirect papers are the highest-value unexplored sources and should be accessed if possible before the quantitative model is finalized, as they may contain plasma parameters and magnet manufacturing details that improve the cost basis beyond generic analogues.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Significant Gaps"
-blocking_count: 5
-important_count: 5
-counting_method: "section_5_missing_parameters"
+blocking_count: 6
+important_count: 9
+counting_method: "section_5_missing_parameters_plus_sections_1_to_4_blocking_gaps_deduplicated; section 5 blocking: net electrical output, capital cost by CAS, full-HTS magnet cost premium, thermal conversion efficiency, capacity factor; sections 1-4 added: blanket/TBR design"
 section_coverage:
   availability_of_data:       "Partial"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
-  materials_supply_chain:     "Partial"
+  materials_supply_chain:     "Poor"
   lcoe_parameter_extraction:  "Poor"
-```
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
